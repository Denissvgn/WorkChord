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
20. [acceptance_artifacts](modules/acceptance_artifacts.md)
21. [agent_preflight](modules/agent_preflight.md)
22. [cli_server_acceptance](modules/cli_server_acceptance.md)
23. [commands](modules/commands.md)
24. [database_config](modules/database_config.md)
25. [config](modules/config.md)
26. [authority](modules/authority.md)
27. [database_migration_manifest](modules/database_migration_manifest.md)
28. [database_migration_cutover](modules/database_migration_cutover.md)
29. [cli_cutover](modules/cli_cutover.md)
30. [database_migration_closeout](modules/database_migration_closeout.md)
31. [cli_closeout](modules/cli_closeout.md)
32. [project_identity](modules/project_identity.md)
33. [20260928_0001_initial_schema](modules/20260928_0001_initial_schema.md)
34. [20260930_0002_profile_capacity](modules/20260930_0002_profile_capacity.md)
35. [20260930_0003_delivery_dependencies](modules/20260930_0003_delivery_dependencies.md)
36. [20260930_0004_discussion](modules/20260930_0004_discussion.md)
37. [20261003_0005_native_connections](modules/20261003_0005_native_connections.md)
38. [20261004_0006_delivery_observations](modules/20261004_0006_delivery_observations.md)
39. [20261004_0007_execution_usage](modules/20261004_0007_execution_usage.md)
40. [20261007_0008_time_entries](modules/20261007_0008_time_entries.md)
41. [20261008_0009_project_identity](modules/20261008_0009_project_identity.md)
42. [query_limits](modules/query_limits.md)
43. [runtime_telemetry](modules/runtime_telemetry.md)
44. [database_runtime](modules/database_runtime.md)
45. [maintenance](modules/maintenance.md)
46. [mutation_versions](modules/mutation_versions.md)
47. [schemas_agent_planning](modules/schemas_agent_planning.md)
48. [agent_skill_bundle](modules/agent_skill_bundle.md)
49. [agent_team_setup](modules/agent_team_setup.md)
50. [schemas_autonomy](modules/schemas_autonomy.md)
51. [schemas_common](modules/schemas_common.md)
52. [delivery_metrics](modules/delivery_metrics.md)
53. [schemas_execution_usage](modules/schemas_execution_usage.md)
54. [schemas_github](modules/schemas_github.md)
55. [schemas_intake](modules/schemas_intake.md)
56. [schemas_label](modules/schemas_label.md)
57. [schemas_plan_share](modules/schemas_plan_share.md)
58. [planning_inputs](modules/planning_inputs.md)
59. [schemas_calendar](modules/schemas_calendar.md)
60. [schemas_saved_view](modules/schemas_saved_view.md)
61. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
62. [schemas_session](modules/schemas_session.md)
63. [snapshot](modules/snapshot.md)
64. [schemas_system_settings](modules/schemas_system_settings.md)
65. [schemas_email_settings](modules/schemas_email_settings.md)
66. [schemas_task_brief](modules/schemas_task_brief.md)
67. [schemas_llm](modules/schemas_llm.md)
68. [schemas_task_domain](modules/schemas_task_domain.md)
69. [schemas_team](modules/schemas_team.md)
70. [schemas_template](modules/schemas_template.md)
71. [schemas_time_entry](modules/schemas_time_entry.md)
72. [time_report](modules/time_report.md)
73. [schemas_work_metrics](modules/schemas_work_metrics.md)
74. [schemas_iteration](modules/schemas_iteration.md)
75. [schemas_project](modules/schemas_project.md)
76. [schemas_release](modules/schemas_release.md)
77. [security](modules/security.md)
78. [agent_routing_policy](modules/agent_routing_policy.md)
79. [agent_routing](modules/agent_routing.md)
80. [agent_routing_rollout](modules/agent_routing_rollout.md)
81. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
82. [agent_team_credentials](modules/agent_team_credentials.md)
83. [bounded_scope_reads](modules/bounded_scope_reads.md)
84. [language_service](modules/language_service.md)
85. [planning_input_context](modules/planning_input_context.md)
86. [scheduling_rules_service](modules/scheduling_rules_service.md)
87. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
88. [upgrade_service](modules/upgrade_service.md)
89. [upgrade](modules/upgrade.md)
90. [sql_semantics](modules/sql_semantics.md)
91. [exceptions](modules/exceptions.md)
92. [text_similarity](modules/text_similarity.md)
93. [time](modules/time.md)
94. [observability](modules/observability.md)
95. [app_database](modules/app_database.md)
96. [models_agent](modules/models_agent.md)
97. [models_autonomy](modules/models_autonomy.md)
98. [models_calendar](modules/models_calendar.md)
99. [models_capacity](modules/models_capacity.md)
100. [models_database_migration](modules/models_database_migration.md)
101. [delivery_dependency](modules/delivery_dependency.md)
102. [models_discussion](modules/models_discussion.md)
103. [models_execution_usage](modules/models_execution_usage.md)
104. [models_external_link](modules/models_external_link.md)
105. [models_github](modules/models_github.md)
106. [models_identity](modules/models_identity.md)
107. [models_iteration](modules/models_iteration.md)
108. [models_label](modules/models_label.md)
109. [native_connection](modules/native_connection.md)
110. [models_outbound_webhook](modules/models_outbound_webhook.md)
111. [models_plan_share](modules/models_plan_share.md)
112. [models_release](modules/models_release.md)
113. [models_project](modules/models_project.md)
114. [models_request_source](modules/models_request_source.md)
115. [models_saved_view](modules/models_saved_view.md)
116. [models_system_settings](modules/models_system_settings.md)
117. [models_task](modules/models_task.md)
118. [recovery](modules/recovery.md)
119. [models_task_brief](modules/models_task_brief.md)
120. [delivery_observation](modules/delivery_observation.md)
121. [task_status_log](modules/task_status_log.md)
122. [team_member](modules/team_member.md)
123. [models_template](modules/models_template.md)
124. [models_time_entry](modules/models_time_entry.md)
125. [models_triage](modules/models_triage.md)
126. [user_session](modules/user_session.md)
127. [models___init__](modules/models___init__.md)
128. [catalog](modules/catalog.md)
129. [database_migration_canonical](modules/database_migration_canonical.md)
130. [source](modules/source.md)
131. [transfer](modules/transfer.md)
132. [cli_database_migration](modules/cli_database_migration.md)
133. [database_migration___init__](modules/database_migration___init__.md)
134. [migrations_env](modules/migrations_env.md)
135. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
136. [calendar_service](modules/calendar_service.md)
137. [calendars](modules/calendars.md)
138. [capacity_service](modules/capacity_service.md)
139. [routers_capacity](modules/routers_capacity.md)
140. [delivery_dependency_service](modules/delivery_dependency_service.md)
141. [delivery_metrics_service](modules/delivery_metrics_service.md)
142. [discussion_service](modules/discussion_service.md)
143. [identity_service](modules/identity_service.md)
144. [iteration_service](modules/iteration_service.md)
145. [iterations](modules/iterations.md)
146. [label_service](modules/label_service.md)
147. [labels](modules/labels.md)
148. [native_session_service](modules/native_session_service.md)
149. [saved_view_service](modules/saved_view_service.md)
150. [session_service](modules/session_service.md)
151. [http_authority](modules/http_authority.md)
152. [routers_identity](modules/routers_identity.md)
153. [saved_views](modules/saved_views.md)
154. [routers_session](modules/routers_session.md)
155. [task_brief_service](modules/task_brief_service.md)
156. [task_context_revision_service](modules/task_context_revision_service.md)
157. [task_domain_service](modules/task_domain_service.md)
158. [task_hierarchy_service](modules/task_hierarchy_service.md)
159. [task_recovery_service](modules/task_recovery_service.md)
160. [task_timeline_service](modules/task_timeline_service.md)
161. [team_service](modules/team_service.md)
162. [routers_team](modules/routers_team.md)
163. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
164. [snapshot_service](modules/snapshot_service.md)
165. [plan_share_service](modules/plan_share_service.md)
166. [plan_shares](modules/plan_shares.md)
167. [template_service](modules/template_service.md)
168. [templates](modules/templates.md)
169. [time_entry_service](modules/time_entry_service.md)
170. [time_report_service](modules/time_report_service.md)
171. [services_work_metrics](modules/services_work_metrics.md)
172. [import_parser](modules/import_parser.md)
173. [url_policy](modules/url_policy.md)
174. [schemas_external_link](modules/schemas_external_link.md)
175. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
176. [schemas_request_source](modules/schemas_request_source.md)
177. [schemas_task](modules/schemas_task.md)
178. [schemas_gantt](modules/schemas_gantt.md)
179. [task_detail](modules/task_detail.md)
180. [schemas_triage](modules/schemas_triage.md)
181. [schemas___init__](modules/schemas___init__.md)
182. [schemas_agent](modules/schemas_agent.md)
183. [agent_readiness](modules/agent_readiness.md)
184. [llm_service](modules/llm_service.md)
185. [system_settings_service](modules/system_settings_service.md)
186. [routers_system_settings](modules/routers_system_settings.md)
187. [email_settings_service](modules/email_settings_service.md)
188. [routers_email_settings](modules/routers_email_settings.md)
189. [notification_service](modules/notification_service.md)
190. [outbound_webhook_service](modules/outbound_webhook_service.md)
191. [worker](modules/worker.md)
192. [outbound_webhooks](modules/outbound_webhooks.md)
193. [external_link_service](modules/external_link_service.md)
194. [github_status_service](modules/github_status_service.md)
195. [request_source_service](modules/request_source_service.md)
196. [request_sources](modules/request_sources.md)
197. [project_service](modules/project_service.md)
198. [task_detail_service](modules/task_detail_service.md)
199. [task_import_service](modules/task_import_service.md)
200. [task_service](modules/task_service.md)
201. [export](modules/export.md)
202. [snapshots](modules/snapshots.md)
203. [agent_routing_observability](modules/agent_routing_observability.md)
204. [agent_service](modules/agent_service.md)
205. [agent_skill_bundles](modules/agent_skill_bundles.md)
206. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
207. [agent_routing_service](modules/agent_routing_service.md)
208. [agent_team_setup_service](modules/agent_team_setup_service.md)
209. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
210. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
211. [execution_usage_service](modules/execution_usage_service.md)
212. [routers_task_domain](modules/routers_task_domain.md)
213. [delivery_dependencies](modules/delivery_dependencies.md)
214. [routers_discussion](modules/routers_discussion.md)
215. [time_entries](modules/time_entries.md)
216. [github_status_automation_service](modules/github_status_automation_service.md)
217. [release_service](modules/release_service.md)
218. [projects](modules/projects.md)
219. [scheduler_service](modules/scheduler_service.md)
220. [routers_gantt](modules/routers_gantt.md)
221. [routers_llm](modules/routers_llm.md)
222. [agent_planning_service](modules/agent_planning_service.md)
223. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
224. [tasks](modules/tasks.md)
225. [task_status_service](modules/task_status_service.md)
226. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
227. [triage_service](modules/triage_service.md)
228. [routers_triage](modules/routers_triage.md)
229. [agent_work_service](modules/agent_work_service.md)
230. [mcp_agent_tools](modules/mcp_agent_tools.md)
231. [mcp_server](modules/mcp_server.md)
232. [routers_agent](modules/routers_agent.md)
233. [routers_agent_planning](modules/routers_agent_planning.md)
234. [agent_catalog](modules/agent_catalog.md)
235. [github_webhook_service](modules/github_webhook_service.md)
236. [routers_github](modules/routers_github.md)
237. [web_intake_service](modules/web_intake_service.md)
238. [routers_intake](modules/routers_intake.md)
239. [app_main](modules/app_main.md)
240. [routers___init__](modules/routers___init__.md)
241. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
242. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
243. [test_server_acceptance](modules/test_server_acceptance.md)
244. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
245. [test_work_package_service](modules/test_work_package_service.md)
246. [test_database_configuration](modules/test_database_configuration.md)
247. [test_deployment_topology](modules/test_deployment_topology.md)
248. [test_observability](modules/test_observability.md)
249. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
250. [test_query_boundaries](modules/test_query_boundaries.md)
251. [test_runtime_policy](modules/test_runtime_policy.md)
252. [test_schema_behavior](modules/test_schema_behavior.md)
253. [test_cutover_evidence](modules/test_cutover_evidence.md)
254. [test_documentation_boundary](modules/test_documentation_boundary.md)
255. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
256. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
257. [test_source_preflight](modules/test_source_preflight.md)
258. [test_transfer_catalog](modules/test_transfer_catalog.md)
259. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
260. [0001_wave0_probe](modules/0001_wave0_probe.md)
261. [test_initial_schema](modules/test_initial_schema.md)
262. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
263. [test_load_tooling](modules/test_load_tooling.md)
264. [test_local_baseline](modules/test_local_baseline.md)
265. [test_routing_evidence](modules/test_routing_evidence.md)
266. [support_database](modules/support_database.md)
267. [delivery](modules/delivery.md)
268. [factories](modules/factories.md)
269. [faults](modules/faults.md)
270. [runtime_peer](modules/runtime_peer.md)
271. [schema](modules/schema.md)
272. [support___init__](modules/support___init__.md)
273. [conftest](modules/conftest.md)
274. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
275. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
276. [test_project_identity](modules/test_project_identity.md)
277. [test_project_identity_scope](modules/test_project_identity_scope.md)
278. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
279. [transactions](modules/transactions.md)
280. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
281. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
282. [test_agent_routing_data](modules/test_agent_routing_data.md)
283. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
284. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
285. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
286. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
287. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
288. [test_agent_routing_service](modules/test_agent_routing_service.md)
289. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
290. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
291. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
292. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
293. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
294. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
295. [test_authority_migrations](modules/test_authority_migrations.md)
296. [test_capacity_contract](modules/test_capacity_contract.md)
297. [test_client_contract](modules/test_client_contract.md)
298. [test_database_harness](modules/test_database_harness.md)
299. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
300. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
301. [test_agent_team_setup](modules/test_agent_team_setup.md)
302. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
303. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
304. [test_deployment_configuration](modules/test_deployment_configuration.md)
305. [test_effective_deferral](modules/test_effective_deferral.md)
306. [test_execution_usage](modules/test_execution_usage.md)
307. [test_execution_working_dates](modules/test_execution_working_dates.md)
308. [test_managed_authority](modules/test_managed_authority.md)
309. [test_allocation_recovery](modules/test_allocation_recovery.md)
310. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
311. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
312. [test_mobile_contract](modules/test_mobile_contract.md)
313. [test_mutation_versions](modules/test_mutation_versions.md)
314. [test_native_connections](modules/test_native_connections.md)
315. [test_plan_shares](modules/test_plan_shares.md)
316. [test_planning_input_context](modules/test_planning_input_context.md)
317. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
318. [test_process_roles](modules/test_process_roles.md)
319. [test_profile_capacity](modules/test_profile_capacity.md)
320. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
321. [test_project_working_timezone](modules/test_project_working_timezone.md)
322. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
323. [test_saved_view_service](modules/test_saved_view_service.md)
324. [test_task_domain](modules/test_task_domain.md)
325. [test_delivery_metrics](modules/test_delivery_metrics.md)
326. [test_human_work_queries](modules/test_human_work_queries.md)
327. [test_task_discussion](modules/test_task_discussion.md)
328. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
329. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
330. [test_task_pagination](modules/test_task_pagination.md)
331. [test_time_entries](modules/test_time_entries.md)
332. [test_time_reports](modules/test_time_reports.md)
333. [test_work_correctness](modules/test_work_correctness.md)
334. [eslint.config](modules/eslint.config.md)
335. [postcss.config](modules/postcss.config.md)
336. [Button](modules/Button.md)
337. [Button.test](modules/Button.test.md)
338. [Checkbox](modules/Checkbox.md)
339. [CollapsibleSection](modules/CollapsibleSection.md)
340. [Input](modules/Input.md)
341. [Input.test](modules/Input.test.md)
342. [dialogLayer](modules/dialogLayer.md)
343. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
344. [Modal](modules/Modal.md)
345. [ConfirmDialog](modules/ConfirmDialog.md)
346. [useConfirmDialog](modules/useConfirmDialog.md)
347. [LiveWindowStatus](modules/LiveWindowStatus.md)
348. [WorkFreshness](modules/WorkFreshness.md)
349. [toast](modules/toast.md)
350. [ToastProvider](modules/ToastProvider.md)
351. [Breadcrumbs](modules/Breadcrumbs.md)
352. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
353. [commandMenuEvents](modules/commandMenuEvents.md)
354. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
355. [SortableTaskItem](modules/SortableTaskItem.md)
356. [useDraftDismissal](modules/useDraftDismissal.md)
357. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
358. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
359. [InlineEmptyState](modules/InlineEmptyState.md)
360. [MasterProgress](modules/MasterProgress.md)
361. [MasterProgress.test](modules/MasterProgress.test.md)
362. [OverflowMenu](modules/OverflowMenu.md)
363. [PageLayout](modules/PageLayout.md)
364. [SectionCard](modules/SectionCard.md)
365. [SlideOverDrawer](modules/SlideOverDrawer.md)
366. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
367. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
368. [StickyRail](modules/StickyRail.md)
369. [index](modules/index.md)
370. [overviewTaskThread](modules/overviewTaskThread.md)
371. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
372. [planningReturn](modules/planningReturn.md)
373. [PlanReturnBar](modules/PlanReturnBar.md)
374. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
375. [useLiveWindow](modules/useLiveWindow.md)
376. [workQueryFreshness](modules/workQueryFreshness.md)
377. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
378. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
379. [pagination](modules/pagination.md)
380. [teamwork.en](modules/teamwork.en.md)
381. [teamwork.ru](modules/teamwork.ru.md)
382. [timeEntries](modules/timeEntries.md)
383. [resources.en](modules/resources.en.md)
384. [i18n](modules/i18n.md)
385. [dateLocale](modules/dateLocale.md)
386. [InteractiveCalendar](modules/InteractiveCalendar.md)
387. [resources.ru](modules/resources.ru.md)
388. [i18n.test](modules/i18n.test.md)
389. [routeModules](modules/routeModules.md)
390. [DocumentMetadata](modules/DocumentMetadata.md)
391. [workspaces](modules/workspaces.md)
392. [helpContexts](modules/helpContexts.md)
393. [workspaces.test](modules/workspaces.test.md)
394. [LandingPage](modules/LandingPage.md)
395. [NotFoundPage](modules/NotFoundPage.md)
396. [healthService](modules/healthService.md)
397. [SystemHealthPanel](modules/SystemHealthPanel.md)
398. [iterationStore](modules/iterationStore.md)
399. [themeStore](modules/themeStore.md)
400. [planning-masters.test](modules/planning-masters.test.md)
401. [accessibilityInvariants](modules/accessibilityInvariants.md)
402. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
403. [renderWithProviders](modules/renderWithProviders.md)
404. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
405. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
406. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
407. [OverflowMenu.test](modules/OverflowMenu.test.md)
408. [renderWithProviders.test](modules/renderWithProviders.test.md)
409. [setup](modules/setup.md)
410. [types_calendar](modules/types_calendar.md)
411. [deliveryMetrics](modules/deliveryMetrics.md)
412. [executionUsage](modules/executionUsage.md)
413. [types_label](modules/types_label.md)
414. [outboundWebhook](modules/outboundWebhook.md)
415. [requestSource](modules/requestSource.md)
416. [savedView](modules/savedView.md)
417. [schedulingRules](modules/schedulingRules.md)
418. [ConstraintsPanel](modules/ConstraintsPanel.md)
419. [schedulingDisplay](modules/schedulingDisplay.md)
420. [EffortModifierCard](modules/EffortModifierCard.md)
421. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
422. [SchedulingPassCard](modules/SchedulingPassCard.md)
423. [systemSettings](modules/systemSettings.md)
424. [emailSettings](modules/emailSettings.md)
425. [types_team](modules/types_team.md)
426. [types_task](modules/types_task.md)
427. [types_triage](modules/types_triage.md)
428. [KanbanCard](modules/KanbanCard.md)
429. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
430. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
431. [tone](modules/tone.md)
432. [KanbanColumn](modules/KanbanColumn.md)
433. [Pill](modules/Pill.md)
434. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
435. [tone.test](modules/tone.test.md)
436. [attentionRanking](modules/attentionRanking.md)
437. [attentionRanking.test](modules/attentionRanking.test.md)
438. [planningTaskIssues](modules/planningTaskIssues.md)
439. [planningMasters_masters](modules/planningMasters_masters.md)
440. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
441. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
442. [types_agent](modules/types_agent.md)
443. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
444. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
445. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
446. [statusScopes](modules/statusScopes.md)
447. [statusScopes.test](modules/statusScopes.test.md)
448. [modelAwareRouting](modules/modelAwareRouting.md)
449. [types_github](modules/types_github.md)
450. [types_template](modules/types_template.md)
451. [seedDisplay](modules/seedDisplay.md)
452. [workMetrics](modules/workMetrics.md)
453. [WorkMetricsLine](modules/WorkMetricsLine.md)
454. [types_iteration](modules/types_iteration.md)
455. [types_gantt](modules/types_gantt.md)
456. [types_project](modules/types_project.md)
457. [projectStatusStyles](modules/projectStatusStyles.md)
458. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
459. [types_release](modules/types_release.md)
460. [agentAccess](modules/agentAccess.md)
461. [useAgentAccess](modules/useAgentAccess.md)
462. [apiError](modules/apiError.md)
463. [QueryState](modules/QueryState.md)
464. [taskEditorContract](modules/taskEditorContract.md)
465. [TaskBriefEditor](modules/TaskBriefEditor.md)
466. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
467. [taskDraftStorage](modules/taskDraftStorage.md)
468. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
469. [adminAccess](modules/adminAccess.md)
470. [api](modules/api.md)
471. [identityService](modules/identityService.md)
472. [identityContext](modules/identityContext.md)
473. [useAdminAccess](modules/useAdminAccess.md)
474. [AdminAccessPanel](modules/AdminAccessPanel.md)
475. [AdminAccessGate](modules/AdminAccessGate.md)
476. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
477. [NativeConnectionPage](modules/NativeConnectionPage.md)
478. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
479. [agentService](modules/agentService.md)
480. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
481. [AgentTeamStepList](modules/AgentTeamStepList.md)
482. [agentService.test](modules/agentService.test.md)
483. [calendarService](modules/calendarService.md)
484. [PersonCapacity](modules/PersonCapacity.md)
485. [deliveryMetricsService](modules/deliveryMetricsService.md)
486. [discussionService](modules/discussionService.md)
487. [TaskDiscussion](modules/TaskDiscussion.md)
488. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
489. [emailSettingsService](modules/emailSettingsService.md)
490. [executionUsageService](modules/executionUsageService.md)
491. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
492. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
493. [exportService](modules/exportService.md)
494. [ganttService](modules/ganttService.md)
495. [githubService](modules/githubService.md)
496. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
497. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
498. [iterationService](modules/iterationService.md)
499. [IterationSelector](modules/IterationSelector.md)
500. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
501. [SidebarIterationCard](modules/SidebarIterationCard.md)
502. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
503. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
504. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
505. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
506. [useLiveWindow.test](modules/useLiveWindow.test.md)
507. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
508. [labelService](modules/labelService.md)
509. [LabelSelector](modules/LabelSelector.md)
510. [outboundWebhookService](modules/outboundWebhookService.md)
511. [planShareService](modules/planShareService.md)
512. [planningInputService](modules/planningInputService.md)
513. [planningInputService.test](modules/planningInputService.test.md)
514. [projectService](modules/projectService.md)
515. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
516. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
517. [releaseService](modules/releaseService.md)
518. [ReleaseForm](modules/ReleaseForm.md)
519. [requestSourceService](modules/requestSourceService.md)
520. [savedViewService](modules/savedViewService.md)
521. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
522. [AppSidebar](modules/AppSidebar.md)
523. [AppSidebar.test](modules/AppSidebar.test.md)
524. [schedulingRulesService](modules/schedulingRulesService.md)
525. [sessionService](modules/sessionService.md)
526. [snapshotService](modules/snapshotService.md)
527. [systemSettingsService](modules/systemSettingsService.md)
528. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
529. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
530. [taskService](modules/taskService.md)
531. [DeliveryDependencies](modules/DeliveryDependencies.md)
532. [ImportTasksModal](modules/ImportTasksModal.md)
533. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
534. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
535. [TaskContextSummary](modules/TaskContextSummary.md)
536. [TaskDependencySelector](modules/TaskDependencySelector.md)
537. [TaskSearch](modules/TaskSearch.md)
538. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
539. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
540. [TaskWorkPanel](modules/TaskWorkPanel.md)
541. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
542. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
543. [teamService](modules/teamService.md)
544. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
545. [TaskFiltersBar](modules/TaskFiltersBar.md)
546. [taskFilterDefaults](modules/taskFilterDefaults.md)
547. [ImportTeamModal](modules/ImportTeamModal.md)
548. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
549. [TeamForm](modules/TeamForm.md)
550. [TeamForm.test](modules/TeamForm.test.md)
551. [TeamProfileManager](modules/TeamProfileManager.md)
552. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
553. [IdentityProvider](modules/IdentityProvider.md)
554. [UserSessionBadge](modules/UserSessionBadge.md)
555. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
556. [IdentityProvider.test](modules/IdentityProvider.test.md)
557. [CalendarPage](modules/CalendarPage.md)
558. [templateService](modules/templateService.md)
559. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
560. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
561. [timeEntryService](modules/timeEntryService.md)
562. [useTimeEntries](modules/useTimeEntries.md)
563. [timeEntryService.test](modules/timeEntryService.test.md)
564. [triageService](modules/triageService.md)
565. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
566. [usePlanningReadiness](modules/usePlanningReadiness.md)
567. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
568. [copyText](modules/copyText.md)
569. [focusLifecycle](modules/focusLifecycle.md)
570. [focusLifecycle.test](modules/focusLifecycle.test.md)
571. [formatDate](modules/formatDate.md)
572. [TaskStatusFlow](modules/TaskStatusFlow.md)
573. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
574. [IterationForm](modules/IterationForm.md)
575. [IterationForm.test](modules/IterationForm.test.md)
576. [IterationList](modules/IterationList.md)
577. [NotificationsPanel](modules/NotificationsPanel.md)
578. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
579. [StatusChangeControl](modules/StatusChangeControl.md)
580. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
581. [TimeEntriesReport](modules/TimeEntriesReport.md)
582. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
583. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
584. [VacationManager](modules/VacationManager.md)
585. [TeamList](modules/TeamList.md)
586. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
587. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
588. [AnalyticsPage](modules/AnalyticsPage.md)
589. [IterationsPage](modules/IterationsPage.md)
590. [PlanMasterPage](modules/PlanMasterPage.md)
591. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
592. [PlanPage](modules/PlanPage.md)
593. [PlanPage.test](modules/PlanPage.test.md)
594. [PlanSharePage](modules/PlanSharePage.md)
595. [PlanSharePage.test](modules/PlanSharePage.test.md)
596. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
597. [TeamPage](modules/TeamPage.md)
598. [graphLimitError](modules/graphLimitError.md)
599. [modelRouting](modules/modelRouting.md)
600. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
601. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
602. [modelRouting.test](modules/modelRouting.test.md)
603. [protectedQueries](modules/protectedQueries.md)
604. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
605. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
606. [AgentAccessPanel](modules/AgentAccessPanel.md)
607. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
608. [AgentModelAdministration](modules/AgentModelAdministration.md)
609. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
610. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
611. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
612. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
613. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
614. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
615. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
616. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
617. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
618. [AgentPipelinePage](modules/AgentPipelinePage.md)
619. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
620. [safeUrl](modules/safeUrl.md)
621. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
622. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
623. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
624. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
625. [savedViewState](modules/savedViewState.md)
626. [savedViewState.test](modules/savedViewState.test.md)
627. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
628. [OverviewPage](modules/OverviewPage.md)
629. [OverviewPage.test](modules/OverviewPage.test.md)
630. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
631. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
632. [CommandMenu](modules/CommandMenu.md)
633. [CommandMenu.test](modules/CommandMenu.test.md)
634. [ContextHelp](modules/ContextHelp.md)
635. [AppTopNav](modules/AppTopNav.md)
636. [AppShell](modules/AppShell.md)
637. [App](modules/App.md)
638. [AppShell.test](modules/AppShell.test.md)
639. [AppTopNav.test](modules/AppTopNav.test.md)
640. [ContextHelp.test](modules/ContextHelp.test.md)
641. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
642. [src_main](modules/src_main.md)
643. [SettingsPage](modules/SettingsPage.md)
644. [SettingsPage.test](modules/SettingsPage.test.md)
645. [taskFilters](modules/taskFilters.md)
646. [taskFilters.test](modules/taskFilters.test.md)
647. [teamMemberLabels](modules/teamMemberLabels.md)
648. [InitiativeForm](modules/InitiativeForm.md)
649. [RoadmapPage](modules/RoadmapPage.md)
650. [RoadmapPage.test](modules/RoadmapPage.test.md)
651. [templateDefaults](modules/templateDefaults.md)
652. [ProjectForm](modules/ProjectForm.md)
653. [TaskForm](modules/TaskForm.md)
654. [TaskEditModal](modules/TaskEditModal.md)
655. [GanttChart](modules/GanttChart.md)
656. [GanttChart.test](modules/GanttChart.test.md)
657. [GuardedTaskModal](modules/GuardedTaskModal.md)
658. [BacklogPanel](modules/BacklogPanel.md)
659. [CurrentTaskModal.test](modules/CurrentTaskModal.test.md)
660. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
661. [ProjectTaskTree](modules/ProjectTaskTree.md)
662. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
663. [TaskForm.test](modules/TaskForm.test.md)
664. [GanttPage](modules/GanttPage.md)
665. [GanttPage.test](modules/GanttPage.test.md)
666. [MyWorkPage](modules/MyWorkPage.md)
667. [MyWorkPage.test](modules/MyWorkPage.test.md)
668. [ProjectDetailPage](modules/ProjectDetailPage.md)
669. [ProjectsPage](modules/ProjectsPage.md)
670. [ProjectsPage.test](modules/ProjectsPage.test.md)
671. [TriagePage](modules/TriagePage.md)
672. [visibleWork](modules/visibleWork.md)
673. [KanbanBoard](modules/KanbanBoard.md)
674. [KanbanBoard.test](modules/KanbanBoard.test.md)
675. [TaskList](modules/TaskList.md)
676. [SavedViewsControl](modules/SavedViewsControl.md)
677. [TaskList.test](modules/TaskList.test.md)
678. [taskViewState](modules/taskViewState.md)
679. [TasksPage](modules/TasksPage.md)
680. [TasksPage.test](modules/TasksPage.test.md)
681. [visibleWork.test](modules/visibleWork.test.md)
682. [tailwind.config](modules/tailwind.config.md)
683. [vite.config](modules/vite.config.md)
684. [vitest.config](modules/vitest.config.md)
685. [create_agent_actor](modules/create_agent_actor.md)
686. [generate_workchord_keys](modules/generate_workchord_keys.md)
687. [setup_agent_team](modules/setup_agent_team.md)
688. [build_agent_skills](modules/build_agent_skills.md)
689. [apt_runtime](modules/apt_runtime.md)
690. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
691. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
692. [ci_runtime](modules/ci_runtime.md)
693. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
694. [postgres_runtime](modules/postgres_runtime.md)
695. [run_android_checks](modules/run_android_checks.md)
696. [run_disposable_checks](modules/run_disposable_checks.md)
697. [serve_disposable_api](modules/serve_disposable_api.md)
698. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
699. [test_apt_runtime](modules/test_apt_runtime.md)
700. [test_ci_runtime](modules/test_ci_runtime.md)
701. [test_native_runtimes](modules/test_native_runtimes.md)
702. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
703. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
704. [generate_client_contract](modules/generate_client_contract.md)
705. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
706. [load_common](modules/load_common.md)
707. [collect](modules/collect.md)
708. [result](modules/result.md)
709. [compare](modules/compare.md)
710. [finalize](modules/finalize.md)
711. [qualify](modules/qualify.md)
712. [resilience](modules/resilience.md)
713. [run](modules/run.md)
714. [local_baseline](modules/local_baseline.md)
715. [seal](modules/seal.md)
716. [seed](modules/seed.md)
717. [service_worksets](modules/service_worksets.md)
718. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)

## Module-level side effects

| Module | Import-time calls |
|--------|-------------------|
| [acceptance_artifacts](modules/acceptance_artifacts.md) | `RECEIPT_NAME = re.compile`, `PUBLIC_PIN_NAME = re.compile` |
| [build_identity](modules/build_identity.md) | `BUILD_IDENTITY_PATH = Path` |
| [app_database](modules/app_database.md) | `settings = get_settings`, `database_configuration = parse_database_configuration`, `engine = create_async_engine`, `install_database_instrumentation`, `async_session_maker = async_sessionmaker` |
| [database_config](modules/database_config.md) | `_POSTGRESQL_CONNECTION_QUERY_KEYS = frozenset`, `_APPLICATION_NAME_PATTERN = re.compile`, `_POSTGRESQL_ROLE_PATTERN = re.compile` |
| [catalog](modules/catalog.md) | `TARGET_OWNED_TABLES = frozenset`, `TEXT_JSON_COLUMNS = frozenset` |
| [database_migration_closeout](modules/database_migration_closeout.md) | `POSTGRESQL_VERSION_PATTERN = re.compile`, `SAFE_IDENTIFIER_PATTERN = re.compile`, `APPLICATION_VERSION_PATTERN = re.compile`, `RELEASE_GATE_IDS = tuple`, `NON_WAIVABLE_TASKS = frozenset`, `NON_WAIVABLE_GATES = frozenset` |
| [database_migration_cutover](modules/database_migration_cutover.md) | `SHA256_PATTERN = re.compile`, `COMMIT_PATTERN = re.compile`, `IMAGE_PATTERN = re.compile`, `GATE_IDS = tuple`, `OPERATOR_ROLES = frozenset`, `DOCUMENTATION_CHECKS = frozenset`, `QUALIFICATION_GATES = frozenset` |
| [source](modules/source.md) | `DRAIN_EVIDENCE_MAX_AGE = timedelta` |
| [transfer](modules/transfer.md) | `MIGRATION_LOADER_LOCK_NAMESPACE = int.from_bytes`, `REPAIR_OWNED_TABLES = frozenset` |
| [database_runtime](modules/database_runtime.md) | `logger = logging.getLogger`, `T = TypeVar`, `RETRYABLE_TRANSACTION_SQLSTATES = frozenset`, `RETRYABLE_CONNECTION_SQLSTATES = frozenset` |
| [app_main](modules/app_main.md) | `settings = get_settings`, `app = FastAPI`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.add_middleware`, `app.add_middleware`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `mount_mcp_http` |
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
| [time_entries](modules/time_entries.md) | `router = APIRouter` |
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
| [TimeEntriesReport.test](modules/TimeEntriesReport.test.md) | `capability = hoisted`, `mock`, `it` |
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
| [CurrentTaskModal.test](modules/CurrentTaskModal.test.md) | `service = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it` |
| [KanbanBoard.test](modules/KanbanBoard.test.md) | `dragState = hoisted`, `taskServiceMock = hoisted`, `teamServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [KanbanCard](modules/KanbanCard.md) | `t = bind` |
| [KanbanColumn](modules/KanbanColumn.md) | `t = bind` |
| [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md) | `lookup = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it` |
| [SavedViewsControl](modules/SavedViewsControl.md) | `t = bind` |
| [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md) | `describe` |
| [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md) | `t = bind` |
| [TaskBriefEditor.test](modules/TaskBriefEditor.test.md) | `describe` |
| [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md) | `t = bind` |
| [TaskDependencySelector](modules/TaskDependencySelector.md) | `t = bind` |
| [TaskDiscussion.test](modules/TaskDiscussion.test.md) | `service = hoisted`, `mock`, `describe` |
| [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `it` |
| [TaskForm.test](modules/TaskForm.test.md) | `api = hoisted`, `mock`, `describe` |
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md) | `service = hoisted`, `iterations = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind` |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | `service = hoisted`, `mock`, `mock`, `describe` |
| [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md) | `service = hoisted`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it`, `it.each([true, false])`, `it` |
| [taskDraftStorage.test](modules/taskDraftStorage.test.md) | `it` |
| [useDraftDismissal.test](modules/useDraftDismissal.test.md) | `it`, `describe`, `it` |
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
| [useLiveWindow.test](modules/useLiveWindow.test.md) | `it`, `it.each([0, -1, NaN, undefined])`, `it`, `it`, `it` |
| [workQueryFreshness.test](modules/workQueryFreshness.test.md) | `cases = flatMap`, `it.each(cases)` |
| [workQueryFreshness](modules/workQueryFreshness.md) | `WORKSPACE_QUERY_POLICIES = fromEntries` |
| [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md) | `it.each(['hidden', 'disabled', 'unauthorized', 'too-many-pages'])`, `it`, `it`, `it`, `it` |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | `describe` |
| [i18n.test](modules/i18n.test.md) | `describe` |
| [src_main](modules/src_main.md) | `queryClient = QueryClient`, `router = createBrowserRouter`, `render` |
| [workspaces.test](modules/workspaces.test.md) | `describe` |
| [workspaces](modules/workspaces.md) | `PRIMARY_NAV_ITEMS = flatMap` |
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set`, `TASK_STATUSES = Set` |
| [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe` |
| [GanttPage.test](modules/GanttPage.test.md) | `ganttServiceMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [MyWorkPage.test](modules/MyWorkPage.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `it`, `it` |
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
| [planningInputService.test](modules/planningInputService.test.md) | `mock`, `beforeEach`, `it`, `it` |
| [timeEntryService.test](modules/timeEntryService.test.md) | `api = hoisted`, `mock`, `beforeEach`, `it`, `it` |
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
| [test_apt_runtime](modules/test_apt_runtime.md) | `sys.path.insert` |
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
| [export_acceptance_artifacts](modules/export_acceptance_artifacts.md) | `sys.path.insert` |

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
| `create_entry` | factory | [time_entries](modules/time_entries.md) |
| `create_triage_item` | factory | [routers_triage](modules/routers_triage.md) |
| `setup_exception_handlers` | wiring | [exceptions](modules/exceptions.md) |
| `configure_database` | wiring | [conftest](modules/conftest.md) |
| `create_empty_project_as_owner` | factory | [test_managed_authority](modules/test_managed_authority.md) |
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
