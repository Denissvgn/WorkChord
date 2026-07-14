"""Schemas package."""
from app.schemas.calendar import (
    CalendarCreate, CalendarUpdate, CalendarResponse,
    CalendarImportError, CalendarImportRequest, CalendarImportResponse,
    WorkingDaysRequest, WorkingDaysResponse, HolidayImportRequest
)
from app.schemas.external_link import (
    ExternalLinkCreate, ExternalLinkEntityType, ExternalLinkProvider,
    ExternalLinkResponse, ExternalLinkUpdate, GitHubExternalLinkCreate,
    TaskExternalLinkCreate
)
from app.schemas.iteration import (
    IterationCreate, IterationSeriesCreate, IterationSeriesResponse,
    IterationSeriesStop, IterationUpdate, IterationResponse, IterationSummary
)
from app.schemas.intake import WebIntakeRateLimitInfo, WebIntakeRequest
from app.schemas.label import (
    LabelCreate, LabelGroupBrief, LabelGroupCreate, LabelGroupResponse,
    LabelGroupUpdate, LabelResponse, LabelUpdate
)
from app.schemas.outbound_webhook import (
    OutboundWebhookDeliveryResponse,
    OutboundWebhookEventResponse,
    OutboundWebhookRetryResponse,
    OutboundWebhookTargetCreate,
    OutboundWebhookTargetResponse,
    OutboundWebhookTargetUpdate,
)
from app.schemas.project import (
    InitiativeCreate, InitiativeResponse, InitiativeUpdate,
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectSummary,
    ProjectInitiativeSummary,
    ProjectStatus, ProjectHealth, ProjectTargetDateRisk,
    ProjectUpdateEntryCreate, ProjectUpdateEntryResponse, ProjectUpdateFreshness,
    ProjectMilestoneCreate, ProjectMilestoneCreateRequest,
    ProjectMilestoneDeleteResponse, ProjectMilestoneResponse,
    ProjectMilestoneStatus, ProjectMilestoneSummary, ProjectMilestoneTaskGroup,
    ProjectMilestoneUpdate
)
from app.schemas.saved_view import (
    SavedViewCreate, SavedViewCreateRequest, SavedViewDashboardCardResponse,
    SavedViewDuplicateRequest, SavedViewResponse, SavedViewScope, SavedViewType,
    SavedViewUpdate, SavedViewUpdateRequest
)
from app.schemas.system_settings import (
    AppRuntimeSettingsResponse, AppRuntimeSettingsUpdate,
    GitHubRuntimeSettingsResponse, GitHubRuntimeSettingsUpdate,
    LLMRuntimeSettingsResponse, LLMRuntimeSettingsUpdate, RestartRequiredSetting,
    RuntimeSecretField, RuntimeSettingField, RuntimeSettingSource,
    SystemSettingsResponse, WebIntakeRuntimeSettingsResponse,
    WebIntakeRuntimeSettingsUpdate
)
from app.schemas.release import (
    ReleaseCreate, ReleaseCreateRequest, ReleaseResponse, ReleaseStatus,
    ReleaseTaskSummary, ReleaseUpdate, ReleaseUpdateRequest
)
from app.schemas.request_source import (
    RequestSourceCreate, RequestSourceLinkCreate, RequestSourceLinkCreateRequest,
    RequestSourceLinkResponse, RequestSourceLinkWithSourceResponse,
    RequestSourceResponse, RequestSourceTargetType, RequestSourceType,
    RequestSourceUpdate
)
from app.schemas.team import (
    AssigneeRecommendationResponse,
    TeamMemberCreate, TeamMemberUpdate, TeamMemberResponse,
    TeamMemberProfileCompact, TeamMemberProfileCreate, TeamMemberProfileResponse,
    TeamMemberProfileSkillCreate, TeamMemberProfileSkillResponse,
    TeamMemberProfileSkillUpdate, TeamMemberProfileUpdate,
    VacationCreate, VacationImportError, VacationImportRequest,
    VacationImportResponse, VacationResponse, MemberCapacity, MemberWorkload
)
from app.schemas.template import (
    TemplateType, WorkTemplateCreate, WorkTemplateResponse, WorkTemplateUpdate
)
from app.schemas.task import (
    TaskAgentReadiness, TaskAgentReadinessCriterion, TaskBulkOperationRequest,
    TaskBulkOperationResponse, TaskBulkOperationResult, TaskCreate,
    TaskDependencyCreate, TaskImportTriageItemResponse, TaskMilestone, TaskProject,
    TaskMoveRequest, TaskResponse, TaskStatus, TaskUpdate, TasksImportRequest,
    TasksImportResponse
)
from app.schemas.triage import (
    TriageClassificationDraft, TriageClassificationSuggestionResponse,
    TriageTaskDraftRequest, TriageTaskDraftResponse,
    TriageActionRequest, TriageConvertToTaskRequest, TriageConvertToTaskResponse,
    TriageDuplicateRequest, TriageDuplicateSuggestion,
    TriageDuplicateSuggestionsResponse, TriageItemCreate, TriageItemUpdate,
    TriageItemResponse, TriageItemStatus, TriageSnoozeRequest
)
from app.schemas.gantt import (
    GanttMilestone, GanttTask, GanttResponse, SchedulingDecision, ScheduleResult
)
from app.schemas.github import (
    GitHubStatusAutomationResult,
    GitHubStatusAutomationRuleCreate,
    GitHubStatusAutomationRuleResponse,
    GitHubStatusAutomationRuleUpdate,
    GitHubWebhookResponse,
)
from app.schemas.llm import (
    FormalizeRequest, FormalizeResponse, GroundedAISuggestionResponse,
    GroundedFact, TaskAISuggestRequest,
    ImproveDescriptionRequest, ImproveDescriptionResponse,
    ExplainScheduleRequest, ExplainScheduleResponse
)
from app.schemas.common import ErrorResponse, MessageResponse

__all__ = [
    # Calendar
    "CalendarCreate", "CalendarUpdate", "CalendarResponse",
    "CalendarImportError", "CalendarImportRequest", "CalendarImportResponse",
    "WorkingDaysRequest", "WorkingDaysResponse", "HolidayImportRequest",
    # Iteration
    "IterationCreate", "IterationSeriesCreate", "IterationSeriesResponse",
    "IterationSeriesStop", "IterationUpdate", "IterationResponse",
    "IterationSummary",
    # Intake
    "WebIntakeRateLimitInfo", "WebIntakeRequest",
    # External link
    "ExternalLinkCreate", "ExternalLinkEntityType", "ExternalLinkProvider",
    "ExternalLinkResponse", "ExternalLinkUpdate", "GitHubExternalLinkCreate",
    "TaskExternalLinkCreate",
    # Label
    "LabelCreate", "LabelGroupBrief", "LabelGroupCreate", "LabelGroupResponse",
    "LabelGroupUpdate", "LabelResponse", "LabelUpdate",
    # Outbound webhooks
    "OutboundWebhookDeliveryResponse", "OutboundWebhookEventResponse",
    "OutboundWebhookRetryResponse", "OutboundWebhookTargetCreate",
    "OutboundWebhookTargetResponse", "OutboundWebhookTargetUpdate",
    # Project
    "InitiativeCreate", "InitiativeResponse", "InitiativeUpdate",
    "ProjectCreate", "ProjectUpdate", "ProjectResponse", "ProjectSummary",
    "ProjectInitiativeSummary",
    "ProjectStatus", "ProjectHealth", "ProjectTargetDateRisk",
    "ProjectUpdateEntryCreate", "ProjectUpdateEntryResponse", "ProjectUpdateFreshness",
    "ProjectMilestoneCreate", "ProjectMilestoneCreateRequest",
    "ProjectMilestoneDeleteResponse", "ProjectMilestoneResponse",
    "ProjectMilestoneStatus", "ProjectMilestoneSummary", "ProjectMilestoneTaskGroup",
    "ProjectMilestoneUpdate",
    # Saved view
    "SavedViewCreate", "SavedViewCreateRequest", "SavedViewDashboardCardResponse",
    "SavedViewDuplicateRequest", "SavedViewResponse", "SavedViewScope",
    "SavedViewType", "SavedViewUpdate", "SavedViewUpdateRequest",
    # System settings
    "AppRuntimeSettingsResponse", "AppRuntimeSettingsUpdate",
    "GitHubRuntimeSettingsResponse", "GitHubRuntimeSettingsUpdate",
    "LLMRuntimeSettingsResponse", "LLMRuntimeSettingsUpdate",
    "RestartRequiredSetting", "RuntimeSecretField", "RuntimeSettingField",
    "RuntimeSettingSource", "SystemSettingsResponse",
    "WebIntakeRuntimeSettingsResponse", "WebIntakeRuntimeSettingsUpdate",
    # Release
    "ReleaseCreate", "ReleaseCreateRequest", "ReleaseResponse", "ReleaseStatus",
    "ReleaseTaskSummary", "ReleaseUpdate", "ReleaseUpdateRequest",
    # Request source
    "RequestSourceCreate", "RequestSourceLinkCreate", "RequestSourceLinkCreateRequest",
    "RequestSourceLinkResponse", "RequestSourceLinkWithSourceResponse",
    "RequestSourceResponse", "RequestSourceTargetType", "RequestSourceType",
    "RequestSourceUpdate",
    # Team
    "AssigneeRecommendationResponse",
    "TeamMemberCreate", "TeamMemberUpdate", "TeamMemberResponse",
    "TeamMemberProfileCompact", "TeamMemberProfileCreate", "TeamMemberProfileResponse",
    "TeamMemberProfileSkillCreate", "TeamMemberProfileSkillResponse",
    "TeamMemberProfileSkillUpdate", "TeamMemberProfileUpdate",
    "VacationCreate", "VacationImportError", "VacationImportRequest",
    "VacationImportResponse", "VacationResponse", "MemberCapacity", "MemberWorkload",
    # Template
    "TemplateType", "WorkTemplateCreate", "WorkTemplateResponse", "WorkTemplateUpdate",
    # Task
    "TaskAgentReadiness", "TaskAgentReadinessCriterion", "TaskBulkOperationRequest",
    "TaskBulkOperationResponse", "TaskBulkOperationResult", "TaskCreate",
    "TaskDependencyCreate", "TaskImportTriageItemResponse", "TaskMilestone", "TaskProject",
    "TaskMoveRequest", "TaskResponse", "TaskStatus", "TaskUpdate", "TasksImportRequest",
    "TasksImportResponse",
    # Triage
    "TriageClassificationDraft", "TriageClassificationSuggestionResponse",
    "TriageTaskDraftRequest", "TriageTaskDraftResponse",
    "TriageActionRequest", "TriageConvertToTaskRequest", "TriageConvertToTaskResponse",
    "TriageDuplicateRequest", "TriageDuplicateSuggestion",
    "TriageDuplicateSuggestionsResponse", "TriageItemCreate", "TriageItemUpdate",
    "TriageItemResponse", "TriageItemStatus", "TriageSnoozeRequest",
    # Gantt
    "GanttMilestone", "GanttTask", "GanttResponse", "SchedulingDecision", "ScheduleResult",
    # GitHub
    "GitHubStatusAutomationResult", "GitHubStatusAutomationRuleCreate",
    "GitHubStatusAutomationRuleResponse", "GitHubStatusAutomationRuleUpdate",
    "GitHubWebhookResponse",
    # LLM
    "FormalizeRequest", "FormalizeResponse", "GroundedAISuggestionResponse",
    "GroundedFact", "TaskAISuggestRequest",
    "ImproveDescriptionRequest", "ImproveDescriptionResponse",
    "ExplainScheduleRequest", "ExplainScheduleResponse",
    # Common
    "ErrorResponse", "MessageResponse",
]
