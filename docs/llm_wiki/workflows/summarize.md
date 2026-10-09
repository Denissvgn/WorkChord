# summarize

**Entry point:** `local_baseline.summarize`
**Modules involved:** [load_common](../modules/load_common.md), [local_baseline](../modules/local_baseline.md), [result](../modules/result.md), [run](../modules/run.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `load_common.QualificationInputError`
2. `load_common.QualificationInputError`
3. `run.Recorder`
4. `load_common.QualificationInputError`
5. `load_common.QualificationInputError`
6. `load_common.QualificationInputError`
7. `run.Attempt`
8. `load_common.QualificationInputError`
9. `load_common.QualificationInputError`
10. `load_common.QualificationInputError`
11. `load_common.QualificationInputError`
12. `result.latency_summary`
13. `load_common.utc_now_text`

## Touches

- [load_common](../modules/load_common.md)
- [local_baseline](../modules/local_baseline.md)
- [result](../modules/result.md)
- [run](../modules/run.md)

## Behavior

This workflow starts at `local_baseline.summarize`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
