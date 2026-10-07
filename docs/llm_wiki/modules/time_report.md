# time_report Module

**Path:** `backend/app/schemas/time_report.py`

## Description

Scoped recorded coverage, distinct from current effort estimates.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `date` |
| `pydantic` | `BaseModel` |
| `typing` | `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/time_entries.py"]
    n1["backend/app/schemas/time_report.py"]
    n0 --> n1
    click n0 "../modules/time_entries.md"
    click n1 "../modules/time_report.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [time_entries](../modules/time_entries.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TimeReportItem](../entities/TimeReportItem.md) | 8 | `BaseModel` | — |
| [TimeReportTotals](../entities/TimeReportTotals.md) | 17 | `BaseModel` | — |
| [TimeReportPage](../entities/TimeReportPage.md) | 26 | `BaseModel` | — |
