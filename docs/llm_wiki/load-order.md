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
37. [20261004_0007_execution_usage](modules/20261004_0007_execution_usage.md)
38. [query_limits](modules/query_limits.md)
39. [runtime_telemetry](modules/runtime_telemetry.md)
40. [database_runtime](modules/database_runtime.md)
41. [maintenance](modules/maintenance.md)
42. [mutation_versions](modules/mutation_versions.md)
43. [schemas_agent_planning](modules/schemas_agent_planning.md)
44. [agent_skill_bundle](modules/agent_skill_bundle.md)
45. [agent_team_setup](modules/agent_team_setup.md)
46. [schemas_autonomy](modules/schemas_autonomy.md)
47. [schemas_common](modules/schemas_common.md)
48. [delivery_metrics](modules/delivery_metrics.md)
49. [schemas_execution_usage](modules/schemas_execution_usage.md)
50. [schemas_github](modules/schemas_github.md)
51. [schemas_intake](modules/schemas_intake.md)
52. [schemas_label](modules/schemas_label.md)
53. [schemas_plan_share](modules/schemas_plan_share.md)
54. [planning_inputs](modules/planning_inputs.md)
55. [schemas_calendar](modules/schemas_calendar.md)
56. [schemas_saved_view](modules/schemas_saved_view.md)
57. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
58. [schemas_session](modules/schemas_session.md)
59. [snapshot](modules/snapshot.md)
60. [schemas_system_settings](modules/schemas_system_settings.md)
61. [schemas_email_settings](modules/schemas_email_settings.md)
62. [schemas_task_brief](modules/schemas_task_brief.md)
63. [schemas_llm](modules/schemas_llm.md)
64. [schemas_task_domain](modules/schemas_task_domain.md)
65. [schemas_team](modules/schemas_team.md)
66. [schemas_template](modules/schemas_template.md)
67. [schemas_work_metrics](modules/schemas_work_metrics.md)
68. [schemas_iteration](modules/schemas_iteration.md)
69. [schemas_project](modules/schemas_project.md)
70. [schemas_release](modules/schemas_release.md)
71. [security](modules/security.md)
72. [agent_routing_policy](modules/agent_routing_policy.md)
73. [agent_routing](modules/agent_routing.md)
74. [agent_routing_rollout](modules/agent_routing_rollout.md)
75. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
76. [language_service](modules/language_service.md)
77. [scheduling_rules_service](modules/scheduling_rules_service.md)
78. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
79. [upgrade_service](modules/upgrade_service.md)
80. [upgrade](modules/upgrade.md)
81. [sql_semantics](modules/sql_semantics.md)
82. [exceptions](modules/exceptions.md)
83. [text_similarity](modules/text_similarity.md)
84. [time](modules/time.md)
85. [observability](modules/observability.md)
86. [app_database](modules/app_database.md)
87. [models_agent](modules/models_agent.md)
88. [models_autonomy](modules/models_autonomy.md)
89. [models_calendar](modules/models_calendar.md)
90. [models_capacity](modules/models_capacity.md)
91. [models_database_migration](modules/models_database_migration.md)
92. [delivery_dependency](modules/delivery_dependency.md)
93. [models_discussion](modules/models_discussion.md)
94. [models_execution_usage](modules/models_execution_usage.md)
95. [models_external_link](modules/models_external_link.md)
96. [models_github](modules/models_github.md)
97. [models_identity](modules/models_identity.md)
98. [models_iteration](modules/models_iteration.md)
99. [models_label](modules/models_label.md)
100. [native_connection](modules/native_connection.md)
101. [models_outbound_webhook](modules/models_outbound_webhook.md)
102. [models_plan_share](modules/models_plan_share.md)
103. [models_release](modules/models_release.md)
104. [models_project](modules/models_project.md)
105. [models_request_source](modules/models_request_source.md)
106. [models_saved_view](modules/models_saved_view.md)
107. [models_system_settings](modules/models_system_settings.md)
108. [models_task](modules/models_task.md)
109. [recovery](modules/recovery.md)
110. [models_task_brief](modules/models_task_brief.md)
111. [delivery_observation](modules/delivery_observation.md)
112. [task_status_log](modules/task_status_log.md)
113. [team_member](modules/team_member.md)
114. [models_template](modules/models_template.md)
115. [models_triage](modules/models_triage.md)
116. [user_session](modules/user_session.md)
117. [models___init__](modules/models___init__.md)
118. [catalog](modules/catalog.md)
119. [database_migration_canonical](modules/database_migration_canonical.md)
120. [source](modules/source.md)
121. [transfer](modules/transfer.md)
122. [cli_database_migration](modules/cli_database_migration.md)
123. [database_migration___init__](modules/database_migration___init__.md)
124. [migrations_env](modules/migrations_env.md)
125. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
126. [calendar_service](modules/calendar_service.md)
127. [calendars](modules/calendars.md)
128. [capacity_service](modules/capacity_service.md)
129. [routers_capacity](modules/routers_capacity.md)
130. [delivery_dependency_service](modules/delivery_dependency_service.md)
131. [delivery_metrics_service](modules/delivery_metrics_service.md)
132. [discussion_service](modules/discussion_service.md)
133. [identity_service](modules/identity_service.md)
134. [iteration_service](modules/iteration_service.md)
135. [iterations](modules/iterations.md)
136. [label_service](modules/label_service.md)
137. [labels](modules/labels.md)
138. [native_session_service](modules/native_session_service.md)
139. [saved_view_service](modules/saved_view_service.md)
140. [session_service](modules/session_service.md)
141. [http_authority](modules/http_authority.md)
142. [routers_identity](modules/routers_identity.md)
143. [saved_views](modules/saved_views.md)
144. [routers_session](modules/routers_session.md)
145. [task_brief_service](modules/task_brief_service.md)
146. [task_context_revision_service](modules/task_context_revision_service.md)
147. [task_domain_service](modules/task_domain_service.md)
148. [task_recovery_service](modules/task_recovery_service.md)
149. [team_service](modules/team_service.md)
150. [routers_team](modules/routers_team.md)
151. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
152. [snapshot_service](modules/snapshot_service.md)
153. [plan_share_service](modules/plan_share_service.md)
154. [plan_shares](modules/plan_shares.md)
155. [template_service](modules/template_service.md)
156. [templates](modules/templates.md)
157. [services_work_metrics](modules/services_work_metrics.md)
158. [import_parser](modules/import_parser.md)
159. [url_policy](modules/url_policy.md)
160. [schemas_external_link](modules/schemas_external_link.md)
161. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
162. [schemas_request_source](modules/schemas_request_source.md)
163. [schemas_task](modules/schemas_task.md)
164. [schemas_gantt](modules/schemas_gantt.md)
165. [task_detail](modules/task_detail.md)
166. [schemas_triage](modules/schemas_triage.md)
167. [schemas___init__](modules/schemas___init__.md)
168. [schemas_agent](modules/schemas_agent.md)
169. [agent_readiness](modules/agent_readiness.md)
170. [llm_service](modules/llm_service.md)
171. [system_settings_service](modules/system_settings_service.md)
172. [routers_system_settings](modules/routers_system_settings.md)
173. [email_settings_service](modules/email_settings_service.md)
174. [routers_email_settings](modules/routers_email_settings.md)
175. [notification_service](modules/notification_service.md)
176. [outbound_webhook_service](modules/outbound_webhook_service.md)
177. [worker](modules/worker.md)
178. [outbound_webhooks](modules/outbound_webhooks.md)
179. [external_link_service](modules/external_link_service.md)
180. [github_status_service](modules/github_status_service.md)
181. [request_source_service](modules/request_source_service.md)
182. [request_sources](modules/request_sources.md)
183. [project_service](modules/project_service.md)
184. [task_detail_service](modules/task_detail_service.md)
185. [task_import_service](modules/task_import_service.md)
186. [task_service](modules/task_service.md)
187. [export](modules/export.md)
188. [snapshots](modules/snapshots.md)
189. [agent_routing_observability](modules/agent_routing_observability.md)
190. [agent_service](modules/agent_service.md)
191. [agent_skill_bundles](modules/agent_skill_bundles.md)
192. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
193. [agent_routing_service](modules/agent_routing_service.md)
194. [agent_team_setup_service](modules/agent_team_setup_service.md)
195. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
196. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
197. [execution_usage_service](modules/execution_usage_service.md)
198. [routers_task_domain](modules/routers_task_domain.md)
199. [delivery_dependencies](modules/delivery_dependencies.md)
200. [routers_discussion](modules/routers_discussion.md)
201. [github_status_automation_service](modules/github_status_automation_service.md)
202. [release_service](modules/release_service.md)
203. [projects](modules/projects.md)
204. [scheduler_service](modules/scheduler_service.md)
205. [routers_gantt](modules/routers_gantt.md)
206. [routers_llm](modules/routers_llm.md)
207. [agent_planning_service](modules/agent_planning_service.md)
208. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
209. [tasks](modules/tasks.md)
210. [task_status_service](modules/task_status_service.md)
211. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
212. [triage_service](modules/triage_service.md)
213. [routers_triage](modules/routers_triage.md)
214. [agent_work_service](modules/agent_work_service.md)
215. [mcp_agent_tools](modules/mcp_agent_tools.md)
216. [mcp_server](modules/mcp_server.md)
217. [routers_agent](modules/routers_agent.md)
218. [routers_agent_planning](modules/routers_agent_planning.md)
219. [agent_catalog](modules/agent_catalog.md)
220. [github_webhook_service](modules/github_webhook_service.md)
221. [routers_github](modules/routers_github.md)
222. [web_intake_service](modules/web_intake_service.md)
223. [routers_intake](modules/routers_intake.md)
224. [app_main](modules/app_main.md)
225. [routers___init__](modules/routers___init__.md)
226. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
227. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
228. [test_server_acceptance](modules/test_server_acceptance.md)
229. [test_work_package_service](modules/test_work_package_service.md)
230. [test_database_configuration](modules/test_database_configuration.md)
231. [test_deployment_topology](modules/test_deployment_topology.md)
232. [test_observability](modules/test_observability.md)
233. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
234. [test_query_boundaries](modules/test_query_boundaries.md)
235. [test_runtime_policy](modules/test_runtime_policy.md)
236. [test_schema_behavior](modules/test_schema_behavior.md)
237. [test_cutover_evidence](modules/test_cutover_evidence.md)
238. [test_documentation_boundary](modules/test_documentation_boundary.md)
239. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
240. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
241. [test_source_preflight](modules/test_source_preflight.md)
242. [test_transfer_catalog](modules/test_transfer_catalog.md)
243. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
244. [0001_wave0_probe](modules/0001_wave0_probe.md)
245. [test_initial_schema](modules/test_initial_schema.md)
246. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
247. [test_load_tooling](modules/test_load_tooling.md)
248. [test_routing_evidence](modules/test_routing_evidence.md)
249. [support_database](modules/support_database.md)
250. [delivery](modules/delivery.md)
251. [factories](modules/factories.md)
252. [faults](modules/faults.md)
253. [runtime_peer](modules/runtime_peer.md)
254. [schema](modules/schema.md)
255. [support___init__](modules/support___init__.md)
256. [conftest](modules/conftest.md)
257. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
258. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
259. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
260. [transactions](modules/transactions.md)
261. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
262. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
263. [test_agent_routing_data](modules/test_agent_routing_data.md)
264. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
265. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
266. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
267. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
268. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
269. [test_agent_routing_service](modules/test_agent_routing_service.md)
270. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
271. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
272. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
273. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
274. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
275. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
276. [test_authority_migrations](modules/test_authority_migrations.md)
277. [test_capacity_contract](modules/test_capacity_contract.md)
278. [test_client_contract](modules/test_client_contract.md)
279. [test_database_harness](modules/test_database_harness.md)
280. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
281. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
282. [test_agent_team_setup](modules/test_agent_team_setup.md)
283. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
284. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
285. [test_execution_usage](modules/test_execution_usage.md)
286. [test_managed_authority](modules/test_managed_authority.md)
287. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
288. [test_mobile_contract](modules/test_mobile_contract.md)
289. [test_mutation_versions](modules/test_mutation_versions.md)
290. [test_native_connections](modules/test_native_connections.md)
291. [test_plan_shares](modules/test_plan_shares.md)
292. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
293. [test_process_roles](modules/test_process_roles.md)
294. [test_profile_capacity](modules/test_profile_capacity.md)
295. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
296. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
297. [test_saved_view_service](modules/test_saved_view_service.md)
298. [test_task_domain](modules/test_task_domain.md)
299. [test_delivery_metrics](modules/test_delivery_metrics.md)
300. [test_human_work_queries](modules/test_human_work_queries.md)
301. [test_task_discussion](modules/test_task_discussion.md)
302. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
303. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
304. [test_work_correctness](modules/test_work_correctness.md)
305. [eslint.config](modules/eslint.config.md)
306. [postcss.config](modules/postcss.config.md)
307. [Button](modules/Button.md)
308. [Button.test](modules/Button.test.md)
309. [Checkbox](modules/Checkbox.md)
310. [CollapsibleSection](modules/CollapsibleSection.md)
311. [Input](modules/Input.md)
312. [Input.test](modules/Input.test.md)
313. [dialogLayer](modules/dialogLayer.md)
314. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
315. [Modal](modules/Modal.md)
316. [ConfirmDialog](modules/ConfirmDialog.md)
317. [useConfirmDialog](modules/useConfirmDialog.md)
318. [WorkFreshness](modules/WorkFreshness.md)
319. [toast](modules/toast.md)
320. [ToastProvider](modules/ToastProvider.md)
321. [Breadcrumbs](modules/Breadcrumbs.md)
322. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
323. [commandMenuEvents](modules/commandMenuEvents.md)
324. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
325. [SortableTaskItem](modules/SortableTaskItem.md)
326. [useDraftDismissal](modules/useDraftDismissal.md)
327. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
328. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
329. [InlineEmptyState](modules/InlineEmptyState.md)
330. [MasterProgress](modules/MasterProgress.md)
331. [MasterProgress.test](modules/MasterProgress.test.md)
332. [OverflowMenu](modules/OverflowMenu.md)
333. [PageLayout](modules/PageLayout.md)
334. [SectionCard](modules/SectionCard.md)
335. [SlideOverDrawer](modules/SlideOverDrawer.md)
336. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
337. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
338. [StickyRail](modules/StickyRail.md)
339. [index](modules/index.md)
340. [overviewTaskThread](modules/overviewTaskThread.md)
341. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
342. [planningReturn](modules/planningReturn.md)
343. [PlanReturnBar](modules/PlanReturnBar.md)
344. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
345. [workQueryFreshness](modules/workQueryFreshness.md)
346. [teamwork.en](modules/teamwork.en.md)
347. [resources.en](modules/resources.en.md)
348. [i18n](modules/i18n.md)
349. [dateLocale](modules/dateLocale.md)
350. [InteractiveCalendar](modules/InteractiveCalendar.md)
351. [teamwork.ru](modules/teamwork.ru.md)
352. [resources.ru](modules/resources.ru.md)
353. [i18n.test](modules/i18n.test.md)
354. [routeModules](modules/routeModules.md)
355. [DocumentMetadata](modules/DocumentMetadata.md)
356. [workspaces](modules/workspaces.md)
357. [helpContexts](modules/helpContexts.md)
358. [workspaces.test](modules/workspaces.test.md)
359. [LandingPage](modules/LandingPage.md)
360. [NotFoundPage](modules/NotFoundPage.md)
361. [healthService](modules/healthService.md)
362. [SystemHealthPanel](modules/SystemHealthPanel.md)
363. [iterationStore](modules/iterationStore.md)
364. [themeStore](modules/themeStore.md)
365. [planning-masters.test](modules/planning-masters.test.md)
366. [accessibilityInvariants](modules/accessibilityInvariants.md)
367. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
368. [renderWithProviders](modules/renderWithProviders.md)
369. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
370. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
371. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
372. [OverflowMenu.test](modules/OverflowMenu.test.md)
373. [renderWithProviders.test](modules/renderWithProviders.test.md)
374. [setup](modules/setup.md)
375. [types_calendar](modules/types_calendar.md)
376. [deliveryMetrics](modules/deliveryMetrics.md)
377. [executionUsage](modules/executionUsage.md)
378. [types_label](modules/types_label.md)
379. [outboundWebhook](modules/outboundWebhook.md)
380. [requestSource](modules/requestSource.md)
381. [savedView](modules/savedView.md)
382. [schedulingRules](modules/schedulingRules.md)
383. [ConstraintsPanel](modules/ConstraintsPanel.md)
384. [schedulingDisplay](modules/schedulingDisplay.md)
385. [EffortModifierCard](modules/EffortModifierCard.md)
386. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
387. [SchedulingPassCard](modules/SchedulingPassCard.md)
388. [systemSettings](modules/systemSettings.md)
389. [emailSettings](modules/emailSettings.md)
390. [types_team](modules/types_team.md)
391. [types_task](modules/types_task.md)
392. [types_triage](modules/types_triage.md)
393. [KanbanCard](modules/KanbanCard.md)
394. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
395. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
396. [tone](modules/tone.md)
397. [KanbanColumn](modules/KanbanColumn.md)
398. [Pill](modules/Pill.md)
399. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
400. [tone.test](modules/tone.test.md)
401. [attentionRanking](modules/attentionRanking.md)
402. [attentionRanking.test](modules/attentionRanking.test.md)
403. [planningTaskIssues](modules/planningTaskIssues.md)
404. [planningMasters_masters](modules/planningMasters_masters.md)
405. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
406. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
407. [types_agent](modules/types_agent.md)
408. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
409. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
410. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
411. [statusScopes](modules/statusScopes.md)
412. [statusScopes.test](modules/statusScopes.test.md)
413. [modelAwareRouting](modules/modelAwareRouting.md)
414. [types_github](modules/types_github.md)
415. [types_template](modules/types_template.md)
416. [seedDisplay](modules/seedDisplay.md)
417. [workMetrics](modules/workMetrics.md)
418. [WorkMetricsLine](modules/WorkMetricsLine.md)
419. [types_iteration](modules/types_iteration.md)
420. [types_gantt](modules/types_gantt.md)
421. [types_project](modules/types_project.md)
422. [projectStatusStyles](modules/projectStatusStyles.md)
423. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
424. [types_release](modules/types_release.md)
425. [agentAccess](modules/agentAccess.md)
426. [useAgentAccess](modules/useAgentAccess.md)
427. [apiError](modules/apiError.md)
428. [QueryState](modules/QueryState.md)
429. [taskEditorContract](modules/taskEditorContract.md)
430. [TaskBriefEditor](modules/TaskBriefEditor.md)
431. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
432. [taskDraftStorage](modules/taskDraftStorage.md)
433. [adminAccess](modules/adminAccess.md)
434. [api](modules/api.md)
435. [identityService](modules/identityService.md)
436. [identityContext](modules/identityContext.md)
437. [useAdminAccess](modules/useAdminAccess.md)
438. [AdminAccessPanel](modules/AdminAccessPanel.md)
439. [AdminAccessGate](modules/AdminAccessGate.md)
440. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
441. [NativeConnectionPage](modules/NativeConnectionPage.md)
442. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
443. [agentService](modules/agentService.md)
444. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
445. [agentService.test](modules/agentService.test.md)
446. [calendarService](modules/calendarService.md)
447. [PersonCapacity](modules/PersonCapacity.md)
448. [deliveryMetricsService](modules/deliveryMetricsService.md)
449. [discussionService](modules/discussionService.md)
450. [TaskDiscussion](modules/TaskDiscussion.md)
451. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
452. [emailSettingsService](modules/emailSettingsService.md)
453. [executionUsageService](modules/executionUsageService.md)
454. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
455. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
456. [exportService](modules/exportService.md)
457. [ganttService](modules/ganttService.md)
458. [githubService](modules/githubService.md)
459. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
460. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
461. [iterationService](modules/iterationService.md)
462. [IterationSelector](modules/IterationSelector.md)
463. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
464. [SidebarIterationCard](modules/SidebarIterationCard.md)
465. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
466. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
467. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
468. [labelService](modules/labelService.md)
469. [LabelSelector](modules/LabelSelector.md)
470. [outboundWebhookService](modules/outboundWebhookService.md)
471. [planShareService](modules/planShareService.md)
472. [projectService](modules/projectService.md)
473. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
474. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
475. [releaseService](modules/releaseService.md)
476. [ReleaseForm](modules/ReleaseForm.md)
477. [requestSourceService](modules/requestSourceService.md)
478. [savedViewService](modules/savedViewService.md)
479. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
480. [AppSidebar](modules/AppSidebar.md)
481. [AppSidebar.test](modules/AppSidebar.test.md)
482. [schedulingRulesService](modules/schedulingRulesService.md)
483. [sessionService](modules/sessionService.md)
484. [snapshotService](modules/snapshotService.md)
485. [systemSettingsService](modules/systemSettingsService.md)
486. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
487. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
488. [taskService](modules/taskService.md)
489. [DeliveryDependencies](modules/DeliveryDependencies.md)
490. [ImportTasksModal](modules/ImportTasksModal.md)
491. [TaskContextSummary](modules/TaskContextSummary.md)
492. [TaskDependencySelector](modules/TaskDependencySelector.md)
493. [TaskSearch](modules/TaskSearch.md)
494. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
495. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
496. [TaskWorkPanel](modules/TaskWorkPanel.md)
497. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
498. [teamService](modules/teamService.md)
499. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
500. [TaskFiltersBar](modules/TaskFiltersBar.md)
501. [taskFilterDefaults](modules/taskFilterDefaults.md)
502. [ImportTeamModal](modules/ImportTeamModal.md)
503. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
504. [TeamForm](modules/TeamForm.md)
505. [TeamForm.test](modules/TeamForm.test.md)
506. [TeamProfileManager](modules/TeamProfileManager.md)
507. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
508. [IdentityProvider](modules/IdentityProvider.md)
509. [UserSessionBadge](modules/UserSessionBadge.md)
510. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
511. [IdentityProvider.test](modules/IdentityProvider.test.md)
512. [CalendarPage](modules/CalendarPage.md)
513. [templateService](modules/templateService.md)
514. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
515. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
516. [triageService](modules/triageService.md)
517. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
518. [usePlanningReadiness](modules/usePlanningReadiness.md)
519. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
520. [copyText](modules/copyText.md)
521. [focusLifecycle](modules/focusLifecycle.md)
522. [focusLifecycle.test](modules/focusLifecycle.test.md)
523. [formatDate](modules/formatDate.md)
524. [TaskStatusFlow](modules/TaskStatusFlow.md)
525. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
526. [IterationForm](modules/IterationForm.md)
527. [IterationForm.test](modules/IterationForm.test.md)
528. [IterationList](modules/IterationList.md)
529. [NotificationsPanel](modules/NotificationsPanel.md)
530. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
531. [StatusChangeControl](modules/StatusChangeControl.md)
532. [VacationManager](modules/VacationManager.md)
533. [TeamList](modules/TeamList.md)
534. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
535. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
536. [AnalyticsPage](modules/AnalyticsPage.md)
537. [IterationsPage](modules/IterationsPage.md)
538. [PlanMasterPage](modules/PlanMasterPage.md)
539. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
540. [PlanPage](modules/PlanPage.md)
541. [PlanPage.test](modules/PlanPage.test.md)
542. [PlanSharePage](modules/PlanSharePage.md)
543. [PlanSharePage.test](modules/PlanSharePage.test.md)
544. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
545. [TeamPage](modules/TeamPage.md)
546. [modelRouting](modules/modelRouting.md)
547. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
548. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
549. [modelRouting.test](modules/modelRouting.test.md)
550. [protectedQueries](modules/protectedQueries.md)
551. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
552. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
553. [AgentAccessPanel](modules/AgentAccessPanel.md)
554. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
555. [AgentModelAdministration](modules/AgentModelAdministration.md)
556. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
557. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
558. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
559. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
560. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
561. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
562. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
563. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
564. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
565. [AgentPipelinePage](modules/AgentPipelinePage.md)
566. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
567. [safeUrl](modules/safeUrl.md)
568. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
569. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
570. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
571. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
572. [savedViewState](modules/savedViewState.md)
573. [savedViewState.test](modules/savedViewState.test.md)
574. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
575. [OverviewPage](modules/OverviewPage.md)
576. [OverviewPage.test](modules/OverviewPage.test.md)
577. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
578. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
579. [CommandMenu](modules/CommandMenu.md)
580. [CommandMenu.test](modules/CommandMenu.test.md)
581. [ContextHelp](modules/ContextHelp.md)
582. [AppTopNav](modules/AppTopNav.md)
583. [AppShell](modules/AppShell.md)
584. [App](modules/App.md)
585. [AppShell.test](modules/AppShell.test.md)
586. [AppTopNav.test](modules/AppTopNav.test.md)
587. [ContextHelp.test](modules/ContextHelp.test.md)
588. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
589. [src_main](modules/src_main.md)
590. [SettingsPage](modules/SettingsPage.md)
591. [SettingsPage.test](modules/SettingsPage.test.md)
592. [taskFilters](modules/taskFilters.md)
593. [taskFilters.test](modules/taskFilters.test.md)
594. [teamMemberLabels](modules/teamMemberLabels.md)
595. [InitiativeForm](modules/InitiativeForm.md)
596. [RoadmapPage](modules/RoadmapPage.md)
597. [RoadmapPage.test](modules/RoadmapPage.test.md)
598. [templateDefaults](modules/templateDefaults.md)
599. [ProjectForm](modules/ProjectForm.md)
600. [TaskForm](modules/TaskForm.md)
601. [TaskEditModal](modules/TaskEditModal.md)
602. [GanttChart](modules/GanttChart.md)
603. [GanttChart.test](modules/GanttChart.test.md)
604. [GuardedTaskModal](modules/GuardedTaskModal.md)
605. [BacklogPanel](modules/BacklogPanel.md)
606. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
607. [ProjectTaskTree](modules/ProjectTaskTree.md)
608. [TaskForm.test](modules/TaskForm.test.md)
609. [GanttPage](modules/GanttPage.md)
610. [GanttPage.test](modules/GanttPage.test.md)
611. [MyWorkPage](modules/MyWorkPage.md)
612. [ProjectDetailPage](modules/ProjectDetailPage.md)
613. [ProjectsPage](modules/ProjectsPage.md)
614. [ProjectsPage.test](modules/ProjectsPage.test.md)
615. [TriagePage](modules/TriagePage.md)
616. [visibleWork](modules/visibleWork.md)
617. [KanbanBoard](modules/KanbanBoard.md)
618. [KanbanBoard.test](modules/KanbanBoard.test.md)
619. [TaskList](modules/TaskList.md)
620. [SavedViewsControl](modules/SavedViewsControl.md)
621. [TaskList.test](modules/TaskList.test.md)
622. [TasksPage](modules/TasksPage.md)
623. [TasksPage.test](modules/TasksPage.test.md)
624. [visibleWork.test](modules/visibleWork.test.md)
625. [tailwind.config](modules/tailwind.config.md)
626. [vite.config](modules/vite.config.md)
627. [vitest.config](modules/vitest.config.md)
628. [create_agent_actor](modules/create_agent_actor.md)
629. [generate_workchord_keys](modules/generate_workchord_keys.md)
630. [setup_agent_team](modules/setup_agent_team.md)
631. [build_agent_skills](modules/build_agent_skills.md)
632. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
633. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
634. [ci_runtime](modules/ci_runtime.md)
635. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
636. [postgres_runtime](modules/postgres_runtime.md)
637. [run_android_checks](modules/run_android_checks.md)
638. [run_disposable_checks](modules/run_disposable_checks.md)
639. [serve_disposable_api](modules/serve_disposable_api.md)
640. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
641. [test_ci_runtime](modules/test_ci_runtime.md)
642. [test_native_runtimes](modules/test_native_runtimes.md)
643. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
644. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
645. [generate_client_contract](modules/generate_client_contract.md)
646. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
647. [load_common](modules/load_common.md)
648. [collect](modules/collect.md)
649. [result](modules/result.md)
650. [compare](modules/compare.md)
651. [finalize](modules/finalize.md)
652. [qualify](modules/qualify.md)
653. [resilience](modules/resilience.md)
654. [run](modules/run.md)
655. [seal](modules/seal.md)
656. [seed](modules/seed.md)

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
| [models_execution_usage](modules/models_execution_usage.md) | `event.listen`, `event.listen` |
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
| [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md) | `metrics = hoisted`, `projects = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md) | `service = hoisted`, `mock`, `describe` |
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
