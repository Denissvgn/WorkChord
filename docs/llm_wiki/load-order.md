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
89. [agent_routing_policy](modules/agent_routing_policy.md)
90. [agent_routing](modules/agent_routing.md)
91. [agent_routing_rollout](modules/agent_routing_rollout.md)
92. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
93. [routers_agent_connect](modules/routers_agent_connect.md)
94. [agent_team_credentials](modules/agent_team_credentials.md)
95. [bounded_scope_reads](modules/bounded_scope_reads.md)
96. [language_service](modules/language_service.md)
97. [plan_checkpoints](modules/plan_checkpoints.md)
98. [planning_input_context](modules/planning_input_context.md)
99. [planning_issues](modules/planning_issues.md)
100. [scheduling_rules_service](modules/scheduling_rules_service.md)
101. [upgrade_service](modules/upgrade_service.md)
102. [upgrade](modules/upgrade.md)
103. [settings_read](modules/settings_read.md)
104. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
105. [sql_semantics](modules/sql_semantics.md)
106. [exceptions](modules/exceptions.md)
107. [text_similarity](modules/text_similarity.md)
108. [time](modules/time.md)
109. [observability](modules/observability.md)
110. [app_database](modules/app_database.md)
111. [models_agent](modules/models_agent.md)
112. [models_autonomy](modules/models_autonomy.md)
113. [models_calendar](modules/models_calendar.md)
114. [models_capacity](modules/models_capacity.md)
115. [models_database_migration](modules/models_database_migration.md)
116. [delivery_dependency](modules/delivery_dependency.md)
117. [models_discussion](modules/models_discussion.md)
118. [models_execution_usage](modules/models_execution_usage.md)
119. [models_external_link](modules/models_external_link.md)
120. [models_github](modules/models_github.md)
121. [models_identity](modules/models_identity.md)
122. [models_iteration](modules/models_iteration.md)
123. [models_label](modules/models_label.md)
124. [native_connection](modules/native_connection.md)
125. [models_outbound_webhook](modules/models_outbound_webhook.md)
126. [models_plan_share](modules/models_plan_share.md)
127. [models_release](modules/models_release.md)
128. [models_project](modules/models_project.md)
129. [models_request_source](modules/models_request_source.md)
130. [models_runtime_observation](modules/models_runtime_observation.md)
131. [models_saved_view](modules/models_saved_view.md)
132. [models_system_settings](modules/models_system_settings.md)
133. [models_task](modules/models_task.md)
134. [recovery](modules/recovery.md)
135. [models_task_brief](modules/models_task_brief.md)
136. [delivery_observation](modules/delivery_observation.md)
137. [task_status_log](modules/task_status_log.md)
138. [team_member](modules/team_member.md)
139. [models_template](modules/models_template.md)
140. [models_time_entry](modules/models_time_entry.md)
141. [models_triage](modules/models_triage.md)
142. [user_session](modules/user_session.md)
143. [models___init__](modules/models___init__.md)
144. [catalog](modules/catalog.md)
145. [database_migration_canonical](modules/database_migration_canonical.md)
146. [source](modules/source.md)
147. [transfer](modules/transfer.md)
148. [cli_database_migration](modules/cli_database_migration.md)
149. [database_migration___init__](modules/database_migration___init__.md)
150. [migrations_env](modules/migrations_env.md)
151. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
152. [calendar_service](modules/calendar_service.md)
153. [calendars](modules/calendars.md)
154. [capacity_service](modules/capacity_service.md)
155. [routers_capacity](modules/routers_capacity.md)
156. [delivery_dependency_service](modules/delivery_dependency_service.md)
157. [delivery_metrics_service](modules/delivery_metrics_service.md)
158. [discussion_service](modules/discussion_service.md)
159. [identity_service](modules/identity_service.md)
160. [import_planning_service](modules/import_planning_service.md)
161. [iteration_service](modules/iteration_service.md)
162. [iterations](modules/iterations.md)
163. [label_service](modules/label_service.md)
164. [labels](modules/labels.md)
165. [native_session_service](modules/native_session_service.md)
166. [saved_view_service](modules/saved_view_service.md)
167. [session_service](modules/session_service.md)
168. [http_authority](modules/http_authority.md)
169. [routers_identity](modules/routers_identity.md)
170. [saved_views](modules/saved_views.md)
171. [routers_session](modules/routers_session.md)
172. [task_brief_service](modules/task_brief_service.md)
173. [task_context_revision_service](modules/task_context_revision_service.md)
174. [task_domain_service](modules/task_domain_service.md)
175. [task_hierarchy_service](modules/task_hierarchy_service.md)
176. [task_recovery_service](modules/task_recovery_service.md)
177. [task_timeline_service](modules/task_timeline_service.md)
178. [team_service](modules/team_service.md)
179. [routers_team](modules/routers_team.md)
180. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
181. [snapshot_service](modules/snapshot_service.md)
182. [plan_share_service](modules/plan_share_service.md)
183. [plan_shares](modules/plan_shares.md)
184. [template_service](modules/template_service.md)
185. [templates](modules/templates.md)
186. [time_entry_service](modules/time_entry_service.md)
187. [time_report_service](modules/time_report_service.md)
188. [services_work_metrics](modules/services_work_metrics.md)
189. [import_parser](modules/import_parser.md)
190. [url_policy](modules/url_policy.md)
191. [schemas_external_link](modules/schemas_external_link.md)
192. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
193. [schemas_request_source](modules/schemas_request_source.md)
194. [schemas_task](modules/schemas_task.md)
195. [schemas_gantt](modules/schemas_gantt.md)
196. [task_detail](modules/task_detail.md)
197. [schemas_triage](modules/schemas_triage.md)
198. [schemas___init__](modules/schemas___init__.md)
199. [schemas_agent](modules/schemas_agent.md)
200. [agent_run_read](modules/agent_run_read.md)
201. [schemas_runtime_observation](modules/schemas_runtime_observation.md)
202. [agent_readiness](modules/agent_readiness.md)
203. [llm_service](modules/llm_service.md)
204. [runtime_observation_service](modules/runtime_observation_service.md)
205. [system_settings_service](modules/system_settings_service.md)
206. [routers_system_settings](modules/routers_system_settings.md)
207. [email_settings_service](modules/email_settings_service.md)
208. [routers_email_settings](modules/routers_email_settings.md)
209. [notification_service](modules/notification_service.md)
210. [outbound_webhook_service](modules/outbound_webhook_service.md)
211. [worker](modules/worker.md)
212. [outbound_webhooks](modules/outbound_webhooks.md)
213. [external_link_service](modules/external_link_service.md)
214. [github_status_service](modules/github_status_service.md)
215. [request_source_service](modules/request_source_service.md)
216. [request_sources](modules/request_sources.md)
217. [project_service](modules/project_service.md)
218. [task_detail_service](modules/task_detail_service.md)
219. [task_import_service](modules/task_import_service.md)
220. [task_service](modules/task_service.md)
221. [export](modules/export.md)
222. [snapshots](modules/snapshots.md)
223. [agent_routing_observability](modules/agent_routing_observability.md)
224. [agent_service](modules/agent_service.md)
225. [agent_skill_bundles](modules/agent_skill_bundles.md)
226. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
227. [agent_routing_service](modules/agent_routing_service.md)
228. [agent_team_setup_service](modules/agent_team_setup_service.md)
229. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
230. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
231. [execution_usage_service](modules/execution_usage_service.md)
232. [routers_task_domain](modules/routers_task_domain.md)
233. [delivery_dependencies](modules/delivery_dependencies.md)
234. [routers_discussion](modules/routers_discussion.md)
235. [time_entries](modules/time_entries.md)
236. [agent_run_read_service](modules/agent_run_read_service.md)
237. [github_status_automation_service](modules/github_status_automation_service.md)
238. [release_service](modules/release_service.md)
239. [projects](modules/projects.md)
240. [scheduler_service](modules/scheduler_service.md)
241. [routers_gantt](modules/routers_gantt.md)
242. [routers_llm](modules/routers_llm.md)
243. [agent_planning_service](modules/agent_planning_service.md)
244. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
245. [tasks](modules/tasks.md)
246. [task_status_service](modules/task_status_service.md)
247. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
248. [triage_service](modules/triage_service.md)
249. [routers_triage](modules/routers_triage.md)
250. [agent_work_service](modules/agent_work_service.md)
251. [mcp_agent_tools](modules/mcp_agent_tools.md)
252. [mcp_server](modules/mcp_server.md)
253. [routers_agent](modules/routers_agent.md)
254. [routers_agent_planning](modules/routers_agent_planning.md)
255. [agent_catalog](modules/agent_catalog.md)
256. [github_webhook_service](modules/github_webhook_service.md)
257. [routers_github](modules/routers_github.md)
258. [web_intake_service](modules/web_intake_service.md)
259. [routers_intake](modules/routers_intake.md)
260. [app_main](modules/app_main.md)
261. [routers___init__](modules/routers___init__.md)
262. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
263. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
264. [test_server_acceptance](modules/test_server_acceptance.md)
265. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
266. [test_work_package_service](modules/test_work_package_service.md)
267. [test_database_configuration](modules/test_database_configuration.md)
268. [test_deployment_topology](modules/test_deployment_topology.md)
269. [test_observability](modules/test_observability.md)
270. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
271. [test_query_boundaries](modules/test_query_boundaries.md)
272. [test_runtime_policy](modules/test_runtime_policy.md)
273. [test_schema_behavior](modules/test_schema_behavior.md)
274. [test_cutover_evidence](modules/test_cutover_evidence.md)
275. [test_documentation_boundary](modules/test_documentation_boundary.md)
276. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
277. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
278. [test_source_preflight](modules/test_source_preflight.md)
279. [test_transfer_catalog](modules/test_transfer_catalog.md)
280. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
281. [0001_wave0_probe](modules/0001_wave0_probe.md)
282. [test_allocation_identity](modules/test_allocation_identity.md)
283. [test_initial_schema](modules/test_initial_schema.md)
284. [test_profile_identity](modules/test_profile_identity.md)
285. [test_android_cleanup](modules/test_android_cleanup.md)
286. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
287. [test_load_tooling](modules/test_load_tooling.md)
288. [test_local_baseline](modules/test_local_baseline.md)
289. [test_routing_evidence](modules/test_routing_evidence.md)
290. [support_database](modules/support_database.md)
291. [delivery](modules/delivery.md)
292. [factories](modules/factories.md)
293. [faults](modules/faults.md)
294. [runtime_peer](modules/runtime_peer.md)
295. [schema](modules/schema.md)
296. [support___init__](modules/support___init__.md)
297. [conftest](modules/conftest.md)
298. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
299. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
300. [test_project_identity](modules/test_project_identity.md)
301. [test_project_identity_scope](modules/test_project_identity_scope.md)
302. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
303. [transactions](modules/transactions.md)
304. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
305. [test_agent_key_delivery](modules/test_agent_key_delivery.md)
306. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
307. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
308. [test_agent_routing_data](modules/test_agent_routing_data.md)
309. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
310. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
311. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
312. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
313. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
314. [test_agent_routing_service](modules/test_agent_routing_service.md)
315. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
316. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
317. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
318. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
319. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
320. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
321. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
322. [test_authority_migrations](modules/test_authority_migrations.md)
323. [test_capacity_contract](modules/test_capacity_contract.md)
324. [test_client_contract](modules/test_client_contract.md)
325. [test_database_harness](modules/test_database_harness.md)
326. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
327. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
328. [test_agent_team_setup](modules/test_agent_team_setup.md)
329. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
330. [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md)
331. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
332. [test_dependency_date_cascade](modules/test_dependency_date_cascade.md)
333. [test_deployment_configuration](modules/test_deployment_configuration.md)
334. [test_effective_deferral](modules/test_effective_deferral.md)
335. [test_execution_usage](modules/test_execution_usage.md)
336. [test_execution_working_dates](modules/test_execution_working_dates.md)
337. [test_harness_session_metadata](modules/test_harness_session_metadata.md)
338. [test_managed_authority](modules/test_managed_authority.md)
339. [test_allocation_recovery](modules/test_allocation_recovery.md)
340. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
341. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
342. [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md)
343. [test_metric_matches](modules/test_metric_matches.md)
344. [test_mobile_contract](modules/test_mobile_contract.md)
345. [test_mutation_versions](modules/test_mutation_versions.md)
346. [test_native_connections](modules/test_native_connections.md)
347. [test_observer_sessions](modules/test_observer_sessions.md)
348. [test_agdash_link_provider](modules/test_agdash_link_provider.md)
349. [test_person_assignment_reads](modules/test_person_assignment_reads.md)
350. [test_person_run_reads](modules/test_person_run_reads.md)
351. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
352. [test_plan_shares](modules/test_plan_shares.md)
353. [test_planning_input_context](modules/test_planning_input_context.md)
354. [test_planning_issues](modules/test_planning_issues.md)
355. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
356. [test_process_roles](modules/test_process_roles.md)
357. [test_profile_capacity](modules/test_profile_capacity.md)
358. [test_planning_read_models](modules/test_planning_read_models.md)
359. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
360. [test_project_working_timezone](modules/test_project_working_timezone.md)
361. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
362. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
363. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
364. [test_runtime_observations](modules/test_runtime_observations.md)
365. [test_saved_view_service](modules/test_saved_view_service.md)
366. [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md)
367. [test_settings_read_access](modules/test_settings_read_access.md)
368. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
369. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
370. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
371. [test_task_domain](modules/test_task_domain.md)
372. [test_delivery_metrics](modules/test_delivery_metrics.md)
373. [test_human_work_queries](modules/test_human_work_queries.md)
374. [test_task_discussion](modules/test_task_discussion.md)
375. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
376. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
377. [test_task_pagination](modules/test_task_pagination.md)
378. [test_team_topology_read](modules/test_team_topology_read.md)
379. [test_time_entries](modules/test_time_entries.md)
380. [test_time_reports](modules/test_time_reports.md)
381. [test_unscheduled_tasks](modules/test_unscheduled_tasks.md)
382. [test_work_correctness](modules/test_work_correctness.md)
383. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
384. [eslint.config](modules/eslint.config.md)
385. [postcss.config](modules/postcss.config.md)
386. [check-bundle-budget](modules/check-bundle-budget.md)
387. [check-query-feedback](modules/check-query-feedback.md)
388. [Button](modules/Button.md)
389. [Button.test](modules/Button.test.md)
390. [Checkbox](modules/Checkbox.md)
391. [CollapsibleSection](modules/CollapsibleSection.md)
392. [DisabledReason](modules/DisabledReason.md)
393. [Input](modules/Input.md)
394. [Input.test](modules/Input.test.md)
395. [Select](modules/Select.md)
396. [Textarea](modules/Textarea.md)
397. [dialogLayer](modules/dialogLayer.md)
398. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
399. [Modal](modules/Modal.md)
400. [ConfirmDialog](modules/ConfirmDialog.md)
401. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
402. [formControlLabels.test](modules/formControlLabels.test.md)
403. [iconButtonTooltips.test](modules/iconButtonTooltips.test.md)
404. [useConfirmDialog](modules/useConfirmDialog.md)
405. [LiveWindowStatus](modules/LiveWindowStatus.md)
406. [WorkFreshness](modules/WorkFreshness.md)
407. [toast](modules/toast.md)
408. [ToastProvider](modules/ToastProvider.md)
409. [ToastProvider.test](modules/ToastProvider.test.md)
410. [UnscheduledTasks](modules/UnscheduledTasks.md)
411. [LabelChip](modules/LabelChip.md)
412. [Breadcrumbs](modules/Breadcrumbs.md)
413. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
414. [commandMenuEvents](modules/commandMenuEvents.md)
415. [AccessKeysSummary](modules/AccessKeysSummary.md)
416. [AgentTeamManifestPreview](modules/AgentTeamManifestPreview.md)
417. [ConstraintsPanel](modules/ConstraintsPanel.md)
418. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
419. [SettingsUnsavedBar](modules/SettingsUnsavedBar.md)
420. [WithheldValuesNote](modules/WithheldValuesNote.md)
421. [claimTime](modules/claimTime.md)
422. [SortableTaskItem](modules/SortableTaskItem.md)
423. [taskDraftStorage](modules/taskDraftStorage.md)
424. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
425. [useDraftDismissal](modules/useDraftDismissal.md)
426. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
427. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
428. [InlineEmptyState](modules/InlineEmptyState.md)
429. [MasterProgress](modules/MasterProgress.md)
430. [MasterProgress.test](modules/MasterProgress.test.md)
431. [OverflowMenu](modules/OverflowMenu.md)
432. [PageLayout](modules/PageLayout.md)
433. [SectionCard](modules/SectionCard.md)
434. [SegmentedControl](modules/SegmentedControl.md)
435. [Select.test](modules/Select.test.md)
436. [SlideOverDrawer](modules/SlideOverDrawer.md)
437. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
438. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
439. [StickyRail](modules/StickyRail.md)
440. [index](modules/index.md)
441. [tone](modules/tone.md)
442. [projectStatusStyles](modules/projectStatusStyles.md)
443. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
444. [Pill](modules/Pill.md)
445. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
446. [tone.test](modules/tone.test.md)
447. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
448. [manifestLocations](modules/manifestLocations.md)
449. [manifestLocations.test](modules/manifestLocations.test.md)
450. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
451. [AgentTeamStepList](modules/AgentTeamStepList.md)
452. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
453. [statusScopes](modules/statusScopes.md)
454. [statusScopes.test](modules/statusScopes.test.md)
455. [identityContext](modules/identityContext.md)
456. [mutationFeedback](modules/mutationFeedback.md)
457. [attentionRanking](modules/attentionRanking.md)
458. [attentionRanking.test](modules/attentionRanking.test.md)
459. [overviewTaskThread](modules/overviewTaskThread.md)
460. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
461. [planningReturn](modules/planningReturn.md)
462. [PlanReturnBar](modules/PlanReturnBar.md)
463. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
464. [planningTaskIssues](modules/planningTaskIssues.md)
465. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
466. [taskTransitions](modules/taskTransitions.md)
467. [taskTransitions.test](modules/taskTransitions.test.md)
468. [useLiveWindow](modules/useLiveWindow.md)
469. [workQueryFreshness](modules/workQueryFreshness.md)
470. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
471. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
472. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
473. [landing.en](modules/landing.en.md)
474. [landing.ru](modules/landing.ru.md)
475. [literals.ru](modules/literals.ru.md)
476. [pagination](modules/pagination.md)
477. [plan.ru](modules/plan.ru.md)
478. [planningInputMessages](modules/planningInputMessages.md)
479. [surfaces.ru](modules/surfaces.ru.md)
480. [teamwork.en](modules/teamwork.en.md)
481. [teamwork.ru](modules/teamwork.ru.md)
482. [timeEntries](modules/timeEntries.md)
483. [resources.en](modules/resources.en.md)
484. [i18n](modules/i18n.md)
485. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
486. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
487. [dateLocale](modules/dateLocale.md)
488. [InteractiveCalendar](modules/InteractiveCalendar.md)
489. [formatsAndWording.test](modules/formatsAndWording.test.md)
490. [resources.ru](modules/resources.ru.md)
491. [i18n.test](modules/i18n.test.md)
492. [schedulingDisplay](modules/schedulingDisplay.md)
493. [seedDisplay](modules/seedDisplay.md)
494. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
495. [routeModules](modules/routeModules.md)
496. [DocumentMetadata](modules/DocumentMetadata.md)
497. [workspaces](modules/workspaces.md)
498. [helpContexts](modules/helpContexts.md)
499. [workspaces.test](modules/workspaces.test.md)
500. [LandingPage](modules/LandingPage.md)
501. [NotFoundPage](modules/NotFoundPage.md)
502. [healthService](modules/healthService.md)
503. [SystemHealthPanel](modules/SystemHealthPanel.md)
504. [iterationStore](modules/iterationStore.md)
505. [iterationStore.test](modules/iterationStore.test.md)
506. [themeStore](modules/themeStore.md)
507. [colorRoles.test](modules/colorRoles.test.md)
508. [planning-masters.test](modules/planning-masters.test.md)
509. [accessibilityInvariants](modules/accessibilityInvariants.md)
510. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
511. [modelAwareRouting](modules/modelAwareRouting.md)
512. [renderWithProviders](modules/renderWithProviders.md)
513. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
514. [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md)
515. [UnscheduledTasks.test](modules/UnscheduledTasks.test.md)
516. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
517. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
518. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
519. [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md)
520. [OverflowMenu.test](modules/OverflowMenu.test.md)
521. [LandingPage.test](modules/LandingPage.test.md)
522. [renderWithProviders.test](modules/renderWithProviders.test.md)
523. [setup](modules/setup.md)
524. [types_agent](modules/types_agent.md)
525. [types_calendar](modules/types_calendar.md)
526. [deliveryMetrics](modules/deliveryMetrics.md)
527. [emailSettings](modules/emailSettings.md)
528. [executionUsage](modules/executionUsage.md)
529. [types_gantt](modules/types_gantt.md)
530. [types_github](modules/types_github.md)
531. [types_iteration](modules/types_iteration.md)
532. [types_label](modules/types_label.md)
533. [outboundWebhook](modules/outboundWebhook.md)
534. [types_project](modules/types_project.md)
535. [types_release](modules/types_release.md)
536. [requestSource](modules/requestSource.md)
537. [savedView](modules/savedView.md)
538. [schedulingRules](modules/schedulingRules.md)
539. [EffortModifierCard](modules/EffortModifierCard.md)
540. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
541. [SchedulingPassCard](modules/SchedulingPassCard.md)
542. [systemSettings](modules/systemSettings.md)
543. [types_task](modules/types_task.md)
544. [types_team](modules/types_team.md)
545. [types_template](modules/types_template.md)
546. [types_triage](modules/types_triage.md)
547. [workMetrics](modules/workMetrics.md)
548. [agentAccess](modules/agentAccess.md)
549. [useAgentAccess](modules/useAgentAccess.md)
550. [apiError](modules/apiError.md)
551. [QueryState](modules/QueryState.md)
552. [taskEditorContract](modules/taskEditorContract.md)
553. [TaskBriefEditor](modules/TaskBriefEditor.md)
554. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
555. [MutationSuccessFeedback](modules/MutationSuccessFeedback.md)
556. [mutationFeedback.test](modules/mutationFeedback.test.md)
557. [adminAccess](modules/adminAccess.md)
558. [useAdminAccess](modules/useAdminAccess.md)
559. [api](modules/api.md)
560. [identityService](modules/identityService.md)
561. [NativeConnectionPage](modules/NativeConnectionPage.md)
562. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
563. [agentService](modules/agentService.md)
564. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
565. [agentService.test](modules/agentService.test.md)
566. [deliveryMetricsService](modules/deliveryMetricsService.md)
567. [discussionService](modules/discussionService.md)
568. [emailSettingsService](modules/emailSettingsService.md)
569. [executionUsageService](modules/executionUsageService.md)
570. [ganttService](modules/ganttService.md)
571. [githubService](modules/githubService.md)
572. [labelService](modules/labelService.md)
573. [LabelSelector](modules/LabelSelector.md)
574. [outboundWebhookService](modules/outboundWebhookService.md)
575. [planShareService](modules/planShareService.md)
576. [planningInputService](modules/planningInputService.md)
577. [usePlanningObservation](modules/usePlanningObservation.md)
578. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
579. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
580. [calendarService](modules/calendarService.md)
581. [PersonCapacity](modules/PersonCapacity.md)
582. [PersonCapacity.test](modules/PersonCapacity.test.md)
583. [exportService](modules/exportService.md)
584. [IterationImportDialog](modules/IterationImportDialog.md)
585. [iterationService](modules/iterationService.md)
586. [IterationSelector](modules/IterationSelector.md)
587. [planningInputService.test](modules/planningInputService.test.md)
588. [projectService](modules/projectService.md)
589. [releaseService](modules/releaseService.md)
590. [ReleaseForm](modules/ReleaseForm.md)
591. [requestSourceService](modules/requestSourceService.md)
592. [savedViewService](modules/savedViewService.md)
593. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
594. [schedulingRulesService](modules/schedulingRulesService.md)
595. [AdminAccessPanel](modules/AdminAccessPanel.md)
596. [AdminAccessGate](modules/AdminAccessGate.md)
597. [AdminAccessGate.test](modules/AdminAccessGate.test.md)
598. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
599. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
600. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
601. [sessionService](modules/sessionService.md)
602. [snapshotService](modules/snapshotService.md)
603. [snapshotVersions.test](modules/snapshotVersions.test.md)
604. [systemSettingsService](modules/systemSettingsService.md)
605. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
606. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
607. [taskService](modules/taskService.md)
608. [DeliveryDependencies](modules/DeliveryDependencies.md)
609. [ImportTasksModal](modules/ImportTasksModal.md)
610. [MetricCount](modules/MetricCount.md)
611. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
612. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
613. [TaskContextSummary](modules/TaskContextSummary.md)
614. [TaskDependencySelector](modules/TaskDependencySelector.md)
615. [TaskReviewer](modules/TaskReviewer.md)
616. [TaskSearch](modules/TaskSearch.md)
617. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
618. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
619. [TaskWorkPanel](modules/TaskWorkPanel.md)
620. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
621. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
622. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
623. [teamService](modules/teamService.md)
624. [GanttBarInputs](modules/GanttBarInputs.md)
625. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
626. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
627. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
628. [ImportTeamModal](modules/ImportTeamModal.md)
629. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
630. [TeamForm](modules/TeamForm.md)
631. [TeamForm.test](modules/TeamForm.test.md)
632. [TeamProfileManager](modules/TeamProfileManager.md)
633. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
634. [VacationCsvImport](modules/VacationCsvImport.md)
635. [LocalProfilePicker](modules/LocalProfilePicker.md)
636. [CalendarPage](modules/CalendarPage.md)
637. [CalendarPage.test](modules/CalendarPage.test.md)
638. [templateService](modules/templateService.md)
639. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
640. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
641. [timeEntryService](modules/timeEntryService.md)
642. [useTimeEntries](modules/useTimeEntries.md)
643. [timeEntryService.test](modules/timeEntryService.test.md)
644. [triageService](modules/triageService.md)
645. [QuickCapture](modules/QuickCapture.md)
646. [QuickCapture.test](modules/QuickCapture.test.md)
647. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
648. [copyText](modules/copyText.md)
649. [focusLifecycle](modules/focusLifecycle.md)
650. [focusLifecycle.test](modules/focusLifecycle.test.md)
651. [formatDate](modules/formatDate.md)
652. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
653. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
654. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
655. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
656. [TaskStatusFlow](modules/TaskStatusFlow.md)
657. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
658. [IterationForm](modules/IterationForm.md)
659. [IterationForm.test](modules/IterationForm.test.md)
660. [NotificationsPanel](modules/NotificationsPanel.md)
661. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
662. [ConnectedReadersPanel](modules/ConnectedReadersPanel.md)
663. [ConnectedReadersPanel.test](modules/ConnectedReadersPanel.test.md)
664. [StatusChangeControl](modules/StatusChangeControl.md)
665. [TaskDiscussion](modules/TaskDiscussion.md)
666. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
667. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
668. [TimeEntriesReport](modules/TimeEntriesReport.md)
669. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
670. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
671. [VacationManager](modules/VacationManager.md)
672. [planningMasters_masters](modules/planningMasters_masters.md)
673. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
674. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
675. [SidebarIterationCard](modules/SidebarIterationCard.md)
676. [AppSidebar](modules/AppSidebar.md)
677. [AppSidebar.test](modules/AppSidebar.test.md)
678. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
679. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
680. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
681. [usePlanningReadiness](modules/usePlanningReadiness.md)
682. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
683. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
684. [IdentityProvider](modules/IdentityProvider.md)
685. [UserSessionBadge](modules/UserSessionBadge.md)
686. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
687. [IdentityProvider.test](modules/IdentityProvider.test.md)
688. [useLiveWindow.test](modules/useLiveWindow.test.md)
689. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
690. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
691. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
692. [PlanMasterPage](modules/PlanMasterPage.md)
693. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
694. [PlanPage](modules/PlanPage.md)
695. [PlanPage.test](modules/PlanPage.test.md)
696. [PlanSharePage](modules/PlanSharePage.md)
697. [PlanSharePage.test](modules/PlanSharePage.test.md)
698. [graphLimitError](modules/graphLimitError.md)
699. [modelRouting](modules/modelRouting.md)
700. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
701. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
702. [modelRouting.test](modules/modelRouting.test.md)
703. [protectedQueries](modules/protectedQueries.md)
704. [AssignedAgentsSummary](modules/AssignedAgentsSummary.md)
705. [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md)
706. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
707. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
708. [AgentAccessPanel](modules/AgentAccessPanel.md)
709. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
710. [AgentModelAdministration](modules/AgentModelAdministration.md)
711. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
712. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
713. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
714. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
715. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
716. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
717. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
718. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
719. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
720. [AgentPipelinePage](modules/AgentPipelinePage.md)
721. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
722. [safeUrl](modules/safeUrl.md)
723. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
724. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
725. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
726. [TaskReadView](modules/TaskReadView.md)
727. [TaskReadView.test](modules/TaskReadView.test.md)
728. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
729. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
730. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
731. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
732. [CommandMenu](modules/CommandMenu.md)
733. [CommandMenu.test](modules/CommandMenu.test.md)
734. [ContextHelp](modules/ContextHelp.md)
735. [AppTopNav](modules/AppTopNav.md)
736. [AppShell](modules/AppShell.md)
737. [App](modules/App.md)
738. [AppShell.test](modules/AppShell.test.md)
739. [AppTopNav.test](modules/AppTopNav.test.md)
740. [ContextHelp.test](modules/ContextHelp.test.md)
741. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
742. [src_main](modules/src_main.md)
743. [SettingsPage](modules/SettingsPage.md)
744. [SettingsPage.test](modules/SettingsPage.test.md)
745. [taskFilterDefaults](modules/taskFilterDefaults.md)
746. [TaskFiltersBar](modules/TaskFiltersBar.md)
747. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
748. [taskViewState](modules/taskViewState.md)
749. [savedViewState](modules/savedViewState.md)
750. [SavedViewsControl](modules/SavedViewsControl.md)
751. [savedViewState.test](modules/savedViewState.test.md)
752. [taskFilters](modules/taskFilters.md)
753. [taskFilters.test](modules/taskFilters.test.md)
754. [teamMemberLabels](modules/teamMemberLabels.md)
755. [InitiativeForm](modules/InitiativeForm.md)
756. [RoadmapPage](modules/RoadmapPage.md)
757. [RoadmapPage.test](modules/RoadmapPage.test.md)
758. [templateDefaults](modules/templateDefaults.md)
759. [ProjectForm](modules/ProjectForm.md)
760. [ProjectForm.test](modules/ProjectForm.test.md)
761. [TaskForm](modules/TaskForm.md)
762. [GuardedTaskModal](modules/GuardedTaskModal.md)
763. [BacklogPanel](modules/BacklogPanel.md)
764. [CurrentTaskModal.test](modules/CurrentTaskModal.test.md)
765. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
766. [TaskEditModal](modules/TaskEditModal.md)
767. [GanttChart](modules/GanttChart.md)
768. [GanttChart.test](modules/GanttChart.test.md)
769. [TaskEditModal.test](modules/TaskEditModal.test.md)
770. [ProjectTaskTree](modules/ProjectTaskTree.md)
771. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
772. [TaskForm.test](modules/TaskForm.test.md)
773. [GanttPage](modules/GanttPage.md)
774. [GanttPage.test](modules/GanttPage.test.md)
775. [MyWorkPage](modules/MyWorkPage.md)
776. [MyWorkPage.test](modules/MyWorkPage.test.md)
777. [TriagePage](modules/TriagePage.md)
778. [visibleWork](modules/visibleWork.md)
779. [TaskList](modules/TaskList.md)
780. [TaskList.test](modules/TaskList.test.md)
781. [visibleWork.test](modules/visibleWork.test.md)
782. [workNumbers](modules/workNumbers.md)
783. [OnTrackSummary](modules/OnTrackSummary.md)
784. [StatusDistribution](modules/StatusDistribution.md)
785. [IterationOutlook.test](modules/IterationOutlook.test.md)
786. [IterationCapacityLine](modules/IterationCapacityLine.md)
787. [IterationList](modules/IterationList.md)
788. [IterationList.test](modules/IterationList.test.md)
789. [KanbanCard](modules/KanbanCard.md)
790. [KanbanColumn](modules/KanbanColumn.md)
791. [KanbanBoard](modules/KanbanBoard.md)
792. [KanbanBoard.test](modules/KanbanBoard.test.md)
793. [KanbanColumn.test](modules/KanbanColumn.test.md)
794. [WorkMetricsLine](modules/WorkMetricsLine.md)
795. [MetricCount.test](modules/MetricCount.test.md)
796. [TeamList](modules/TeamList.md)
797. [TeamList.test](modules/TeamList.test.md)
798. [AnalyticsPage](modules/AnalyticsPage.md)
799. [IterationsPage](modules/IterationsPage.md)
800. [OverviewPage](modules/OverviewPage.md)
801. [OverviewPage.test](modules/OverviewPage.test.md)
802. [ProjectDetailPage](modules/ProjectDetailPage.md)
803. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
804. [ProjectsPage](modules/ProjectsPage.md)
805. [ProjectsPage.test](modules/ProjectsPage.test.md)
806. [TasksPage](modules/TasksPage.md)
807. [TasksPage.test](modules/TasksPage.test.md)
808. [TeamPage](modules/TeamPage.md)
809. [tailwind.config](modules/tailwind.config.md)
810. [check-tailwind-classes](modules/check-tailwind-classes.md)
811. [vite.config](modules/vite.config.md)
812. [vitest.config](modules/vitest.config.md)
813. [create_agent_actor](modules/create_agent_actor.md)
814. [generate_workchord_keys](modules/generate_workchord_keys.md)
815. [setup_agent_team](modules/setup_agent_team.md)
816. [build_agent_skills](modules/build_agent_skills.md)
817. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
818. [android_qualification](modules/android_qualification.md)
819. [android_web_peer](modules/android_web_peer.md)
820. [apt_runtime](modules/apt_runtime.md)
821. [browser_performance](modules/browser_performance.md)
822. [browser_planning_inputs](modules/browser_planning_inputs.md)
823. [browser_worker](modules/browser_worker.md)
824. [browser_managed_work](modules/browser_managed_work.md)
825. [browser_write_readback](modules/browser_write_readback.md)
826. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
827. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
828. [ci_runtime](modules/ci_runtime.md)
829. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
830. [postgres_runtime](modules/postgres_runtime.md)
831. [run_android_checks](modules/run_android_checks.md)
832. [run_disposable_checks](modules/run_disposable_checks.md)
833. [serve_disposable_api](modules/serve_disposable_api.md)
834. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
835. [test_apt_runtime](modules/test_apt_runtime.md)
836. [test_ci_runtime](modules/test_ci_runtime.md)
837. [test_native_runtimes](modules/test_native_runtimes.md)
838. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
839. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
840. [generate_client_contract](modules/generate_client_contract.md)
841. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
842. [load_common](modules/load_common.md)
843. [collect](modules/collect.md)
844. [result](modules/result.md)
845. [compare](modules/compare.md)
846. [finalize](modules/finalize.md)
847. [qualify](modules/qualify.md)
848. [resilience](modules/resilience.md)
849. [run](modules/run.md)
850. [seal](modules/seal.md)
851. [seed](modules/seed.md)
852. [source_binding](modules/source_binding.md)
853. [local_baseline](modules/local_baseline.md)
854. [service_worksets](modules/service_worksets.md)
855. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
856. [isolated_rehearsal](modules/isolated_rehearsal.md)

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
