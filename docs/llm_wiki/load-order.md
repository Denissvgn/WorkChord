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
46. [20261111_0013_local_comment_authors](modules/20261111_0013_local_comment_authors.md)
47. [query_limits](modules/query_limits.md)
48. [runtime_telemetry](modules/runtime_telemetry.md)
49. [database_runtime](modules/database_runtime.md)
50. [maintenance](modules/maintenance.md)
51. [mutation_versions](modules/mutation_versions.md)
52. [schemas_agent_planning](modules/schemas_agent_planning.md)
53. [agent_skill_bundle](modules/agent_skill_bundle.md)
54. [agent_team_setup](modules/agent_team_setup.md)
55. [schemas_autonomy](modules/schemas_autonomy.md)
56. [schemas_common](modules/schemas_common.md)
57. [delivery_metrics](modules/delivery_metrics.md)
58. [schemas_execution_usage](modules/schemas_execution_usage.md)
59. [schemas_github](modules/schemas_github.md)
60. [schemas_intake](modules/schemas_intake.md)
61. [schemas_label](modules/schemas_label.md)
62. [schemas_plan_share](modules/schemas_plan_share.md)
63. [planning_inputs](modules/planning_inputs.md)
64. [schemas_calendar](modules/schemas_calendar.md)
65. [schemas_saved_view](modules/schemas_saved_view.md)
66. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
67. [schemas_session](modules/schemas_session.md)
68. [snapshot](modules/snapshot.md)
69. [schemas_system_settings](modules/schemas_system_settings.md)
70. [schemas_email_settings](modules/schemas_email_settings.md)
71. [schemas_task_brief](modules/schemas_task_brief.md)
72. [schemas_llm](modules/schemas_llm.md)
73. [schemas_task_domain](modules/schemas_task_domain.md)
74. [schemas_team](modules/schemas_team.md)
75. [schemas_template](modules/schemas_template.md)
76. [schemas_time_entry](modules/schemas_time_entry.md)
77. [time_report](modules/time_report.md)
78. [schemas_work_metrics](modules/schemas_work_metrics.md)
79. [schemas_iteration](modules/schemas_iteration.md)
80. [schemas_project](modules/schemas_project.md)
81. [schemas_release](modules/schemas_release.md)
82. [security](modules/security.md)
83. [agent_routing_policy](modules/agent_routing_policy.md)
84. [agent_routing](modules/agent_routing.md)
85. [agent_routing_rollout](modules/agent_routing_rollout.md)
86. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
87. [agent_team_credentials](modules/agent_team_credentials.md)
88. [bounded_scope_reads](modules/bounded_scope_reads.md)
89. [language_service](modules/language_service.md)
90. [plan_checkpoints](modules/plan_checkpoints.md)
91. [planning_input_context](modules/planning_input_context.md)
92. [planning_issues](modules/planning_issues.md)
93. [scheduling_rules_service](modules/scheduling_rules_service.md)
94. [upgrade_service](modules/upgrade_service.md)
95. [upgrade](modules/upgrade.md)
96. [settings_read](modules/settings_read.md)
97. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
98. [sql_semantics](modules/sql_semantics.md)
99. [exceptions](modules/exceptions.md)
100. [text_similarity](modules/text_similarity.md)
101. [time](modules/time.md)
102. [observability](modules/observability.md)
103. [app_database](modules/app_database.md)
104. [models_agent](modules/models_agent.md)
105. [models_autonomy](modules/models_autonomy.md)
106. [models_calendar](modules/models_calendar.md)
107. [models_capacity](modules/models_capacity.md)
108. [models_database_migration](modules/models_database_migration.md)
109. [delivery_dependency](modules/delivery_dependency.md)
110. [models_discussion](modules/models_discussion.md)
111. [models_execution_usage](modules/models_execution_usage.md)
112. [models_external_link](modules/models_external_link.md)
113. [models_github](modules/models_github.md)
114. [models_identity](modules/models_identity.md)
115. [models_iteration](modules/models_iteration.md)
116. [models_label](modules/models_label.md)
117. [native_connection](modules/native_connection.md)
118. [models_outbound_webhook](modules/models_outbound_webhook.md)
119. [models_plan_share](modules/models_plan_share.md)
120. [models_release](modules/models_release.md)
121. [models_project](modules/models_project.md)
122. [models_request_source](modules/models_request_source.md)
123. [models_saved_view](modules/models_saved_view.md)
124. [models_system_settings](modules/models_system_settings.md)
125. [models_task](modules/models_task.md)
126. [recovery](modules/recovery.md)
127. [models_task_brief](modules/models_task_brief.md)
128. [delivery_observation](modules/delivery_observation.md)
129. [task_status_log](modules/task_status_log.md)
130. [team_member](modules/team_member.md)
131. [models_template](modules/models_template.md)
132. [models_time_entry](modules/models_time_entry.md)
133. [models_triage](modules/models_triage.md)
134. [user_session](modules/user_session.md)
135. [models___init__](modules/models___init__.md)
136. [catalog](modules/catalog.md)
137. [database_migration_canonical](modules/database_migration_canonical.md)
138. [source](modules/source.md)
139. [transfer](modules/transfer.md)
140. [cli_database_migration](modules/cli_database_migration.md)
141. [database_migration___init__](modules/database_migration___init__.md)
142. [migrations_env](modules/migrations_env.md)
143. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
144. [calendar_service](modules/calendar_service.md)
145. [calendars](modules/calendars.md)
146. [capacity_service](modules/capacity_service.md)
147. [routers_capacity](modules/routers_capacity.md)
148. [delivery_dependency_service](modules/delivery_dependency_service.md)
149. [delivery_metrics_service](modules/delivery_metrics_service.md)
150. [discussion_service](modules/discussion_service.md)
151. [identity_service](modules/identity_service.md)
152. [import_planning_service](modules/import_planning_service.md)
153. [iteration_service](modules/iteration_service.md)
154. [iterations](modules/iterations.md)
155. [label_service](modules/label_service.md)
156. [labels](modules/labels.md)
157. [native_session_service](modules/native_session_service.md)
158. [saved_view_service](modules/saved_view_service.md)
159. [session_service](modules/session_service.md)
160. [http_authority](modules/http_authority.md)
161. [routers_identity](modules/routers_identity.md)
162. [saved_views](modules/saved_views.md)
163. [routers_session](modules/routers_session.md)
164. [task_brief_service](modules/task_brief_service.md)
165. [task_context_revision_service](modules/task_context_revision_service.md)
166. [task_domain_service](modules/task_domain_service.md)
167. [task_hierarchy_service](modules/task_hierarchy_service.md)
168. [task_recovery_service](modules/task_recovery_service.md)
169. [task_timeline_service](modules/task_timeline_service.md)
170. [team_service](modules/team_service.md)
171. [routers_team](modules/routers_team.md)
172. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
173. [snapshot_service](modules/snapshot_service.md)
174. [plan_share_service](modules/plan_share_service.md)
175. [plan_shares](modules/plan_shares.md)
176. [template_service](modules/template_service.md)
177. [templates](modules/templates.md)
178. [time_entry_service](modules/time_entry_service.md)
179. [time_report_service](modules/time_report_service.md)
180. [services_work_metrics](modules/services_work_metrics.md)
181. [import_parser](modules/import_parser.md)
182. [url_policy](modules/url_policy.md)
183. [schemas_external_link](modules/schemas_external_link.md)
184. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
185. [schemas_request_source](modules/schemas_request_source.md)
186. [schemas_task](modules/schemas_task.md)
187. [schemas_gantt](modules/schemas_gantt.md)
188. [task_detail](modules/task_detail.md)
189. [schemas_triage](modules/schemas_triage.md)
190. [schemas___init__](modules/schemas___init__.md)
191. [schemas_agent](modules/schemas_agent.md)
192. [agent_readiness](modules/agent_readiness.md)
193. [llm_service](modules/llm_service.md)
194. [system_settings_service](modules/system_settings_service.md)
195. [routers_system_settings](modules/routers_system_settings.md)
196. [email_settings_service](modules/email_settings_service.md)
197. [routers_email_settings](modules/routers_email_settings.md)
198. [notification_service](modules/notification_service.md)
199. [outbound_webhook_service](modules/outbound_webhook_service.md)
200. [worker](modules/worker.md)
201. [outbound_webhooks](modules/outbound_webhooks.md)
202. [external_link_service](modules/external_link_service.md)
203. [github_status_service](modules/github_status_service.md)
204. [request_source_service](modules/request_source_service.md)
205. [request_sources](modules/request_sources.md)
206. [project_service](modules/project_service.md)
207. [task_detail_service](modules/task_detail_service.md)
208. [task_import_service](modules/task_import_service.md)
209. [task_service](modules/task_service.md)
210. [export](modules/export.md)
211. [snapshots](modules/snapshots.md)
212. [agent_routing_observability](modules/agent_routing_observability.md)
213. [agent_service](modules/agent_service.md)
214. [agent_skill_bundles](modules/agent_skill_bundles.md)
215. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
216. [agent_routing_service](modules/agent_routing_service.md)
217. [agent_team_setup_service](modules/agent_team_setup_service.md)
218. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
219. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
220. [execution_usage_service](modules/execution_usage_service.md)
221. [routers_task_domain](modules/routers_task_domain.md)
222. [delivery_dependencies](modules/delivery_dependencies.md)
223. [routers_discussion](modules/routers_discussion.md)
224. [time_entries](modules/time_entries.md)
225. [github_status_automation_service](modules/github_status_automation_service.md)
226. [release_service](modules/release_service.md)
227. [projects](modules/projects.md)
228. [scheduler_service](modules/scheduler_service.md)
229. [routers_gantt](modules/routers_gantt.md)
230. [routers_llm](modules/routers_llm.md)
231. [agent_planning_service](modules/agent_planning_service.md)
232. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
233. [tasks](modules/tasks.md)
234. [task_status_service](modules/task_status_service.md)
235. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
236. [triage_service](modules/triage_service.md)
237. [routers_triage](modules/routers_triage.md)
238. [agent_work_service](modules/agent_work_service.md)
239. [mcp_agent_tools](modules/mcp_agent_tools.md)
240. [mcp_server](modules/mcp_server.md)
241. [routers_agent](modules/routers_agent.md)
242. [routers_agent_planning](modules/routers_agent_planning.md)
243. [agent_catalog](modules/agent_catalog.md)
244. [github_webhook_service](modules/github_webhook_service.md)
245. [routers_github](modules/routers_github.md)
246. [web_intake_service](modules/web_intake_service.md)
247. [routers_intake](modules/routers_intake.md)
248. [app_main](modules/app_main.md)
249. [routers___init__](modules/routers___init__.md)
250. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
251. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
252. [test_server_acceptance](modules/test_server_acceptance.md)
253. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
254. [test_work_package_service](modules/test_work_package_service.md)
255. [test_database_configuration](modules/test_database_configuration.md)
256. [test_deployment_topology](modules/test_deployment_topology.md)
257. [test_observability](modules/test_observability.md)
258. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
259. [test_query_boundaries](modules/test_query_boundaries.md)
260. [test_runtime_policy](modules/test_runtime_policy.md)
261. [test_schema_behavior](modules/test_schema_behavior.md)
262. [test_cutover_evidence](modules/test_cutover_evidence.md)
263. [test_documentation_boundary](modules/test_documentation_boundary.md)
264. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
265. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
266. [test_source_preflight](modules/test_source_preflight.md)
267. [test_transfer_catalog](modules/test_transfer_catalog.md)
268. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
269. [0001_wave0_probe](modules/0001_wave0_probe.md)
270. [test_allocation_identity](modules/test_allocation_identity.md)
271. [test_initial_schema](modules/test_initial_schema.md)
272. [test_profile_identity](modules/test_profile_identity.md)
273. [test_android_cleanup](modules/test_android_cleanup.md)
274. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
275. [test_load_tooling](modules/test_load_tooling.md)
276. [test_local_baseline](modules/test_local_baseline.md)
277. [test_routing_evidence](modules/test_routing_evidence.md)
278. [support_database](modules/support_database.md)
279. [delivery](modules/delivery.md)
280. [factories](modules/factories.md)
281. [faults](modules/faults.md)
282. [runtime_peer](modules/runtime_peer.md)
283. [schema](modules/schema.md)
284. [support___init__](modules/support___init__.md)
285. [conftest](modules/conftest.md)
286. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
287. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
288. [test_project_identity](modules/test_project_identity.md)
289. [test_project_identity_scope](modules/test_project_identity_scope.md)
290. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
291. [transactions](modules/transactions.md)
292. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
293. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
294. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
295. [test_agent_routing_data](modules/test_agent_routing_data.md)
296. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
297. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
298. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
299. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
300. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
301. [test_agent_routing_service](modules/test_agent_routing_service.md)
302. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
303. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
304. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
305. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
306. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
307. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
308. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
309. [test_authority_migrations](modules/test_authority_migrations.md)
310. [test_capacity_contract](modules/test_capacity_contract.md)
311. [test_client_contract](modules/test_client_contract.md)
312. [test_database_harness](modules/test_database_harness.md)
313. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
314. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
315. [test_agent_team_setup](modules/test_agent_team_setup.md)
316. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
317. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
318. [test_deployment_configuration](modules/test_deployment_configuration.md)
319. [test_effective_deferral](modules/test_effective_deferral.md)
320. [test_execution_usage](modules/test_execution_usage.md)
321. [test_execution_working_dates](modules/test_execution_working_dates.md)
322. [test_managed_authority](modules/test_managed_authority.md)
323. [test_allocation_recovery](modules/test_allocation_recovery.md)
324. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
325. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
326. [test_metric_matches](modules/test_metric_matches.md)
327. [test_mobile_contract](modules/test_mobile_contract.md)
328. [test_mutation_versions](modules/test_mutation_versions.md)
329. [test_native_connections](modules/test_native_connections.md)
330. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
331. [test_plan_shares](modules/test_plan_shares.md)
332. [test_planning_input_context](modules/test_planning_input_context.md)
333. [test_planning_issues](modules/test_planning_issues.md)
334. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
335. [test_process_roles](modules/test_process_roles.md)
336. [test_profile_capacity](modules/test_profile_capacity.md)
337. [test_planning_read_models](modules/test_planning_read_models.md)
338. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
339. [test_project_working_timezone](modules/test_project_working_timezone.md)
340. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
341. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
342. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
343. [test_saved_view_service](modules/test_saved_view_service.md)
344. [test_settings_read_access](modules/test_settings_read_access.md)
345. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
346. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
347. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
348. [test_task_domain](modules/test_task_domain.md)
349. [test_delivery_metrics](modules/test_delivery_metrics.md)
350. [test_human_work_queries](modules/test_human_work_queries.md)
351. [test_task_discussion](modules/test_task_discussion.md)
352. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
353. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
354. [test_task_pagination](modules/test_task_pagination.md)
355. [test_time_entries](modules/test_time_entries.md)
356. [test_time_reports](modules/test_time_reports.md)
357. [test_work_correctness](modules/test_work_correctness.md)
358. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
359. [eslint.config](modules/eslint.config.md)
360. [postcss.config](modules/postcss.config.md)
361. [check-bundle-budget](modules/check-bundle-budget.md)
362. [check-query-feedback](modules/check-query-feedback.md)
363. [Button](modules/Button.md)
364. [Button.test](modules/Button.test.md)
365. [Checkbox](modules/Checkbox.md)
366. [CollapsibleSection](modules/CollapsibleSection.md)
367. [Input](modules/Input.md)
368. [Input.test](modules/Input.test.md)
369. [dialogLayer](modules/dialogLayer.md)
370. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
371. [Modal](modules/Modal.md)
372. [ConfirmDialog](modules/ConfirmDialog.md)
373. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
374. [useConfirmDialog](modules/useConfirmDialog.md)
375. [LiveWindowStatus](modules/LiveWindowStatus.md)
376. [WorkFreshness](modules/WorkFreshness.md)
377. [toast](modules/toast.md)
378. [ToastProvider](modules/ToastProvider.md)
379. [ToastProvider.test](modules/ToastProvider.test.md)
380. [LabelChip](modules/LabelChip.md)
381. [Breadcrumbs](modules/Breadcrumbs.md)
382. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
383. [commandMenuEvents](modules/commandMenuEvents.md)
384. [AccessKeysSummary](modules/AccessKeysSummary.md)
385. [AgentTeamManifestPreview](modules/AgentTeamManifestPreview.md)
386. [ConstraintsPanel](modules/ConstraintsPanel.md)
387. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
388. [SettingsUnsavedBar](modules/SettingsUnsavedBar.md)
389. [WithheldValuesNote](modules/WithheldValuesNote.md)
390. [claimTime](modules/claimTime.md)
391. [SortableTaskItem](modules/SortableTaskItem.md)
392. [taskDraftStorage](modules/taskDraftStorage.md)
393. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
394. [useDraftDismissal](modules/useDraftDismissal.md)
395. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
396. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
397. [InlineEmptyState](modules/InlineEmptyState.md)
398. [MasterProgress](modules/MasterProgress.md)
399. [MasterProgress.test](modules/MasterProgress.test.md)
400. [OverflowMenu](modules/OverflowMenu.md)
401. [PageLayout](modules/PageLayout.md)
402. [SectionCard](modules/SectionCard.md)
403. [SlideOverDrawer](modules/SlideOverDrawer.md)
404. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
405. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
406. [StickyRail](modules/StickyRail.md)
407. [index](modules/index.md)
408. [tone](modules/tone.md)
409. [projectStatusStyles](modules/projectStatusStyles.md)
410. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
411. [Pill](modules/Pill.md)
412. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
413. [tone.test](modules/tone.test.md)
414. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
415. [manifestLocations](modules/manifestLocations.md)
416. [manifestLocations.test](modules/manifestLocations.test.md)
417. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
418. [AgentTeamStepList](modules/AgentTeamStepList.md)
419. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
420. [statusScopes](modules/statusScopes.md)
421. [statusScopes.test](modules/statusScopes.test.md)
422. [identityContext](modules/identityContext.md)
423. [mutationFeedback](modules/mutationFeedback.md)
424. [attentionRanking](modules/attentionRanking.md)
425. [attentionRanking.test](modules/attentionRanking.test.md)
426. [overviewTaskThread](modules/overviewTaskThread.md)
427. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
428. [planningReturn](modules/planningReturn.md)
429. [PlanReturnBar](modules/PlanReturnBar.md)
430. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
431. [planningTaskIssues](modules/planningTaskIssues.md)
432. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
433. [useLiveWindow](modules/useLiveWindow.md)
434. [workQueryFreshness](modules/workQueryFreshness.md)
435. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
436. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
437. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
438. [pagination](modules/pagination.md)
439. [plan.ru](modules/plan.ru.md)
440. [planningInputMessages](modules/planningInputMessages.md)
441. [teamwork.en](modules/teamwork.en.md)
442. [teamwork.ru](modules/teamwork.ru.md)
443. [timeEntries](modules/timeEntries.md)
444. [resources.en](modules/resources.en.md)
445. [i18n](modules/i18n.md)
446. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
447. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
448. [dateLocale](modules/dateLocale.md)
449. [InteractiveCalendar](modules/InteractiveCalendar.md)
450. [resources.ru](modules/resources.ru.md)
451. [i18n.test](modules/i18n.test.md)
452. [schedulingDisplay](modules/schedulingDisplay.md)
453. [seedDisplay](modules/seedDisplay.md)
454. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
455. [routeModules](modules/routeModules.md)
456. [DocumentMetadata](modules/DocumentMetadata.md)
457. [workspaces](modules/workspaces.md)
458. [helpContexts](modules/helpContexts.md)
459. [workspaces.test](modules/workspaces.test.md)
460. [LandingPage](modules/LandingPage.md)
461. [NotFoundPage](modules/NotFoundPage.md)
462. [healthService](modules/healthService.md)
463. [SystemHealthPanel](modules/SystemHealthPanel.md)
464. [iterationStore](modules/iterationStore.md)
465. [iterationStore.test](modules/iterationStore.test.md)
466. [themeStore](modules/themeStore.md)
467. [colorRoles.test](modules/colorRoles.test.md)
468. [planning-masters.test](modules/planning-masters.test.md)
469. [accessibilityInvariants](modules/accessibilityInvariants.md)
470. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
471. [modelAwareRouting](modules/modelAwareRouting.md)
472. [renderWithProviders](modules/renderWithProviders.md)
473. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
474. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
475. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
476. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
477. [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md)
478. [OverflowMenu.test](modules/OverflowMenu.test.md)
479. [renderWithProviders.test](modules/renderWithProviders.test.md)
480. [setup](modules/setup.md)
481. [types_agent](modules/types_agent.md)
482. [types_calendar](modules/types_calendar.md)
483. [deliveryMetrics](modules/deliveryMetrics.md)
484. [emailSettings](modules/emailSettings.md)
485. [executionUsage](modules/executionUsage.md)
486. [types_gantt](modules/types_gantt.md)
487. [types_github](modules/types_github.md)
488. [types_iteration](modules/types_iteration.md)
489. [types_label](modules/types_label.md)
490. [outboundWebhook](modules/outboundWebhook.md)
491. [types_project](modules/types_project.md)
492. [types_release](modules/types_release.md)
493. [requestSource](modules/requestSource.md)
494. [savedView](modules/savedView.md)
495. [schedulingRules](modules/schedulingRules.md)
496. [EffortModifierCard](modules/EffortModifierCard.md)
497. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
498. [SchedulingPassCard](modules/SchedulingPassCard.md)
499. [systemSettings](modules/systemSettings.md)
500. [types_task](modules/types_task.md)
501. [types_team](modules/types_team.md)
502. [types_template](modules/types_template.md)
503. [types_triage](modules/types_triage.md)
504. [workMetrics](modules/workMetrics.md)
505. [agentAccess](modules/agentAccess.md)
506. [useAgentAccess](modules/useAgentAccess.md)
507. [apiError](modules/apiError.md)
508. [QueryState](modules/QueryState.md)
509. [taskEditorContract](modules/taskEditorContract.md)
510. [TaskBriefEditor](modules/TaskBriefEditor.md)
511. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
512. [MutationSuccessFeedback](modules/MutationSuccessFeedback.md)
513. [mutationFeedback.test](modules/mutationFeedback.test.md)
514. [adminAccess](modules/adminAccess.md)
515. [useAdminAccess](modules/useAdminAccess.md)
516. [api](modules/api.md)
517. [identityService](modules/identityService.md)
518. [NativeConnectionPage](modules/NativeConnectionPage.md)
519. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
520. [agentService](modules/agentService.md)
521. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
522. [agentService.test](modules/agentService.test.md)
523. [deliveryMetricsService](modules/deliveryMetricsService.md)
524. [discussionService](modules/discussionService.md)
525. [TaskDiscussion](modules/TaskDiscussion.md)
526. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
527. [emailSettingsService](modules/emailSettingsService.md)
528. [executionUsageService](modules/executionUsageService.md)
529. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
530. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
531. [ganttService](modules/ganttService.md)
532. [githubService](modules/githubService.md)
533. [labelService](modules/labelService.md)
534. [LabelSelector](modules/LabelSelector.md)
535. [outboundWebhookService](modules/outboundWebhookService.md)
536. [planShareService](modules/planShareService.md)
537. [planningInputService](modules/planningInputService.md)
538. [usePlanningObservation](modules/usePlanningObservation.md)
539. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
540. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
541. [calendarService](modules/calendarService.md)
542. [PersonCapacity](modules/PersonCapacity.md)
543. [PersonCapacity.test](modules/PersonCapacity.test.md)
544. [exportService](modules/exportService.md)
545. [IterationImportDialog](modules/IterationImportDialog.md)
546. [iterationService](modules/iterationService.md)
547. [IterationSelector](modules/IterationSelector.md)
548. [planningInputService.test](modules/planningInputService.test.md)
549. [projectService](modules/projectService.md)
550. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
551. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
552. [releaseService](modules/releaseService.md)
553. [ReleaseForm](modules/ReleaseForm.md)
554. [requestSourceService](modules/requestSourceService.md)
555. [savedViewService](modules/savedViewService.md)
556. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
557. [schedulingRulesService](modules/schedulingRulesService.md)
558. [AdminAccessPanel](modules/AdminAccessPanel.md)
559. [AdminAccessGate](modules/AdminAccessGate.md)
560. [AdminAccessGate.test](modules/AdminAccessGate.test.md)
561. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
562. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
563. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
564. [sessionService](modules/sessionService.md)
565. [snapshotService](modules/snapshotService.md)
566. [snapshotVersions.test](modules/snapshotVersions.test.md)
567. [systemSettingsService](modules/systemSettingsService.md)
568. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
569. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
570. [taskService](modules/taskService.md)
571. [DeliveryDependencies](modules/DeliveryDependencies.md)
572. [ImportTasksModal](modules/ImportTasksModal.md)
573. [MetricCount](modules/MetricCount.md)
574. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
575. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
576. [TaskContextSummary](modules/TaskContextSummary.md)
577. [TaskDependencySelector](modules/TaskDependencySelector.md)
578. [TaskReviewer](modules/TaskReviewer.md)
579. [TaskSearch](modules/TaskSearch.md)
580. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
581. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
582. [TaskWorkPanel](modules/TaskWorkPanel.md)
583. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
584. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
585. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
586. [teamService](modules/teamService.md)
587. [GanttBarInputs](modules/GanttBarInputs.md)
588. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
589. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
590. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
591. [ImportTeamModal](modules/ImportTeamModal.md)
592. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
593. [TeamForm](modules/TeamForm.md)
594. [TeamForm.test](modules/TeamForm.test.md)
595. [TeamProfileManager](modules/TeamProfileManager.md)
596. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
597. [VacationCsvImport](modules/VacationCsvImport.md)
598. [LocalProfilePicker](modules/LocalProfilePicker.md)
599. [CalendarPage](modules/CalendarPage.md)
600. [CalendarPage.test](modules/CalendarPage.test.md)
601. [templateService](modules/templateService.md)
602. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
603. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
604. [timeEntryService](modules/timeEntryService.md)
605. [useTimeEntries](modules/useTimeEntries.md)
606. [timeEntryService.test](modules/timeEntryService.test.md)
607. [triageService](modules/triageService.md)
608. [QuickCapture](modules/QuickCapture.md)
609. [QuickCapture.test](modules/QuickCapture.test.md)
610. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
611. [copyText](modules/copyText.md)
612. [focusLifecycle](modules/focusLifecycle.md)
613. [focusLifecycle.test](modules/focusLifecycle.test.md)
614. [formatDate](modules/formatDate.md)
615. [TaskStatusFlow](modules/TaskStatusFlow.md)
616. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
617. [IterationForm](modules/IterationForm.md)
618. [IterationForm.test](modules/IterationForm.test.md)
619. [NotificationsPanel](modules/NotificationsPanel.md)
620. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
621. [StatusChangeControl](modules/StatusChangeControl.md)
622. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
623. [TimeEntriesReport](modules/TimeEntriesReport.md)
624. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
625. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
626. [VacationManager](modules/VacationManager.md)
627. [planningMasters_masters](modules/planningMasters_masters.md)
628. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
629. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
630. [SidebarIterationCard](modules/SidebarIterationCard.md)
631. [AppSidebar](modules/AppSidebar.md)
632. [AppSidebar.test](modules/AppSidebar.test.md)
633. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
634. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
635. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
636. [usePlanningReadiness](modules/usePlanningReadiness.md)
637. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
638. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
639. [IdentityProvider](modules/IdentityProvider.md)
640. [UserSessionBadge](modules/UserSessionBadge.md)
641. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
642. [IdentityProvider.test](modules/IdentityProvider.test.md)
643. [useLiveWindow.test](modules/useLiveWindow.test.md)
644. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
645. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
646. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
647. [PlanMasterPage](modules/PlanMasterPage.md)
648. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
649. [PlanPage](modules/PlanPage.md)
650. [PlanPage.test](modules/PlanPage.test.md)
651. [PlanSharePage](modules/PlanSharePage.md)
652. [PlanSharePage.test](modules/PlanSharePage.test.md)
653. [graphLimitError](modules/graphLimitError.md)
654. [modelRouting](modules/modelRouting.md)
655. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
656. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
657. [modelRouting.test](modules/modelRouting.test.md)
658. [protectedQueries](modules/protectedQueries.md)
659. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
660. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
661. [AgentAccessPanel](modules/AgentAccessPanel.md)
662. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
663. [AgentModelAdministration](modules/AgentModelAdministration.md)
664. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
665. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
666. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
667. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
668. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
669. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
670. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
671. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
672. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
673. [AgentPipelinePage](modules/AgentPipelinePage.md)
674. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
675. [safeUrl](modules/safeUrl.md)
676. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
677. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
678. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
679. [TaskReadView](modules/TaskReadView.md)
680. [TaskReadView.test](modules/TaskReadView.test.md)
681. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
682. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
683. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
684. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
685. [CommandMenu](modules/CommandMenu.md)
686. [CommandMenu.test](modules/CommandMenu.test.md)
687. [ContextHelp](modules/ContextHelp.md)
688. [AppTopNav](modules/AppTopNav.md)
689. [AppShell](modules/AppShell.md)
690. [App](modules/App.md)
691. [AppShell.test](modules/AppShell.test.md)
692. [AppTopNav.test](modules/AppTopNav.test.md)
693. [ContextHelp.test](modules/ContextHelp.test.md)
694. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
695. [src_main](modules/src_main.md)
696. [SettingsPage](modules/SettingsPage.md)
697. [SettingsPage.test](modules/SettingsPage.test.md)
698. [taskFilterDefaults](modules/taskFilterDefaults.md)
699. [TaskFiltersBar](modules/TaskFiltersBar.md)
700. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
701. [taskViewState](modules/taskViewState.md)
702. [savedViewState](modules/savedViewState.md)
703. [SavedViewsControl](modules/SavedViewsControl.md)
704. [savedViewState.test](modules/savedViewState.test.md)
705. [taskFilters](modules/taskFilters.md)
706. [taskFilters.test](modules/taskFilters.test.md)
707. [teamMemberLabels](modules/teamMemberLabels.md)
708. [InitiativeForm](modules/InitiativeForm.md)
709. [RoadmapPage](modules/RoadmapPage.md)
710. [RoadmapPage.test](modules/RoadmapPage.test.md)
711. [templateDefaults](modules/templateDefaults.md)
712. [ProjectForm](modules/ProjectForm.md)
713. [ProjectForm.test](modules/ProjectForm.test.md)
714. [TaskForm](modules/TaskForm.md)
715. [TaskEditModal](modules/TaskEditModal.md)
716. [GanttChart](modules/GanttChart.md)
717. [GanttChart.test](modules/GanttChart.test.md)
718. [GuardedTaskModal](modules/GuardedTaskModal.md)
719. [BacklogPanel](modules/BacklogPanel.md)
720. [CurrentTaskModal.test](modules/CurrentTaskModal.test.md)
721. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
722. [ProjectTaskTree](modules/ProjectTaskTree.md)
723. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
724. [TaskForm.test](modules/TaskForm.test.md)
725. [GanttPage](modules/GanttPage.md)
726. [GanttPage.test](modules/GanttPage.test.md)
727. [MyWorkPage](modules/MyWorkPage.md)
728. [MyWorkPage.test](modules/MyWorkPage.test.md)
729. [TriagePage](modules/TriagePage.md)
730. [visibleWork](modules/visibleWork.md)
731. [TaskList](modules/TaskList.md)
732. [TaskList.test](modules/TaskList.test.md)
733. [visibleWork.test](modules/visibleWork.test.md)
734. [workNumbers](modules/workNumbers.md)
735. [OnTrackSummary](modules/OnTrackSummary.md)
736. [StatusDistribution](modules/StatusDistribution.md)
737. [IterationOutlook.test](modules/IterationOutlook.test.md)
738. [IterationCapacityLine](modules/IterationCapacityLine.md)
739. [IterationList](modules/IterationList.md)
740. [IterationList.test](modules/IterationList.test.md)
741. [KanbanCard](modules/KanbanCard.md)
742. [KanbanColumn](modules/KanbanColumn.md)
743. [KanbanBoard](modules/KanbanBoard.md)
744. [KanbanBoard.test](modules/KanbanBoard.test.md)
745. [KanbanColumn.test](modules/KanbanColumn.test.md)
746. [WorkMetricsLine](modules/WorkMetricsLine.md)
747. [MetricCount.test](modules/MetricCount.test.md)
748. [TeamList](modules/TeamList.md)
749. [TeamList.test](modules/TeamList.test.md)
750. [AnalyticsPage](modules/AnalyticsPage.md)
751. [IterationsPage](modules/IterationsPage.md)
752. [OverviewPage](modules/OverviewPage.md)
753. [OverviewPage.test](modules/OverviewPage.test.md)
754. [ProjectDetailPage](modules/ProjectDetailPage.md)
755. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
756. [ProjectsPage](modules/ProjectsPage.md)
757. [ProjectsPage.test](modules/ProjectsPage.test.md)
758. [TasksPage](modules/TasksPage.md)
759. [TasksPage.test](modules/TasksPage.test.md)
760. [TeamPage](modules/TeamPage.md)
761. [tailwind.config](modules/tailwind.config.md)
762. [check-tailwind-classes](modules/check-tailwind-classes.md)
763. [vite.config](modules/vite.config.md)
764. [vitest.config](modules/vitest.config.md)
765. [create_agent_actor](modules/create_agent_actor.md)
766. [generate_workchord_keys](modules/generate_workchord_keys.md)
767. [setup_agent_team](modules/setup_agent_team.md)
768. [build_agent_skills](modules/build_agent_skills.md)
769. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
770. [android_qualification](modules/android_qualification.md)
771. [android_web_peer](modules/android_web_peer.md)
772. [apt_runtime](modules/apt_runtime.md)
773. [browser_performance](modules/browser_performance.md)
774. [browser_planning_inputs](modules/browser_planning_inputs.md)
775. [browser_worker](modules/browser_worker.md)
776. [browser_managed_work](modules/browser_managed_work.md)
777. [browser_write_readback](modules/browser_write_readback.md)
778. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
779. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
780. [ci_runtime](modules/ci_runtime.md)
781. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
782. [postgres_runtime](modules/postgres_runtime.md)
783. [run_android_checks](modules/run_android_checks.md)
784. [run_disposable_checks](modules/run_disposable_checks.md)
785. [serve_disposable_api](modules/serve_disposable_api.md)
786. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
787. [test_apt_runtime](modules/test_apt_runtime.md)
788. [test_ci_runtime](modules/test_ci_runtime.md)
789. [test_native_runtimes](modules/test_native_runtimes.md)
790. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
791. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
792. [generate_client_contract](modules/generate_client_contract.md)
793. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
794. [load_common](modules/load_common.md)
795. [collect](modules/collect.md)
796. [result](modules/result.md)
797. [compare](modules/compare.md)
798. [finalize](modules/finalize.md)
799. [qualify](modules/qualify.md)
800. [resilience](modules/resilience.md)
801. [run](modules/run.md)
802. [seal](modules/seal.md)
803. [seed](modules/seed.md)
804. [source_binding](modules/source_binding.md)
805. [local_baseline](modules/local_baseline.md)
806. [service_worksets](modules/service_worksets.md)
807. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
808. [isolated_rehearsal](modules/isolated_rehearsal.md)

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
| [settings_read](modules/settings_read.md) | `READABLE_SETTINGS_PATHS = frozenset` |
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
| [IterationOutlook.test](modules/IterationOutlook.test.md) | `mock`, `describe` |
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
| [IterationList.test](modules/IterationList.test.md) | `iterations = hoisted`, `mock`, `describe` |
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
| [ProjectForm.test](modules/ProjectForm.test.md) | `projects = hoisted`, `mock`, `mock`, `mock`, `planning = hoisted`, `mock`, `describe` |
| [ProjectForm](modules/ProjectForm.md) | `projectStatusValues = map`, `projectHealthValues = map` |
| [ProjectTaskTree](modules/ProjectTaskTree.md) | `t = bind` |
| [TimeEntriesReport.test](modules/TimeEntriesReport.test.md) | `capability = hoisted`, `mock`, `it` |
| [projectStatusStyles.test](modules/projectStatusStyles.test.md) | `describe` |
| [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md) | `requestSourceServiceMock = hoisted`, `mock`, `describe` |
| [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md) | `t = bind` |
| [AdminAccessGate.test](modules/AdminAccessGate.test.md) | `mock`, `describe` |
| [AdminAccessPanel.test](modules/AdminAccessPanel.test.md) | `adminAccessHookMock = hoisted`, `adminAccessStorageMock = hoisted`, `schedulingRulesMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [AgentAccessPanel.test](modules/AgentAccessPanel.test.md) | `agentAccessHookMock = hoisted`, `agentAccessStorageMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [AgentModelAdministration.test](modules/AgentModelAdministration.test.md) | `agentAccessMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [AgentTeamStepList](modules/AgentTeamStepList.md) | `MANIFEST_STEPS = Set` |
| [EffortModifierCard.test](modules/EffortModifierCard.test.md) | `describe` |
| [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md) | `adminAccessMock = hoisted`, `emailSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md) | `githubServiceMock = hoisted`, `mock`, `describe` |
| [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md) | `adminAccessMock = hoisted`, `outboundWebhookServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md) | `adminAccessMock = hoisted`, `systemSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md) | `adminAccessMock = hoisted`, `schedulingRulesServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [SchedulingRulesSettings](modules/SchedulingRulesSettings.md) | `SETTINGS_ROW_ID = Symbol` |
| [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md) | `health = hoisted`, `mock`, `describe` |
| [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md) | `labelServiceMock = hoisted`, `templateServiceMock = hoisted`, `toastMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [CurrentTaskModal.test](modules/CurrentTaskModal.test.md) | `service = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it` |
| [KanbanBoard.test](modules/KanbanBoard.test.md) | `dragState = hoisted`, `taskServiceMock = hoisted`, `teamServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [KanbanColumn.test](modules/KanbanColumn.test.md) | `mock`, `mock`, `describe`, `describe` |
| [MetricCount.test](modules/MetricCount.test.md) | `service = hoisted`, `mock`, `describe` |
| [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md) | `lookup = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it` |
| [PersonCapacity.test](modules/PersonCapacity.test.md) | `api = hoisted`, `mock`, `beforeEach`, `it` |
| [QuickCapture.test](modules/QuickCapture.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it` |
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
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `it`, `it`, `it`, `describe` |
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
| [TeamList.test](modules/TeamList.test.md) | `team = hoisted`, `mock`, `iterations = hoisted`, `mock`, `describe` |
| [TeamProfileManager.test](modules/TeamProfileManager.test.md) | `teamServiceMock = hoisted`, `planningMock = hoisted`, `mock`, `mock`, `describe`, `describe` |
| [MasterProgress.test](modules/MasterProgress.test.md) | `describe` |
| [OverflowMenu.test](modules/OverflowMenu.test.md) | `describe` |
| [tone.test](modules/tone.test.md) | `describe` |
| [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md) | `SECRET_FIELDS = Set` |
| [manifestLocations.test](modules/manifestLocations.test.md) | `describe` |
| [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md) | `describe` |
| [agentTeamSetup_masters](modules/agentTeamSetup_masters.md) | `AGENT_TEAM_STEP_DEFINITIONS = map` |
| [statusScopes.test](modules/statusScopes.test.md) | `describe` |
| [IdentityProvider.test](modules/IdentityProvider.test.md) | `service = hoisted`, `mock`, `describe` |
| [identityContext](modules/identityContext.md) | `IdentityContext = createContext` |
| [mutationFeedback.test](modules/mutationFeedback.test.md) | `describe` |
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
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `useKeylessReaderMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | `HUMAN_GATED_STAGES = Set`, `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set`, `TASK_STATUSES = Set` |
| [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe`, `describe` |
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
| [colorRoles.test](modules/colorRoles.test.md) | `css = readFileSync`, `describe` |
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
