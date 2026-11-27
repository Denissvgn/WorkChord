# ManualProvenanceService__agent_recorder

**Entry point:** `manual_provenance_service.ManualProvenanceService._agent_recorder`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [manual_provenance_service](../modules/manual_provenance_service.md), [review_provenance](../modules/review_provenance.md)

> An agent recorder is accountable like a contributor: its actor, profile and publisher are kept.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `review_provenance.actor_provenance`
3. `commands.PlanningConflict`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [manual_provenance_service](../modules/manual_provenance_service.md)
- [review_provenance](../modules/review_provenance.md)

## Behavior

This workflow starts at `manual_provenance_service.ManualProvenanceService._agent_recorder`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
