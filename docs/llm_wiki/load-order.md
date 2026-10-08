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
31. [project_identity](modules/project_identity.md)
32. [20260928_0001_initial_schema](modules/20260928_0001_initial_schema.md)
33. [20260930_0002_profile_capacity](modules/20260930_0002_profile_capacity.md)
34. [20260930_0003_delivery_dependencies](modules/20260930_0003_delivery_dependencies.md)
35. [20260930_0004_discussion](modules/20260930_0004_discussion.md)
36. [20261003_0005_native_connections](modules/20261003_0005_native_connections.md)
37. [20261004_0006_delivery_observations](modules/20261004_0006_delivery_observations.md)
38. [20261004_0007_execution_usage](modules/20261004_0007_execution_usage.md)
39. [20261007_0008_time_entries](modules/20261007_0008_time_entries.md)
40. [20261008_0009_project_identity](modules/20261008_0009_project_identity.md)
41. [query_limits](modules/query_limits.md)
42. [runtime_telemetry](modules/runtime_telemetry.md)
43. [database_runtime](modules/database_runtime.md)
44. [maintenance](modules/maintenance.md)
45. [mutation_versions](modules/mutation_versions.md)
46. [schemas_agent_planning](modules/schemas_agent_planning.md)
47. [agent_skill_bundle](modules/agent_skill_bundle.md)
48. [agent_team_setup](modules/agent_team_setup.md)
49. [schemas_autonomy](modules/schemas_autonomy.md)
50. [schemas_common](modules/schemas_common.md)
51. [delivery_metrics](modules/delivery_metrics.md)
52. [schemas_execution_usage](modules/schemas_execution_usage.md)
53. [schemas_github](modules/schemas_github.md)
54. [schemas_intake](modules/schemas_intake.md)
55. [schemas_label](modules/schemas_label.md)
56. [schemas_plan_share](modules/schemas_plan_share.md)
57. [planning_inputs](modules/planning_inputs.md)
58. [schemas_calendar](modules/schemas_calendar.md)
59. [schemas_saved_view](modules/schemas_saved_view.md)
60. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
61. [schemas_session](modules/schemas_session.md)
62. [snapshot](modules/snapshot.md)
63. [schemas_system_settings](modules/schemas_system_settings.md)
64. [schemas_email_settings](modules/schemas_email_settings.md)
65. [schemas_task_brief](modules/schemas_task_brief.md)
66. [schemas_llm](modules/schemas_llm.md)
67. [schemas_task_domain](modules/schemas_task_domain.md)
68. [schemas_team](modules/schemas_team.md)
69. [schemas_template](modules/schemas_template.md)
70. [schemas_time_entry](modules/schemas_time_entry.md)
71. [time_report](modules/time_report.md)
72. [schemas_work_metrics](modules/schemas_work_metrics.md)
73. [schemas_iteration](modules/schemas_iteration.md)
74. [schemas_project](modules/schemas_project.md)
75. [schemas_release](modules/schemas_release.md)
76. [security](modules/security.md)
77. [agent_routing_policy](modules/agent_routing_policy.md)
78. [agent_routing](modules/agent_routing.md)
79. [agent_routing_rollout](modules/agent_routing_rollout.md)
80. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
81. [agent_team_credentials](modules/agent_team_credentials.md)
82. [bounded_scope_reads](modules/bounded_scope_reads.md)
83. [language_service](modules/language_service.md)
84. [scheduling_rules_service](modules/scheduling_rules_service.md)
85. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
86. [upgrade_service](modules/upgrade_service.md)
87. [upgrade](modules/upgrade.md)
88. [sql_semantics](modules/sql_semantics.md)
89. [exceptions](modules/exceptions.md)
90. [text_similarity](modules/text_similarity.md)
91. [time](modules/time.md)
92. [observability](modules/observability.md)
93. [app_database](modules/app_database.md)
94. [models_agent](modules/models_agent.md)
95. [models_autonomy](modules/models_autonomy.md)
96. [models_calendar](modules/models_calendar.md)
97. [models_capacity](modules/models_capacity.md)
98. [models_database_migration](modules/models_database_migration.md)
99. [delivery_dependency](modules/delivery_dependency.md)
100. [models_discussion](modules/models_discussion.md)
101. [models_execution_usage](modules/models_execution_usage.md)
102. [models_external_link](modules/models_external_link.md)
103. [models_github](modules/models_github.md)
104. [models_identity](modules/models_identity.md)
105. [models_iteration](modules/models_iteration.md)
106. [models_label](modules/models_label.md)
107. [native_connection](modules/native_connection.md)
108. [models_outbound_webhook](modules/models_outbound_webhook.md)
109. [models_plan_share](modules/models_plan_share.md)
110. [models_release](modules/models_release.md)
111. [models_project](modules/models_project.md)
112. [models_request_source](modules/models_request_source.md)
113. [models_saved_view](modules/models_saved_view.md)
114. [models_system_settings](modules/models_system_settings.md)
115. [models_task](modules/models_task.md)
116. [recovery](modules/recovery.md)
117. [models_task_brief](modules/models_task_brief.md)
118. [delivery_observation](modules/delivery_observation.md)
119. [task_status_log](modules/task_status_log.md)
120. [team_member](modules/team_member.md)
121. [models_template](modules/models_template.md)
122. [models_time_entry](modules/models_time_entry.md)
123. [models_triage](modules/models_triage.md)
124. [user_session](modules/user_session.md)
125. [models___init__](modules/models___init__.md)
126. [catalog](modules/catalog.md)
127. [database_migration_canonical](modules/database_migration_canonical.md)
128. [source](modules/source.md)
129. [transfer](modules/transfer.md)
130. [cli_database_migration](modules/cli_database_migration.md)
131. [database_migration___init__](modules/database_migration___init__.md)
132. [migrations_env](modules/migrations_env.md)
133. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
134. [calendar_service](modules/calendar_service.md)
135. [calendars](modules/calendars.md)
136. [capacity_service](modules/capacity_service.md)
137. [routers_capacity](modules/routers_capacity.md)
138. [delivery_dependency_service](modules/delivery_dependency_service.md)
139. [delivery_metrics_service](modules/delivery_metrics_service.md)
140. [discussion_service](modules/discussion_service.md)
141. [identity_service](modules/identity_service.md)
142. [iteration_service](modules/iteration_service.md)
143. [iterations](modules/iterations.md)
144. [label_service](modules/label_service.md)
145. [labels](modules/labels.md)
146. [native_session_service](modules/native_session_service.md)
147. [saved_view_service](modules/saved_view_service.md)
148. [session_service](modules/session_service.md)
149. [http_authority](modules/http_authority.md)
150. [routers_identity](modules/routers_identity.md)
151. [saved_views](modules/saved_views.md)
152. [routers_session](modules/routers_session.md)
153. [task_brief_service](modules/task_brief_service.md)
154. [task_context_revision_service](modules/task_context_revision_service.md)
155. [task_domain_service](modules/task_domain_service.md)
156. [task_hierarchy_service](modules/task_hierarchy_service.md)
157. [task_recovery_service](modules/task_recovery_service.md)
158. [task_timeline_service](modules/task_timeline_service.md)
159. [team_service](modules/team_service.md)
160. [routers_team](modules/routers_team.md)
161. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
162. [snapshot_service](modules/snapshot_service.md)
163. [plan_share_service](modules/plan_share_service.md)
164. [plan_shares](modules/plan_shares.md)
165. [template_service](modules/template_service.md)
166. [templates](modules/templates.md)
167. [time_entry_service](modules/time_entry_service.md)
168. [time_report_service](modules/time_report_service.md)
169. [services_work_metrics](modules/services_work_metrics.md)
170. [import_parser](modules/import_parser.md)
171. [url_policy](modules/url_policy.md)
172. [schemas_external_link](modules/schemas_external_link.md)
173. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
174. [schemas_request_source](modules/schemas_request_source.md)
175. [schemas_task](modules/schemas_task.md)
176. [schemas_gantt](modules/schemas_gantt.md)
177. [task_detail](modules/task_detail.md)
178. [schemas_triage](modules/schemas_triage.md)
179. [schemas___init__](modules/schemas___init__.md)
180. [schemas_agent](modules/schemas_agent.md)
181. [agent_readiness](modules/agent_readiness.md)
182. [llm_service](modules/llm_service.md)
183. [system_settings_service](modules/system_settings_service.md)
184. [routers_system_settings](modules/routers_system_settings.md)
185. [email_settings_service](modules/email_settings_service.md)
186. [routers_email_settings](modules/routers_email_settings.md)
187. [notification_service](modules/notification_service.md)
188. [outbound_webhook_service](modules/outbound_webhook_service.md)
189. [worker](modules/worker.md)
190. [outbound_webhooks](modules/outbound_webhooks.md)
191. [external_link_service](modules/external_link_service.md)
192. [github_status_service](modules/github_status_service.md)
193. [request_source_service](modules/request_source_service.md)
194. [request_sources](modules/request_sources.md)
195. [project_service](modules/project_service.md)
196. [task_detail_service](modules/task_detail_service.md)
197. [task_import_service](modules/task_import_service.md)
198. [task_service](modules/task_service.md)
199. [export](modules/export.md)
200. [snapshots](modules/snapshots.md)
201. [agent_routing_observability](modules/agent_routing_observability.md)
202. [agent_service](modules/agent_service.md)
203. [agent_skill_bundles](modules/agent_skill_bundles.md)
204. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
205. [agent_routing_service](modules/agent_routing_service.md)
206. [agent_team_setup_service](modules/agent_team_setup_service.md)
207. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
208. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
209. [execution_usage_service](modules/execution_usage_service.md)
210. [routers_task_domain](modules/routers_task_domain.md)
211. [delivery_dependencies](modules/delivery_dependencies.md)
212. [routers_discussion](modules/routers_discussion.md)
213. [time_entries](modules/time_entries.md)
214. [github_status_automation_service](modules/github_status_automation_service.md)
215. [release_service](modules/release_service.md)
216. [projects](modules/projects.md)
217. [scheduler_service](modules/scheduler_service.md)
218. [routers_gantt](modules/routers_gantt.md)
219. [routers_llm](modules/routers_llm.md)
220. [agent_planning_service](modules/agent_planning_service.md)
221. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
222. [tasks](modules/tasks.md)
223. [task_status_service](modules/task_status_service.md)
224. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
225. [triage_service](modules/triage_service.md)
226. [routers_triage](modules/routers_triage.md)
227. [agent_work_service](modules/agent_work_service.md)
228. [mcp_agent_tools](modules/mcp_agent_tools.md)
229. [mcp_server](modules/mcp_server.md)
230. [routers_agent](modules/routers_agent.md)
231. [routers_agent_planning](modules/routers_agent_planning.md)
232. [agent_catalog](modules/agent_catalog.md)
233. [github_webhook_service](modules/github_webhook_service.md)
234. [routers_github](modules/routers_github.md)
235. [web_intake_service](modules/web_intake_service.md)
236. [routers_intake](modules/routers_intake.md)
237. [app_main](modules/app_main.md)
238. [routers___init__](modules/routers___init__.md)
239. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
240. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
241. [test_server_acceptance](modules/test_server_acceptance.md)
242. [test_work_package_service](modules/test_work_package_service.md)
243. [test_database_configuration](modules/test_database_configuration.md)
244. [test_deployment_topology](modules/test_deployment_topology.md)
245. [test_observability](modules/test_observability.md)
246. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
247. [test_query_boundaries](modules/test_query_boundaries.md)
248. [test_runtime_policy](modules/test_runtime_policy.md)
249. [test_schema_behavior](modules/test_schema_behavior.md)
250. [test_cutover_evidence](modules/test_cutover_evidence.md)
251. [test_documentation_boundary](modules/test_documentation_boundary.md)
252. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
253. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
254. [test_source_preflight](modules/test_source_preflight.md)
255. [test_transfer_catalog](modules/test_transfer_catalog.md)
256. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
257. [0001_wave0_probe](modules/0001_wave0_probe.md)
258. [test_initial_schema](modules/test_initial_schema.md)
259. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
260. [test_load_tooling](modules/test_load_tooling.md)
261. [test_local_baseline](modules/test_local_baseline.md)
262. [test_routing_evidence](modules/test_routing_evidence.md)
263. [support_database](modules/support_database.md)
264. [delivery](modules/delivery.md)
265. [factories](modules/factories.md)
266. [faults](modules/faults.md)
267. [runtime_peer](modules/runtime_peer.md)
268. [schema](modules/schema.md)
269. [support___init__](modules/support___init__.md)
270. [conftest](modules/conftest.md)
271. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
272. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
273. [test_project_identity](modules/test_project_identity.md)
274. [test_project_identity_scope](modules/test_project_identity_scope.md)
275. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
276. [transactions](modules/transactions.md)
277. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
278. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
279. [test_agent_routing_data](modules/test_agent_routing_data.md)
280. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
281. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
282. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
283. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
284. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
285. [test_agent_routing_service](modules/test_agent_routing_service.md)
286. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
287. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
288. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
289. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
290. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
291. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
292. [test_authority_migrations](modules/test_authority_migrations.md)
293. [test_capacity_contract](modules/test_capacity_contract.md)
294. [test_client_contract](modules/test_client_contract.md)
295. [test_database_harness](modules/test_database_harness.md)
296. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
297. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
298. [test_agent_team_setup](modules/test_agent_team_setup.md)
299. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
300. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
301. [test_deployment_configuration](modules/test_deployment_configuration.md)
302. [test_execution_usage](modules/test_execution_usage.md)
303. [test_managed_authority](modules/test_managed_authority.md)
304. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
305. [test_mobile_contract](modules/test_mobile_contract.md)
306. [test_mutation_versions](modules/test_mutation_versions.md)
307. [test_native_connections](modules/test_native_connections.md)
308. [test_plan_shares](modules/test_plan_shares.md)
309. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
310. [test_process_roles](modules/test_process_roles.md)
311. [test_profile_capacity](modules/test_profile_capacity.md)
312. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
313. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
314. [test_saved_view_service](modules/test_saved_view_service.md)
315. [test_task_domain](modules/test_task_domain.md)
316. [test_delivery_metrics](modules/test_delivery_metrics.md)
317. [test_human_work_queries](modules/test_human_work_queries.md)
318. [test_task_discussion](modules/test_task_discussion.md)
319. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
320. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
321. [test_task_pagination](modules/test_task_pagination.md)
322. [test_time_entries](modules/test_time_entries.md)
323. [test_time_reports](modules/test_time_reports.md)
324. [test_work_correctness](modules/test_work_correctness.md)
325. [eslint.config](modules/eslint.config.md)
326. [postcss.config](modules/postcss.config.md)
327. [Button](modules/Button.md)
328. [Button.test](modules/Button.test.md)
329. [Checkbox](modules/Checkbox.md)
330. [CollapsibleSection](modules/CollapsibleSection.md)
331. [Input](modules/Input.md)
332. [Input.test](modules/Input.test.md)
333. [dialogLayer](modules/dialogLayer.md)
334. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
335. [Modal](modules/Modal.md)
336. [ConfirmDialog](modules/ConfirmDialog.md)
337. [useConfirmDialog](modules/useConfirmDialog.md)
338. [WorkFreshness](modules/WorkFreshness.md)
339. [toast](modules/toast.md)
340. [ToastProvider](modules/ToastProvider.md)
341. [Breadcrumbs](modules/Breadcrumbs.md)
342. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
343. [commandMenuEvents](modules/commandMenuEvents.md)
344. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
345. [SortableTaskItem](modules/SortableTaskItem.md)
346. [useDraftDismissal](modules/useDraftDismissal.md)
347. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
348. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
349. [InlineEmptyState](modules/InlineEmptyState.md)
350. [MasterProgress](modules/MasterProgress.md)
351. [MasterProgress.test](modules/MasterProgress.test.md)
352. [OverflowMenu](modules/OverflowMenu.md)
353. [PageLayout](modules/PageLayout.md)
354. [SectionCard](modules/SectionCard.md)
355. [SlideOverDrawer](modules/SlideOverDrawer.md)
356. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
357. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
358. [StickyRail](modules/StickyRail.md)
359. [index](modules/index.md)
360. [overviewTaskThread](modules/overviewTaskThread.md)
361. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
362. [planningReturn](modules/planningReturn.md)
363. [PlanReturnBar](modules/PlanReturnBar.md)
364. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
365. [workQueryFreshness](modules/workQueryFreshness.md)
366. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
367. [pagination](modules/pagination.md)
368. [teamwork.en](modules/teamwork.en.md)
369. [teamwork.ru](modules/teamwork.ru.md)
370. [timeEntries](modules/timeEntries.md)
371. [resources.en](modules/resources.en.md)
372. [i18n](modules/i18n.md)
373. [dateLocale](modules/dateLocale.md)
374. [InteractiveCalendar](modules/InteractiveCalendar.md)
375. [resources.ru](modules/resources.ru.md)
376. [i18n.test](modules/i18n.test.md)
377. [routeModules](modules/routeModules.md)
378. [DocumentMetadata](modules/DocumentMetadata.md)
379. [workspaces](modules/workspaces.md)
380. [helpContexts](modules/helpContexts.md)
381. [workspaces.test](modules/workspaces.test.md)
382. [LandingPage](modules/LandingPage.md)
383. [NotFoundPage](modules/NotFoundPage.md)
384. [healthService](modules/healthService.md)
385. [SystemHealthPanel](modules/SystemHealthPanel.md)
386. [iterationStore](modules/iterationStore.md)
387. [themeStore](modules/themeStore.md)
388. [planning-masters.test](modules/planning-masters.test.md)
389. [accessibilityInvariants](modules/accessibilityInvariants.md)
390. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
391. [renderWithProviders](modules/renderWithProviders.md)
392. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
393. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
394. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
395. [OverflowMenu.test](modules/OverflowMenu.test.md)
396. [renderWithProviders.test](modules/renderWithProviders.test.md)
397. [setup](modules/setup.md)
398. [types_calendar](modules/types_calendar.md)
399. [deliveryMetrics](modules/deliveryMetrics.md)
400. [executionUsage](modules/executionUsage.md)
401. [types_label](modules/types_label.md)
402. [outboundWebhook](modules/outboundWebhook.md)
403. [requestSource](modules/requestSource.md)
404. [savedView](modules/savedView.md)
405. [schedulingRules](modules/schedulingRules.md)
406. [ConstraintsPanel](modules/ConstraintsPanel.md)
407. [schedulingDisplay](modules/schedulingDisplay.md)
408. [EffortModifierCard](modules/EffortModifierCard.md)
409. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
410. [SchedulingPassCard](modules/SchedulingPassCard.md)
411. [systemSettings](modules/systemSettings.md)
412. [emailSettings](modules/emailSettings.md)
413. [types_team](modules/types_team.md)
414. [types_task](modules/types_task.md)
415. [types_triage](modules/types_triage.md)
416. [KanbanCard](modules/KanbanCard.md)
417. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
418. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
419. [tone](modules/tone.md)
420. [KanbanColumn](modules/KanbanColumn.md)
421. [Pill](modules/Pill.md)
422. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
423. [tone.test](modules/tone.test.md)
424. [attentionRanking](modules/attentionRanking.md)
425. [attentionRanking.test](modules/attentionRanking.test.md)
426. [planningTaskIssues](modules/planningTaskIssues.md)
427. [planningMasters_masters](modules/planningMasters_masters.md)
428. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
429. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
430. [types_agent](modules/types_agent.md)
431. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
432. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
433. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
434. [statusScopes](modules/statusScopes.md)
435. [statusScopes.test](modules/statusScopes.test.md)
436. [modelAwareRouting](modules/modelAwareRouting.md)
437. [types_github](modules/types_github.md)
438. [types_template](modules/types_template.md)
439. [seedDisplay](modules/seedDisplay.md)
440. [workMetrics](modules/workMetrics.md)
441. [WorkMetricsLine](modules/WorkMetricsLine.md)
442. [types_iteration](modules/types_iteration.md)
443. [types_gantt](modules/types_gantt.md)
444. [types_project](modules/types_project.md)
445. [projectStatusStyles](modules/projectStatusStyles.md)
446. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
447. [types_release](modules/types_release.md)
448. [agentAccess](modules/agentAccess.md)
449. [useAgentAccess](modules/useAgentAccess.md)
450. [apiError](modules/apiError.md)
451. [QueryState](modules/QueryState.md)
452. [taskEditorContract](modules/taskEditorContract.md)
453. [TaskBriefEditor](modules/TaskBriefEditor.md)
454. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
455. [taskDraftStorage](modules/taskDraftStorage.md)
456. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
457. [adminAccess](modules/adminAccess.md)
458. [api](modules/api.md)
459. [identityService](modules/identityService.md)
460. [identityContext](modules/identityContext.md)
461. [useAdminAccess](modules/useAdminAccess.md)
462. [AdminAccessPanel](modules/AdminAccessPanel.md)
463. [AdminAccessGate](modules/AdminAccessGate.md)
464. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
465. [NativeConnectionPage](modules/NativeConnectionPage.md)
466. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
467. [agentService](modules/agentService.md)
468. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
469. [AgentTeamStepList](modules/AgentTeamStepList.md)
470. [agentService.test](modules/agentService.test.md)
471. [calendarService](modules/calendarService.md)
472. [PersonCapacity](modules/PersonCapacity.md)
473. [deliveryMetricsService](modules/deliveryMetricsService.md)
474. [discussionService](modules/discussionService.md)
475. [TaskDiscussion](modules/TaskDiscussion.md)
476. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
477. [emailSettingsService](modules/emailSettingsService.md)
478. [executionUsageService](modules/executionUsageService.md)
479. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
480. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
481. [exportService](modules/exportService.md)
482. [ganttService](modules/ganttService.md)
483. [githubService](modules/githubService.md)
484. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
485. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
486. [iterationService](modules/iterationService.md)
487. [IterationSelector](modules/IterationSelector.md)
488. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
489. [SidebarIterationCard](modules/SidebarIterationCard.md)
490. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
491. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
492. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
493. [labelService](modules/labelService.md)
494. [LabelSelector](modules/LabelSelector.md)
495. [outboundWebhookService](modules/outboundWebhookService.md)
496. [planShareService](modules/planShareService.md)
497. [projectService](modules/projectService.md)
498. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
499. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
500. [releaseService](modules/releaseService.md)
501. [ReleaseForm](modules/ReleaseForm.md)
502. [requestSourceService](modules/requestSourceService.md)
503. [savedViewService](modules/savedViewService.md)
504. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
505. [AppSidebar](modules/AppSidebar.md)
506. [AppSidebar.test](modules/AppSidebar.test.md)
507. [schedulingRulesService](modules/schedulingRulesService.md)
508. [sessionService](modules/sessionService.md)
509. [snapshotService](modules/snapshotService.md)
510. [systemSettingsService](modules/systemSettingsService.md)
511. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
512. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
513. [taskService](modules/taskService.md)
514. [DeliveryDependencies](modules/DeliveryDependencies.md)
515. [ImportTasksModal](modules/ImportTasksModal.md)
516. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
517. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
518. [TaskContextSummary](modules/TaskContextSummary.md)
519. [TaskDependencySelector](modules/TaskDependencySelector.md)
520. [TaskSearch](modules/TaskSearch.md)
521. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
522. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
523. [TaskWorkPanel](modules/TaskWorkPanel.md)
524. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
525. [teamService](modules/teamService.md)
526. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
527. [TaskFiltersBar](modules/TaskFiltersBar.md)
528. [taskFilterDefaults](modules/taskFilterDefaults.md)
529. [ImportTeamModal](modules/ImportTeamModal.md)
530. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
531. [TeamForm](modules/TeamForm.md)
532. [TeamForm.test](modules/TeamForm.test.md)
533. [TeamProfileManager](modules/TeamProfileManager.md)
534. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
535. [IdentityProvider](modules/IdentityProvider.md)
536. [UserSessionBadge](modules/UserSessionBadge.md)
537. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
538. [IdentityProvider.test](modules/IdentityProvider.test.md)
539. [CalendarPage](modules/CalendarPage.md)
540. [templateService](modules/templateService.md)
541. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
542. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
543. [timeEntryService](modules/timeEntryService.md)
544. [useTimeEntries](modules/useTimeEntries.md)
545. [timeEntryService.test](modules/timeEntryService.test.md)
546. [triageService](modules/triageService.md)
547. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
548. [usePlanningReadiness](modules/usePlanningReadiness.md)
549. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
550. [copyText](modules/copyText.md)
551. [focusLifecycle](modules/focusLifecycle.md)
552. [focusLifecycle.test](modules/focusLifecycle.test.md)
553. [formatDate](modules/formatDate.md)
554. [TaskStatusFlow](modules/TaskStatusFlow.md)
555. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
556. [IterationForm](modules/IterationForm.md)
557. [IterationForm.test](modules/IterationForm.test.md)
558. [IterationList](modules/IterationList.md)
559. [NotificationsPanel](modules/NotificationsPanel.md)
560. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
561. [StatusChangeControl](modules/StatusChangeControl.md)
562. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
563. [TimeEntriesReport](modules/TimeEntriesReport.md)
564. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
565. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
566. [VacationManager](modules/VacationManager.md)
567. [TeamList](modules/TeamList.md)
568. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
569. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
570. [AnalyticsPage](modules/AnalyticsPage.md)
571. [IterationsPage](modules/IterationsPage.md)
572. [PlanMasterPage](modules/PlanMasterPage.md)
573. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
574. [PlanPage](modules/PlanPage.md)
575. [PlanPage.test](modules/PlanPage.test.md)
576. [PlanSharePage](modules/PlanSharePage.md)
577. [PlanSharePage.test](modules/PlanSharePage.test.md)
578. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
579. [TeamPage](modules/TeamPage.md)
580. [graphLimitError](modules/graphLimitError.md)
581. [modelRouting](modules/modelRouting.md)
582. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
583. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
584. [modelRouting.test](modules/modelRouting.test.md)
585. [protectedQueries](modules/protectedQueries.md)
586. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
587. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
588. [AgentAccessPanel](modules/AgentAccessPanel.md)
589. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
590. [AgentModelAdministration](modules/AgentModelAdministration.md)
591. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
592. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
593. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
594. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
595. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
596. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
597. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
598. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
599. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
600. [AgentPipelinePage](modules/AgentPipelinePage.md)
601. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
602. [safeUrl](modules/safeUrl.md)
603. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
604. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
605. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
606. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
607. [savedViewState](modules/savedViewState.md)
608. [savedViewState.test](modules/savedViewState.test.md)
609. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
610. [OverviewPage](modules/OverviewPage.md)
611. [OverviewPage.test](modules/OverviewPage.test.md)
612. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
613. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
614. [CommandMenu](modules/CommandMenu.md)
615. [CommandMenu.test](modules/CommandMenu.test.md)
616. [ContextHelp](modules/ContextHelp.md)
617. [AppTopNav](modules/AppTopNav.md)
618. [AppShell](modules/AppShell.md)
619. [App](modules/App.md)
620. [AppShell.test](modules/AppShell.test.md)
621. [AppTopNav.test](modules/AppTopNav.test.md)
622. [ContextHelp.test](modules/ContextHelp.test.md)
623. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
624. [src_main](modules/src_main.md)
625. [SettingsPage](modules/SettingsPage.md)
626. [SettingsPage.test](modules/SettingsPage.test.md)
627. [taskFilters](modules/taskFilters.md)
628. [taskFilters.test](modules/taskFilters.test.md)
629. [teamMemberLabels](modules/teamMemberLabels.md)
630. [InitiativeForm](modules/InitiativeForm.md)
631. [RoadmapPage](modules/RoadmapPage.md)
632. [RoadmapPage.test](modules/RoadmapPage.test.md)
633. [templateDefaults](modules/templateDefaults.md)
634. [ProjectForm](modules/ProjectForm.md)
635. [TaskForm](modules/TaskForm.md)
636. [TaskEditModal](modules/TaskEditModal.md)
637. [GanttChart](modules/GanttChart.md)
638. [GanttChart.test](modules/GanttChart.test.md)
639. [GuardedTaskModal](modules/GuardedTaskModal.md)
640. [BacklogPanel](modules/BacklogPanel.md)
641. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
642. [ProjectTaskTree](modules/ProjectTaskTree.md)
643. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
644. [TaskForm.test](modules/TaskForm.test.md)
645. [GanttPage](modules/GanttPage.md)
646. [GanttPage.test](modules/GanttPage.test.md)
647. [MyWorkPage](modules/MyWorkPage.md)
648. [MyWorkPage.test](modules/MyWorkPage.test.md)
649. [ProjectDetailPage](modules/ProjectDetailPage.md)
650. [ProjectsPage](modules/ProjectsPage.md)
651. [ProjectsPage.test](modules/ProjectsPage.test.md)
652. [TriagePage](modules/TriagePage.md)
653. [visibleWork](modules/visibleWork.md)
654. [KanbanBoard](modules/KanbanBoard.md)
655. [KanbanBoard.test](modules/KanbanBoard.test.md)
656. [TaskList](modules/TaskList.md)
657. [SavedViewsControl](modules/SavedViewsControl.md)
658. [TaskList.test](modules/TaskList.test.md)
659. [taskViewState](modules/taskViewState.md)
660. [TasksPage](modules/TasksPage.md)
661. [TasksPage.test](modules/TasksPage.test.md)
662. [visibleWork.test](modules/visibleWork.test.md)
663. [tailwind.config](modules/tailwind.config.md)
664. [vite.config](modules/vite.config.md)
665. [vitest.config](modules/vitest.config.md)
666. [create_agent_actor](modules/create_agent_actor.md)
667. [generate_workchord_keys](modules/generate_workchord_keys.md)
668. [setup_agent_team](modules/setup_agent_team.md)
669. [build_agent_skills](modules/build_agent_skills.md)
670. [apt_runtime](modules/apt_runtime.md)
671. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
672. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
673. [ci_runtime](modules/ci_runtime.md)
674. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
675. [postgres_runtime](modules/postgres_runtime.md)
676. [run_android_checks](modules/run_android_checks.md)
677. [run_disposable_checks](modules/run_disposable_checks.md)
678. [serve_disposable_api](modules/serve_disposable_api.md)
679. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
680. [test_apt_runtime](modules/test_apt_runtime.md)
681. [test_ci_runtime](modules/test_ci_runtime.md)
682. [test_native_runtimes](modules/test_native_runtimes.md)
683. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
684. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
685. [generate_client_contract](modules/generate_client_contract.md)
686. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
687. [load_common](modules/load_common.md)
688. [collect](modules/collect.md)
689. [result](modules/result.md)
690. [compare](modules/compare.md)
691. [finalize](modules/finalize.md)
692. [qualify](modules/qualify.md)
693. [resilience](modules/resilience.md)
694. [run](modules/run.md)
695. [local_baseline](modules/local_baseline.md)
696. [seal](modules/seal.md)
697. [seed](modules/seed.md)
698. [service_worksets](modules/service_worksets.md)

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
| [workQueryFreshness.test](modules/workQueryFreshness.test.md) | `cases = flatMap`, `it.each(cases)` |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | `describe` |
| [i18n.test](modules/i18n.test.md) | `describe` |
| [src_main](modules/src_main.md) | `queryClient = QueryClient`, `installPlanningNavigationInvalidation`, `installWorkFreshness`, `router = createBrowserRouter`, `render` |
| [workspaces.test](modules/workspaces.test.md) | `describe` |
| [workspaces](modules/workspaces.md) | `PRIMARY_NAV_ITEMS = flatMap` |
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set`, `TASK_STATUSES = Set` |
| [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe` |
| [GanttPage.test](modules/GanttPage.test.md) | `ganttServiceMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [MyWorkPage.test](modules/MyWorkPage.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `it` |
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
