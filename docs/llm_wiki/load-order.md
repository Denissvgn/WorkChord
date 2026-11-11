# Load order

Topological module load / startup order and import-time side effects.

## Load order

<!-- Dependency-first order: each module loads after the internal modules it imports. -->

TypeScript binding imports are possible startup constraints: their emission depends on compiler settings. Guaranteed-erased type imports are excluded. This is a static projection, not an emitted-JavaScript execution trace.

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
27. [allocation_identity](modules/allocation_identity.md)
28. [database_migration_manifest](modules/database_migration_manifest.md)
29. [database_migration_cutover](modules/database_migration_cutover.md)
30. [cli_cutover](modules/cli_cutover.md)
31. [database_migration_closeout](modules/database_migration_closeout.md)
32. [cli_closeout](modules/cli_closeout.md)
33. [project_identity](modules/project_identity.md)
34. [20260928_0001_initial_schema](modules/20260928_0001_initial_schema.md)
35. [20260930_0002_profile_capacity](modules/20260930_0002_profile_capacity.md)
36. [20260930_0003_delivery_dependencies](modules/20260930_0003_delivery_dependencies.md)
37. [20260930_0004_discussion](modules/20260930_0004_discussion.md)
38. [20261003_0005_native_connections](modules/20261003_0005_native_connections.md)
39. [20261004_0006_delivery_observations](modules/20261004_0006_delivery_observations.md)
40. [20261004_0007_execution_usage](modules/20261004_0007_execution_usage.md)
41. [20261007_0008_time_entries](modules/20261007_0008_time_entries.md)
42. [20261008_0009_project_identity](modules/20261008_0009_project_identity.md)
43. [20261009_0010_allocation_identity](modules/20261009_0010_allocation_identity.md)
44. [20261009_0011_profile_identity](modules/20261009_0011_profile_identity.md)
45. [20261111_0012_session_work_profile](modules/20261111_0012_session_work_profile.md)
46. [query_limits](modules/query_limits.md)
47. [runtime_telemetry](modules/runtime_telemetry.md)
48. [database_runtime](modules/database_runtime.md)
49. [maintenance](modules/maintenance.md)
50. [mutation_versions](modules/mutation_versions.md)
51. [schemas_agent_planning](modules/schemas_agent_planning.md)
52. [agent_skill_bundle](modules/agent_skill_bundle.md)
53. [agent_team_setup](modules/agent_team_setup.md)
54. [schemas_autonomy](modules/schemas_autonomy.md)
55. [schemas_common](modules/schemas_common.md)
56. [delivery_metrics](modules/delivery_metrics.md)
57. [schemas_execution_usage](modules/schemas_execution_usage.md)
58. [schemas_github](modules/schemas_github.md)
59. [schemas_intake](modules/schemas_intake.md)
60. [schemas_label](modules/schemas_label.md)
61. [schemas_plan_share](modules/schemas_plan_share.md)
62. [planning_inputs](modules/planning_inputs.md)
63. [schemas_calendar](modules/schemas_calendar.md)
64. [schemas_saved_view](modules/schemas_saved_view.md)
65. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
66. [schemas_session](modules/schemas_session.md)
67. [snapshot](modules/snapshot.md)
68. [schemas_system_settings](modules/schemas_system_settings.md)
69. [schemas_email_settings](modules/schemas_email_settings.md)
70. [schemas_task_brief](modules/schemas_task_brief.md)
71. [schemas_llm](modules/schemas_llm.md)
72. [schemas_task_domain](modules/schemas_task_domain.md)
73. [schemas_team](modules/schemas_team.md)
74. [schemas_template](modules/schemas_template.md)
75. [schemas_time_entry](modules/schemas_time_entry.md)
76. [time_report](modules/time_report.md)
77. [schemas_work_metrics](modules/schemas_work_metrics.md)
78. [schemas_iteration](modules/schemas_iteration.md)
79. [schemas_project](modules/schemas_project.md)
80. [schemas_release](modules/schemas_release.md)
81. [security](modules/security.md)
82. [agent_routing_policy](modules/agent_routing_policy.md)
83. [agent_routing](modules/agent_routing.md)
84. [agent_routing_rollout](modules/agent_routing_rollout.md)
85. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
86. [agent_team_credentials](modules/agent_team_credentials.md)
87. [bounded_scope_reads](modules/bounded_scope_reads.md)
88. [language_service](modules/language_service.md)
89. [plan_checkpoints](modules/plan_checkpoints.md)
90. [planning_input_context](modules/planning_input_context.md)
91. [planning_issues](modules/planning_issues.md)
92. [scheduling_rules_service](modules/scheduling_rules_service.md)
93. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
94. [upgrade_service](modules/upgrade_service.md)
95. [upgrade](modules/upgrade.md)
96. [sql_semantics](modules/sql_semantics.md)
97. [exceptions](modules/exceptions.md)
98. [text_similarity](modules/text_similarity.md)
99. [time](modules/time.md)
100. [observability](modules/observability.md)
101. [app_database](modules/app_database.md)
102. [models_agent](modules/models_agent.md)
103. [models_autonomy](modules/models_autonomy.md)
104. [models_calendar](modules/models_calendar.md)
105. [models_capacity](modules/models_capacity.md)
106. [models_database_migration](modules/models_database_migration.md)
107. [delivery_dependency](modules/delivery_dependency.md)
108. [models_discussion](modules/models_discussion.md)
109. [models_execution_usage](modules/models_execution_usage.md)
110. [models_external_link](modules/models_external_link.md)
111. [models_github](modules/models_github.md)
112. [models_identity](modules/models_identity.md)
113. [models_iteration](modules/models_iteration.md)
114. [models_label](modules/models_label.md)
115. [native_connection](modules/native_connection.md)
116. [models_outbound_webhook](modules/models_outbound_webhook.md)
117. [models_plan_share](modules/models_plan_share.md)
118. [models_release](modules/models_release.md)
119. [models_project](modules/models_project.md)
120. [models_request_source](modules/models_request_source.md)
121. [models_saved_view](modules/models_saved_view.md)
122. [models_system_settings](modules/models_system_settings.md)
123. [models_task](modules/models_task.md)
124. [recovery](modules/recovery.md)
125. [models_task_brief](modules/models_task_brief.md)
126. [delivery_observation](modules/delivery_observation.md)
127. [task_status_log](modules/task_status_log.md)
128. [team_member](modules/team_member.md)
129. [models_template](modules/models_template.md)
130. [models_time_entry](modules/models_time_entry.md)
131. [models_triage](modules/models_triage.md)
132. [user_session](modules/user_session.md)
133. [models___init__](modules/models___init__.md)
134. [catalog](modules/catalog.md)
135. [database_migration_canonical](modules/database_migration_canonical.md)
136. [source](modules/source.md)
137. [transfer](modules/transfer.md)
138. [cli_database_migration](modules/cli_database_migration.md)
139. [database_migration___init__](modules/database_migration___init__.md)
140. [migrations_env](modules/migrations_env.md)
141. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
142. [calendar_service](modules/calendar_service.md)
143. [calendars](modules/calendars.md)
144. [capacity_service](modules/capacity_service.md)
145. [routers_capacity](modules/routers_capacity.md)
146. [delivery_dependency_service](modules/delivery_dependency_service.md)
147. [delivery_metrics_service](modules/delivery_metrics_service.md)
148. [discussion_service](modules/discussion_service.md)
149. [identity_service](modules/identity_service.md)
150. [import_planning_service](modules/import_planning_service.md)
151. [iteration_service](modules/iteration_service.md)
152. [iterations](modules/iterations.md)
153. [label_service](modules/label_service.md)
154. [labels](modules/labels.md)
155. [native_session_service](modules/native_session_service.md)
156. [saved_view_service](modules/saved_view_service.md)
157. [session_service](modules/session_service.md)
158. [http_authority](modules/http_authority.md)
159. [routers_identity](modules/routers_identity.md)
160. [saved_views](modules/saved_views.md)
161. [routers_session](modules/routers_session.md)
162. [task_brief_service](modules/task_brief_service.md)
163. [task_context_revision_service](modules/task_context_revision_service.md)
164. [task_domain_service](modules/task_domain_service.md)
165. [task_hierarchy_service](modules/task_hierarchy_service.md)
166. [task_recovery_service](modules/task_recovery_service.md)
167. [task_timeline_service](modules/task_timeline_service.md)
168. [team_service](modules/team_service.md)
169. [routers_team](modules/routers_team.md)
170. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
171. [snapshot_service](modules/snapshot_service.md)
172. [plan_share_service](modules/plan_share_service.md)
173. [plan_shares](modules/plan_shares.md)
174. [template_service](modules/template_service.md)
175. [templates](modules/templates.md)
176. [time_entry_service](modules/time_entry_service.md)
177. [time_report_service](modules/time_report_service.md)
178. [services_work_metrics](modules/services_work_metrics.md)
179. [import_parser](modules/import_parser.md)
180. [url_policy](modules/url_policy.md)
181. [schemas_external_link](modules/schemas_external_link.md)
182. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
183. [schemas_request_source](modules/schemas_request_source.md)
184. [schemas_task](modules/schemas_task.md)
185. [schemas_gantt](modules/schemas_gantt.md)
186. [task_detail](modules/task_detail.md)
187. [schemas_triage](modules/schemas_triage.md)
188. [schemas___init__](modules/schemas___init__.md)
189. [schemas_agent](modules/schemas_agent.md)
190. [agent_readiness](modules/agent_readiness.md)
191. [llm_service](modules/llm_service.md)
192. [system_settings_service](modules/system_settings_service.md)
193. [routers_system_settings](modules/routers_system_settings.md)
194. [email_settings_service](modules/email_settings_service.md)
195. [routers_email_settings](modules/routers_email_settings.md)
196. [notification_service](modules/notification_service.md)
197. [outbound_webhook_service](modules/outbound_webhook_service.md)
198. [worker](modules/worker.md)
199. [outbound_webhooks](modules/outbound_webhooks.md)
200. [external_link_service](modules/external_link_service.md)
201. [github_status_service](modules/github_status_service.md)
202. [request_source_service](modules/request_source_service.md)
203. [request_sources](modules/request_sources.md)
204. [project_service](modules/project_service.md)
205. [task_detail_service](modules/task_detail_service.md)
206. [task_import_service](modules/task_import_service.md)
207. [task_service](modules/task_service.md)
208. [export](modules/export.md)
209. [snapshots](modules/snapshots.md)
210. [agent_routing_observability](modules/agent_routing_observability.md)
211. [agent_service](modules/agent_service.md)
212. [agent_skill_bundles](modules/agent_skill_bundles.md)
213. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
214. [agent_routing_service](modules/agent_routing_service.md)
215. [agent_team_setup_service](modules/agent_team_setup_service.md)
216. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
217. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
218. [execution_usage_service](modules/execution_usage_service.md)
219. [routers_task_domain](modules/routers_task_domain.md)
220. [delivery_dependencies](modules/delivery_dependencies.md)
221. [routers_discussion](modules/routers_discussion.md)
222. [time_entries](modules/time_entries.md)
223. [github_status_automation_service](modules/github_status_automation_service.md)
224. [release_service](modules/release_service.md)
225. [projects](modules/projects.md)
226. [scheduler_service](modules/scheduler_service.md)
227. [routers_gantt](modules/routers_gantt.md)
228. [routers_llm](modules/routers_llm.md)
229. [agent_planning_service](modules/agent_planning_service.md)
230. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
231. [tasks](modules/tasks.md)
232. [task_status_service](modules/task_status_service.md)
233. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
234. [triage_service](modules/triage_service.md)
235. [routers_triage](modules/routers_triage.md)
236. [agent_work_service](modules/agent_work_service.md)
237. [mcp_agent_tools](modules/mcp_agent_tools.md)
238. [mcp_server](modules/mcp_server.md)
239. [routers_agent](modules/routers_agent.md)
240. [routers_agent_planning](modules/routers_agent_planning.md)
241. [agent_catalog](modules/agent_catalog.md)
242. [github_webhook_service](modules/github_webhook_service.md)
243. [routers_github](modules/routers_github.md)
244. [web_intake_service](modules/web_intake_service.md)
245. [routers_intake](modules/routers_intake.md)
246. [app_main](modules/app_main.md)
247. [routers___init__](modules/routers___init__.md)
248. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
249. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
250. [test_server_acceptance](modules/test_server_acceptance.md)
251. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
252. [test_work_package_service](modules/test_work_package_service.md)
253. [test_database_configuration](modules/test_database_configuration.md)
254. [test_deployment_topology](modules/test_deployment_topology.md)
255. [test_observability](modules/test_observability.md)
256. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
257. [test_query_boundaries](modules/test_query_boundaries.md)
258. [test_runtime_policy](modules/test_runtime_policy.md)
259. [test_schema_behavior](modules/test_schema_behavior.md)
260. [test_cutover_evidence](modules/test_cutover_evidence.md)
261. [test_documentation_boundary](modules/test_documentation_boundary.md)
262. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
263. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
264. [test_source_preflight](modules/test_source_preflight.md)
265. [test_transfer_catalog](modules/test_transfer_catalog.md)
266. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
267. [0001_wave0_probe](modules/0001_wave0_probe.md)
268. [test_allocation_identity](modules/test_allocation_identity.md)
269. [test_initial_schema](modules/test_initial_schema.md)
270. [test_profile_identity](modules/test_profile_identity.md)
271. [test_android_cleanup](modules/test_android_cleanup.md)
272. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
273. [test_load_tooling](modules/test_load_tooling.md)
274. [test_local_baseline](modules/test_local_baseline.md)
275. [test_routing_evidence](modules/test_routing_evidence.md)
276. [support_database](modules/support_database.md)
277. [delivery](modules/delivery.md)
278. [factories](modules/factories.md)
279. [faults](modules/faults.md)
280. [runtime_peer](modules/runtime_peer.md)
281. [schema](modules/schema.md)
282. [support___init__](modules/support___init__.md)
283. [conftest](modules/conftest.md)
284. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
285. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
286. [test_project_identity](modules/test_project_identity.md)
287. [test_project_identity_scope](modules/test_project_identity_scope.md)
288. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
289. [transactions](modules/transactions.md)
290. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
291. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
292. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
293. [test_agent_routing_data](modules/test_agent_routing_data.md)
294. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
295. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
296. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
297. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
298. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
299. [test_agent_routing_service](modules/test_agent_routing_service.md)
300. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
301. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
302. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
303. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
304. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
305. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
306. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
307. [test_authority_migrations](modules/test_authority_migrations.md)
308. [test_capacity_contract](modules/test_capacity_contract.md)
309. [test_client_contract](modules/test_client_contract.md)
310. [test_database_harness](modules/test_database_harness.md)
311. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
312. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
313. [test_agent_team_setup](modules/test_agent_team_setup.md)
314. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
315. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
316. [test_deployment_configuration](modules/test_deployment_configuration.md)
317. [test_effective_deferral](modules/test_effective_deferral.md)
318. [test_execution_usage](modules/test_execution_usage.md)
319. [test_execution_working_dates](modules/test_execution_working_dates.md)
320. [test_managed_authority](modules/test_managed_authority.md)
321. [test_allocation_recovery](modules/test_allocation_recovery.md)
322. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
323. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
324. [test_mobile_contract](modules/test_mobile_contract.md)
325. [test_mutation_versions](modules/test_mutation_versions.md)
326. [test_native_connections](modules/test_native_connections.md)
327. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
328. [test_plan_shares](modules/test_plan_shares.md)
329. [test_planning_input_context](modules/test_planning_input_context.md)
330. [test_planning_issues](modules/test_planning_issues.md)
331. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
332. [test_process_roles](modules/test_process_roles.md)
333. [test_profile_capacity](modules/test_profile_capacity.md)
334. [test_planning_read_models](modules/test_planning_read_models.md)
335. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
336. [test_project_working_timezone](modules/test_project_working_timezone.md)
337. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
338. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
339. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
340. [test_saved_view_service](modules/test_saved_view_service.md)
341. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
342. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
343. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
344. [test_task_domain](modules/test_task_domain.md)
345. [test_delivery_metrics](modules/test_delivery_metrics.md)
346. [test_human_work_queries](modules/test_human_work_queries.md)
347. [test_task_discussion](modules/test_task_discussion.md)
348. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
349. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
350. [test_task_pagination](modules/test_task_pagination.md)
351. [test_time_entries](modules/test_time_entries.md)
352. [test_time_reports](modules/test_time_reports.md)
353. [test_work_correctness](modules/test_work_correctness.md)
354. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
355. [eslint.config](modules/eslint.config.md)
356. [postcss.config](modules/postcss.config.md)
357. [check-bundle-budget](modules/check-bundle-budget.md)
358. [check-query-feedback](modules/check-query-feedback.md)
359. [Button](modules/Button.md)
360. [Button.test](modules/Button.test.md)
361. [Checkbox](modules/Checkbox.md)
362. [CollapsibleSection](modules/CollapsibleSection.md)
363. [Input](modules/Input.md)
364. [Input.test](modules/Input.test.md)
365. [dialogLayer](modules/dialogLayer.md)
366. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
367. [Modal](modules/Modal.md)
368. [ConfirmDialog](modules/ConfirmDialog.md)
369. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
370. [useConfirmDialog](modules/useConfirmDialog.md)
371. [LiveWindowStatus](modules/LiveWindowStatus.md)
372. [WorkFreshness](modules/WorkFreshness.md)
373. [toast](modules/toast.md)
374. [ToastProvider](modules/ToastProvider.md)
375. [ToastProvider.test](modules/ToastProvider.test.md)
376. [Breadcrumbs](modules/Breadcrumbs.md)
377. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
378. [commandMenuEvents](modules/commandMenuEvents.md)
379. [ConstraintsPanel](modules/ConstraintsPanel.md)
380. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
381. [SortableTaskItem](modules/SortableTaskItem.md)
382. [WorkMetricsLine](modules/WorkMetricsLine.md)
383. [taskDraftStorage](modules/taskDraftStorage.md)
384. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
385. [useDraftDismissal](modules/useDraftDismissal.md)
386. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
387. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
388. [InlineEmptyState](modules/InlineEmptyState.md)
389. [MasterProgress](modules/MasterProgress.md)
390. [MasterProgress.test](modules/MasterProgress.test.md)
391. [OverflowMenu](modules/OverflowMenu.md)
392. [PageLayout](modules/PageLayout.md)
393. [SectionCard](modules/SectionCard.md)
394. [SlideOverDrawer](modules/SlideOverDrawer.md)
395. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
396. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
397. [StickyRail](modules/StickyRail.md)
398. [index](modules/index.md)
399. [tone](modules/tone.md)
400. [projectStatusStyles](modules/projectStatusStyles.md)
401. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
402. [Pill](modules/Pill.md)
403. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
404. [tone.test](modules/tone.test.md)
405. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
406. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
407. [AgentTeamStepList](modules/AgentTeamStepList.md)
408. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
409. [statusScopes](modules/statusScopes.md)
410. [statusScopes.test](modules/statusScopes.test.md)
411. [identityContext](modules/identityContext.md)
412. [attentionRanking](modules/attentionRanking.md)
413. [attentionRanking.test](modules/attentionRanking.test.md)
414. [overviewTaskThread](modules/overviewTaskThread.md)
415. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
416. [planningReturn](modules/planningReturn.md)
417. [PlanReturnBar](modules/PlanReturnBar.md)
418. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
419. [planningTaskIssues](modules/planningTaskIssues.md)
420. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
421. [useLiveWindow](modules/useLiveWindow.md)
422. [workQueryFreshness](modules/workQueryFreshness.md)
423. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
424. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
425. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
426. [pagination](modules/pagination.md)
427. [plan.ru](modules/plan.ru.md)
428. [planningInputMessages](modules/planningInputMessages.md)
429. [teamwork.en](modules/teamwork.en.md)
430. [teamwork.ru](modules/teamwork.ru.md)
431. [timeEntries](modules/timeEntries.md)
432. [resources.en](modules/resources.en.md)
433. [i18n](modules/i18n.md)
434. [KanbanCard](modules/KanbanCard.md)
435. [KanbanColumn](modules/KanbanColumn.md)
436. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
437. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
438. [dateLocale](modules/dateLocale.md)
439. [InteractiveCalendar](modules/InteractiveCalendar.md)
440. [resources.ru](modules/resources.ru.md)
441. [i18n.test](modules/i18n.test.md)
442. [schedulingDisplay](modules/schedulingDisplay.md)
443. [seedDisplay](modules/seedDisplay.md)
444. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
445. [routeModules](modules/routeModules.md)
446. [DocumentMetadata](modules/DocumentMetadata.md)
447. [workspaces](modules/workspaces.md)
448. [helpContexts](modules/helpContexts.md)
449. [workspaces.test](modules/workspaces.test.md)
450. [LandingPage](modules/LandingPage.md)
451. [NotFoundPage](modules/NotFoundPage.md)
452. [healthService](modules/healthService.md)
453. [SystemHealthPanel](modules/SystemHealthPanel.md)
454. [iterationStore](modules/iterationStore.md)
455. [iterationStore.test](modules/iterationStore.test.md)
456. [themeStore](modules/themeStore.md)
457. [planning-masters.test](modules/planning-masters.test.md)
458. [accessibilityInvariants](modules/accessibilityInvariants.md)
459. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
460. [modelAwareRouting](modules/modelAwareRouting.md)
461. [renderWithProviders](modules/renderWithProviders.md)
462. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
463. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
464. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
465. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
466. [OverflowMenu.test](modules/OverflowMenu.test.md)
467. [renderWithProviders.test](modules/renderWithProviders.test.md)
468. [setup](modules/setup.md)
469. [types_agent](modules/types_agent.md)
470. [types_calendar](modules/types_calendar.md)
471. [deliveryMetrics](modules/deliveryMetrics.md)
472. [emailSettings](modules/emailSettings.md)
473. [executionUsage](modules/executionUsage.md)
474. [types_gantt](modules/types_gantt.md)
475. [types_github](modules/types_github.md)
476. [types_iteration](modules/types_iteration.md)
477. [types_label](modules/types_label.md)
478. [outboundWebhook](modules/outboundWebhook.md)
479. [types_project](modules/types_project.md)
480. [types_release](modules/types_release.md)
481. [requestSource](modules/requestSource.md)
482. [savedView](modules/savedView.md)
483. [schedulingRules](modules/schedulingRules.md)
484. [EffortModifierCard](modules/EffortModifierCard.md)
485. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
486. [SchedulingPassCard](modules/SchedulingPassCard.md)
487. [systemSettings](modules/systemSettings.md)
488. [types_task](modules/types_task.md)
489. [types_team](modules/types_team.md)
490. [types_template](modules/types_template.md)
491. [types_triage](modules/types_triage.md)
492. [workMetrics](modules/workMetrics.md)
493. [agentAccess](modules/agentAccess.md)
494. [useAgentAccess](modules/useAgentAccess.md)
495. [apiError](modules/apiError.md)
496. [QueryState](modules/QueryState.md)
497. [taskEditorContract](modules/taskEditorContract.md)
498. [TaskBriefEditor](modules/TaskBriefEditor.md)
499. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
500. [adminAccess](modules/adminAccess.md)
501. [useAdminAccess](modules/useAdminAccess.md)
502. [api](modules/api.md)
503. [identityService](modules/identityService.md)
504. [NativeConnectionPage](modules/NativeConnectionPage.md)
505. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
506. [agentService](modules/agentService.md)
507. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
508. [agentService.test](modules/agentService.test.md)
509. [deliveryMetricsService](modules/deliveryMetricsService.md)
510. [discussionService](modules/discussionService.md)
511. [TaskDiscussion](modules/TaskDiscussion.md)
512. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
513. [emailSettingsService](modules/emailSettingsService.md)
514. [executionUsageService](modules/executionUsageService.md)
515. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
516. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
517. [ganttService](modules/ganttService.md)
518. [githubService](modules/githubService.md)
519. [labelService](modules/labelService.md)
520. [LabelSelector](modules/LabelSelector.md)
521. [outboundWebhookService](modules/outboundWebhookService.md)
522. [planShareService](modules/planShareService.md)
523. [planningInputService](modules/planningInputService.md)
524. [usePlanningObservation](modules/usePlanningObservation.md)
525. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
526. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
527. [calendarService](modules/calendarService.md)
528. [PersonCapacity](modules/PersonCapacity.md)
529. [PersonCapacity.test](modules/PersonCapacity.test.md)
530. [exportService](modules/exportService.md)
531. [IterationImportDialog](modules/IterationImportDialog.md)
532. [iterationService](modules/iterationService.md)
533. [IterationSelector](modules/IterationSelector.md)
534. [planningInputService.test](modules/planningInputService.test.md)
535. [projectService](modules/projectService.md)
536. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
537. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
538. [releaseService](modules/releaseService.md)
539. [ReleaseForm](modules/ReleaseForm.md)
540. [requestSourceService](modules/requestSourceService.md)
541. [savedViewService](modules/savedViewService.md)
542. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
543. [schedulingRulesService](modules/schedulingRulesService.md)
544. [AdminAccessPanel](modules/AdminAccessPanel.md)
545. [AdminAccessGate](modules/AdminAccessGate.md)
546. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
547. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
548. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
549. [sessionService](modules/sessionService.md)
550. [snapshotService](modules/snapshotService.md)
551. [snapshotVersions.test](modules/snapshotVersions.test.md)
552. [systemSettingsService](modules/systemSettingsService.md)
553. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
554. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
555. [taskService](modules/taskService.md)
556. [DeliveryDependencies](modules/DeliveryDependencies.md)
557. [ImportTasksModal](modules/ImportTasksModal.md)
558. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
559. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
560. [TaskContextSummary](modules/TaskContextSummary.md)
561. [TaskDependencySelector](modules/TaskDependencySelector.md)
562. [TaskReviewer](modules/TaskReviewer.md)
563. [TaskSearch](modules/TaskSearch.md)
564. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
565. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
566. [TaskWorkPanel](modules/TaskWorkPanel.md)
567. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
568. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
569. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
570. [teamService](modules/teamService.md)
571. [GanttBarInputs](modules/GanttBarInputs.md)
572. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
573. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
574. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
575. [ImportTeamModal](modules/ImportTeamModal.md)
576. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
577. [TeamForm](modules/TeamForm.md)
578. [TeamForm.test](modules/TeamForm.test.md)
579. [TeamProfileManager](modules/TeamProfileManager.md)
580. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
581. [VacationCsvImport](modules/VacationCsvImport.md)
582. [LocalProfilePicker](modules/LocalProfilePicker.md)
583. [CalendarPage](modules/CalendarPage.md)
584. [CalendarPage.test](modules/CalendarPage.test.md)
585. [templateService](modules/templateService.md)
586. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
587. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
588. [timeEntryService](modules/timeEntryService.md)
589. [useTimeEntries](modules/useTimeEntries.md)
590. [timeEntryService.test](modules/timeEntryService.test.md)
591. [triageService](modules/triageService.md)
592. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
593. [copyText](modules/copyText.md)
594. [focusLifecycle](modules/focusLifecycle.md)
595. [focusLifecycle.test](modules/focusLifecycle.test.md)
596. [formatDate](modules/formatDate.md)
597. [TaskStatusFlow](modules/TaskStatusFlow.md)
598. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
599. [IterationForm](modules/IterationForm.md)
600. [IterationForm.test](modules/IterationForm.test.md)
601. [IterationList](modules/IterationList.md)
602. [NotificationsPanel](modules/NotificationsPanel.md)
603. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
604. [StatusChangeControl](modules/StatusChangeControl.md)
605. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
606. [TimeEntriesReport](modules/TimeEntriesReport.md)
607. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
608. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
609. [VacationManager](modules/VacationManager.md)
610. [TeamList](modules/TeamList.md)
611. [planningMasters_masters](modules/planningMasters_masters.md)
612. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
613. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
614. [SidebarIterationCard](modules/SidebarIterationCard.md)
615. [AppSidebar](modules/AppSidebar.md)
616. [AppSidebar.test](modules/AppSidebar.test.md)
617. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
618. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
619. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
620. [usePlanningReadiness](modules/usePlanningReadiness.md)
621. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
622. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
623. [IdentityProvider](modules/IdentityProvider.md)
624. [UserSessionBadge](modules/UserSessionBadge.md)
625. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
626. [IdentityProvider.test](modules/IdentityProvider.test.md)
627. [useLiveWindow.test](modules/useLiveWindow.test.md)
628. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
629. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
630. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
631. [AnalyticsPage](modules/AnalyticsPage.md)
632. [IterationsPage](modules/IterationsPage.md)
633. [PlanMasterPage](modules/PlanMasterPage.md)
634. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
635. [PlanPage](modules/PlanPage.md)
636. [PlanPage.test](modules/PlanPage.test.md)
637. [PlanSharePage](modules/PlanSharePage.md)
638. [PlanSharePage.test](modules/PlanSharePage.test.md)
639. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
640. [TeamPage](modules/TeamPage.md)
641. [graphLimitError](modules/graphLimitError.md)
642. [modelRouting](modules/modelRouting.md)
643. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
644. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
645. [modelRouting.test](modules/modelRouting.test.md)
646. [protectedQueries](modules/protectedQueries.md)
647. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
648. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
649. [AgentAccessPanel](modules/AgentAccessPanel.md)
650. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
651. [AgentModelAdministration](modules/AgentModelAdministration.md)
652. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
653. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
654. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
655. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
656. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
657. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
658. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
659. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
660. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
661. [AgentPipelinePage](modules/AgentPipelinePage.md)
662. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
663. [safeUrl](modules/safeUrl.md)
664. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
665. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
666. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
667. [TaskReadView](modules/TaskReadView.md)
668. [TaskReadView.test](modules/TaskReadView.test.md)
669. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
670. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
671. [OverviewPage](modules/OverviewPage.md)
672. [OverviewPage.test](modules/OverviewPage.test.md)
673. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
674. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
675. [CommandMenu](modules/CommandMenu.md)
676. [CommandMenu.test](modules/CommandMenu.test.md)
677. [ContextHelp](modules/ContextHelp.md)
678. [AppTopNav](modules/AppTopNav.md)
679. [AppShell](modules/AppShell.md)
680. [App](modules/App.md)
681. [AppShell.test](modules/AppShell.test.md)
682. [AppTopNav.test](modules/AppTopNav.test.md)
683. [ContextHelp.test](modules/ContextHelp.test.md)
684. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
685. [src_main](modules/src_main.md)
686. [SettingsPage](modules/SettingsPage.md)
687. [SettingsPage.test](modules/SettingsPage.test.md)
688. [taskFilterDefaults](modules/taskFilterDefaults.md)
689. [TaskFiltersBar](modules/TaskFiltersBar.md)
690. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
691. [taskViewState](modules/taskViewState.md)
692. [savedViewState](modules/savedViewState.md)
693. [SavedViewsControl](modules/SavedViewsControl.md)
694. [savedViewState.test](modules/savedViewState.test.md)
695. [taskFilters](modules/taskFilters.md)
696. [taskFilters.test](modules/taskFilters.test.md)
697. [teamMemberLabels](modules/teamMemberLabels.md)
698. [InitiativeForm](modules/InitiativeForm.md)
699. [RoadmapPage](modules/RoadmapPage.md)
700. [RoadmapPage.test](modules/RoadmapPage.test.md)
701. [templateDefaults](modules/templateDefaults.md)
702. [ProjectForm](modules/ProjectForm.md)
703. [TaskForm](modules/TaskForm.md)
704. [TaskEditModal](modules/TaskEditModal.md)
705. [GanttChart](modules/GanttChart.md)
706. [GanttChart.test](modules/GanttChart.test.md)
707. [GuardedTaskModal](modules/GuardedTaskModal.md)
708. [BacklogPanel](modules/BacklogPanel.md)
709. [CurrentTaskModal.test](modules/CurrentTaskModal.test.md)
710. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
711. [ProjectTaskTree](modules/ProjectTaskTree.md)
712. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
713. [TaskForm.test](modules/TaskForm.test.md)
714. [GanttPage](modules/GanttPage.md)
715. [GanttPage.test](modules/GanttPage.test.md)
716. [MyWorkPage](modules/MyWorkPage.md)
717. [MyWorkPage.test](modules/MyWorkPage.test.md)
718. [ProjectDetailPage](modules/ProjectDetailPage.md)
719. [ProjectsPage](modules/ProjectsPage.md)
720. [ProjectsPage.test](modules/ProjectsPage.test.md)
721. [TriagePage](modules/TriagePage.md)
722. [visibleWork](modules/visibleWork.md)
723. [KanbanBoard](modules/KanbanBoard.md)
724. [KanbanBoard.test](modules/KanbanBoard.test.md)
725. [TaskList](modules/TaskList.md)
726. [TaskList.test](modules/TaskList.test.md)
727. [TasksPage](modules/TasksPage.md)
728. [TasksPage.test](modules/TasksPage.test.md)
729. [visibleWork.test](modules/visibleWork.test.md)
730. [tailwind.config](modules/tailwind.config.md)
731. [check-tailwind-classes](modules/check-tailwind-classes.md)
732. [vite.config](modules/vite.config.md)
733. [vitest.config](modules/vitest.config.md)
734. [create_agent_actor](modules/create_agent_actor.md)
735. [generate_workchord_keys](modules/generate_workchord_keys.md)
736. [setup_agent_team](modules/setup_agent_team.md)
737. [build_agent_skills](modules/build_agent_skills.md)
738. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
739. [android_qualification](modules/android_qualification.md)
740. [android_web_peer](modules/android_web_peer.md)
741. [apt_runtime](modules/apt_runtime.md)
742. [browser_performance](modules/browser_performance.md)
743. [browser_planning_inputs](modules/browser_planning_inputs.md)
744. [browser_worker](modules/browser_worker.md)
745. [browser_managed_work](modules/browser_managed_work.md)
746. [browser_write_readback](modules/browser_write_readback.md)
747. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
748. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
749. [ci_runtime](modules/ci_runtime.md)
750. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
751. [postgres_runtime](modules/postgres_runtime.md)
752. [run_android_checks](modules/run_android_checks.md)
753. [run_disposable_checks](modules/run_disposable_checks.md)
754. [serve_disposable_api](modules/serve_disposable_api.md)
755. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
756. [test_apt_runtime](modules/test_apt_runtime.md)
757. [test_ci_runtime](modules/test_ci_runtime.md)
758. [test_native_runtimes](modules/test_native_runtimes.md)
759. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
760. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
761. [generate_client_contract](modules/generate_client_contract.md)
762. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
763. [load_common](modules/load_common.md)
764. [collect](modules/collect.md)
765. [result](modules/result.md)
766. [compare](modules/compare.md)
767. [finalize](modules/finalize.md)
768. [qualify](modules/qualify.md)
769. [resilience](modules/resilience.md)
770. [run](modules/run.md)
771. [seal](modules/seal.md)
772. [seed](modules/seed.md)
773. [source_binding](modules/source_binding.md)
774. [local_baseline](modules/local_baseline.md)
775. [service_worksets](modules/service_worksets.md)
776. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
777. [isolated_rehearsal](modules/isolated_rehearsal.md)

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
| [test_android_cleanup](modules/test_android_cleanup.md) | `sys.path.insert` |
| [test_load_seed_postgresql](modules/test_load_seed_postgresql.md) | `sys.path.insert` |
| [test_load_tooling](modules/test_load_tooling.md) | `sys.path.insert` |
| [test_routing_evidence](modules/test_routing_evidence.md) | `sys.path.insert` |
| [support_database](modules/support_database.md) | `TEST_DATABASE_PATTERN = re.compile`, `TEST_RUNTIME_ROLE_PATTERN = re.compile`, `DEFAULT_POSTGRES_HOSTS = frozenset`, `ADMIN_DATABASES = frozenset` |
| [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md) | `_PROVISION_SPEC = importlib.util.spec_from_file_location`, `provision_actor = importlib.util.module_from_spec`, `_PROVISION_SPEC.loader.exec_module` |
| [test_agent_routing_service](modules/test_agent_routing_service.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md) | `pytestmark = pytest.mark.usefixtures`, `_FIXED_NOW = datetime` |
| [test_agent_team_setup](modules/test_agent_team_setup.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md) | `SPEC = importlib.util.spec_from_file_location`, `setup_agent_team = importlib.util.module_from_spec`, `SPEC.loader.exec_module` |
| [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md) | `FIXED_NOW = datetime` |
| [test_native_connections](modules/test_native_connections.md) | `CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b'=').decode` |
| [test_plan_checkpoints](modules/test_plan_checkpoints.md) | `READY = dict` |
| [check-bundle-budget](modules/check-bundle-budget.md) | `BUDGETS = freeze` |
| [check-query-feedback](modules/check-query-feedback.md) | `HOOK_KINDS = Map` |
| [check-tailwind-classes](modules/check-tailwind-classes.md) | `semanticRoots = Set`, `colorUtilityPrefixes = sort`, `colorUtilitySource = join`, `semanticRootSource = join`, `semanticClassPattern = RegExp`, `legacyClassPattern = RegExp`, `rawPaletteClassPattern = RegExp`, `darkVariantClassPattern = RegExp`, `arbitraryColorClassPattern = RegExp`, `translucentSemanticTextPattern = RegExp`, `semanticColorNames = Set` |
| [App](modules/App.md) | `OverviewPage = lazy`, `LandingPage = lazy`, `PlanPage = lazy`, `PlanMasterPage = lazy`, `PlanSharePage = lazy`, `CalendarPage = lazy`, `IterationsPage = lazy`, `TeamPage = lazy`, `TasksPage = lazy`, `MyWorkPage = lazy`, `NativeConnectionPage = lazy`, `TriagePage = lazy`, `ProjectsPage = lazy`, `ProjectDetailPage = lazy`, `ProjectReleaseDetailPage = lazy`, `RoadmapPage = lazy`, `GanttPage = lazy`, `AnalyticsPage = lazy`, `SettingsPage = lazy`, `AgentPipelinePage = lazy`, `AgentTeamSetupMasterPage = lazy`, `NotFoundPage = lazy` |
| [UserSessionBadge.test](modules/UserSessionBadge.test.md) | `sessionServiceMock = hoisted`, `mock`, `describe` |
| [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md) | `describe` |
| [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md) | `agentServiceMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `dispatchableRoster = map`, `describe` |
| [TaskRoutingPanel](modules/TaskRoutingPanel.md) | `SKILL_CATALOG_READ_SCOPES = Set`, `TEAM_ASSIGNMENT_READ_SCOPES = Set` |
| [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md) | `metrics = hoisted`, `projects = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md) | `service = hoisted`, `mock`, `describe` |
| [InteractiveCalendar.test](modules/InteractiveCalendar.test.md) | `describe` |
| [Button.test](modules/Button.test.md) | `describe` |
| [Button](modules/Button.md) | `Button = forwardRef` |
| [Checkbox](modules/Checkbox.md) | `Checkbox = forwardRef` |
| [Input.test](modules/Input.test.md) | `describe` |
| [Input](modules/Input.md) | `Input = forwardRef` |
| [dialogLayer](modules/dialogLayer.md) | `focusableSelector = join` |
| [ToastProvider.test](modules/ToastProvider.test.md) | `describe` |
| [toast](modules/toast.md) | `ToastContext = createContext` |
| [GanttChart.test](modules/GanttChart.test.md) | `ganttServiceMock = hoisted`, `mock`, `mock`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe` |
| [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md) | `t = bind` |
| [IterationForm.test](modules/IterationForm.test.md) | `planningMock = hoisted`, `mock`, `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `iterationStoreMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [AppShell.test](modules/AppShell.test.md) | `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AppSidebar.test](modules/AppSidebar.test.md) | `savedViewServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [AppSidebar](modules/AppSidebar.md) | `SAVED_VIEW_ROUTE_PATHS = Set` |
| [AppTopNav.test](modules/AppTopNav.test.md) | `planningReadinessMock = hoisted`, `triageServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [CommandMenu.test](modules/CommandMenu.test.md) | `lookup = hoisted`, `mock`, `describe` |
| [ContextHelp.test](modules/ContextHelp.test.md) | `describe` |
| [SidebarIterationCard.test](modules/SidebarIterationCard.test.md) | `planningReadinessMock = hoisted`, `mock`, `describe` |
| [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md) | `team = hoisted`, `planning = hoisted`, `mock`, `mock`, `describe` |
| [PlanReturnBar.test](modules/PlanReturnBar.test.md) | `describe` |
| [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md) | `reader = hoisted`, `mock`, `beforeEach`, `it`, `it` |
| [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md) | `describe` |
| [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md) | `describe` |
| [ProjectForm](modules/ProjectForm.md) | `projectStatusValues = map`, `projectHealthValues = map` |
| [ProjectTaskTree](modules/ProjectTaskTree.md) | `t = bind` |
| [TimeEntriesReport.test](modules/TimeEntriesReport.test.md) | `capability = hoisted`, `mock`, `it` |
| [projectStatusStyles.test](modules/projectStatusStyles.test.md) | `describe` |
| [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md) | `requestSourceServiceMock = hoisted`, `mock`, `describe` |
| [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md) | `t = bind` |
| [AdminAccessPanel.test](modules/AdminAccessPanel.test.md) | `adminAccessHookMock = hoisted`, `adminAccessStorageMock = hoisted`, `schedulingRulesMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
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
| [PersonCapacity.test](modules/PersonCapacity.test.md) | `api = hoisted`, `mock`, `beforeEach`, `it` |
| [SavedViewsControl](modules/SavedViewsControl.md) | `t = bind` |
| [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md) | `describe` |
| [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md) | `t = bind` |
| [TaskBriefEditor.test](modules/TaskBriefEditor.test.md) | `describe` |
| [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md) | `t = bind` |
| [TaskDependencySelector](modules/TaskDependencySelector.md) | `t = bind` |
| [TaskDiscussion.test](modules/TaskDiscussion.test.md) | `service = hoisted`, `mock`, `describe` |
| [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `it` |
| [TaskFiltersBar.test](modules/TaskFiltersBar.test.md) | `mock`, `mock`, `mock`, `describe` |
| [TaskForm.test](modules/TaskForm.test.md) | `api = hoisted`, `mock`, `describe` |
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `it`, `it`, `it` |
| [TaskReadView.test](modules/TaskReadView.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md) | `service = hoisted`, `iterations = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind` |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | `service = hoisted`, `mock`, `mock`, `describe`, `it`, `describe` |
| [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md) | `service = hoisted`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it`, `it.each([true, false])`, `it` |
| [taskDraftStorage.test](modules/taskDraftStorage.test.md) | `it` |
| [useDraftDismissal.test](modules/useDraftDismissal.test.md) | `it`, `describe`, `it` |
| [ImportTeamModal.test](modules/ImportTeamModal.test.md) | `planningMock = hoisted`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe` |
| [TeamForm.test](modules/TeamForm.test.md) | `planningMock = hoisted`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe` |
| [TeamProfileManager.test](modules/TeamProfileManager.test.md) | `teamServiceMock = hoisted`, `planningMock = hoisted`, `mock`, `mock`, `describe`, `describe` |
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
| [planningMasters_masters.test](modules/planningMasters_masters.test.md) | `describe`, `describe` |
| [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md) | `describe` |
| [planningNavigationInvalidation](modules/planningNavigationInvalidation.md) | `READINESS_INPUT_QUERY_ROOTS = Set` |
| [planningTaskIssues.test](modules/planningTaskIssues.test.md) | `describe`, `describe` |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [useLiveWindow.test](modules/useLiveWindow.test.md) | `it`, `it.each([0, -1, NaN, undefined])`, `it`, `it`, `it` |
| [workQueryFreshness.test](modules/workQueryFreshness.test.md) | `cases = flatMap`, `it.each(cases)` |
| [workQueryFreshness](modules/workQueryFreshness.md) | `WORKSPACE_QUERY_POLICIES = fromEntries` |
| [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md) | `it.each(['hidden', 'disabled', 'unauthorized', 'too-many-pages'])`, `it`, `it`, `it`, `it` |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | `describe` |
| [i18n.test](modules/i18n.test.md) | `describe` |
| [workflowVocabulary.test](modules/workflowVocabulary.test.md) | `describe` |
| [src_main](modules/src_main.md) | `queryClient = QueryClient`, `router = createBrowserRouter`, `render` |
| [workspaces.test](modules/workspaces.test.md) | `describe` |
| [workspaces](modules/workspaces.md) | `PRIMARY_NAV_ITEMS = flatMap` |
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set`, `TASK_STATUSES = Set` |
| [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe` |
| [CalendarPage.test](modules/CalendarPage.test.md) | `api = hoisted`, `mock`, `it` |
| [GanttPage.test](modules/GanttPage.test.md) | `ganttServiceMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [MyWorkPage.test](modules/MyWorkPage.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `it`, `it`, `it` |
| [NativeConnectionPage.test](modules/NativeConnectionPage.test.md) | `service = hoisted`, `mock`, `request = repeat`, `describe` |
| [OverviewPage.test](modules/OverviewPage.test.md) | `planningReadinessMock = hoisted`, `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [OverviewPage](modules/OverviewPage.md) | `doneStatuses = Set`, `invalidCachedStatuses = Set`, `operationalAttentionIds = Set`, `commitmentAttentionIds = Set` |
| [PlanMasterPage.test](modules/PlanMasterPage.test.md) | `planningReadinessMock = hoisted`, `planShareServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [PlanPage.test](modules/PlanPage.test.md) | `planningReadinessMock = hoisted`, `mock`, `describe` |
| [PlanSharePage.test](modules/PlanSharePage.test.md) | `planShareServiceMock = hoisted`, `mock`, `describe` |
| [ProjectDetailPage](modules/ProjectDetailPage.md) | `t = bind` |
| [ProjectsPage.test](modules/ProjectsPage.test.md) | `projectServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [RoadmapPage.test](modules/RoadmapPage.test.md) | `projectServiceMock = hoisted`, `mock`, `describe`, `describe` |
| [RoadmapPage](modules/RoadmapPage.md) | `t = bind` |
| [SettingsPage.test](modules/SettingsPage.test.md) | `themeStoreMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [SettingsPage](modules/SettingsPage.md) | `SETTINGS_DESTINATIONS = flatMap` |
| [TasksPage.test](modules/TasksPage.test.md) | `iterationServiceMock = hoisted`, `iterationStoreMock = hoisted`, `savedViewServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TriagePage](modules/TriagePage.md) | `t = bind` |
| [agentService.test](modules/agentService.test.md) | `mock`, `mockedApi = mocked`, `describe` |
| [api](modules/api.md) | `api = create`, `use`, `use` |
| [planningInputService.test](modules/planningInputService.test.md) | `mock`, `beforeEach`, `it`, `it`, `it.each([
    { complete: false }, { resource_id: 8 }, { expected_revisions: { 1: 0 } },
    { expected_revisions: { 1: true } }, { expected_revisions: { '-1': 4 } }, { resource: { id: 8 } },
])` |
| [snapshotVersions.test](modules/snapshotVersions.test.md) | `mock`, `it` |
| [taskDependencyVersions.test](modules/taskDependencyVersions.test.md) | `mock`, `it` |
| [timeEntryService.test](modules/timeEntryService.test.md) | `api = hoisted`, `mock`, `beforeEach`, `it`, `it` |
| [iterationStore.test](modules/iterationStore.test.md) | `describe` |
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
| [taskFilters.test](modules/taskFilters.test.md) | `describe`, `describe`, `describe` |
| [teamMemberLabels](modules/teamMemberLabels.md) | `t = bind` |
| [visibleWork.test](modules/visibleWork.test.md) | `it`, `it`, `it` |
| [build_agent_skills](modules/build_agent_skills.md) | `SEMVER_RE = re.compile`, `SKILL_NAME_RE = re.compile`, `COMPATIBILITY_RE = re.compile`, `MARKDOWN_LINK_RE = re.compile`, `URL_RE = re.compile` |
| [build_frontend_image_identity](modules/build_frontend_image_identity.md) | `[artifactRootArg, sourceRevision, outputArg] = slice`, `artifactRoot = resolve`, `output = resolve`, `digest = createHash` |
| [android_web_peer](modules/android_web_peer.md) | `[origin, task, nonce] = slice`, `on`, `on` |
| [browser_managed_work](modules/browser_managed_work.md) | `on`, `on` |
| [browser_performance](modules/browser_performance.md) | `on` |
| [browser_write_readback](modules/browser_write_readback.md) | `on` |
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

## Notes

This page presents a static dependency projection. Lazy imports, conditional initialization, and runtime side effects can change the effective order.

The authority and command modules are cross-cutting runtime boundaries. Intentional late imports connect the model registry, task services, recovery and identity without treating static cycles as proof of runtime order. The extraction remains bounded; unsupported Kotlin/shell sources and unsupported YAML candidates require direct source evidence.

Task, brief, status and recovery services use deliberate late imports to share command ownership without eager initialization cycles. The triage draft projection invokes the canonical renderer at serialization time. Bounded UI detail remains separate from the full graph used for assigned execution and scheduling.

Recovery models register the task deletion hook; the task recovery helper imports TaskService lazily to reuse command version reservations. This keeps the model-registration side effect explicit without treating static import order as runtime execution order.

Database creation order is explicit in the initial Alembic revision and is separate from this module-import projection. PostgreSQL cyclic foreign keys are installed after all participating tables exist; SQLite creates the inline references without inserting application rows.

Delivery and discussion model imports register flush listeners. The command owner invokes delivery reconciliation and outbox enqueue after flushing and before commit; previews roll back the same work. Outbound dispatch imports the discussion sink lazily, and the sink uses the existing transport error type lazily to avoid eager initialization cycles. Typed transfer references remain present where aggregate constraints forbid staging them as null.

NativeSessionService reuses IdentityService session issuance and the command transaction owner. Native exchange locks the principal before its approving browser session to align with account revocation. The Android session and cookie implementation requires direct platform evidence because Kotlin extraction is unavailable in the configured analyzer.
