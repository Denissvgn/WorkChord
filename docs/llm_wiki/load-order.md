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
36. [20261004_0006_delivery_observations](modules/20261004_0006_delivery_observations.md)
37. [query_limits](modules/query_limits.md)
38. [runtime_telemetry](modules/runtime_telemetry.md)
39. [database_runtime](modules/database_runtime.md)
40. [maintenance](modules/maintenance.md)
41. [mutation_versions](modules/mutation_versions.md)
42. [schemas_agent_planning](modules/schemas_agent_planning.md)
43. [agent_skill_bundle](modules/agent_skill_bundle.md)
44. [agent_team_setup](modules/agent_team_setup.md)
45. [schemas_autonomy](modules/schemas_autonomy.md)
46. [schemas_common](modules/schemas_common.md)
47. [delivery_metrics](modules/delivery_metrics.md)
48. [schemas_github](modules/schemas_github.md)
49. [schemas_intake](modules/schemas_intake.md)
50. [schemas_label](modules/schemas_label.md)
51. [schemas_plan_share](modules/schemas_plan_share.md)
52. [planning_inputs](modules/planning_inputs.md)
53. [schemas_calendar](modules/schemas_calendar.md)
54. [schemas_saved_view](modules/schemas_saved_view.md)
55. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
56. [schemas_session](modules/schemas_session.md)
57. [snapshot](modules/snapshot.md)
58. [schemas_system_settings](modules/schemas_system_settings.md)
59. [schemas_email_settings](modules/schemas_email_settings.md)
60. [schemas_task_brief](modules/schemas_task_brief.md)
61. [schemas_llm](modules/schemas_llm.md)
62. [schemas_task_domain](modules/schemas_task_domain.md)
63. [schemas_team](modules/schemas_team.md)
64. [schemas_template](modules/schemas_template.md)
65. [schemas_work_metrics](modules/schemas_work_metrics.md)
66. [schemas_iteration](modules/schemas_iteration.md)
67. [schemas_project](modules/schemas_project.md)
68. [schemas_release](modules/schemas_release.md)
69. [security](modules/security.md)
70. [agent_routing_policy](modules/agent_routing_policy.md)
71. [agent_routing](modules/agent_routing.md)
72. [agent_routing_rollout](modules/agent_routing_rollout.md)
73. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
74. [language_service](modules/language_service.md)
75. [scheduling_rules_service](modules/scheduling_rules_service.md)
76. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
77. [upgrade_service](modules/upgrade_service.md)
78. [upgrade](modules/upgrade.md)
79. [sql_semantics](modules/sql_semantics.md)
80. [exceptions](modules/exceptions.md)
81. [text_similarity](modules/text_similarity.md)
82. [time](modules/time.md)
83. [observability](modules/observability.md)
84. [app_database](modules/app_database.md)
85. [models_agent](modules/models_agent.md)
86. [models_autonomy](modules/models_autonomy.md)
87. [models_calendar](modules/models_calendar.md)
88. [models_capacity](modules/models_capacity.md)
89. [models_database_migration](modules/models_database_migration.md)
90. [delivery_dependency](modules/delivery_dependency.md)
91. [models_discussion](modules/models_discussion.md)
92. [models_external_link](modules/models_external_link.md)
93. [models_github](modules/models_github.md)
94. [models_identity](modules/models_identity.md)
95. [models_iteration](modules/models_iteration.md)
96. [models_label](modules/models_label.md)
97. [native_connection](modules/native_connection.md)
98. [models_outbound_webhook](modules/models_outbound_webhook.md)
99. [models_plan_share](modules/models_plan_share.md)
100. [models_release](modules/models_release.md)
101. [models_project](modules/models_project.md)
102. [models_request_source](modules/models_request_source.md)
103. [models_saved_view](modules/models_saved_view.md)
104. [models_system_settings](modules/models_system_settings.md)
105. [models_task](modules/models_task.md)
106. [recovery](modules/recovery.md)
107. [models_task_brief](modules/models_task_brief.md)
108. [delivery_observation](modules/delivery_observation.md)
109. [task_status_log](modules/task_status_log.md)
110. [team_member](modules/team_member.md)
111. [models_template](modules/models_template.md)
112. [models_triage](modules/models_triage.md)
113. [user_session](modules/user_session.md)
114. [models___init__](modules/models___init__.md)
115. [catalog](modules/catalog.md)
116. [database_migration_canonical](modules/database_migration_canonical.md)
117. [source](modules/source.md)
118. [transfer](modules/transfer.md)
119. [cli_database_migration](modules/cli_database_migration.md)
120. [database_migration___init__](modules/database_migration___init__.md)
121. [migrations_env](modules/migrations_env.md)
122. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
123. [calendar_service](modules/calendar_service.md)
124. [calendars](modules/calendars.md)
125. [capacity_service](modules/capacity_service.md)
126. [routers_capacity](modules/routers_capacity.md)
127. [delivery_dependency_service](modules/delivery_dependency_service.md)
128. [delivery_metrics_service](modules/delivery_metrics_service.md)
129. [discussion_service](modules/discussion_service.md)
130. [identity_service](modules/identity_service.md)
131. [iteration_service](modules/iteration_service.md)
132. [iterations](modules/iterations.md)
133. [label_service](modules/label_service.md)
134. [labels](modules/labels.md)
135. [native_session_service](modules/native_session_service.md)
136. [saved_view_service](modules/saved_view_service.md)
137. [session_service](modules/session_service.md)
138. [http_authority](modules/http_authority.md)
139. [routers_identity](modules/routers_identity.md)
140. [saved_views](modules/saved_views.md)
141. [routers_session](modules/routers_session.md)
142. [task_brief_service](modules/task_brief_service.md)
143. [task_context_revision_service](modules/task_context_revision_service.md)
144. [task_domain_service](modules/task_domain_service.md)
145. [task_recovery_service](modules/task_recovery_service.md)
146. [team_service](modules/team_service.md)
147. [routers_team](modules/routers_team.md)
148. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
149. [snapshot_service](modules/snapshot_service.md)
150. [plan_share_service](modules/plan_share_service.md)
151. [plan_shares](modules/plan_shares.md)
152. [template_service](modules/template_service.md)
153. [templates](modules/templates.md)
154. [services_work_metrics](modules/services_work_metrics.md)
155. [import_parser](modules/import_parser.md)
156. [url_policy](modules/url_policy.md)
157. [schemas_external_link](modules/schemas_external_link.md)
158. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
159. [schemas_request_source](modules/schemas_request_source.md)
160. [schemas_task](modules/schemas_task.md)
161. [schemas_gantt](modules/schemas_gantt.md)
162. [task_detail](modules/task_detail.md)
163. [schemas_triage](modules/schemas_triage.md)
164. [schemas___init__](modules/schemas___init__.md)
165. [schemas_agent](modules/schemas_agent.md)
166. [agent_readiness](modules/agent_readiness.md)
167. [llm_service](modules/llm_service.md)
168. [system_settings_service](modules/system_settings_service.md)
169. [routers_system_settings](modules/routers_system_settings.md)
170. [email_settings_service](modules/email_settings_service.md)
171. [routers_email_settings](modules/routers_email_settings.md)
172. [notification_service](modules/notification_service.md)
173. [outbound_webhook_service](modules/outbound_webhook_service.md)
174. [worker](modules/worker.md)
175. [outbound_webhooks](modules/outbound_webhooks.md)
176. [external_link_service](modules/external_link_service.md)
177. [github_status_service](modules/github_status_service.md)
178. [request_source_service](modules/request_source_service.md)
179. [request_sources](modules/request_sources.md)
180. [project_service](modules/project_service.md)
181. [task_detail_service](modules/task_detail_service.md)
182. [task_import_service](modules/task_import_service.md)
183. [task_service](modules/task_service.md)
184. [export](modules/export.md)
185. [snapshots](modules/snapshots.md)
186. [routers_task_domain](modules/routers_task_domain.md)
187. [delivery_dependencies](modules/delivery_dependencies.md)
188. [routers_discussion](modules/routers_discussion.md)
189. [agent_routing_observability](modules/agent_routing_observability.md)
190. [agent_service](modules/agent_service.md)
191. [agent_skill_bundles](modules/agent_skill_bundles.md)
192. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
193. [agent_routing_service](modules/agent_routing_service.md)
194. [agent_team_setup_service](modules/agent_team_setup_service.md)
195. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
196. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
197. [github_status_automation_service](modules/github_status_automation_service.md)
198. [release_service](modules/release_service.md)
199. [projects](modules/projects.md)
200. [scheduler_service](modules/scheduler_service.md)
201. [routers_gantt](modules/routers_gantt.md)
202. [routers_llm](modules/routers_llm.md)
203. [agent_planning_service](modules/agent_planning_service.md)
204. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
205. [tasks](modules/tasks.md)
206. [task_status_service](modules/task_status_service.md)
207. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
208. [triage_service](modules/triage_service.md)
209. [routers_triage](modules/routers_triage.md)
210. [agent_work_service](modules/agent_work_service.md)
211. [mcp_agent_tools](modules/mcp_agent_tools.md)
212. [mcp_server](modules/mcp_server.md)
213. [routers_agent](modules/routers_agent.md)
214. [routers_agent_planning](modules/routers_agent_planning.md)
215. [agent_catalog](modules/agent_catalog.md)
216. [github_webhook_service](modules/github_webhook_service.md)
217. [routers_github](modules/routers_github.md)
218. [web_intake_service](modules/web_intake_service.md)
219. [routers_intake](modules/routers_intake.md)
220. [app_main](modules/app_main.md)
221. [routers___init__](modules/routers___init__.md)
222. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
223. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
224. [test_server_acceptance](modules/test_server_acceptance.md)
225. [test_work_package_service](modules/test_work_package_service.md)
226. [test_database_configuration](modules/test_database_configuration.md)
227. [test_deployment_topology](modules/test_deployment_topology.md)
228. [test_observability](modules/test_observability.md)
229. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
230. [test_query_boundaries](modules/test_query_boundaries.md)
231. [test_runtime_policy](modules/test_runtime_policy.md)
232. [test_schema_behavior](modules/test_schema_behavior.md)
233. [test_cutover_evidence](modules/test_cutover_evidence.md)
234. [test_documentation_boundary](modules/test_documentation_boundary.md)
235. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
236. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
237. [test_source_preflight](modules/test_source_preflight.md)
238. [test_transfer_catalog](modules/test_transfer_catalog.md)
239. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
240. [0001_wave0_probe](modules/0001_wave0_probe.md)
241. [test_initial_schema](modules/test_initial_schema.md)
242. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
243. [test_load_tooling](modules/test_load_tooling.md)
244. [test_routing_evidence](modules/test_routing_evidence.md)
245. [support_database](modules/support_database.md)
246. [delivery](modules/delivery.md)
247. [factories](modules/factories.md)
248. [faults](modules/faults.md)
249. [runtime_peer](modules/runtime_peer.md)
250. [schema](modules/schema.md)
251. [support___init__](modules/support___init__.md)
252. [conftest](modules/conftest.md)
253. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
254. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
255. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
256. [transactions](modules/transactions.md)
257. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
258. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
259. [test_agent_routing_data](modules/test_agent_routing_data.md)
260. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
261. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
262. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
263. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
264. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
265. [test_agent_routing_service](modules/test_agent_routing_service.md)
266. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
267. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
268. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
269. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
270. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
271. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
272. [test_authority_migrations](modules/test_authority_migrations.md)
273. [test_capacity_contract](modules/test_capacity_contract.md)
274. [test_client_contract](modules/test_client_contract.md)
275. [test_database_harness](modules/test_database_harness.md)
276. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
277. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
278. [test_agent_team_setup](modules/test_agent_team_setup.md)
279. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
280. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
281. [test_managed_authority](modules/test_managed_authority.md)
282. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
283. [test_mobile_contract](modules/test_mobile_contract.md)
284. [test_mutation_versions](modules/test_mutation_versions.md)
285. [test_native_connections](modules/test_native_connections.md)
286. [test_plan_shares](modules/test_plan_shares.md)
287. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
288. [test_process_roles](modules/test_process_roles.md)
289. [test_profile_capacity](modules/test_profile_capacity.md)
290. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
291. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
292. [test_saved_view_service](modules/test_saved_view_service.md)
293. [test_task_domain](modules/test_task_domain.md)
294. [test_delivery_metrics](modules/test_delivery_metrics.md)
295. [test_human_work_queries](modules/test_human_work_queries.md)
296. [test_task_discussion](modules/test_task_discussion.md)
297. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
298. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
299. [test_work_correctness](modules/test_work_correctness.md)
300. [eslint.config](modules/eslint.config.md)
301. [postcss.config](modules/postcss.config.md)
302. [Button](modules/Button.md)
303. [Button.test](modules/Button.test.md)
304. [Checkbox](modules/Checkbox.md)
305. [CollapsibleSection](modules/CollapsibleSection.md)
306. [Input](modules/Input.md)
307. [Input.test](modules/Input.test.md)
308. [dialogLayer](modules/dialogLayer.md)
309. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
310. [Modal](modules/Modal.md)
311. [ConfirmDialog](modules/ConfirmDialog.md)
312. [useConfirmDialog](modules/useConfirmDialog.md)
313. [WorkFreshness](modules/WorkFreshness.md)
314. [toast](modules/toast.md)
315. [ToastProvider](modules/ToastProvider.md)
316. [Breadcrumbs](modules/Breadcrumbs.md)
317. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
318. [commandMenuEvents](modules/commandMenuEvents.md)
319. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
320. [SortableTaskItem](modules/SortableTaskItem.md)
321. [useDraftDismissal](modules/useDraftDismissal.md)
322. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
323. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
324. [InlineEmptyState](modules/InlineEmptyState.md)
325. [MasterProgress](modules/MasterProgress.md)
326. [MasterProgress.test](modules/MasterProgress.test.md)
327. [OverflowMenu](modules/OverflowMenu.md)
328. [PageLayout](modules/PageLayout.md)
329. [SectionCard](modules/SectionCard.md)
330. [SlideOverDrawer](modules/SlideOverDrawer.md)
331. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
332. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
333. [StickyRail](modules/StickyRail.md)
334. [index](modules/index.md)
335. [overviewTaskThread](modules/overviewTaskThread.md)
336. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
337. [planningReturn](modules/planningReturn.md)
338. [PlanReturnBar](modules/PlanReturnBar.md)
339. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
340. [workQueryFreshness](modules/workQueryFreshness.md)
341. [teamwork.en](modules/teamwork.en.md)
342. [resources.en](modules/resources.en.md)
343. [i18n](modules/i18n.md)
344. [dateLocale](modules/dateLocale.md)
345. [InteractiveCalendar](modules/InteractiveCalendar.md)
346. [teamwork.ru](modules/teamwork.ru.md)
347. [resources.ru](modules/resources.ru.md)
348. [i18n.test](modules/i18n.test.md)
349. [routeModules](modules/routeModules.md)
350. [DocumentMetadata](modules/DocumentMetadata.md)
351. [workspaces](modules/workspaces.md)
352. [helpContexts](modules/helpContexts.md)
353. [workspaces.test](modules/workspaces.test.md)
354. [LandingPage](modules/LandingPage.md)
355. [NotFoundPage](modules/NotFoundPage.md)
356. [healthService](modules/healthService.md)
357. [SystemHealthPanel](modules/SystemHealthPanel.md)
358. [iterationStore](modules/iterationStore.md)
359. [themeStore](modules/themeStore.md)
360. [planning-masters.test](modules/planning-masters.test.md)
361. [accessibilityInvariants](modules/accessibilityInvariants.md)
362. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
363. [renderWithProviders](modules/renderWithProviders.md)
364. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
365. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
366. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
367. [OverflowMenu.test](modules/OverflowMenu.test.md)
368. [renderWithProviders.test](modules/renderWithProviders.test.md)
369. [setup](modules/setup.md)
370. [types_calendar](modules/types_calendar.md)
371. [deliveryMetrics](modules/deliveryMetrics.md)
372. [types_label](modules/types_label.md)
373. [outboundWebhook](modules/outboundWebhook.md)
374. [requestSource](modules/requestSource.md)
375. [savedView](modules/savedView.md)
376. [schedulingRules](modules/schedulingRules.md)
377. [ConstraintsPanel](modules/ConstraintsPanel.md)
378. [schedulingDisplay](modules/schedulingDisplay.md)
379. [EffortModifierCard](modules/EffortModifierCard.md)
380. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
381. [SchedulingPassCard](modules/SchedulingPassCard.md)
382. [systemSettings](modules/systemSettings.md)
383. [emailSettings](modules/emailSettings.md)
384. [types_team](modules/types_team.md)
385. [types_task](modules/types_task.md)
386. [types_triage](modules/types_triage.md)
387. [KanbanCard](modules/KanbanCard.md)
388. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
389. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
390. [tone](modules/tone.md)
391. [KanbanColumn](modules/KanbanColumn.md)
392. [Pill](modules/Pill.md)
393. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
394. [tone.test](modules/tone.test.md)
395. [attentionRanking](modules/attentionRanking.md)
396. [attentionRanking.test](modules/attentionRanking.test.md)
397. [planningTaskIssues](modules/planningTaskIssues.md)
398. [planningMasters_masters](modules/planningMasters_masters.md)
399. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
400. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
401. [types_agent](modules/types_agent.md)
402. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
403. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
404. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
405. [statusScopes](modules/statusScopes.md)
406. [statusScopes.test](modules/statusScopes.test.md)
407. [modelAwareRouting](modules/modelAwareRouting.md)
408. [types_github](modules/types_github.md)
409. [types_template](modules/types_template.md)
410. [seedDisplay](modules/seedDisplay.md)
411. [workMetrics](modules/workMetrics.md)
412. [WorkMetricsLine](modules/WorkMetricsLine.md)
413. [types_iteration](modules/types_iteration.md)
414. [types_gantt](modules/types_gantt.md)
415. [types_project](modules/types_project.md)
416. [projectStatusStyles](modules/projectStatusStyles.md)
417. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
418. [types_release](modules/types_release.md)
419. [agentAccess](modules/agentAccess.md)
420. [useAgentAccess](modules/useAgentAccess.md)
421. [apiError](modules/apiError.md)
422. [QueryState](modules/QueryState.md)
423. [taskEditorContract](modules/taskEditorContract.md)
424. [TaskBriefEditor](modules/TaskBriefEditor.md)
425. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
426. [taskDraftStorage](modules/taskDraftStorage.md)
427. [adminAccess](modules/adminAccess.md)
428. [api](modules/api.md)
429. [identityService](modules/identityService.md)
430. [identityContext](modules/identityContext.md)
431. [useAdminAccess](modules/useAdminAccess.md)
432. [AdminAccessPanel](modules/AdminAccessPanel.md)
433. [AdminAccessGate](modules/AdminAccessGate.md)
434. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
435. [NativeConnectionPage](modules/NativeConnectionPage.md)
436. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
437. [agentService](modules/agentService.md)
438. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
439. [agentService.test](modules/agentService.test.md)
440. [calendarService](modules/calendarService.md)
441. [PersonCapacity](modules/PersonCapacity.md)
442. [deliveryMetricsService](modules/deliveryMetricsService.md)
443. [discussionService](modules/discussionService.md)
444. [TaskDiscussion](modules/TaskDiscussion.md)
445. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
446. [emailSettingsService](modules/emailSettingsService.md)
447. [exportService](modules/exportService.md)
448. [ganttService](modules/ganttService.md)
449. [githubService](modules/githubService.md)
450. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
451. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
452. [iterationService](modules/iterationService.md)
453. [IterationSelector](modules/IterationSelector.md)
454. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
455. [SidebarIterationCard](modules/SidebarIterationCard.md)
456. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
457. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
458. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
459. [labelService](modules/labelService.md)
460. [LabelSelector](modules/LabelSelector.md)
461. [outboundWebhookService](modules/outboundWebhookService.md)
462. [planShareService](modules/planShareService.md)
463. [projectService](modules/projectService.md)
464. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
465. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
466. [releaseService](modules/releaseService.md)
467. [ReleaseForm](modules/ReleaseForm.md)
468. [requestSourceService](modules/requestSourceService.md)
469. [savedViewService](modules/savedViewService.md)
470. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
471. [AppSidebar](modules/AppSidebar.md)
472. [AppSidebar.test](modules/AppSidebar.test.md)
473. [schedulingRulesService](modules/schedulingRulesService.md)
474. [sessionService](modules/sessionService.md)
475. [snapshotService](modules/snapshotService.md)
476. [systemSettingsService](modules/systemSettingsService.md)
477. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
478. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
479. [taskService](modules/taskService.md)
480. [DeliveryDependencies](modules/DeliveryDependencies.md)
481. [ImportTasksModal](modules/ImportTasksModal.md)
482. [TaskContextSummary](modules/TaskContextSummary.md)
483. [TaskDependencySelector](modules/TaskDependencySelector.md)
484. [TaskSearch](modules/TaskSearch.md)
485. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
486. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
487. [TaskWorkPanel](modules/TaskWorkPanel.md)
488. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
489. [teamService](modules/teamService.md)
490. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
491. [TaskFiltersBar](modules/TaskFiltersBar.md)
492. [taskFilterDefaults](modules/taskFilterDefaults.md)
493. [ImportTeamModal](modules/ImportTeamModal.md)
494. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
495. [TeamForm](modules/TeamForm.md)
496. [TeamForm.test](modules/TeamForm.test.md)
497. [TeamProfileManager](modules/TeamProfileManager.md)
498. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
499. [IdentityProvider](modules/IdentityProvider.md)
500. [UserSessionBadge](modules/UserSessionBadge.md)
501. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
502. [IdentityProvider.test](modules/IdentityProvider.test.md)
503. [CalendarPage](modules/CalendarPage.md)
504. [templateService](modules/templateService.md)
505. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
506. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
507. [triageService](modules/triageService.md)
508. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
509. [usePlanningReadiness](modules/usePlanningReadiness.md)
510. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
511. [copyText](modules/copyText.md)
512. [focusLifecycle](modules/focusLifecycle.md)
513. [focusLifecycle.test](modules/focusLifecycle.test.md)
514. [formatDate](modules/formatDate.md)
515. [TaskStatusFlow](modules/TaskStatusFlow.md)
516. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
517. [IterationForm](modules/IterationForm.md)
518. [IterationForm.test](modules/IterationForm.test.md)
519. [IterationList](modules/IterationList.md)
520. [NotificationsPanel](modules/NotificationsPanel.md)
521. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
522. [StatusChangeControl](modules/StatusChangeControl.md)
523. [VacationManager](modules/VacationManager.md)
524. [TeamList](modules/TeamList.md)
525. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
526. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
527. [AnalyticsPage](modules/AnalyticsPage.md)
528. [IterationsPage](modules/IterationsPage.md)
529. [PlanMasterPage](modules/PlanMasterPage.md)
530. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
531. [PlanPage](modules/PlanPage.md)
532. [PlanPage.test](modules/PlanPage.test.md)
533. [PlanSharePage](modules/PlanSharePage.md)
534. [PlanSharePage.test](modules/PlanSharePage.test.md)
535. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
536. [TeamPage](modules/TeamPage.md)
537. [modelRouting](modules/modelRouting.md)
538. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
539. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
540. [modelRouting.test](modules/modelRouting.test.md)
541. [protectedQueries](modules/protectedQueries.md)
542. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
543. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
544. [AgentAccessPanel](modules/AgentAccessPanel.md)
545. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
546. [AgentModelAdministration](modules/AgentModelAdministration.md)
547. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
548. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
549. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
550. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
551. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
552. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
553. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
554. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
555. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
556. [AgentPipelinePage](modules/AgentPipelinePage.md)
557. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
558. [safeUrl](modules/safeUrl.md)
559. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
560. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
561. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
562. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
563. [savedViewState](modules/savedViewState.md)
564. [savedViewState.test](modules/savedViewState.test.md)
565. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
566. [OverviewPage](modules/OverviewPage.md)
567. [OverviewPage.test](modules/OverviewPage.test.md)
568. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
569. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
570. [CommandMenu](modules/CommandMenu.md)
571. [CommandMenu.test](modules/CommandMenu.test.md)
572. [ContextHelp](modules/ContextHelp.md)
573. [AppTopNav](modules/AppTopNav.md)
574. [AppShell](modules/AppShell.md)
575. [App](modules/App.md)
576. [AppShell.test](modules/AppShell.test.md)
577. [AppTopNav.test](modules/AppTopNav.test.md)
578. [ContextHelp.test](modules/ContextHelp.test.md)
579. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
580. [src_main](modules/src_main.md)
581. [SettingsPage](modules/SettingsPage.md)
582. [SettingsPage.test](modules/SettingsPage.test.md)
583. [taskFilters](modules/taskFilters.md)
584. [taskFilters.test](modules/taskFilters.test.md)
585. [teamMemberLabels](modules/teamMemberLabels.md)
586. [InitiativeForm](modules/InitiativeForm.md)
587. [RoadmapPage](modules/RoadmapPage.md)
588. [RoadmapPage.test](modules/RoadmapPage.test.md)
589. [templateDefaults](modules/templateDefaults.md)
590. [ProjectForm](modules/ProjectForm.md)
591. [TaskForm](modules/TaskForm.md)
592. [TaskEditModal](modules/TaskEditModal.md)
593. [GanttChart](modules/GanttChart.md)
594. [GanttChart.test](modules/GanttChart.test.md)
595. [GuardedTaskModal](modules/GuardedTaskModal.md)
596. [BacklogPanel](modules/BacklogPanel.md)
597. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
598. [ProjectTaskTree](modules/ProjectTaskTree.md)
599. [TaskForm.test](modules/TaskForm.test.md)
600. [GanttPage](modules/GanttPage.md)
601. [GanttPage.test](modules/GanttPage.test.md)
602. [MyWorkPage](modules/MyWorkPage.md)
603. [ProjectDetailPage](modules/ProjectDetailPage.md)
604. [ProjectsPage](modules/ProjectsPage.md)
605. [ProjectsPage.test](modules/ProjectsPage.test.md)
606. [TriagePage](modules/TriagePage.md)
607. [visibleWork](modules/visibleWork.md)
608. [KanbanBoard](modules/KanbanBoard.md)
609. [KanbanBoard.test](modules/KanbanBoard.test.md)
610. [TaskList](modules/TaskList.md)
611. [SavedViewsControl](modules/SavedViewsControl.md)
612. [TaskList.test](modules/TaskList.test.md)
613. [TasksPage](modules/TasksPage.md)
614. [TasksPage.test](modules/TasksPage.test.md)
615. [visibleWork.test](modules/visibleWork.test.md)
616. [tailwind.config](modules/tailwind.config.md)
617. [vite.config](modules/vite.config.md)
618. [vitest.config](modules/vitest.config.md)
619. [create_agent_actor](modules/create_agent_actor.md)
620. [generate_workchord_keys](modules/generate_workchord_keys.md)
621. [setup_agent_team](modules/setup_agent_team.md)
622. [build_agent_skills](modules/build_agent_skills.md)
623. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
624. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
625. [ci_runtime](modules/ci_runtime.md)
626. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
627. [postgres_runtime](modules/postgres_runtime.md)
628. [run_android_checks](modules/run_android_checks.md)
629. [run_disposable_checks](modules/run_disposable_checks.md)
630. [serve_disposable_api](modules/serve_disposable_api.md)
631. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
632. [test_ci_runtime](modules/test_ci_runtime.md)
633. [test_native_runtimes](modules/test_native_runtimes.md)
634. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
635. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
636. [generate_client_contract](modules/generate_client_contract.md)
637. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
638. [load_common](modules/load_common.md)
639. [collect](modules/collect.md)
640. [result](modules/result.md)
641. [compare](modules/compare.md)
642. [finalize](modules/finalize.md)
643. [qualify](modules/qualify.md)
644. [resilience](modules/resilience.md)
645. [run](modules/run.md)
646. [seal](modules/seal.md)
647. [seed](modules/seed.md)

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
| [delivery_observation](modules/delivery_observation.md) | `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen` |
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
| [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md) | `metrics = hoisted`, `projects = hoisted`, `mock`, `mock`, `describe` |
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
| [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md) | `service = hoisted`, `iterations = hoisted`, `mock`, `mock`, `describe` |
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
