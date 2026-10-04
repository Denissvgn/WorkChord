# runtime_peer

**Entry point:** `__main__` (`process`)
**Source:** [runtime_peer](../modules/runtime_peer.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), and 3 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [runtime_peer](../modules/runtime_peer.md)

**Related modules:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [schemas_agent](../modules/schemas_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as __main__
    participant p1 as print
    participant p2 as json.dumps
    participant p3 as asyncio.run
    participant p4 as execute
    participant p5 as create_async_engine
    participant p6 as async_sessionmaker
    participant p7 as command_transaction
    participant p8 as current_command
    participant p9 as getattr (backend/app/commands.py:current_command)
    participant p10 as isinstance
    participant p11 as info.get
    participant p12 as RuntimeError
    participant p13 as CommandState
    participant p14 as db.flush
    participant p15 as db.info.get
    participant p16 as DeliveryDependencyService(…).reconcile
    participant p17 as DeliveryDependencyService
    participant p18 as sorted
    participant p19 as db.info.pop
    participant p20 as set
    participant p21 as DiscussionService(…).enqueue
    participant p22 as DiscussionService
    participant p23 as db.rollback
    participant p24 as db.commit
    p0-->>p1: print
    p0-->>p2: json.dumps
    p0-->>p3: asyncio.run
    p0->>p4: execute
    p4-->>p5: create_async_engine
    p4-->>p6: async_sessionmaker
    p4->>p7: command_transaction
    p7->>p8: current_command
    p8-->>p9: getattr (backend/app/commands.py:current_command)
    p8-->>p10: isinstance
    p8-->>p11: info.get
    p7-->>p12: RuntimeError
    p7->>p13: CommandState
    p7-->>p12: RuntimeError
    p7-->>p14: db.flush
    p7-->>p15: db.info.get
    p7-->>p15: db.info.get
    p7-->>p15: db.info.get
    p7-->>p16: DeliveryDependencyService(…).reconcile
    p7->>p17: DeliveryDependencyService
    p7-->>p18: sorted
    p7-->>p19: db.info.pop
    p7-->>p20: set
    p7-->>p21: DiscussionService(…).enqueue
    p7->>p22: DiscussionService
    p7-->>p23: db.rollback
    p7-->>p24: db.commit
    p7-->>p14: db.flush
    p7-->>p23: db.rollback
    p7-->>p19: db.info.pop
```

> Call sequence diagram shows 30 of 56 interactions; 26 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. __main__"]
    s2["2. print"]
    s3["3. json.dumps"]
    s4["4. asyncio.run"]
    s5["5. execute"]
    s6["6. create_async_engine"]
    s7["7. async_sessionmaker"]
    s8["8. command_transaction"]
    s9["9. current_command"]
    s10["10. getattr (backend/app/commands.py:current_command)"]
    s11["11. isinstance"]
    s12["12. info.get"]
    s1 -. "print(json.dumps(...))" .-> s2
    s1 -. "json.dumps(asyncio.run(...))" .-> s3
    s1 -. "asyncio.run(execute(...))" .-> s4
    s1 -->|"execute(json.load(...))"| s5
    s5 -. "create_async_engine(packet[...])" .-> s6
    s5 -. "async_sessionmaker(engine, expire_on_commit=False)" .-> s7
    s5 -->|"command_transaction(db)"| s8
    s8 -->|"current_command(db)"| s9
    s9 -. "getattr (backend/app/commands.py:current_command)(db, 'info', None)" .-> s10
    s9 -. "isinstance(info, dict)" .-> s11
    s9 -. "info.get('command')" .-> s12
    b0["mutation db.info.pop"]
    s8 -. "mutation db.info.pop" .-> b0
    b1["mutation db.info.pop"]
    s8 -. "mutation db.info.pop" .-> b1
    b2["mutation db.info.pop"]
    s8 -. "mutation db.info.pop" .-> b2
    click s1 "../modules/runtime_peer.md"
    click s5 "../modules/runtime_peer.md"
    click s8 "../modules/commands.md"
    click s9 "../modules/commands.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `__main__` | - | - | - | - |
| `print` | - | - | - | - |
| `json.dumps` | - | - | - | - |
| `asyncio.run` | - | - | - | - |
| `execute` | `packet` | `AgentWorkBegin`, `AgentWorkRenew`, `AgentWorkSubmit`, `AgentWorkTerminal` | - | `{...}`, `{...}` |
| `create_async_engine` | - | - | - | - |
| `async_sessionmaker` | - | - | - | - |
| `command_transaction` | `db: AsyncSession`, `mode`, `commit` | - | `previous.failed`, `db.info[...]` | `none` |
| `current_command` | `db` | - | - | `...` |
| `getattr (backend/app/commands.py:current_command)` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `info.get` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| __main__ | print | 63 | `print(json.dumps(...))` |
| __main__ | json.dumps | 63 | `json.dumps(asyncio.run(...))` |
| __main__ | asyncio.run | 63 | `asyncio.run(execute(...))` |
| __main__ | execute | 63 | `execute(json.load(...))` |
| execute | create_async_engine | 22 | `create_async_engine(packet[...])` |
| execute | async_sessionmaker | 28 | `async_sessionmaker(engine, expire_on_commit=False)` |
| execute | command_transaction | 29 | `command_transaction(db)` |
| command_transaction | current_command | 85 | `current_command(db)` |
| current_command | getattr (backend/app/commands.py:current_command) | 71 | `getattr(db, 'info', None)` |
| current_command | isinstance | 72 | `isinstance(info, dict)` |
| current_command | info.get | 72 | `info.get('command')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `db.info.pop` | `command_transaction` | 105 |
| mutation | `db.info.pop` | `command_transaction` | 118 |
| mutation | `db.info.pop` | `command_transaction` | 120 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `__main__` | `print` | 63 |
| external_call | `__main__` | `json.dumps` | 63 |
| external_call | `__main__` | `asyncio.run` | 63 |
| external_call | `execute` | `create_async_engine` | 22 |
| external_call | `execute` | `async_sessionmaker` | 28 |
| external_call | `current_command` | `getattr` | 71 |
| external_call | `current_command` | `isinstance` | 72 |
| unresolved_call | `current_command` | `info.get` | 72 |
| step_limit | `__main__` | `first 12 steps` | 0 |

## Behavior

This flow starts at `__main__` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
