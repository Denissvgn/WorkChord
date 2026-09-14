# Task

**Location:** `backend/app/models/task.py:44`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_task](../modules/models_task.md)

## Description

Task model with tree structure and dependencies.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `title` | `Mapped[str]` | `mapped_column(String(500), nullable=False)` | — |
| `description` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `priority` | `Mapped[int]` | `mapped_column(Integer, default=5)` | — |
| `effort_days` | `Mapped[float]` | `mapped_column(Float, default=1.0)` | — |
| `effort_hours` | `Mapped[float]` | `mapped_column(Float, default=8.0)` | — |
| `status` | `Mapped[str]` | `mapped_column(String(50), default=TaskStatus.PLANNED.value)` | — |
| `start_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True)` | — |
| `end_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True)` | — |
| `actual_start_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True)` | — |
| `actual_end_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True)` | — |
| `calculated_effort_days` | `Mapped[Optional[float]]` | `mapped_column(Float, nullable=True)` | — |
| `min_start_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True)` | — |
| `max_end_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True)` | — |
| `is_optional` | `Mapped[bool]` | `mapped_column(default=False)` | — |
| `is_deferred` | `Mapped[bool]` | `mapped_column(default=False)` | — |
| `tags` | `Mapped[Optional[str]]` | `mapped_column(String(1000), nullable=True, default='[]')` | — |
| `sort_order` | `Mapped[int]` | `mapped_column(Integer, default=0)` | — |
| `external_key` | `Mapped[Optional[str]]` | `mapped_column(String(255), nullable=True, index=True)` | — |
| `source` | `Mapped[Optional[str]]` | `mapped_column(String(100), nullable=True)` | — |
| `source_url` | `Mapped[Optional[str]]` | `mapped_column(String(1000), nullable=True)` | — |
| `version` | `Mapped[int]` | `mapped_column(Integer, default=1, nullable=False)` | — |
| `claim_expires_at` | `Mapped[Optional[datetime]]` | `mapped_column(UTCDateTime(), nullable=True)` | — |
| `claim_id` | `Mapped[Optional[str]]` | `mapped_column(String(64), nullable=True, index=True)` | — |
| `claim_generation` | `Mapped[int]` | `mapped_column(Integer, default=0, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `iteration_id` | `Mapped[int]` | `mapped_column(Integer, ForeignKey('iterations.id'), nullable=False)` | — |
| `project_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('projects.id', ondelete='SET NULL'), nullable=True, index=True)` | — |
| `milestone_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('project_milestones.id', ondelete='SET NULL'), nullable=True, index=True)` | — |
| `parent_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('tasks.id'), nullable=True)` | — |
| `assignee_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('team_members.id'), nullable=True)` | — |
| `claimed_by` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('agent_actors.id'), nullable=True)` | — |
| `iteration` | `Mapped['Iteration']` | `relationship('Iteration', back_populates='tasks')` | — |
| `project` | `Mapped[Optional['Project']]` | `relationship('Project', back_populates='tasks')` | — |
| `milestone` | `Mapped[Optional['ProjectMilestone']]` | `relationship('ProjectMilestone', back_populates='tasks')` | — |
| `assignee` | `Mapped[Optional['TeamMember']]` | `relationship('TeamMember', back_populates='tasks')` | — |
| `claimed_agent` | `Mapped[Optional['AgentActor']]` | `relationship('AgentActor', back_populates='claimed_tasks')` | — |
| `parent` | `Mapped[Optional['Task']]` | `relationship('Task', back_populates='children', remote_side=[id])` | — |
| `children` | `Mapped[list['Task']]` | `relationship('Task', back_populates='parent', cascade='all, delete-orphan', order_by='Task.sort_order, Task.id')` | — |
| `dependencies` | `Mapped[list['TaskDependency']]` | `relationship('TaskDependency', foreign_keys='TaskDependency.task_id', back_populates='task', cascade='all, delete-orphan')` | — |
| `dependents` | `Mapped[list['TaskDependency']]` | `relationship('TaskDependency', foreign_keys='TaskDependency.depends_on_id', back_populates='depends_on', cascade='all, delete-orphan')` | — |
| `status_logs` | `Mapped[list['TaskStatusLog']]` | `relationship('TaskStatusLog', back_populates='task', cascade='all, delete-orphan', order_by='TaskStatusLog.changed_at.desc()')` | — |
| `events` | `Mapped[list['TaskEvent']]` | `relationship('TaskEvent', back_populates='task', passive_deletes=True, order_by='TaskEvent.created_at.desc()')` | — |
| `agent_runs` | `Mapped[list['AgentRun']]` | `relationship('AgentRun', back_populates='task', passive_deletes=True, order_by='AgentRun.started_at.desc()')` | — |
| `agent_assignments` | `Mapped[list['AgentTaskAssignment']]` | `relationship('AgentTaskAssignment', back_populates='task', cascade='all, delete-orphan', order_by='AgentTaskAssignment.created_at.desc()')` | — |
| `routing_assessments` | `Mapped[list['TaskRoutingAssessment']]` | `relationship('TaskRoutingAssessment', back_populates='task', passive_deletes=True, order_by='TaskRoutingAssessment.task_version.desc(), TaskRoutingAssessment.created_at.desc()')` | — |
| `external_links` | `Mapped[list['ExternalLink']]` | `relationship('ExternalLink', primaryjoin=lambda: and_(Task.id == foreign(ExternalLink.entity_id), ExternalLink.entity_type == 'task'), order_by='ExternalLink.created_at, ExternalLink.id', viewonly=True)` | — |
| `request_source_links` | `Mapped[list['RequestSourceLink']]` | `relationship('RequestSourceLink', back_populates='task', passive_deletes=True, order_by='RequestSourceLink.created_at, RequestSourceLink.id')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Task (backend/app/models/task.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["_reject_routing_assessment_mutation (backend/app/models/agent.py)"]
    n4["backend/app/models/iteration.py"]
    n5["backend/app/models/project.py"]
    n6["backend/app/models/release.py"]
    n7["backend/app/models/request_source.py"]
    n8["backend/app/models/task_status_log.py"]
    n9["backend/app/models/team_member.py"]
    n10["backend/app/models/triage.py"]
    n11["_get_calculated_effort (backend/app/routers/gantt.py)"]
    n12["_task_to_gantt (backend/app/routers/gantt.py)"]
    n13["AgentPlanningService._iteration_tasks_for_update (backend/app/services/agent_planning_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/models_task.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_agent.md"
    click n4 "../modules/models_iteration.md"
    click n5 "../modules/models_project.md"
    click n6 "../modules/models_release.md"
    click n7 "../modules/models_request_source.md"
    click n8 "../modules/task_status_log.md"
    click n9 "../modules/team_member.md"
    click n10 "../modules/models_triage.md"
    click n11 "../modules/routers_gantt.md"
    click n12 "../modules/routers_gantt.md"
    click n13 "../modules/agent_planning_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_task](../modules/models_task.md) | 0 | `actual_end_date`, `actual_start_date`, `agent_assignments`, `agent_runs`, `assignee`, `assignee_id`, `calculated_effort_days`, `children`, `claim_expires_at`, `claim_generation`, `claim_id`, `claimed_agent` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `_reject_routing_assessment_mutation` | type_reference | [models_agent](../modules/models_agent.md) | — |
| `iteration` | import | [models_iteration](../modules/models_iteration.md) | — |
| `project` | import | [models_project](../modules/models_project.md) | — |
| `release` | import | [models_release](../modules/models_release.md) | — |
| `request_source` | import | [models_request_source](../modules/models_request_source.md) | — |
| `task_status_log` | import | [task_status_log](../modules/task_status_log.md) | — |
| `team_member` | import | [team_member](../modules/team_member.md) | — |
| `triage` | import | [models_triage](../modules/models_triage.md) | — |
| `_get_calculated_effort` | type_reference | [routers_gantt](../modules/routers_gantt.md) | — |
| `_task_to_gantt` | type_reference | [routers_gantt](../modules/routers_gantt.md) | — |
| `AgentPlanningService._iteration_tasks_for_update` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |

> References: showing 12 of 163 logical references; 151 omitted by the 12-row generated summary limit.
