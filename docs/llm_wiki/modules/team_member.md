# team_member Module

**Path:** `backend/app/models/team_member.py`

## Description

Team member model.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.agent` | `AgentActor` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Initiative`, `Project` |
| `app.models.task` | `Task` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `date`, `datetime` |
| `sqlalchemy` | `Boolean`, `CheckConstraint`, `Date`, `Float`, `ForeignKey`, `Index`, `Integer`, `JSON`, `String`, `Text`, `UniqueConstraint` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `TYPE_CHECKING`, `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/models/team_member.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/team_member.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (43) |
| Outbound | `backend` (6) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 45 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TeamMember](../entities/team_member_TeamMember.md) | 18 | `Base` | Team member model with availability and capacity settings. |
| [TeamMemberProfile](../entities/team_member_TeamMemberProfile.md) | 68 | `Base` | Reusable person profile for durable capability and preference metadata. |
| [TeamMemberProfileSkill](../entities/team_member_TeamMemberProfileSkill.md) | 122 | `Base` | Structured skill or weakness attached to a reusable team-member profile. |
| [Vacation](../entities/team_member_Vacation.md) | 164 | `Base` | Vacation period for a team member. |
