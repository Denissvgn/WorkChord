"""Disposable protocol peer: each invocation uses a new process and connection."""

import asyncio
import json
import os
import sys

from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.commands import command_transaction
from app.schemas.agent import (
    AgentRecoveryRequeue, AgentReviewVerdict, AgentTaskAssignmentCreate,
    AgentTaskAssignmentUpdate, AgentWorkBegin, AgentWorkRenew,
    AgentWorkSubmit, AgentWorkTerminal,
)
from app.services.agent_service import AgentService
from app.services.agent_work_service import AgentWorkService


async def execute(packet):
    engine = create_async_engine(packet["database_url"])
    if engine.dialect.name == "sqlite":
        @event.listens_for(engine.sync_engine, "connect")
        def enforce_foreign_keys(connection, _record):
            connection.execute("PRAGMA foreign_keys=ON")
    try:
        async with async_sessionmaker(engine, expire_on_commit=False)() as db:
            async with command_transaction(db):
                actor = await AgentService(db).authenticate(packet["key"])
                if actor is None:
                    raise ValueError("Peer authentication rejected")
                service = AgentWorkService(db)
                action = packet["action"]
                if action == "work":
                    result = await service.get_work(actor)
                elif action == "context":
                    result = await service.get_task_context(actor, packet["task_id"], assignment_id=packet["assignment_id"])
                elif action in {"begin", "renew", "submit", "fail"}:
                    model = {"begin": AgentWorkBegin, "renew": AgentWorkRenew,
                             "submit": AgentWorkSubmit, "fail": AgentWorkTerminal}[action]
                    method = service.renew_work if action == "renew" else getattr(service, action)
                    result = await method(actor, model.model_validate(packet["body"]), idempotency_key=packet["idempotency_key"])
                elif action == "review":
                    result = await service.review(actor, AgentReviewVerdict.model_validate(packet["body"]), idempotency_key=packet["idempotency_key"], rationale="Independent artifact inspection", correlation_id=packet["idempotency_key"])
                elif action == "requeue":
                    result = await service.requeue_recovery(actor, packet["task_id"], AgentRecoveryRequeue.model_validate(packet["body"]), idempotency_key=packet["idempotency_key"], rationale="Observed expired ownership", correlation_id=packet["idempotency_key"])
                elif action == "assignment_update":
                    result = await service.update_assignment(packet["assignment_id"], actor, AgentTaskAssignmentUpdate.model_validate(packet["body"]), idempotency_key=packet["idempotency_key"], rationale="Explicit supervised reassignment", correlation_id=packet["idempotency_key"])
                elif action == "assignment_create":
                    result = await service.create_assignment(actor, AgentTaskAssignmentCreate.model_validate(packet["body"]), idempotency_key=packet["idempotency_key"], rationale="Explicit supervised reassignment", correlation_id=packet["idempotency_key"])
                else:
                    raise ValueError("Unsupported peer action")
                response = result.model_dump(mode="json")
        return {"ok": True, "pid": os.getpid(), "response": response}
    except Exception as error:
        return {"ok": False, "pid": os.getpid(), "error_type": type(error).__name__, "error": str(error)}
    finally:
        await engine.dispose()


if __name__ == "__main__":
    print(json.dumps(asyncio.run(execute(json.load(sys.stdin)))))
