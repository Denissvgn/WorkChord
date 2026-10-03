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
35. [20261003_0005_native_connections](modules/20261003_0005_native_connections.md)
36. [query_limits](modules/query_limits.md)
37. [runtime_telemetry](modules/runtime_telemetry.md)
38. [database_runtime](modules/database_runtime.md)
39. [maintenance](modules/maintenance.md)
40. [schemas_agent_planning](modules/schemas_agent_planning.md)
41. [agent_skill_bundle](modules/agent_skill_bundle.md)
42. [agent_team_setup](modules/agent_team_setup.md)
43. [schemas_autonomy](modules/schemas_autonomy.md)
44. [schemas_common](modules/schemas_common.md)
45. [schemas_github](modules/schemas_github.md)
46. [schemas_intake](modules/schemas_intake.md)
47. [schemas_label](modules/schemas_label.md)
48. [schemas_plan_share](modules/schemas_plan_share.md)
49. [planning_inputs](modules/planning_inputs.md)
50. [schemas_calendar](modules/schemas_calendar.md)
51. [schemas_saved_view](modules/schemas_saved_view.md)
52. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
53. [schemas_session](modules/schemas_session.md)
54. [snapshot](modules/snapshot.md)
55. [schemas_system_settings](modules/schemas_system_settings.md)
56. [schemas_email_settings](modules/schemas_email_settings.md)
57. [schemas_task_brief](modules/schemas_task_brief.md)
58. [schemas_llm](modules/schemas_llm.md)
59. [schemas_task_domain](modules/schemas_task_domain.md)
60. [schemas_team](modules/schemas_team.md)
61. [schemas_template](modules/schemas_template.md)
62. [schemas_work_metrics](modules/schemas_work_metrics.md)
63. [schemas_iteration](modules/schemas_iteration.md)
64. [schemas_project](modules/schemas_project.md)
65. [schemas_release](modules/schemas_release.md)
66. [security](modules/security.md)
67. [agent_routing_policy](modules/agent_routing_policy.md)
68. [agent_routing](modules/agent_routing.md)
69. [agent_routing_rollout](modules/agent_routing_rollout.md)
70. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
71. [language_service](modules/language_service.md)
72. [scheduling_rules_service](modules/scheduling_rules_service.md)
73. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
74. [upgrade_service](modules/upgrade_service.md)
75. [upgrade](modules/upgrade.md)
76. [sql_semantics](modules/sql_semantics.md)
77. [exceptions](modules/exceptions.md)
78. [text_similarity](modules/text_similarity.md)
79. [time](modules/time.md)
80. [observability](modules/observability.md)
81. [app_database](modules/app_database.md)
82. [models_agent](modules/models_agent.md)
83. [models_autonomy](modules/models_autonomy.md)
84. [models_calendar](modules/models_calendar.md)
85. [models_capacity](modules/models_capacity.md)
86. [models_database_migration](modules/models_database_migration.md)
87. [delivery_dependency](modules/delivery_dependency.md)
88. [models_discussion](modules/models_discussion.md)
89. [models_external_link](modules/models_external_link.md)
90. [models_github](modules/models_github.md)
91. [models_identity](modules/models_identity.md)
92. [models_iteration](modules/models_iteration.md)
93. [models_label](modules/models_label.md)
94. [native_connection](modules/native_connection.md)
95. [models_outbound_webhook](modules/models_outbound_webhook.md)
96. [models_plan_share](modules/models_plan_share.md)
97. [models_release](modules/models_release.md)
98. [models_project](modules/models_project.md)
99. [models_request_source](modules/models_request_source.md)
100. [models_saved_view](modules/models_saved_view.md)
101. [models_system_settings](modules/models_system_settings.md)
102. [models_task](modules/models_task.md)
103. [recovery](modules/recovery.md)
104. [models_task_brief](modules/models_task_brief.md)
105. [task_status_log](modules/task_status_log.md)
106. [team_member](modules/team_member.md)
107. [models_template](modules/models_template.md)
108. [models_triage](modules/models_triage.md)
109. [user_session](modules/user_session.md)
110. [models___init__](modules/models___init__.md)
111. [catalog](modules/catalog.md)
112. [database_migration_canonical](modules/database_migration_canonical.md)
113. [source](modules/source.md)
114. [transfer](modules/transfer.md)
115. [cli_database_migration](modules/cli_database_migration.md)
116. [database_migration___init__](modules/database_migration___init__.md)
117. [migrations_env](modules/migrations_env.md)
118. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
119. [calendar_service](modules/calendar_service.md)
120. [calendars](modules/calendars.md)
121. [capacity_service](modules/capacity_service.md)
122. [routers_capacity](modules/routers_capacity.md)
123. [delivery_dependency_service](modules/delivery_dependency_service.md)
124. [discussion_service](modules/discussion_service.md)
125. [identity_service](modules/identity_service.md)
126. [iteration_service](modules/iteration_service.md)
127. [iterations](modules/iterations.md)
128. [label_service](modules/label_service.md)
129. [labels](modules/labels.md)
130. [native_session_service](modules/native_session_service.md)
131. [saved_view_service](modules/saved_view_service.md)
132. [session_service](modules/session_service.md)
133. [http_authority](modules/http_authority.md)
134. [routers_identity](modules/routers_identity.md)
135. [saved_views](modules/saved_views.md)
136. [routers_session](modules/routers_session.md)
137. [task_brief_service](modules/task_brief_service.md)
138. [task_context_revision_service](modules/task_context_revision_service.md)
139. [task_domain_service](modules/task_domain_service.md)
140. [task_recovery_service](modules/task_recovery_service.md)
141. [team_service](modules/team_service.md)
142. [routers_team](modules/routers_team.md)
143. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
144. [snapshot_service](modules/snapshot_service.md)
145. [plan_share_service](modules/plan_share_service.md)
146. [plan_shares](modules/plan_shares.md)
147. [template_service](modules/template_service.md)
148. [templates](modules/templates.md)
149. [services_work_metrics](modules/services_work_metrics.md)
150. [import_parser](modules/import_parser.md)
151. [url_policy](modules/url_policy.md)
152. [schemas_external_link](modules/schemas_external_link.md)
153. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
154. [schemas_request_source](modules/schemas_request_source.md)
155. [schemas_task](modules/schemas_task.md)
156. [schemas_gantt](modules/schemas_gantt.md)
157. [task_detail](modules/task_detail.md)
158. [schemas_triage](modules/schemas_triage.md)
159. [schemas___init__](modules/schemas___init__.md)
160. [schemas_agent](modules/schemas_agent.md)
161. [agent_readiness](modules/agent_readiness.md)
162. [llm_service](modules/llm_service.md)
163. [system_settings_service](modules/system_settings_service.md)
164. [routers_system_settings](modules/routers_system_settings.md)
165. [email_settings_service](modules/email_settings_service.md)
166. [routers_email_settings](modules/routers_email_settings.md)
167. [notification_service](modules/notification_service.md)
168. [outbound_webhook_service](modules/outbound_webhook_service.md)
169. [worker](modules/worker.md)
170. [outbound_webhooks](modules/outbound_webhooks.md)
171. [external_link_service](modules/external_link_service.md)
172. [github_status_service](modules/github_status_service.md)
173. [request_source_service](modules/request_source_service.md)
174. [request_sources](modules/request_sources.md)
175. [project_service](modules/project_service.md)
176. [task_detail_service](modules/task_detail_service.md)
177. [task_import_service](modules/task_import_service.md)
178. [task_service](modules/task_service.md)
179. [export](modules/export.md)
180. [snapshots](modules/snapshots.md)
181. [routers_task_domain](modules/routers_task_domain.md)
182. [delivery_dependencies](modules/delivery_dependencies.md)
183. [routers_discussion](modules/routers_discussion.md)
184. [agent_routing_observability](modules/agent_routing_observability.md)
185. [agent_service](modules/agent_service.md)
186. [agent_skill_bundles](modules/agent_skill_bundles.md)
187. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
188. [agent_routing_service](modules/agent_routing_service.md)
189. [agent_team_setup_service](modules/agent_team_setup_service.md)
190. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
191. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
192. [github_status_automation_service](modules/github_status_automation_service.md)
193. [release_service](modules/release_service.md)
194. [projects](modules/projects.md)
195. [scheduler_service](modules/scheduler_service.md)
196. [routers_gantt](modules/routers_gantt.md)
197. [routers_llm](modules/routers_llm.md)
198. [agent_planning_service](modules/agent_planning_service.md)
199. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
200. [tasks](modules/tasks.md)
201. [task_status_service](modules/task_status_service.md)
202. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
203. [triage_service](modules/triage_service.md)
204. [routers_triage](modules/routers_triage.md)
205. [agent_work_service](modules/agent_work_service.md)
206. [mcp_agent_tools](modules/mcp_agent_tools.md)
207. [mcp_server](modules/mcp_server.md)
208. [routers_agent](modules/routers_agent.md)
209. [routers_agent_planning](modules/routers_agent_planning.md)
210. [agent_catalog](modules/agent_catalog.md)
211. [github_webhook_service](modules/github_webhook_service.md)
212. [routers_github](modules/routers_github.md)
213. [web_intake_service](modules/web_intake_service.md)
214. [routers_intake](modules/routers_intake.md)
215. [app_main](modules/app_main.md)
216. [routers___init__](modules/routers___init__.md)
217. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
218. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
219. [test_server_acceptance](modules/test_server_acceptance.md)
220. [test_work_package_service](modules/test_work_package_service.md)
221. [test_database_configuration](modules/test_database_configuration.md)
222. [test_deployment_topology](modules/test_deployment_topology.md)
223. [test_observability](modules/test_observability.md)
224. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
225. [test_query_boundaries](modules/test_query_boundaries.md)
226. [test_runtime_policy](modules/test_runtime_policy.md)
227. [test_schema_behavior](modules/test_schema_behavior.md)
228. [test_cutover_evidence](modules/test_cutover_evidence.md)
229. [test_documentation_boundary](modules/test_documentation_boundary.md)
230. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
231. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
232. [test_source_preflight](modules/test_source_preflight.md)
233. [test_transfer_catalog](modules/test_transfer_catalog.md)
234. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
235. [0001_wave0_probe](modules/0001_wave0_probe.md)
236. [test_initial_schema](modules/test_initial_schema.md)
237. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
238. [test_load_tooling](modules/test_load_tooling.md)
239. [test_routing_evidence](modules/test_routing_evidence.md)
240. [support_database](modules/support_database.md)
241. [delivery](modules/delivery.md)
242. [factories](modules/factories.md)
243. [faults](modules/faults.md)
244. [schema](modules/schema.md)
245. [support___init__](modules/support___init__.md)
246. [conftest](modules/conftest.md)
247. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
248. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
249. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
250. [transactions](modules/transactions.md)
251. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
252. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
253. [test_agent_routing_data](modules/test_agent_routing_data.md)
254. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
255. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
256. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
257. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
258. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
259. [test_agent_routing_service](modules/test_agent_routing_service.md)
260. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
261. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
262. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
263. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
264. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
265. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
266. [test_authority_migrations](modules/test_authority_migrations.md)
267. [test_capacity_contract](modules/test_capacity_contract.md)
268. [test_client_contract](modules/test_client_contract.md)
269. [test_database_harness](modules/test_database_harness.md)
270. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
271. [test_agent_team_setup](modules/test_agent_team_setup.md)
272. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
273. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
274. [test_managed_authority](modules/test_managed_authority.md)
275. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
276. [test_mobile_contract](modules/test_mobile_contract.md)
277. [test_native_connections](modules/test_native_connections.md)
278. [test_plan_shares](modules/test_plan_shares.md)
279. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
280. [test_process_roles](modules/test_process_roles.md)
281. [test_profile_capacity](modules/test_profile_capacity.md)
282. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
283. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
284. [test_saved_view_service](modules/test_saved_view_service.md)
285. [test_task_domain](modules/test_task_domain.md)
286. [test_human_work_queries](modules/test_human_work_queries.md)
287. [test_task_discussion](modules/test_task_discussion.md)
288. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
289. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
290. [test_work_correctness](modules/test_work_correctness.md)
291. [eslint.config](modules/eslint.config.md)
292. [postcss.config](modules/postcss.config.md)
293. [Button](modules/Button.md)
294. [Button.test](modules/Button.test.md)
295. [Checkbox](modules/Checkbox.md)
296. [CollapsibleSection](modules/CollapsibleSection.md)
297. [Input](modules/Input.md)
298. [Input.test](modules/Input.test.md)
299. [dialogLayer](modules/dialogLayer.md)
300. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
301. [Modal](modules/Modal.md)
302. [ConfirmDialog](modules/ConfirmDialog.md)
303. [useConfirmDialog](modules/useConfirmDialog.md)
304. [WorkFreshness](modules/WorkFreshness.md)
305. [toast](modules/toast.md)
306. [ToastProvider](modules/ToastProvider.md)
307. [Breadcrumbs](modules/Breadcrumbs.md)
308. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
309. [commandMenuEvents](modules/commandMenuEvents.md)
310. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
311. [SortableTaskItem](modules/SortableTaskItem.md)
312. [useDraftDismissal](modules/useDraftDismissal.md)
313. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
314. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
315. [InlineEmptyState](modules/InlineEmptyState.md)
316. [MasterProgress](modules/MasterProgress.md)
317. [MasterProgress.test](modules/MasterProgress.test.md)
318. [OverflowMenu](modules/OverflowMenu.md)
319. [PageLayout](modules/PageLayout.md)
320. [SectionCard](modules/SectionCard.md)
321. [SlideOverDrawer](modules/SlideOverDrawer.md)
322. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
323. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
324. [StickyRail](modules/StickyRail.md)
325. [index](modules/index.md)
326. [overviewTaskThread](modules/overviewTaskThread.md)
327. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
328. [planningReturn](modules/planningReturn.md)
329. [PlanReturnBar](modules/PlanReturnBar.md)
330. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
331. [workQueryFreshness](modules/workQueryFreshness.md)
332. [teamwork.en](modules/teamwork.en.md)
333. [resources.en](modules/resources.en.md)
334. [i18n](modules/i18n.md)
335. [dateLocale](modules/dateLocale.md)
336. [InteractiveCalendar](modules/InteractiveCalendar.md)
337. [teamwork.ru](modules/teamwork.ru.md)
338. [resources.ru](modules/resources.ru.md)
339. [i18n.test](modules/i18n.test.md)
340. [routeModules](modules/routeModules.md)
341. [DocumentMetadata](modules/DocumentMetadata.md)
342. [workspaces](modules/workspaces.md)
343. [helpContexts](modules/helpContexts.md)
344. [workspaces.test](modules/workspaces.test.md)
345. [LandingPage](modules/LandingPage.md)
346. [NotFoundPage](modules/NotFoundPage.md)
347. [healthService](modules/healthService.md)
348. [SystemHealthPanel](modules/SystemHealthPanel.md)
349. [iterationStore](modules/iterationStore.md)
350. [themeStore](modules/themeStore.md)
351. [planning-masters.test](modules/planning-masters.test.md)
352. [accessibilityInvariants](modules/accessibilityInvariants.md)
353. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
354. [renderWithProviders](modules/renderWithProviders.md)
355. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
356. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
357. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
358. [OverflowMenu.test](modules/OverflowMenu.test.md)
359. [renderWithProviders.test](modules/renderWithProviders.test.md)
360. [setup](modules/setup.md)
361. [types_calendar](modules/types_calendar.md)
362. [types_label](modules/types_label.md)
363. [outboundWebhook](modules/outboundWebhook.md)
364. [requestSource](modules/requestSource.md)
365. [savedView](modules/savedView.md)
366. [schedulingRules](modules/schedulingRules.md)
367. [ConstraintsPanel](modules/ConstraintsPanel.md)
368. [schedulingDisplay](modules/schedulingDisplay.md)
369. [EffortModifierCard](modules/EffortModifierCard.md)
370. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
371. [SchedulingPassCard](modules/SchedulingPassCard.md)
372. [systemSettings](modules/systemSettings.md)
373. [emailSettings](modules/emailSettings.md)
374. [types_team](modules/types_team.md)
375. [types_task](modules/types_task.md)
376. [types_triage](modules/types_triage.md)
377. [KanbanCard](modules/KanbanCard.md)
378. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
379. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
380. [tone](modules/tone.md)
381. [KanbanColumn](modules/KanbanColumn.md)
382. [Pill](modules/Pill.md)
383. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
384. [tone.test](modules/tone.test.md)
385. [attentionRanking](modules/attentionRanking.md)
386. [attentionRanking.test](modules/attentionRanking.test.md)
387. [planningTaskIssues](modules/planningTaskIssues.md)
388. [planningMasters_masters](modules/planningMasters_masters.md)
389. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
390. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
391. [types_agent](modules/types_agent.md)
392. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
393. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
394. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
395. [statusScopes](modules/statusScopes.md)
396. [statusScopes.test](modules/statusScopes.test.md)
397. [modelAwareRouting](modules/modelAwareRouting.md)
398. [types_github](modules/types_github.md)
399. [types_template](modules/types_template.md)
400. [seedDisplay](modules/seedDisplay.md)
401. [workMetrics](modules/workMetrics.md)
402. [WorkMetricsLine](modules/WorkMetricsLine.md)
403. [types_iteration](modules/types_iteration.md)
404. [types_gantt](modules/types_gantt.md)
405. [types_project](modules/types_project.md)
406. [projectStatusStyles](modules/projectStatusStyles.md)
407. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
408. [types_release](modules/types_release.md)
409. [agentAccess](modules/agentAccess.md)
410. [useAgentAccess](modules/useAgentAccess.md)
411. [apiError](modules/apiError.md)
412. [QueryState](modules/QueryState.md)
413. [taskEditorContract](modules/taskEditorContract.md)
414. [TaskBriefEditor](modules/TaskBriefEditor.md)
415. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
416. [taskDraftStorage](modules/taskDraftStorage.md)
417. [adminAccess](modules/adminAccess.md)
418. [api](modules/api.md)
419. [identityService](modules/identityService.md)
420. [identityContext](modules/identityContext.md)
421. [useAdminAccess](modules/useAdminAccess.md)
422. [AdminAccessPanel](modules/AdminAccessPanel.md)
423. [AdminAccessGate](modules/AdminAccessGate.md)
424. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
425. [NativeConnectionPage](modules/NativeConnectionPage.md)
426. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
427. [agentService](modules/agentService.md)
428. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
429. [agentService.test](modules/agentService.test.md)
430. [calendarService](modules/calendarService.md)
431. [PersonCapacity](modules/PersonCapacity.md)
432. [discussionService](modules/discussionService.md)
433. [TaskDiscussion](modules/TaskDiscussion.md)
434. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
435. [emailSettingsService](modules/emailSettingsService.md)
436. [exportService](modules/exportService.md)
437. [ganttService](modules/ganttService.md)
438. [githubService](modules/githubService.md)
439. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
440. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
441. [iterationService](modules/iterationService.md)
442. [IterationSelector](modules/IterationSelector.md)
443. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
444. [SidebarIterationCard](modules/SidebarIterationCard.md)
445. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
446. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
447. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
448. [labelService](modules/labelService.md)
449. [LabelSelector](modules/LabelSelector.md)
450. [outboundWebhookService](modules/outboundWebhookService.md)
451. [planShareService](modules/planShareService.md)
452. [projectService](modules/projectService.md)
453. [releaseService](modules/releaseService.md)
454. [ReleaseForm](modules/ReleaseForm.md)
455. [requestSourceService](modules/requestSourceService.md)
456. [savedViewService](modules/savedViewService.md)
457. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
458. [AppSidebar](modules/AppSidebar.md)
459. [AppSidebar.test](modules/AppSidebar.test.md)
460. [schedulingRulesService](modules/schedulingRulesService.md)
461. [sessionService](modules/sessionService.md)
462. [snapshotService](modules/snapshotService.md)
463. [systemSettingsService](modules/systemSettingsService.md)
464. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
465. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
466. [taskService](modules/taskService.md)
467. [DeliveryDependencies](modules/DeliveryDependencies.md)
468. [ImportTasksModal](modules/ImportTasksModal.md)
469. [TaskContextSummary](modules/TaskContextSummary.md)
470. [TaskDependencySelector](modules/TaskDependencySelector.md)
471. [TaskSearch](modules/TaskSearch.md)
472. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
473. [TaskWorkPanel](modules/TaskWorkPanel.md)
474. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
475. [teamService](modules/teamService.md)
476. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
477. [TaskFiltersBar](modules/TaskFiltersBar.md)
478. [taskFilterDefaults](modules/taskFilterDefaults.md)
479. [ImportTeamModal](modules/ImportTeamModal.md)
480. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
481. [TeamForm](modules/TeamForm.md)
482. [TeamForm.test](modules/TeamForm.test.md)
483. [TeamProfileManager](modules/TeamProfileManager.md)
484. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
485. [IdentityProvider](modules/IdentityProvider.md)
486. [UserSessionBadge](modules/UserSessionBadge.md)
487. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
488. [IdentityProvider.test](modules/IdentityProvider.test.md)
489. [CalendarPage](modules/CalendarPage.md)
490. [templateService](modules/templateService.md)
491. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
492. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
493. [triageService](modules/triageService.md)
494. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
495. [usePlanningReadiness](modules/usePlanningReadiness.md)
496. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
497. [copyText](modules/copyText.md)
498. [focusLifecycle](modules/focusLifecycle.md)
499. [focusLifecycle.test](modules/focusLifecycle.test.md)
500. [formatDate](modules/formatDate.md)
501. [TaskStatusFlow](modules/TaskStatusFlow.md)
502. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
503. [IterationForm](modules/IterationForm.md)
504. [IterationForm.test](modules/IterationForm.test.md)
505. [IterationList](modules/IterationList.md)
506. [NotificationsPanel](modules/NotificationsPanel.md)
507. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
508. [StatusChangeControl](modules/StatusChangeControl.md)
509. [VacationManager](modules/VacationManager.md)
510. [TeamList](modules/TeamList.md)
511. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
512. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
513. [AnalyticsPage](modules/AnalyticsPage.md)
514. [IterationsPage](modules/IterationsPage.md)
515. [PlanMasterPage](modules/PlanMasterPage.md)
516. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
517. [PlanPage](modules/PlanPage.md)
518. [PlanPage.test](modules/PlanPage.test.md)
519. [PlanSharePage](modules/PlanSharePage.md)
520. [PlanSharePage.test](modules/PlanSharePage.test.md)
521. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
522. [TeamPage](modules/TeamPage.md)
523. [modelRouting](modules/modelRouting.md)
524. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
525. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
526. [modelRouting.test](modules/modelRouting.test.md)
527. [protectedQueries](modules/protectedQueries.md)
528. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
529. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
530. [AgentAccessPanel](modules/AgentAccessPanel.md)
531. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
532. [AgentModelAdministration](modules/AgentModelAdministration.md)
533. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
534. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
535. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
536. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
537. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
538. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
539. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
540. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
541. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
542. [AgentPipelinePage](modules/AgentPipelinePage.md)
543. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
544. [safeUrl](modules/safeUrl.md)
545. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
546. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
547. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
548. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
549. [savedViewState](modules/savedViewState.md)
550. [savedViewState.test](modules/savedViewState.test.md)
551. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
552. [OverviewPage](modules/OverviewPage.md)
553. [OverviewPage.test](modules/OverviewPage.test.md)
554. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
555. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
556. [CommandMenu](modules/CommandMenu.md)
557. [CommandMenu.test](modules/CommandMenu.test.md)
558. [ContextHelp](modules/ContextHelp.md)
559. [AppTopNav](modules/AppTopNav.md)
560. [AppShell](modules/AppShell.md)
561. [App](modules/App.md)
562. [AppShell.test](modules/AppShell.test.md)
563. [AppTopNav.test](modules/AppTopNav.test.md)
564. [ContextHelp.test](modules/ContextHelp.test.md)
565. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
566. [src_main](modules/src_main.md)
567. [SettingsPage](modules/SettingsPage.md)
568. [SettingsPage.test](modules/SettingsPage.test.md)
569. [taskFilters](modules/taskFilters.md)
570. [taskFilters.test](modules/taskFilters.test.md)
571. [teamMemberLabels](modules/teamMemberLabels.md)
572. [InitiativeForm](modules/InitiativeForm.md)
573. [RoadmapPage](modules/RoadmapPage.md)
574. [RoadmapPage.test](modules/RoadmapPage.test.md)
575. [templateDefaults](modules/templateDefaults.md)
576. [ProjectForm](modules/ProjectForm.md)
577. [TaskForm](modules/TaskForm.md)
578. [TaskEditModal](modules/TaskEditModal.md)
579. [GanttChart](modules/GanttChart.md)
580. [GanttChart.test](modules/GanttChart.test.md)
581. [GuardedTaskModal](modules/GuardedTaskModal.md)
582. [BacklogPanel](modules/BacklogPanel.md)
583. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
584. [ProjectTaskTree](modules/ProjectTaskTree.md)
585. [TaskForm.test](modules/TaskForm.test.md)
586. [GanttPage](modules/GanttPage.md)
587. [GanttPage.test](modules/GanttPage.test.md)
588. [MyWorkPage](modules/MyWorkPage.md)
589. [ProjectDetailPage](modules/ProjectDetailPage.md)
590. [ProjectsPage](modules/ProjectsPage.md)
591. [ProjectsPage.test](modules/ProjectsPage.test.md)
592. [TriagePage](modules/TriagePage.md)
593. [visibleWork](modules/visibleWork.md)
594. [KanbanBoard](modules/KanbanBoard.md)
595. [KanbanBoard.test](modules/KanbanBoard.test.md)
596. [TaskList](modules/TaskList.md)
597. [SavedViewsControl](modules/SavedViewsControl.md)
598. [TaskList.test](modules/TaskList.test.md)
599. [TasksPage](modules/TasksPage.md)
600. [TasksPage.test](modules/TasksPage.test.md)
601. [visibleWork.test](modules/visibleWork.test.md)
602. [tailwind.config](modules/tailwind.config.md)
603. [vite.config](modules/vite.config.md)
604. [vitest.config](modules/vitest.config.md)
605. [create_agent_actor](modules/create_agent_actor.md)
606. [generate_workchord_keys](modules/generate_workchord_keys.md)
607. [setup_agent_team](modules/setup_agent_team.md)
608. [build_agent_skills](modules/build_agent_skills.md)
609. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
610. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
611. [ci_runtime](modules/ci_runtime.md)
612. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
613. [postgres_runtime](modules/postgres_runtime.md)
614. [run_android_checks](modules/run_android_checks.md)
615. [run_disposable_checks](modules/run_disposable_checks.md)
616. [serve_disposable_api](modules/serve_disposable_api.md)
617. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
618. [test_ci_runtime](modules/test_ci_runtime.md)
619. [test_native_runtimes](modules/test_native_runtimes.md)
620. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
621. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
622. [generate_client_contract](modules/generate_client_contract.md)
623. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
624. [load_common](modules/load_common.md)
625. [collect](modules/collect.md)
626. [result](modules/result.md)
627. [compare](modules/compare.md)
628. [finalize](modules/finalize.md)
629. [qualify](modules/qualify.md)
630. [resilience](modules/resilience.md)
631. [run](modules/run.md)
632. [seal](modules/seal.md)
633. [seed](modules/seed.md)

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
| [test_native_connections](modules/test_native_connections.md) | `CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b'=').decode` |
| [App](modules/App.md) | `OverviewPage = lazy`, `LandingPage = lazy`, `PlanPage = lazy`, `PlanMasterPage = lazy`, `PlanSharePage = lazy`, `CalendarPage = lazy`, `IterationsPage = lazy`, `TeamPage = lazy`, `TasksPage = lazy`, `MyWorkPage = lazy`, `NativeConnectionPage = lazy`, `TriagePage = lazy`, `ProjectsPage = lazy`, `ProjectDetailPage = lazy`, `ProjectReleaseDetailPage = lazy`, `RoadmapPage = lazy`, `GanttPage = lazy`, `AnalyticsPage = lazy`, `SettingsPage = lazy`, `AgentPipelinePage = lazy`, `AgentTeamSetupMasterPage = lazy`, `NotFoundPage = lazy` |
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
| [IdentityProvider.test](modules/IdentityProvider.test.md) | `service = hoisted`, `mock`, `describe` |
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
| [NativeConnectionPage.test](modules/NativeConnectionPage.test.md) | `service = hoisted`, `mock`, `request = repeat`, `describe` |
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

NativeSessionService reuses IdentityService session issuance and the command transaction owner. Native exchange locks the principal before its approving browser session to align with account revocation. The Android session and cookie implementation requires direct platform evidence because Kotlin extraction is unavailable in the configured analyzer.
