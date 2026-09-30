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
32. [20260930_0002_profile_capacity](modules/20260930_0002_profile_capacity.md)
33. [20260930_0003_delivery_dependencies](modules/20260930_0003_delivery_dependencies.md)
34. [20260930_0004_discussion](modules/20260930_0004_discussion.md)
35. [query_limits](modules/query_limits.md)
36. [runtime_telemetry](modules/runtime_telemetry.md)
37. [database_runtime](modules/database_runtime.md)
38. [maintenance](modules/maintenance.md)
39. [schemas_agent_planning](modules/schemas_agent_planning.md)
40. [agent_skill_bundle](modules/agent_skill_bundle.md)
41. [agent_team_setup](modules/agent_team_setup.md)
42. [schemas_autonomy](modules/schemas_autonomy.md)
43. [schemas_common](modules/schemas_common.md)
44. [schemas_github](modules/schemas_github.md)
45. [schemas_intake](modules/schemas_intake.md)
46. [schemas_label](modules/schemas_label.md)
47. [schemas_plan_share](modules/schemas_plan_share.md)
48. [planning_inputs](modules/planning_inputs.md)
49. [schemas_calendar](modules/schemas_calendar.md)
50. [schemas_saved_view](modules/schemas_saved_view.md)
51. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
52. [schemas_session](modules/schemas_session.md)
53. [snapshot](modules/snapshot.md)
54. [schemas_system_settings](modules/schemas_system_settings.md)
55. [schemas_email_settings](modules/schemas_email_settings.md)
56. [schemas_task_brief](modules/schemas_task_brief.md)
57. [schemas_llm](modules/schemas_llm.md)
58. [schemas_task_domain](modules/schemas_task_domain.md)
59. [schemas_team](modules/schemas_team.md)
60. [schemas_template](modules/schemas_template.md)
61. [schemas_work_metrics](modules/schemas_work_metrics.md)
62. [schemas_iteration](modules/schemas_iteration.md)
63. [schemas_project](modules/schemas_project.md)
64. [schemas_release](modules/schemas_release.md)
65. [security](modules/security.md)
66. [agent_routing_policy](modules/agent_routing_policy.md)
67. [agent_routing](modules/agent_routing.md)
68. [agent_routing_rollout](modules/agent_routing_rollout.md)
69. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
70. [language_service](modules/language_service.md)
71. [scheduling_rules_service](modules/scheduling_rules_service.md)
72. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
73. [upgrade_service](modules/upgrade_service.md)
74. [upgrade](modules/upgrade.md)
75. [sql_semantics](modules/sql_semantics.md)
76. [exceptions](modules/exceptions.md)
77. [text_similarity](modules/text_similarity.md)
78. [time](modules/time.md)
79. [observability](modules/observability.md)
80. [app_database](modules/app_database.md)
81. [models_agent](modules/models_agent.md)
82. [models_autonomy](modules/models_autonomy.md)
83. [models_calendar](modules/models_calendar.md)
84. [models_capacity](modules/models_capacity.md)
85. [models_database_migration](modules/models_database_migration.md)
86. [delivery_dependency](modules/delivery_dependency.md)
87. [models_discussion](modules/models_discussion.md)
88. [models_external_link](modules/models_external_link.md)
89. [models_github](modules/models_github.md)
90. [models_identity](modules/models_identity.md)
91. [models_iteration](modules/models_iteration.md)
92. [models_label](modules/models_label.md)
93. [models_outbound_webhook](modules/models_outbound_webhook.md)
94. [models_plan_share](modules/models_plan_share.md)
95. [models_release](modules/models_release.md)
96. [models_project](modules/models_project.md)
97. [models_request_source](modules/models_request_source.md)
98. [models_saved_view](modules/models_saved_view.md)
99. [models_system_settings](modules/models_system_settings.md)
100. [models_task](modules/models_task.md)
101. [recovery](modules/recovery.md)
102. [models_task_brief](modules/models_task_brief.md)
103. [task_status_log](modules/task_status_log.md)
104. [team_member](modules/team_member.md)
105. [models_template](modules/models_template.md)
106. [models_triage](modules/models_triage.md)
107. [user_session](modules/user_session.md)
108. [models___init__](modules/models___init__.md)
109. [catalog](modules/catalog.md)
110. [database_migration_canonical](modules/database_migration_canonical.md)
111. [source](modules/source.md)
112. [transfer](modules/transfer.md)
113. [cli_database_migration](modules/cli_database_migration.md)
114. [database_migration___init__](modules/database_migration___init__.md)
115. [migrations_env](modules/migrations_env.md)
116. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
117. [calendar_service](modules/calendar_service.md)
118. [calendars](modules/calendars.md)
119. [capacity_service](modules/capacity_service.md)
120. [routers_capacity](modules/routers_capacity.md)
121. [delivery_dependency_service](modules/delivery_dependency_service.md)
122. [discussion_service](modules/discussion_service.md)
123. [identity_service](modules/identity_service.md)
124. [iteration_service](modules/iteration_service.md)
125. [iterations](modules/iterations.md)
126. [label_service](modules/label_service.md)
127. [labels](modules/labels.md)
128. [saved_view_service](modules/saved_view_service.md)
129. [session_service](modules/session_service.md)
130. [http_authority](modules/http_authority.md)
131. [routers_identity](modules/routers_identity.md)
132. [saved_views](modules/saved_views.md)
133. [routers_session](modules/routers_session.md)
134. [task_brief_service](modules/task_brief_service.md)
135. [task_context_revision_service](modules/task_context_revision_service.md)
136. [task_domain_service](modules/task_domain_service.md)
137. [task_recovery_service](modules/task_recovery_service.md)
138. [team_service](modules/team_service.md)
139. [routers_team](modules/routers_team.md)
140. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
141. [snapshot_service](modules/snapshot_service.md)
142. [plan_share_service](modules/plan_share_service.md)
143. [plan_shares](modules/plan_shares.md)
144. [template_service](modules/template_service.md)
145. [templates](modules/templates.md)
146. [services_work_metrics](modules/services_work_metrics.md)
147. [import_parser](modules/import_parser.md)
148. [url_policy](modules/url_policy.md)
149. [schemas_external_link](modules/schemas_external_link.md)
150. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
151. [schemas_request_source](modules/schemas_request_source.md)
152. [schemas_task](modules/schemas_task.md)
153. [schemas_gantt](modules/schemas_gantt.md)
154. [task_detail](modules/task_detail.md)
155. [schemas_triage](modules/schemas_triage.md)
156. [schemas___init__](modules/schemas___init__.md)
157. [schemas_agent](modules/schemas_agent.md)
158. [agent_readiness](modules/agent_readiness.md)
159. [llm_service](modules/llm_service.md)
160. [system_settings_service](modules/system_settings_service.md)
161. [routers_system_settings](modules/routers_system_settings.md)
162. [email_settings_service](modules/email_settings_service.md)
163. [routers_email_settings](modules/routers_email_settings.md)
164. [notification_service](modules/notification_service.md)
165. [outbound_webhook_service](modules/outbound_webhook_service.md)
166. [worker](modules/worker.md)
167. [outbound_webhooks](modules/outbound_webhooks.md)
168. [external_link_service](modules/external_link_service.md)
169. [github_status_service](modules/github_status_service.md)
170. [request_source_service](modules/request_source_service.md)
171. [request_sources](modules/request_sources.md)
172. [project_service](modules/project_service.md)
173. [task_detail_service](modules/task_detail_service.md)
174. [task_import_service](modules/task_import_service.md)
175. [task_service](modules/task_service.md)
176. [export](modules/export.md)
177. [snapshots](modules/snapshots.md)
178. [routers_task_domain](modules/routers_task_domain.md)
179. [delivery_dependencies](modules/delivery_dependencies.md)
180. [routers_discussion](modules/routers_discussion.md)
181. [agent_routing_observability](modules/agent_routing_observability.md)
182. [agent_service](modules/agent_service.md)
183. [agent_skill_bundles](modules/agent_skill_bundles.md)
184. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
185. [agent_routing_service](modules/agent_routing_service.md)
186. [agent_team_setup_service](modules/agent_team_setup_service.md)
187. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
188. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
189. [github_status_automation_service](modules/github_status_automation_service.md)
190. [release_service](modules/release_service.md)
191. [projects](modules/projects.md)
192. [scheduler_service](modules/scheduler_service.md)
193. [routers_gantt](modules/routers_gantt.md)
194. [routers_llm](modules/routers_llm.md)
195. [agent_planning_service](modules/agent_planning_service.md)
196. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
197. [tasks](modules/tasks.md)
198. [task_status_service](modules/task_status_service.md)
199. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
200. [triage_service](modules/triage_service.md)
201. [routers_triage](modules/routers_triage.md)
202. [agent_work_service](modules/agent_work_service.md)
203. [mcp_agent_tools](modules/mcp_agent_tools.md)
204. [mcp_server](modules/mcp_server.md)
205. [routers_agent](modules/routers_agent.md)
206. [routers_agent_planning](modules/routers_agent_planning.md)
207. [agent_catalog](modules/agent_catalog.md)
208. [github_webhook_service](modules/github_webhook_service.md)
209. [routers_github](modules/routers_github.md)
210. [web_intake_service](modules/web_intake_service.md)
211. [routers_intake](modules/routers_intake.md)
212. [app_main](modules/app_main.md)
213. [routers___init__](modules/routers___init__.md)
214. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
215. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
216. [test_server_acceptance](modules/test_server_acceptance.md)
217. [test_work_package_service](modules/test_work_package_service.md)
218. [test_database_configuration](modules/test_database_configuration.md)
219. [test_deployment_topology](modules/test_deployment_topology.md)
220. [test_observability](modules/test_observability.md)
221. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
222. [test_query_boundaries](modules/test_query_boundaries.md)
223. [test_runtime_policy](modules/test_runtime_policy.md)
224. [test_schema_behavior](modules/test_schema_behavior.md)
225. [test_cutover_evidence](modules/test_cutover_evidence.md)
226. [test_documentation_boundary](modules/test_documentation_boundary.md)
227. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
228. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
229. [test_source_preflight](modules/test_source_preflight.md)
230. [test_transfer_catalog](modules/test_transfer_catalog.md)
231. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
232. [0001_wave0_probe](modules/0001_wave0_probe.md)
233. [test_initial_schema](modules/test_initial_schema.md)
234. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
235. [test_load_tooling](modules/test_load_tooling.md)
236. [test_routing_evidence](modules/test_routing_evidence.md)
237. [support_database](modules/support_database.md)
238. [delivery](modules/delivery.md)
239. [factories](modules/factories.md)
240. [faults](modules/faults.md)
241. [schema](modules/schema.md)
242. [support___init__](modules/support___init__.md)
243. [conftest](modules/conftest.md)
244. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
245. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
246. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
247. [transactions](modules/transactions.md)
248. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
249. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
250. [test_agent_routing_data](modules/test_agent_routing_data.md)
251. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
252. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
253. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
254. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
255. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
256. [test_agent_routing_service](modules/test_agent_routing_service.md)
257. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
258. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
259. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
260. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
261. [test_agent_team_setup](modules/test_agent_team_setup.md)
262. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
263. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
264. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
265. [test_authority_migrations](modules/test_authority_migrations.md)
266. [test_capacity_contract](modules/test_capacity_contract.md)
267. [test_client_contract](modules/test_client_contract.md)
268. [test_database_harness](modules/test_database_harness.md)
269. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
270. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
271. [test_managed_authority](modules/test_managed_authority.md)
272. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
273. [test_plan_shares](modules/test_plan_shares.md)
274. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
275. [test_process_roles](modules/test_process_roles.md)
276. [test_profile_capacity](modules/test_profile_capacity.md)
277. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
278. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
279. [test_saved_view_service](modules/test_saved_view_service.md)
280. [test_task_domain](modules/test_task_domain.md)
281. [test_human_work_queries](modules/test_human_work_queries.md)
282. [test_task_discussion](modules/test_task_discussion.md)
283. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
284. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
285. [test_work_correctness](modules/test_work_correctness.md)
286. [eslint.config](modules/eslint.config.md)
287. [postcss.config](modules/postcss.config.md)
288. [Button](modules/Button.md)
289. [Button.test](modules/Button.test.md)
290. [Checkbox](modules/Checkbox.md)
291. [CollapsibleSection](modules/CollapsibleSection.md)
292. [Input](modules/Input.md)
293. [Input.test](modules/Input.test.md)
294. [dialogLayer](modules/dialogLayer.md)
295. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
296. [Modal](modules/Modal.md)
297. [ConfirmDialog](modules/ConfirmDialog.md)
298. [useConfirmDialog](modules/useConfirmDialog.md)
299. [WorkFreshness](modules/WorkFreshness.md)
300. [toast](modules/toast.md)
301. [ToastProvider](modules/ToastProvider.md)
302. [Breadcrumbs](modules/Breadcrumbs.md)
303. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
304. [commandMenuEvents](modules/commandMenuEvents.md)
305. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
306. [SortableTaskItem](modules/SortableTaskItem.md)
307. [useDraftDismissal](modules/useDraftDismissal.md)
308. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
309. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
310. [InlineEmptyState](modules/InlineEmptyState.md)
311. [MasterProgress](modules/MasterProgress.md)
312. [MasterProgress.test](modules/MasterProgress.test.md)
313. [OverflowMenu](modules/OverflowMenu.md)
314. [PageLayout](modules/PageLayout.md)
315. [SectionCard](modules/SectionCard.md)
316. [SlideOverDrawer](modules/SlideOverDrawer.md)
317. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
318. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
319. [StickyRail](modules/StickyRail.md)
320. [index](modules/index.md)
321. [overviewTaskThread](modules/overviewTaskThread.md)
322. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
323. [planningReturn](modules/planningReturn.md)
324. [PlanReturnBar](modules/PlanReturnBar.md)
325. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
326. [workQueryFreshness](modules/workQueryFreshness.md)
327. [teamwork.en](modules/teamwork.en.md)
328. [resources.en](modules/resources.en.md)
329. [i18n](modules/i18n.md)
330. [dateLocale](modules/dateLocale.md)
331. [InteractiveCalendar](modules/InteractiveCalendar.md)
332. [teamwork.ru](modules/teamwork.ru.md)
333. [resources.ru](modules/resources.ru.md)
334. [i18n.test](modules/i18n.test.md)
335. [routeModules](modules/routeModules.md)
336. [DocumentMetadata](modules/DocumentMetadata.md)
337. [workspaces](modules/workspaces.md)
338. [helpContexts](modules/helpContexts.md)
339. [workspaces.test](modules/workspaces.test.md)
340. [LandingPage](modules/LandingPage.md)
341. [NotFoundPage](modules/NotFoundPage.md)
342. [healthService](modules/healthService.md)
343. [SystemHealthPanel](modules/SystemHealthPanel.md)
344. [iterationStore](modules/iterationStore.md)
345. [themeStore](modules/themeStore.md)
346. [planning-masters.test](modules/planning-masters.test.md)
347. [accessibilityInvariants](modules/accessibilityInvariants.md)
348. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
349. [renderWithProviders](modules/renderWithProviders.md)
350. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
351. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
352. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
353. [OverflowMenu.test](modules/OverflowMenu.test.md)
354. [renderWithProviders.test](modules/renderWithProviders.test.md)
355. [setup](modules/setup.md)
356. [types_calendar](modules/types_calendar.md)
357. [types_label](modules/types_label.md)
358. [outboundWebhook](modules/outboundWebhook.md)
359. [requestSource](modules/requestSource.md)
360. [savedView](modules/savedView.md)
361. [schedulingRules](modules/schedulingRules.md)
362. [ConstraintsPanel](modules/ConstraintsPanel.md)
363. [schedulingDisplay](modules/schedulingDisplay.md)
364. [EffortModifierCard](modules/EffortModifierCard.md)
365. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
366. [SchedulingPassCard](modules/SchedulingPassCard.md)
367. [systemSettings](modules/systemSettings.md)
368. [emailSettings](modules/emailSettings.md)
369. [types_team](modules/types_team.md)
370. [types_task](modules/types_task.md)
371. [types_triage](modules/types_triage.md)
372. [KanbanCard](modules/KanbanCard.md)
373. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
374. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
375. [tone](modules/tone.md)
376. [KanbanColumn](modules/KanbanColumn.md)
377. [Pill](modules/Pill.md)
378. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
379. [tone.test](modules/tone.test.md)
380. [attentionRanking](modules/attentionRanking.md)
381. [attentionRanking.test](modules/attentionRanking.test.md)
382. [planningTaskIssues](modules/planningTaskIssues.md)
383. [planningMasters_masters](modules/planningMasters_masters.md)
384. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
385. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
386. [types_agent](modules/types_agent.md)
387. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
388. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
389. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
390. [statusScopes](modules/statusScopes.md)
391. [statusScopes.test](modules/statusScopes.test.md)
392. [modelAwareRouting](modules/modelAwareRouting.md)
393. [types_github](modules/types_github.md)
394. [types_template](modules/types_template.md)
395. [seedDisplay](modules/seedDisplay.md)
396. [workMetrics](modules/workMetrics.md)
397. [WorkMetricsLine](modules/WorkMetricsLine.md)
398. [types_iteration](modules/types_iteration.md)
399. [types_gantt](modules/types_gantt.md)
400. [types_project](modules/types_project.md)
401. [projectStatusStyles](modules/projectStatusStyles.md)
402. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
403. [types_release](modules/types_release.md)
404. [agentAccess](modules/agentAccess.md)
405. [useAgentAccess](modules/useAgentAccess.md)
406. [apiError](modules/apiError.md)
407. [QueryState](modules/QueryState.md)
408. [taskEditorContract](modules/taskEditorContract.md)
409. [TaskBriefEditor](modules/TaskBriefEditor.md)
410. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
411. [taskDraftStorage](modules/taskDraftStorage.md)
412. [adminAccess](modules/adminAccess.md)
413. [api](modules/api.md)
414. [identityService](modules/identityService.md)
415. [identityContext](modules/identityContext.md)
416. [useAdminAccess](modules/useAdminAccess.md)
417. [AdminAccessPanel](modules/AdminAccessPanel.md)
418. [AdminAccessGate](modules/AdminAccessGate.md)
419. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
420. [agentService](modules/agentService.md)
421. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
422. [agentService.test](modules/agentService.test.md)
423. [calendarService](modules/calendarService.md)
424. [PersonCapacity](modules/PersonCapacity.md)
425. [discussionService](modules/discussionService.md)
426. [TaskDiscussion](modules/TaskDiscussion.md)
427. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
428. [emailSettingsService](modules/emailSettingsService.md)
429. [exportService](modules/exportService.md)
430. [ganttService](modules/ganttService.md)
431. [githubService](modules/githubService.md)
432. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
433. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
434. [iterationService](modules/iterationService.md)
435. [IterationSelector](modules/IterationSelector.md)
436. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
437. [SidebarIterationCard](modules/SidebarIterationCard.md)
438. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
439. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
440. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
441. [labelService](modules/labelService.md)
442. [LabelSelector](modules/LabelSelector.md)
443. [outboundWebhookService](modules/outboundWebhookService.md)
444. [planShareService](modules/planShareService.md)
445. [projectService](modules/projectService.md)
446. [releaseService](modules/releaseService.md)
447. [ReleaseForm](modules/ReleaseForm.md)
448. [requestSourceService](modules/requestSourceService.md)
449. [savedViewService](modules/savedViewService.md)
450. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
451. [AppSidebar](modules/AppSidebar.md)
452. [AppSidebar.test](modules/AppSidebar.test.md)
453. [schedulingRulesService](modules/schedulingRulesService.md)
454. [sessionService](modules/sessionService.md)
455. [snapshotService](modules/snapshotService.md)
456. [systemSettingsService](modules/systemSettingsService.md)
457. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
458. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
459. [taskService](modules/taskService.md)
460. [DeliveryDependencies](modules/DeliveryDependencies.md)
461. [ImportTasksModal](modules/ImportTasksModal.md)
462. [TaskContextSummary](modules/TaskContextSummary.md)
463. [TaskDependencySelector](modules/TaskDependencySelector.md)
464. [TaskSearch](modules/TaskSearch.md)
465. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
466. [TaskWorkPanel](modules/TaskWorkPanel.md)
467. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
468. [teamService](modules/teamService.md)
469. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
470. [TaskFiltersBar](modules/TaskFiltersBar.md)
471. [taskFilterDefaults](modules/taskFilterDefaults.md)
472. [ImportTeamModal](modules/ImportTeamModal.md)
473. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
474. [TeamForm](modules/TeamForm.md)
475. [TeamForm.test](modules/TeamForm.test.md)
476. [TeamProfileManager](modules/TeamProfileManager.md)
477. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
478. [IdentityProvider](modules/IdentityProvider.md)
479. [UserSessionBadge](modules/UserSessionBadge.md)
480. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
481. [CalendarPage](modules/CalendarPage.md)
482. [templateService](modules/templateService.md)
483. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
484. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
485. [triageService](modules/triageService.md)
486. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
487. [usePlanningReadiness](modules/usePlanningReadiness.md)
488. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
489. [copyText](modules/copyText.md)
490. [focusLifecycle](modules/focusLifecycle.md)
491. [focusLifecycle.test](modules/focusLifecycle.test.md)
492. [formatDate](modules/formatDate.md)
493. [TaskStatusFlow](modules/TaskStatusFlow.md)
494. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
495. [IterationForm](modules/IterationForm.md)
496. [IterationForm.test](modules/IterationForm.test.md)
497. [IterationList](modules/IterationList.md)
498. [NotificationsPanel](modules/NotificationsPanel.md)
499. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
500. [StatusChangeControl](modules/StatusChangeControl.md)
501. [VacationManager](modules/VacationManager.md)
502. [TeamList](modules/TeamList.md)
503. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
504. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
505. [AnalyticsPage](modules/AnalyticsPage.md)
506. [IterationsPage](modules/IterationsPage.md)
507. [PlanMasterPage](modules/PlanMasterPage.md)
508. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
509. [PlanPage](modules/PlanPage.md)
510. [PlanPage.test](modules/PlanPage.test.md)
511. [PlanSharePage](modules/PlanSharePage.md)
512. [PlanSharePage.test](modules/PlanSharePage.test.md)
513. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
514. [TeamPage](modules/TeamPage.md)
515. [modelRouting](modules/modelRouting.md)
516. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
517. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
518. [modelRouting.test](modules/modelRouting.test.md)
519. [protectedQueries](modules/protectedQueries.md)
520. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
521. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
522. [AgentAccessPanel](modules/AgentAccessPanel.md)
523. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
524. [AgentModelAdministration](modules/AgentModelAdministration.md)
525. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
526. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
527. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
528. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
529. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
530. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
531. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
532. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
533. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
534. [AgentPipelinePage](modules/AgentPipelinePage.md)
535. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
536. [safeUrl](modules/safeUrl.md)
537. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
538. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
539. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
540. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
541. [savedViewState](modules/savedViewState.md)
542. [savedViewState.test](modules/savedViewState.test.md)
543. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
544. [OverviewPage](modules/OverviewPage.md)
545. [OverviewPage.test](modules/OverviewPage.test.md)
546. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
547. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
548. [CommandMenu](modules/CommandMenu.md)
549. [CommandMenu.test](modules/CommandMenu.test.md)
550. [ContextHelp](modules/ContextHelp.md)
551. [AppTopNav](modules/AppTopNav.md)
552. [AppShell](modules/AppShell.md)
553. [App](modules/App.md)
554. [AppShell.test](modules/AppShell.test.md)
555. [AppTopNav.test](modules/AppTopNav.test.md)
556. [ContextHelp.test](modules/ContextHelp.test.md)
557. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
558. [src_main](modules/src_main.md)
559. [SettingsPage](modules/SettingsPage.md)
560. [SettingsPage.test](modules/SettingsPage.test.md)
561. [taskFilters](modules/taskFilters.md)
562. [taskFilters.test](modules/taskFilters.test.md)
563. [teamMemberLabels](modules/teamMemberLabels.md)
564. [InitiativeForm](modules/InitiativeForm.md)
565. [RoadmapPage](modules/RoadmapPage.md)
566. [RoadmapPage.test](modules/RoadmapPage.test.md)
567. [templateDefaults](modules/templateDefaults.md)
568. [ProjectForm](modules/ProjectForm.md)
569. [TaskForm](modules/TaskForm.md)
570. [TaskEditModal](modules/TaskEditModal.md)
571. [GanttChart](modules/GanttChart.md)
572. [GanttChart.test](modules/GanttChart.test.md)
573. [GuardedTaskModal](modules/GuardedTaskModal.md)
574. [BacklogPanel](modules/BacklogPanel.md)
575. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
576. [ProjectTaskTree](modules/ProjectTaskTree.md)
577. [TaskForm.test](modules/TaskForm.test.md)
578. [GanttPage](modules/GanttPage.md)
579. [GanttPage.test](modules/GanttPage.test.md)
580. [MyWorkPage](modules/MyWorkPage.md)
581. [ProjectDetailPage](modules/ProjectDetailPage.md)
582. [ProjectsPage](modules/ProjectsPage.md)
583. [ProjectsPage.test](modules/ProjectsPage.test.md)
584. [TriagePage](modules/TriagePage.md)
585. [visibleWork](modules/visibleWork.md)
586. [KanbanBoard](modules/KanbanBoard.md)
587. [KanbanBoard.test](modules/KanbanBoard.test.md)
588. [TaskList](modules/TaskList.md)
589. [SavedViewsControl](modules/SavedViewsControl.md)
590. [TaskList.test](modules/TaskList.test.md)
591. [TasksPage](modules/TasksPage.md)
592. [TasksPage.test](modules/TasksPage.test.md)
593. [visibleWork.test](modules/visibleWork.test.md)
594. [tailwind.config](modules/tailwind.config.md)
595. [vite.config](modules/vite.config.md)
596. [vitest.config](modules/vitest.config.md)
597. [create_agent_actor](modules/create_agent_actor.md)
598. [generate_workchord_keys](modules/generate_workchord_keys.md)
599. [setup_agent_team](modules/setup_agent_team.md)
600. [build_agent_skills](modules/build_agent_skills.md)
601. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
602. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
603. [ci_runtime](modules/ci_runtime.md)
604. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
605. [postgres_runtime](modules/postgres_runtime.md)
606. [run_android_checks](modules/run_android_checks.md)
607. [run_disposable_checks](modules/run_disposable_checks.md)
608. [serve_disposable_api](modules/serve_disposable_api.md)
609. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
610. [test_ci_runtime](modules/test_ci_runtime.md)
611. [test_native_runtimes](modules/test_native_runtimes.md)
612. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
613. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
614. [generate_client_contract](modules/generate_client_contract.md)
615. [load_common](modules/load_common.md)
616. [collect](modules/collect.md)
617. [result](modules/result.md)
618. [compare](modules/compare.md)
619. [finalize](modules/finalize.md)
620. [qualify](modules/qualify.md)
621. [resilience](modules/resilience.md)
622. [run](modules/run.md)
623. [seal](modules/seal.md)
624. [seed](modules/seed.md)

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
| [app_main](modules/app_main.md) | `settings = get_settings`, `app = FastAPI`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.add_middleware`, `app.add_middleware`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `mount_mcp_http` |
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
| [routers_capacity](modules/routers_capacity.md) | `router = APIRouter` |
| [delivery_dependencies](modules/delivery_dependencies.md) | `router = APIRouter` |
| [routers_discussion](modules/routers_discussion.md) | `router = APIRouter` |
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
| [test_routing_evidence](modules/test_routing_evidence.md) | `sys.path.insert` |
| [support_database](modules/support_database.md) | `TEST_DATABASE_PATTERN = re.compile`, `TEST_RUNTIME_ROLE_PATTERN = re.compile`, `DEFAULT_POSTGRES_HOSTS = frozenset`, `ADMIN_DATABASES = frozenset` |
| [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md) | `_PROVISION_SPEC = importlib.util.spec_from_file_location`, `provision_actor = importlib.util.module_from_spec`, `_PROVISION_SPEC.loader.exec_module` |
| [test_agent_routing_service](modules/test_agent_routing_service.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md) | `pytestmark = pytest.mark.usefixtures`, `_FIXED_NOW = datetime` |
| [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md) | `SPEC = importlib.util.spec_from_file_location`, `setup_agent_team = importlib.util.module_from_spec`, `SPEC.loader.exec_module` |
| [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md) | `FIXED_NOW = datetime` |
| [App](modules/App.md) | `OverviewPage = lazy`, `LandingPage = lazy`, `PlanPage = lazy`, `PlanMasterPage = lazy`, `PlanSharePage = lazy`, `CalendarPage = lazy`, `IterationsPage = lazy`, `TeamPage = lazy`, `TasksPage = lazy`, `MyWorkPage = lazy`, `TriagePage = lazy`, `ProjectsPage = lazy`, `ProjectDetailPage = lazy`, `ProjectReleaseDetailPage = lazy`, `RoadmapPage = lazy`, `GanttPage = lazy`, `AnalyticsPage = lazy`, `SettingsPage = lazy`, `AgentPipelinePage = lazy`, `AgentTeamSetupMasterPage = lazy`, `NotFoundPage = lazy` |
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
| [CommandMenu.test](modules/CommandMenu.test.md) | `lookup = hoisted`, `mock`, `describe` |
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
| [TaskDiscussion.test](modules/TaskDiscussion.test.md) | `service = hoisted`, `mock`, `describe` |
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
| [savedViewState.test](modules/savedViewState.test.md) | `describe` |
| [selectWorkNowTasks](modules/selectWorkNowTasks.md) | `doneStatuses = Set` |
| [taskFilters.test](modules/taskFilters.test.md) | `describe` |
| [teamMemberLabels](modules/teamMemberLabels.md) | `t = bind` |
| [visibleWork.test](modules/visibleWork.test.md) | `it`, `it`, `it` |
| [build_agent_skills](modules/build_agent_skills.md) | `SEMVER_RE = re.compile`, `SKILL_NAME_RE = re.compile`, `COMPATIBILITY_RE = re.compile`, `MARKDOWN_LINK_RE = re.compile`, `URL_RE = re.compile` |
| [check_postgresql_documentation](modules/check_postgresql_documentation.md) | `LINK_PATTERN = re.compile`, `SHELL_FENCE_PATTERN = re.compile`, `LIVE_SQLITE_COPY_PATTERN = re.compile` |
| [serve_disposable_oidc](modules/serve_disposable_oidc.md) | `url = assert_safe_test_database_url`, `issuer = os.environ.get`, `key = rsa.generate_private_key`, `jwk = json.loads`, `jwk['kid'] = 'disposable-key'`, `app = FastAPI` |
| [test_ci_runtime](modules/test_ci_runtime.md) | `sys.path.insert` |
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
| `create_absence` | factory | [routers_capacity](modules/routers_capacity.md) |
| `create_task_comment` | factory | [routers_discussion](modules/routers_discussion.md) |
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

Delivery and discussion model imports register flush listeners. The command owner invokes delivery reconciliation and outbox enqueue after flushing and before commit; previews roll back the same work. Outbound dispatch imports the discussion sink lazily, and the sink uses the existing transport error type lazily to avoid eager initialization cycles. Typed transfer references remain present where aggregate constraints forbid staging them as null.
