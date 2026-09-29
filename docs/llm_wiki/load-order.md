# Load order

Topological module load / startup order and import-time side effects.

## Load order

<!-- Dependency-first order: each module loads after the internal modules it imports. -->
1. [agent_contract](modules/agent_contract.md)
2. [autonomy_canonical](modules/autonomy_canonical.md)
3. [autonomy___init__](modules/autonomy___init__.md)
4. [loader](modules/loader.md)
5. [postgresql___init__](modules/postgresql___init__.md)
6. [topology](modules/topology.md)
7. [execution_mode](modules/execution_mode.md)
8. [signing](modules/signing.md)
9. [charter](modules/charter.md)
10. [contracts___init__](modules/contracts___init__.md)
11. [evidence](modules/evidence.md)
12. [leases](modules/leases.md)
13. [orchestration](modules/orchestration.md)
14. [preflight](modules/preflight.md)
15. [providers](modules/providers.md)
16. [status](modules/status.md)
17. [handoff](modules/handoff.md)
18. [build_identity](modules/build_identity.md)
19. [autonomy_server_acceptance](modules/autonomy_server_acceptance.md)
20. [agent_preflight](modules/agent_preflight.md)
21. [cli_server_acceptance](modules/cli_server_acceptance.md)
22. [commands](modules/commands.md)
23. [database_config](modules/database_config.md)
24. [config](modules/config.md)
25. [authority](modules/authority.md)
26. [database_migration_manifest](modules/database_migration_manifest.md)
27. [database_migration_cutover](modules/database_migration_cutover.md)
28. [cli_cutover](modules/cli_cutover.md)
29. [database_migration_closeout](modules/database_migration_closeout.md)
30. [cli_closeout](modules/cli_closeout.md)
31. [20260928_0001_initial_schema](modules/20260928_0001_initial_schema.md)
32. [query_limits](modules/query_limits.md)
33. [runtime_telemetry](modules/runtime_telemetry.md)
34. [database_runtime](modules/database_runtime.md)
35. [maintenance](modules/maintenance.md)
36. [schemas_agent_planning](modules/schemas_agent_planning.md)
37. [agent_skill_bundle](modules/agent_skill_bundle.md)
38. [agent_team_setup](modules/agent_team_setup.md)
39. [schemas_autonomy](modules/schemas_autonomy.md)
40. [schemas_common](modules/schemas_common.md)
41. [schemas_github](modules/schemas_github.md)
42. [schemas_intake](modules/schemas_intake.md)
43. [schemas_label](modules/schemas_label.md)
44. [schemas_plan_share](modules/schemas_plan_share.md)
45. [planning_inputs](modules/planning_inputs.md)
46. [schemas_calendar](modules/schemas_calendar.md)
47. [schemas_saved_view](modules/schemas_saved_view.md)
48. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
49. [schemas_session](modules/schemas_session.md)
50. [snapshot](modules/snapshot.md)
51. [schemas_system_settings](modules/schemas_system_settings.md)
52. [schemas_email_settings](modules/schemas_email_settings.md)
53. [schemas_task_brief](modules/schemas_task_brief.md)
54. [schemas_llm](modules/schemas_llm.md)
55. [schemas_task_domain](modules/schemas_task_domain.md)
56. [schemas_team](modules/schemas_team.md)
57. [schemas_template](modules/schemas_template.md)
58. [schemas_work_metrics](modules/schemas_work_metrics.md)
59. [schemas_iteration](modules/schemas_iteration.md)
60. [schemas_project](modules/schemas_project.md)
61. [schemas_release](modules/schemas_release.md)
62. [security](modules/security.md)
63. [agent_routing_policy](modules/agent_routing_policy.md)
64. [agent_routing](modules/agent_routing.md)
65. [agent_routing_rollout](modules/agent_routing_rollout.md)
66. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
67. [language_service](modules/language_service.md)
68. [scheduling_rules_service](modules/scheduling_rules_service.md)
69. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
70. [upgrade_service](modules/upgrade_service.md)
71. [upgrade](modules/upgrade.md)
72. [sql_semantics](modules/sql_semantics.md)
73. [exceptions](modules/exceptions.md)
74. [text_similarity](modules/text_similarity.md)
75. [time](modules/time.md)
76. [observability](modules/observability.md)
77. [app_database](modules/app_database.md)
78. [models_agent](modules/models_agent.md)
79. [models_autonomy](modules/models_autonomy.md)
80. [models_calendar](modules/models_calendar.md)
81. [models_database_migration](modules/models_database_migration.md)
82. [models_external_link](modules/models_external_link.md)
83. [models_github](modules/models_github.md)
84. [models_identity](modules/models_identity.md)
85. [models_iteration](modules/models_iteration.md)
86. [models_label](modules/models_label.md)
87. [models_outbound_webhook](modules/models_outbound_webhook.md)
88. [models_plan_share](modules/models_plan_share.md)
89. [models_release](modules/models_release.md)
90. [models_project](modules/models_project.md)
91. [models_request_source](modules/models_request_source.md)
92. [models_saved_view](modules/models_saved_view.md)
93. [models_system_settings](modules/models_system_settings.md)
94. [models_task](modules/models_task.md)
95. [recovery](modules/recovery.md)
96. [models_task_brief](modules/models_task_brief.md)
97. [task_status_log](modules/task_status_log.md)
98. [team_member](modules/team_member.md)
99. [models_template](modules/models_template.md)
100. [models_triage](modules/models_triage.md)
101. [user_session](modules/user_session.md)
102. [models___init__](modules/models___init__.md)
103. [catalog](modules/catalog.md)
104. [database_migration_canonical](modules/database_migration_canonical.md)
105. [source](modules/source.md)
106. [transfer](modules/transfer.md)
107. [cli_database_migration](modules/cli_database_migration.md)
108. [database_migration___init__](modules/database_migration___init__.md)
109. [migrations_env](modules/migrations_env.md)
110. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
111. [calendar_service](modules/calendar_service.md)
112. [calendars](modules/calendars.md)
113. [identity_service](modules/identity_service.md)
114. [iteration_service](modules/iteration_service.md)
115. [iterations](modules/iterations.md)
116. [label_service](modules/label_service.md)
117. [labels](modules/labels.md)
118. [saved_view_service](modules/saved_view_service.md)
119. [session_service](modules/session_service.md)
120. [http_authority](modules/http_authority.md)
121. [routers_identity](modules/routers_identity.md)
122. [saved_views](modules/saved_views.md)
123. [routers_session](modules/routers_session.md)
124. [task_brief_service](modules/task_brief_service.md)
125. [task_context_revision_service](modules/task_context_revision_service.md)
126. [task_domain_service](modules/task_domain_service.md)
127. [task_recovery_service](modules/task_recovery_service.md)
128. [team_service](modules/team_service.md)
129. [routers_team](modules/routers_team.md)
130. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
131. [snapshot_service](modules/snapshot_service.md)
132. [plan_share_service](modules/plan_share_service.md)
133. [plan_shares](modules/plan_shares.md)
134. [template_service](modules/template_service.md)
135. [templates](modules/templates.md)
136. [services_work_metrics](modules/services_work_metrics.md)
137. [import_parser](modules/import_parser.md)
138. [url_policy](modules/url_policy.md)
139. [schemas_external_link](modules/schemas_external_link.md)
140. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
141. [schemas_request_source](modules/schemas_request_source.md)
142. [schemas_task](modules/schemas_task.md)
143. [schemas_gantt](modules/schemas_gantt.md)
144. [task_detail](modules/task_detail.md)
145. [schemas_triage](modules/schemas_triage.md)
146. [schemas___init__](modules/schemas___init__.md)
147. [schemas_agent](modules/schemas_agent.md)
148. [agent_readiness](modules/agent_readiness.md)
149. [llm_service](modules/llm_service.md)
150. [system_settings_service](modules/system_settings_service.md)
151. [routers_system_settings](modules/routers_system_settings.md)
152. [email_settings_service](modules/email_settings_service.md)
153. [routers_email_settings](modules/routers_email_settings.md)
154. [notification_service](modules/notification_service.md)
155. [outbound_webhook_service](modules/outbound_webhook_service.md)
156. [worker](modules/worker.md)
157. [outbound_webhooks](modules/outbound_webhooks.md)
158. [external_link_service](modules/external_link_service.md)
159. [github_status_service](modules/github_status_service.md)
160. [request_source_service](modules/request_source_service.md)
161. [request_sources](modules/request_sources.md)
162. [project_service](modules/project_service.md)
163. [task_detail_service](modules/task_detail_service.md)
164. [task_import_service](modules/task_import_service.md)
165. [task_service](modules/task_service.md)
166. [export](modules/export.md)
167. [snapshots](modules/snapshots.md)
168. [routers_task_domain](modules/routers_task_domain.md)
169. [agent_routing_observability](modules/agent_routing_observability.md)
170. [agent_service](modules/agent_service.md)
171. [agent_skill_bundles](modules/agent_skill_bundles.md)
172. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
173. [agent_routing_service](modules/agent_routing_service.md)
174. [agent_team_setup_service](modules/agent_team_setup_service.md)
175. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
176. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
177. [github_status_automation_service](modules/github_status_automation_service.md)
178. [release_service](modules/release_service.md)
179. [projects](modules/projects.md)
180. [scheduler_service](modules/scheduler_service.md)
181. [routers_gantt](modules/routers_gantt.md)
182. [routers_llm](modules/routers_llm.md)
183. [agent_planning_service](modules/agent_planning_service.md)
184. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
185. [tasks](modules/tasks.md)
186. [task_status_service](modules/task_status_service.md)
187. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
188. [triage_service](modules/triage_service.md)
189. [routers_triage](modules/routers_triage.md)
190. [agent_work_service](modules/agent_work_service.md)
191. [mcp_agent_tools](modules/mcp_agent_tools.md)
192. [mcp_server](modules/mcp_server.md)
193. [routers_agent](modules/routers_agent.md)
194. [routers_agent_planning](modules/routers_agent_planning.md)
195. [agent_catalog](modules/agent_catalog.md)
196. [github_webhook_service](modules/github_webhook_service.md)
197. [routers_github](modules/routers_github.md)
198. [web_intake_service](modules/web_intake_service.md)
199. [routers_intake](modules/routers_intake.md)
200. [app_main](modules/app_main.md)
201. [routers___init__](modules/routers___init__.md)
202. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
203. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
204. [test_server_acceptance](modules/test_server_acceptance.md)
205. [test_work_package_service](modules/test_work_package_service.md)
206. [test_database_configuration](modules/test_database_configuration.md)
207. [test_deployment_topology](modules/test_deployment_topology.md)
208. [test_observability](modules/test_observability.md)
209. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
210. [test_query_boundaries](modules/test_query_boundaries.md)
211. [test_runtime_policy](modules/test_runtime_policy.md)
212. [test_schema_behavior](modules/test_schema_behavior.md)
213. [test_cutover_evidence](modules/test_cutover_evidence.md)
214. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
215. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
216. [test_source_preflight](modules/test_source_preflight.md)
217. [test_transfer_catalog](modules/test_transfer_catalog.md)
218. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
219. [0001_wave0_probe](modules/0001_wave0_probe.md)
220. [test_initial_schema](modules/test_initial_schema.md)
221. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
222. [test_load_tooling](modules/test_load_tooling.md)
223. [support_database](modules/support_database.md)
224. [delivery](modules/delivery.md)
225. [factories](modules/factories.md)
226. [faults](modules/faults.md)
227. [schema](modules/schema.md)
228. [support___init__](modules/support___init__.md)
229. [conftest](modules/conftest.md)
230. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
231. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
232. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
233. [transactions](modules/transactions.md)
234. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
235. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
236. [test_agent_routing_data](modules/test_agent_routing_data.md)
237. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
238. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
239. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
240. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
241. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
242. [test_agent_routing_service](modules/test_agent_routing_service.md)
243. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
244. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
245. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
246. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
247. [test_agent_team_setup](modules/test_agent_team_setup.md)
248. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
249. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
250. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
251. [test_authority_migrations](modules/test_authority_migrations.md)
252. [test_capacity_contract](modules/test_capacity_contract.md)
253. [test_client_contract](modules/test_client_contract.md)
254. [test_database_harness](modules/test_database_harness.md)
255. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
256. [test_managed_authority](modules/test_managed_authority.md)
257. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
258. [test_plan_shares](modules/test_plan_shares.md)
259. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
260. [test_process_roles](modules/test_process_roles.md)
261. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
262. [test_saved_view_service](modules/test_saved_view_service.md)
263. [test_task_domain](modules/test_task_domain.md)
264. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
265. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
266. [test_work_correctness](modules/test_work_correctness.md)
267. [eslint.config](modules/eslint.config.md)
268. [postcss.config](modules/postcss.config.md)
269. [Button](modules/Button.md)
270. [Button.test](modules/Button.test.md)
271. [Checkbox](modules/Checkbox.md)
272. [CollapsibleSection](modules/CollapsibleSection.md)
273. [Input](modules/Input.md)
274. [Input.test](modules/Input.test.md)
275. [dialogLayer](modules/dialogLayer.md)
276. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
277. [Modal](modules/Modal.md)
278. [ConfirmDialog](modules/ConfirmDialog.md)
279. [useConfirmDialog](modules/useConfirmDialog.md)
280. [WorkFreshness](modules/WorkFreshness.md)
281. [toast](modules/toast.md)
282. [ToastProvider](modules/ToastProvider.md)
283. [Breadcrumbs](modules/Breadcrumbs.md)
284. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
285. [commandMenuEvents](modules/commandMenuEvents.md)
286. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
287. [SortableTaskItem](modules/SortableTaskItem.md)
288. [useDraftDismissal](modules/useDraftDismissal.md)
289. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
290. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
291. [InlineEmptyState](modules/InlineEmptyState.md)
292. [MasterProgress](modules/MasterProgress.md)
293. [MasterProgress.test](modules/MasterProgress.test.md)
294. [OverflowMenu](modules/OverflowMenu.md)
295. [PageLayout](modules/PageLayout.md)
296. [SectionCard](modules/SectionCard.md)
297. [SlideOverDrawer](modules/SlideOverDrawer.md)
298. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
299. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
300. [StickyRail](modules/StickyRail.md)
301. [index](modules/index.md)
302. [overviewTaskThread](modules/overviewTaskThread.md)
303. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
304. [planningReturn](modules/planningReturn.md)
305. [PlanReturnBar](modules/PlanReturnBar.md)
306. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
307. [workQueryFreshness](modules/workQueryFreshness.md)
308. [resources.en](modules/resources.en.md)
309. [i18n](modules/i18n.md)
310. [dateLocale](modules/dateLocale.md)
311. [InteractiveCalendar](modules/InteractiveCalendar.md)
312. [resources.ru](modules/resources.ru.md)
313. [i18n.test](modules/i18n.test.md)
314. [routeModules](modules/routeModules.md)
315. [DocumentMetadata](modules/DocumentMetadata.md)
316. [workspaces](modules/workspaces.md)
317. [helpContexts](modules/helpContexts.md)
318. [workspaces.test](modules/workspaces.test.md)
319. [LandingPage](modules/LandingPage.md)
320. [NotFoundPage](modules/NotFoundPage.md)
321. [healthService](modules/healthService.md)
322. [SystemHealthPanel](modules/SystemHealthPanel.md)
323. [iterationStore](modules/iterationStore.md)
324. [themeStore](modules/themeStore.md)
325. [planning-masters.test](modules/planning-masters.test.md)
326. [accessibilityInvariants](modules/accessibilityInvariants.md)
327. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
328. [renderWithProviders](modules/renderWithProviders.md)
329. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
330. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
331. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
332. [OverflowMenu.test](modules/OverflowMenu.test.md)
333. [renderWithProviders.test](modules/renderWithProviders.test.md)
334. [setup](modules/setup.md)
335. [types_calendar](modules/types_calendar.md)
336. [types_label](modules/types_label.md)
337. [outboundWebhook](modules/outboundWebhook.md)
338. [requestSource](modules/requestSource.md)
339. [savedView](modules/savedView.md)
340. [schedulingRules](modules/schedulingRules.md)
341. [ConstraintsPanel](modules/ConstraintsPanel.md)
342. [schedulingDisplay](modules/schedulingDisplay.md)
343. [EffortModifierCard](modules/EffortModifierCard.md)
344. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
345. [SchedulingPassCard](modules/SchedulingPassCard.md)
346. [systemSettings](modules/systemSettings.md)
347. [emailSettings](modules/emailSettings.md)
348. [types_team](modules/types_team.md)
349. [types_task](modules/types_task.md)
350. [types_triage](modules/types_triage.md)
351. [KanbanCard](modules/KanbanCard.md)
352. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
353. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
354. [tone](modules/tone.md)
355. [KanbanColumn](modules/KanbanColumn.md)
356. [Pill](modules/Pill.md)
357. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
358. [tone.test](modules/tone.test.md)
359. [attentionRanking](modules/attentionRanking.md)
360. [attentionRanking.test](modules/attentionRanking.test.md)
361. [planningTaskIssues](modules/planningTaskIssues.md)
362. [planningMasters_masters](modules/planningMasters_masters.md)
363. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
364. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
365. [types_agent](modules/types_agent.md)
366. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
367. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
368. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
369. [statusScopes](modules/statusScopes.md)
370. [statusScopes.test](modules/statusScopes.test.md)
371. [modelAwareRouting](modules/modelAwareRouting.md)
372. [types_github](modules/types_github.md)
373. [types_template](modules/types_template.md)
374. [seedDisplay](modules/seedDisplay.md)
375. [workMetrics](modules/workMetrics.md)
376. [WorkMetricsLine](modules/WorkMetricsLine.md)
377. [types_iteration](modules/types_iteration.md)
378. [types_gantt](modules/types_gantt.md)
379. [types_project](modules/types_project.md)
380. [projectStatusStyles](modules/projectStatusStyles.md)
381. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
382. [types_release](modules/types_release.md)
383. [agentAccess](modules/agentAccess.md)
384. [useAgentAccess](modules/useAgentAccess.md)
385. [apiError](modules/apiError.md)
386. [QueryState](modules/QueryState.md)
387. [taskEditorContract](modules/taskEditorContract.md)
388. [TaskBriefEditor](modules/TaskBriefEditor.md)
389. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
390. [taskDraftStorage](modules/taskDraftStorage.md)
391. [adminAccess](modules/adminAccess.md)
392. [api](modules/api.md)
393. [identityService](modules/identityService.md)
394. [identityContext](modules/identityContext.md)
395. [useAdminAccess](modules/useAdminAccess.md)
396. [AdminAccessPanel](modules/AdminAccessPanel.md)
397. [AdminAccessGate](modules/AdminAccessGate.md)
398. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
399. [agentService](modules/agentService.md)
400. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
401. [agentService.test](modules/agentService.test.md)
402. [calendarService](modules/calendarService.md)
403. [emailSettingsService](modules/emailSettingsService.md)
404. [exportService](modules/exportService.md)
405. [ganttService](modules/ganttService.md)
406. [githubService](modules/githubService.md)
407. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
408. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
409. [iterationService](modules/iterationService.md)
410. [IterationSelector](modules/IterationSelector.md)
411. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
412. [SidebarIterationCard](modules/SidebarIterationCard.md)
413. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
414. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
415. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
416. [labelService](modules/labelService.md)
417. [LabelSelector](modules/LabelSelector.md)
418. [outboundWebhookService](modules/outboundWebhookService.md)
419. [planShareService](modules/planShareService.md)
420. [projectService](modules/projectService.md)
421. [releaseService](modules/releaseService.md)
422. [ReleaseForm](modules/ReleaseForm.md)
423. [requestSourceService](modules/requestSourceService.md)
424. [savedViewService](modules/savedViewService.md)
425. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
426. [AppSidebar](modules/AppSidebar.md)
427. [AppSidebar.test](modules/AppSidebar.test.md)
428. [schedulingRulesService](modules/schedulingRulesService.md)
429. [sessionService](modules/sessionService.md)
430. [snapshotService](modules/snapshotService.md)
431. [systemSettingsService](modules/systemSettingsService.md)
432. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
433. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
434. [taskService](modules/taskService.md)
435. [ImportTasksModal](modules/ImportTasksModal.md)
436. [TaskContextSummary](modules/TaskContextSummary.md)
437. [TaskDependencySelector](modules/TaskDependencySelector.md)
438. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
439. [TaskWorkPanel](modules/TaskWorkPanel.md)
440. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
441. [teamService](modules/teamService.md)
442. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
443. [TaskFiltersBar](modules/TaskFiltersBar.md)
444. [taskFilterDefaults](modules/taskFilterDefaults.md)
445. [ImportTeamModal](modules/ImportTeamModal.md)
446. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
447. [TeamForm](modules/TeamForm.md)
448. [TeamForm.test](modules/TeamForm.test.md)
449. [TeamProfileManager](modules/TeamProfileManager.md)
450. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
451. [IdentityProvider](modules/IdentityProvider.md)
452. [UserSessionBadge](modules/UserSessionBadge.md)
453. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
454. [CalendarPage](modules/CalendarPage.md)
455. [templateService](modules/templateService.md)
456. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
457. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
458. [triageService](modules/triageService.md)
459. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
460. [usePlanningReadiness](modules/usePlanningReadiness.md)
461. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
462. [copyText](modules/copyText.md)
463. [focusLifecycle](modules/focusLifecycle.md)
464. [focusLifecycle.test](modules/focusLifecycle.test.md)
465. [formatDate](modules/formatDate.md)
466. [TaskStatusFlow](modules/TaskStatusFlow.md)
467. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
468. [IterationForm](modules/IterationForm.md)
469. [IterationForm.test](modules/IterationForm.test.md)
470. [IterationList](modules/IterationList.md)
471. [NotificationsPanel](modules/NotificationsPanel.md)
472. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
473. [StatusChangeControl](modules/StatusChangeControl.md)
474. [VacationManager](modules/VacationManager.md)
475. [TeamList](modules/TeamList.md)
476. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
477. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
478. [AnalyticsPage](modules/AnalyticsPage.md)
479. [IterationsPage](modules/IterationsPage.md)
480. [PlanMasterPage](modules/PlanMasterPage.md)
481. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
482. [PlanPage](modules/PlanPage.md)
483. [PlanPage.test](modules/PlanPage.test.md)
484. [PlanSharePage](modules/PlanSharePage.md)
485. [PlanSharePage.test](modules/PlanSharePage.test.md)
486. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
487. [TeamPage](modules/TeamPage.md)
488. [modelRouting](modules/modelRouting.md)
489. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
490. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
491. [modelRouting.test](modules/modelRouting.test.md)
492. [protectedQueries](modules/protectedQueries.md)
493. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
494. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
495. [AgentAccessPanel](modules/AgentAccessPanel.md)
496. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
497. [AgentModelAdministration](modules/AgentModelAdministration.md)
498. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
499. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
500. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
501. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
502. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
503. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
504. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
505. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
506. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
507. [AgentPipelinePage](modules/AgentPipelinePage.md)
508. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
509. [safeUrl](modules/safeUrl.md)
510. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
511. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
512. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
513. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
514. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
515. [OverviewPage](modules/OverviewPage.md)
516. [OverviewPage.test](modules/OverviewPage.test.md)
517. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
518. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
519. [CommandMenu](modules/CommandMenu.md)
520. [CommandMenu.test](modules/CommandMenu.test.md)
521. [ContextHelp](modules/ContextHelp.md)
522. [AppTopNav](modules/AppTopNav.md)
523. [AppShell](modules/AppShell.md)
524. [App](modules/App.md)
525. [AppShell.test](modules/AppShell.test.md)
526. [AppTopNav.test](modules/AppTopNav.test.md)
527. [ContextHelp.test](modules/ContextHelp.test.md)
528. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
529. [src_main](modules/src_main.md)
530. [SettingsPage](modules/SettingsPage.md)
531. [SettingsPage.test](modules/SettingsPage.test.md)
532. [taskFilters](modules/taskFilters.md)
533. [taskFilters.test](modules/taskFilters.test.md)
534. [teamMemberLabels](modules/teamMemberLabels.md)
535. [InitiativeForm](modules/InitiativeForm.md)
536. [RoadmapPage](modules/RoadmapPage.md)
537. [RoadmapPage.test](modules/RoadmapPage.test.md)
538. [templateDefaults](modules/templateDefaults.md)
539. [ProjectForm](modules/ProjectForm.md)
540. [TaskForm](modules/TaskForm.md)
541. [TaskEditModal](modules/TaskEditModal.md)
542. [GanttChart](modules/GanttChart.md)
543. [GanttChart.test](modules/GanttChart.test.md)
544. [GuardedTaskModal](modules/GuardedTaskModal.md)
545. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
546. [ProjectTaskTree](modules/ProjectTaskTree.md)
547. [TaskForm.test](modules/TaskForm.test.md)
548. [GanttPage](modules/GanttPage.md)
549. [GanttPage.test](modules/GanttPage.test.md)
550. [ProjectDetailPage](modules/ProjectDetailPage.md)
551. [ProjectsPage](modules/ProjectsPage.md)
552. [ProjectsPage.test](modules/ProjectsPage.test.md)
553. [TriagePage](modules/TriagePage.md)
554. [visibleWork](modules/visibleWork.md)
555. [KanbanBoard](modules/KanbanBoard.md)
556. [KanbanBoard.test](modules/KanbanBoard.test.md)
557. [TaskList](modules/TaskList.md)
558. [SavedViewsControl](modules/SavedViewsControl.md)
559. [TaskList.test](modules/TaskList.test.md)
560. [TasksPage](modules/TasksPage.md)
561. [TasksPage.test](modules/TasksPage.test.md)
562. [visibleWork.test](modules/visibleWork.test.md)
563. [tailwind.config](modules/tailwind.config.md)
564. [vite.config](modules/vite.config.md)
565. [vitest.config](modules/vitest.config.md)
566. [create_agent_actor](modules/create_agent_actor.md)
567. [generate_workchord_keys](modules/generate_workchord_keys.md)
568. [setup_agent_team](modules/setup_agent_team.md)
569. [build_agent_skills](modules/build_agent_skills.md)
570. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
571. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
572. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
573. [postgres_runtime](modules/postgres_runtime.md)
574. [run_android_checks](modules/run_android_checks.md)
575. [run_disposable_checks](modules/run_disposable_checks.md)
576. [serve_disposable_api](modules/serve_disposable_api.md)
577. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
578. [test_native_runtimes](modules/test_native_runtimes.md)
579. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
580. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
581. [generate_client_contract](modules/generate_client_contract.md)
582. [load_common](modules/load_common.md)
583. [collect](modules/collect.md)
584. [result](modules/result.md)
585. [compare](modules/compare.md)
586. [finalize](modules/finalize.md)
587. [qualify](modules/qualify.md)
588. [resilience](modules/resilience.md)
589. [run](modules/run.md)
590. [seal](modules/seal.md)
591. [seed](modules/seed.md)

## Module-level side effects

| Module | Import-time calls |
|--------|-------------------|
| [build_identity](modules/build_identity.md) | `BUILD_IDENTITY_PATH = Path` |
| [app_database](modules/app_database.md) | `settings = get_settings`, `database_configuration = parse_database_configuration`, `engine = create_async_engine`, `install_database_instrumentation`, `async_session_maker = async_sessionmaker` |
| [database_config](modules/database_config.md) | `_POSTGRESQL_CONNECTION_QUERY_KEYS = frozenset`, `_APPLICATION_NAME_PATTERN = re.compile`, `_POSTGRESQL_ROLE_PATTERN = re.compile` |
| [catalog](modules/catalog.md) | `TARGET_OWNED_TABLES = frozenset`, `TEXT_JSON_COLUMNS = frozenset` |
| [database_migration_closeout](modules/database_migration_closeout.md) | `POSTGRESQL_VERSION_PATTERN = re.compile`, `SAFE_IDENTIFIER_PATTERN = re.compile`, `APPLICATION_VERSION_PATTERN = re.compile`, `RELEASE_GATE_IDS = tuple`, `NON_WAIVABLE_TASKS = frozenset`, `NON_WAIVABLE_GATES = frozenset` |
| [database_migration_cutover](modules/database_migration_cutover.md) | `SHA256_PATTERN = re.compile`, `COMMIT_PATTERN = re.compile`, `IMAGE_PATTERN = re.compile`, `GATE_IDS = tuple`, `OPERATOR_ROLES = frozenset`, `DOCUMENTATION_CHECKS = frozenset`, `QUALIFICATION_GATES = frozenset` |
| [source](modules/source.md) | `DRAIN_EVIDENCE_MAX_AGE = timedelta` |
| [transfer](modules/transfer.md) | `MIGRATION_LOADER_LOCK_NAMESPACE = int.from_bytes`, `REPAIR_OWNED_TABLES = frozenset` |
| [database_runtime](modules/database_runtime.md) | `logger = logging.getLogger`, `T = TypeVar`, `RETRYABLE_TRANSACTION_SQLSTATES = frozenset`, `RETRYABLE_CONNECTION_SQLSTATES = frozenset` |
| [app_main](modules/app_main.md) | `settings = get_settings`, `app = FastAPI`, `app.include_router`, `app.include_router`, `app.add_middleware`, `app.add_middleware`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `mount_mcp_http` |
| [maintenance](modules/maintenance.md) | `SAFE_HTTP_METHODS = frozenset`, `_CORRELATION_ID_PATTERN = re.compile` |
| [mcp_agent_tools](modules/mcp_agent_tools.md) | `_AGENT_ASSIGNMENT_CREATE_ADAPTER = TypeAdapter`, `_AGENT_ASSIGNMENT_UPDATE_ADAPTER = TypeAdapter`, `_AGENT_WORK_BEGIN_ADAPTER = TypeAdapter` |
| [mcp_server](modules/mcp_server.md) | `_http_agent_key = ContextVar`, `mcp = create_mcp_server` |
| [migrations_env](modules/migrations_env.md) | `settings = get_settings`, `database_configuration = parse_database_configuration`, `config.set_main_option`, `fileConfig`, `run_migrations_offline`, `run_migrations_online` |
| [recovery](modules/recovery.md) | `event.listen` |
| [models_release](modules/models_release.md) | `release_tasks = Table` |
| [observability](modules/observability.md) | `logger = logging.getLogger` |
| [routers_agent](modules/routers_agent.md) | `router = APIRouter`, `logger = logging.getLogger` |
| [agent_catalog](modules/agent_catalog.md) | `router = APIRouter` |
| [routers_agent_planning](modules/routers_agent_planning.md) | `router = APIRouter` |
| [agent_skill_bundles](modules/agent_skill_bundles.md) | `router = APIRouter`, `well_known_router = APIRouter` |
| [calendars](modules/calendars.md) | `router = APIRouter` |
| [routers_email_settings](modules/routers_email_settings.md) | `router = APIRouter`, `logger = logging.getLogger` |
| [export](modules/export.md) | `router = APIRouter` |
| [routers_gantt](modules/routers_gantt.md) | `router = APIRouter` |
| [routers_github](modules/routers_github.md) | `router = APIRouter` |
| [routers_identity](modules/routers_identity.md) | `router = APIRouter` |
| [routers_intake](modules/routers_intake.md) | `router = APIRouter` |
| [iterations](modules/iterations.md) | `router = APIRouter` |
| [labels](modules/labels.md) | `router = APIRouter` |
| [routers_llm](modules/routers_llm.md) | `router = APIRouter` |
| [outbound_webhooks](modules/outbound_webhooks.md) | `router = APIRouter` |
| [plan_shares](modules/plan_shares.md) | `router = APIRouter` |
| [projects](modules/projects.md) | `router = APIRouter` |
| [request_sources](modules/request_sources.md) | `router = APIRouter` |
| [saved_views](modules/saved_views.md) | `router = APIRouter` |
| [routers_scheduling_rules](modules/routers_scheduling_rules.md) | `router = APIRouter`, `logger = logging.getLogger` |
| [routers_session](modules/routers_session.md) | `router = APIRouter` |
| [snapshots](modules/snapshots.md) | `router = APIRouter` |
| [routers_system_settings](modules/routers_system_settings.md) | `router = APIRouter` |
| [routers_task_domain](modules/routers_task_domain.md) | `router = APIRouter` |
| [tasks](modules/tasks.md) | `router = APIRouter`, `logger = logging.getLogger` |
| [routers_team](modules/routers_team.md) | `router = APIRouter` |
| [templates](modules/templates.md) | `router = APIRouter` |
| [routers_triage](modules/routers_triage.md) | `router = APIRouter` |
| [runtime_telemetry](modules/runtime_telemetry.md) | `metrics = MetricRegistry`, `activity = RuntimeActivity`, `correlation_id_context = ContextVar` |
| [schemas_agent](modules/schemas_agent.md) | `SUPPORTED_AGENT_SCOPES = frozenset` |
| [agent_routing](modules/agent_routing.md) | `MAX_REASON_CODES = len` |
| [agent_team_setup](modules/agent_team_setup.md) | `SECRET_QUERY_KEYS = frozenset` |
| [schemas_gantt](modules/schemas_gantt.md) | `GanttTask.model_rebuild` |
| [schemas_task](modules/schemas_task.md) | `TaskResponse.model_rebuild` |
| [agent_readiness](modules/agent_readiness.md) | `DEFAULT_AGENT_CAPABILITY_SLUGS = frozenset`, `DESCRIPTION_SIGNAL_PATTERN = re.compile`, `BULLET_PATTERN = re.compile` |
| [agent_routing_observability](modules/agent_routing_observability.md) | `MAX_ROUTING_OPERATIONAL_EXCLUSIONS = min`, `_COMMON_FIELDS = frozenset`, `_INTEGER_FIELDS = frozenset`, `_BOOLEAN_FIELDS = frozenset`, `_DIGEST_FIELDS = frozenset`, `_CODE_LIST_FIELDS = frozenset`, `_EXCLUSION_FIELDS = frozenset` |
| [agent_routing_policy](modules/agent_routing_policy.md) | `MODEL_FAILURE_CATEGORIES = frozenset`, `SERVER_OWNED_ROUTING_SNAPSHOT_SCHEMAS = frozenset`, `CONTEXT_TIER_ORDER = MappingProxyType`, `COST_TIER_ORDER = MappingProxyType`, `LATENCY_TIER_ORDER = MappingProxyType`, `DIFFICULTY_BAND_ORDER = MappingProxyType`, `REVIEW_MODE_ORDER = MappingProxyType`, `ROUTING_SKILL_KEYS = frozenset`, `CAPABILITY_LABEL_SKILL_KEYS = MappingProxyType`, `REASON_CODE_RULES = MappingProxyType`, `ASSESSMENT_REASON_CODES = frozenset`, `VALID_ASSIGNMENT_INTENTS = MappingProxyType` |
| [agent_routing_rollout](modules/agent_routing_rollout.md) | `_BLOCKER_CODE_PATTERN = re.compile`, `_TOPOLOGY_ID_PATTERN = re.compile`, `_topology_readiness_context = ContextVar` |
| [agent_service](modules/agent_service.md) | `ALL_AGENT_SCOPES = sorted` |
| [agent_skill_bundle_service](modules/agent_skill_bundle_service.md) | `logger = logging.getLogger` |
| [agent_work_service](modules/agent_work_service.md) | `logger = logging.getLogger` |
| [assignee_recommendation_service](modules/assignee_recommendation_service.md) | `TOKEN_PATTERN = re.compile` |
| [email_settings_service](modules/email_settings_service.md) | `logger = logging.getLogger` |
| [github_status_service](modules/github_status_service.md) | `logger = logging.getLogger` |
| [language_service](modules/language_service.md) | `_CYRILLIC_RE = re.compile`, `_LATIN_RE = re.compile`, `logger = logging.getLogger` |
| [llm_service](modules/llm_service.md) | `logger = logging.getLogger` |
| [notification_service](modules/notification_service.md) | `logger = logging.getLogger` |
| [outbound_webhook_service](modules/outbound_webhook_service.md) | `logger = logging.getLogger` |
| [scheduler_service](modules/scheduler_service.md) | `logger = logging.getLogger` |
| [scheduling_rules_service](modules/scheduling_rules_service.md) | `logger = logging.getLogger`, `CONDITION_PATTERN = re.compile` |
| [session_service](modules/session_service.md) | `_SESSION_TOKEN_PATTERN = re.compile` |
| [snapshot_service](modules/snapshot_service.md) | `SNAPSHOTS_DIR = Path`, `SNAPSHOT_REASON_PATTERN = re.compile`, `SNAPSHOT_FILENAME_PATTERN = re.compile` |
| [system_settings_service](modules/system_settings_service.md) | `logger = logging.getLogger`, `LEGACY_EMAIL_SETTINGS_FILE = Path` |
| [web_intake_service](modules/web_intake_service.md) | `default_web_intake_rate_limiter = WebIntakeRateLimiter` |
| [text_similarity](modules/text_similarity.md) | `TOKEN_PATTERN = re.compile` |
| [test_autonomy_foundation](modules/test_autonomy_foundation.md) | `NOW = datetime` |
| [test_server_acceptance](modules/test_server_acceptance.md) | `NOW = datetime.now(UTC).replace`, `PRIVATE_KEY = Ed25519PrivateKey.from_private_bytes`, `PUBLIC_KEY_BYTES = PRIVATE_KEY.public_key().public_bytes`, `PUBLIC_KEY_BASE64 = base64.b64encode(PUBLIC_KEY_BYTES).decode` |
| [test_work_package_service](modules/test_work_package_service.md) | `DIGESTS = tuple` |
| [conftest](modules/conftest.md) | `os.environ.setdefault` |
| [postgresql_migrations_env](modules/postgresql_migrations_env.md) | `run_migrations_offline`, `run_migrations_online` |
| [test_load_seed_postgresql](modules/test_load_seed_postgresql.md) | `sys.path.insert` |
| [test_load_tooling](modules/test_load_tooling.md) | `sys.path.insert` |
| [support_database](modules/support_database.md) | `TEST_DATABASE_PATTERN = re.compile`, `TEST_RUNTIME_ROLE_PATTERN = re.compile`, `DEFAULT_POSTGRES_HOSTS = frozenset`, `ADMIN_DATABASES = frozenset` |
| [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md) | `_PROVISION_SPEC = importlib.util.spec_from_file_location`, `provision_actor = importlib.util.module_from_spec`, `_PROVISION_SPEC.loader.exec_module` |
| [test_agent_routing_service](modules/test_agent_routing_service.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md) | `pytestmark = pytest.mark.usefixtures`, `_FIXED_NOW = datetime` |
| [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md) | `SPEC = importlib.util.spec_from_file_location`, `setup_agent_team = importlib.util.module_from_spec`, `SPEC.loader.exec_module` |
| [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md) | `FIXED_NOW = datetime` |
| [App](modules/App.md) | `OverviewPage = lazy`, `LandingPage = lazy`, `PlanPage = lazy`, `PlanMasterPage = lazy`, `PlanSharePage = lazy`, `CalendarPage = lazy`, `IterationsPage = lazy`, `TeamPage = lazy`, `TasksPage = lazy`, `TriagePage = lazy`, `ProjectsPage = lazy`, `ProjectDetailPage = lazy`, `ProjectReleaseDetailPage = lazy`, `RoadmapPage = lazy`, `GanttPage = lazy`, `AnalyticsPage = lazy`, `SettingsPage = lazy`, `AgentPipelinePage = lazy`, `AgentTeamSetupMasterPage = lazy`, `NotFoundPage = lazy` |
| [UserSessionBadge.test](modules/UserSessionBadge.test.md) | `sessionServiceMock = hoisted`, `mock`, `describe` |
| [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md) | `describe` |
| [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md) | `agentServiceMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `dispatchableRoster = map`, `describe` |
| [TaskRoutingPanel](modules/TaskRoutingPanel.md) | `SKILL_CATALOG_READ_SCOPES = Set`, `TEAM_ASSIGNMENT_READ_SCOPES = Set` |
| [Button.test](modules/Button.test.md) | `describe` |
| [Button](modules/Button.md) | `Button = forwardRef` |
| [Checkbox](modules/Checkbox.md) | `Checkbox = forwardRef` |
| [Input.test](modules/Input.test.md) | `describe` |
| [Input](modules/Input.md) | `Input = forwardRef` |
| [dialogLayer](modules/dialogLayer.md) | `focusableSelector = join` |
| [toast](modules/toast.md) | `ToastContext = createContext` |
| [GanttChart.test](modules/GanttChart.test.md) | `ganttServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md) | `t = bind` |
| [IterationForm.test](modules/IterationForm.test.md) | `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `iterationStoreMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [AppShell.test](modules/AppShell.test.md) | `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AppSidebar.test](modules/AppSidebar.test.md) | `savedViewServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [AppSidebar](modules/AppSidebar.md) | `SAVED_VIEW_ROUTE_PATHS = Set` |
| [AppTopNav.test](modules/AppTopNav.test.md) | `planningReadinessMock = hoisted`, `triageServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [CommandMenu.test](modules/CommandMenu.test.md) | `describe` |
| [ContextHelp.test](modules/ContextHelp.test.md) | `describe` |
| [SidebarIterationCard.test](modules/SidebarIterationCard.test.md) | `planningReadinessMock = hoisted`, `mock`, `describe` |
| [PlanReturnBar.test](modules/PlanReturnBar.test.md) | `describe` |
| [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md) | `describe` |
| [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md) | `describe` |
| [ProjectForm](modules/ProjectForm.md) | `projectStatusValues = map`, `projectHealthValues = map` |
| [ProjectTaskTree](modules/ProjectTaskTree.md) | `t = bind` |
| [projectStatusStyles.test](modules/projectStatusStyles.test.md) | `describe` |
| [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md) | `requestSourceServiceMock = hoisted`, `mock`, `describe` |
| [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md) | `t = bind` |
| [AdminAccessPanel.test](modules/AdminAccessPanel.test.md) | `adminAccessHookMock = hoisted`, `adminAccessStorageMock = hoisted`, `mock`, `mock`, `describe` |
| [AgentAccessPanel.test](modules/AgentAccessPanel.test.md) | `agentAccessHookMock = hoisted`, `agentAccessStorageMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [AgentModelAdministration.test](modules/AgentModelAdministration.test.md) | `agentAccessMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [EffortModifierCard.test](modules/EffortModifierCard.test.md) | `describe` |
| [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md) | `adminAccessMock = hoisted`, `emailSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md) | `githubServiceMock = hoisted`, `mock`, `describe` |
| [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md) | `adminAccessMock = hoisted`, `outboundWebhookServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md) | `adminAccessMock = hoisted`, `systemSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md) | `adminAccessMock = hoisted`, `schedulingRulesServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [SchedulingRulesSettings](modules/SchedulingRulesSettings.md) | `SETTINGS_ROW_ID = Symbol` |
| [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md) | `labelServiceMock = hoisted`, `templateServiceMock = hoisted`, `toastMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [KanbanBoard.test](modules/KanbanBoard.test.md) | `dragState = hoisted`, `taskServiceMock = hoisted`, `teamServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [KanbanCard](modules/KanbanCard.md) | `t = bind` |
| [KanbanColumn](modules/KanbanColumn.md) | `t = bind` |
| [SavedViewsControl](modules/SavedViewsControl.md) | `t = bind` |
| [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md) | `describe` |
| [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md) | `t = bind` |
| [TaskBriefEditor.test](modules/TaskBriefEditor.test.md) | `describe` |
| [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md) | `t = bind` |
| [TaskDependencySelector](modules/TaskDependencySelector.md) | `t = bind` |
| [TaskForm.test](modules/TaskForm.test.md) | `api = hoisted`, `mock`, `describe` |
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind` |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | `service = hoisted`, `mock`, `mock`, `describe` |
| [useDraftDismissal.test](modules/useDraftDismissal.test.md) | `it`, `describe` |
| [ImportTeamModal.test](modules/ImportTeamModal.test.md) | `teamServiceMock = hoisted`, `mock`, `describe` |
| [TeamForm.test](modules/TeamForm.test.md) | `teamServiceMock = hoisted`, `mock`, `describe` |
| [TeamProfileManager.test](modules/TeamProfileManager.test.md) | `teamServiceMock = hoisted`, `mock`, `describe` |
| [MasterProgress.test](modules/MasterProgress.test.md) | `describe` |
| [OverflowMenu.test](modules/OverflowMenu.test.md) | `describe` |
| [tone.test](modules/tone.test.md) | `describe` |
| [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md) | `SECRET_FIELDS = Set` |
| [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md) | `describe` |
| [agentTeamSetup_masters](modules/agentTeamSetup_masters.md) | `AGENT_TEAM_STEP_DEFINITIONS = map` |
| [statusScopes.test](modules/statusScopes.test.md) | `describe` |
| [identityContext](modules/identityContext.md) | `IdentityContext = createContext` |
| [attentionRanking.test](modules/attentionRanking.test.md) | `describe`, `describe` |
| [planningMasters_masters.test](modules/planningMasters_masters.test.md) | `describe` |
| [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md) | `describe` |
| [planningNavigationInvalidation](modules/planningNavigationInvalidation.md) | `READINESS_INPUT_QUERY_ROOTS = Set` |
| [planningTaskIssues.test](modules/planningTaskIssues.test.md) | `describe` |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | `describe` |
| [i18n.test](modules/i18n.test.md) | `describe` |
| [src_main](modules/src_main.md) | `queryClient = QueryClient`, `installPlanningNavigationInvalidation`, `installWorkFreshness`, `router = createBrowserRouter`, `render` |
| [workspaces.test](modules/workspaces.test.md) | `describe` |
| [workspaces](modules/workspaces.md) | `PRIMARY_NAV_ITEMS = flatMap` |
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set`, `TASK_STATUSES = Set` |
| [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe` |
| [GanttPage.test](modules/GanttPage.test.md) | `ganttServiceMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [OverviewPage.test](modules/OverviewPage.test.md) | `planningReadinessMock = hoisted`, `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [OverviewPage](modules/OverviewPage.md) | `doneStatuses = Set`, `invalidCachedStatuses = Set`, `operationalAttentionIds = Set`, `commitmentAttentionIds = Set` |
| [PlanMasterPage.test](modules/PlanMasterPage.test.md) | `planningReadinessMock = hoisted`, `planShareServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [PlanPage.test](modules/PlanPage.test.md) | `planningReadinessMock = hoisted`, `mock`, `describe` |
| [PlanSharePage.test](modules/PlanSharePage.test.md) | `planShareServiceMock = hoisted`, `mock`, `describe` |
| [ProjectDetailPage](modules/ProjectDetailPage.md) | `t = bind` |
| [ProjectsPage.test](modules/ProjectsPage.test.md) | `projectServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [RoadmapPage.test](modules/RoadmapPage.test.md) | `projectServiceMock = hoisted`, `mock`, `describe` |
| [RoadmapPage](modules/RoadmapPage.md) | `t = bind` |
| [SettingsPage.test](modules/SettingsPage.test.md) | `themeStoreMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [SettingsPage](modules/SettingsPage.md) | `SETTINGS_DESTINATIONS = flatMap` |
| [TasksPage.test](modules/TasksPage.test.md) | `iterationServiceMock = hoisted`, `iterationStoreMock = hoisted`, `savedViewServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TriagePage](modules/TriagePage.md) | `t = bind` |
| [agentService.test](modules/agentService.test.md) | `mock`, `mockedApi = mocked`, `describe` |
| [api](modules/api.md) | `api = create`, `use`, `use` |
| [iterationStore](modules/iterationStore.md) | `useIterationStore = create<IterationStore>()` |
| [themeStore](modules/themeStore.md) | `useThemeStore = create<ThemeState>()` |
| [planning-masters.test](modules/planning-masters.test.md) | `planningMastersCss = readFileSync`, `agentTeamMasterSource = readFileSync`, `describe` |
| [accessibilityInvariants.test](modules/accessibilityInvariants.test.md) | `describe` |
| [renderWithProviders.test](modules/renderWithProviders.test.md) | `describe` |
| [setup](modules/setup.md) | `afterEach` |
| [focusLifecycle.test](modules/focusLifecycle.test.md) | `describe` |
| [modelRouting.test](modules/modelRouting.test.md) | `describe` |
| [modelRouting](modules/modelRouting.md) | `ADVANCED_REASON_CODES = Set`, `INDEPENDENT_REASON_CODES = Set`, `STANDARD_REVIEW_REASON_CODES = Set` |
| [selectWorkNowTasks](modules/selectWorkNowTasks.md) | `doneStatuses = Set` |
| [taskFilters.test](modules/taskFilters.test.md) | `describe` |
| [teamMemberLabels](modules/teamMemberLabels.md) | `t = bind` |
| [visibleWork.test](modules/visibleWork.test.md) | `it`, `it`, `it` |
| [build_agent_skills](modules/build_agent_skills.md) | `SEMVER_RE = re.compile`, `SKILL_NAME_RE = re.compile`, `COMPATIBILITY_RE = re.compile`, `MARKDOWN_LINK_RE = re.compile`, `URL_RE = re.compile` |
| [check_postgresql_documentation](modules/check_postgresql_documentation.md) | `LINK_PATTERN = re.compile`, `SHELL_FENCE_PATTERN = re.compile`, `LIVE_SQLITE_COPY_PATTERN = re.compile` |
| [serve_disposable_oidc](modules/serve_disposable_oidc.md) | `url = assert_safe_test_database_url`, `issuer = os.environ.get`, `key = rsa.generate_private_key`, `jwk = json.loads`, `jwk['kid'] = 'disposable-key'`, `app = FastAPI` |
| [test_native_runtimes](modules/test_native_runtimes.md) | `sys.path.insert` |
| [collect](modules/collect.md) | `sys.path.insert` |
| [compare](modules/compare.md) | `sys.path.insert` |
| [finalize](modules/finalize.md) | `sys.path.insert` |
| [qualify](modules/qualify.md) | `sys.path.insert`, `IMAGE_PATTERN = re.compile`, `COMMIT_PATTERN = re.compile`, `RUN_GATES = frozenset`, `REPORT_GATES = frozenset`, `SHA256_PATTERN = re.compile` |
| [resilience](modules/resilience.md) | `sys.path.insert` |
| [run](modules/run.md) | `sys.path.insert`, `RETRYABLE_STATUSES = frozenset` |
| [seal](modules/seal.md) | `sys.path.insert` |
| [seed](modules/seed.md) | `sys.path.insert` |

## Factory / wiring

<!-- Heuristic, name-based detection of app-factory / wiring functions. -->

| Function | Kind | Module |
|----------|------|--------|
| `create_agent_assignment` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_agent_model_binding` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_agent_model_catalog_entry` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_agent_project_update` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_planning_iteration` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_planning_milestone` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_planning_profile` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_planning_project` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_planning_task` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_planning_team_member` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_planning_vacation` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_project_backlog_task` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_request_source_link` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_task` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_task_github_link` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_task_routing_assessment` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_triage_item` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
| `create_mcp_http_app` | factory | [mcp_server](modules/mcp_server.md) |
| `create_mcp_server` | factory | [mcp_server](modules/mcp_server.md) |
| `create_agent_actor` | factory | [routers_agent](modules/routers_agent.md) |
| `create_agent_assignment` | factory | [routers_agent](modules/routers_agent.md) |
| `create_agent_project_update` | factory | [routers_agent](modules/routers_agent.md) |
| `create_agent_task` | factory | [routers_agent](modules/routers_agent.md) |
| `create_agent_model_binding` | factory | [agent_catalog](modules/agent_catalog.md) |
| `create_agent_model_catalog_entry` | factory | [agent_catalog](modules/agent_catalog.md) |
| `create_iteration` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_planning_task` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_planning_triage_item` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_profile` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_project` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_project_milestone` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_task_routing_assessment` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_team_member` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_vacation` | factory | [routers_agent_planning](modules/routers_agent_planning.md) |
| `create_calendar` | factory | [calendars](modules/calendars.md) |
| `create_github_status_automation_rule` | factory | [routers_github](modules/routers_github.md) |
| `create_web_intake_item` | factory | [routers_intake](modules/routers_intake.md) |
| `create_iteration` | factory | [iterations](modules/iterations.md) |
| `create_iteration_series` | factory | [iterations](modules/iterations.md) |
| `create_label` | factory | [labels](modules/labels.md) |
| `create_label_group` | factory | [labels](modules/labels.md) |
| `create_outbound_webhook_target` | factory | [outbound_webhooks](modules/outbound_webhooks.md) |
| `create_plan_share` | factory | [plan_shares](modules/plan_shares.md) |
| `create_initiative` | factory | [projects](modules/projects.md) |
| `create_project` | factory | [projects](modules/projects.md) |
| `create_project_milestone` | factory | [projects](modules/projects.md) |
| `create_project_release` | factory | [projects](modules/projects.md) |
| `create_project_update` | factory | [projects](modules/projects.md) |
| `create_request_source_link` | factory | [request_sources](modules/request_sources.md) |
| `create_saved_view` | factory | [saved_views](modules/saved_views.md) |
| `create_backlog_task` | factory | [routers_task_domain](modules/routers_task_domain.md) |
| `create_subtask` | factory | [tasks](modules/tasks.md) |
| `create_task` | factory | [tasks](modules/tasks.md) |
| `create_task_external_link` | factory | [tasks](modules/tasks.md) |
| `create_task_github_external_link` | factory | [tasks](modules/tasks.md) |
| `create_team_member` | factory | [routers_team](modules/routers_team.md) |
| `create_team_member_profile` | factory | [routers_team](modules/routers_team.md) |
| `create_team_member_profile_skill` | factory | [routers_team](modules/routers_team.md) |
| `create_template` | factory | [templates](modules/templates.md) |
| `create_triage_item` | factory | [routers_triage](modules/routers_triage.md) |
| `setup_exception_handlers` | wiring | [exceptions](modules/exceptions.md) |
| `configure_database` | wiring | [conftest](modules/conftest.md) |
| `create_actor` | factory | [create_agent_actor](modules/create_agent_actor.md) |

## Indeterminate (cyclic) groups

> These modules form import cycles, so their relative load order is indeterminate.

- [TaskFiltersBar](modules/TaskFiltersBar.md) ⇄ [taskFilterDefaults](modules/taskFilterDefaults.md)
- [types_task](modules/types_task.md) ⇄ [types_triage](modules/types_triage.md)

## Notes

This page presents a static dependency projection. Lazy imports, conditional initialization, and runtime side effects can change the effective order.

The authority and command modules are cross-cutting runtime boundaries. Intentional late imports connect the model registry, task services, recovery and identity without treating static cycles as proof of runtime order. The extraction remains bounded; unsupported Kotlin/shell sources and unsupported YAML candidates require direct source evidence.

Task, brief, status and recovery services use deliberate late imports to share command ownership without eager initialization cycles. The triage draft projection invokes the canonical renderer at serialization time. Bounded UI detail remains separate from the full graph used for assigned execution and scheduling.

Recovery models register the task deletion hook; the task recovery helper imports TaskService lazily to reuse command version reservations. This keeps the model-registration side effect explicit without treating static import order as runtime execution order.

Database creation order is explicit in the initial Alembic revision and is separate from this module-import projection. PostgreSQL cyclic foreign keys are installed after all participating tables exist; SQLite creates the inline references without inserting application rows.
