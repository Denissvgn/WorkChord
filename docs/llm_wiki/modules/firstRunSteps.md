# firstRunSteps Module

**Path:** `frontend/src/features/firstRun/firstRunSteps.ts`

## Description

_Auto-generated from `frontend/src/features/firstRun/firstRunSteps.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../planningMasters/planningReturn` | `PlanningStepId` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FIRST_RUN_PLAN_CHECKPOINT`, `FIRST_RUN_SETUP_PARAM`, `FIRST_RUN_STEP_IDS`, `FirstRunFacts`, `FirstRunStep`, `FirstRunStepId`, `firstRunPlanHref`, `firstRunSteps`, `nextFirstRunStep` |
| Constants | `FIRST_RUN_STEP_IDS`, `FIRST_RUN_PLAN_CHECKPOINT`, `FIRST_RUN_SETUP_PARAM`, `STEP_DONE` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/features/firstRun/firstRunSteps.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/firstRunSteps.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (14) |
| Outbound | `frontend` (1) |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FirstRunFacts](../entities/FirstRunFacts.md) | Interface | 27 | — | What the workspace holds, read from the server. Nothing here is a stored flag: every step |
| [FirstRunStep](../entities/FirstRunStep.md) | Interface | 40 | — | — |
| [FirstRunStepId](../entities/FirstRunStepId.md) | Type alias | 6 | `typeof FIRST_RUN_STEP_IDS[number]` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `firstRunPlanHref` | `(checkpoint: PlanningStepId)` | — | — |
| `firstRunSteps` | `(facts: FirstRunFacts) -> FirstRunStep[]` | — | — |
| `nextFirstRunStep` | `(steps: readonly FirstRunStep[]) -> FirstRunStepId \| null` | — | The step the panel opens: the first one not done, or null once all six are. |
