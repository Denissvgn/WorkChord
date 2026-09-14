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
    participant p2 as agent_service.task_service.get_by_id
    participant p3 as HTTPException
    participant p4 as agent_service.get_task_timeline
    participant p5 as TaskTimelineResponse
    participant p6 as TaskTimelineItem
    p0->>p1: AgentService
    p0-->>p2: agent_service.task_service.get_by_id
    p0-->>p3: HTTPException
    p0-->>p4: agent_service.get_task_timeline
    p0->>p5: TaskTimelineResponse
    p0->>p6: TaskTimelineItem
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_task_timeline"]
    s2["2. AgentService"]
    s3["3. agent_service.task_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. agent_service.get_task_timeline"]
    s6["6. TaskTimelineResponse"]
    s7["7. TaskTimelineItem"]
    s1 -->|"AgentService(db)"| s2
    s1 -. "agent_service.task_service.get_by_id(task_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -. "agent_service.get_task_timeline(task_id)" .-> s5
    s1 -->|"TaskTimelineResponse(task_id=task_id, items=...)"| s6
    s1 -->|"TaskTimelineItem(**=item)"| s7
    click s1 "../modules/tasks.md"
    click s2 "../modules/agent_service.md"
    click s6 "../modules/schemas_agent.md"
    click s7 "../modules/schemas_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_task_timeline` | `task_id: int`, `db: Annotated[AsyncSession, Depends(get_db)]` | `status` | - | `TaskTimelineResponse(...)` |
| `AgentService` | - | - | - | - |
| `agent_service.task_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `agent_service.get_task_timeline` | - | - | - | - |
| `TaskTimelineResponse` | - | - | - | - |
| `TaskTimelineItem` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_task_timeline | AgentService | 982 | `AgentService(db)` |
| get_task_timeline | agent_service.task_service.get_by_id | 983 | `agent_service.task_service.get_by_id(task_id)` |
| get_task_timeline | HTTPException | 985 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| get_task_timeline | agent_service.get_task_timeline | 990 | `agent_service.get_task_timeline(task_id)` |
| get_task_timeline | TaskTimelineResponse | 991 | `TaskTimelineResponse(task_id=task_id, items=...)` |
| get_task_timeline | TaskTimelineItem | 993 | `TaskTimelineItem(**=item)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_task_timeline` | `agent_service.task_service.get_by_id` | 983 |
| external_call | `get_task_timeline` | `HTTPException` | 985 |
| unresolved_call | `get_task_timeline` | `agent_service.get_task_timeline` | 990 |

## Behavior

This flow starts at `get_task_timeline` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
