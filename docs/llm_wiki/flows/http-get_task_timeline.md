# get_task_timeline

**Entry point:** `get_task_timeline` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [schemas_agent](../modules/schemas_agent.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_task_timeline
    participant p1 as AgentService
    participant p2 as db.scalar
    participant p3 as select(…).where
    participant p4 as select
    participant p5 as HTTPException
    participant p6 as agent_service.get_task_timeline
    participant p7 as TaskTimelineResponse
    participant p8 as TaskTimelineItem
    p0->>p1: AgentService
    p0-->>p2: db.scalar
    p0-->>p3: select(…).where
    p0-->>p4: select
    p0-->>p5: HTTPException
    p0-->>p6: agent_service.get_task_timeline
    p0->>p7: TaskTimelineResponse
    p0->>p8: TaskTimelineItem
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_task_timeline"]
    s2["2. AgentService"]
    s3["3. db.scalar"]
    s4["4. select(…).where"]
    s5["5. select"]
    s6["6. HTTPException"]
    s7["7. agent_service.get_task_timeline"]
    s8["8. TaskTimelineResponse"]
    s9["9. TaskTimelineItem"]
    s1 -->|"AgentService(db)"| s2
    s1 -. "db.scalar(...)" .-> s3
    s1 -. "select(…).where(...)" .-> s4
    s1 -. "select(Task.id)" .-> s5
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s6
    s1 -. "agent_service.get_task_timeline(task_id)" .-> s7
    s1 -->|"TaskTimelineResponse(task_id=task_id, items=...)"| s8
    s1 -->|"TaskTimelineItem(**=item)"| s9
    click s1 "../modules/tasks.md"
    click s2 "../modules/agent_service.md"
    click s8 "../modules/schemas_agent.md"
    click s9 "../modules/schemas_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_task_timeline` | `task_id: int`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `Task`, `status` | - | `TaskTimelineResponse(...)` |
| `AgentService` | - | - | - | - |
| `db.scalar` | - | - | - | - |
| `select(…).where` | - | - | - | - |
| `select` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `agent_service.get_task_timeline` | - | - | - | - |
| `TaskTimelineResponse` | - | - | - | - |
| `TaskTimelineItem` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_task_timeline | AgentService | 1005 | `AgentService(db)` |
| get_task_timeline | db.scalar | 1006 | `db.scalar(...)` |
| get_task_timeline | select(…).where | 1006 | `select(Task.id).where(...)` |
| get_task_timeline | select | 1006 | `select(Task.id)` |
| get_task_timeline | HTTPException | 1008 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| get_task_timeline | agent_service.get_task_timeline | 1013 | `agent_service.get_task_timeline(task_id)` |
| get_task_timeline | TaskTimelineResponse | 1014 | `TaskTimelineResponse(task_id=task_id, items=...)` |
| get_task_timeline | TaskTimelineItem | 1016 | `TaskTimelineItem(**=item)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_task_timeline` | `db.scalar` | 1006 |
| unresolved_call | `get_task_timeline` | `select(Task.id).where` | 1006 |
| external_call | `get_task_timeline` | `select` | 1006 |
| external_call | `get_task_timeline` | `HTTPException` | 1008 |
| unresolved_call | `get_task_timeline` | `agent_service.get_task_timeline` | 1013 |

## Behavior

This flow starts at `get_task_timeline` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
