# worker_flow

**Entry point:** `worker._run`
**Modules involved:** [app_database](../modules/app_database.md), [config](../modules/config.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [worker](../modules/worker.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `app_database.init_db`
3. `outbound_webhook_service.run_due_outbound_delivery_jobs`
4. `outbound_webhook_service.outbound_delivery_worker_loop`
5. `app_database.close_database`

## Touches

- [app_database](../modules/app_database.md)
- [config](../modules/config.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [worker](../modules/worker.md)

## Behavior

This workflow starts at `worker._run`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
