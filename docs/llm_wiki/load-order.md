# Load order

Topological module load / startup order and import-time side effects.

## Load order

<!-- Dependency-first order: each module loads after the internal modules it imports. -->

TypeScript binding imports are possible startup constraints: their emission depends on compiler settings. Guaranteed-erased type imports are excluded. This is a static projection, not an emitted-JavaScript execution trace.

1. [agent_contract](modules/agent_contract.md)
2. [agent_key_file](modules/agent_key_file.md)
3. [autonomy_canonical](modules/autonomy_canonical.md)
4. [autonomy___init__](modules/autonomy___init__.md)
5. [loader](modules/loader.md)
6. [postgresql___init__](modules/postgresql___init__.md)
7. [topology](modules/topology.md)
8. [execution_mode](modules/execution_mode.md)
9. [signing](modules/signing.md)
10. [charter](modules/charter.md)
11. [contracts___init__](modules/contracts___init__.md)
12. [evidence](modules/evidence.md)
13. [leases](modules/leases.md)
14. [orchestration](modules/orchestration.md)
15. [preflight](modules/preflight.md)
16. [providers](modules/providers.md)
17. [status](modules/status.md)
18. [handoff](modules/handoff.md)
19. [build_identity](modules/build_identity.md)
20. [autonomy_server_acceptance](modules/autonomy_server_acceptance.md)
21. [acceptance_artifacts](modules/acceptance_artifacts.md)
22. [agent_preflight](modules/agent_preflight.md)
23. [cli_server_acceptance](modules/cli_server_acceptance.md)
24. [commands](modules/commands.md)
25. [database_config](modules/database_config.md)
26. [config](modules/config.md)
27. [authority](modules/authority.md)
28. [allocation_identity](modules/allocation_identity.md)
29. [database_migration_manifest](modules/database_migration_manifest.md)
30. [database_migration_cutover](modules/database_migration_cutover.md)
31. [cli_cutover](modules/cli_cutover.md)
32. [database_migration_closeout](modules/database_migration_closeout.md)
33. [cli_closeout](modules/cli_closeout.md)
34. [project_identity](modules/project_identity.md)
35. [20260928_0001_initial_schema](modules/20260928_0001_initial_schema.md)
36. [20260930_0002_profile_capacity](modules/20260930_0002_profile_capacity.md)
37. [20260930_0003_delivery_dependencies](modules/20260930_0003_delivery_dependencies.md)
38. [20260930_0004_discussion](modules/20260930_0004_discussion.md)
39. [20261003_0005_native_connections](modules/20261003_0005_native_connections.md)
40. [20261004_0006_delivery_observations](modules/20261004_0006_delivery_observations.md)
41. [20261004_0007_execution_usage](modules/20261004_0007_execution_usage.md)
42. [20261007_0008_time_entries](modules/20261007_0008_time_entries.md)
43. [20261008_0009_project_identity](modules/20261008_0009_project_identity.md)
44. [20261009_0010_allocation_identity](modules/20261009_0010_allocation_identity.md)
45. [20261009_0011_profile_identity](modules/20261009_0011_profile_identity.md)
46. [20261111_0012_session_work_profile](modules/20261111_0012_session_work_profile.md)
47. [20261111_0013_local_comment_authors](modules/20261111_0013_local_comment_authors.md)
48. [20261115_0014_observer_sessions](modules/20261115_0014_observer_sessions.md)
49. [20261116_0015_agdash_link_provider](modules/20261116_0015_agdash_link_provider.md)
50. [20261116_0016_runtime_observations](modules/20261116_0016_runtime_observations.md)
51. [20261116_0017_run_harness_session](modules/20261116_0017_run_harness_session.md)
52. [query_limits](modules/query_limits.md)
53. [runtime_telemetry](modules/runtime_telemetry.md)
54. [database_runtime](modules/database_runtime.md)
55. [maintenance](modules/maintenance.md)
56. [mutation_versions](modules/mutation_versions.md)
57. [schemas_agent_connect](modules/schemas_agent_connect.md)
58. [schemas_agent_planning](modules/schemas_agent_planning.md)
59. [agent_skill_bundle](modules/agent_skill_bundle.md)
60. [agent_team_setup](modules/agent_team_setup.md)
61. [schemas_autonomy](modules/schemas_autonomy.md)
62. [schemas_common](modules/schemas_common.md)
63. [delivery_metrics](modules/delivery_metrics.md)
64. [schemas_execution_usage](modules/schemas_execution_usage.md)
65. [schemas_github](modules/schemas_github.md)
66. [schemas_intake](modules/schemas_intake.md)
67. [schemas_label](modules/schemas_label.md)
68. [schemas_plan_share](modules/schemas_plan_share.md)
69. [planning_inputs](modules/planning_inputs.md)
70. [schemas_calendar](modules/schemas_calendar.md)
71. [schemas_saved_view](modules/schemas_saved_view.md)
72. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
73. [schemas_session](modules/schemas_session.md)
74. [snapshot](modules/snapshot.md)
75. [schemas_system_settings](modules/schemas_system_settings.md)
76. [schemas_email_settings](modules/schemas_email_settings.md)
77. [schemas_task_brief](modules/schemas_task_brief.md)
78. [schemas_llm](modules/schemas_llm.md)
79. [schemas_task_domain](modules/schemas_task_domain.md)
80. [schemas_team](modules/schemas_team.md)
81. [schemas_template](modules/schemas_template.md)
82. [schemas_time_entry](modules/schemas_time_entry.md)
83. [time_report](modules/time_report.md)
84. [schemas_work_metrics](modules/schemas_work_metrics.md)
85. [schemas_iteration](modules/schemas_iteration.md)
86. [schemas_project](modules/schemas_project.md)
87. [schemas_release](modules/schemas_release.md)
88. [security](modules/security.md)
89. [server_features](modules/server_features.md)
90. [agent_routing_policy](modules/agent_routing_policy.md)
91. [agent_routing](modules/agent_routing.md)
92. [agent_routing_rollout](modules/agent_routing_rollout.md)
93. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
94. [routers_agent_connect](modules/routers_agent_connect.md)
95. [agent_team_credentials](modules/agent_team_credentials.md)
96. [bounded_scope_reads](modules/bounded_scope_reads.md)
97. [language_service](modules/language_service.md)
98. [plan_checkpoints](modules/plan_checkpoints.md)
99. [planning_input_context](modules/planning_input_context.md)
100. [planning_issues](modules/planning_issues.md)
101. [scheduling_rules_service](modules/scheduling_rules_service.md)
102. [upgrade_service](modules/upgrade_service.md)
103. [upgrade](modules/upgrade.md)
104. [settings_read](modules/settings_read.md)
105. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
106. [sql_semantics](modules/sql_semantics.md)
107. [exceptions](modules/exceptions.md)
108. [text_similarity](modules/text_similarity.md)
109. [time](modules/time.md)
110. [observability](modules/observability.md)
111. [app_database](modules/app_database.md)
112. [models_agent](modules/models_agent.md)
113. [models_autonomy](modules/models_autonomy.md)
114. [models_calendar](modules/models_calendar.md)
115. [models_capacity](modules/models_capacity.md)
116. [models_database_migration](modules/models_database_migration.md)
117. [delivery_dependency](modules/delivery_dependency.md)
118. [models_discussion](modules/models_discussion.md)
119. [models_execution_usage](modules/models_execution_usage.md)
120. [models_external_link](modules/models_external_link.md)
121. [models_github](modules/models_github.md)
122. [models_identity](modules/models_identity.md)
123. [models_iteration](modules/models_iteration.md)
124. [models_label](modules/models_label.md)
125. [native_connection](modules/native_connection.md)
126. [models_outbound_webhook](modules/models_outbound_webhook.md)
127. [models_plan_share](modules/models_plan_share.md)
128. [models_release](modules/models_release.md)
129. [models_project](modules/models_project.md)
130. [models_request_source](modules/models_request_source.md)
131. [models_runtime_observation](modules/models_runtime_observation.md)
132. [models_saved_view](modules/models_saved_view.md)
133. [models_system_settings](modules/models_system_settings.md)
134. [models_task](modules/models_task.md)
135. [recovery](modules/recovery.md)
136. [models_task_brief](modules/models_task_brief.md)
137. [delivery_observation](modules/delivery_observation.md)
138. [task_status_log](modules/task_status_log.md)
139. [team_member](modules/team_member.md)
140. [models_template](modules/models_template.md)
141. [models_time_entry](modules/models_time_entry.md)
142. [models_triage](modules/models_triage.md)
143. [user_session](modules/user_session.md)
144. [models___init__](modules/models___init__.md)
145. [catalog](modules/catalog.md)
146. [database_migration_canonical](modules/database_migration_canonical.md)
147. [source](modules/source.md)
148. [transfer](modules/transfer.md)
149. [cli_database_migration](modules/cli_database_migration.md)
150. [database_migration___init__](modules/database_migration___init__.md)
151. [migrations_env](modules/migrations_env.md)
152. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
153. [calendar_service](modules/calendar_service.md)
154. [calendars](modules/calendars.md)
155. [capacity_service](modules/capacity_service.md)
156. [routers_capacity](modules/routers_capacity.md)
157. [delivery_dependency_service](modules/delivery_dependency_service.md)
158. [delivery_metrics_service](modules/delivery_metrics_service.md)
159. [discussion_service](modules/discussion_service.md)
160. [identity_service](modules/identity_service.md)
161. [import_planning_service](modules/import_planning_service.md)
162. [iteration_service](modules/iteration_service.md)
163. [iterations](modules/iterations.md)
164. [label_service](modules/label_service.md)
165. [labels](modules/labels.md)
166. [native_session_service](modules/native_session_service.md)
167. [saved_view_service](modules/saved_view_service.md)
168. [session_service](modules/session_service.md)
169. [http_authority](modules/http_authority.md)
170. [routers_identity](modules/routers_identity.md)
171. [saved_views](modules/saved_views.md)
172. [routers_session](modules/routers_session.md)
173. [task_brief_service](modules/task_brief_service.md)
174. [task_context_revision_service](modules/task_context_revision_service.md)
175. [task_domain_service](modules/task_domain_service.md)
176. [task_hierarchy_service](modules/task_hierarchy_service.md)
177. [task_recovery_service](modules/task_recovery_service.md)
178. [task_timeline_service](modules/task_timeline_service.md)
179. [team_service](modules/team_service.md)
180. [routers_team](modules/routers_team.md)
181. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
182. [snapshot_service](modules/snapshot_service.md)
183. [plan_share_service](modules/plan_share_service.md)
184. [plan_shares](modules/plan_shares.md)
185. [template_service](modules/template_service.md)
186. [templates](modules/templates.md)
187. [time_entry_service](modules/time_entry_service.md)
188. [time_report_service](modules/time_report_service.md)
189. [services_work_metrics](modules/services_work_metrics.md)
190. [import_parser](modules/import_parser.md)
191. [url_policy](modules/url_policy.md)
192. [schemas_external_link](modules/schemas_external_link.md)
193. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
194. [schemas_request_source](modules/schemas_request_source.md)
195. [schemas_task](modules/schemas_task.md)
196. [schemas_gantt](modules/schemas_gantt.md)
197. [task_detail](modules/task_detail.md)
198. [schemas_triage](modules/schemas_triage.md)
199. [schemas___init__](modules/schemas___init__.md)
200. [schemas_agent](modules/schemas_agent.md)
201. [agent_run_read](modules/agent_run_read.md)
202. [schemas_runtime_observation](modules/schemas_runtime_observation.md)
203. [agent_readiness](modules/agent_readiness.md)
204. [llm_service](modules/llm_service.md)
205. [runtime_observation_service](modules/runtime_observation_service.md)
206. [system_settings_service](modules/system_settings_service.md)
207. [routers_system_settings](modules/routers_system_settings.md)
208. [email_settings_service](modules/email_settings_service.md)
209. [routers_email_settings](modules/routers_email_settings.md)
210. [notification_service](modules/notification_service.md)
211. [outbound_webhook_service](modules/outbound_webhook_service.md)
212. [worker](modules/worker.md)
213. [outbound_webhooks](modules/outbound_webhooks.md)
214. [external_link_service](modules/external_link_service.md)
215. [github_status_service](modules/github_status_service.md)
216. [request_source_service](modules/request_source_service.md)
217. [request_sources](modules/request_sources.md)
218. [project_service](modules/project_service.md)
219. [task_detail_service](modules/task_detail_service.md)
220. [task_import_service](modules/task_import_service.md)
221. [task_service](modules/task_service.md)
222. [export](modules/export.md)
223. [snapshots](modules/snapshots.md)
224. [agent_routing_observability](modules/agent_routing_observability.md)
225. [agent_service](modules/agent_service.md)
226. [agent_skill_bundles](modules/agent_skill_bundles.md)
227. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
228. [agent_routing_service](modules/agent_routing_service.md)
229. [agent_team_setup_service](modules/agent_team_setup_service.md)
230. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
231. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
232. [execution_usage_service](modules/execution_usage_service.md)
233. [routers_task_domain](modules/routers_task_domain.md)
234. [delivery_dependencies](modules/delivery_dependencies.md)
235. [routers_discussion](modules/routers_discussion.md)
236. [time_entries](modules/time_entries.md)
237. [agent_run_read_service](modules/agent_run_read_service.md)
238. [github_status_automation_service](modules/github_status_automation_service.md)
239. [release_service](modules/release_service.md)
240. [projects](modules/projects.md)
241. [scheduler_service](modules/scheduler_service.md)
242. [routers_gantt](modules/routers_gantt.md)
243. [routers_llm](modules/routers_llm.md)
244. [agent_planning_service](modules/agent_planning_service.md)
245. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
246. [tasks](modules/tasks.md)
247. [task_status_service](modules/task_status_service.md)
248. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
249. [triage_service](modules/triage_service.md)
250. [routers_triage](modules/routers_triage.md)
251. [agent_work_service](modules/agent_work_service.md)
252. [mcp_agent_tools](modules/mcp_agent_tools.md)
253. [mcp_server](modules/mcp_server.md)
254. [routers_agent](modules/routers_agent.md)
255. [routers_agent_planning](modules/routers_agent_planning.md)
256. [agent_catalog](modules/agent_catalog.md)
257. [github_webhook_service](modules/github_webhook_service.md)
258. [routers_github](modules/routers_github.md)
259. [web_intake_service](modules/web_intake_service.md)
260. [routers_intake](modules/routers_intake.md)
261. [app_main](modules/app_main.md)
262. [routers___init__](modules/routers___init__.md)
263. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
264. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
265. [test_server_acceptance](modules/test_server_acceptance.md)
266. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
267. [test_work_package_service](modules/test_work_package_service.md)
268. [test_database_configuration](modules/test_database_configuration.md)
269. [test_deployment_topology](modules/test_deployment_topology.md)
270. [test_observability](modules/test_observability.md)
271. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
272. [test_query_boundaries](modules/test_query_boundaries.md)
273. [test_runtime_policy](modules/test_runtime_policy.md)
274. [test_schema_behavior](modules/test_schema_behavior.md)
275. [test_cutover_evidence](modules/test_cutover_evidence.md)
276. [test_documentation_boundary](modules/test_documentation_boundary.md)
277. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
278. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
279. [test_source_preflight](modules/test_source_preflight.md)
280. [test_transfer_catalog](modules/test_transfer_catalog.md)
281. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
282. [0001_wave0_probe](modules/0001_wave0_probe.md)
283. [test_allocation_identity](modules/test_allocation_identity.md)
284. [test_initial_schema](modules/test_initial_schema.md)
285. [test_profile_identity](modules/test_profile_identity.md)
286. [test_android_cleanup](modules/test_android_cleanup.md)
287. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
288. [test_load_tooling](modules/test_load_tooling.md)
289. [test_local_baseline](modules/test_local_baseline.md)
290. [test_routing_evidence](modules/test_routing_evidence.md)
291. [support_database](modules/support_database.md)
292. [delivery](modules/delivery.md)
293. [factories](modules/factories.md)
294. [faults](modules/faults.md)
295. [runtime_peer](modules/runtime_peer.md)
296. [schema](modules/schema.md)
297. [support___init__](modules/support___init__.md)
298. [conftest](modules/conftest.md)
299. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
300. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
301. [test_project_identity](modules/test_project_identity.md)
302. [test_project_identity_scope](modules/test_project_identity_scope.md)
303. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
304. [transactions](modules/transactions.md)
305. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
306. [test_agent_key_delivery](modules/test_agent_key_delivery.md)
307. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
308. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
309. [test_agent_routing_data](modules/test_agent_routing_data.md)
310. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
311. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
312. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
313. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
314. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
315. [test_agent_routing_service](modules/test_agent_routing_service.md)
316. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
317. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
318. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
319. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
320. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
321. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
322. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
323. [test_authority_migrations](modules/test_authority_migrations.md)
324. [test_capacity_contract](modules/test_capacity_contract.md)
325. [test_client_contract](modules/test_client_contract.md)
326. [test_database_harness](modules/test_database_harness.md)
327. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
328. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
329. [test_agent_team_setup](modules/test_agent_team_setup.md)
330. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
331. [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md)
332. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
333. [test_dependency_date_cascade](modules/test_dependency_date_cascade.md)
334. [test_deployment_configuration](modules/test_deployment_configuration.md)
335. [test_effective_deferral](modules/test_effective_deferral.md)
336. [test_execution_usage](modules/test_execution_usage.md)
337. [test_execution_working_dates](modules/test_execution_working_dates.md)
338. [test_harness_session_metadata](modules/test_harness_session_metadata.md)
339. [test_managed_authority](modules/test_managed_authority.md)
340. [test_allocation_recovery](modules/test_allocation_recovery.md)
341. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
342. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
343. [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md)
344. [test_metric_matches](modules/test_metric_matches.md)
345. [test_mobile_contract](modules/test_mobile_contract.md)
346. [test_mutation_versions](modules/test_mutation_versions.md)
347. [test_native_connections](modules/test_native_connections.md)
348. [test_observer_sessions](modules/test_observer_sessions.md)
349. [test_agdash_link_provider](modules/test_agdash_link_provider.md)
350. [test_person_assignment_reads](modules/test_person_assignment_reads.md)
351. [test_person_run_reads](modules/test_person_run_reads.md)
352. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
353. [test_plan_shares](modules/test_plan_shares.md)
354. [test_planning_input_context](modules/test_planning_input_context.md)
355. [test_planning_issues](modules/test_planning_issues.md)
356. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
357. [test_process_roles](modules/test_process_roles.md)
358. [test_profile_capacity](modules/test_profile_capacity.md)
359. [test_planning_read_models](modules/test_planning_read_models.md)
360. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
361. [test_project_working_timezone](modules/test_project_working_timezone.md)
362. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
363. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
364. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
365. [test_runtime_observations](modules/test_runtime_observations.md)
366. [test_saved_view_service](modules/test_saved_view_service.md)
367. [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md)
368. [test_server_features](modules/test_server_features.md)
369. [test_settings_read_access](modules/test_settings_read_access.md)
370. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
371. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
372. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
373. [test_task_domain](modules/test_task_domain.md)
374. [test_delivery_metrics](modules/test_delivery_metrics.md)
375. [test_human_work_queries](modules/test_human_work_queries.md)
376. [test_task_discussion](modules/test_task_discussion.md)
377. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
378. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
379. [test_task_pagination](modules/test_task_pagination.md)
380. [test_team_topology_read](modules/test_team_topology_read.md)
381. [test_time_entries](modules/test_time_entries.md)
382. [test_time_reports](modules/test_time_reports.md)
383. [test_unscheduled_tasks](modules/test_unscheduled_tasks.md)
384. [test_work_correctness](modules/test_work_correctness.md)
385. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
386. [eslint.config](modules/eslint.config.md)
387. [postcss.config](modules/postcss.config.md)
388. [check-bundle-budget](modules/check-bundle-budget.md)
389. [check-query-feedback](modules/check-query-feedback.md)
390. [Button](modules/Button.md)
391. [Button.test](modules/Button.test.md)
392. [Checkbox](modules/Checkbox.md)
393. [CollapsibleSection](modules/CollapsibleSection.md)
394. [DisabledReason](modules/DisabledReason.md)
395. [Input](modules/Input.md)
396. [Input.test](modules/Input.test.md)
397. [Select](modules/Select.md)
398. [Textarea](modules/Textarea.md)
399. [dialogLayer](modules/dialogLayer.md)
400. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
401. [Modal](modules/Modal.md)
402. [ConfirmDialog](modules/ConfirmDialog.md)
403. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
404. [formControlLabels.test](modules/formControlLabels.test.md)
405. [iconButtonTooltips.test](modules/iconButtonTooltips.test.md)
406. [useConfirmDialog](modules/useConfirmDialog.md)
407. [LiveWindowStatus](modules/LiveWindowStatus.md)
408. [WorkFreshness](modules/WorkFreshness.md)
409. [toast](modules/toast.md)
410. [ToastProvider](modules/ToastProvider.md)
411. [ToastProvider.test](modules/ToastProvider.test.md)
412. [UnscheduledTasks](modules/UnscheduledTasks.md)
413. [LabelChip](modules/LabelChip.md)
414. [Breadcrumbs](modules/Breadcrumbs.md)
415. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
416. [commandMenuEvents](modules/commandMenuEvents.md)
417. [AccessKeysSummary](modules/AccessKeysSummary.md)
418. [AgentTeamManifestPreview](modules/AgentTeamManifestPreview.md)
419. [ConstraintsPanel](modules/ConstraintsPanel.md)
420. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
421. [SettingsUnsavedBar](modules/SettingsUnsavedBar.md)
422. [WithheldValuesNote](modules/WithheldValuesNote.md)
423. [claimTime](modules/claimTime.md)
424. [SortableTaskItem](modules/SortableTaskItem.md)
425. [taskDraftStorage](modules/taskDraftStorage.md)
426. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
427. [useDraftDismissal](modules/useDraftDismissal.md)
428. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
429. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
430. [InlineEmptyState](modules/InlineEmptyState.md)
431. [MasterProgress](modules/MasterProgress.md)
432. [MasterProgress.test](modules/MasterProgress.test.md)
433. [OverflowMenu](modules/OverflowMenu.md)
434. [PageLayout](modules/PageLayout.md)
435. [SectionCard](modules/SectionCard.md)
436. [SegmentedControl](modules/SegmentedControl.md)
437. [Select.test](modules/Select.test.md)
438. [SlideOverDrawer](modules/SlideOverDrawer.md)
439. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
440. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
441. [StickyRail](modules/StickyRail.md)
442. [index](modules/index.md)
443. [tone](modules/tone.md)
444. [projectStatusStyles](modules/projectStatusStyles.md)
445. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
446. [Pill](modules/Pill.md)
447. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
448. [tone.test](modules/tone.test.md)
449. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
450. [manifestLocations](modules/manifestLocations.md)
451. [manifestLocations.test](modules/manifestLocations.test.md)
452. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
453. [AgentTeamStepList](modules/AgentTeamStepList.md)
454. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
455. [statusScopes](modules/statusScopes.md)
456. [statusScopes.test](modules/statusScopes.test.md)
457. [identityContext](modules/identityContext.md)
458. [mutationFeedback](modules/mutationFeedback.md)
459. [attentionRanking](modules/attentionRanking.md)
460. [attentionRanking.test](modules/attentionRanking.test.md)
461. [overviewTaskThread](modules/overviewTaskThread.md)
462. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
463. [planningReturn](modules/planningReturn.md)
464. [PlanReturnBar](modules/PlanReturnBar.md)
465. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
466. [planningTaskIssues](modules/planningTaskIssues.md)
467. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
468. [taskTransitions](modules/taskTransitions.md)
469. [taskTransitions.test](modules/taskTransitions.test.md)
470. [useLiveWindow](modules/useLiveWindow.md)
471. [workQueryFreshness](modules/workQueryFreshness.md)
472. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
473. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
474. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
475. [landing.en](modules/landing.en.md)
476. [landing.ru](modules/landing.ru.md)
477. [literals.ru](modules/literals.ru.md)
478. [pagination](modules/pagination.md)
479. [plan.ru](modules/plan.ru.md)
480. [planningInputMessages](modules/planningInputMessages.md)
481. [surfaces.ru](modules/surfaces.ru.md)
482. [teamwork.en](modules/teamwork.en.md)
483. [teamwork.ru](modules/teamwork.ru.md)
484. [timeEntries](modules/timeEntries.md)
485. [resources.en](modules/resources.en.md)
486. [i18n](modules/i18n.md)
487. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
488. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
489. [dateLocale](modules/dateLocale.md)
490. [InteractiveCalendar](modules/InteractiveCalendar.md)
491. [formatsAndWording.test](modules/formatsAndWording.test.md)
492. [resources.ru](modules/resources.ru.md)
493. [i18n.test](modules/i18n.test.md)
494. [schedulingDisplay](modules/schedulingDisplay.md)
495. [seedDisplay](modules/seedDisplay.md)
496. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
497. [routeModules](modules/routeModules.md)
498. [DocumentMetadata](modules/DocumentMetadata.md)
499. [workspaces](modules/workspaces.md)
500. [helpContexts](modules/helpContexts.md)
501. [workspaces.test](modules/workspaces.test.md)
502. [LandingPage](modules/LandingPage.md)
503. [NotFoundPage](modules/NotFoundPage.md)
504. [healthService](modules/healthService.md)
505. [SystemHealthPanel](modules/SystemHealthPanel.md)
506. [iterationStore](modules/iterationStore.md)
507. [iterationStore.test](modules/iterationStore.test.md)
508. [themeStore](modules/themeStore.md)
509. [colorRoles.test](modules/colorRoles.test.md)
510. [planning-masters.test](modules/planning-masters.test.md)
511. [accessibilityInvariants](modules/accessibilityInvariants.md)
512. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
513. [modelAwareRouting](modules/modelAwareRouting.md)
514. [renderWithProviders](modules/renderWithProviders.md)
515. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
516. [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md)
517. [UnscheduledTasks.test](modules/UnscheduledTasks.test.md)
518. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
519. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
520. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
521. [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md)
522. [OverflowMenu.test](modules/OverflowMenu.test.md)
523. [LandingPage.test](modules/LandingPage.test.md)
524. [renderWithProviders.test](modules/renderWithProviders.test.md)
525. [setup](modules/setup.md)
526. [types_agent](modules/types_agent.md)
527. [types_calendar](modules/types_calendar.md)
528. [deliveryMetrics](modules/deliveryMetrics.md)
529. [emailSettings](modules/emailSettings.md)
530. [executionUsage](modules/executionUsage.md)
531. [types_gantt](modules/types_gantt.md)
532. [types_github](modules/types_github.md)
533. [types_iteration](modules/types_iteration.md)
534. [types_label](modules/types_label.md)
535. [outboundWebhook](modules/outboundWebhook.md)
536. [types_project](modules/types_project.md)
537. [types_release](modules/types_release.md)
538. [requestSource](modules/requestSource.md)
539. [savedView](modules/savedView.md)
540. [schedulingRules](modules/schedulingRules.md)
541. [EffortModifierCard](modules/EffortModifierCard.md)
542. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
543. [SchedulingPassCard](modules/SchedulingPassCard.md)
544. [systemSettings](modules/systemSettings.md)
545. [types_task](modules/types_task.md)
546. [types_team](modules/types_team.md)
547. [types_template](modules/types_template.md)
548. [types_triage](modules/types_triage.md)
549. [workMetrics](modules/workMetrics.md)
550. [agentAccess](modules/agentAccess.md)
551. [useAgentAccess](modules/useAgentAccess.md)
552. [apiError](modules/apiError.md)
553. [QueryState](modules/QueryState.md)
554. [taskEditorContract](modules/taskEditorContract.md)
555. [TaskBriefEditor](modules/TaskBriefEditor.md)
556. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
557. [MutationSuccessFeedback](modules/MutationSuccessFeedback.md)
558. [mutationFeedback.test](modules/mutationFeedback.test.md)
559. [adminAccess](modules/adminAccess.md)
560. [useAdminAccess](modules/useAdminAccess.md)
561. [api](modules/api.md)
562. [identityService](modules/identityService.md)
563. [NativeConnectionPage](modules/NativeConnectionPage.md)
564. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
565. [agentService](modules/agentService.md)
566. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
567. [agentService.test](modules/agentService.test.md)
568. [deliveryMetricsService](modules/deliveryMetricsService.md)
569. [discussionService](modules/discussionService.md)
570. [emailSettingsService](modules/emailSettingsService.md)
571. [executionUsageService](modules/executionUsageService.md)
572. [ganttService](modules/ganttService.md)
573. [githubService](modules/githubService.md)
574. [labelService](modules/labelService.md)
575. [LabelSelector](modules/LabelSelector.md)
576. [outboundWebhookService](modules/outboundWebhookService.md)
577. [planShareService](modules/planShareService.md)
578. [planningInputService](modules/planningInputService.md)
579. [usePlanningObservation](modules/usePlanningObservation.md)
580. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
581. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
582. [calendarService](modules/calendarService.md)
583. [PersonCapacity](modules/PersonCapacity.md)
584. [PersonCapacity.test](modules/PersonCapacity.test.md)
585. [exportService](modules/exportService.md)
586. [IterationImportDialog](modules/IterationImportDialog.md)
587. [iterationService](modules/iterationService.md)
588. [IterationSelector](modules/IterationSelector.md)
589. [planningInputService.test](modules/planningInputService.test.md)
590. [projectService](modules/projectService.md)
591. [releaseService](modules/releaseService.md)
592. [ReleaseForm](modules/ReleaseForm.md)
593. [requestSourceService](modules/requestSourceService.md)
594. [savedViewService](modules/savedViewService.md)
595. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
596. [schedulingRulesService](modules/schedulingRulesService.md)
597. [AdminAccessPanel](modules/AdminAccessPanel.md)
598. [AdminAccessGate](modules/AdminAccessGate.md)
599. [AdminAccessGate.test](modules/AdminAccessGate.test.md)
600. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
601. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
602. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
603. [sessionService](modules/sessionService.md)
604. [snapshotService](modules/snapshotService.md)
605. [snapshotVersions.test](modules/snapshotVersions.test.md)
606. [systemSettingsService](modules/systemSettingsService.md)
607. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
608. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
609. [taskService](modules/taskService.md)
610. [DeliveryDependencies](modules/DeliveryDependencies.md)
611. [ImportTasksModal](modules/ImportTasksModal.md)
612. [MetricCount](modules/MetricCount.md)
613. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
614. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
615. [TaskContextSummary](modules/TaskContextSummary.md)
616. [TaskDependencySelector](modules/TaskDependencySelector.md)
617. [TaskReviewer](modules/TaskReviewer.md)
618. [TaskSearch](modules/TaskSearch.md)
619. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
620. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
621. [TaskWorkPanel](modules/TaskWorkPanel.md)
622. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
623. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
624. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
625. [teamService](modules/teamService.md)
626. [GanttBarInputs](modules/GanttBarInputs.md)
627. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
628. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
629. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
630. [ImportTeamModal](modules/ImportTeamModal.md)
631. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
632. [TeamForm](modules/TeamForm.md)
633. [TeamForm.test](modules/TeamForm.test.md)
634. [TeamProfileManager](modules/TeamProfileManager.md)
635. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
636. [VacationCsvImport](modules/VacationCsvImport.md)
637. [LocalProfilePicker](modules/LocalProfilePicker.md)
638. [CalendarPage](modules/CalendarPage.md)
639. [CalendarPage.test](modules/CalendarPage.test.md)
640. [templateService](modules/templateService.md)
641. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
642. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
643. [timeEntryService](modules/timeEntryService.md)
644. [useTimeEntries](modules/useTimeEntries.md)
645. [timeEntryService.test](modules/timeEntryService.test.md)
646. [triageService](modules/triageService.md)
647. [QuickCapture](modules/QuickCapture.md)
648. [QuickCapture.test](modules/QuickCapture.test.md)
649. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
650. [copyText](modules/copyText.md)
651. [focusLifecycle](modules/focusLifecycle.md)
652. [focusLifecycle.test](modules/focusLifecycle.test.md)
653. [formatDate](modules/formatDate.md)
654. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
655. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
656. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
657. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
658. [TaskStatusFlow](modules/TaskStatusFlow.md)
659. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
660. [IterationForm](modules/IterationForm.md)
661. [IterationForm.test](modules/IterationForm.test.md)
662. [NotificationsPanel](modules/NotificationsPanel.md)
663. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
664. [ConnectedReadersPanel](modules/ConnectedReadersPanel.md)
665. [ConnectedReadersPanel.test](modules/ConnectedReadersPanel.test.md)
666. [StatusChangeControl](modules/StatusChangeControl.md)
667. [TaskDiscussion](modules/TaskDiscussion.md)
668. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
669. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
670. [TimeEntriesReport](modules/TimeEntriesReport.md)
671. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
672. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
673. [VacationManager](modules/VacationManager.md)
674. [planningMasters_masters](modules/planningMasters_masters.md)
675. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
676. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
677. [SidebarIterationCard](modules/SidebarIterationCard.md)
678. [AppSidebar](modules/AppSidebar.md)
679. [AppSidebar.test](modules/AppSidebar.test.md)
680. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
681. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
682. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
683. [usePlanningReadiness](modules/usePlanningReadiness.md)
684. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
685. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
686. [IdentityProvider](modules/IdentityProvider.md)
687. [UserSessionBadge](modules/UserSessionBadge.md)
688. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
689. [IdentityProvider.test](modules/IdentityProvider.test.md)
690. [useLiveWindow.test](modules/useLiveWindow.test.md)
691. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
692. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
693. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
694. [PlanMasterPage](modules/PlanMasterPage.md)
695. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
696. [PlanPage](modules/PlanPage.md)
697. [PlanPage.test](modules/PlanPage.test.md)
698. [PlanSharePage](modules/PlanSharePage.md)
699. [PlanSharePage.test](modules/PlanSharePage.test.md)
700. [graphLimitError](modules/graphLimitError.md)
701. [modelRouting](modules/modelRouting.md)
702. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
703. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
704. [modelRouting.test](modules/modelRouting.test.md)
705. [protectedQueries](modules/protectedQueries.md)
706. [AssignedAgentsSummary](modules/AssignedAgentsSummary.md)
707. [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md)
708. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
709. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
710. [AgentAccessPanel](modules/AgentAccessPanel.md)
711. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
712. [AgentModelAdministration](modules/AgentModelAdministration.md)
713. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
714. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
715. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
716. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
717. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
718. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
719. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
720. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
721. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
722. [AgentPipelinePage](modules/AgentPipelinePage.md)
723. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
724. [safeUrl](modules/safeUrl.md)
725. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
726. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
727. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
728. [TaskReadView](modules/TaskReadView.md)
729. [TaskReadView.test](modules/TaskReadView.test.md)
730. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
731. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
732. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
733. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
734. [CommandMenu](modules/CommandMenu.md)
735. [CommandMenu.test](modules/CommandMenu.test.md)
736. [ContextHelp](modules/ContextHelp.md)
737. [AppTopNav](modules/AppTopNav.md)
738. [AppShell](modules/AppShell.md)
739. [App](modules/App.md)
740. [AppShell.test](modules/AppShell.test.md)
741. [AppTopNav.test](modules/AppTopNav.test.md)
742. [ContextHelp.test](modules/ContextHelp.test.md)
743. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
744. [src_main](modules/src_main.md)
745. [SettingsPage](modules/SettingsPage.md)
746. [SettingsPage.test](modules/SettingsPage.test.md)
747. [taskFilterDefaults](modules/taskFilterDefaults.md)
748. [TaskFiltersBar](modules/TaskFiltersBar.md)
749. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
750. [taskViewState](modules/taskViewState.md)
751. [savedViewState](modules/savedViewState.md)
752. [SavedViewsControl](modules/SavedViewsControl.md)
753. [savedViewState.test](modules/savedViewState.test.md)
754. [taskFilters](modules/taskFilters.md)
755. [taskFilters.test](modules/taskFilters.test.md)
756. [teamMemberLabels](modules/teamMemberLabels.md)
757. [InitiativeForm](modules/InitiativeForm.md)
758. [RoadmapPage](modules/RoadmapPage.md)
759. [RoadmapPage.test](modules/RoadmapPage.test.md)
760. [templateDefaults](modules/templateDefaults.md)
761. [ProjectForm](modules/ProjectForm.md)
762. [ProjectForm.test](modules/ProjectForm.test.md)
763. [TaskForm](modules/TaskForm.md)
764. [GuardedTaskModal](modules/GuardedTaskModal.md)
765. [BacklogPanel](modules/BacklogPanel.md)
766. [CurrentTaskModal.test](modules/CurrentTaskModal.test.md)
767. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
768. [TaskEditModal](modules/TaskEditModal.md)
769. [GanttChart](modules/GanttChart.md)
770. [GanttChart.test](modules/GanttChart.test.md)
771. [TaskEditModal.test](modules/TaskEditModal.test.md)
772. [ProjectTaskTree](modules/ProjectTaskTree.md)
773. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
774. [TaskForm.test](modules/TaskForm.test.md)
775. [GanttPage](modules/GanttPage.md)
776. [GanttPage.test](modules/GanttPage.test.md)
777. [MyWorkPage](modules/MyWorkPage.md)
778. [MyWorkPage.test](modules/MyWorkPage.test.md)
779. [TriagePage](modules/TriagePage.md)
780. [visibleWork](modules/visibleWork.md)
781. [TaskList](modules/TaskList.md)
782. [TaskList.test](modules/TaskList.test.md)
783. [visibleWork.test](modules/visibleWork.test.md)
784. [workNumbers](modules/workNumbers.md)
785. [OnTrackSummary](modules/OnTrackSummary.md)
786. [StatusDistribution](modules/StatusDistribution.md)
787. [IterationOutlook.test](modules/IterationOutlook.test.md)
788. [IterationCapacityLine](modules/IterationCapacityLine.md)
789. [IterationList](modules/IterationList.md)
790. [IterationList.test](modules/IterationList.test.md)
791. [KanbanCard](modules/KanbanCard.md)
792. [KanbanColumn](modules/KanbanColumn.md)
793. [KanbanBoard](modules/KanbanBoard.md)
794. [KanbanBoard.test](modules/KanbanBoard.test.md)
795. [KanbanColumn.test](modules/KanbanColumn.test.md)
796. [WorkMetricsLine](modules/WorkMetricsLine.md)
797. [MetricCount.test](modules/MetricCount.test.md)
798. [TeamList](modules/TeamList.md)
799. [TeamList.test](modules/TeamList.test.md)
800. [AnalyticsPage](modules/AnalyticsPage.md)
801. [IterationsPage](modules/IterationsPage.md)
802. [OverviewPage](modules/OverviewPage.md)
803. [OverviewPage.test](modules/OverviewPage.test.md)
804. [ProjectDetailPage](modules/ProjectDetailPage.md)
805. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
806. [ProjectsPage](modules/ProjectsPage.md)
807. [ProjectsPage.test](modules/ProjectsPage.test.md)
808. [TasksPage](modules/TasksPage.md)
809. [TasksPage.test](modules/TasksPage.test.md)
810. [TeamPage](modules/TeamPage.md)
811. [tailwind.config](modules/tailwind.config.md)
812. [check-tailwind-classes](modules/check-tailwind-classes.md)
813. [vite.config](modules/vite.config.md)
814. [vitest.config](modules/vitest.config.md)
815. [create_agent_actor](modules/create_agent_actor.md)
816. [generate_workchord_keys](modules/generate_workchord_keys.md)
817. [setup_agent_team](modules/setup_agent_team.md)
818. [build_agent_skills](modules/build_agent_skills.md)
819. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
820. [android_qualification](modules/android_qualification.md)
821. [android_web_peer](modules/android_web_peer.md)
822. [apt_runtime](modules/apt_runtime.md)
823. [browser_performance](modules/browser_performance.md)
824. [browser_planning_inputs](modules/browser_planning_inputs.md)
825. [browser_worker](modules/browser_worker.md)
826. [browser_managed_work](modules/browser_managed_work.md)
827. [browser_write_readback](modules/browser_write_readback.md)
828. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
829. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
830. [ci_runtime](modules/ci_runtime.md)
831. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
832. [postgres_runtime](modules/postgres_runtime.md)
833. [run_android_checks](modules/run_android_checks.md)
834. [run_disposable_checks](modules/run_disposable_checks.md)
835. [serve_disposable_api](modules/serve_disposable_api.md)
836. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
837. [test_apt_runtime](modules/test_apt_runtime.md)
838. [test_ci_runtime](modules/test_ci_runtime.md)
839. [test_native_runtimes](modules/test_native_runtimes.md)
840. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
841. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
842. [generate_client_contract](modules/generate_client_contract.md)
843. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
844. [load_common](modules/load_common.md)
845. [collect](modules/collect.md)
846. [result](modules/result.md)
847. [compare](modules/compare.md)
848. [finalize](modules/finalize.md)
849. [qualify](modules/qualify.md)
850. [resilience](modules/resilience.md)
851. [run](modules/run.md)
852. [seal](modules/seal.md)
853. [seed](modules/seed.md)
854. [source_binding](modules/source_binding.md)
855. [local_baseline](modules/local_baseline.md)
856. [service_worksets](modules/service_worksets.md)
857. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
858. [isolated_rehearsal](modules/isolated_rehearsal.md)

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
| [app_main](modules/app_main.md) | `settings = get_settings`, `app = FastAPI`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.add_middleware`, `app.add_middleware`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `mount_mcp_http` |
| [maintenance](modules/maintenance.md) | `SAFE_HTTP_METHODS = frozenset`, `_CORRELATION_ID_PATTERN = re.compile` |
| [mcp_agent_tools](modules/mcp_agent_tools.md) | `_AGENT_ASSIGNMENT_CREATE_ADAPTER = TypeAdapter`, `_AGENT_ASSIGNMENT_UPDATE_ADAPTER = TypeAdapter`, `_AGENT_WORK_BEGIN_ADAPTER = TypeAdapter` |
| [mcp_server](modules/mcp_server.md) | `_http_agent_key = ContextVar`, `READ_ONLY_TOOL = ToolAnnotations`, `WRITE_TOOL = ToolAnnotations`, `REMOVAL_TOOL = ToolAnnotations`, `mcp = create_mcp_server` |
| [migrations_env](modules/migrations_env.md) | `settings = get_settings`, `database_configuration = parse_database_configuration`, `config.set_main_option`, `fileConfig`, `run_migrations_offline`, `run_migrations_online` |
| [delivery_observation](modules/delivery_observation.md) | `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen` |
| [models_execution_usage](modules/models_execution_usage.md) | `event.listen`, `event.listen` |
| [recovery](modules/recovery.md) | `event.listen` |
| [models_release](modules/models_release.md) | `release_tasks = Table` |
| [models_runtime_observation](modules/models_runtime_observation.md) | `event.listen` |
| [observability](modules/observability.md) | `logger = logging.getLogger` |
| [routers_agent](modules/routers_agent.md) | `router = APIRouter`, `logger = logging.getLogger` |
| [agent_catalog](modules/agent_catalog.md) | `router = APIRouter` |
| [routers_agent_connect](modules/routers_agent_connect.md) | `router = APIRouter` |
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
| [schemas_agent](modules/schemas_agent.md) | `SUPPORTED_AGENT_SCOPES = frozenset`, `HARNESS_KIND_PATTERN = re.compile` |
| [agent_routing](modules/agent_routing.md) | `MAX_REASON_CODES = len` |
| [agent_team_setup](modules/agent_team_setup.md) | `AGENT_TEAM_ROLE_RULE_FIELDS = frozenset`, `SECRET_QUERY_KEYS = frozenset` |
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
| [test_agent_key_delivery](modules/test_agent_key_delivery.md) | `_PROVISION_SPEC = importlib.util.spec_from_file_location`, `provision_actor = importlib.util.module_from_spec`, `_PROVISION_SPEC.loader.exec_module`, `posix_only = pytest.mark.skipif` |
| [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md) | `_PROVISION_SPEC = importlib.util.spec_from_file_location`, `provision_actor = importlib.util.module_from_spec`, `_PROVISION_SPEC.loader.exec_module` |
| [test_agent_routing_service](modules/test_agent_routing_service.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md) | `pytestmark = pytest.mark.usefixtures`, `_FIXED_NOW = datetime` |
| [test_agent_team_setup](modules/test_agent_team_setup.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md) | `SPEC = importlib.util.spec_from_file_location`, `setup_agent_team = importlib.util.module_from_spec`, `SPEC.loader.exec_module` |
| [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md) | `FIXED_NOW = datetime` |
| [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_dependency_date_cascade](modules/test_dependency_date_cascade.md) | `PLANNED_START = date`, `LATER_START = date` |
| [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md) | `READ_NAME = re.compile` |
| [test_native_connections](modules/test_native_connections.md) | `CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b'=').decode` |
| [test_observer_sessions](modules/test_observer_sessions.md) | `CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b'=').decode`, `OBSERVER_CAP = timedelta`, `PERSON_CAP = timedelta` |
| [test_plan_checkpoints](modules/test_plan_checkpoints.md) | `READY = dict` |
| [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md) | `TODAY = date`, `NOW = datetime.fromisoformat` |
| [test_team_topology_read](modules/test_team_topology_read.md) | `pytestmark = pytest.mark.usefixtures` |
| [check-bundle-budget](modules/check-bundle-budget.md) | `BUDGETS = freeze` |
| [check-query-feedback](modules/check-query-feedback.md) | `HOOK_KINDS = Map` |
| [check-tailwind-classes](modules/check-tailwind-classes.md) | `semanticRoots = Set`, `colorUtilityPrefixes = sort`, `colorUtilitySource = join`, `semanticRootSource = join`, `semanticClassPattern = RegExp`, `legacyClassPattern = RegExp`, `rawPaletteClassPattern = RegExp`, `darkVariantClassPattern = RegExp`, `arbitraryColorClassPattern = RegExp`, `translucentSemanticTextPattern = RegExp`, `semanticColorNames = Set` |
| [App](modules/App.md) | `OverviewPage = lazy`, `LandingPage = lazy`, `PlanPage = lazy`, `PlanMasterPage = lazy`, `PlanSharePage = lazy`, `CalendarPage = lazy`, `IterationsPage = lazy`, `TeamPage = lazy`, `TasksPage = lazy`, `MyWorkPage = lazy`, `NativeConnectionPage = lazy`, `TriagePage = lazy`, `ProjectsPage = lazy`, `ProjectDetailPage = lazy`, `ProjectReleaseDetailPage = lazy`, `RoadmapPage = lazy`, `GanttPage = lazy`, `AnalyticsPage = lazy`, `SettingsPage = lazy`, `AgentPipelinePage = lazy`, `AgentTeamSetupMasterPage = lazy`, `NotFoundPage = lazy` |
| [UserSessionBadge.test](modules/UserSessionBadge.test.md) | `sessionServiceMock = hoisted`, `mock`, `describe` |
| [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md) | `agentServiceMock = hoisted`, `mock`, `describe` |
| [AssignedAgentsSummary](modules/AssignedAgentsSummary.md) | `KNOWN_PURPOSES = Set`, `KNOWN_STATES = Set` |
| [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md) | `describe` |
| [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md) | `agentServiceMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `dispatchableRoster = map`, `describe`, `describe` |
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
| [Select.test](modules/Select.test.md) | `describe` |
| [Select](modules/Select.md) | `Select = forwardRef` |
| [Textarea](modules/Textarea.md) | `Textarea = forwardRef` |
| [dialogLayer](modules/dialogLayer.md) | `focusableSelector = join` |
| [formControlLabels.test](modules/formControlLabels.test.md) | `root = resolve`, `LABEL_WRAPPERS = Set`, `it` |
| [iconButtonTooltips.test](modules/iconButtonTooltips.test.md) | `root = resolve`, `it` |
| [ToastProvider.test](modules/ToastProvider.test.md) | `describe` |
| [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md) | `afterEach`, `it` |
| [toast](modules/toast.md) | `ToastContext = createContext` |
| [GanttChart.test](modules/GanttChart.test.md) | `ganttServiceMock = hoisted`, `mock`, `mock`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe` |
| [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md) | `t = bind` |
| [TaskEditModal.test](modules/TaskEditModal.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `it`, `it` |
| [UnscheduledTasks.test](modules/UnscheduledTasks.test.md) | `it`, `it` |
| [IterationForm.test](modules/IterationForm.test.md) | `planningMock = hoisted`, `mock`, `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `iterationStoreMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [IterationList.test](modules/IterationList.test.md) | `iterations = hoisted`, `mock`, `describe` |
| [AppShell.test](modules/AppShell.test.md) | `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AppSidebar.test](modules/AppSidebar.test.md) | `savedViewServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [AppSidebar](modules/AppSidebar.md) | `SAVED_VIEW_ROUTE_PATHS = Set` |
| [AppTopNav.test](modules/AppTopNav.test.md) | `planningReadinessMock = hoisted`, `triageServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [CommandMenu.test](modules/CommandMenu.test.md) | `lookup = hoisted`, `mock`, `projects = hoisted`, `mock`, `savedViews = hoisted`, `mock`, `describe` |
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
| [ConnectedReadersPanel.test](modules/ConnectedReadersPanel.test.md) | `service = hoisted`, `mock`, `later = toISOString`, `describe` |
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
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind`, `LOOPBACK_HOSTS = Set` |
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
| [taskTransitions.test](modules/taskTransitions.test.md) | `it` |
| [useLiveWindow.test](modules/useLiveWindow.test.md) | `it`, `it.each([0, -1, NaN, undefined])`, `it`, `it`, `it` |
| [workQueryFreshness.test](modules/workQueryFreshness.test.md) | `cases = flatMap`, `it.each(cases)` |
| [workQueryFreshness](modules/workQueryFreshness.md) | `WORKSPACE_QUERY_POLICIES = fromEntries` |
| [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md) | `it.each(['hidden', 'disabled', 'unauthorized', 'too-many-pages'])`, `it`, `it`, `it`, `it` |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | `describe` |
| [formatsAndWording.test](modules/formatsAndWording.test.md) | `english = flatten`, `describe` |
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
| [LandingPage.test](modules/LandingPage.test.md) | `it` |
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
