"""Owned cross-dialect service measurements, separate from HTTP and certification."""
import argparse, asyncio, json, os, time
from contextvars import ContextVar
from datetime import date
from pathlib import Path
from sqlalchemy import event, inspect, text, select, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database import Base
from app.authority import Authority
from app.models.task import Task
from app.models.iteration import Iteration
from app.models.agent import AgentRun
from app.services.task_detail_service import TaskDetailService
from app.services.task_service import TaskService
from app.services.project_service import ProjectService
from app.services.delivery_metrics_service import DeliveryMetricsService
from app.services.capacity_service import CapacityService
from app.query_limits import CollectionLimitExceededError
from tests.support.delivery import seed_delivery_scenario
from tests.support.database import assert_safe_test_database_url
from scripts.load.local_baseline import summarize
from scripts.load.common import atomic_write_json
from scripts.load.source_binding import source_binding, verify_binding


def validate_declaration(declaration):
    if (declaration.get('concurrency') != [1, 5, 10]
            or type(declaration.get('rounds')) is not int or declaration['rounds'] < 1
            or declaration.get('datasets', {}).get('actual_task_count') != 3009):
        raise ValueError('Declare 3009 service tasks, concurrency 1/5/10 and positive rounds')


async def run(url, declaration):
    validate_declaration(declaration)
    binding = source_binding()
    assert_safe_test_database_url(url)
    engine=create_async_engine(url,pool_size=10,max_overflow=5) if url.startswith("postgresql") else create_async_engine(url)
    queries = ContextVar('measurement_queries', default=None)
    captured = []
    @event.listens_for(engine.sync_engine, 'before_cursor_execute')
    def before_query(conn, cursor, statement, parameters, context, executemany):
        context.measurement_started = time.perf_counter()
    @event.listens_for(engine.sync_engine, 'after_cursor_execute')
    def after_query(conn, cursor, statement, parameters, context, executemany):
        rows = queries.get()
        if rows is not None:
            rows.append((statement, parameters, (time.perf_counter() - context.measurement_started) * 1000))
    try:
        async with engine.begin() as conn:
            if await conn.run_sync(lambda c: inspect(c).get_table_names()):
                raise ValueError('Service measurement requires a fresh empty owned database')
            await conn.run_sync(Base.metadata.create_all)
        factory=async_sessionmaker(engine,expire_on_commit=False)
        async with factory() as db:
            scenario=await seed_delivery_scenario(db)
            db.add(Iteration(id=3,name="Bounded local sample",calendar_id=1,project_id=1,start_date=date(2026,1,1),end_date=date(2026,1,20)))
            await db.flush()
            db.add_all([Task(title=f"Large {i}",project_id=1,iteration_id=1,owner_profile_id=1) for i in range(2501)])
            rows=[Task(title=f"Bounded {i}",project_id=1,iteration_id=3,owner_profile_id=1,status=("planned","active","resolved")[i%3]) for i in range(500)]
            db.add_all(rows);await db.flush();db.add(AgentRun(task_id=rows[0].id,actor_id=1,status="running"));await db.commit()
            actual_tasks=await db.scalar(select(func.count()).select_from(Task))
        samples=[]
        for concurrency in declaration["concurrency"]:
            async def client(index):
                for _ in range(declaration["rounds"]):
                    async with factory() as db:
                        db.info["authority"]=Authority(None,"human",profile_id=1,projects={1:"viewer"})
                        operations=[("task_page",lambda:TaskDetailService(db).lookup(iteration_id=1,limit=100)),
                            ("scope_summary",lambda:ProjectService(db).get_summary(1)),
                            ("shared_capacity",lambda:CapacityService(db).projection(1,date(2026,1,1),date(2026,2,1))),
                            ("delivery_recovery",lambda:DeliveryMetricsService(db).report(iteration_id=3)),
                            ("graph_bound",lambda:TaskService(db).get_by_iteration(1))]
                        for label,operation in operations:
                            before=time.perf_counter();status=200;code=None
                            sql_rows = []; token = queries.set(sql_rows)
                            try:
                                result=await operation()
                                count=len(result.items) if hasattr(result,"items") and isinstance(result.items,list) else len(result) if isinstance(result,list) else 1
                            except CollectionLimitExceededError:
                                status=413;code="collection_limit_exceeded";count=0
                            finally:
                                queries.reset(token)
                            if label == 'scope_summary' and concurrency == 1 and not captured:
                                captured.extend(sql_rows)
                            samples.append(dict(profile="service_reads_v1",client_kind="synthetic_service_authority",concurrency=concurrency,client=index,
                                path=label,status=status,code=code,latency_ms=(time.perf_counter()-before)*1000,response_bytes=0,response_cardinality=count,
                                query_count=len(sql_rows), query_ms=sum(row[2] for row in sql_rows)))
            await asyncio.gather(*(client(i) for i in range(concurrency)))
        plans = []
        if engine.dialect.name == 'postgresql':
            async with engine.connect() as conn:
                for statement, parameters, elapsed in captured:
                    if statement.lstrip().upper().startswith(('SELECT', 'WITH')):
                        rows = await conn.exec_driver_sql('EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ' + statement, parameters)
                        plans.append({'sql': statement, 'parameters': json.loads(json.dumps(parameters, default=str)), 'observed_query_ms': elapsed,
                                      'plan': rows.scalar()})
                configuration = dict((await conn.execute(text('SELECT name, setting FROM pg_settings WHERE name IN '
                    "('server_version','shared_buffers','work_mem','max_connections','effective_cache_size')"))).all())
        else:
            configuration = {'dialect': engine.dialect.name}
        # Actual rollback followed by an independent session read.
        async with factory() as db:
            task=await db.get(Task,scenario.tasks["planned"]);title=task.title;task.title="Uncommitted contention probe";await db.flush();await db.rollback()
        async with factory() as db:rollback=(await db.get(Task,scenario.tasks["planned"])).title==title
        raw=dict(nonce=declaration["fixture"],fixture="synthetic-owned",real_provider_pilot=False,samples=samples,
            resilience=dict(transaction_rollback_verified=rollback),
            environment=dict(database_dialect=engine.dialect.name,identity_basis="synthetic_service_authority_not_HTTP_authentication",
                resource_scope="owned disposable database",response_bytes_basis="not_measured_for_direct_service_calls",rollback_verified=rollback))
        result=summarize(raw,declaration)
        if actual_tasks != 3009:
            raise ValueError('Seeded task count differs from frozen workload')
        result['raw_observations'] = raw
        result['query_plans'] = plans
        result['database_configuration'] = configuration
        result['source_binding'] = {'before': binding, 'after': verify_binding(binding)}
        result["datasets"]={"actual_task_count":actual_tasks,"large_iteration_tasks":2501,"bounded_iteration_tasks":500,"initial_seed_tasks":8}
        return result
    finally:await engine.dispose()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database-url",required=True);parser.add_argument("--declaration",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True);args=parser.parse_args()
    if args.output.exists():parser.error("Output already exists")
    result=asyncio.run(run(args.database_url,json.loads(args.declaration.read_text())))
    atomic_write_json(args.output,result);print(result["status"])
    return 0 if result["status"]=="passed" else 1


if __name__=="__main__":raise SystemExit(main())
