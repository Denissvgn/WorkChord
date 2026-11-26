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
28. [database_migration_manifest](modules/database_migration_manifest.md)
29. [database_migration_cutover](modules/database_migration_cutover.md)
30. [cli_cutover](modules/cli_cutover.md)
31. [database_migration_closeout](modules/database_migration_closeout.md)
32. [cli_closeout](modules/cli_closeout.md)
33. [project_identity](modules/project_identity.md)
34. [allocation_identity](modules/allocation_identity.md)
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
52. [20261120_0018_review_provenance](modules/20261120_0018_review_provenance.md)
53. [20261121_0019_execution_planning_window](modules/20261121_0019_execution_planning_window.md)
54. [20261121_0020_annual_calendar_coverage](modules/20261121_0020_annual_calendar_coverage.md)
55. [20261124_0021_maintenance_windows](modules/20261124_0021_maintenance_windows.md)
56. [20261124_0022_capacity_adjustments](modules/20261124_0022_capacity_adjustments.md)
57. [20261124_0023_task_replacements](modules/20261124_0023_task_replacements.md)
58. [20261124_0024_delivery_dependency_target_branch](modules/20261124_0024_delivery_dependency_target_branch.md)
59. [20261126_0025_catalog_local_first](modules/20261126_0025_catalog_local_first.md)
60. [query_limits](modules/query_limits.md)
61. [runtime_telemetry](modules/runtime_telemetry.md)
62. [database_runtime](modules/database_runtime.md)
63. [app_maintenance](modules/app_maintenance.md)
64. [mutation_versions](modules/mutation_versions.md)
65. [schemas_agent_connect](modules/schemas_agent_connect.md)
66. [schemas_agent_planning](modules/schemas_agent_planning.md)
67. [agent_skill_bundle](modules/agent_skill_bundle.md)
68. [agent_team_setup](modules/agent_team_setup.md)
69. [schemas_autonomy](modules/schemas_autonomy.md)
70. [schemas_common](modules/schemas_common.md)
71. [schemas_delivery_dependency](modules/schemas_delivery_dependency.md)
72. [delivery_metrics](modules/delivery_metrics.md)
73. [schemas_execution_usage](modules/schemas_execution_usage.md)
74. [schemas_github](modules/schemas_github.md)
75. [schemas_intake](modules/schemas_intake.md)
76. [schemas_label](modules/schemas_label.md)
77. [schemas_maintenance](modules/schemas_maintenance.md)
78. [schemas_plan_share](modules/schemas_plan_share.md)
79. [planning_inputs](modules/planning_inputs.md)
80. [schemas_calendar](modules/schemas_calendar.md)
81. [schemas_review_evidence](modules/schemas_review_evidence.md)
82. [schemas_saved_view](modules/schemas_saved_view.md)
83. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
84. [schemas_session](modules/schemas_session.md)
85. [snapshot](modules/snapshot.md)
86. [schemas_system_settings](modules/schemas_system_settings.md)
87. [schemas_email_settings](modules/schemas_email_settings.md)
88. [schemas_task_brief](modules/schemas_task_brief.md)
89. [schemas_llm](modules/schemas_llm.md)
90. [schemas_task_domain](modules/schemas_task_domain.md)
91. [schemas_task_replacement](modules/schemas_task_replacement.md)
92. [schemas_team](modules/schemas_team.md)
93. [schemas_template](modules/schemas_template.md)
94. [schemas_time_entry](modules/schemas_time_entry.md)
95. [time_report](modules/time_report.md)
96. [schemas_work_metrics](modules/schemas_work_metrics.md)
97. [schemas_iteration](modules/schemas_iteration.md)
98. [schemas_project](modules/schemas_project.md)
99. [schemas_release](modules/schemas_release.md)
100. [security](modules/security.md)
101. [server_features](modules/server_features.md)
102. [agent_routing_policy](modules/agent_routing_policy.md)
103. [agent_routing](modules/agent_routing.md)
104. [agent_routing_rollout](modules/agent_routing_rollout.md)
105. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
106. [routers_agent_connect](modules/routers_agent_connect.md)
107. [agent_team_credentials](modules/agent_team_credentials.md)
108. [bounded_scope_reads](modules/bounded_scope_reads.md)
109. [language_service](modules/language_service.md)
110. [plan_checkpoints](modules/plan_checkpoints.md)
111. [planning_input_context](modules/planning_input_context.md)
112. [planning_issues](modules/planning_issues.md)
113. [scheduling_rules_service](modules/scheduling_rules_service.md)
114. [upgrade_service](modules/upgrade_service.md)
115. [upgrade](modules/upgrade.md)
116. [settings_read](modules/settings_read.md)
117. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
118. [sql_semantics](modules/sql_semantics.md)
119. [exceptions](modules/exceptions.md)
120. [github_links](modules/github_links.md)
121. [text_similarity](modules/text_similarity.md)
122. [time](modules/time.md)
123. [observability](modules/observability.md)
124. [app_database](modules/app_database.md)
125. [models_autonomy](modules/models_autonomy.md)
126. [models_calendar](modules/models_calendar.md)
127. [models_capacity](modules/models_capacity.md)
128. [models_database_migration](modules/models_database_migration.md)
129. [models_delivery_dependency](modules/models_delivery_dependency.md)
130. [models_discussion](modules/models_discussion.md)
131. [models_execution_usage](modules/models_execution_usage.md)
132. [models_external_link](modules/models_external_link.md)
133. [models_github](modules/models_github.md)
134. [models_identity](modules/models_identity.md)
135. [models_iteration](modules/models_iteration.md)
136. [models_label](modules/models_label.md)
137. [models_maintenance](modules/models_maintenance.md)
138. [native_connection](modules/native_connection.md)
139. [models_outbound_webhook](modules/models_outbound_webhook.md)
140. [models_plan_share](modules/models_plan_share.md)
141. [models_release](modules/models_release.md)
142. [models_project](modules/models_project.md)
143. [models_request_source](modules/models_request_source.md)
144. [models_runtime_observation](modules/models_runtime_observation.md)
145. [models_saved_view](modules/models_saved_view.md)
146. [models_system_settings](modules/models_system_settings.md)
147. [models_task](modules/models_task.md)
148. [recovery](modules/recovery.md)
149. [models_task_brief](modules/models_task_brief.md)
150. [models_task_replacement](modules/models_task_replacement.md)
151. [task_status_log](modules/task_status_log.md)
152. [team_member](modules/team_member.md)
153. [models_agent](modules/models_agent.md)
154. [delivery_observation](modules/delivery_observation.md)
155. [models_template](modules/models_template.md)
156. [models_time_entry](modules/models_time_entry.md)
157. [models_triage](modules/models_triage.md)
158. [user_session](modules/user_session.md)
159. [models___init__](modules/models___init__.md)
160. [catalog](modules/catalog.md)
161. [database_migration_canonical](modules/database_migration_canonical.md)
162. [source](modules/source.md)
163. [transfer](modules/transfer.md)
164. [cli_database_migration](modules/cli_database_migration.md)
165. [database_migration___init__](modules/database_migration___init__.md)
166. [migrations_env](modules/migrations_env.md)
167. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
168. [calendar_rules](modules/calendar_rules.md)
169. [calendar_service](modules/calendar_service.md)
170. [calendars](modules/calendars.md)
171. [capacity_adjustments](modules/capacity_adjustments.md)
172. [capacity_service](modules/capacity_service.md)
173. [routers_capacity](modules/routers_capacity.md)
174. [delivery_dependency_service](modules/delivery_dependency_service.md)
175. [delivery_metrics_service](modules/delivery_metrics_service.md)
176. [dependency_order](modules/dependency_order.md)
177. [discussion_service](modules/discussion_service.md)
178. [execution_planning_window](modules/execution_planning_window.md)
179. [allocation_removal](modules/allocation_removal.md)
180. [identity_service](modules/identity_service.md)
181. [import_planning_service](modules/import_planning_service.md)
182. [iteration_date_move](modules/iteration_date_move.md)
183. [iteration_service](modules/iteration_service.md)
184. [iterations](modules/iterations.md)
185. [label_service](modules/label_service.md)
186. [labels](modules/labels.md)
187. [native_session_service](modules/native_session_service.md)
188. [saved_view_service](modules/saved_view_service.md)
189. [session_service](modules/session_service.md)
190. [http_authority](modules/http_authority.md)
191. [routers_identity](modules/routers_identity.md)
192. [saved_views](modules/saved_views.md)
193. [routers_session](modules/routers_session.md)
194. [task_brief_service](modules/task_brief_service.md)
195. [task_context_revision_service](modules/task_context_revision_service.md)
196. [task_domain_service](modules/task_domain_service.md)
197. [task_hierarchy_service](modules/task_hierarchy_service.md)
198. [task_recovery_service](modules/task_recovery_service.md)
199. [task_replacement_service](modules/task_replacement_service.md)
200. [task_timeline_service](modules/task_timeline_service.md)
201. [team_service](modules/team_service.md)
202. [routers_team](modules/routers_team.md)
203. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
204. [snapshot_service](modules/snapshot_service.md)
205. [plan_share_service](modules/plan_share_service.md)
206. [plan_shares](modules/plan_shares.md)
207. [template_service](modules/template_service.md)
208. [templates](modules/templates.md)
209. [time_entry_service](modules/time_entry_service.md)
210. [time_report_service](modules/time_report_service.md)
211. [services_work_metrics](modules/services_work_metrics.md)
212. [capacity_transfers](modules/capacity_transfers.md)
213. [import_parser](modules/import_parser.md)
214. [url_policy](modules/url_policy.md)
215. [schemas_external_link](modules/schemas_external_link.md)
216. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
217. [schemas_request_source](modules/schemas_request_source.md)
218. [schemas_task](modules/schemas_task.md)
219. [schemas_gantt](modules/schemas_gantt.md)
220. [task_detail](modules/task_detail.md)
221. [schemas_triage](modules/schemas_triage.md)
222. [schemas___init__](modules/schemas___init__.md)
223. [schemas_agent](modules/schemas_agent.md)
224. [agent_run_read](modules/agent_run_read.md)
225. [schemas_runtime_observation](modules/schemas_runtime_observation.md)
226. [agent_readiness](modules/agent_readiness.md)
227. [llm_service](modules/llm_service.md)
228. [review_provenance](modules/review_provenance.md)
229. [runtime_observation_service](modules/runtime_observation_service.md)
230. [system_settings_service](modules/system_settings_service.md)
231. [routers_system_settings](modules/routers_system_settings.md)
232. [email_settings_service](modules/email_settings_service.md)
233. [routers_email_settings](modules/routers_email_settings.md)
234. [notification_service](modules/notification_service.md)
235. [outbound_webhook_service](modules/outbound_webhook_service.md)
236. [worker](modules/worker.md)
237. [outbound_webhooks](modules/outbound_webhooks.md)
238. [external_link_service](modules/external_link_service.md)
239. [github_status_service](modules/github_status_service.md)
240. [github_reconciliation_service](modules/github_reconciliation_service.md)
241. [request_source_service](modules/request_source_service.md)
242. [request_sources](modules/request_sources.md)
243. [project_service](modules/project_service.md)
244. [task_detail_service](modules/task_detail_service.md)
245. [task_import_service](modules/task_import_service.md)
246. [task_service](modules/task_service.md)
247. [export](modules/export.md)
248. [snapshots](modules/snapshots.md)
249. [agent_routing_observability](modules/agent_routing_observability.md)
250. [agent_service](modules/agent_service.md)
251. [agent_skill_bundles](modules/agent_skill_bundles.md)
252. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
253. [agent_routing_service](modules/agent_routing_service.md)
254. [agent_team_setup_service](modules/agent_team_setup_service.md)
255. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
256. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
257. [execution_reconciliation](modules/execution_reconciliation.md)
258. [execution_usage_service](modules/execution_usage_service.md)
259. [routers_task_domain](modules/routers_task_domain.md)
260. [delivery_dependencies](modules/delivery_dependencies.md)
261. [routers_discussion](modules/routers_discussion.md)
262. [time_entries](modules/time_entries.md)
263. [agent_run_read_service](modules/agent_run_read_service.md)
264. [github_status_automation_service](modules/github_status_automation_service.md)
265. [maintenance_window_service](modules/maintenance_window_service.md)
266. [maintenance_windows](modules/maintenance_windows.md)
267. [release_service](modules/release_service.md)
268. [projects](modules/projects.md)
269. [services_review_evidence](modules/services_review_evidence.md)
270. [scheduler_service](modules/scheduler_service.md)
271. [routers_gantt](modules/routers_gantt.md)
272. [routers_llm](modules/routers_llm.md)
273. [agent_planning_service](modules/agent_planning_service.md)
274. [planning_window_reconciliation](modules/planning_window_reconciliation.md)
275. [retained_planning_output](modules/retained_planning_output.md)
276. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
277. [tasks](modules/tasks.md)
278. [task_status_service](modules/task_status_service.md)
279. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
280. [triage_service](modules/triage_service.md)
281. [routers_triage](modules/routers_triage.md)
282. [agent_work_service](modules/agent_work_service.md)
283. [mcp_agent_tools](modules/mcp_agent_tools.md)
284. [mcp_server](modules/mcp_server.md)
285. [routers_agent](modules/routers_agent.md)
286. [routers_agent_planning](modules/routers_agent_planning.md)
287. [agent_catalog](modules/agent_catalog.md)
288. [github_webhook_service](modules/github_webhook_service.md)
289. [routers_github](modules/routers_github.md)
290. [web_intake_service](modules/web_intake_service.md)
291. [routers_intake](modules/routers_intake.md)
292. [app_main](modules/app_main.md)
293. [routers___init__](modules/routers___init__.md)
294. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
295. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
296. [test_server_acceptance](modules/test_server_acceptance.md)
297. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
298. [test_work_package_service](modules/test_work_package_service.md)
299. [test_database_configuration](modules/test_database_configuration.md)
300. [test_deployment_topology](modules/test_deployment_topology.md)
301. [test_observability](modules/test_observability.md)
302. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
303. [test_query_boundaries](modules/test_query_boundaries.md)
304. [test_runtime_policy](modules/test_runtime_policy.md)
305. [test_schema_behavior](modules/test_schema_behavior.md)
306. [test_wal_archive_retention](modules/test_wal_archive_retention.md)
307. [test_cutover_evidence](modules/test_cutover_evidence.md)
308. [test_documentation_boundary](modules/test_documentation_boundary.md)
309. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
310. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
311. [test_source_preflight](modules/test_source_preflight.md)
312. [test_transfer_catalog](modules/test_transfer_catalog.md)
313. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
314. [0001_wave0_probe](modules/0001_wave0_probe.md)
315. [test_allocation_identity](modules/test_allocation_identity.md)
316. [test_annual_calendar_migration](modules/test_annual_calendar_migration.md)
317. [test_capacity_adjustment_migration](modules/test_capacity_adjustment_migration.md)
318. [test_delivery_target_branch_migration](modules/test_delivery_target_branch_migration.md)
319. [test_initial_schema](modules/test_initial_schema.md)
320. [test_profile_identity](modules/test_profile_identity.md)
321. [test_task_replacement_migration](modules/test_task_replacement_migration.md)
322. [test_android_cleanup](modules/test_android_cleanup.md)
323. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
324. [test_load_tooling](modules/test_load_tooling.md)
325. [test_local_baseline](modules/test_local_baseline.md)
326. [test_routing_evidence](modules/test_routing_evidence.md)
327. [support_database](modules/support_database.md)
328. [delivery](modules/delivery.md)
329. [factories](modules/factories.md)
330. [faults](modules/faults.md)
331. [runtime_peer](modules/runtime_peer.md)
332. [schema](modules/schema.md)
333. [support___init__](modules/support___init__.md)
334. [conftest](modules/conftest.md)
335. [test_github_closure_concurrency](modules/test_github_closure_concurrency.md)
336. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
337. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
338. [test_project_identity](modules/test_project_identity.md)
339. [test_project_identity_scope](modules/test_project_identity_scope.md)
340. [test_populated_history_migration](modules/test_populated_history_migration.md)
341. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
342. [test_upgrade_current_database_history](modules/test_upgrade_current_database_history.md)
343. [transactions](modules/transactions.md)
344. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
345. [test_agent_key_delivery](modules/test_agent_key_delivery.md)
346. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
347. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
348. [test_agent_routing_data](modules/test_agent_routing_data.md)
349. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
350. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
351. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
352. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
353. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
354. [test_agent_routing_service](modules/test_agent_routing_service.md)
355. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
356. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
357. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
358. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
359. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
360. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
361. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
362. [test_authority_migrations](modules/test_authority_migrations.md)
363. [test_capacity_contract](modules/test_capacity_contract.md)
364. [test_client_contract](modules/test_client_contract.md)
365. [test_database_harness](modules/test_database_harness.md)
366. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
367. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
368. [test_agent_discovery_report](modules/test_agent_discovery_report.md)
369. [test_agent_team_setup](modules/test_agent_team_setup.md)
370. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
371. [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md)
372. [test_analytics_scopes](modules/test_analytics_scopes.md)
373. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
374. [test_dependency_date_cascade](modules/test_dependency_date_cascade.md)
375. [test_deployment_configuration](modules/test_deployment_configuration.md)
376. [test_deployment_record](modules/test_deployment_record.md)
377. [test_effective_deferral](modules/test_effective_deferral.md)
378. [test_execution_usage](modules/test_execution_usage.md)
379. [test_execution_working_dates](modules/test_execution_working_dates.md)
380. [test_gantt_iteration_project](modules/test_gantt_iteration_project.md)
381. [test_github_reconciliation](modules/test_github_reconciliation.md)
382. [test_delivery_merge_prerequisites](modules/test_delivery_merge_prerequisites.md)
383. [test_harness_session_metadata](modules/test_harness_session_metadata.md)
384. [test_managed_authority](modules/test_managed_authority.md)
385. [test_allocation_recovery](modules/test_allocation_recovery.md)
386. [test_assignment_paging](modules/test_assignment_paging.md)
387. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
388. [test_delivery_prerequisite_tools](modules/test_delivery_prerequisite_tools.md)
389. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
390. [test_managed_worker_discovery](modules/test_managed_worker_discovery.md)
391. [test_mcp_proxy_host_header](modules/test_mcp_proxy_host_header.md)
392. [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md)
393. [test_metric_matches](modules/test_metric_matches.md)
394. [test_mobile_contract](modules/test_mobile_contract.md)
395. [test_mutation_versions](modules/test_mutation_versions.md)
396. [test_native_connections](modules/test_native_connections.md)
397. [test_observer_sessions](modules/test_observer_sessions.md)
398. [test_agdash_link_provider](modules/test_agdash_link_provider.md)
399. [test_person_assignment_reads](modules/test_person_assignment_reads.md)
400. [test_person_run_reads](modules/test_person_run_reads.md)
401. [test_pipeline_active_outside_run](modules/test_pipeline_active_outside_run.md)
402. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
403. [test_plan_shares](modules/test_plan_shares.md)
404. [test_planning_input_context](modules/test_planning_input_context.md)
405. [test_planning_issues](modules/test_planning_issues.md)
406. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
407. [test_process_roles](modules/test_process_roles.md)
408. [test_profile_capacity](modules/test_profile_capacity.md)
409. [test_annual_calendar_coverage](modules/test_annual_calendar_coverage.md)
410. [test_planning_read_models](modules/test_planning_read_models.md)
411. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
412. [test_profile_seed_key_binding](modules/test_profile_seed_key_binding.md)
413. [test_project_review_policy](modules/test_project_review_policy.md)
414. [test_project_working_timezone](modules/test_project_working_timezone.md)
415. [test_readiness_detail](modules/test_readiness_detail.md)
416. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
417. [test_run_detail_execution_provenance](modules/test_run_detail_execution_provenance.md)
418. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
419. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
420. [test_runtime_observations](modules/test_runtime_observations.md)
421. [test_saved_dependency_order](modules/test_saved_dependency_order.md)
422. [test_saved_view_service](modules/test_saved_view_service.md)
423. [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md)
424. [test_maintenance_window](modules/test_maintenance_window.md)
425. [test_scheduler_dependencies](modules/test_scheduler_dependencies.md)
426. [test_schedule_working_date](modules/test_schedule_working_date.md)
427. [test_server_features](modules/test_server_features.md)
428. [test_settings_read_access](modules/test_settings_read_access.md)
429. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
430. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
431. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
432. [test_task_domain](modules/test_task_domain.md)
433. [test_acceptance_attribution](modules/test_acceptance_attribution.md)
434. [test_delivery_metrics](modules/test_delivery_metrics.md)
435. [test_human_work_queries](modules/test_human_work_queries.md)
436. [test_task_discussion](modules/test_task_discussion.md)
437. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
438. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
439. [test_task_pagination](modules/test_task_pagination.md)
440. [test_team_member_agent_connected](modules/test_team_member_agent_connected.md)
441. [test_task_assignee_kind](modules/test_task_assignee_kind.md)
442. [test_team_pm_dispatch](modules/test_team_pm_dispatch.md)
443. [test_review_provenance](modules/test_review_provenance.md)
444. [test_capacity_adjustments](modules/test_capacity_adjustments.md)
445. [test_capacity_transfers](modules/test_capacity_transfers.md)
446. [test_iteration_date_move](modules/test_iteration_date_move.md)
447. [test_scoped_review_evidence](modules/test_scoped_review_evidence.md)
448. [test_routing_preview_focus](modules/test_routing_preview_focus.md)
449. [test_routing_preview_size](modules/test_routing_preview_size.md)
450. [test_routing_preview_team_scope](modules/test_routing_preview_team_scope.md)
451. [test_team_pm_recovery](modules/test_team_pm_recovery.md)
452. [test_execution_reconciliation](modules/test_execution_reconciliation.md)
453. [test_review_provenance_transports](modules/test_review_provenance_transports.md)
454. [test_execution_planning_window](modules/test_execution_planning_window.md)
455. [test_annual_calendar_work_control](modules/test_annual_calendar_work_control.md)
456. [test_manual_review_provenance](modules/test_manual_review_provenance.md)
457. [test_planning_window_digest_validation](modules/test_planning_window_digest_validation.md)
458. [test_pm_forecast_calendar](modules/test_pm_forecast_calendar.md)
459. [test_shadow_review_independence](modules/test_shadow_review_independence.md)
460. [test_supervised_shadow_rework](modules/test_supervised_shadow_rework.md)
461. [test_task_replacement](modules/test_task_replacement.md)
462. [test_replacement_carried_provenance](modules/test_replacement_carried_provenance.md)
463. [test_team_topology_read](modules/test_team_topology_read.md)
464. [test_time_entries](modules/test_time_entries.md)
465. [test_time_reports](modules/test_time_reports.md)
466. [test_unscheduled_tasks](modules/test_unscheduled_tasks.md)
467. [test_unused_allocation](modules/test_unused_allocation.md)
468. [test_verification_preview_history](modules/test_verification_preview_history.md)
469. [test_work_correctness](modules/test_work_correctness.md)
470. [test_work_delivery_links](modules/test_work_delivery_links.md)
471. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
472. [single-page-toolbar](modules/single-page-toolbar.md)
473. [eslint.config](modules/eslint.config.md)
474. [check-bundle-budget](modules/check-bundle-budget.md)
475. [check-query-feedback](modules/check-query-feedback.md)
476. [check-tailwind-classes](modules/check-tailwind-classes.md)
477. [check-task-selection-layout](modules/check-task-selection-layout.md)
478. [find-unread-i18n-keys](modules/find-unread-i18n-keys.md)
479. [find-unused-exports](modules/find-unused-exports.md)
480. [Checkbox](modules/Checkbox.md)
481. [CollapsibleSection](modules/CollapsibleSection.md)
482. [DisabledReason](modules/DisabledReason.md)
483. [Input](modules/Input.md)
484. [Input.test](modules/Input.test.md)
485. [Select](modules/Select.md)
486. [Textarea](modules/Textarea.md)
487. [buttonStyles](modules/buttonStyles.md)
488. [Button](modules/Button.md)
489. [Button.test](modules/Button.test.md)
490. [ButtonLink](modules/ButtonLink.md)
491. [ButtonLink.test](modules/ButtonLink.test.md)
492. [dialogLayer](modules/dialogLayer.md)
493. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
494. [Modal](modules/Modal.md)
495. [ConfirmDialog](modules/ConfirmDialog.md)
496. [formControlLabels.test](modules/formControlLabels.test.md)
497. [iconButtonTooltips.test](modules/iconButtonTooltips.test.md)
498. [leaveGuardBypass](modules/leaveGuardBypass.md)
499. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
500. [useConfirmDialog](modules/useConfirmDialog.md)
501. [LiveWindowStatus](modules/LiveWindowStatus.md)
502. [WorkFreshness](modules/WorkFreshness.md)
503. [toast](modules/toast.md)
504. [ToastProvider](modules/ToastProvider.md)
505. [ToastProvider.test](modules/ToastProvider.test.md)
506. [UnscheduledTasks](modules/UnscheduledTasks.md)
507. [AnnualCalendarFields](modules/AnnualCalendarFields.md)
508. [LabelChip](modules/LabelChip.md)
509. [BrandMark](modules/BrandMark.md)
510. [ScopePicker](modules/ScopePicker.md)
511. [commandMenuEvents](modules/commandMenuEvents.md)
512. [setupGuideEvents](modules/setupGuideEvents.md)
513. [ProjectIterationsTab](modules/ProjectIterationsTab.md)
514. [projectPortfolio](modules/projectPortfolio.md)
515. [AccessKeysSummary](modules/AccessKeysSummary.md)
516. [AgentTeamManifestPreview](modules/AgentTeamManifestPreview.md)
517. [ConstraintsPanel](modules/ConstraintsPanel.md)
518. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
519. [SettingsUnsavedBar](modules/SettingsUnsavedBar.md)
520. [WithheldValuesNote](modules/WithheldValuesNote.md)
521. [protectedQueryKeys](modules/protectedQueryKeys.md)
522. [settingsFieldLabels](modules/settingsFieldLabels.md)
523. [sharedUnlock](modules/sharedUnlock.md)
524. [ReadOnlyFieldset](modules/ReadOnlyFieldset.md)
525. [AssigneeSelect](modules/AssigneeSelect.md)
526. [claimTime](modules/claimTime.md)
527. [SortableTaskItem](modules/SortableTaskItem.md)
528. [TaskCreateSections](modules/TaskCreateSections.md)
529. [TaskViewOptions](modules/TaskViewOptions.md)
530. [taskDraftStorage](modules/taskDraftStorage.md)
531. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
532. [taskRowValues](modules/taskRowValues.md)
533. [taskSearchResults](modules/taskSearchResults.md)
534. [taskStateChip](modules/taskStateChip.md)
535. [taskViewSession](modules/taskViewSession.md)
536. [useDraftDismissal](modules/useDraftDismissal.md)
537. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
538. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
539. [useTaskSelection](modules/useTaskSelection.md)
540. [ModelBindings](modules/ModelBindings.md)
541. [directoryModel](modules/directoryModel.md)
542. [directoryModel.test](modules/directoryModel.test.md)
543. [FilterBar](modules/FilterBar.md)
544. [InlineEmptyState](modules/InlineEmptyState.md)
545. [MasterProgress](modules/MasterProgress.md)
546. [MasterProgress.test](modules/MasterProgress.test.md)
547. [OverflowMenu](modules/OverflowMenu.md)
548. [PageLayout](modules/PageLayout.md)
549. [PageToolbar.layout.test](modules/PageToolbar.layout.test.md)
550. [PageToolbar](modules/PageToolbar.md)
551. [PageToolbar.test](modules/PageToolbar.test.md)
552. [SectionCard](modules/SectionCard.md)
553. [SegmentedControl](modules/SegmentedControl.md)
554. [Select.test](modules/Select.test.md)
555. [SlideOverDrawer](modules/SlideOverDrawer.md)
556. [StickyRail](modules/StickyRail.md)
557. [ViewSwitch](modules/ViewSwitch.md)
558. [index](modules/index.md)
559. [tone](modules/tone.md)
560. [projectStatusStyles](modules/projectStatusStyles.md)
561. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
562. [Pill](modules/Pill.md)
563. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
564. [tone.test](modules/tone.test.md)
565. [agentDispatch](modules/agentDispatch.md)
566. [taskRowParts](modules/taskRowParts.md)
567. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
568. [connectAgent](modules/connectAgent.md)
569. [ConnectionSteps](modules/ConnectionSteps.md)
570. [manifestLocations](modules/manifestLocations.md)
571. [manifestLocations.test](modules/manifestLocations.test.md)
572. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
573. [AgentTeamStepList](modules/AgentTeamStepList.md)
574. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
575. [statusScopes](modules/statusScopes.md)
576. [statusScopes.test](modules/statusScopes.test.md)
577. [firstRunSteps](modules/firstRunSteps.md)
578. [getStartedVisibility](modules/getStartedVisibility.md)
579. [sampleProject.fixture](modules/sampleProject.fixture.md)
580. [sampleProjectStore](modules/sampleProjectStore.md)
581. [setupReturn](modules/setupReturn.md)
582. [accountMenuRow](modules/accountMenuRow.md)
583. [credentialRemount](modules/credentialRemount.md)
584. [identityContext](modules/identityContext.md)
585. [useProjectEditAccess](modules/useProjectEditAccess.md)
586. [mutationFeedback](modules/mutationFeedback.md)
587. [overviewTaskThread](modules/overviewTaskThread.md)
588. [planningMasters_masters](modules/planningMasters_masters.md)
589. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
590. [planningReturn](modules/planningReturn.md)
591. [planCheckpoints](modules/planCheckpoints.md)
592. [planCheckpoints.test](modules/planCheckpoints.test.md)
593. [planningTaskIssues](modules/planningTaskIssues.md)
594. [atRiskReasons](modules/atRiskReasons.md)
595. [AtRiskTaskReasons](modules/AtRiskTaskReasons.md)
596. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
597. [scheduleEvidence](modules/scheduleEvidence.md)
598. [useIterationPanels](modules/useIterationPanels.md)
599. [scopeStore](modules/scopeStore.md)
600. [taskTransitions](modules/taskTransitions.md)
601. [TaskRow](modules/TaskRow.md)
602. [taskTransitions.test](modules/taskTransitions.test.md)
603. [useLiveWindow](modules/useLiveWindow.md)
604. [workQueryFreshness](modules/workQueryFreshness.md)
605. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
606. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
607. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
608. [emptyStates](modules/emptyStates.md)
609. [emptyStates.test](modules/emptyStates.test.md)
610. [firstRun](modules/firstRun.md)
611. [landing.en](modules/landing.en.md)
612. [landing.ru](modules/landing.ru.md)
613. [literals.ru](modules/literals.ru.md)
614. [pagination](modules/pagination.md)
615. [plan.ru](modules/plan.ru.md)
616. [planSchedule](modules/planSchedule.md)
617. [planWork](modules/planWork.md)
618. [planningInputMessages](modules/planningInputMessages.md)
619. [surfaces.ru](modules/surfaces.ru.md)
620. [teamwork.en](modules/teamwork.en.md)
621. [teamwork.ru](modules/teamwork.ru.md)
622. [timeEntries](modules/timeEntries.md)
623. [resources.en](modules/resources.en.md)
624. [agentDispatch.test](modules/agentDispatch.test.md)
625. [englishNames.test](modules/englishNames.test.md)
626. [i18n](modules/i18n.md)
627. [settingsFieldLabels.test](modules/settingsFieldLabels.test.md)
628. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
629. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
630. [triageUtils](modules/triageUtils.md)
631. [StatusPill](modules/StatusPill.md)
632. [TriageToolbar](modules/TriageToolbar.md)
633. [dateLocale](modules/dateLocale.md)
634. [InteractiveCalendar](modules/InteractiveCalendar.md)
635. [formatsAndWording.test](modules/formatsAndWording.test.md)
636. [planWork.test](modules/planWork.test.md)
637. [resources.ru](modules/resources.ru.md)
638. [i18n.test](modules/i18n.test.md)
639. [russianNames.test](modules/russianNames.test.md)
640. [schedulingDisplay](modules/schedulingDisplay.md)
641. [seedDisplay](modules/seedDisplay.md)
642. [SavedViewsControl](modules/SavedViewsControl.md)
643. [seedDisplay.test](modules/seedDisplay.test.md)
644. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
645. [destinations](modules/destinations.md)
646. [legacyPaths](modules/legacyPaths.md)
647. [LegacyRedirect](modules/LegacyRedirect.md)
648. [CalendarRedirect.test](modules/CalendarRedirect.test.md)
649. [LegacyRedirect.test](modules/LegacyRedirect.test.md)
650. [legacyPaths.check.test](modules/legacyPaths.check.test.md)
651. [routeModules](modules/routeModules.md)
652. [DocumentMetadata](modules/DocumentMetadata.md)
653. [destinations.test](modules/destinations.test.md)
654. [helpContexts](modules/helpContexts.md)
655. [helpContexts.test](modules/helpContexts.test.md)
656. [scopeParams](modules/scopeParams.md)
657. [namedIteration](modules/namedIteration.md)
658. [namedIteration.test](modules/namedIteration.test.md)
659. [workScope](modules/workScope.md)
660. [useScopeLink](modules/useScopeLink.md)
661. [Breadcrumbs](modules/Breadcrumbs.md)
662. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
663. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
664. [PlanReturnBar](modules/PlanReturnBar.md)
665. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
666. [PlanningWorkflowHelpContent](modules/PlanningWorkflowHelpContent.md)
667. [TaskWorkflowHelpContent](modules/TaskWorkflowHelpContent.md)
668. [SetupReturnBar](modules/SetupReturnBar.md)
669. [useScopeLink.test](modules/useScopeLink.test.md)
670. [workScope.test](modules/workScope.test.md)
671. [scopeParams.check.test](modules/scopeParams.check.test.md)
672. [workspaces](modules/workspaces.md)
673. [workspaces.test](modules/workspaces.test.md)
674. [LandingPage](modules/LandingPage.md)
675. [NotFoundPage](modules/NotFoundPage.md)
676. [healthService](modules/healthService.md)
677. [SystemHealthPanel](modules/SystemHealthPanel.md)
678. [iterationStore](modules/iterationStore.md)
679. [iterationStore.test](modules/iterationStore.test.md)
680. [themeStore](modules/themeStore.md)
681. [BareLayout](modules/BareLayout.md)
682. [colorRoles.test](modules/colorRoles.test.md)
683. [planning-masters.test](modules/planning-masters.test.md)
684. [accessibilityInvariants](modules/accessibilityInvariants.md)
685. [modelAwareRouting](modules/modelAwareRouting.md)
686. [taskDetail](modules/taskDetail.md)
687. [lintRules.test](modules/lintRules.test.md)
688. [pageChrome](modules/pageChrome.md)
689. [renderWithProviders](modules/renderWithProviders.md)
690. [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md)
691. [UnscheduledTasks.test](modules/UnscheduledTasks.test.md)
692. [BareLayout.test](modules/BareLayout.test.md)
693. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
694. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
695. [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md)
696. [TaskRow.test](modules/TaskRow.test.md)
697. [FilterBar.test](modules/FilterBar.test.md)
698. [OverflowMenu.test](modules/OverflowMenu.test.md)
699. [PageLayout.test](modules/PageLayout.test.md)
700. [ViewSwitch.test](modules/ViewSwitch.test.md)
701. [LandingPage.test](modules/LandingPage.test.md)
702. [renderWithProviders.test](modules/renderWithProviders.test.md)
703. [routeRegistry](modules/routeRegistry.md)
704. [setup](modules/setup.md)
705. [types_agent](modules/types_agent.md)
706. [analyticsScope](modules/analyticsScope.md)
707. [types_calendar](modules/types_calendar.md)
708. [deliveryMetrics](modules/deliveryMetrics.md)
709. [emailSettings](modules/emailSettings.md)
710. [executionUsage](modules/executionUsage.md)
711. [types_gantt](modules/types_gantt.md)
712. [types_github](modules/types_github.md)
713. [types_iteration](modules/types_iteration.md)
714. [types_label](modules/types_label.md)
715. [outboundWebhook](modules/outboundWebhook.md)
716. [types_project](modules/types_project.md)
717. [types_release](modules/types_release.md)
718. [requestSource](modules/requestSource.md)
719. [savedView](modules/savedView.md)
720. [schedulingRules](modules/schedulingRules.md)
721. [EffortModifierCard](modules/EffortModifierCard.md)
722. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
723. [SchedulingPassCard](modules/SchedulingPassCard.md)
724. [schedulingSearchLabels.test](modules/schedulingSearchLabels.test.md)
725. [systemSettings](modules/systemSettings.md)
726. [types_task](modules/types_task.md)
727. [types_team](modules/types_team.md)
728. [types_template](modules/types_template.md)
729. [types_triage](modules/types_triage.md)
730. [workMetrics](modules/workMetrics.md)
731. [agentAccess](modules/agentAccess.md)
732. [useAgentAccess](modules/useAgentAccess.md)
733. [apiError](modules/apiError.md)
734. [QueryState](modules/QueryState.md)
735. [taskEditorContract](modules/taskEditorContract.md)
736. [TaskBriefEditor](modules/TaskBriefEditor.md)
737. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
738. [TriageDraftPreview](modules/TriageDraftPreview.md)
739. [MutationSuccessFeedback](modules/MutationSuccessFeedback.md)
740. [mutationFeedback.test](modules/mutationFeedback.test.md)
741. [adminAccess](modules/adminAccess.md)
742. [OperatorIdentityNotice](modules/OperatorIdentityNotice.md)
743. [useAdminAccess](modules/useAdminAccess.md)
744. [api](modules/api.md)
745. [identityService](modules/identityService.md)
746. [NativeConnectionPage](modules/NativeConnectionPage.md)
747. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
748. [adminAccessService](modules/adminAccessService.md)
749. [AdminAccessPanel](modules/AdminAccessPanel.md)
750. [AdminAccessGate](modules/AdminAccessGate.md)
751. [AdminAccessGate.test](modules/AdminAccessGate.test.md)
752. [agentService](modules/agentService.md)
753. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
754. [useWaitingAgents](modules/useWaitingAgents.md)
755. [agentService.test](modules/agentService.test.md)
756. [deliveryMetricsService](modules/deliveryMetricsService.md)
757. [discussionService](modules/discussionService.md)
758. [emailSettingsService](modules/emailSettingsService.md)
759. [executionUsageService](modules/executionUsageService.md)
760. [ganttService](modules/ganttService.md)
761. [githubService](modules/githubService.md)
762. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
763. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
764. [labelService](modules/labelService.md)
765. [LabelSelector](modules/LabelSelector.md)
766. [outboundWebhookService](modules/outboundWebhookService.md)
767. [planShareService](modules/planShareService.md)
768. [planningInputService](modules/planningInputService.md)
769. [usePlanningObservation](modules/usePlanningObservation.md)
770. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
771. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
772. [calendarService](modules/calendarService.md)
773. [WorkCalendarSettings](modules/WorkCalendarSettings.md)
774. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
775. [WorkCalendarSettings.test](modules/WorkCalendarSettings.test.md)
776. [PersonCapacity](modules/PersonCapacity.md)
777. [PersonCapacity.test](modules/PersonCapacity.test.md)
778. [exportService](modules/exportService.md)
779. [IterationImportDialog](modules/IterationImportDialog.md)
780. [iterationService](modules/iterationService.md)
781. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
782. [planProgress.test](modules/planProgress.test.md)
783. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
784. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
785. [useWorkScope](modules/useWorkScope.md)
786. [useAnalyticsScope](modules/useAnalyticsScope.md)
787. [useWorkScope.test](modules/useWorkScope.test.md)
788. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
789. [IdentityProvider](modules/IdentityProvider.md)
790. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
791. [useLiveWindow.test](modules/useLiveWindow.test.md)
792. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
793. [planningInputService.test](modules/planningInputService.test.md)
794. [projectService](modules/projectService.md)
795. [AddMilestoneModal](modules/AddMilestoneModal.md)
796. [SetDatesPopover](modules/SetDatesPopover.md)
797. [CreateProjectModal](modules/CreateProjectModal.md)
798. [FirstRunLanding](modules/FirstRunLanding.md)
799. [useFirstRunProgress](modules/useFirstRunProgress.md)
800. [useGetStarted](modules/useGetStarted.md)
801. [useNextSetupAction](modules/useNextSetupAction.md)
802. [NextStepEmptyState](modules/NextStepEmptyState.md)
803. [NextStepEmptyState.test](modules/NextStepEmptyState.test.md)
804. [releaseService](modules/releaseService.md)
805. [ReleaseForm](modules/ReleaseForm.md)
806. [requestSourceService](modules/requestSourceService.md)
807. [savedViewService](modules/savedViewService.md)
808. [schedulingRulesService](modules/schedulingRulesService.md)
809. [sessionService](modules/sessionService.md)
810. [snapshotService](modules/snapshotService.md)
811. [snapshotVersions.test](modules/snapshotVersions.test.md)
812. [systemSettingsService](modules/systemSettingsService.md)
813. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
814. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
815. [taskService](modules/taskService.md)
816. [DeliveryDependencies](modules/DeliveryDependencies.md)
817. [DeliveryDependencies.test](modules/DeliveryDependencies.test.md)
818. [ImportTasksModal](modules/ImportTasksModal.md)
819. [MetricCount](modules/MetricCount.md)
820. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
821. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
822. [TaskContextSummary](modules/TaskContextSummary.md)
823. [TaskDependencySelector](modules/TaskDependencySelector.md)
824. [TaskMergeDialog](modules/TaskMergeDialog.md)
825. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
826. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
827. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
828. [useAgentRowFacts](modules/useAgentRowFacts.md)
829. [useTaskReviewer](modules/useTaskReviewer.md)
830. [TaskReviewer](modules/TaskReviewer.md)
831. [TaskWorkPanel](modules/TaskWorkPanel.md)
832. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
833. [TriageActionModal](modules/TriageActionModal.md)
834. [overviewBacklog](modules/overviewBacklog.md)
835. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
836. [teamService](modules/teamService.md)
837. [TeamForm](modules/TeamForm.md)
838. [TeamForm.test](modules/TeamForm.test.md)
839. [capacityMutations](modules/capacityMutations.md)
840. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
841. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
842. [GanttBarInputs](modules/GanttBarInputs.md)
843. [AssigneePicker](modules/AssigneePicker.md)
844. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
845. [TaskBulkOperationsPanel.test](modules/TaskBulkOperationsPanel.test.md)
846. [TaskSelectionBar](modules/TaskSelectionBar.md)
847. [useTaskRowEdits](modules/useTaskRowEdits.md)
848. [useIterationRowData](modules/useIterationRowData.md)
849. [useTaskAssigneeDisplay](modules/useTaskAssigneeDisplay.md)
850. [TaskAssigneeDisplay](modules/TaskAssigneeDisplay.md)
851. [KanbanCard](modules/KanbanCard.md)
852. [KanbanColumn](modules/KanbanColumn.md)
853. [KanbanColumn.test](modules/KanbanColumn.test.md)
854. [ImportTeamModal](modules/ImportTeamModal.md)
855. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
856. [VacationCsvImport](modules/VacationCsvImport.md)
857. [sampleProject](modules/sampleProject.md)
858. [SampleProjectAction](modules/SampleProjectAction.md)
859. [LocalProfilePicker](modules/LocalProfilePicker.md)
860. [GetStartedPanel](modules/GetStartedPanel.md)
861. [AccountMenu](modules/AccountMenu.md)
862. [UserSessionBadge](modules/UserSessionBadge.md)
863. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
864. [IdentityProvider.test](modules/IdentityProvider.test.md)
865. [usePlanScheduleWorkloads](modules/usePlanScheduleWorkloads.md)
866. [templateService](modules/templateService.md)
867. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
868. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
869. [timeEntryService](modules/timeEntryService.md)
870. [useTimeEntries](modules/useTimeEntries.md)
871. [timeEntryService.test](modules/timeEntryService.test.md)
872. [triageService](modules/triageService.md)
873. [AppSidebar](modules/AppSidebar.md)
874. [AppSidebar.planProgress.test](modules/AppSidebar.planProgress.test.md)
875. [AppSidebar.test](modules/AppSidebar.test.md)
876. [QuickCapture](modules/QuickCapture.md)
877. [QuickCapture.test](modules/QuickCapture.test.md)
878. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
879. [usePlanningReadiness](modules/usePlanningReadiness.md)
880. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
881. [planningScope.test](modules/planningScope.test.md)
882. [workspaceApi](modules/workspaceApi.md)
883. [pageChrome.test](modules/pageChrome.test.md)
884. [copyText](modules/copyText.md)
885. [focusLifecycle](modules/focusLifecycle.md)
886. [focusLifecycle.test](modules/focusLifecycle.test.md)
887. [formatDate](modules/formatDate.md)
888. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
889. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
890. [VacationManager](modules/VacationManager.md)
891. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
892. [IterationForm](modules/IterationForm.md)
893. [IterationEditorDrawer](modules/IterationEditorDrawer.md)
894. [IterationForm.test](modules/IterationForm.test.md)
895. [ScopeBar](modules/ScopeBar.md)
896. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
897. [ScopeBar.test](modules/ScopeBar.test.md)
898. [NotificationsPanel](modules/NotificationsPanel.md)
899. [PlanIterationCheckpoint](modules/PlanIterationCheckpoint.md)
900. [PlanShareSection](modules/PlanShareSection.md)
901. [PlanReviewSection](modules/PlanReviewSection.md)
902. [PlanShareSection.test](modules/PlanShareSection.test.md)
903. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
904. [ConnectedReadersPanel](modules/ConnectedReadersPanel.md)
905. [ConnectedReadersPanel.test](modules/ConnectedReadersPanel.test.md)
906. [GitHubReconciliationPanel](modules/GitHubReconciliationPanel.md)
907. [GitHubReconciliationPanel.test](modules/GitHubReconciliationPanel.test.md)
908. [StatusChangeControl](modules/StatusChangeControl.md)
909. [TaskDiscussion](modules/TaskDiscussion.md)
910. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
911. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
912. [TimeEntriesReport](modules/TimeEntriesReport.md)
913. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
914. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
915. [AgentManifestWorkflow](modules/AgentManifestWorkflow.md)
916. [AgentManifestWorkflow.test](modules/AgentManifestWorkflow.test.md)
917. [ModelCatalog](modules/ModelCatalog.md)
918. [TeamProfileManager](modules/TeamProfileManager.md)
919. [TeamDirectory](modules/TeamDirectory.md)
920. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
921. [TriageRow](modules/TriageRow.md)
922. [TriageList](modules/TriageList.md)
923. [TriageList.test](modules/TriageList.test.md)
924. [TriageSuggestions](modules/TriageSuggestions.md)
925. [planEvidence](modules/planEvidence.md)
926. [PlanSharePage](modules/PlanSharePage.md)
927. [PlanSharePage.test](modules/PlanSharePage.test.md)
928. [scopedPageRender.test](modules/scopedPageRender.test.md)
929. [graphLimitError](modules/graphLimitError.md)
930. [modelRouting](modules/modelRouting.md)
931. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
932. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
933. [ConnectAgentSteps](modules/ConnectAgentSteps.md)
934. [ConnectAgentSteps.test](modules/ConnectAgentSteps.test.md)
935. [modelRouting.test](modules/modelRouting.test.md)
936. [protectedQueries](modules/protectedQueries.md)
937. [AssignedAgentsSummary](modules/AssignedAgentsSummary.md)
938. [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md)
939. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
940. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
941. [AgentAccessPanel](modules/AgentAccessPanel.md)
942. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
943. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
944. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
945. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
946. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
947. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
948. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
949. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
950. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
951. [PipelineTaskEvidence](modules/PipelineTaskEvidence.md)
952. [usePipeline](modules/usePipeline.md)
953. [AgentModelAdministration](modules/AgentModelAdministration.md)
954. [PipelineTaskEvidence.test](modules/PipelineTaskEvidence.test.md)
955. [TeamPage](modules/TeamPage.md)
956. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
957. [IdentityProvider.keepRoute.test](modules/IdentityProvider.keepRoute.test.md)
958. [TeamPage.test](modules/TeamPage.test.md)
959. [TeamPage.transport.test](modules/TeamPage.transport.test.md)
960. [safeUrl](modules/safeUrl.md)
961. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
962. [ProjectRequestsTab](modules/ProjectRequestsTab.md)
963. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
964. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
965. [TaskReadView](modules/TaskReadView.md)
966. [TaskReadView.brief.test](modules/TaskReadView.brief.test.md)
967. [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md)
968. [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md)
969. [TaskReadView.test](modules/TaskReadView.test.md)
970. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
971. [TriageDetailPanel](modules/TriageDetailPanel.md)
972. [TriageConvertSource](modules/TriageConvertSource.md)
973. [ConvertTriageDrawer](modules/ConvertTriageDrawer.md)
974. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
975. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
976. [CommandMenu](modules/CommandMenu.md)
977. [CommandMenu.test](modules/CommandMenu.test.md)
978. [ContextHelp](modules/ContextHelp.md)
979. [AppTopNav](modules/AppTopNav.md)
980. [AppShell](modules/AppShell.md)
981. [App](modules/App.md)
982. [App.legacyRoutes.test](modules/App.legacyRoutes.test.md)
983. [AppShell.test](modules/AppShell.test.md)
984. [AppTopNav.test](modules/AppTopNav.test.md)
985. [ContextHelp.test](modules/ContextHelp.test.md)
986. [shellViewport.test](modules/shellViewport.test.md)
987. [AccountMenu.test](modules/AccountMenu.test.md)
988. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
989. [src_main](modules/src_main.md)
990. [SettingsPage](modules/SettingsPage.md)
991. [SettingsPage.calendar.test](modules/SettingsPage.calendar.test.md)
992. [SettingsPage.labels.test](modules/SettingsPage.labels.test.md)
993. [SettingsPage.readOnlyPanels.test](modules/SettingsPage.readOnlyPanels.test.md)
994. [SettingsPage.test](modules/SettingsPage.test.md)
995. [SettingsPage.unlock.test](modules/SettingsPage.unlock.test.md)
996. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
997. [taskFilterDefaults](modules/taskFilterDefaults.md)
998. [TaskFiltersBar](modules/TaskFiltersBar.md)
999. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
1000. [taskViewParams](modules/taskViewParams.md)
1001. [taskViewParams.test](modules/taskViewParams.test.md)
1002. [taskViewState](modules/taskViewState.md)
1003. [savedViewState](modules/savedViewState.md)
1004. [useSavedViewManager](modules/useSavedViewManager.md)
1005. [savedViewState.test](modules/savedViewState.test.md)
1006. [taskFilters](modules/taskFilters.md)
1007. [taskFilters.test](modules/taskFilters.test.md)
1008. [teamMemberLabels](modules/teamMemberLabels.md)
1009. [InitiativeForm](modules/InitiativeForm.md)
1010. [InitiativeGroupHeader](modules/InitiativeGroupHeader.md)
1011. [RoadmapView](modules/RoadmapView.md)
1012. [RoadmapView.test](modules/RoadmapView.test.md)
1013. [sampleProject.test](modules/sampleProject.test.md)
1014. [templateDefaults](modules/templateDefaults.md)
1015. [ProjectForm](modules/ProjectForm.md)
1016. [ProjectForm.test](modules/ProjectForm.test.md)
1017. [TaskForm](modules/TaskForm.md)
1018. [AssigneePicker.test](modules/AssigneePicker.test.md)
1019. [GuardedTaskDrawer](modules/GuardedTaskDrawer.md)
1020. [BacklogPanel](modules/BacklogPanel.md)
1021. [CurrentTaskDrawer.test](modules/CurrentTaskDrawer.test.md)
1022. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
1023. [TaskEditDrawer](modules/TaskEditDrawer.md)
1024. [GanttChart](modules/GanttChart.md)
1025. [GanttChart.test](modules/GanttChart.test.md)
1026. [TaskEditDrawer.test](modules/TaskEditDrawer.test.md)
1027. [ProjectTaskTree](modules/ProjectTaskTree.md)
1028. [ProjectTasksTab](modules/ProjectTasksTab.md)
1029. [ProjectTaskTree.test](modules/ProjectTaskTree.test.md)
1030. [TaskEditorDrawer.flow.test](modules/TaskEditorDrawer.flow.test.md)
1031. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
1032. [TaskForm.test](modules/TaskForm.test.md)
1033. [TaskFormSections.test](modules/TaskFormSections.test.md)
1034. [CreateTriageDrawer](modules/CreateTriageDrawer.md)
1035. [GanttPage](modules/GanttPage.md)
1036. [GanttPage.test](modules/GanttPage.test.md)
1037. [MyWorkPage](modules/MyWorkPage.md)
1038. [MyWorkPage.test](modules/MyWorkPage.test.md)
1039. [TriagePage](modules/TriagePage.md)
1040. [TriagePage.test](modules/TriagePage.test.md)
1041. [ganttChrome.test](modules/ganttChrome.test.md)
1042. [visibleWork](modules/visibleWork.md)
1043. [KanbanBoard](modules/KanbanBoard.md)
1044. [KanbanBoard.test](modules/KanbanBoard.test.md)
1045. [TaskList](modules/TaskList.md)
1046. [TaskList.test](modules/TaskList.test.md)
1047. [overviewSignals](modules/overviewSignals.md)
1048. [PipelineView](modules/PipelineView.md)
1049. [assigneeDisplay.test](modules/assigneeDisplay.test.md)
1050. [overviewSignals.test](modules/overviewSignals.test.md)
1051. [TasksPage](modules/TasksPage.md)
1052. [backlogScope.test](modules/backlogScope.test.md)
1053. [TasksPage.board.test](modules/TasksPage.board.test.md)
1054. [TasksPage.pipeline.test](modules/TasksPage.pipeline.test.md)
1055. [TasksPage.test](modules/TasksPage.test.md)
1056. [TasksPage.toolbar.test](modules/TasksPage.toolbar.test.md)
1057. [visibleWork.test](modules/visibleWork.test.md)
1058. [workNumbers](modules/workNumbers.md)
1059. [OnTrackSummary](modules/OnTrackSummary.md)
1060. [StatusDistribution](modules/StatusDistribution.md)
1061. [IterationOutlook.test](modules/IterationOutlook.test.md)
1062. [CapacityTable](modules/CapacityTable.md)
1063. [TeamList](modules/TeamList.md)
1064. [CapacitySection](modules/CapacitySection.md)
1065. [CapacitySection.test](modules/CapacitySection.test.md)
1066. [IterationCapacityLine](modules/IterationCapacityLine.md)
1067. [TeamList.test](modules/TeamList.test.md)
1068. [IterationList](modules/IterationList.md)
1069. [AllIterationsDrawer](modules/AllIterationsDrawer.md)
1070. [AllIterationsDrawer.test](modules/AllIterationsDrawer.test.md)
1071. [PlanBlockersSection](modules/PlanBlockersSection.md)
1072. [PlanIterationDrawers](modules/PlanIterationDrawers.md)
1073. [PlanScheduleSection](modules/PlanScheduleSection.md)
1074. [PlanWorkSection](modules/PlanWorkSection.md)
1075. [projectDetailShared](modules/projectDetailShared.md)
1076. [MilestoneFormDrawer](modules/MilestoneFormDrawer.md)
1077. [MilestonesSection](modules/MilestonesSection.md)
1078. [PostUpdateDrawer](modules/PostUpdateDrawer.md)
1079. [ProjectHeaderFields](modules/ProjectHeaderFields.md)
1080. [ProjectReleasesTab](modules/ProjectReleasesTab.md)
1081. [ProjectSummaryTab](modules/ProjectSummaryTab.md)
1082. [ProjectUpdatesTab](modules/ProjectUpdatesTab.md)
1083. [WorkMetricsLine](modules/WorkMetricsLine.md)
1084. [MetricCount.test](modules/MetricCount.test.md)
1085. [planningLinks.test](modules/planningLinks.test.md)
1086. [AnalyticsPage](modules/AnalyticsPage.md)
1087. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
1088. [scopedPages.test](modules/scopedPages.test.md)
1089. [AnalyticsPage.test](modules/AnalyticsPage.test.md)
1090. [OverviewPage](modules/OverviewPage.md)
1091. [GetStartedPanel.test](modules/GetStartedPanel.test.md)
1092. [OverviewPage.test](modules/OverviewPage.test.md)
1093. [PlanPage](modules/PlanPage.md)
1094. [planProgressPlacement.test](modules/planProgressPlacement.test.md)
1095. [GetStartedFlow.test](modules/GetStartedFlow.test.md)
1096. [PlanIterations.test](modules/PlanIterations.test.md)
1097. [PlanPage.test](modules/PlanPage.test.md)
1098. [ProjectDetailPage](modules/ProjectDetailPage.md)
1099. [ProjectDetailPage.test](modules/ProjectDetailPage.test.md)
1100. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
1101. [ProjectReleaseDetailPage.test](modules/ProjectReleaseDetailPage.test.md)
1102. [ProjectsPage](modules/ProjectsPage.md)
1103. [ProjectsPage.test](modules/ProjectsPage.test.md)
1104. [destinationEmptyStates.test](modules/destinationEmptyStates.test.md)
1105. [vite.config](modules/vite.config.md)
1106. [vitest.config](modules/vitest.config.md)
1107. [create_agent_actor](modules/create_agent_actor.md)
1108. [generate_workchord_keys](modules/generate_workchord_keys.md)
1109. [setup_agent_team](modules/setup_agent_team.md)
1110. [build_agent_skills](modules/build_agent_skills.md)
1111. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
1112. [android_qualification](modules/android_qualification.md)
1113. [android_web_peer](modules/android_web_peer.md)
1114. [apt_runtime](modules/apt_runtime.md)
1115. [browser_performance](modules/browser_performance.md)
1116. [browser_planning_inputs](modules/browser_planning_inputs.md)
1117. [browser_worker](modules/browser_worker.md)
1118. [browser_managed_work](modules/browser_managed_work.md)
1119. [browser_write_readback](modules/browser_write_readback.md)
1120. [check_markdown_links](modules/check_markdown_links.md)
1121. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
1122. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
1123. [ci_runtime](modules/ci_runtime.md)
1124. [classify_change_scope](modules/classify_change_scope.md)
1125. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
1126. [postgres_runtime](modules/postgres_runtime.md)
1127. [run_android_checks](modules/run_android_checks.md)
1128. [run_disposable_checks](modules/run_disposable_checks.md)
1129. [serve_disposable_api](modules/serve_disposable_api.md)
1130. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
1131. [test_apt_runtime](modules/test_apt_runtime.md)
1132. [test_check_markdown_links](modules/test_check_markdown_links.md)
1133. [test_ci_runtime](modules/test_ci_runtime.md)
1134. [test_classify_change_scope](modules/test_classify_change_scope.md)
1135. [test_native_runtimes](modules/test_native_runtimes.md)
1136. [test_wiki_lock_root_preflight](modules/test_wiki_lock_root_preflight.md)
1137. [wiki_lock_root_preflight](modules/wiki_lock_root_preflight.md)
1138. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
1139. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
1140. [generate_client_contract](modules/generate_client_contract.md)
1141. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
1142. [load_common](modules/load_common.md)
1143. [collect](modules/collect.md)
1144. [result](modules/result.md)
1145. [compare](modules/compare.md)
1146. [finalize](modules/finalize.md)
1147. [qualify](modules/qualify.md)
1148. [resilience](modules/resilience.md)
1149. [run](modules/run.md)
1150. [seal](modules/seal.md)
1151. [seed](modules/seed.md)
1152. [source_binding](modules/source_binding.md)
1153. [local_baseline](modules/local_baseline.md)
1154. [service_worksets](modules/service_worksets.md)
1155. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
1156. [isolated_rehearsal](modules/isolated_rehearsal.md)
1157. [seed_adoption_env](modules/seed_adoption_env.md)
1158. [write_deployment_record](modules/write_deployment_record.md)

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
| [app_main](modules/app_main.md) | `settings = get_settings`, `app = FastAPI`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.add_middleware`, `app.add_middleware`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `mount_mcp_http` |
| [app_maintenance](modules/app_maintenance.md) | `SAFE_HTTP_METHODS = frozenset`, `_CORRELATION_ID_PATTERN = re.compile` |
| [mcp_agent_tools](modules/mcp_agent_tools.md) | `_AGENT_ASSIGNMENT_CREATE_ADAPTER = TypeAdapter`, `_AGENT_ASSIGNMENT_UPDATE_ADAPTER = TypeAdapter`, `_AGENT_WORK_BEGIN_ADAPTER = TypeAdapter` |
| [mcp_server](modules/mcp_server.md) | `_http_agent_key = ContextVar`, `READ_ONLY_TOOL = ToolAnnotations`, `WRITE_TOOL = ToolAnnotations`, `REMOVAL_TOOL = ToolAnnotations`, `mcp = create_mcp_server` |
| [migrations_env](modules/migrations_env.md) | `settings = get_settings`, `database_configuration = parse_database_configuration`, `config.set_main_option`, `fileConfig`, `run_migrations_offline`, `run_migrations_online` |
| [models_agent](modules/models_agent.md) | `TeamMemberProfile.agent_connected = column_property` |
| [models_calendar](modules/models_calendar.md) | `iteration_annual_calendars = Table`, `profile_annual_calendars = Table` |
| [delivery_observation](modules/delivery_observation.md) | `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen`, `event.listen` |
| [models_execution_usage](modules/models_execution_usage.md) | `event.listen`, `event.listen` |
| [recovery](modules/recovery.md) | `event.listen` |
| [models_release](modules/models_release.md) | `release_tasks = Table` |
| [models_runtime_observation](modules/models_runtime_observation.md) | `event.listen` |
| [team_member](modules/team_member.md) | `TeamMember.assignee_kind = column_property` |
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
| [maintenance_windows](modules/maintenance_windows.md) | `router = APIRouter` |
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
| [agent_team_setup](modules/agent_team_setup.md) | `_BINDING_KEY_RE = re.compile`, `AGENT_TEAM_ROLE_RULE_FIELDS = frozenset`, `SECRET_QUERY_KEYS = frozenset` |
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
| [maintenance_window_service](modules/maintenance_window_service.md) | `MAX_WINDOW = timedelta` |
| [notification_service](modules/notification_service.md) | `logger = logging.getLogger` |
| [outbound_webhook_service](modules/outbound_webhook_service.md) | `logger = logging.getLogger` |
| [planning_window_reconciliation](modules/planning_window_reconciliation.md) | `_EVIDENCE_DIGEST = re.compile`, `_SNAPSHOT_CACHE = OrderedDict`, `_CACHE_LOCK = Lock` |
| [scheduler_service](modules/scheduler_service.md) | `logger = logging.getLogger` |
| [scheduling_rules_service](modules/scheduling_rules_service.md) | `logger = logging.getLogger`, `CONDITION_PATTERN = re.compile` |
| [session_service](modules/session_service.md) | `_SESSION_TOKEN_PATTERN = re.compile` |
| [snapshot_service](modules/snapshot_service.md) | `SNAPSHOTS_DIR = Path`, `SNAPSHOT_REASON_PATTERN = re.compile`, `SNAPSHOT_FILENAME_PATTERN = re.compile` |
| [system_settings_service](modules/system_settings_service.md) | `logger = logging.getLogger`, `LEGACY_EMAIL_SETTINGS_FILE = Path` |
| [web_intake_service](modules/web_intake_service.md) | `default_web_intake_rate_limiter = WebIntakeRateLimiter` |
| [settings_read](modules/settings_read.md) | `READABLE_SETTINGS_PATHS = frozenset` |
| [github_links](modules/github_links.md) | `_FULL_COMMIT_SHA = re.compile` |
| [text_similarity](modules/text_similarity.md) | `TOKEN_PATTERN = re.compile` |
| [test_autonomy_foundation](modules/test_autonomy_foundation.md) | `NOW = datetime` |
| [test_server_acceptance](modules/test_server_acceptance.md) | `NOW = datetime.now(UTC).replace`, `PRIVATE_KEY = Ed25519PrivateKey.from_private_bytes`, `PUBLIC_KEY_BYTES = PRIVATE_KEY.public_key().public_bytes`, `PUBLIC_KEY_BASE64 = base64.b64encode(PUBLIC_KEY_BYTES).decode` |
| [test_work_package_service](modules/test_work_package_service.md) | `DIGESTS = tuple` |
| [conftest](modules/conftest.md) | `os.environ.setdefault` |
| [postgresql_migrations_env](modules/postgresql_migrations_env.md) | `run_migrations_offline`, `run_migrations_online` |
| [test_populated_history_migration](modules/test_populated_history_migration.md) | `PROJECTS_CREATED = datetime` |
| [test_android_cleanup](modules/test_android_cleanup.md) | `sys.path.insert` |
| [test_load_seed_postgresql](modules/test_load_seed_postgresql.md) | `sys.path.insert` |
| [test_load_tooling](modules/test_load_tooling.md) | `sys.path.insert` |
| [test_routing_evidence](modules/test_routing_evidence.md) | `sys.path.insert` |
| [support_database](modules/support_database.md) | `TEST_DATABASE_PATTERN = re.compile`, `TEST_RUNTIME_ROLE_PATTERN = re.compile`, `DEFAULT_POSTGRES_HOSTS = frozenset`, `ADMIN_DATABASES = frozenset` |
| [test_agent_discovery_report](modules/test_agent_discovery_report.md) | `NOW = datetime.fromisoformat` |
| [test_agent_key_delivery](modules/test_agent_key_delivery.md) | `_PROVISION_SPEC = importlib.util.spec_from_file_location`, `provision_actor = importlib.util.module_from_spec`, `_PROVISION_SPEC.loader.exec_module`, `posix_only = pytest.mark.skipif` |
| [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md) | `_PROVISION_SPEC = importlib.util.spec_from_file_location`, `provision_actor = importlib.util.module_from_spec`, `_PROVISION_SPEC.loader.exec_module` |
| [test_agent_routing_service](modules/test_agent_routing_service.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md) | `pytestmark = pytest.mark.usefixtures`, `_FIXED_NOW = datetime` |
| [test_agent_team_setup](modules/test_agent_team_setup.md) | `pytestmark = pytest.mark.usefixtures`, `both_databases = pytest.mark.parametrize` |
| [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md) | `SPEC = importlib.util.spec_from_file_location`, `setup_agent_team = importlib.util.module_from_spec`, `SPEC.loader.exec_module` |
| [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md) | `FIXED_NOW = datetime` |
| [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_dependency_date_cascade](modules/test_dependency_date_cascade.md) | `PLANNED_START = date`, `LATER_START = date` |
| [test_execution_reconciliation](modules/test_execution_reconciliation.md) | `database_engines = pytest.mark.parametrize` |
| [test_mcp_proxy_host_header](modules/test_mcp_proxy_host_header.md) | `needs_docker = pytest.mark.skipif` |
| [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md) | `READ_NAME = re.compile` |
| [test_native_connections](modules/test_native_connections.md) | `CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b'=').decode` |
| [test_observer_sessions](modules/test_observer_sessions.md) | `CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b'=').decode`, `OBSERVER_CAP = timedelta`, `PERSON_CAP = timedelta` |
| [test_plan_checkpoints](modules/test_plan_checkpoints.md) | `READY = dict` |
| [test_profile_seed_key_binding](modules/test_profile_seed_key_binding.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_review_provenance](modules/test_review_provenance.md) | `database_engines = pytest.mark.parametrize` |
| [test_review_provenance_transports](modules/test_review_provenance_transports.md) | `databases = pytest.mark.parametrize` |
| [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md) | `TODAY = date`, `NOW = datetime.fromisoformat` |
| [test_team_topology_read](modules/test_team_topology_read.md) | `pytestmark = pytest.mark.usefixtures` |
| [single-page-toolbar](modules/single-page-toolbar.md) | `CALL = Symbol`, `DYNAMIC = Symbol`, `ALL = Symbol`, `WRAPPERS = Set`, `ELEMENT_FACTORIES = Set`, `MUTATING_METHODS = Set`, `PER_ITEM_METHODS = Set`, `exportCache = Map` |
| [check-bundle-budget](modules/check-bundle-budget.md) | `BUDGETS = freeze` |
| [check-query-feedback](modules/check-query-feedback.md) | `HOOK_KINDS = Map` |
| [check-tailwind-classes](modules/check-tailwind-classes.md) | `semanticRoots = Set`, `colorUtilityPrefixes = sort`, `colorUtilitySource = join`, `semanticRootSource = join`, `semanticClassPattern = RegExp`, `legacyClassPattern = RegExp`, `rawPaletteClassPattern = RegExp`, `darkVariantClassPattern = RegExp`, `arbitraryColorClassPattern = RegExp`, `translucentSemanticTextPattern = RegExp`, `globalsCss = readFileSync`, `semanticColorNames = Set` |
| [check-task-selection-layout](modules/check-task-selection-layout.md) | `appUrl = arg`, `pagePath = arg`, `devtoolsUrl = arg`, `shotsDir = arg`, `maxFirstRow = Number`, `log` |
| [find-unread-i18n-keys](modules/find-unread-i18n-keys.md) | `srcRoot = resolve`, `resourceFiles = Set`, `sourceFiles = filesUnder`, `parsed = Map`, `importMaps = Map`, `english = get`, `englishObject = resolveObject`, `translationProperty = find`, `fullKeys = Set`, `keyLocations = Map`, `subtreeKeys = Map`, `flattenResolved`, `usedLiterals = Set`, `dynamicPrefixes = Set`, `dynamicLookups = Map`, `usedSubtrees = Set`, `relevantDynamicPrefixes = sort`, `unmatched = filter`, `sort`, `retiredUnread = filter`, `log`, `log`, `log`, `log`, `log`, `log`, `log`, `log`, `log`, `log` |
| [find-unused-exports](modules/find-unused-exports.md) | `srcRoot = resolve`, `scopes = flatMap`, `sourceFiles = filesUnder`, `parsed = Map`, `exports = Map`, `imported = Map`, `selected = sort`, `log`, `log`, `log` |
| [App.legacyRoutes.test](modules/App.legacyRoutes.test.md) | `mock`, `mock`, `describe` |
| [App](modules/App.md) | `OverviewPage = lazy`, `LandingPage = lazy`, `PlanPage = lazy`, `PlanSharePage = lazy`, `TeamPage = lazy`, `TasksPage = lazy`, `MyWorkPage = lazy`, `NativeConnectionPage = lazy`, `TriagePage = lazy`, `ProjectsPage = lazy`, `ProjectDetailPage = lazy`, `ProjectReleaseDetailPage = lazy`, `GanttPage = lazy`, `AnalyticsPage = lazy`, `SettingsPage = lazy`, `NotFoundPage = lazy` |
| [UserSessionBadge.test](modules/UserSessionBadge.test.md) | `sessionServiceMock = hoisted`, `mock`, `describe` |
| [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md) | `agentServiceMock = hoisted`, `mock`, `describe` |
| [AssignedAgentsSummary](modules/AssignedAgentsSummary.md) | `KNOWN_PURPOSES = Set`, `KNOWN_STATES = Set` |
| [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md) | `describe` |
| [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md) | `agentServiceMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `dispatchableRoster = map`, `describe`, `describe` |
| [TaskRoutingPanel](modules/TaskRoutingPanel.md) | `SKILL_CATALOG_READ_SCOPES = Set`, `TEAM_ASSIGNMENT_READ_SCOPES = Set` |
| [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md) | `metrics = hoisted`, `iterationsMock = hoisted`, `projects = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md) | `delivery = hoisted`, `mock`, `mock`, `service = hoisted`, `mock`, `describe` |
| [IterationOutlook.test](modules/IterationOutlook.test.md) | `mock`, `describe` |
| [InteractiveCalendar.test](modules/InteractiveCalendar.test.md) | `describe`, `describe` |
| [CapacitySection.test](modules/CapacitySection.test.md) | `mock`, `mock`, `mock`, `it`, `capacityApi = hoisted`, `mock`, `mock`, `mock`, `it`, `it`, `it` |
| [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md) | `team = hoisted`, `planning = hoisted`, `mock`, `mock`, `beforeEach`, `describe` |
| [TeamForm.test](modules/TeamForm.test.md) | `planningMock = hoisted`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe` |
| [TeamList.test](modules/TeamList.test.md) | `team = hoisted`, `mock`, `iterations = hoisted`, `mock`, `describe` |
| [Button.test](modules/Button.test.md) | `describe` |
| [Button](modules/Button.md) | `Button = forwardRef` |
| [ButtonLink.test](modules/ButtonLink.test.md) | `describe`, `describe` |
| [ButtonLink](modules/ButtonLink.md) | `ButtonLink = forwardRef` |
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
| [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md) | `afterEach`, `it`, `it` |
| [toast](modules/toast.md) | `ToastContext = createContext` |
| [GanttChart.test](modules/GanttChart.test.md) | `ganttServiceMock = hoisted`, `mock`, `mock`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe`, `describe` |
| [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md) | `t = bind` |
| [TaskEditDrawer.test](modules/TaskEditDrawer.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `it`, `it` |
| [UnscheduledTasks.test](modules/UnscheduledTasks.test.md) | `it`, `it` |
| [AllIterationsDrawer.test](modules/AllIterationsDrawer.test.md) | `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `planningMock = hoisted`, `exportMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [IterationForm.test](modules/IterationForm.test.md) | `planningMock = hoisted`, `mock`, `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `calendarServiceMock = hoisted`, `iterationStoreMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AppShell.test](modules/AppShell.test.md) | `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AppSidebar.planProgress.test](modules/AppSidebar.planProgress.test.md) | `services = hoisted`, `mock`, `mock`, `describe` |
| [AppSidebar.test](modules/AppSidebar.test.md) | `planningSummaryMock = hoisted`, `triageServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [AppTopNav.test](modules/AppTopNav.test.md) | `planningSummaryMock = hoisted`, `triageServiceMock = hoisted`, `scopeServiceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [BareLayout.test](modules/BareLayout.test.md) | `describe` |
| [CommandMenu.test](modules/CommandMenu.test.md) | `lookup = hoisted`, `mock`, `projects = hoisted`, `mock`, `savedViews = hoisted`, `mock`, `iterations = hoisted`, `mock`, `describe` |
| [ContextHelp.test](modules/ContextHelp.test.md) | `describe` |
| [ScopeBar.test](modules/ScopeBar.test.md) | `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [planProgressPlacement.test](modules/planProgressPlacement.test.md) | `mocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [shellViewport.test](modules/shellViewport.test.md) | `planningSummaryMock = hoisted`, `scopeServiceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `css = readFileSync`, `describe` |
| [PlanReturnBar.test](modules/PlanReturnBar.test.md) | `describe` |
| [PlanShareSection.test](modules/PlanShareSection.test.md) | `service = hoisted`, `mock`, `describe` |
| [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md) | `reader = hoisted`, `mock`, `beforeEach`, `it`, `it` |
| [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md) | `describe` |
| [ProjectForm.test](modules/ProjectForm.test.md) | `projects = hoisted`, `mock`, `mock`, `mock`, `planning = hoisted`, `mock`, `describe` |
| [ProjectForm](modules/ProjectForm.md) | `projectStatusValues = map`, `projectHealthValues = map` |
| [ProjectTaskTree.test](modules/ProjectTaskTree.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [ProjectTaskTree](modules/ProjectTaskTree.md) | `t = bind` |
| [RoadmapView.test](modules/RoadmapView.test.md) | `projectServiceMock = hoisted`, `mock`, `describe` |
| [TimeEntriesReport.test](modules/TimeEntriesReport.test.md) | `capability = hoisted`, `mock`, `it` |
| [projectDetailShared](modules/projectDetailShared.md) | `t = bind` |
| [projectStatusStyles.test](modules/projectStatusStyles.test.md) | `describe` |
| [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md) | `requestSourceServiceMock = hoisted`, `mock`, `describe` |
| [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md) | `t = bind` |
| [AdminAccessGate.test](modules/AdminAccessGate.test.md) | `mock`, `describe` |
| [AdminAccessPanel.test](modules/AdminAccessPanel.test.md) | `server = fn`, `describe` |
| [AgentAccessPanel.test](modules/AgentAccessPanel.test.md) | `agentAccessHookMock = hoisted`, `agentAccessStorageMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
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
| [WorkCalendarSettings.test](modules/WorkCalendarSettings.test.md) | `mock`, `it` |
| [schedulingSearchLabels.test](modules/schedulingSearchLabels.test.md) | `describe` |
| [settingsFieldLabels.test](modules/settingsFieldLabels.test.md) | `describe` |
| [sharedUnlock](modules/sharedUnlock.md) | `SharedUnlockContext = createContext`, `SettingsReadOnlyContext = createContext` |
| [AssigneePicker.test](modules/AssigneePicker.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [CurrentTaskDrawer.test](modules/CurrentTaskDrawer.test.md) | `service = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it` |
| [DeliveryDependencies.test](modules/DeliveryDependencies.test.md) | `mocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [GitHubReconciliationPanel.test](modules/GitHubReconciliationPanel.test.md) | `service = hoisted`, `tasks = hoisted`, `mock`, `mock`, `onTaskUpdated = fn`, `beforeEach`, `describe` |
| [KanbanBoard.test](modules/KanbanBoard.test.md) | `dragState = hoisted`, `taskServiceMock = hoisted`, `teamServiceMock = hoisted`, `planningMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [KanbanColumn.test](modules/KanbanColumn.test.md) | `mock`, `mock`, `describe`, `describe` |
| [MetricCount.test](modules/MetricCount.test.md) | `service = hoisted`, `mock`, `describe` |
| [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md) | `lookup = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it` |
| [PersonCapacity.test](modules/PersonCapacity.test.md) | `api = hoisted`, `mock`, `beforeEach`, `it`, `it` |
| [PipelineTaskEvidence](modules/PipelineTaskEvidence.md) | `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set` |
| [PipelineView](modules/PipelineView.md) | `HUMAN_GATED_STAGES = Set` |
| [QuickCapture.test](modules/QuickCapture.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it` |
| [SavedViewsControl](modules/SavedViewsControl.md) | `t = bind` |
| [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md) | `describe` |
| [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md) | `t = bind` |
| [TaskBriefEditor.test](modules/TaskBriefEditor.test.md) | `describe` |
| [TaskBulkOperationsPanel.test](modules/TaskBulkOperationsPanel.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskDependencySelector](modules/TaskDependencySelector.md) | `t = bind` |
| [TaskDiscussion.test](modules/TaskDiscussion.test.md) | `service = hoisted`, `mock`, `describe` |
| [TaskEditorDrawer.flow.test](modules/TaskEditorDrawer.flow.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `describe` |
| [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `it` |
| [TaskFiltersBar.test](modules/TaskFiltersBar.test.md) | `mock`, `mock`, `mock`, `describe` |
| [TaskForm.test](modules/TaskForm.test.md) | `api = hoisted`, `mock`, `describe`, `describe` |
| [TaskFormSections.test](modules/TaskFormSections.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `teamMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `it`, `it`, `it`, `describe`, `describe`, `describe` |
| [TaskReadView.brief.test](modules/TaskReadView.brief.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `it.each(['en', 'ru'])` |
| [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskReadView.test](modules/TaskReadView.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `describe` |
| [TaskRow.test](modules/TaskRow.test.md) | `describe` |
| [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md) | `service = hoisted`, `iterations = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind`, `LOOPBACK_HOSTS = Set` |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | `service = hoisted`, `mock`, `mock`, `describe`, `it`, `describe`, `describe` |
| [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md) | `service = hoisted`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it`, `it.each([true, false])`, `it` |
| [assigneeDisplay.test](modules/assigneeDisplay.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [taskDraftStorage.test](modules/taskDraftStorage.test.md) | `it` |
| [useDraftDismissal.test](modules/useDraftDismissal.test.md) | `it`, `describe`, `it` |
| [useSavedViewManager](modules/useSavedViewManager.md) | `t = bind` |
| [AgentManifestWorkflow.test](modules/AgentManifestWorkflow.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe`, `describe` |
| [AgentModelAdministration.test](modules/AgentModelAdministration.test.md) | `agentAccessMock = hoisted`, `adminAccessMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [ConnectAgentSteps.test](modules/ConnectAgentSteps.test.md) | `mock`, `mock`, `mock`, `service = mocked`, `teams = mocked`, `beforeEach`, `afterEach`, `describe` |
| [ImportTeamModal.test](modules/ImportTeamModal.test.md) | `planningMock = hoisted`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe` |
| [TeamProfileManager.test](modules/TeamProfileManager.test.md) | `teamServiceMock = hoisted`, `planningMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe`, `describe`, `describe`, `describe` |
| [directoryModel.test](modules/directoryModel.test.md) | `NOW = parse`, `describe` |
| [TriageList.test](modules/TriageList.test.md) | `describe` |
| [triageUtils](modules/triageUtils.md) | `t = bind` |
| [FilterBar.test](modules/FilterBar.test.md) | `describe` |
| [MasterProgress.test](modules/MasterProgress.test.md) | `describe` |
| [OverflowMenu.test](modules/OverflowMenu.test.md) | `describe` |
| [PageLayout.test](modules/PageLayout.test.md) | `describe` |
| [PageToolbar.layout.test](modules/PageToolbar.layout.test.md) | `css = readFileSync`, `describe` |
| [PageToolbar.test](modules/PageToolbar.test.md) | `describe` |
| [ViewSwitch.test](modules/ViewSwitch.test.md) | `describe` |
| [tone.test](modules/tone.test.md) | `describe` |
| [agentDispatch.test](modules/agentDispatch.test.md) | `describe` |
| [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md) | `SECRET_FIELDS = Set` |
| [manifestLocations.test](modules/manifestLocations.test.md) | `describe` |
| [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md) | `describe` |
| [agentTeamSetup_masters](modules/agentTeamSetup_masters.md) | `AGENT_TEAM_STEP_DEFINITIONS = map` |
| [statusScopes.test](modules/statusScopes.test.md) | `describe` |
| [GetStartedFlow.test](modules/GetStartedFlow.test.md) | `server = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `describe` |
| [GetStartedPanel.test](modules/GetStartedPanel.test.md) | `server = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `describe`, `describe`, `describe` |
| [NextStepEmptyState.test](modules/NextStepEmptyState.test.md) | `progress = hoisted`, `mock`, `afterEach`, `describe` |
| [getStartedVisibility](modules/getStartedVisibility.md) | `useGetStartedVisibility = create` |
| [sampleProject.test](modules/sampleProject.test.md) | `mock`, `mock`, `queryClients = Set`, `beforeEach`, `afterEach`, `describe` |
| [sampleProjectStore](modules/sampleProjectStore.md) | `useSampleProject = create` |
| [setupReturn](modules/setupReturn.md) | `useSetupReturn = create` |
| [AccountMenu.test](modules/AccountMenu.test.md) | `service = hoisted`, `mock`, `team = hoisted`, `mock`, `topBarMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [IdentityProvider.keepRoute.test](modules/IdentityProvider.keepRoute.test.md) | `describe` |
| [IdentityProvider.test](modules/IdentityProvider.test.md) | `service = hoisted`, `mock`, `describe` |
| [accountMenuRow](modules/accountMenuRow.md) | `AccountMenuRowContext = createContext` |
| [identityContext](modules/identityContext.md) | `IdentityContext = createContext` |
| [mutationFeedback.test](modules/mutationFeedback.test.md) | `describe` |
| [overviewSignals.test](modules/overviewSignals.test.md) | `describe`, `describe`, `describe`, `describe` |
| [overviewSignals](modules/overviewSignals.md) | `DONE_STATUSES = Set` |
| [planningMasters_masters.test](modules/planningMasters_masters.test.md) | `describe` |
| [planCheckpoints.test](modules/planCheckpoints.test.md) | `describe` |
| [planProgress.test](modules/planProgress.test.md) | `describe` |
| [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md) | `describe` |
| [planningNavigationInvalidation](modules/planningNavigationInvalidation.md) | `READINESS_INPUT_QUERY_ROOTS = Set` |
| [planningTaskIssues.test](modules/planningTaskIssues.test.md) | `describe`, `describe` |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [taskViewParams.test](modules/taskViewParams.test.md) | `describe` |
| [backlogScope.test](modules/backlogScope.test.md) | `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `taskServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [namedIteration.test](modules/namedIteration.test.md) | `describe` |
| [planningLinks.test](modules/planningLinks.test.md) | `iterationServiceMock = hoisted`, `planShareServiceMock = hoisted`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `describe`, `describe` |
| [planningScope.test](modules/planningScope.test.md) | `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [scopeStore](modules/scopeStore.md) | `migrateLegacyIterationStorage`, `useScopeStore = create<ScopeStore>()` |
| [scopedPages.test](modules/scopedPages.test.md) | `iterationServiceMock = hoisted`, `ganttServiceMock = hoisted`, `taskServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `projectServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [useScopeLink.test](modules/useScopeLink.test.md) | `describe` |
| [useWorkScope.test](modules/useWorkScope.test.md) | `iterationServiceMock = hoisted`, `mock`, `describe` |
| [workScope.test](modules/workScope.test.md) | `describe`, `describe`, `describe` |
| [taskTransitions.test](modules/taskTransitions.test.md) | `it` |
| [useLiveWindow.test](modules/useLiveWindow.test.md) | `it`, `it.each([0, -1, NaN, undefined])`, `it`, `it`, `it` |
| [workQueryFreshness.test](modules/workQueryFreshness.test.md) | `cases = flatMap`, `it.each(cases)` |
| [workQueryFreshness](modules/workQueryFreshness.md) | `WORKSPACE_QUERY_POLICIES = fromEntries` |
| [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md) | `it.each(['hidden', 'disabled', 'unauthorized', 'too-many-pages'])`, `it`, `it`, `it`, `it` |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | `describe` |
| [emptyStates.test](modules/emptyStates.test.md) | `describe` |
| [englishNames.test](modules/englishNames.test.md) | `describe` |
| [formatsAndWording.test](modules/formatsAndWording.test.md) | `english = flatten`, `describe` |
| [i18n.test](modules/i18n.test.md) | `describe` |
| [planWork.test](modules/planWork.test.md) | `describe` |
| [russianNames.test](modules/russianNames.test.md) | `ALLOWED_STRINGS = Set`, `describe` |
| [seedDisplay.test](modules/seedDisplay.test.md) | `describe` |
| [workflowVocabulary.test](modules/workflowVocabulary.test.md) | `describe` |
| [src_main](modules/src_main.md) | `queryClient = QueryClient`, `router = createBrowserRouter`, `render` |
| [CalendarRedirect.test](modules/CalendarRedirect.test.md) | `it` |
| [LegacyRedirect.test](modules/LegacyRedirect.test.md) | `describe` |
| [destinations.test](modules/destinations.test.md) | `describe`, `describe`, `describe`, `describe` |
| [destinations](modules/destinations.md) | `DESTINATIONS = flatMap` |
| [helpContexts.test](modules/helpContexts.test.md) | `describe` |
| [legacyPaths.check.test](modules/legacyPaths.check.test.md) | `describe` |
| [legacyPaths](modules/legacyPaths.md) | `CURRENT_PATHS = Set` |
| [scopeParams.check.test](modules/scopeParams.check.test.md) | `describe`, `describe`, `describe` |
| [workspaces.test](modules/workspaces.test.md) | `describe` |
| [AnalyticsPage.test](modules/AnalyticsPage.test.md) | `metrics = hoisted`, `usage = hoisted`, `iterationServiceMock = hoisted`, `projectServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [GanttPage.test](modules/GanttPage.test.md) | `ganttServiceMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [LandingPage.test](modules/LandingPage.test.md) | `it`, `it` |
| [MyWorkPage.test](modules/MyWorkPage.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `it`, `it`, `it`, `it`, `it.each(['active', 'review', 'inbox'])`, `describe`, `describe`, `it.each(['active', 'queued', 'blocked', 'awaiting_review', 'review'])`, `it`, `it.each(['active', 'inbox'])` |
| [NativeConnectionPage.test](modules/NativeConnectionPage.test.md) | `service = hoisted`, `mock`, `request = repeat`, `describe` |
| [OverviewPage.test](modules/OverviewPage.test.md) | `api = hoisted`, `access = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [PipelineTaskEvidence.test](modules/PipelineTaskEvidence.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `useKeylessReaderMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [PlanIterations.test](modules/PlanIterations.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [PlanPage.test](modules/PlanPage.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `planning = hoisted`, `mock`, `beforeEach`, `afterEach`, `describe`, `describe`, `describe`, `scheduleReady = summary`, `describe`, `describe` |
| [PlanSharePage.test](modules/PlanSharePage.test.md) | `planShareServiceMock = hoisted`, `mock`, `describe` |
| [ProjectDetailPage.test](modules/ProjectDetailPage.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `it`, `it`, `it`, `it`, `it` |
| [ProjectReleaseDetailPage.test](modules/ProjectReleaseDetailPage.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it`, `it.each(['project', 'release'] as const)` |
| [ProjectsPage.test](modules/ProjectsPage.test.md) | `projectServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `planningInputServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [SettingsPage.calendar.test](modules/SettingsPage.calendar.test.md) | `api = hoisted`, `mock`, `it`, `it` |
| [SettingsPage.labels.test](modules/SettingsPage.labels.test.md) | `adminAccessMock = hoisted`, `mock`, `emailMock = hoisted`, `mock`, `healthMock = hoisted`, `mock`, `calendarServiceMock = hoisted`, `planningMock = hoisted`, `mock`, `mock`, `templateServiceMock = hoisted`, `labelServiceMock = hoisted`, `rulesServiceMock = hoisted`, `webhookServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `githubServiceMock = hoisted`, `systemSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [SettingsPage.readOnlyPanels.test](modules/SettingsPage.readOnlyPanels.test.md) | `templateServiceMock = hoisted`, `labelServiceMock = hoisted`, `rulesServiceMock = hoisted`, `verifyKey = hoisted`, `mock`, `webhookServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `githubServiceMock = hoisted`, `systemSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [SettingsPage.test](modules/SettingsPage.test.md) | `themeStoreMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [SettingsPage](modules/SettingsPage.md) | `SETTINGS_SECTIONS = flatMap` |
| [SettingsPage.unlock.test](modules/SettingsPage.unlock.test.md) | `verifyKey = hoisted`, `mock`, `{ field, selfLockingField } = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TasksPage.board.test](modules/TasksPage.board.test.md) | `workScopeMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TasksPage.pipeline.test](modules/TasksPage.pipeline.test.md) | `api = hoisted`, `access = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TasksPage.test](modules/TasksPage.test.md) | `iterationServiceMock = hoisted`, `workScopeMock = hoisted`, `savedViewServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TasksPage.toolbar.test](modules/TasksPage.toolbar.test.md) | `workScopeMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `css = readFileSync`, `describe`, `passStyles = Map`, `describe` |
| [TeamPage.test](modules/TeamPage.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [TeamPage.transport.test](modules/TeamPage.transport.test.md) | `services = hoisted`, `mock`, `mock`, `describe` |
| [TriagePage.test](modules/TriagePage.test.md) | `api = hoisted`, `mock`, `beforeEach`, `describe`, `describe`, `describe` |
| [destinationEmptyStates.test](modules/destinationEmptyStates.test.md) | `beforeEach`, `afterEach`, `describe` |
| [agentService.test](modules/agentService.test.md) | `mock`, `mockedApi = mocked`, `describe` |
| [api](modules/api.md) | `api = create`, `use`, `use` |
| [planningInputService.test](modules/planningInputService.test.md) | `mock`, `beforeEach`, `it`, `it`, `it.each([
    { complete: false }, { resource_id: 8 }, { expected_revisions: { 1: 0 } },
    { expected_revisions: { 1: true } }, { expected_revisions: { '-1': 4 } }, { resource: { id: 8 } },
])` |
| [snapshotVersions.test](modules/snapshotVersions.test.md) | `mock`, `it` |
| [taskDependencyVersions.test](modules/taskDependencyVersions.test.md) | `mock`, `it` |
| [timeEntryService.test](modules/timeEntryService.test.md) | `api = hoisted`, `mock`, `beforeEach`, `it`, `it` |
| [iterationStore.test](modules/iterationStore.test.md) | `describe`, `describe`, `describe` |
| [iterationStore](modules/iterationStore.md) | `useIterationStore = assign` |
| [themeStore](modules/themeStore.md) | `useThemeStore = create<ThemeState>()` |
| [colorRoles.test](modules/colorRoles.test.md) | `css = readFileSync`, `describe` |
| [planning-masters.test](modules/planning-masters.test.md) | `planningMastersCss = readFileSync`, `agentTeamMasterSource = readFileSync`, `describe` |
| [accessibilityInvariants.test](modules/accessibilityInvariants.test.md) | `afterEach`, `describe`, `BARE_ROUTES = Set`, `describe` |
| [ganttChrome.test](modules/ganttChrome.test.md) | `services = hoisted`, `mock`, `mock`, `it` |
| [lintRules.test](modules/lintRules.test.md) | `eslint = ESLint`, `describe` |
| [pageChrome.test](modules/pageChrome.test.md) | `afterEach`, `describe` |
| [renderWithProviders.test](modules/renderWithProviders.test.md) | `describe` |
| [scopedPageRender.test](modules/scopedPageRender.test.md) | `describe` |
| [setup](modules/setup.md) | `afterEach` |
| [focusLifecycle.test](modules/focusLifecycle.test.md) | `describe` |
| [modelRouting.test](modules/modelRouting.test.md) | `describe` |
| [modelRouting](modules/modelRouting.md) | `ADVANCED_REASON_CODES = Set`, `INDEPENDENT_REASON_CODES = Set`, `STANDARD_REVIEW_REASON_CODES = Set` |
| [savedViewState.test](modules/savedViewState.test.md) | `describe` |
| [taskFilters.test](modules/taskFilters.test.md) | `describe`, `describe`, `describe`, `describe` |
| [teamMemberLabels](modules/teamMemberLabels.md) | `t = bind` |
| [visibleWork.test](modules/visibleWork.test.md) | `it`, `it`, `it` |
| [build_agent_skills](modules/build_agent_skills.md) | `SEMVER_RE = re.compile`, `SKILL_NAME_RE = re.compile`, `COMPATIBILITY_RE = re.compile`, `MARKDOWN_LINK_RE = re.compile`, `URL_RE = re.compile` |
| [build_frontend_image_identity](modules/build_frontend_image_identity.md) | `[artifactRootArg, sourceRevision, outputArg] = slice`, `artifactRoot = resolve`, `output = resolve`, `digest = createHash` |
| [android_web_peer](modules/android_web_peer.md) | `[origin, task, nonce] = slice`, `on`, `on` |
| [apt_runtime](modules/apt_runtime.md) | `UNUSED_RUNNER_HOSTS = frozenset` |
| [browser_managed_work](modules/browser_managed_work.md) | `on`, `on` |
| [browser_performance](modules/browser_performance.md) | `on` |
| [browser_write_readback](modules/browser_write_readback.md) | `on` |
| [check_markdown_links](modules/check_markdown_links.md) | `LINK_PATTERN = re.compile` |
| [check_postgresql_documentation](modules/check_postgresql_documentation.md) | `LINK_PATTERN = re.compile`, `SHELL_FENCE_PATTERN = re.compile`, `LIVE_SQLITE_COPY_PATTERN = re.compile` |
| [classify_change_scope](modules/classify_change_scope.md) | `CLASSIFIED_EVENTS = frozenset` |
| [serve_disposable_oidc](modules/serve_disposable_oidc.md) | `url = assert_safe_test_database_url`, `issuer = os.environ.get`, `key = rsa.generate_private_key`, `jwk = json.loads`, `jwk['kid'] = 'disposable-key'`, `app = FastAPI` |
| [test_apt_runtime](modules/test_apt_runtime.md) | `sys.path.insert` |
| [test_check_markdown_links](modules/test_check_markdown_links.md) | `sys.path.insert` |
| [test_ci_runtime](modules/test_ci_runtime.md) | `sys.path.insert` |
| [test_classify_change_scope](modules/test_classify_change_scope.md) | `sys.path.insert` |
| [test_native_runtimes](modules/test_native_runtimes.md) | `sys.path.insert` |
| [test_wiki_lock_root_preflight](modules/test_wiki_lock_root_preflight.md) | `sys.path.insert` |
| [wiki_lock_root_preflight](modules/wiki_lock_root_preflight.md) | `WIKI_DIRECTORY = Path` |
| [collect](modules/collect.md) | `sys.path.insert` |
| [compare](modules/compare.md) | `sys.path.insert` |
| [finalize](modules/finalize.md) | `sys.path.insert` |
| [qualify](modules/qualify.md) | `sys.path.insert`, `IMAGE_PATTERN = re.compile`, `COMMIT_PATTERN = re.compile`, `RUN_GATES = frozenset`, `REPORT_GATES = frozenset`, `SHA256_PATTERN = re.compile` |
| [resilience](modules/resilience.md) | `sys.path.insert` |
| [run](modules/run.md) | `sys.path.insert`, `RETRYABLE_STATUSES = frozenset` |
| [seal](modules/seal.md) | `sys.path.insert` |
| [seed](modules/seed.md) | `sys.path.insert` |
| [export_acceptance_artifacts](modules/export_acceptance_artifacts.md) | `sys.path.insert` |
| [seed_adoption_env](modules/seed_adoption_env.md) | `NAME = re.compile` |

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
| `create_release_github_link` | factory | [mcp_agent_tools](modules/mcp_agent_tools.md) |
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

The browser route registry exposes loader functions. React requests the corresponding page module when a destination is opened, so the static import diagram alone does not describe the browser’s initial bundle.
