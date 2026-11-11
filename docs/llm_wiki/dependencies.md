# Dependencies

Internal module dependency graph and external package reconciliation.

## Module graph

This is the full coupling graph, including type dependencies. Runtime startup cycles and explicit type dependencies are distinguished below.

<!-- Collapsed to top-level packages; the full module list is in the Fan-in / Fan-out table below. -->
```mermaid
flowchart TD
    n0["backend"]
    n1["frontend"]
    n2["scripts"]
    n2 --> n0
```

## Cycles

*No runtime import cycles detected.*

> These additional coupling groups include deferred, `TYPE_CHECKING`, or erased TypeScript imports. Startup cycles, including any smaller cycles within these groups, are listed above.

- [authority](modules/authority.md) ⇄ [commands](modules/commands.md) ⇄ [app_database](modules/app_database.md) ⇄ [models_agent](modules/models_agent.md) ⇄ [models_autonomy](modules/models_autonomy.md) ⇄ [models_calendar](modules/models_calendar.md) ⇄ [models_capacity](modules/models_capacity.md) ⇄ [delivery_dependency](modules/delivery_dependency.md) ⇄ [models_discussion](modules/models_discussion.md) ⇄ [models_external_link](modules/models_external_link.md) ⇄ [models_github](modules/models_github.md) ⇄ [models_identity](modules/models_identity.md) ⇄ [models_iteration](modules/models_iteration.md) ⇄ [models_label](modules/models_label.md) ⇄ [models_outbound_webhook](modules/models_outbound_webhook.md) ⇄ [models_plan_share](modules/models_plan_share.md) ⇄ [models_project](modules/models_project.md) ⇄ [recovery](modules/recovery.md) ⇄ [models_release](modules/models_release.md) ⇄ [models_request_source](modules/models_request_source.md) ⇄ [models_saved_view](modules/models_saved_view.md) ⇄ [models_system_settings](modules/models_system_settings.md) ⇄ [models_task](modules/models_task.md) ⇄ [models_task_brief](modules/models_task_brief.md) ⇄ [task_status_log](modules/task_status_log.md) ⇄ [team_member](modules/team_member.md) ⇄ [models_template](modules/models_template.md) ⇄ [models_triage](modules/models_triage.md) ⇄ [user_session](modules/user_session.md) ⇄ [observability](modules/observability.md) ⇄ [export](modules/export.md) ⇄ [snapshots](modules/snapshots.md) ⇄ [schemas_agent](modules/schemas_agent.md) ⇄ [schemas_triage](modules/schemas_triage.md) ⇄ [agent_model_catalog_service](modules/agent_model_catalog_service.md) ⇄ [agent_profile_catalog_service](modules/agent_profile_catalog_service.md) ⇄ [agent_readiness](modules/agent_readiness.md) ⇄ [agent_routing_observability](modules/agent_routing_observability.md) ⇄ [agent_routing_service](modules/agent_routing_service.md) ⇄ [agent_service](modules/agent_service.md) ⇄ [agent_team_setup_service](modules/agent_team_setup_service.md) ⇄ [agent_work_service](modules/agent_work_service.md) ⇄ [backlog_snapshot_service](modules/backlog_snapshot_service.md) ⇄ [calendar_service](modules/calendar_service.md) ⇄ [capacity_service](modules/capacity_service.md) ⇄ [delivery_dependency_service](modules/delivery_dependency_service.md) ⇄ [discussion_service](modules/discussion_service.md) ⇄ [email_settings_service](modules/email_settings_service.md) ⇄ [external_link_service](modules/external_link_service.md) ⇄ [github_status_automation_service](modules/github_status_automation_service.md) ⇄ [hierarchy_repair_service](modules/hierarchy_repair_service.md) ⇄ [identity_service](modules/identity_service.md) ⇄ [import_planning_service](modules/import_planning_service.md) ⇄ [iteration_service](modules/iteration_service.md) ⇄ [label_service](modules/label_service.md) ⇄ [language_service](modules/language_service.md) ⇄ [llm_service](modules/llm_service.md) ⇄ [notification_service](modules/notification_service.md) ⇄ [outbound_webhook_service](modules/outbound_webhook_service.md) ⇄ [planning_input_context](modules/planning_input_context.md) ⇄ [project_service](modules/project_service.md) ⇄ [request_source_service](modules/request_source_service.md) ⇄ [saved_view_service](modules/saved_view_service.md) ⇄ [snapshot_service](modules/snapshot_service.md) ⇄ [system_settings_service](modules/system_settings_service.md) ⇄ [task_brief_service](modules/task_brief_service.md) ⇄ [task_context_revision_service](modules/task_context_revision_service.md) ⇄ [task_domain_service](modules/task_domain_service.md) ⇄ [task_hierarchy_service](modules/task_hierarchy_service.md) ⇄ [task_import_service](modules/task_import_service.md) ⇄ [task_recovery_service](modules/task_recovery_service.md) ⇄ [task_service](modules/task_service.md) ⇄ [task_status_service](modules/task_status_service.md) ⇄ [task_timeline_service](modules/task_timeline_service.md) ⇄ [team_service](modules/team_service.md) ⇄ [template_service](modules/template_service.md) ⇄ [triage_service](modules/triage_service.md) ⇄ [upgrade_service](modules/upgrade_service.md) ⇄ [services_work_metrics](modules/services_work_metrics.md) ⇄ [import_parser](modules/import_parser.md)
- [TaskFiltersBar](modules/TaskFiltersBar.md) ⇄ [taskFilterDefaults](modules/taskFilterDefaults.md)

### Explicit type dependencies

Type-only bindings and declaration-file dependencies remain part of the coupling graph. Declaration-level `import type` is erased. Specifier-only type imports can retain module evaluation depending on compiler settings; see each module's Imports table.

| From | To |
|------|----|
| [UserSessionBadge](modules/UserSessionBadge.md) | [sessionService](modules/sessionService.md) |
| [RoutingCandidateComparison](modules/RoutingCandidateComparison.md) | [types_agent](modules/types_agent.md) |
| [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md) | [types_agent](modules/types_agent.md) |
| [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md) | [types_task](modules/types_task.md) |
| [TaskRoutingPanel](modules/TaskRoutingPanel.md) | [types_agent](modules/types_agent.md) |
| [TaskRoutingPanel](modules/TaskRoutingPanel.md) | [types_task](modules/types_task.md) |
| [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md) | [deliveryMetrics](modules/deliveryMetrics.md) |
| [DeliveryAnalytics](modules/DeliveryAnalytics.md) | [deliveryMetrics](modules/deliveryMetrics.md) |
| [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md) | [executionUsage](modules/executionUsage.md) |
| [TaskStatusFlow](modules/TaskStatusFlow.md) | [types_task](modules/types_task.md) |
| [useConfirmDialog](modules/useConfirmDialog.md) | [ConfirmDialog](modules/ConfirmDialog.md) |
| [SavedViewDashboardCards](modules/SavedViewDashboardCards.md) | [savedView](modules/savedView.md) |
| [ToastProvider](modules/ToastProvider.md) | [toast](modules/toast.md) |
| [GanttChart.test](modules/GanttChart.test.md) | [types_gantt](modules/types_gantt.md) |
| [GanttChart](modules/GanttChart.md) | [types_gantt](modules/types_gantt.md) |
| [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md) | [types_gantt](modules/types_gantt.md) |
| [TaskEditModal](modules/TaskEditModal.md) | [types_gantt](modules/types_gantt.md) |
| [TaskEditModal](modules/TaskEditModal.md) | [types_task](modules/types_task.md) |
| [IterationForm.test](modules/IterationForm.test.md) | [types_iteration](modules/types_iteration.md) |
| [IterationForm](modules/IterationForm.md) | [planningInputService](modules/planningInputService.md) |
| [IterationForm](modules/IterationForm.md) | [types_iteration](modules/types_iteration.md) |
| [IterationImportDialog](modules/IterationImportDialog.md) | [planningInputService](modules/planningInputService.md) |
| [IterationList](modules/IterationList.md) | [planningInputService](modules/planningInputService.md) |
| [IterationList](modules/IterationList.md) | [types_iteration](modules/types_iteration.md) |
| [IterationSelector](modules/IterationSelector.md) | [types_iteration](modules/types_iteration.md) |
| [LabelSelector](modules/LabelSelector.md) | [types_label](modules/types_label.md) |
| [AppSidebar.test](modules/AppSidebar.test.md) | [savedView](modules/savedView.md) |
| [AppSidebar](modules/AppSidebar.md) | [workspaces](modules/workspaces.md) |
| [AppSidebar](modules/AppSidebar.md) | [savedView](modules/savedView.md) |
| [AppTopNav](modules/AppTopNav.md) | [AppSidebar](modules/AppSidebar.md) |
| [AppTopNav](modules/AppTopNav.md) | [workspaces](modules/workspaces.md) |
| [ContextHelp](modules/ContextHelp.md) | [helpContexts](modules/helpContexts.md) |
| [PlanningInputBoundary](modules/PlanningInputBoundary.md) | [planningInputService](modules/planningInputService.md) |
| [InitiativeForm](modules/InitiativeForm.md) | [types_project](modules/types_project.md) |
| [ProjectForm](modules/ProjectForm.md) | [planningInputService](modules/planningInputService.md) |
| [ProjectForm](modules/ProjectForm.md) | [types_project](modules/types_project.md) |
| [ProjectForm](modules/ProjectForm.md) | [types_template](modules/types_template.md) |
| [ProjectIterationsSection](modules/ProjectIterationsSection.md) | [planningInputService](modules/planningInputService.md) |
| [ProjectIterationsSection](modules/ProjectIterationsSection.md) | [types_iteration](modules/types_iteration.md) |
| [ProjectTaskTree](modules/ProjectTaskTree.md) | [types_task](modules/types_task.md) |
| [projectStatusStyles](modules/projectStatusStyles.md) | [tone](modules/tone.md) |
| [projectStatusStyles](modules/projectStatusStyles.md) | [types_project](modules/types_project.md) |
| [ReleaseForm](modules/ReleaseForm.md) | [types_release](modules/types_release.md) |
| [ReleaseForm](modules/ReleaseForm.md) | [types_task](modules/types_task.md) |
| [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md) | [requestSource](modules/requestSource.md) |
| [AgentAccessPanel.test](modules/AgentAccessPanel.test.md) | [types_agent](modules/types_agent.md) |
| [AgentModelAdministration.test](modules/AgentModelAdministration.test.md) | [types_agent](modules/types_agent.md) |
| [AgentModelAdministration](modules/AgentModelAdministration.md) | [types_agent](modules/types_agent.md) |
| [AgentTeamStepList](modules/AgentTeamStepList.md) | [agentTeamSetup_masters](modules/agentTeamSetup_masters.md) |
| [AgentTeamStepList](modules/AgentTeamStepList.md) | [useAgentTeamReadiness](modules/useAgentTeamReadiness.md) |
| [ConstraintsPanel](modules/ConstraintsPanel.md) | [schedulingRules](modules/schedulingRules.md) |
| [EffortModifierCard.test](modules/EffortModifierCard.test.md) | [schedulingRules](modules/schedulingRules.md) |
| [EffortModifierCard](modules/EffortModifierCard.md) | [schedulingRules](modules/schedulingRules.md) |
| [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md) | [emailSettings](modules/emailSettings.md) |
| [EmailSettingsPanel](modules/EmailSettingsPanel.md) | [emailSettings](modules/emailSettings.md) |
| [EmailSettingsPanel](modules/EmailSettingsPanel.md) | [systemSettings](modules/systemSettings.md) |
| [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md) | [types_github](modules/types_github.md) |
| [GitHubSettingsPanel](modules/GitHubSettingsPanel.md) | [types_github](modules/types_github.md) |
| [GitHubSettingsPanel](modules/GitHubSettingsPanel.md) | [types_task](modules/types_task.md) |
| [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md) | [systemSettings](modules/systemSettings.md) |
| [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md) | [outboundWebhook](modules/outboundWebhook.md) |
| [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md) | [outboundWebhook](modules/outboundWebhook.md) |
| [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md) | [systemSettings](modules/systemSettings.md) |
| [RuntimeConfigSettings](modules/RuntimeConfigSettings.md) | [systemSettings](modules/systemSettings.md) |
| [SchedulingPassCard](modules/SchedulingPassCard.md) | [schedulingRules](modules/schedulingRules.md) |
| [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md) | [schedulingRules](modules/schedulingRules.md) |
| [SchedulingRulesSettings](modules/SchedulingRulesSettings.md) | [schedulingRules](modules/schedulingRules.md) |
| [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md) | [types_label](modules/types_label.md) |
| [TemplateLabelSettings](modules/TemplateLabelSettings.md) | [types_label](modules/types_label.md) |
| [TemplateLabelSettings](modules/TemplateLabelSettings.md) | [types_template](modules/types_template.md) |
| [CurrentTaskModal.test](modules/CurrentTaskModal.test.md) | [types_task](modules/types_task.md) |
| [DeliveryDependencies](modules/DeliveryDependencies.md) | [types_task](modules/types_task.md) |
| [GuardedTaskModal](modules/GuardedTaskModal.md) | [types_task](modules/types_task.md) |
| [ImportTasksModal](modules/ImportTasksModal.md) | [types_task](modules/types_task.md) |
| [KanbanBoard.test](modules/KanbanBoard.test.md) | [types_task](modules/types_task.md) |
| [KanbanBoard.test](modules/KanbanBoard.test.md) | [types_team](modules/types_team.md) |
| [KanbanBoard](modules/KanbanBoard.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [KanbanBoard](modules/KanbanBoard.md) | [types_task](modules/types_task.md) |
| [KanbanCard](modules/KanbanCard.md) | [types_task](modules/types_task.md) |
| [KanbanColumn](modules/KanbanColumn.md) | [tone](modules/tone.md) |
| [KanbanColumn](modules/KanbanColumn.md) | [types_task](modules/types_task.md) |
| [SavedViewsControl](modules/SavedViewsControl.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [SavedViewsControl](modules/SavedViewsControl.md) | [TaskList](modules/TaskList.md) |
| [SavedViewsControl](modules/SavedViewsControl.md) | [savedView](modules/savedView.md) |
| [StatusChangeControl](modules/StatusChangeControl.md) | [types_task](modules/types_task.md) |
| [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md) | [types_task](modules/types_task.md) |
| [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md) | [types_task](modules/types_task.md) |
| [TaskBriefEditor](modules/TaskBriefEditor.md) | [types_task](modules/types_task.md) |
| [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md) | [types_task](modules/types_task.md) |
| [TaskContextSummary](modules/TaskContextSummary.md) | [types_task](modules/types_task.md) |
| [TaskDiscussion](modules/TaskDiscussion.md) | [discussionService](modules/discussionService.md) |
| [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md) | [types_task](modules/types_task.md) |
| [TaskEditorDrawer](modules/TaskEditorDrawer.md) | [types_task](modules/types_task.md) |
| [TaskFiltersBar](modules/TaskFiltersBar.md) | [planningTaskIssues](modules/planningTaskIssues.md) |
| [TaskForm.test](modules/TaskForm.test.md) | [types_template](modules/types_template.md) |
| [TaskForm](modules/TaskForm.md) | [taskEditorContract](modules/taskEditorContract.md) |
| [TaskForm](modules/TaskForm.md) | [types_iteration](modules/types_iteration.md) |
| [TaskForm](modules/TaskForm.md) | [types_task](modules/types_task.md) |
| [TaskForm](modules/TaskForm.md) | [types_template](modules/types_template.md) |
| [TaskForm](modules/TaskForm.md) | [types_triage](modules/types_triage.md) |
| [TaskList.test](modules/TaskList.test.md) | [types_task](modules/types_task.md) |
| [TaskList](modules/TaskList.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [TaskList](modules/TaskList.md) | [types_label](modules/types_label.md) |
| [TaskList](modules/TaskList.md) | [types_task](modules/types_task.md) |
| [TaskTextEditorModal](modules/TaskTextEditorModal.md) | [types_task](modules/types_task.md) |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | [types_task](modules/types_task.md) |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | [types_task](modules/types_task.md) |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | [types_task](modules/types_task.md) |
| [TaskWorkPanel](modules/TaskWorkPanel.md) | [planningInputService](modules/planningInputService.md) |
| [TaskWorkPanel](modules/TaskWorkPanel.md) | [types_iteration](modules/types_iteration.md) |
| [TaskWorkPanel](modules/TaskWorkPanel.md) | [types_task](modules/types_task.md) |
| [TimeEntriesPanel](modules/TimeEntriesPanel.md) | [timeEntryService](modules/timeEntryService.md) |
| [WorkMetricsLine](modules/WorkMetricsLine.md) | [workMetrics](modules/workMetrics.md) |
| [taskDraftStorage](modules/taskDraftStorage.md) | [taskEditorContract](modules/taskEditorContract.md) |
| [taskEditorContract](modules/taskEditorContract.md) | [types_task](modules/types_task.md) |
| [taskEditorSnapshot](modules/taskEditorSnapshot.md) | [types_task](modules/types_task.md) |
| [ImportTeamModal.test](modules/ImportTeamModal.test.md) | [types_team](modules/types_team.md) |
| [TeamForm.test](modules/TeamForm.test.md) | [types_team](modules/types_team.md) |
| [TeamForm](modules/TeamForm.md) | [planningInputService](modules/planningInputService.md) |
| [TeamForm](modules/TeamForm.md) | [types_team](modules/types_team.md) |
| [TeamList](modules/TeamList.md) | [planningInputService](modules/planningInputService.md) |
| [TeamList](modules/TeamList.md) | [types_team](modules/types_team.md) |
| [TeamProfileManager.test](modules/TeamProfileManager.test.md) | [types_team](modules/types_team.md) |
| [TeamProfileManager](modules/TeamProfileManager.md) | [types_team](modules/types_team.md) |
| [VacationCsvImport](modules/VacationCsvImport.md) | [planningInputService](modules/planningInputService.md) |
| [VacationManager](modules/VacationManager.md) | [planningInputService](modules/planningInputService.md) |
| [VacationManager](modules/VacationManager.md) | [types_team](modules/types_team.md) |
| [Pill](modules/Pill.md) | [tone](modules/tone.md) |
| [StatusSegmentStrip](modules/StatusSegmentStrip.md) | [tone](modules/tone.md) |
| [tone](modules/tone.md) | [types_task](modules/types_task.md) |
| [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md) | [types_agent](modules/types_agent.md) |
| [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md) | [types_agent](modules/types_agent.md) |
| [agentTeamSetup_masters](modules/agentTeamSetup_masters.md) | [types_agent](modules/types_agent.md) |
| [statusScopes.test](modules/statusScopes.test.md) | [types_agent](modules/types_agent.md) |
| [statusScopes](modules/statusScopes.md) | [types_agent](modules/types_agent.md) |
| [IdentityProvider](modules/IdentityProvider.md) | [identityService](modules/identityService.md) |
| [identityContext](modules/identityContext.md) | [identityService](modules/identityService.md) |
| [attentionRanking.test](modules/attentionRanking.test.md) | [attentionRanking](modules/attentionRanking.md) |
| [attentionRanking.test](modules/attentionRanking.test.md) | [types_task](modules/types_task.md) |
| [attentionRanking](modules/attentionRanking.md) | [types_task](modules/types_task.md) |
| [planningMasters_masters.test](modules/planningMasters_masters.test.md) | [planningMasters_masters](modules/planningMasters_masters.md) |
| [planningMasters_masters](modules/planningMasters_masters.md) | [planningReturn](modules/planningReturn.md) |
| [planningMasters_masters](modules/planningMasters_masters.md) | [planningTaskIssues](modules/planningTaskIssues.md) |
| [planningTaskIssues.test](modules/planningTaskIssues.test.md) | [types_task](modules/types_task.md) |
| [planningTaskIssues](modules/planningTaskIssues.md) | [planningReturn](modules/planningReturn.md) |
| [planningTaskIssues](modules/planningTaskIssues.md) | [types_task](modules/types_task.md) |
| [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md) | [planningMasters_masters](modules/planningMasters_masters.md) |
| [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md) | [types_iteration](modules/types_iteration.md) |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | [types_gantt](modules/types_gantt.md) |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | [types_iteration](modules/types_iteration.md) |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | [types_task](modules/types_task.md) |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | [types_team](modules/types_team.md) |
| [usePlanningReadiness](modules/usePlanningReadiness.md) | [planningMasters_masters](modules/planningMasters_masters.md) |
| [usePlanningReadiness](modules/usePlanningReadiness.md) | [types_gantt](modules/types_gantt.md) |
| [usePlanningReadiness](modules/usePlanningReadiness.md) | [types_iteration](modules/types_iteration.md) |
| [usePlanningReadiness](modules/usePlanningReadiness.md) | [types_task](modules/types_task.md) |
| [usePlanningReadiness](modules/usePlanningReadiness.md) | [types_team](modules/types_team.md) |
| [taskViewState](modules/taskViewState.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [taskViewState](modules/taskViewState.md) | [TaskList](modules/TaskList.md) |
| [taskViewState](modules/taskViewState.md) | [savedView](modules/savedView.md) |
| [usePlanningObservation](modules/usePlanningObservation.md) | [planningInputService](modules/planningInputService.md) |
| [schedulingDisplay](modules/schedulingDisplay.md) | [schedulingRules](modules/schedulingRules.md) |
| [seedDisplay](modules/seedDisplay.md) | [types_github](modules/types_github.md) |
| [seedDisplay](modules/seedDisplay.md) | [types_label](modules/types_label.md) |
| [seedDisplay](modules/seedDisplay.md) | [savedView](modules/savedView.md) |
| [seedDisplay](modules/seedDisplay.md) | [types_template](modules/types_template.md) |
| [helpContexts](modules/helpContexts.md) | [routeModules](modules/routeModules.md) |
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | [types_agent](modules/types_agent.md) |
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | [types_task](modules/types_task.md) |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | [types_agent](modules/types_agent.md) |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | [types_task](modules/types_task.md) |
| [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md) | [types_agent](modules/types_agent.md) |
| [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md) | [statusScopes](modules/statusScopes.md) |
| [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md) | [types_agent](modules/types_agent.md) |
| [AnalyticsPage](modules/AnalyticsPage.md) | [types_task](modules/types_task.md) |
| [CalendarPage](modules/CalendarPage.md) | [types_calendar](modules/types_calendar.md) |
| [CalendarPage](modules/CalendarPage.md) | [types_team](modules/types_team.md) |
| [GanttPage.test](modules/GanttPage.test.md) | [types_gantt](modules/types_gantt.md) |
| [GanttPage.test](modules/GanttPage.test.md) | [types_iteration](modules/types_iteration.md) |
| [GanttPage](modules/GanttPage.md) | [snapshotService](modules/snapshotService.md) |
| [GanttPage](modules/GanttPage.md) | [types_gantt](modules/types_gantt.md) |
| [GanttPage](modules/GanttPage.md) | [types_iteration](modules/types_iteration.md) |
| [GanttPage](modules/GanttPage.md) | [types_task](modules/types_task.md) |
| [IterationsPage](modules/IterationsPage.md) | [types_iteration](modules/types_iteration.md) |
| [MyWorkPage.test](modules/MyWorkPage.test.md) | [types_task](modules/types_task.md) |
| [MyWorkPage](modules/MyWorkPage.md) | [types_task](modules/types_task.md) |
| [OverviewPage.test](modules/OverviewPage.test.md) | [usePlanningReadiness](modules/usePlanningReadiness.md) |
| [OverviewPage.test](modules/OverviewPage.test.md) | [types_iteration](modules/types_iteration.md) |
| [OverviewPage.test](modules/OverviewPage.test.md) | [types_task](modules/types_task.md) |
| [OverviewPage](modules/OverviewPage.md) | [tone](modules/tone.md) |
| [OverviewPage](modules/OverviewPage.md) | [attentionRanking](modules/attentionRanking.md) |
| [OverviewPage](modules/OverviewPage.md) | [usePlanningReadiness](modules/usePlanningReadiness.md) |
| [OverviewPage](modules/OverviewPage.md) | [types_iteration](modules/types_iteration.md) |
| [OverviewPage](modules/OverviewPage.md) | [types_project](modules/types_project.md) |
| [OverviewPage](modules/OverviewPage.md) | [types_task](modules/types_task.md) |
| [PlanMasterPage.test](modules/PlanMasterPage.test.md) | [planningMasters_masters](modules/planningMasters_masters.md) |
| [PlanMasterPage.test](modules/PlanMasterPage.test.md) | [usePlanningReadiness](modules/usePlanningReadiness.md) |
| [PlanMasterPage.test](modules/PlanMasterPage.test.md) | [types_iteration](modules/types_iteration.md) |
| [PlanMasterPage.test](modules/PlanMasterPage.test.md) | [types_task](modules/types_task.md) |
| [PlanMasterPage](modules/PlanMasterPage.md) | [planningMasters_masters](modules/planningMasters_masters.md) |
| [PlanMasterPage](modules/PlanMasterPage.md) | [planningReturn](modules/planningReturn.md) |
| [PlanMasterPage](modules/PlanMasterPage.md) | [planningTaskIssues](modules/planningTaskIssues.md) |
| [PlanMasterPage](modules/PlanMasterPage.md) | [usePlanningReadiness](modules/usePlanningReadiness.md) |
| [PlanMasterPage](modules/PlanMasterPage.md) | [planShareService](modules/planShareService.md) |
| [PlanSharePage](modules/PlanSharePage.md) | [planShareService](modules/planShareService.md) |
| [ProjectDetailPage](modules/ProjectDetailPage.md) | [planningInputService](modules/planningInputService.md) |
| [ProjectDetailPage](modules/ProjectDetailPage.md) | [types_project](modules/types_project.md) |
| [ProjectDetailPage](modules/ProjectDetailPage.md) | [types_release](modules/types_release.md) |
| [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md) | [types_release](modules/types_release.md) |
| [ProjectsPage](modules/ProjectsPage.md) | [types_project](modules/types_project.md) |
| [ProjectsPage](modules/ProjectsPage.md) | [savedView](modules/savedView.md) |
| [RoadmapPage](modules/RoadmapPage.md) | [types_project](modules/types_project.md) |
| [TasksPage.test](modules/TasksPage.test.md) | [types_task](modules/types_task.md) |
| [TasksPage](modules/TasksPage.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [TasksPage](modules/TasksPage.md) | [TaskList](modules/TaskList.md) |
| [TasksPage](modules/TasksPage.md) | [planningTaskIssues](modules/planningTaskIssues.md) |
| [TasksPage](modules/TasksPage.md) | [savedView](modules/savedView.md) |
| [TeamPage](modules/TeamPage.md) | [types_team](modules/types_team.md) |
| [TriagePage](modules/TriagePage.md) | [types_iteration](modules/types_iteration.md) |
| [TriagePage](modules/TriagePage.md) | [types_project](modules/types_project.md) |
| [TriagePage](modules/TriagePage.md) | [savedView](modules/savedView.md) |
| [TriagePage](modules/TriagePage.md) | [types_task](modules/types_task.md) |
| [TriagePage](modules/TriagePage.md) | [types_team](modules/types_team.md) |
| [TriagePage](modules/TriagePage.md) | [types_template](modules/types_template.md) |
| [TriagePage](modules/TriagePage.md) | [types_triage](modules/types_triage.md) |
| [agentService.test](modules/agentService.test.md) | [types_agent](modules/types_agent.md) |
| [agentService](modules/agentService.md) | [types_agent](modules/types_agent.md) |
| [calendarService](modules/calendarService.md) | [planningInputService](modules/planningInputService.md) |
| [calendarService](modules/calendarService.md) | [types_calendar](modules/types_calendar.md) |
| [deliveryMetricsService](modules/deliveryMetricsService.md) | [deliveryMetrics](modules/deliveryMetrics.md) |
| [emailSettingsService](modules/emailSettingsService.md) | [emailSettings](modules/emailSettings.md) |
| [executionUsageService](modules/executionUsageService.md) | [executionUsage](modules/executionUsage.md) |
| [exportService](modules/exportService.md) | [planningInputService](modules/planningInputService.md) |
| [ganttService](modules/ganttService.md) | [types_gantt](modules/types_gantt.md) |
| [ganttService](modules/ganttService.md) | [types_task](modules/types_task.md) |
| [githubService](modules/githubService.md) | [types_github](modules/types_github.md) |
| [iterationService](modules/iterationService.md) | [planningInputService](modules/planningInputService.md) |
| [iterationService](modules/iterationService.md) | [types_iteration](modules/types_iteration.md) |
| [labelService](modules/labelService.md) | [types_label](modules/types_label.md) |
| [outboundWebhookService](modules/outboundWebhookService.md) | [outboundWebhook](modules/outboundWebhook.md) |
| [projectService](modules/projectService.md) | [planningInputService](modules/planningInputService.md) |
| [projectService](modules/projectService.md) | [types_iteration](modules/types_iteration.md) |
| [projectService](modules/projectService.md) | [types_project](modules/types_project.md) |
| [projectService](modules/projectService.md) | [types_task](modules/types_task.md) |
| [releaseService](modules/releaseService.md) | [types_release](modules/types_release.md) |
| [requestSourceService](modules/requestSourceService.md) | [requestSource](modules/requestSource.md) |
| [savedViewService](modules/savedViewService.md) | [savedView](modules/savedView.md) |
| [schedulingRulesService](modules/schedulingRulesService.md) | [schedulingRules](modules/schedulingRules.md) |
| [systemSettingsService](modules/systemSettingsService.md) | [systemSettings](modules/systemSettings.md) |
| [taskService](modules/taskService.md) | [types_task](modules/types_task.md) |
| [taskService](modules/taskService.md) | [types_team](modules/types_team.md) |
| [teamService](modules/teamService.md) | [planningInputService](modules/planningInputService.md) |
| [teamService](modules/teamService.md) | [types_team](modules/types_team.md) |
| [templateService](modules/templateService.md) | [types_template](modules/types_template.md) |
| [triageService](modules/triageService.md) | [types_team](modules/types_team.md) |
| [triageService](modules/triageService.md) | [types_triage](modules/types_triage.md) |
| [modelAwareRouting](modules/modelAwareRouting.md) | [types_agent](modules/types_agent.md) |
| [types_agent](modules/types_agent.md) | [types_task](modules/types_task.md) |
| [emailSettings](modules/emailSettings.md) | [systemSettings](modules/systemSettings.md) |
| [types_gantt](modules/types_gantt.md) | [types_iteration](modules/types_iteration.md) |
| [types_gantt](modules/types_gantt.md) | [types_task](modules/types_task.md) |
| [types_github](modules/types_github.md) | [types_task](modules/types_task.md) |
| [types_iteration](modules/types_iteration.md) | [workMetrics](modules/workMetrics.md) |
| [types_project](modules/types_project.md) | [types_task](modules/types_task.md) |
| [types_project](modules/types_project.md) | [types_team](modules/types_team.md) |
| [types_project](modules/types_project.md) | [workMetrics](modules/workMetrics.md) |
| [types_release](modules/types_release.md) | [types_task](modules/types_task.md) |
| [types_release](modules/types_release.md) | [workMetrics](modules/workMetrics.md) |
| [types_task](modules/types_task.md) | [types_team](modules/types_team.md) |
| [types_task](modules/types_task.md) | [types_triage](modules/types_triage.md) |
| [types_triage](modules/types_triage.md) | [types_task](modules/types_task.md) |
| [modelRouting.test](modules/modelRouting.test.md) | [types_agent](modules/types_agent.md) |
| [modelRouting](modules/modelRouting.md) | [types_agent](modules/types_agent.md) |
| [savedViewState.test](modules/savedViewState.test.md) | [savedView](modules/savedView.md) |
| [savedViewState](modules/savedViewState.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [savedViewState](modules/savedViewState.md) | [savedView](modules/savedView.md) |
| [selectWorkNowTasks](modules/selectWorkNowTasks.md) | [types_task](modules/types_task.md) |
| [taskFilterDefaults](modules/taskFilterDefaults.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [taskFilters.test](modules/taskFilters.test.md) | [types_task](modules/types_task.md) |
| [taskFilters](modules/taskFilters.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [taskFilters](modules/taskFilters.md) | [types_label](modules/types_label.md) |
| [taskFilters](modules/taskFilters.md) | [types_task](modules/types_task.md) |
| [teamMemberLabels](modules/teamMemberLabels.md) | [types_team](modules/types_team.md) |
| [visibleWork.test](modules/visibleWork.test.md) | [types_task](modules/types_task.md) |
| [visibleWork](modules/visibleWork.md) | [TaskFiltersBar](modules/TaskFiltersBar.md) |
| [visibleWork](modules/visibleWork.md) | [types_label](modules/types_label.md) |
| [visibleWork](modules/visibleWork.md) | [types_task](modules/types_task.md) |

#### Type dependency cycles

- [types_task](modules/types_task.md) ⇄ [types_triage](modules/types_triage.md)

## Fan-in / Fan-out

| Module | Fan-in | Fan-out |
|--------|--------|---------|
| [models_task](modules/models_task.md) | 94 | 9 |
| [app_database](modules/app_database.md) | 88 | 5 |
| [commands](modules/commands.md) | 82 | 12 |
| [time](modules/time.md) | 77 | 0 |
| [Button](modules/Button.md) | 77 | 0 |
| [config](modules/config.md) | 71 | 1 |
| [QueryState](modules/QueryState.md) | 65 | 2 |
| [types_task](modules/types_task.md) | 65 | 2 |
| [models_agent](modules/models_agent.md) | 63 | 5 |
| [renderWithProviders](modules/renderWithProviders.md) | 63 | 2 |
| [task_service](modules/task_service.md) | 61 | 27 |
| [models_iteration](modules/models_iteration.md) | 58 | 6 |
| [authority](modules/authority.md) | 54 | 6 |
| [apiError](modules/apiError.md) | 49 | 0 |
| [team_member](modules/team_member.md) | 47 | 6 |
| [models_project](modules/models_project.md) | 44 | 9 |
| [api](modules/api.md) | 37 | 2 |
| [schemas_task](modules/schemas_task.md) | 36 | 5 |
| [i18n](modules/i18n.md) | 35 | 1 |
| [models_identity](modules/models_identity.md) | 33 | 2 |
| [agent_service](modules/agent_service.md) | 30 | 16 |
| [formatDate](modules/formatDate.md) | 30 | 1 |
| [models_calendar](modules/models_calendar.md) | 29 | 2 |
| [Input](modules/Input.md) | 29 | 0 |
| [test_delivery_scenarios](modules/test_delivery_scenarios.md) | 27 | 9 |
| [taskService](modules/taskService.md) | 27 | 3 |
| [app_main](modules/app_main.md) | 26 | 47 |
| [query_limits](modules/query_limits.md) | 26 | 0 |
| [upgrade_service](modules/upgrade_service.md) | 25 | 13 |
| [user_session](modules/user_session.md) | 24 | 6 |
| [index](modules/index.md) | 23 | 0 |
| [planningInputService](modules/planningInputService.md) | 22 | 1 |
| [schemas_agent](modules/schemas_agent.md) | 21 | 8 |
| [services_work_metrics](modules/services_work_metrics.md) | 21 | 8 |
| [autonomy_canonical](modules/autonomy_canonical.md) | 20 | 0 |
| [schemas_team](modules/schemas_team.md) | 20 | 1 |
| [snapshot_service](modules/snapshot_service.md) | 20 | 20 |
| [types_agent](modules/types_agent.md) | 20 | 1 |
| [types_iteration](modules/types_iteration.md) | 20 | 1 |
| [recovery](modules/recovery.md) | 19 | 3 |
| [toast](modules/toast.md) | 19 | 0 |
| [types_team](modules/types_team.md) | 19 | 0 |
| [task_brief_service](modules/task_brief_service.md) | 18 | 10 |
| [Modal](modules/Modal.md) | 18 | 1 |
| [teamService](modules/teamService.md) | 18 | 3 |
| [identity_service](modules/identity_service.md) | 17 | 9 |
| [iteration_service](modules/iteration_service.md) | 17 | 16 |
| [task_domain_service](modules/task_domain_service.md) | 17 | 19 |
| [team_service](modules/team_service.md) | 17 | 13 |
| [iterationService](modules/iterationService.md) | 17 | 3 |
| [schemas_agent_planning](modules/schemas_agent_planning.md) | 16 | 0 |
| [schemas_common](modules/schemas_common.md) | 16 | 0 |
| [agent_work_service](modules/agent_work_service.md) | 16 | 26 |
| [language_service](modules/language_service.md) | 16 | 2 |
| [outbound_webhook_service](modules/outbound_webhook_service.md) | 16 | 12 |
| [tone](modules/tone.md) | 16 | 1 |
| [projectService](modules/projectService.md) | 16 | 5 |
| [agent_routing](modules/agent_routing.md) | 15 | 1 |
| [schemas_task_brief](modules/schemas_task_brief.md) | 15 | 1 |
| [agent_routing_policy](modules/agent_routing_policy.md) | 15 | 0 |
| [project_service](modules/project_service.md) | 15 | 20 |
| [delivery_dependency_service](modules/delivery_dependency_service.md) | 14 | 7 |
| [iterationStore](modules/iterationStore.md) | 14 | 0 |
| [mcp_agent_tools](modules/mcp_agent_tools.md) | 13 | 51 |
| [runtime_telemetry](modules/runtime_telemetry.md) | 13 | 0 |
| [schemas_triage](modules/schemas_triage.md) | 13 | 3 |
| [Checkbox](modules/Checkbox.md) | 13 | 0 |
| [useDraftDismissal](modules/useDraftDismissal.md) | 13 | 0 |
| [identityContext](modules/identityContext.md) | 13 | 1 |
| [database_migration_manifest](modules/database_migration_manifest.md) | 12 | 0 |
| [schemas_iteration](modules/schemas_iteration.md) | 12 | 2 |
| [schemas_task_domain](modules/schemas_task_domain.md) | 12 | 0 |
| [agent_routing_service](modules/agent_routing_service.md) | 12 | 18 |
| [useConfirmDialog](modules/useConfirmDialog.md) | 12 | 1 |
| [savedView](modules/savedView.md) | 12 | 0 |
| [models_outbound_webhook](modules/models_outbound_webhook.md) | 11 | 2 |
| [system_settings_service](modules/system_settings_service.md) | 11 | 5 |
| [url_policy](modules/url_policy.md) | 11 | 1 |
| [seedDisplay](modules/seedDisplay.md) | 11 | 5 |
| [adminAccess](modules/adminAccess.md) | 11 | 1 |
| [load_common](modules/load_common.md) | 11 | 1 |
| [models_triage](modules/models_triage.md) | 10 | 7 |
| [schemas_project](modules/schemas_project.md) | 10 | 3 |
| [security](modules/security.md) | 10 | 1 |
| [useAdminAccess](modules/useAdminAccess.md) | 10 | 2 |
| [models_capacity](modules/models_capacity.md) | 9 | 1 |
| [models_time_entry](modules/models_time_entry.md) | 9 | 2 |
| [routers_agent](modules/routers_agent.md) | 9 | 25 |
| [agent_team_setup](modules/agent_team_setup.md) | 9 | 1 |
| [calendar_service](modules/calendar_service.md) | 9 | 7 |
| [capacity_service](modules/capacity_service.md) | 9 | 11 |
| [session_service](modules/session_service.md) | 9 | 9 |
| [triage_service](modules/triage_service.md) | 9 | 18 |
| [sql_semantics](modules/sql_semantics.md) | 9 | 0 |
| [CollapsibleSection](modules/CollapsibleSection.md) | 9 | 0 |
| [ConfirmDialog](modules/ConfirmDialog.md) | 9 | 2 |
| [TaskFiltersBar](modules/TaskFiltersBar.md) | 9 | 9 |
| [planningTaskIssues](modules/planningTaskIssues.md) | 9 | 2 |
| [types_gantt](modules/types_gantt.md) | 9 | 2 |
| [types_project](modules/types_project.md) | 9 | 3 |
| [postgresql___init__](modules/postgresql___init__.md) | 8 | 1 |
| [database_config](modules/database_config.md) | 8 | 0 |
| [source](modules/source.md) | 8 | 5 |
| [maintenance](modules/maintenance.md) | 8 | 2 |
| [models___init__](modules/models___init__.md) | 8 | 31 |
| [delivery_dependency](modules/delivery_dependency.md) | 8 | 3 |
| [mutation_versions](modules/mutation_versions.md) | 8 | 2 |
| [agent_routing_rollout](modules/agent_routing_rollout.md) | 8 | 1 |
| [agent_team_setup_service](modules/agent_team_setup_service.md) | 8 | 17 |
| [backlog_snapshot_service](modules/backlog_snapshot_service.md) | 8 | 13 |
| [test_managed_authority](modules/test_managed_authority.md) | 8 | 16 |
| [taskEditorContract](modules/taskEditorContract.md) | 8 | 2 |
| [planningMasters_masters](modules/planningMasters_masters.md) | 8 | 3 |
| [useLiveWindow](modules/useLiveWindow.md) | 8 | 0 |
| [usePlanningObservation](modules/usePlanningObservation.md) | 8 | 2 |
| [types_label](modules/types_label.md) | 8 | 0 |
| [schedulingRules](modules/schedulingRules.md) | 8 | 0 |
| [protectedQueries](modules/protectedQueries.md) | 8 | 1 |
| [agent_contract](modules/agent_contract.md) | 7 | 0 |
| [catalog](modules/catalog.md) | 7 | 2 |
| [mcp_server](modules/mcp_server.md) | 7 | 16 |
| [models_request_source](modules/models_request_source.md) | 7 | 5 |
| [models_saved_view](modules/models_saved_view.md) | 7 | 3 |
| [models_task_brief](modules/models_task_brief.md) | 7 | 2 |
| [task_status_log](modules/task_status_log.md) | 7 | 3 |
| [schemas_work_metrics](modules/schemas_work_metrics.md) | 7 | 0 |
| [agent_skill_bundle_service](modules/agent_skill_bundle_service.md) | 7 | 2 |
| [planning_input_context](modules/planning_input_context.md) | 7 | 11 |
| [scheduler_service](modules/scheduler_service.md) | 7 | 15 |
| [task_detail_service](modules/task_detail_service.md) | 7 | 12 |
| [LiveWindowStatus](modules/LiveWindowStatus.md) | 7 | 1 |
| [agentService](modules/agentService.md) | 7 | 2 |
| [types_template](modules/types_template.md) | 7 | 0 |
| [taskFilterDefaults](modules/taskFilterDefaults.md) | 7 | 1 |
| [evidence](modules/evidence.md) | 6 | 2 |
| [signing](modules/signing.md) | 6 | 1 |
| [project_identity](modules/project_identity.md) | 6 | 0 |
| [models_autonomy](modules/models_autonomy.md) | 6 | 2 |
| [models_external_link](modules/models_external_link.md) | 6 | 2 |
| [routers_task_domain](modules/routers_task_domain.md) | 6 | 21 |
| [agent_skill_bundle](modules/agent_skill_bundle.md) | 6 | 0 |
| [schemas_execution_usage](modules/schemas_execution_usage.md) | 6 | 0 |
| [planning_inputs](modules/planning_inputs.md) | 6 | 0 |
| [schemas_system_settings](modules/schemas_system_settings.md) | 6 | 0 |
| [agent_planning_service](modules/agent_planning_service.md) | 6 | 19 |
| [support___init__](modules/support___init__.md) | 6 | 4 |
| [GuardedTaskModal](modules/GuardedTaskModal.md) | 6 | 7 |
| [usePlanningReadiness](modules/usePlanningReadiness.md) | 6 | 12 |
| [savedViewService](modules/savedViewService.md) | 6 | 2 |
| [systemSettings](modules/systemSettings.md) | 6 | 0 |
| [result](modules/result.md) | 6 | 1 |
| [charter](modules/charter.md) | 5 | 2 |
| [database_migration_cutover](modules/database_migration_cutover.md) | 5 | 2 |
| [transfer](modules/transfer.md) | 5 | 9 |
| [models_plan_share](modules/models_plan_share.md) | 5 | 4 |
| [routers_agent_planning](modules/routers_agent_planning.md) | 5 | 16 |
| [schemas_calendar](modules/schemas_calendar.md) | 5 | 1 |
| [schemas_request_source](modules/schemas_request_source.md) | 5 | 1 |
| [schemas_saved_view](modules/schemas_saved_view.md) | 5 | 0 |
| [agent_model_catalog_service](modules/agent_model_catalog_service.md) | 5 | 6 |
| [agent_profile_catalog_service](modules/agent_profile_catalog_service.md) | 5 | 3 |
| [assignee_recommendation_service](modules/assignee_recommendation_service.md) | 5 | 5 |
| [delivery_metrics_service](modules/delivery_metrics_service.md) | 5 | 9 |
| [label_service](modules/label_service.md) | 5 | 6 |
| [saved_view_service](modules/saved_view_service.md) | 5 | 8 |
| [task_context_revision_service](modules/task_context_revision_service.md) | 5 | 5 |
| [support_database](modules/support_database.md) | 5 | 0 |
| [test_task_domain](modules/test_task_domain.md) | 5 | 25 |
| [PlanReturnBar](modules/PlanReturnBar.md) | 5 | 1 |
| [PlanningInputBoundary](modules/PlanningInputBoundary.md) | 5 | 4 |
| [SlideOverDrawer](modules/SlideOverDrawer.md) | 5 | 1 |
| [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md) | 5 | 4 |
| [dateLocale](modules/dateLocale.md) | 5 | 1 |
| [workspaces](modules/workspaces.md) | 5 | 0 |
| [labelService](modules/labelService.md) | 5 | 2 |
| [triageService](modules/triageService.md) | 5 | 3 |
| [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md) | 5 | 0 |
| [teamMemberLabels](modules/teamMemberLabels.md) | 5 | 2 |
| [autonomy_server_acceptance](modules/autonomy_server_acceptance.md) | 4 | 3 |
| [build_identity](modules/build_identity.md) | 4 | 1 |
| [database_runtime](modules/database_runtime.md) | 4 | 1 |
| [http_authority](modules/http_authority.md) | 4 | 10 |
| [delivery_observation](modules/delivery_observation.md) | 4 | 6 |
| [models_label](modules/models_label.md) | 4 | 2 |
| [models_system_settings](modules/models_system_settings.md) | 4 | 2 |
| [schemas_external_link](modules/schemas_external_link.md) | 4 | 1 |
| [schemas_gantt](modules/schemas_gantt.md) | 4 | 3 |
| [schemas_github](modules/schemas_github.md) | 4 | 0 |
| [schemas_label](modules/schemas_label.md) | 4 | 0 |
| [schemas_release](modules/schemas_release.md) | 4 | 1 |
| [schemas_template](modules/schemas_template.md) | 4 | 1 |
| [schemas_time_entry](modules/schemas_time_entry.md) | 4 | 0 |
| [agent_routing_observability](modules/agent_routing_observability.md) | 4 | 5 |
| [discussion_service](modules/discussion_service.md) | 4 | 10 |
| [email_settings_service](modules/email_settings_service.md) | 4 | 6 |
| [execution_usage_service](modules/execution_usage_service.md) | 4 | 14 |
| [external_link_service](modules/external_link_service.md) | 4 | 6 |
| [request_source_service](modules/request_source_service.md) | 4 | 9 |
| [task_hierarchy_service](modules/task_hierarchy_service.md) | 4 | 4 |
| [time_entry_service](modules/time_entry_service.md) | 4 | 9 |
| [dialogLayer](modules/dialogLayer.md) | 4 | 0 |
| [Breadcrumbs](modules/Breadcrumbs.md) | 4 | 0 |
| [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md) | 4 | 2 |
| [projectStatusStyles](modules/projectStatusStyles.md) | 4 | 2 |
| [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md) | 4 | 6 |
| [AdminAccessGate](modules/AdminAccessGate.md) | 4 | 2 |
| [TaskEditorDrawer](modules/TaskEditorDrawer.md) | 4 | 8 |
| [TaskForm](modules/TaskForm.md) | 4 | 36 |
| [TaskList](modules/TaskList.md) | 4 | 21 |
| [WorkMetricsLine](modules/WorkMetricsLine.md) | 4 | 1 |
| [agentTeamSetup_masters](modules/agentTeamSetup_masters.md) | 4 | 1 |
| [planningReturn](modules/planningReturn.md) | 4 | 0 |
| [workQueryFreshness](modules/workQueryFreshness.md) | 4 | 0 |
| [useAgentAccess](modules/useAgentAccess.md) | 4 | 1 |
| [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md) | 4 | 1 |
| [resources.en](modules/resources.en.md) | 4 | 4 |
| [routeModules](modules/routeModules.md) | 4 | 0 |
| [templateService](modules/templateService.md) | 4 | 2 |
| [timeEntryService](modules/timeEntryService.md) | 4 | 1 |
| [types_github](modules/types_github.md) | 4 | 1 |
| [types_release](modules/types_release.md) | 4 | 2 |
| [types_triage](modules/types_triage.md) | 4 | 1 |
| [workMetrics](modules/workMetrics.md) | 4 | 0 |
| [agentAccess](modules/agentAccess.md) | 4 | 0 |
| [modelRouting](modules/modelRouting.md) | 4 | 1 |
| [acceptance_artifacts](modules/acceptance_artifacts.md) | 3 | 1 |
| [loader](modules/loader.md) | 3 | 1 |
| [status](modules/status.md) | 3 | 3 |
| [database_migration_closeout](modules/database_migration_closeout.md) | 3 | 2 |
| [models_discussion](modules/models_discussion.md) | 3 | 3 |
| [models_execution_usage](modules/models_execution_usage.md) | 3 | 2 |
| [native_connection](modules/native_connection.md) | 3 | 2 |
| [models_release](modules/models_release.md) | 3 | 5 |
| [models_template](modules/models_template.md) | 3 | 2 |
| [observability](modules/observability.md) | 3 | 8 |
| [agent_skill_bundles](modules/agent_skill_bundles.md) | 3 | 5 |
| [export](modules/export.md) | 3 | 14 |
| [routers_gantt](modules/routers_gantt.md) | 3 | 12 |
| [snapshots](modules/snapshots.md) | 3 | 12 |
| [tasks](modules/tasks.md) | 3 | 21 |
| [schemas_intake](modules/schemas_intake.md) | 3 | 0 |
| [schemas_llm](modules/schemas_llm.md) | 3 | 1 |
| [schemas_outbound_webhook](modules/schemas_outbound_webhook.md) | 3 | 1 |
| [task_detail](modules/task_detail.md) | 3 | 2 |
| [github_status_automation_service](modules/github_status_automation_service.md) | 3 | 7 |
| [llm_service](modules/llm_service.md) | 3 | 7 |
| [task_timeline_service](modules/task_timeline_service.md) | 3 | 5 |
| [template_service](modules/template_service.md) | 3 | 3 |
| [import_parser](modules/import_parser.md) | 3 | 1 |
| [delivery](modules/delivery.md) | 3 | 8 |
| [transactions](modules/transactions.md) | 3 | 0 |
| [IterationForm](modules/IterationForm.md) | 3 | 12 |
| [IterationSelector](modules/IterationSelector.md) | 3 | 4 |
| [LabelSelector](modules/LabelSelector.md) | 3 | 5 |
| [AppSidebar](modules/AppSidebar.md) | 3 | 5 |
| [CommandMenu](modules/CommandMenu.md) | 3 | 6 |
| [commandMenuEvents](modules/commandMenuEvents.md) | 3 | 0 |
| [AdminAccessPanel](modules/AdminAccessPanel.md) | 3 | 6 |
| [DraftDismissalDialog](modules/DraftDismissalDialog.md) | 3 | 2 |
| [PagedTaskBrowser](modules/PagedTaskBrowser.md) | 3 | 5 |
| [PersonCapacity](modules/PersonCapacity.md) | 3 | 5 |
| [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md) | 3 | 2 |
| [TaskBriefEditor](modules/TaskBriefEditor.md) | 3 | 3 |
| [TimeEntriesPanel](modules/TimeEntriesPanel.md) | 3 | 13 |
| [taskDraftStorage](modules/taskDraftStorage.md) | 3 | 1 |
| [MasterProgress](modules/MasterProgress.md) | 3 | 0 |
| [IdentityProvider](modules/IdentityProvider.md) | 3 | 9 |
| [overviewTaskThread](modules/overviewTaskThread.md) | 3 | 0 |
| [workspaceQueryPolicy](modules/workspaceQueryPolicy.md) | 3 | 2 |
| [resources.ru](modules/resources.ru.md) | 3 | 5 |
| [ganttService](modules/ganttService.md) | 3 | 3 |
| [releaseService](modules/releaseService.md) | 3 | 2 |
| [systemSettingsService](modules/systemSettingsService.md) | 3 | 2 |
| [accessibilityInvariants](modules/accessibilityInvariants.md) | 3 | 0 |
| [deliveryMetrics](modules/deliveryMetrics.md) | 3 | 0 |
| [emailSettings](modules/emailSettings.md) | 3 | 1 |
| [outboundWebhook](modules/outboundWebhook.md) | 3 | 0 |
| [focusLifecycle](modules/focusLifecycle.md) | 3 | 0 |
| [safeUrl](modules/safeUrl.md) | 3 | 0 |
| [savedViewState](modules/savedViewState.md) | 3 | 3 |
| [taskFilters](modules/taskFilters.md) | 3 | 4 |
| [templateDefaults](modules/templateDefaults.md) | 3 | 0 |
| [visibleWork](modules/visibleWork.md) | 3 | 4 |
| [leases](modules/leases.md) | 2 | 4 |
| [preflight](modules/preflight.md) | 2 | 5 |
| [cli_server_acceptance](modules/cli_server_acceptance.md) | 2 | 3 |
| [allocation_identity](modules/allocation_identity.md) | 2 | 0 |
| [database_migration_canonical](modules/database_migration_canonical.md) | 2 | 2 |
| [models_database_migration](modules/models_database_migration.md) | 2 | 2 |
| [models_github](modules/models_github.md) | 2 | 2 |
| [calendars](modules/calendars.md) | 2 | 4 |
| [routers_email_settings](modules/routers_email_settings.md) | 2 | 5 |
| [routers_github](modules/routers_github.md) | 2 | 7 |
| [routers_intake](modules/routers_intake.md) | 2 | 6 |
| [iterations](modules/iterations.md) | 2 | 5 |
| [labels](modules/labels.md) | 2 | 4 |
| [routers_llm](modules/routers_llm.md) | 2 | 7 |
| [outbound_webhooks](modules/outbound_webhooks.md) | 2 | 6 |
| [projects](modules/projects.md) | 2 | 14 |
| [request_sources](modules/request_sources.md) | 2 | 4 |
| [saved_views](modules/saved_views.md) | 2 | 7 |
| [routers_scheduling_rules](modules/routers_scheduling_rules.md) | 2 | 4 |
| [routers_session](modules/routers_session.md) | 2 | 5 |
| [routers_system_settings](modules/routers_system_settings.md) | 2 | 4 |
| [routers_team](modules/routers_team.md) | 2 | 4 |
| [templates](modules/templates.md) | 2 | 4 |
| [routers_triage](modules/routers_triage.md) | 2 | 9 |
| [schemas_autonomy](modules/schemas_autonomy.md) | 2 | 0 |
| [delivery_metrics](modules/delivery_metrics.md) | 2 | 0 |
| [schemas_email_settings](modules/schemas_email_settings.md) | 2 | 1 |
| [schemas_plan_share](modules/schemas_plan_share.md) | 2 | 0 |
| [agent_readiness](modules/agent_readiness.md) | 2 | 6 |
| [bounded_scope_reads](modules/bounded_scope_reads.md) | 2 | 0 |
| [github_status_service](modules/github_status_service.md) | 2 | 7 |
| [hierarchy_repair_service](modules/hierarchy_repair_service.md) | 2 | 8 |
| [notification_service](modules/notification_service.md) | 2 | 3 |
| [plan_share_service](modules/plan_share_service.md) | 2 | 6 |
| [release_service](modules/release_service.md) | 2 | 11 |
| [scheduling_rules_service](modules/scheduling_rules_service.md) | 2 | 0 |
| [task_recovery_service](modules/task_recovery_service.md) | 2 | 5 |
| [task_status_service](modules/task_status_service.md) | 2 | 17 |
| [time_report_service](modules/time_report_service.md) | 2 | 5 |
| [test_project_identity](modules/test_project_identity.md) | 2 | 8 |
| [UserSessionBadge](modules/UserSessionBadge.md) | 2 | 3 |
| [RoutingCandidateComparison](modules/RoutingCandidateComparison.md) | 2 | 2 |
| [TaskRoutingPanel](modules/TaskRoutingPanel.md) | 2 | 14 |
| [DeliveryAnalytics](modules/DeliveryAnalytics.md) | 2 | 5 |
| [ExecutionUsagePanel](modules/ExecutionUsagePanel.md) | 2 | 3 |
| [FullscreenWorkspace](modules/FullscreenWorkspace.md) | 2 | 1 |
| [ToastProvider](modules/ToastProvider.md) | 2 | 2 |
| [WorkFreshness](modules/WorkFreshness.md) | 2 | 1 |
| [GanttChart](modules/GanttChart.md) | 2 | 12 |
| [TaskEditModal](modules/TaskEditModal.md) | 2 | 9 |
| [IterationImportDialog](modules/IterationImportDialog.md) | 2 | 7 |
| [AppShell](modules/AppShell.md) | 2 | 7 |
| [AppTopNav](modules/AppTopNav.md) | 2 | 9 |
| [ContextHelp](modules/ContextHelp.md) | 2 | 8 |
| [DocumentMetadata](modules/DocumentMetadata.md) | 2 | 1 |
| [SidebarIterationCard](modules/SidebarIterationCard.md) | 2 | 1 |
| [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md) | 2 | 2 |
| [ProjectForm](modules/ProjectForm.md) | 2 | 16 |
| [TimeEntriesReport](modules/TimeEntriesReport.md) | 2 | 10 |
| [ReleaseForm](modules/ReleaseForm.md) | 2 | 9 |
| [AgentAccessPanel](modules/AgentAccessPanel.md) | 2 | 7 |
| [AgentModelAdministration](modules/AgentModelAdministration.md) | 2 | 13 |
| [EffortModifierCard](modules/EffortModifierCard.md) | 2 | 4 |
| [EmailSettingsPanel](modules/EmailSettingsPanel.md) | 2 | 11 |
| [GitHubSettingsPanel](modules/GitHubSettingsPanel.md) | 2 | 12 |
| [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md) | 2 | 12 |
| [RuntimeConfigSettings](modules/RuntimeConfigSettings.md) | 2 | 10 |
| [SchedulingRulesSettings](modules/SchedulingRulesSettings.md) | 2 | 12 |
| [TemplateLabelSettings](modules/TemplateLabelSettings.md) | 2 | 11 |
| [ImportTasksModal](modules/ImportTasksModal.md) | 2 | 7 |
| [KanbanBoard](modules/KanbanBoard.md) | 2 | 16 |
| [KanbanCard](modules/KanbanCard.md) | 2 | 2 |
| [TaskDependencySelector](modules/TaskDependencySelector.md) | 2 | 5 |
| [TaskDiscussion](modules/TaskDiscussion.md) | 2 | 8 |
| [TaskTextEditorModal](modules/TaskTextEditorModal.md) | 2 | 5 |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | 2 | 8 |
| [TaskWorkPanel](modules/TaskWorkPanel.md) | 2 | 11 |
| [taskEditorSnapshot](modules/taskEditorSnapshot.md) | 2 | 2 |
| [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md) | 2 | 4 |
| [ImportTeamModal](modules/ImportTeamModal.md) | 2 | 5 |
| [TeamForm](modules/TeamForm.md) | 2 | 10 |
| [TeamProfileManager](modules/TeamProfileManager.md) | 2 | 9 |
| [VacationCsvImport](modules/VacationCsvImport.md) | 2 | 6 |
| [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md) | 2 | 1 |
| [statusScopes](modules/statusScopes.md) | 2 | 1 |
| [useAgentTeamReadiness](modules/useAgentTeamReadiness.md) | 2 | 2 |
| [identityService](modules/identityService.md) | 2 | 1 |
| [attentionRanking](modules/attentionRanking.md) | 2 | 1 |
| [planningNavigationInvalidation](modules/planningNavigationInvalidation.md) | 2 | 1 |
| [useTimeEntries](modules/useTimeEntries.md) | 2 | 2 |
| [pagination](modules/pagination.md) | 2 | 0 |
| [planningInputMessages](modules/planningInputMessages.md) | 2 | 0 |
| [schedulingDisplay](modules/schedulingDisplay.md) | 2 | 2 |
| [timeEntries](modules/timeEntries.md) | 2 | 0 |
| [calendarService](modules/calendarService.md) | 2 | 3 |
| [discussionService](modules/discussionService.md) | 2 | 1 |
| [exportService](modules/exportService.md) | 2 | 2 |
| [planShareService](modules/planShareService.md) | 2 | 1 |
| [schedulingRulesService](modules/schedulingRulesService.md) | 2 | 2 |
| [sessionService](modules/sessionService.md) | 2 | 1 |
| [snapshotService](modules/snapshotService.md) | 2 | 1 |
| [themeStore](modules/themeStore.md) | 2 | 0 |
| [modelAwareRouting](modules/modelAwareRouting.md) | 2 | 1 |
| [types_calendar](modules/types_calendar.md) | 2 | 0 |
| [executionUsage](modules/executionUsage.md) | 2 | 0 |
| [requestSource](modules/requestSource.md) | 2 | 0 |
| [copyText](modules/copyText.md) | 2 | 0 |
| [graphLimitError](modules/graphLimitError.md) | 2 | 0 |
| [selectWorkNowTasks](modules/selectWorkNowTasks.md) | 2 | 1 |
| [source_binding](modules/source_binding.md) | 2 | 0 |
| [topology](modules/topology.md) | 1 | 1 |
| [execution_mode](modules/execution_mode.md) | 1 | 0 |
| [handoff](modules/handoff.md) | 1 | 5 |
| [orchestration](modules/orchestration.md) | 1 | 2 |
| [providers](modules/providers.md) | 1 | 2 |
| [cli_closeout](modules/cli_closeout.md) | 1 | 3 |
| [cli_cutover](modules/cli_cutover.md) | 1 | 2 |
| [upgrade](modules/upgrade.md) | 1 | 2 |
| [worker](modules/worker.md) | 1 | 3 |
| [agent_catalog](modules/agent_catalog.md) | 1 | 11 |
| [routers_capacity](modules/routers_capacity.md) | 1 | 2 |
| [delivery_dependencies](modules/delivery_dependencies.md) | 1 | 3 |
| [routers_discussion](modules/routers_discussion.md) | 1 | 3 |
| [routers_identity](modules/routers_identity.md) | 1 | 14 |
| [plan_shares](modules/plan_shares.md) | 1 | 6 |
| [time_entries](modules/time_entries.md) | 1 | 7 |
| [schemas_scheduling_rules](modules/schemas_scheduling_rules.md) | 1 | 0 |
| [schemas_session](modules/schemas_session.md) | 1 | 0 |
| [snapshot](modules/snapshot.md) | 1 | 0 |
| [time_report](modules/time_report.md) | 1 | 0 |
| [agent_team_credentials](modules/agent_team_credentials.md) | 1 | 0 |
| [autonomy_work_package_service](modules/autonomy_work_package_service.md) | 1 | 9 |
| [github_webhook_service](modules/github_webhook_service.md) | 1 | 15 |
| [import_planning_service](modules/import_planning_service.md) | 1 | 4 |
| [native_session_service](modules/native_session_service.md) | 1 | 8 |
| [task_bulk_operation_service](modules/task_bulk_operation_service.md) | 1 | 8 |
| [task_import_service](modules/task_import_service.md) | 1 | 10 |
| [web_intake_service](modules/web_intake_service.md) | 1 | 5 |
| [text_similarity](modules/text_similarity.md) | 1 | 0 |
| [test_server_acceptance](modules/test_server_acceptance.md) | 1 | 6 |
| [test_cutover_evidence](modules/test_cutover_evidence.md) | 1 | 2 |
| [test_source_preflight](modules/test_source_preflight.md) | 1 | 4 |
| [factories](modules/factories.md) | 1 | 0 |
| [faults](modules/faults.md) | 1 | 0 |
| [schema](modules/schema.md) | 1 | 0 |
| [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md) | 1 | 14 |
| [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md) | 1 | 12 |
| [test_agent_team_setup](modules/test_agent_team_setup.md) | 1 | 16 |
| [test_authority_migrations](modules/test_authority_migrations.md) | 1 | 2 |
| [test_profile_capacity](modules/test_profile_capacity.md) | 1 | 17 |
| [test_time_entries](modules/test_time_entries.md) | 1 | 14 |
| [App](modules/App.md) | 1 | 3 |
| [TaskStatusFlow](modules/TaskStatusFlow.md) | 1 | 3 |
| [InteractiveCalendar](modules/InteractiveCalendar.md) | 1 | 1 |
| [SavedViewDashboardCards](modules/SavedViewDashboardCards.md) | 1 | 4 |
| [WorkRefreshStatus](modules/WorkRefreshStatus.md) | 1 | 1 |
| [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md) | 1 | 4 |
| [IterationList](modules/IterationList.md) | 1 | 11 |
| [RouteErrorBoundary](modules/RouteErrorBoundary.md) | 1 | 1 |
| [NotificationsPanel](modules/NotificationsPanel.md) | 1 | 4 |
| [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md) | 1 | 1 |
| [InitiativeForm](modules/InitiativeForm.md) | 1 | 9 |
| [ProjectIterationsSection](modules/ProjectIterationsSection.md) | 1 | 12 |
| [ProjectTaskTree](modules/ProjectTaskTree.md) | 1 | 5 |
| [AgentTeamStepList](modules/AgentTeamStepList.md) | 1 | 2 |
| [ConstraintsPanel](modules/ConstraintsPanel.md) | 1 | 3 |
| [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md) | 1 | 7 |
| [SchedulingPassCard](modules/SchedulingPassCard.md) | 1 | 4 |
| [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md) | 1 | 0 |
| [SystemHealthPanel](modules/SystemHealthPanel.md) | 1 | 2 |
| [BacklogPanel](modules/BacklogPanel.md) | 1 | 7 |
| [DeliveryDependencies](modules/DeliveryDependencies.md) | 1 | 7 |
| [KanbanColumn](modules/KanbanColumn.md) | 1 | 4 |
| [SavedViewsControl](modules/SavedViewsControl.md) | 1 | 14 |
| [StatusChangeControl](modules/StatusChangeControl.md) | 1 | 7 |
| [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md) | 1 | 9 |
| [TaskContextSummary](modules/TaskContextSummary.md) | 1 | 4 |
| [TaskSearch](modules/TaskSearch.md) | 1 | 3 |
| [TaskWorkflowGuide](modules/TaskWorkflowGuide.md) | 1 | 2 |
| [TeamList](modules/TeamList.md) | 1 | 9 |
| [VacationManager](modules/VacationManager.md) | 1 | 11 |
| [OverflowMenu](modules/OverflowMenu.md) | 1 | 0 |
| [taskViewState](modules/taskViewState.md) | 1 | 5 |
| [SystemLanguageProvider](modules/SystemLanguageProvider.md) | 1 | 4 |
| [agentTeamSetup.ru](modules/agentTeamSetup.ru.md) | 1 | 0 |
| [teamwork.en](modules/teamwork.en.md) | 1 | 0 |
| [teamwork.ru](modules/teamwork.ru.md) | 1 | 0 |
| [helpContexts](modules/helpContexts.md) | 1 | 2 |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | 1 | 13 |
| [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md) | 1 | 12 |
| [CalendarPage](modules/CalendarPage.md) | 1 | 18 |
| [GanttPage](modules/GanttPage.md) | 1 | 24 |
| [MyWorkPage](modules/MyWorkPage.md) | 1 | 12 |
| [NativeConnectionPage](modules/NativeConnectionPage.md) | 1 | 4 |
| [OverviewPage](modules/OverviewPage.md) | 1 | 17 |
| [PlanMasterPage](modules/PlanMasterPage.md) | 1 | 13 |
| [PlanPage](modules/PlanPage.md) | 1 | 5 |
| [PlanSharePage](modules/PlanSharePage.md) | 1 | 7 |
| [ProjectsPage](modules/ProjectsPage.md) | 1 | 16 |
| [RoadmapPage](modules/RoadmapPage.md) | 1 | 13 |
| [SettingsPage](modules/SettingsPage.md) | 1 | 17 |
| [TasksPage](modules/TasksPage.md) | 1 | 27 |
| [deliveryMetricsService](modules/deliveryMetricsService.md) | 1 | 2 |
| [emailSettingsService](modules/emailSettingsService.md) | 1 | 2 |
| [executionUsageService](modules/executionUsageService.md) | 1 | 2 |
| [githubService](modules/githubService.md) | 1 | 2 |
| [healthService](modules/healthService.md) | 1 | 0 |
| [outboundWebhookService](modules/outboundWebhookService.md) | 1 | 2 |
| [requestSourceService](modules/requestSourceService.md) | 1 | 2 |
| [tailwind.config](modules/tailwind.config.md) | 1 | 0 |
| [browser_worker](modules/browser_worker.md) | 1 | 0 |
| [local_baseline](modules/local_baseline.md) | 1 | 4 |
| [run](modules/run.md) | 1 | 2 |
| [autonomy___init__](modules/autonomy___init__.md) | 0 | 1 |
| [contracts___init__](modules/contracts___init__.md) | 0 | 1 |
| [agent_preflight](modules/agent_preflight.md) | 0 | 3 |
| [cli_database_migration](modules/cli_database_migration.md) | 0 | 4 |
| [database_migration___init__](modules/database_migration___init__.md) | 0 | 2 |
| [migrations_env](modules/migrations_env.md) | 0 | 5 |
| [20260928_0001_initial_schema](modules/20260928_0001_initial_schema.md) | 0 | 0 |
| [20260930_0002_profile_capacity](modules/20260930_0002_profile_capacity.md) | 0 | 0 |
| [20260930_0003_delivery_dependencies](modules/20260930_0003_delivery_dependencies.md) | 0 | 0 |
| [20260930_0004_discussion](modules/20260930_0004_discussion.md) | 0 | 0 |
| [20261003_0005_native_connections](modules/20261003_0005_native_connections.md) | 0 | 0 |
| [20261004_0006_delivery_observations](modules/20261004_0006_delivery_observations.md) | 0 | 0 |
| [20261004_0007_execution_usage](modules/20261004_0007_execution_usage.md) | 0 | 0 |
| [20261007_0008_time_entries](modules/20261007_0008_time_entries.md) | 0 | 0 |
| [20261008_0009_project_identity](modules/20261008_0009_project_identity.md) | 0 | 1 |
| [20261009_0010_allocation_identity](modules/20261009_0010_allocation_identity.md) | 0 | 1 |
| [20261009_0011_profile_identity](modules/20261009_0011_profile_identity.md) | 0 | 1 |
| [routers___init__](modules/routers___init__.md) | 0 | 23 |
| [schemas___init__](modules/schemas___init__.md) | 0 | 19 |
| [exceptions](modules/exceptions.md) | 0 | 1 |
| [test_acceptance_artifacts](modules/test_acceptance_artifacts.md) | 0 | 4 |
| [test_autonomy_foundation](modules/test_autonomy_foundation.md) | 0 | 12 |
| [test_autonomy_migrations](modules/test_autonomy_migrations.md) | 0 | 3 |
| [test_work_package_service](modules/test_work_package_service.md) | 0 | 7 |
| [conftest](modules/conftest.md) | 0 | 11 |
| [test_database_configuration](modules/test_database_configuration.md) | 0 | 3 |
| [test_deployment_topology](modules/test_deployment_topology.md) | 0 | 0 |
| [test_observability](modules/test_observability.md) | 0 | 3 |
| [test_postgresql_concurrency](modules/test_postgresql_concurrency.md) | 0 | 15 |
| [test_postgresql_documentation](modules/test_postgresql_documentation.md) | 0 | 0 |
| [test_query_boundaries](modules/test_query_boundaries.md) | 0 | 8 |
| [test_runtime_policy](modules/test_runtime_policy.md) | 0 | 4 |
| [test_schema_behavior](modules/test_schema_behavior.md) | 0 | 6 |
| [test_documentation_boundary](modules/test_documentation_boundary.md) | 0 | 1 |
| [test_postgresql_closeout](modules/test_postgresql_closeout.md) | 0 | 3 |
| [test_postgresql_transfer](modules/test_postgresql_transfer.md) | 0 | 16 |
| [test_project_identity_scope](modules/test_project_identity_scope.md) | 0 | 8 |
| [test_transfer_catalog](modules/test_transfer_catalog.md) | 0 | 3 |
| [postgresql_migrations_env](modules/postgresql_migrations_env.md) | 0 | 0 |
| [0001_wave0_probe](modules/0001_wave0_probe.md) | 0 | 0 |
| [test_allocation_identity](modules/test_allocation_identity.md) | 0 | 6 |
| [test_initial_schema](modules/test_initial_schema.md) | 0 | 2 |
| [test_postgresql_migrations](modules/test_postgresql_migrations.md) | 0 | 7 |
| [test_profile_identity](modules/test_profile_identity.md) | 0 | 6 |
| [test_sqlite_migrations](modules/test_sqlite_migrations.md) | 0 | 4 |
| [test_android_cleanup](modules/test_android_cleanup.md) | 0 | 0 |
| [test_load_seed_postgresql](modules/test_load_seed_postgresql.md) | 0 | 1 |
| [test_load_tooling](modules/test_load_tooling.md) | 0 | 1 |
| [test_local_baseline](modules/test_local_baseline.md) | 0 | 0 |
| [test_routing_evidence](modules/test_routing_evidence.md) | 0 | 0 |
| [runtime_peer](modules/runtime_peer.md) | 0 | 4 |
| [test_agent_blocker_reason](modules/test_agent_blocker_reason.md) | 0 | 1 |
| [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md) | 0 | 18 |
| [test_agent_routing_contract](modules/test_agent_routing_contract.md) | 0 | 7 |
| [test_agent_routing_data](modules/test_agent_routing_data.md) | 0 | 8 |
| [test_agent_routing_harness](modules/test_agent_routing_harness.md) | 0 | 5 |
| [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md) | 0 | 6 |
| [test_agent_routing_migrations](modules/test_agent_routing_migrations.md) | 0 | 3 |
| [test_agent_routing_observability](modules/test_agent_routing_observability.md) | 0 | 6 |
| [test_agent_routing_rollout](modules/test_agent_routing_rollout.md) | 0 | 15 |
| [test_agent_routing_service](modules/test_agent_routing_service.md) | 0 | 10 |
| [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md) | 0 | 2 |
| [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md) | 0 | 4 |
| [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md) | 0 | 9 |
| [test_agent_team_catalog](modules/test_agent_team_catalog.md) | 0 | 7 |
| [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md) | 0 | 0 |
| [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md) | 0 | 12 |
| [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md) | 0 | 8 |
| [test_allocation_recovery](modules/test_allocation_recovery.md) | 0 | 17 |
| [test_bounded_task_policy](modules/test_bounded_task_policy.md) | 0 | 8 |
| [test_capacity_contract](modules/test_capacity_contract.md) | 0 | 1 |
| [test_client_contract](modules/test_client_contract.md) | 0 | 5 |
| [test_database_harness](modules/test_database_harness.md) | 0 | 5 |
| [test_delivery_dependencies](modules/test_delivery_dependencies.md) | 0 | 13 |
| [test_delivery_metrics](modules/test_delivery_metrics.md) | 0 | 15 |
| [test_deployment_configuration](modules/test_deployment_configuration.md) | 0 | 0 |
| [test_effective_deferral](modules/test_effective_deferral.md) | 0 | 15 |
| [test_execution_usage](modules/test_execution_usage.md) | 0 | 11 |
| [test_execution_working_dates](modules/test_execution_working_dates.md) | 0 | 14 |
| [test_human_work_queries](modules/test_human_work_queries.md) | 0 | 8 |
| [test_identity_lifecycle](modules/test_identity_lifecycle.md) | 0 | 14 |
| [test_mobile_contract](modules/test_mobile_contract.md) | 0 | 0 |
| [test_mutation_versions](modules/test_mutation_versions.md) | 0 | 15 |
| [test_native_connections](modules/test_native_connections.md) | 0 | 6 |
| [test_plan_shares](modules/test_plan_shares.md) | 0 | 6 |
| [test_planning_input_context](modules/test_planning_input_context.md) | 0 | 18 |
| [test_planning_read_models](modules/test_planning_read_models.md) | 0 | 13 |
| [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md) | 0 | 0 |
| [test_process_roles](modules/test_process_roles.md) | 0 | 3 |
| [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md) | 0 | 4 |
| [test_project_working_timezone](modules/test_project_working_timezone.md) | 0 | 13 |
| [test_rehearsal_ownership](modules/test_rehearsal_ownership.md) | 0 | 0 |
| [test_runtime_boundaries](modules/test_runtime_boundaries.md) | 0 | 9 |
| [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md) | 0 | 3 |
| [test_saved_view_service](modules/test_saved_view_service.md) | 0 | 3 |
| [test_shared_member_revisions](modules/test_shared_member_revisions.md) | 0 | 9 |
| [test_shared_profile_revisions](modules/test_shared_profile_revisions.md) | 0 | 7 |
| [test_strict_caller_matrix](modules/test_strict_caller_matrix.md) | 0 | 17 |
| [test_task_discussion](modules/test_task_discussion.md) | 0 | 16 |
| [test_task_domain_integrity](modules/test_task_domain_integrity.md) | 0 | 22 |
| [test_task_domain_migrations](modules/test_task_domain_migrations.md) | 0 | 2 |
| [test_task_pagination](modules/test_task_pagination.md) | 0 | 15 |
| [test_time_reports](modules/test_time_reports.md) | 0 | 18 |
| [test_work_correctness](modules/test_work_correctness.md) | 0 | 27 |
| [test_workflow_vocabulary](modules/test_workflow_vocabulary.md) | 0 | 1 |
| [eslint.config](modules/eslint.config.md) | 0 | 0 |
| [postcss.config](modules/postcss.config.md) | 0 | 0 |
| [check-bundle-budget](modules/check-bundle-budget.md) | 0 | 0 |
| [check-query-feedback](modules/check-query-feedback.md) | 0 | 0 |
| [check-tailwind-classes](modules/check-tailwind-classes.md) | 0 | 1 |
| [UserSessionBadge.test](modules/UserSessionBadge.test.md) | 0 | 2 |
| [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md) | 0 | 4 |
| [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md) | 0 | 6 |
| [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md) | 0 | 3 |
| [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md) | 0 | 3 |
| [Button.test](modules/Button.test.md) | 0 | 1 |
| [Input.test](modules/Input.test.md) | 0 | 1 |
| [GanttChart.test](modules/GanttChart.test.md) | 0 | 5 |
| [IterationForm.test](modules/IterationForm.test.md) | 0 | 3 |
| [AppShell.test](modules/AppShell.test.md) | 0 | 2 |
| [AppSidebar.test](modules/AppSidebar.test.md) | 0 | 3 |
| [AppTopNav.test](modules/AppTopNav.test.md) | 0 | 2 |
| [CommandMenu.test](modules/CommandMenu.test.md) | 0 | 3 |
| [ContextHelp.test](modules/ContextHelp.test.md) | 0 | 4 |
| [SidebarIterationCard.test](modules/SidebarIterationCard.test.md) | 0 | 2 |
| [PlanReturnBar.test](modules/PlanReturnBar.test.md) | 0 | 3 |
| [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md) | 0 | 2 |
| [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md) | 0 | 3 |
| [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md) | 0 | 2 |
| [TimeEntriesReport.test](modules/TimeEntriesReport.test.md) | 0 | 3 |
| [projectStatusStyles.test](modules/projectStatusStyles.test.md) | 0 | 1 |
| [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md) | 0 | 2 |
| [AdminAccessPanel.test](modules/AdminAccessPanel.test.md) | 0 | 3 |
| [AgentAccessPanel.test](modules/AgentAccessPanel.test.md) | 0 | 3 |
| [AgentModelAdministration.test](modules/AgentModelAdministration.test.md) | 0 | 3 |
| [EffortModifierCard.test](modules/EffortModifierCard.test.md) | 0 | 3 |
| [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md) | 0 | 3 |
| [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md) | 0 | 3 |
| [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md) | 0 | 3 |
| [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md) | 0 | 3 |
| [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md) | 0 | 3 |
| [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md) | 0 | 3 |
| [CurrentTaskModal.test](modules/CurrentTaskModal.test.md) | 0 | 3 |
| [KanbanBoard.test](modules/KanbanBoard.test.md) | 0 | 4 |
| [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md) | 0 | 2 |
| [PersonCapacity.test](modules/PersonCapacity.test.md) | 0 | 2 |
| [SortableTaskItem](modules/SortableTaskItem.md) | 0 | 0 |
| [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md) | 0 | 2 |
| [TaskBriefEditor.test](modules/TaskBriefEditor.test.md) | 0 | 3 |
| [TaskDiscussion.test](modules/TaskDiscussion.test.md) | 0 | 3 |
| [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md) | 0 | 3 |
| [TaskForm.test](modules/TaskForm.test.md) | 0 | 4 |
| [TaskList.test](modules/TaskList.test.md) | 0 | 3 |
| [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md) | 0 | 3 |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | 0 | 3 |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | 0 | 4 |
| [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md) | 0 | 3 |
| [taskDraftStorage.test](modules/taskDraftStorage.test.md) | 0 | 1 |
| [useDraftDismissal.test](modules/useDraftDismissal.test.md) | 0 | 1 |
| [ImportTeamModal.test](modules/ImportTeamModal.test.md) | 0 | 3 |
| [TeamForm.test](modules/TeamForm.test.md) | 0 | 3 |
| [TeamProfileManager.test](modules/TeamProfileManager.test.md) | 0 | 3 |
| [InlineEmptyState](modules/InlineEmptyState.md) | 0 | 0 |
| [MasterProgress.test](modules/MasterProgress.test.md) | 0 | 1 |
| [OverflowMenu.test](modules/OverflowMenu.test.md) | 0 | 2 |
| [PageLayout](modules/PageLayout.md) | 0 | 0 |
| [Pill](modules/Pill.md) | 0 | 1 |
| [SectionCard](modules/SectionCard.md) | 0 | 0 |
| [StatusSegmentStrip](modules/StatusSegmentStrip.md) | 0 | 1 |
| [StickyRail](modules/StickyRail.md) | 0 | 0 |
| [tone.test](modules/tone.test.md) | 0 | 1 |
| [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md) | 0 | 3 |
| [statusScopes.test](modules/statusScopes.test.md) | 0 | 2 |
| [IdentityProvider.test](modules/IdentityProvider.test.md) | 0 | 3 |
| [attentionRanking.test](modules/attentionRanking.test.md) | 0 | 2 |
| [planningMasters_masters.test](modules/planningMasters_masters.test.md) | 0 | 1 |
| [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md) | 0 | 2 |
| [planningTaskIssues.test](modules/planningTaskIssues.test.md) | 0 | 2 |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | 0 | 6 |
| [useLiveWindow.test](modules/useLiveWindow.test.md) | 0 | 2 |
| [workQueryFreshness.test](modules/workQueryFreshness.test.md) | 0 | 1 |
| [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md) | 0 | 2 |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | 0 | 3 |
| [i18n.test](modules/i18n.test.md) | 0 | 3 |
| [workflowVocabulary.test](modules/workflowVocabulary.test.md) | 0 | 2 |
| [src_main](modules/src_main.md) | 0 | 5 |
| [workspaces.test](modules/workspaces.test.md) | 0 | 1 |
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | 0 | 5 |
| [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md) | 0 | 5 |
| [AnalyticsPage](modules/AnalyticsPage.md) | 0 | 11 |
| [CalendarPage.test](modules/CalendarPage.test.md) | 0 | 2 |
| [GanttPage.test](modules/GanttPage.test.md) | 0 | 6 |
| [IterationsPage](modules/IterationsPage.md) | 0 | 6 |
| [LandingPage](modules/LandingPage.md) | 0 | 0 |
| [MyWorkPage.test](modules/MyWorkPage.test.md) | 0 | 6 |
| [NativeConnectionPage.test](modules/NativeConnectionPage.test.md) | 0 | 3 |
| [NotFoundPage](modules/NotFoundPage.md) | 0 | 2 |
| [OverviewPage.test](modules/OverviewPage.test.md) | 0 | 6 |
| [PlanMasterPage.test](modules/PlanMasterPage.test.md) | 0 | 10 |
| [PlanPage.test](modules/PlanPage.test.md) | 0 | 3 |
| [PlanSharePage.test](modules/PlanSharePage.test.md) | 0 | 2 |
| [ProjectDetailPage](modules/ProjectDetailPage.md) | 0 | 27 |
| [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md) | 0 | 14 |
| [ProjectsPage.test](modules/ProjectsPage.test.md) | 0 | 3 |
| [RoadmapPage.test](modules/RoadmapPage.test.md) | 0 | 2 |
| [SettingsPage.test](modules/SettingsPage.test.md) | 0 | 5 |
| [TasksPage.test](modules/TasksPage.test.md) | 0 | 3 |
| [TeamPage](modules/TeamPage.md) | 0 | 12 |
| [TriagePage](modules/TriagePage.md) | 0 | 33 |
| [agentService.test](modules/agentService.test.md) | 0 | 3 |
| [planningInputService.test](modules/planningInputService.test.md) | 0 | 2 |
| [snapshotVersions.test](modules/snapshotVersions.test.md) | 0 | 2 |
| [taskDependencyVersions.test](modules/taskDependencyVersions.test.md) | 0 | 2 |
| [timeEntryService.test](modules/timeEntryService.test.md) | 0 | 1 |
| [iterationStore.test](modules/iterationStore.test.md) | 0 | 1 |
| [planning-masters.test](modules/planning-masters.test.md) | 0 | 0 |
| [accessibilityInvariants.test](modules/accessibilityInvariants.test.md) | 0 | 1 |
| [renderWithProviders.test](modules/renderWithProviders.test.md) | 0 | 2 |
| [setup](modules/setup.md) | 0 | 1 |
| [focusLifecycle.test](modules/focusLifecycle.test.md) | 0 | 1 |
| [modelRouting.test](modules/modelRouting.test.md) | 0 | 2 |
| [savedViewState.test](modules/savedViewState.test.md) | 0 | 3 |
| [taskFilters.test](modules/taskFilters.test.md) | 0 | 3 |
| [visibleWork.test](modules/visibleWork.test.md) | 0 | 3 |
| [vite.config](modules/vite.config.md) | 0 | 0 |
| [vitest.config](modules/vitest.config.md) | 0 | 0 |
| [create_agent_actor](modules/create_agent_actor.md) | 0 | 0 |
| [generate_workchord_keys](modules/generate_workchord_keys.md) | 0 | 0 |
| [setup_agent_team](modules/setup_agent_team.md) | 0 | 0 |
| [build_agent_skills](modules/build_agent_skills.md) | 0 | 0 |
| [build_frontend_image_identity](modules/build_frontend_image_identity.md) | 0 | 0 |
| [android_qualification](modules/android_qualification.md) | 0 | 0 |
| [android_web_peer](modules/android_web_peer.md) | 0 | 0 |
| [apt_runtime](modules/apt_runtime.md) | 0 | 0 |
| [browser_managed_work](modules/browser_managed_work.md) | 0 | 1 |
| [browser_performance](modules/browser_performance.md) | 0 | 0 |
| [browser_planning_inputs](modules/browser_planning_inputs.md) | 0 | 0 |
| [browser_write_readback](modules/browser_write_readback.md) | 0 | 0 |
| [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md) | 0 | 3 |
| [check_postgresql_documentation](modules/check_postgresql_documentation.md) | 0 | 0 |
| [ci_runtime](modules/ci_runtime.md) | 0 | 0 |
| [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md) | 0 | 19 |
| [postgres_runtime](modules/postgres_runtime.md) | 0 | 0 |
| [run_android_checks](modules/run_android_checks.md) | 0 | 0 |
| [run_disposable_checks](modules/run_disposable_checks.md) | 0 | 0 |
| [serve_disposable_api](modules/serve_disposable_api.md) | 0 | 9 |
| [serve_disposable_oidc](modules/serve_disposable_oidc.md) | 0 | 1 |
| [test_apt_runtime](modules/test_apt_runtime.md) | 0 | 0 |
| [test_ci_runtime](modules/test_ci_runtime.md) | 0 | 0 |
| [test_native_runtimes](modules/test_native_runtimes.md) | 0 | 0 |
| [generate_agent_team_contract](modules/generate_agent_team_contract.md) | 0 | 1 |
| [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md) | 0 | 1 |
| [generate_client_contract](modules/generate_client_contract.md) | 0 | 1 |
| [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md) | 0 | 6 |
| [collect](modules/collect.md) | 0 | 1 |
| [compare](modules/compare.md) | 0 | 2 |
| [finalize](modules/finalize.md) | 0 | 2 |
| [qualify](modules/qualify.md) | 0 | 2 |
| [resilience](modules/resilience.md) | 0 | 2 |
| [seal](modules/seal.md) | 0 | 1 |
| [seed](modules/seed.md) | 0 | 2 |
| [service_worksets](modules/service_worksets.md) | 0 | 16 |
| [export_acceptance_artifacts](modules/export_acceptance_artifacts.md) | 0 | 1 |
| [isolated_rehearsal](modules/isolated_rehearsal.md) | 0 | 0 |

## External dependencies

### python

- **Used:** `aiosmtplib`, `alembic`, `android-qualification`, `apt-runtime`, `ci-runtime`, `cryptography`, `fastapi`, `generate-client-contract`, `httpx`, `jsonschema`, `mcp`, `postgres-runtime`, `psycopg`, `pydantic`, `pydantic-settings`, `pyjwt`, `pytest`, `pytest-asyncio`, `pyyaml`, `run-android-checks`, `run-disposable-checks`, `scripts`, `sqlalchemy`, `starlette`, `uvicorn`, `workchord-backend`
- ⚠️ **Undeclared:** `alembic`, `android-qualification`, `apt-runtime`, `ci-runtime`, `cryptography`, `fastapi`, `generate-client-contract`, `httpx`, `jsonschema`, `mcp`, `postgres-runtime`, `psycopg`, `pyjwt`, `pytest`, `pytest-asyncio`, `pyyaml`, `run-android-checks`, `run-disposable-checks`, `scripts`, `sqlalchemy`, `starlette`, `uvicorn`, `workchord-backend`
- **Unused (declared, not imported):** `aiosqlite`, `email-validator`, `python-dotenv`, `python-multipart`, `uvicorn`

### typescript

- **Used:** `@dnd-kit/core`, `@dnd-kit/sortable`, `@dnd-kit/utilities`, `@eslint/js`, `@fontsource-variable/inter`, `@tanstack/react-query`, `@tanstack/react-virtual`, `@testing-library/dom`, `@testing-library/jest-dom`, `@testing-library/react`, `@testing-library/user-event`, `@vitejs/plugin-react`, `axios`, `clsx`, `date-fns`, `dom-accessibility-api`, `eslint`, `eslint-plugin-jsx-a11y`, `eslint-plugin-react-hooks`, `eslint-plugin-react-refresh`, `framer-motion`, `globals`, `i18next`, `lucide-react`, `playwright`, `react`, `react-dom`, `react-i18next`, `react-router-dom`, `tailwind-merge`, `typescript`, `typescript-eslint`, `vite`, `vitest`, `zustand`
- ⚠️ **Undeclared:** `playwright`

## Notes

This page reflects statically observed imports and declared dependencies. Dynamic or conditional imports and runtime-loaded integrations may not appear in the generated sections.

The authority and command modules are cross-cutting runtime boundaries. Intentional late imports connect the model registry, task services, recovery and identity without treating static cycles as proof of runtime order. The extraction remains bounded; unsupported Kotlin/shell sources and unsupported YAML candidates require direct source evidence.

Task, brief, status and recovery services use deliberate late imports to share command ownership without eager initialization cycles. The triage draft projection invokes the canonical renderer at serialization time. Bounded UI detail remains separate from the full graph used for assigned execution and scheduling.

Recovery models register the task deletion hook; the task recovery helper imports TaskService lazily to reuse command version reservations. This keeps the model-registration side effect explicit without treating static import order as runtime execution order.

The initial Alembic revision uses frozen SQLAlchemy DDL and does not import application model metadata. The Alembic environment still exposes model metadata for tooling, while upgrade_service owns revision inspection, migration locking and the separate repair boundary.

Both native orchestration entry points depend on ci_runtime for command deadlines, signal handling, process-group cleanup and receipt lifecycle. Result requirements remain caller-owned so a browser-only scope does not infer success from unrelated or absent JUnit files.

CapacityService imports snapshot and task collaborators lazily for derived revisions. commands imports the planning model at reservation time; models registration supplies the new tables before metadata is inspected. These cycles share transaction ownership rather than create separate commits.

Delivery and discussion model imports register flush listeners. The command owner invokes delivery reconciliation and outbox enqueue after flushing and before commit; previews roll back the same work. Outbound dispatch imports the discussion sink lazily, and the sink uses the existing transport error type lazily to avoid eager initialization cycles. Typed transfer references remain present where aggregate constraints forbid staging them as null.

NativeSessionService reuses IdentityService session issuance and the command transaction owner. Native exchange locks the principal before its approving browser session to align with account revocation. The Android session and cookie implementation requires direct platform evidence because Kotlin extraction is unavailable in the configured analyzer.
