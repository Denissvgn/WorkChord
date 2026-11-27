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
60. [20261126_0026_review_record_kind](modules/20261126_0026_review_record_kind.md)
61. [20261126_0027_task_postponements](modules/20261126_0027_task_postponements.md)
62. [20261126_0028_team_runtime_identity](modules/20261126_0028_team_runtime_identity.md)
63. [20261126_0029_catalog_effort](modules/20261126_0029_catalog_effort.md)
64. [query_limits](modules/query_limits.md)
65. [runtime_telemetry](modules/runtime_telemetry.md)
66. [database_runtime](modules/database_runtime.md)
67. [app_maintenance](modules/app_maintenance.md)
68. [mutation_versions](modules/mutation_versions.md)
69. [schemas_agent_connect](modules/schemas_agent_connect.md)
70. [schemas_agent_planning](modules/schemas_agent_planning.md)
71. [agent_skill_bundle](modules/agent_skill_bundle.md)
72. [agent_team_setup](modules/agent_team_setup.md)
73. [schemas_autonomy](modules/schemas_autonomy.md)
74. [schemas_common](modules/schemas_common.md)
75. [schemas_delivery_dependency](modules/schemas_delivery_dependency.md)
76. [delivery_metrics](modules/delivery_metrics.md)
77. [schemas_execution_usage](modules/schemas_execution_usage.md)
78. [schemas_github](modules/schemas_github.md)
79. [schemas_intake](modules/schemas_intake.md)
80. [schemas_label](modules/schemas_label.md)
81. [schemas_maintenance](modules/schemas_maintenance.md)
82. [manual_provenance](modules/manual_provenance.md)
83. [schemas_plan_share](modules/schemas_plan_share.md)
84. [planning_inputs](modules/planning_inputs.md)
85. [schemas_calendar](modules/schemas_calendar.md)
86. [schemas_review_evidence](modules/schemas_review_evidence.md)
87. [schemas_saved_view](modules/schemas_saved_view.md)
88. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
89. [schemas_session](modules/schemas_session.md)
90. [snapshot](modules/snapshot.md)
91. [schemas_system_settings](modules/schemas_system_settings.md)
92. [schemas_email_settings](modules/schemas_email_settings.md)
93. [schemas_task_brief](modules/schemas_task_brief.md)
94. [schemas_llm](modules/schemas_llm.md)
95. [schemas_task_domain](modules/schemas_task_domain.md)
96. [schemas_task_replacement](modules/schemas_task_replacement.md)
97. [schemas_team](modules/schemas_team.md)
98. [schemas_template](modules/schemas_template.md)
99. [schemas_time_entry](modules/schemas_time_entry.md)
100. [time_report](modules/time_report.md)
101. [schemas_work_metrics](modules/schemas_work_metrics.md)
102. [schemas_iteration](modules/schemas_iteration.md)
103. [schemas_project](modules/schemas_project.md)
104. [schemas_release](modules/schemas_release.md)
105. [security](modules/security.md)
106. [server_features](modules/server_features.md)
107. [agent_routing_policy](modules/agent_routing_policy.md)
108. [agent_routing](modules/agent_routing.md)
109. [agent_routing_rollout](modules/agent_routing_rollout.md)
110. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
111. [routers_agent_connect](modules/routers_agent_connect.md)
112. [agent_team_credentials](modules/agent_team_credentials.md)
113. [bounded_scope_reads](modules/bounded_scope_reads.md)
114. [language_service](modules/language_service.md)
115. [plan_checkpoints](modules/plan_checkpoints.md)
116. [planning_input_context](modules/planning_input_context.md)
117. [planning_issues](modules/planning_issues.md)
118. [scheduling_rules_service](modules/scheduling_rules_service.md)
119. [upgrade_service](modules/upgrade_service.md)
120. [upgrade](modules/upgrade.md)
121. [settings_read](modules/settings_read.md)
122. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
123. [sql_semantics](modules/sql_semantics.md)
124. [exceptions](modules/exceptions.md)
125. [github_links](modules/github_links.md)
126. [text_similarity](modules/text_similarity.md)
127. [time](modules/time.md)
128. [observability](modules/observability.md)
129. [app_database](modules/app_database.md)
130. [models_autonomy](modules/models_autonomy.md)
131. [models_calendar](modules/models_calendar.md)
132. [models_capacity](modules/models_capacity.md)
133. [models_database_migration](modules/models_database_migration.md)
134. [models_delivery_dependency](modules/models_delivery_dependency.md)
135. [models_discussion](modules/models_discussion.md)
136. [models_execution_usage](modules/models_execution_usage.md)
137. [models_external_link](modules/models_external_link.md)
138. [models_github](modules/models_github.md)
139. [models_identity](modules/models_identity.md)
140. [models_iteration](modules/models_iteration.md)
141. [models_label](modules/models_label.md)
142. [models_maintenance](modules/models_maintenance.md)
143. [native_connection](modules/native_connection.md)
144. [models_outbound_webhook](modules/models_outbound_webhook.md)
145. [models_plan_share](modules/models_plan_share.md)
146. [models_release](modules/models_release.md)
147. [models_project](modules/models_project.md)
148. [models_request_source](modules/models_request_source.md)
149. [models_runtime_observation](modules/models_runtime_observation.md)
150. [models_saved_view](modules/models_saved_view.md)
151. [models_system_settings](modules/models_system_settings.md)
152. [models_task](modules/models_task.md)
153. [recovery](modules/recovery.md)
154. [models_task_brief](modules/models_task_brief.md)
155. [models_task_postponement](modules/models_task_postponement.md)
156. [models_task_replacement](modules/models_task_replacement.md)
157. [task_status_log](modules/task_status_log.md)
158. [team_member](modules/team_member.md)
159. [models_agent](modules/models_agent.md)
160. [delivery_observation](modules/delivery_observation.md)
161. [models_template](modules/models_template.md)
162. [models_time_entry](modules/models_time_entry.md)
163. [models_triage](modules/models_triage.md)
164. [user_session](modules/user_session.md)
165. [models___init__](modules/models___init__.md)
166. [catalog](modules/catalog.md)
167. [database_migration_canonical](modules/database_migration_canonical.md)
168. [source](modules/source.md)
169. [transfer](modules/transfer.md)
170. [cli_database_migration](modules/cli_database_migration.md)
171. [database_migration___init__](modules/database_migration___init__.md)
172. [migrations_env](modules/migrations_env.md)
173. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
174. [calendar_rules](modules/calendar_rules.md)
175. [calendar_service](modules/calendar_service.md)
176. [calendars](modules/calendars.md)
177. [capacity_adjustments](modules/capacity_adjustments.md)
178. [capacity_service](modules/capacity_service.md)
179. [routers_capacity](modules/routers_capacity.md)
180. [delivery_dependency_service](modules/delivery_dependency_service.md)
181. [delivery_metrics_service](modules/delivery_metrics_service.md)
182. [dependency_order](modules/dependency_order.md)
183. [discussion_service](modules/discussion_service.md)
184. [execution_planning_window](modules/execution_planning_window.md)
185. [allocation_removal](modules/allocation_removal.md)
186. [identity_service](modules/identity_service.md)
187. [import_planning_service](modules/import_planning_service.md)
188. [iteration_date_move](modules/iteration_date_move.md)
189. [iteration_service](modules/iteration_service.md)
190. [iterations](modules/iterations.md)
191. [label_service](modules/label_service.md)
192. [labels](modules/labels.md)
193. [manual_provenance_service](modules/manual_provenance_service.md)
194. [native_session_service](modules/native_session_service.md)
195. [saved_view_service](modules/saved_view_service.md)
196. [session_service](modules/session_service.md)
197. [http_authority](modules/http_authority.md)
198. [routers_identity](modules/routers_identity.md)
199. [saved_views](modules/saved_views.md)
200. [routers_session](modules/routers_session.md)
201. [task_brief_service](modules/task_brief_service.md)
202. [task_context_revision_service](modules/task_context_revision_service.md)
203. [task_domain_service](modules/task_domain_service.md)
204. [task_hierarchy_service](modules/task_hierarchy_service.md)
205. [task_postponement_service](modules/task_postponement_service.md)
206. [task_recovery_service](modules/task_recovery_service.md)
207. [task_replacement_service](modules/task_replacement_service.md)
208. [task_timeline_service](modules/task_timeline_service.md)
209. [team_service](modules/team_service.md)
210. [routers_team](modules/routers_team.md)
211. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
212. [snapshot_service](modules/snapshot_service.md)
213. [plan_share_service](modules/plan_share_service.md)
214. [plan_shares](modules/plan_shares.md)
215. [template_service](modules/template_service.md)
216. [templates](modules/templates.md)
217. [time_entry_service](modules/time_entry_service.md)
218. [time_report_service](modules/time_report_service.md)
219. [services_work_metrics](modules/services_work_metrics.md)
220. [capacity_transfers](modules/capacity_transfers.md)
221. [import_parser](modules/import_parser.md)
222. [url_policy](modules/url_policy.md)
223. [schemas_external_link](modules/schemas_external_link.md)
224. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
225. [schemas_request_source](modules/schemas_request_source.md)
226. [review_provenance](modules/review_provenance.md)
227. [system_settings_service](modules/system_settings_service.md)
228. [routers_system_settings](modules/routers_system_settings.md)
229. [email_settings_service](modules/email_settings_service.md)
230. [routers_email_settings](modules/routers_email_settings.md)
231. [notification_service](modules/notification_service.md)
232. [outbound_webhook_service](modules/outbound_webhook_service.md)
233. [worker](modules/worker.md)
234. [outbound_webhooks](modules/outbound_webhooks.md)
235. [external_link_service](modules/external_link_service.md)
236. [github_status_service](modules/github_status_service.md)
237. [github_reconciliation_service](modules/github_reconciliation_service.md)
238. [request_source_service](modules/request_source_service.md)
239. [request_sources](modules/request_sources.md)
240. [project_service](modules/project_service.md)
241. [task_status_service](modules/task_status_service.md)
242. [source_link_policy](modules/source_link_policy.md)
243. [schemas_task](modules/schemas_task.md)
244. [schemas_gantt](modules/schemas_gantt.md)
245. [task_detail](modules/task_detail.md)
246. [schemas_task_postponement](modules/schemas_task_postponement.md)
247. [schemas_triage](modules/schemas_triage.md)
248. [schemas___init__](modules/schemas___init__.md)
249. [schemas_agent](modules/schemas_agent.md)
250. [agent_run_read](modules/agent_run_read.md)
251. [schemas_runtime_observation](modules/schemas_runtime_observation.md)
252. [agent_readiness](modules/agent_readiness.md)
253. [llm_service](modules/llm_service.md)
254. [runtime_observation_service](modules/runtime_observation_service.md)
255. [task_detail_service](modules/task_detail_service.md)
256. [task_import_service](modules/task_import_service.md)
257. [task_service](modules/task_service.md)
258. [export](modules/export.md)
259. [snapshots](modules/snapshots.md)
260. [agent_routing_observability](modules/agent_routing_observability.md)
261. [agent_service](modules/agent_service.md)
262. [agent_skill_bundles](modules/agent_skill_bundles.md)
263. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
264. [agent_routing_service](modules/agent_routing_service.md)
265. [agent_team_setup_service](modules/agent_team_setup_service.md)
266. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
267. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
268. [execution_reconciliation](modules/execution_reconciliation.md)
269. [execution_usage_service](modules/execution_usage_service.md)
270. [routers_task_domain](modules/routers_task_domain.md)
271. [delivery_dependencies](modules/delivery_dependencies.md)
272. [routers_discussion](modules/routers_discussion.md)
273. [time_entries](modules/time_entries.md)
274. [agent_run_read_service](modules/agent_run_read_service.md)
275. [github_status_automation_service](modules/github_status_automation_service.md)
276. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
277. [maintenance_window_service](modules/maintenance_window_service.md)
278. [maintenance_windows](modules/maintenance_windows.md)
279. [release_service](modules/release_service.md)
280. [projects](modules/projects.md)
281. [services_review_evidence](modules/services_review_evidence.md)
282. [scheduler_service](modules/scheduler_service.md)
283. [routers_gantt](modules/routers_gantt.md)
284. [routers_llm](modules/routers_llm.md)
285. [agent_planning_service](modules/agent_planning_service.md)
286. [planning_window_reconciliation](modules/planning_window_reconciliation.md)
287. [retained_planning_output](modules/retained_planning_output.md)
288. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
289. [tasks](modules/tasks.md)
290. [triage_service](modules/triage_service.md)
291. [routers_triage](modules/routers_triage.md)
292. [agent_work_service](modules/agent_work_service.md)
293. [mcp_agent_tools](modules/mcp_agent_tools.md)
294. [mcp_server](modules/mcp_server.md)
295. [routers_agent](modules/routers_agent.md)
296. [routers_agent_planning](modules/routers_agent_planning.md)
297. [agent_catalog](modules/agent_catalog.md)
298. [github_webhook_service](modules/github_webhook_service.md)
299. [routers_github](modules/routers_github.md)
300. [web_intake_service](modules/web_intake_service.md)
301. [routers_intake](modules/routers_intake.md)
302. [app_main](modules/app_main.md)
303. [routers___init__](modules/routers___init__.md)
304. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
305. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
306. [test_server_acceptance](modules/test_server_acceptance.md)
307. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
308. [test_work_package_service](modules/test_work_package_service.md)
309. [test_database_configuration](modules/test_database_configuration.md)
310. [test_deployment_topology](modules/test_deployment_topology.md)
311. [test_observability](modules/test_observability.md)
312. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
313. [test_query_boundaries](modules/test_query_boundaries.md)
314. [test_runtime_policy](modules/test_runtime_policy.md)
315. [test_schema_behavior](modules/test_schema_behavior.md)
316. [test_wal_archive_retention](modules/test_wal_archive_retention.md)
317. [test_cutover_evidence](modules/test_cutover_evidence.md)
318. [test_documentation_boundary](modules/test_documentation_boundary.md)
319. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
320. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
321. [test_source_preflight](modules/test_source_preflight.md)
322. [test_transfer_catalog](modules/test_transfer_catalog.md)
323. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
324. [0001_wave0_probe](modules/0001_wave0_probe.md)
325. [test_allocation_identity](modules/test_allocation_identity.md)
326. [test_annual_calendar_migration](modules/test_annual_calendar_migration.md)
327. [test_capacity_adjustment_migration](modules/test_capacity_adjustment_migration.md)
328. [test_catalog_effort_migration](modules/test_catalog_effort_migration.md)
329. [test_delivery_target_branch_migration](modules/test_delivery_target_branch_migration.md)
330. [test_initial_schema](modules/test_initial_schema.md)
331. [test_profile_identity](modules/test_profile_identity.md)
332. [test_review_record_kind_migration](modules/test_review_record_kind_migration.md)
333. [test_runtime_identity_migration](modules/test_runtime_identity_migration.md)
334. [test_task_postponement_migration](modules/test_task_postponement_migration.md)
335. [test_task_replacement_migration](modules/test_task_replacement_migration.md)
336. [test_android_cleanup](modules/test_android_cleanup.md)
337. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
338. [test_load_tooling](modules/test_load_tooling.md)
339. [test_local_baseline](modules/test_local_baseline.md)
340. [test_routing_evidence](modules/test_routing_evidence.md)
341. [support_database](modules/support_database.md)
342. [delivery](modules/delivery.md)
343. [factories](modules/factories.md)
344. [faults](modules/faults.md)
345. [runtime_peer](modules/runtime_peer.md)
346. [schema](modules/schema.md)
347. [support___init__](modules/support___init__.md)
348. [conftest](modules/conftest.md)
349. [test_github_closure_concurrency](modules/test_github_closure_concurrency.md)
350. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
351. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
352. [test_project_identity](modules/test_project_identity.md)
353. [test_project_identity_scope](modules/test_project_identity_scope.md)
354. [test_populated_history_migration](modules/test_populated_history_migration.md)
355. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
356. [test_upgrade_current_database_history](modules/test_upgrade_current_database_history.md)
357. [transactions](modules/transactions.md)
358. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
359. [test_agent_key_delivery](modules/test_agent_key_delivery.md)
360. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
361. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
362. [test_agent_routing_data](modules/test_agent_routing_data.md)
363. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
364. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
365. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
366. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
367. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
368. [test_agent_routing_service](modules/test_agent_routing_service.md)
369. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
370. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
371. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
372. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
373. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
374. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
375. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
376. [test_authority_migrations](modules/test_authority_migrations.md)
377. [test_capacity_contract](modules/test_capacity_contract.md)
378. [test_client_contract](modules/test_client_contract.md)
379. [test_database_harness](modules/test_database_harness.md)
380. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
381. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
382. [test_agent_discovery_report](modules/test_agent_discovery_report.md)
383. [test_agent_team_setup](modules/test_agent_team_setup.md)
384. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
385. [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md)
386. [test_agent_team_runtime_identity](modules/test_agent_team_runtime_identity.md)
387. [test_analytics_scopes](modules/test_analytics_scopes.md)
388. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
389. [test_dependency_date_cascade](modules/test_dependency_date_cascade.md)
390. [test_deployment_configuration](modules/test_deployment_configuration.md)
391. [test_deployment_record](modules/test_deployment_record.md)
392. [test_effective_deferral](modules/test_effective_deferral.md)
393. [test_execution_usage](modules/test_execution_usage.md)
394. [test_execution_working_dates](modules/test_execution_working_dates.md)
395. [test_gantt_iteration_project](modules/test_gantt_iteration_project.md)
396. [test_github_reconciliation](modules/test_github_reconciliation.md)
397. [test_delivery_merge_prerequisites](modules/test_delivery_merge_prerequisites.md)
398. [test_harness_session_metadata](modules/test_harness_session_metadata.md)
399. [test_intake_source_link](modules/test_intake_source_link.md)
400. [test_managed_authority](modules/test_managed_authority.md)
401. [test_allocation_recovery](modules/test_allocation_recovery.md)
402. [test_assignment_paging](modules/test_assignment_paging.md)
403. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
404. [test_delivery_prerequisite_tools](modules/test_delivery_prerequisite_tools.md)
405. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
406. [test_managed_worker_discovery](modules/test_managed_worker_discovery.md)
407. [test_mcp_proxy_host_header](modules/test_mcp_proxy_host_header.md)
408. [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md)
409. [test_metric_matches](modules/test_metric_matches.md)
410. [test_mobile_contract](modules/test_mobile_contract.md)
411. [test_mutation_versions](modules/test_mutation_versions.md)
412. [test_native_connections](modules/test_native_connections.md)
413. [test_observer_sessions](modules/test_observer_sessions.md)
414. [test_agdash_link_provider](modules/test_agdash_link_provider.md)
415. [test_owner_override_acceptance](modules/test_owner_override_acceptance.md)
416. [test_person_assignment_reads](modules/test_person_assignment_reads.md)
417. [test_person_run_reads](modules/test_person_run_reads.md)
418. [test_pipeline_active_outside_run](modules/test_pipeline_active_outside_run.md)
419. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
420. [test_plan_shares](modules/test_plan_shares.md)
421. [test_planning_input_context](modules/test_planning_input_context.md)
422. [test_planning_issues](modules/test_planning_issues.md)
423. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
424. [test_process_roles](modules/test_process_roles.md)
425. [test_profile_capacity](modules/test_profile_capacity.md)
426. [test_annual_calendar_coverage](modules/test_annual_calendar_coverage.md)
427. [test_planning_read_models](modules/test_planning_read_models.md)
428. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
429. [test_profile_seed_key_binding](modules/test_profile_seed_key_binding.md)
430. [test_project_review_policy](modules/test_project_review_policy.md)
431. [test_project_working_timezone](modules/test_project_working_timezone.md)
432. [test_readiness_detail](modules/test_readiness_detail.md)
433. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
434. [test_run_detail_execution_provenance](modules/test_run_detail_execution_provenance.md)
435. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
436. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
437. [test_runtime_observations](modules/test_runtime_observations.md)
438. [test_saved_dependency_order](modules/test_saved_dependency_order.md)
439. [test_saved_view_service](modules/test_saved_view_service.md)
440. [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md)
441. [test_maintenance_window](modules/test_maintenance_window.md)
442. [test_scheduler_dependencies](modules/test_scheduler_dependencies.md)
443. [test_schedule_working_date](modules/test_schedule_working_date.md)
444. [test_server_features](modules/test_server_features.md)
445. [test_settings_read_access](modules/test_settings_read_access.md)
446. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
447. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
448. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
449. [test_task_domain](modules/test_task_domain.md)
450. [test_acceptance_attribution](modules/test_acceptance_attribution.md)
451. [test_delivery_metrics](modules/test_delivery_metrics.md)
452. [test_human_work_queries](modules/test_human_work_queries.md)
453. [test_task_discussion](modules/test_task_discussion.md)
454. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
455. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
456. [test_task_pagination](modules/test_task_pagination.md)
457. [test_task_postponement](modules/test_task_postponement.md)
458. [test_team_member_agent_connected](modules/test_team_member_agent_connected.md)
459. [test_task_assignee_kind](modules/test_task_assignee_kind.md)
460. [test_team_pm_dispatch](modules/test_team_pm_dispatch.md)
461. [test_review_provenance](modules/test_review_provenance.md)
462. [test_capacity_adjustments](modules/test_capacity_adjustments.md)
463. [test_capacity_transfers](modules/test_capacity_transfers.md)
464. [test_iteration_date_move](modules/test_iteration_date_move.md)
465. [test_scoped_review_evidence](modules/test_scoped_review_evidence.md)
466. [test_routing_preview_focus](modules/test_routing_preview_focus.md)
467. [test_routing_preview_size](modules/test_routing_preview_size.md)
468. [test_routing_preview_team_scope](modules/test_routing_preview_team_scope.md)
469. [test_team_pm_recovery](modules/test_team_pm_recovery.md)
470. [test_execution_reconciliation](modules/test_execution_reconciliation.md)
471. [test_review_provenance_transports](modules/test_review_provenance_transports.md)
472. [test_execution_planning_window](modules/test_execution_planning_window.md)
473. [test_annual_calendar_work_control](modules/test_annual_calendar_work_control.md)
474. [test_manual_provenance_record](modules/test_manual_provenance_record.md)
475. [test_manual_review_provenance](modules/test_manual_review_provenance.md)
476. [test_planning_only_edit_fence](modules/test_planning_only_edit_fence.md)
477. [test_planning_window_digest_validation](modules/test_planning_window_digest_validation.md)
478. [test_pm_forecast_calendar](modules/test_pm_forecast_calendar.md)
479. [test_shadow_review_independence](modules/test_shadow_review_independence.md)
480. [test_supervised_shadow_rework](modules/test_supervised_shadow_rework.md)
481. [test_task_replacement](modules/test_task_replacement.md)
482. [test_replacement_carried_provenance](modules/test_replacement_carried_provenance.md)
483. [test_team_topology_read](modules/test_team_topology_read.md)
484. [test_time_entries](modules/test_time_entries.md)
485. [test_time_reports](modules/test_time_reports.md)
486. [test_unscheduled_tasks](modules/test_unscheduled_tasks.md)
487. [test_unused_allocation](modules/test_unused_allocation.md)
488. [test_verification_preview_history](modules/test_verification_preview_history.md)
489. [test_work_correctness](modules/test_work_correctness.md)
490. [test_work_delivery_links](modules/test_work_delivery_links.md)
491. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
492. [single-page-toolbar](modules/single-page-toolbar.md)
493. [eslint.config](modules/eslint.config.md)
494. [check-bundle-budget](modules/check-bundle-budget.md)
495. [check-query-feedback](modules/check-query-feedback.md)
496. [check-tailwind-classes](modules/check-tailwind-classes.md)
497. [check-task-selection-layout](modules/check-task-selection-layout.md)
498. [find-unread-i18n-keys](modules/find-unread-i18n-keys.md)
499. [find-unused-exports](modules/find-unused-exports.md)
500. [Checkbox](modules/Checkbox.md)
501. [CollapsibleSection](modules/CollapsibleSection.md)
502. [DisabledReason](modules/DisabledReason.md)
503. [Input](modules/Input.md)
504. [Input.test](modules/Input.test.md)
505. [Select](modules/Select.md)
506. [Textarea](modules/Textarea.md)
507. [buttonStyles](modules/buttonStyles.md)
508. [Button](modules/Button.md)
509. [Button.test](modules/Button.test.md)
510. [ButtonLink](modules/ButtonLink.md)
511. [ButtonLink.test](modules/ButtonLink.test.md)
512. [dialogLayer](modules/dialogLayer.md)
513. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
514. [Modal](modules/Modal.md)
515. [ConfirmDialog](modules/ConfirmDialog.md)
516. [formControlLabels.test](modules/formControlLabels.test.md)
517. [iconButtonTooltips.test](modules/iconButtonTooltips.test.md)
518. [leaveGuardBypass](modules/leaveGuardBypass.md)
519. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
520. [useConfirmDialog](modules/useConfirmDialog.md)
521. [LiveWindowStatus](modules/LiveWindowStatus.md)
522. [WorkFreshness](modules/WorkFreshness.md)
523. [toast](modules/toast.md)
524. [ToastProvider](modules/ToastProvider.md)
525. [ToastProvider.test](modules/ToastProvider.test.md)
526. [UnscheduledTasks](modules/UnscheduledTasks.md)
527. [AnnualCalendarFields](modules/AnnualCalendarFields.md)
528. [LabelChip](modules/LabelChip.md)
529. [BrandMark](modules/BrandMark.md)
530. [ScopePicker](modules/ScopePicker.md)
531. [commandMenuEvents](modules/commandMenuEvents.md)
532. [setupGuideEvents](modules/setupGuideEvents.md)
533. [ProjectIterationsTab](modules/ProjectIterationsTab.md)
534. [projectPortfolio](modules/projectPortfolio.md)
535. [AccessKeysSummary](modules/AccessKeysSummary.md)
536. [AgentTeamManifestPreview](modules/AgentTeamManifestPreview.md)
537. [ConstraintsPanel](modules/ConstraintsPanel.md)
538. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
539. [SettingsUnsavedBar](modules/SettingsUnsavedBar.md)
540. [WithheldValuesNote](modules/WithheldValuesNote.md)
541. [protectedQueryKeys](modules/protectedQueryKeys.md)
542. [settingsFieldLabels](modules/settingsFieldLabels.md)
543. [sharedUnlock](modules/sharedUnlock.md)
544. [ReadOnlyFieldset](modules/ReadOnlyFieldset.md)
545. [AssigneeSelect](modules/AssigneeSelect.md)
546. [claimTime](modules/claimTime.md)
547. [SortableTaskItem](modules/SortableTaskItem.md)
548. [TaskCreateSections](modules/TaskCreateSections.md)
549. [TaskViewOptions](modules/TaskViewOptions.md)
550. [taskDraftStorage](modules/taskDraftStorage.md)
551. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
552. [taskRowValues](modules/taskRowValues.md)
553. [taskSearchResults](modules/taskSearchResults.md)
554. [taskStateChip](modules/taskStateChip.md)
555. [taskViewSession](modules/taskViewSession.md)
556. [useDraftDismissal](modules/useDraftDismissal.md)
557. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
558. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
559. [useTaskSelection](modules/useTaskSelection.md)
560. [ModelBindings](modules/ModelBindings.md)
561. [directoryModel](modules/directoryModel.md)
562. [directoryModel.test](modules/directoryModel.test.md)
563. [FilterBar](modules/FilterBar.md)
564. [InlineEmptyState](modules/InlineEmptyState.md)
565. [MasterProgress](modules/MasterProgress.md)
566. [MasterProgress.test](modules/MasterProgress.test.md)
567. [OverflowMenu](modules/OverflowMenu.md)
568. [PageLayout](modules/PageLayout.md)
569. [PageToolbar.layout.test](modules/PageToolbar.layout.test.md)
570. [PageToolbar](modules/PageToolbar.md)
571. [PageToolbar.test](modules/PageToolbar.test.md)
572. [SectionCard](modules/SectionCard.md)
573. [SegmentedControl](modules/SegmentedControl.md)
574. [Select.test](modules/Select.test.md)
575. [SlideOverDrawer](modules/SlideOverDrawer.md)
576. [StickyRail](modules/StickyRail.md)
577. [ViewSwitch](modules/ViewSwitch.md)
578. [index](modules/index.md)
579. [tone](modules/tone.md)
580. [projectStatusStyles](modules/projectStatusStyles.md)
581. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
582. [Pill](modules/Pill.md)
583. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
584. [tone.test](modules/tone.test.md)
585. [agentDispatch](modules/agentDispatch.md)
586. [taskRowParts](modules/taskRowParts.md)
587. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
588. [connectAgent](modules/connectAgent.md)
589. [manifestLocations](modules/manifestLocations.md)
590. [manifestLocations.test](modules/manifestLocations.test.md)
591. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
592. [AgentTeamStepList](modules/AgentTeamStepList.md)
593. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
594. [statusScopes](modules/statusScopes.md)
595. [statusScopes.test](modules/statusScopes.test.md)
596. [firstRunSteps](modules/firstRunSteps.md)
597. [getStartedVisibility](modules/getStartedVisibility.md)
598. [sampleProject.fixture](modules/sampleProject.fixture.md)
599. [sampleProjectStore](modules/sampleProjectStore.md)
600. [setupReturn](modules/setupReturn.md)
601. [accountMenuRow](modules/accountMenuRow.md)
602. [credentialRemount](modules/credentialRemount.md)
603. [identityContext](modules/identityContext.md)
604. [useProjectEditAccess](modules/useProjectEditAccess.md)
605. [mutationFeedback](modules/mutationFeedback.md)
606. [overviewTaskThread](modules/overviewTaskThread.md)
607. [planningMasters_masters](modules/planningMasters_masters.md)
608. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
609. [planningReturn](modules/planningReturn.md)
610. [planCheckpoints](modules/planCheckpoints.md)
611. [planCheckpoints.test](modules/planCheckpoints.test.md)
612. [planningTaskIssues](modules/planningTaskIssues.md)
613. [atRiskReasons](modules/atRiskReasons.md)
614. [AtRiskTaskReasons](modules/AtRiskTaskReasons.md)
615. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
616. [scheduleEvidence](modules/scheduleEvidence.md)
617. [useIterationPanels](modules/useIterationPanels.md)
618. [scopeStore](modules/scopeStore.md)
619. [taskTransitions](modules/taskTransitions.md)
620. [TaskRow](modules/TaskRow.md)
621. [taskTransitions.test](modules/taskTransitions.test.md)
622. [useLiveWindow](modules/useLiveWindow.md)
623. [workQueryFreshness](modules/workQueryFreshness.md)
624. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
625. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
626. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
627. [emptyStates](modules/emptyStates.md)
628. [emptyStates.test](modules/emptyStates.test.md)
629. [firstRun](modules/firstRun.md)
630. [landing.en](modules/landing.en.md)
631. [landing.ru](modules/landing.ru.md)
632. [literals.ru](modules/literals.ru.md)
633. [pagination](modules/pagination.md)
634. [plan.ru](modules/plan.ru.md)
635. [planSchedule](modules/planSchedule.md)
636. [planWork](modules/planWork.md)
637. [planningInputMessages](modules/planningInputMessages.md)
638. [surfaces.ru](modules/surfaces.ru.md)
639. [teamwork.en](modules/teamwork.en.md)
640. [teamwork.ru](modules/teamwork.ru.md)
641. [timeEntries](modules/timeEntries.md)
642. [resources.en](modules/resources.en.md)
643. [agentDispatch.test](modules/agentDispatch.test.md)
644. [englishNames.test](modules/englishNames.test.md)
645. [i18n](modules/i18n.md)
646. [settingsFieldLabels.test](modules/settingsFieldLabels.test.md)
647. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
648. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
649. [triageUtils](modules/triageUtils.md)
650. [StatusPill](modules/StatusPill.md)
651. [TriageToolbar](modules/TriageToolbar.md)
652. [dateLocale](modules/dateLocale.md)
653. [InteractiveCalendar](modules/InteractiveCalendar.md)
654. [formatsAndWording.test](modules/formatsAndWording.test.md)
655. [planWork.test](modules/planWork.test.md)
656. [resources.ru](modules/resources.ru.md)
657. [i18n.test](modules/i18n.test.md)
658. [russianNames.test](modules/russianNames.test.md)
659. [schedulingDisplay](modules/schedulingDisplay.md)
660. [seedDisplay](modules/seedDisplay.md)
661. [SavedViewsControl](modules/SavedViewsControl.md)
662. [seedDisplay.test](modules/seedDisplay.test.md)
663. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
664. [destinations](modules/destinations.md)
665. [legacyPaths](modules/legacyPaths.md)
666. [LegacyRedirect](modules/LegacyRedirect.md)
667. [CalendarRedirect.test](modules/CalendarRedirect.test.md)
668. [LegacyRedirect.test](modules/LegacyRedirect.test.md)
669. [legacyPaths.check.test](modules/legacyPaths.check.test.md)
670. [routeModules](modules/routeModules.md)
671. [DocumentMetadata](modules/DocumentMetadata.md)
672. [destinations.test](modules/destinations.test.md)
673. [helpContexts](modules/helpContexts.md)
674. [helpContexts.test](modules/helpContexts.test.md)
675. [scopeParams](modules/scopeParams.md)
676. [namedIteration](modules/namedIteration.md)
677. [namedIteration.test](modules/namedIteration.test.md)
678. [workScope](modules/workScope.md)
679. [useScopeLink](modules/useScopeLink.md)
680. [Breadcrumbs](modules/Breadcrumbs.md)
681. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
682. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
683. [PlanReturnBar](modules/PlanReturnBar.md)
684. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
685. [PlanningWorkflowHelpContent](modules/PlanningWorkflowHelpContent.md)
686. [TaskWorkflowHelpContent](modules/TaskWorkflowHelpContent.md)
687. [SetupReturnBar](modules/SetupReturnBar.md)
688. [useScopeLink.test](modules/useScopeLink.test.md)
689. [workScope.test](modules/workScope.test.md)
690. [scopeParams.check.test](modules/scopeParams.check.test.md)
691. [workspaces](modules/workspaces.md)
692. [workspaces.test](modules/workspaces.test.md)
693. [LandingPage](modules/LandingPage.md)
694. [NotFoundPage](modules/NotFoundPage.md)
695. [healthService](modules/healthService.md)
696. [SystemHealthPanel](modules/SystemHealthPanel.md)
697. [iterationStore](modules/iterationStore.md)
698. [iterationStore.test](modules/iterationStore.test.md)
699. [themeStore](modules/themeStore.md)
700. [BareLayout](modules/BareLayout.md)
701. [colorRoles.test](modules/colorRoles.test.md)
702. [planning-masters.test](modules/planning-masters.test.md)
703. [accessibilityInvariants](modules/accessibilityInvariants.md)
704. [modelAwareRouting](modules/modelAwareRouting.md)
705. [taskDetail](modules/taskDetail.md)
706. [lintRules.test](modules/lintRules.test.md)
707. [pageChrome](modules/pageChrome.md)
708. [renderWithProviders](modules/renderWithProviders.md)
709. [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md)
710. [UnscheduledTasks.test](modules/UnscheduledTasks.test.md)
711. [BareLayout.test](modules/BareLayout.test.md)
712. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
713. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
714. [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md)
715. [TaskRow.test](modules/TaskRow.test.md)
716. [FilterBar.test](modules/FilterBar.test.md)
717. [OverflowMenu.test](modules/OverflowMenu.test.md)
718. [PageLayout.test](modules/PageLayout.test.md)
719. [ViewSwitch.test](modules/ViewSwitch.test.md)
720. [LandingPage.test](modules/LandingPage.test.md)
721. [renderWithProviders.test](modules/renderWithProviders.test.md)
722. [routeRegistry](modules/routeRegistry.md)
723. [setup](modules/setup.md)
724. [types_agent](modules/types_agent.md)
725. [analyticsScope](modules/analyticsScope.md)
726. [types_calendar](modules/types_calendar.md)
727. [deliveryMetrics](modules/deliveryMetrics.md)
728. [emailSettings](modules/emailSettings.md)
729. [executionUsage](modules/executionUsage.md)
730. [types_gantt](modules/types_gantt.md)
731. [types_github](modules/types_github.md)
732. [types_iteration](modules/types_iteration.md)
733. [types_label](modules/types_label.md)
734. [outboundWebhook](modules/outboundWebhook.md)
735. [types_project](modules/types_project.md)
736. [types_release](modules/types_release.md)
737. [requestSource](modules/requestSource.md)
738. [savedView](modules/savedView.md)
739. [schedulingRules](modules/schedulingRules.md)
740. [EffortModifierCard](modules/EffortModifierCard.md)
741. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
742. [SchedulingPassCard](modules/SchedulingPassCard.md)
743. [schedulingSearchLabels.test](modules/schedulingSearchLabels.test.md)
744. [systemSettings](modules/systemSettings.md)
745. [types_task](modules/types_task.md)
746. [types_team](modules/types_team.md)
747. [types_template](modules/types_template.md)
748. [types_triage](modules/types_triage.md)
749. [workMetrics](modules/workMetrics.md)
750. [agentAccess](modules/agentAccess.md)
751. [useAgentAccess](modules/useAgentAccess.md)
752. [apiError](modules/apiError.md)
753. [QueryState](modules/QueryState.md)
754. [taskEditorContract](modules/taskEditorContract.md)
755. [TaskBriefEditor](modules/TaskBriefEditor.md)
756. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
757. [TriageDraftPreview](modules/TriageDraftPreview.md)
758. [MutationSuccessFeedback](modules/MutationSuccessFeedback.md)
759. [mutationFeedback.test](modules/mutationFeedback.test.md)
760. [adminAccess](modules/adminAccess.md)
761. [OperatorIdentityNotice](modules/OperatorIdentityNotice.md)
762. [useAdminAccess](modules/useAdminAccess.md)
763. [api](modules/api.md)
764. [identityService](modules/identityService.md)
765. [NativeConnectionPage](modules/NativeConnectionPage.md)
766. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
767. [adminAccessService](modules/adminAccessService.md)
768. [AdminAccessPanel](modules/AdminAccessPanel.md)
769. [AdminAccessGate](modules/AdminAccessGate.md)
770. [AdminAccessGate.test](modules/AdminAccessGate.test.md)
771. [agentService](modules/agentService.md)
772. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
773. [useWaitingAgents](modules/useWaitingAgents.md)
774. [agentService.test](modules/agentService.test.md)
775. [deliveryMetricsService](modules/deliveryMetricsService.md)
776. [discussionService](modules/discussionService.md)
777. [emailSettingsService](modules/emailSettingsService.md)
778. [executionUsageService](modules/executionUsageService.md)
779. [ganttService](modules/ganttService.md)
780. [githubService](modules/githubService.md)
781. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
782. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
783. [labelService](modules/labelService.md)
784. [LabelSelector](modules/LabelSelector.md)
785. [outboundWebhookService](modules/outboundWebhookService.md)
786. [planShareService](modules/planShareService.md)
787. [planningInputService](modules/planningInputService.md)
788. [usePlanningObservation](modules/usePlanningObservation.md)
789. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
790. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
791. [calendarService](modules/calendarService.md)
792. [WorkCalendarSettings](modules/WorkCalendarSettings.md)
793. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
794. [WorkCalendarSettings.test](modules/WorkCalendarSettings.test.md)
795. [PersonCapacity](modules/PersonCapacity.md)
796. [PersonCapacity.test](modules/PersonCapacity.test.md)
797. [exportService](modules/exportService.md)
798. [IterationImportDialog](modules/IterationImportDialog.md)
799. [iterationService](modules/iterationService.md)
800. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
801. [planProgress.test](modules/planProgress.test.md)
802. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
803. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
804. [useWorkScope](modules/useWorkScope.md)
805. [useAnalyticsScope](modules/useAnalyticsScope.md)
806. [useWorkScope.test](modules/useWorkScope.test.md)
807. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
808. [IdentityProvider](modules/IdentityProvider.md)
809. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
810. [useLiveWindow.test](modules/useLiveWindow.test.md)
811. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
812. [planningInputService.test](modules/planningInputService.test.md)
813. [projectService](modules/projectService.md)
814. [AddMilestoneModal](modules/AddMilestoneModal.md)
815. [SetDatesPopover](modules/SetDatesPopover.md)
816. [CreateProjectModal](modules/CreateProjectModal.md)
817. [FirstRunLanding](modules/FirstRunLanding.md)
818. [useFirstRunProgress](modules/useFirstRunProgress.md)
819. [useGetStarted](modules/useGetStarted.md)
820. [useNextSetupAction](modules/useNextSetupAction.md)
821. [NextStepEmptyState](modules/NextStepEmptyState.md)
822. [NextStepEmptyState.test](modules/NextStepEmptyState.test.md)
823. [releaseService](modules/releaseService.md)
824. [ReleaseForm](modules/ReleaseForm.md)
825. [requestSourceService](modules/requestSourceService.md)
826. [savedViewService](modules/savedViewService.md)
827. [schedulingRulesService](modules/schedulingRulesService.md)
828. [sessionService](modules/sessionService.md)
829. [snapshotService](modules/snapshotService.md)
830. [snapshotVersions.test](modules/snapshotVersions.test.md)
831. [systemSettingsService](modules/systemSettingsService.md)
832. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
833. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
834. [taskService](modules/taskService.md)
835. [DeliveryDependencies](modules/DeliveryDependencies.md)
836. [DeliveryDependencies.test](modules/DeliveryDependencies.test.md)
837. [ImportTasksModal](modules/ImportTasksModal.md)
838. [MetricCount](modules/MetricCount.md)
839. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
840. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
841. [TaskContextSummary](modules/TaskContextSummary.md)
842. [TaskDependencySelector](modules/TaskDependencySelector.md)
843. [TaskMergeDialog](modules/TaskMergeDialog.md)
844. [TaskOwnerAcceptance](modules/TaskOwnerAcceptance.md)
845. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
846. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
847. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
848. [useAgentRowFacts](modules/useAgentRowFacts.md)
849. [useTaskReviewer](modules/useTaskReviewer.md)
850. [TaskReviewer](modules/TaskReviewer.md)
851. [TriageActionModal](modules/TriageActionModal.md)
852. [overviewBacklog](modules/overviewBacklog.md)
853. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
854. [teamService](modules/teamService.md)
855. [TeamForm](modules/TeamForm.md)
856. [TeamForm.test](modules/TeamForm.test.md)
857. [capacityMutations](modules/capacityMutations.md)
858. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
859. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
860. [GanttBarInputs](modules/GanttBarInputs.md)
861. [AssigneePicker](modules/AssigneePicker.md)
862. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
863. [TaskBulkOperationsPanel.test](modules/TaskBulkOperationsPanel.test.md)
864. [TaskSelectionBar](modules/TaskSelectionBar.md)
865. [useTaskRowEdits](modules/useTaskRowEdits.md)
866. [useIterationRowData](modules/useIterationRowData.md)
867. [useTaskAssigneeDisplay](modules/useTaskAssigneeDisplay.md)
868. [TaskAssigneeDisplay](modules/TaskAssigneeDisplay.md)
869. [KanbanCard](modules/KanbanCard.md)
870. [KanbanColumn](modules/KanbanColumn.md)
871. [KanbanColumn.test](modules/KanbanColumn.test.md)
872. [ImportTeamModal](modules/ImportTeamModal.md)
873. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
874. [VacationCsvImport](modules/VacationCsvImport.md)
875. [sampleProject](modules/sampleProject.md)
876. [SampleProjectAction](modules/SampleProjectAction.md)
877. [LocalProfilePicker](modules/LocalProfilePicker.md)
878. [GetStartedPanel](modules/GetStartedPanel.md)
879. [AccountMenu](modules/AccountMenu.md)
880. [UserSessionBadge](modules/UserSessionBadge.md)
881. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
882. [IdentityProvider.test](modules/IdentityProvider.test.md)
883. [usePlanScheduleWorkloads](modules/usePlanScheduleWorkloads.md)
884. [templateService](modules/templateService.md)
885. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
886. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
887. [timeEntryService](modules/timeEntryService.md)
888. [useTimeEntries](modules/useTimeEntries.md)
889. [timeEntryService.test](modules/timeEntryService.test.md)
890. [triageService](modules/triageService.md)
891. [AppSidebar](modules/AppSidebar.md)
892. [AppSidebar.planProgress.test](modules/AppSidebar.planProgress.test.md)
893. [AppSidebar.test](modules/AppSidebar.test.md)
894. [QuickCapture](modules/QuickCapture.md)
895. [QuickCapture.test](modules/QuickCapture.test.md)
896. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
897. [usePlanningReadiness](modules/usePlanningReadiness.md)
898. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
899. [planningScope.test](modules/planningScope.test.md)
900. [workspaceApi](modules/workspaceApi.md)
901. [pageChrome.test](modules/pageChrome.test.md)
902. [copyText](modules/copyText.md)
903. [focusLifecycle](modules/focusLifecycle.md)
904. [focusLifecycle.test](modules/focusLifecycle.test.md)
905. [formatDate](modules/formatDate.md)
906. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
907. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
908. [VacationManager](modules/VacationManager.md)
909. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
910. [IterationForm](modules/IterationForm.md)
911. [IterationEditorDrawer](modules/IterationEditorDrawer.md)
912. [IterationForm.test](modules/IterationForm.test.md)
913. [ScopeBar](modules/ScopeBar.md)
914. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
915. [ScopeBar.test](modules/ScopeBar.test.md)
916. [NotificationsPanel](modules/NotificationsPanel.md)
917. [PlanIterationCheckpoint](modules/PlanIterationCheckpoint.md)
918. [PlanShareSection](modules/PlanShareSection.md)
919. [PlanReviewSection](modules/PlanReviewSection.md)
920. [PlanShareSection.test](modules/PlanShareSection.test.md)
921. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
922. [ConnectedReadersPanel](modules/ConnectedReadersPanel.md)
923. [ConnectedReadersPanel.test](modules/ConnectedReadersPanel.test.md)
924. [GitHubReconciliationPanel](modules/GitHubReconciliationPanel.md)
925. [GitHubReconciliationPanel.test](modules/GitHubReconciliationPanel.test.md)
926. [StatusChangeControl](modules/StatusChangeControl.md)
927. [TaskDiscussion](modules/TaskDiscussion.md)
928. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
929. [TaskReviewHistory](modules/TaskReviewHistory.md)
930. [TaskWorkPanel](modules/TaskWorkPanel.md)
931. [TaskOwnerAcceptance.test](modules/TaskOwnerAcceptance.test.md)
932. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
933. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
934. [TimeEntriesReport](modules/TimeEntriesReport.md)
935. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
936. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
937. [ModelCatalog](modules/ModelCatalog.md)
938. [RuntimeIdentity](modules/RuntimeIdentity.md)
939. [AgentManifestWorkflow](modules/AgentManifestWorkflow.md)
940. [AgentManifestWorkflow.test](modules/AgentManifestWorkflow.test.md)
941. [ConnectionSteps](modules/ConnectionSteps.md)
942. [ConnectionSteps.test](modules/ConnectionSteps.test.md)
943. [TeamProfileManager](modules/TeamProfileManager.md)
944. [TeamDirectory](modules/TeamDirectory.md)
945. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
946. [TriageRow](modules/TriageRow.md)
947. [TriageList](modules/TriageList.md)
948. [TriageList.test](modules/TriageList.test.md)
949. [TriageSuggestions](modules/TriageSuggestions.md)
950. [planEvidence](modules/planEvidence.md)
951. [PlanSharePage](modules/PlanSharePage.md)
952. [PlanSharePage.test](modules/PlanSharePage.test.md)
953. [scopedPageRender.test](modules/scopedPageRender.test.md)
954. [graphLimitError](modules/graphLimitError.md)
955. [modelRouting](modules/modelRouting.md)
956. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
957. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
958. [ConnectAgentSteps](modules/ConnectAgentSteps.md)
959. [ConnectAgentSteps.test](modules/ConnectAgentSteps.test.md)
960. [modelRouting.test](modules/modelRouting.test.md)
961. [protectedQueries](modules/protectedQueries.md)
962. [AssignedAgentsSummary](modules/AssignedAgentsSummary.md)
963. [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md)
964. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
965. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
966. [AgentAccessPanel](modules/AgentAccessPanel.md)
967. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
968. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
969. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
970. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
971. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
972. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
973. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
974. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
975. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
976. [PipelineTaskEvidence](modules/PipelineTaskEvidence.md)
977. [usePipeline](modules/usePipeline.md)
978. [AgentModelAdministration](modules/AgentModelAdministration.md)
979. [PipelineTaskEvidence.test](modules/PipelineTaskEvidence.test.md)
980. [TeamPage](modules/TeamPage.md)
981. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
982. [IdentityProvider.keepRoute.test](modules/IdentityProvider.keepRoute.test.md)
983. [TeamPage.test](modules/TeamPage.test.md)
984. [TeamPage.transport.test](modules/TeamPage.transport.test.md)
985. [safeUrl](modules/safeUrl.md)
986. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
987. [ProjectRequestsTab](modules/ProjectRequestsTab.md)
988. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
989. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
990. [TaskReadView](modules/TaskReadView.md)
991. [TaskReadView.brief.test](modules/TaskReadView.brief.test.md)
992. [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md)
993. [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md)
994. [TaskReadView.test](modules/TaskReadView.test.md)
995. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
996. [TriageDetailPanel](modules/TriageDetailPanel.md)
997. [TriageConvertSource](modules/TriageConvertSource.md)
998. [ConvertTriageDrawer](modules/ConvertTriageDrawer.md)
999. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
1000. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
1001. [CommandMenu](modules/CommandMenu.md)
1002. [CommandMenu.test](modules/CommandMenu.test.md)
1003. [ContextHelp](modules/ContextHelp.md)
1004. [AppTopNav](modules/AppTopNav.md)
1005. [AppShell](modules/AppShell.md)
1006. [App](modules/App.md)
1007. [App.legacyRoutes.test](modules/App.legacyRoutes.test.md)
1008. [AppShell.test](modules/AppShell.test.md)
1009. [AppTopNav.test](modules/AppTopNav.test.md)
1010. [ContextHelp.test](modules/ContextHelp.test.md)
1011. [shellViewport.test](modules/shellViewport.test.md)
1012. [AccountMenu.test](modules/AccountMenu.test.md)
1013. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
1014. [src_main](modules/src_main.md)
1015. [SettingsPage](modules/SettingsPage.md)
1016. [SettingsPage.calendar.test](modules/SettingsPage.calendar.test.md)
1017. [SettingsPage.labels.test](modules/SettingsPage.labels.test.md)
1018. [SettingsPage.readOnlyPanels.test](modules/SettingsPage.readOnlyPanels.test.md)
1019. [SettingsPage.test](modules/SettingsPage.test.md)
1020. [SettingsPage.unlock.test](modules/SettingsPage.unlock.test.md)
1021. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
1022. [taskFilterDefaults](modules/taskFilterDefaults.md)
1023. [TaskFiltersBar](modules/TaskFiltersBar.md)
1024. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
1025. [taskViewParams](modules/taskViewParams.md)
1026. [taskViewParams.test](modules/taskViewParams.test.md)
1027. [taskViewState](modules/taskViewState.md)
1028. [savedViewState](modules/savedViewState.md)
1029. [useSavedViewManager](modules/useSavedViewManager.md)
1030. [savedViewState.test](modules/savedViewState.test.md)
1031. [taskFilters](modules/taskFilters.md)
1032. [taskFilters.test](modules/taskFilters.test.md)
1033. [teamMemberLabels](modules/teamMemberLabels.md)
1034. [InitiativeForm](modules/InitiativeForm.md)
1035. [InitiativeGroupHeader](modules/InitiativeGroupHeader.md)
1036. [RoadmapView](modules/RoadmapView.md)
1037. [RoadmapView.test](modules/RoadmapView.test.md)
1038. [sampleProject.test](modules/sampleProject.test.md)
1039. [templateDefaults](modules/templateDefaults.md)
1040. [ProjectForm](modules/ProjectForm.md)
1041. [ProjectForm.test](modules/ProjectForm.test.md)
1042. [TaskForm](modules/TaskForm.md)
1043. [AssigneePicker.test](modules/AssigneePicker.test.md)
1044. [GuardedTaskDrawer](modules/GuardedTaskDrawer.md)
1045. [BacklogPanel](modules/BacklogPanel.md)
1046. [CurrentTaskDrawer.test](modules/CurrentTaskDrawer.test.md)
1047. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
1048. [TaskEditDrawer](modules/TaskEditDrawer.md)
1049. [GanttChart](modules/GanttChart.md)
1050. [GanttChart.test](modules/GanttChart.test.md)
1051. [TaskEditDrawer.test](modules/TaskEditDrawer.test.md)
1052. [ProjectTaskTree](modules/ProjectTaskTree.md)
1053. [ProjectTasksTab](modules/ProjectTasksTab.md)
1054. [ProjectTaskTree.test](modules/ProjectTaskTree.test.md)
1055. [TaskEditorDrawer.flow.test](modules/TaskEditorDrawer.flow.test.md)
1056. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
1057. [TaskForm.test](modules/TaskForm.test.md)
1058. [TaskFormSections.test](modules/TaskFormSections.test.md)
1059. [CreateTriageDrawer](modules/CreateTriageDrawer.md)
1060. [GanttPage](modules/GanttPage.md)
1061. [GanttPage.test](modules/GanttPage.test.md)
1062. [MyWorkPage](modules/MyWorkPage.md)
1063. [MyWorkPage.test](modules/MyWorkPage.test.md)
1064. [TriagePage](modules/TriagePage.md)
1065. [TriagePage.test](modules/TriagePage.test.md)
1066. [ganttChrome.test](modules/ganttChrome.test.md)
1067. [visibleWork](modules/visibleWork.md)
1068. [KanbanBoard](modules/KanbanBoard.md)
1069. [KanbanBoard.test](modules/KanbanBoard.test.md)
1070. [TaskList](modules/TaskList.md)
1071. [TaskList.test](modules/TaskList.test.md)
1072. [overviewSignals](modules/overviewSignals.md)
1073. [PipelineView](modules/PipelineView.md)
1074. [assigneeDisplay.test](modules/assigneeDisplay.test.md)
1075. [overviewSignals.test](modules/overviewSignals.test.md)
1076. [TasksPage](modules/TasksPage.md)
1077. [backlogScope.test](modules/backlogScope.test.md)
1078. [TasksPage.board.test](modules/TasksPage.board.test.md)
1079. [TasksPage.pipeline.test](modules/TasksPage.pipeline.test.md)
1080. [TasksPage.test](modules/TasksPage.test.md)
1081. [TasksPage.toolbar.test](modules/TasksPage.toolbar.test.md)
1082. [visibleWork.test](modules/visibleWork.test.md)
1083. [workNumbers](modules/workNumbers.md)
1084. [OnTrackSummary](modules/OnTrackSummary.md)
1085. [StatusDistribution](modules/StatusDistribution.md)
1086. [IterationOutlook.test](modules/IterationOutlook.test.md)
1087. [CapacityTable](modules/CapacityTable.md)
1088. [TeamList](modules/TeamList.md)
1089. [CapacitySection](modules/CapacitySection.md)
1090. [CapacitySection.test](modules/CapacitySection.test.md)
1091. [IterationCapacityLine](modules/IterationCapacityLine.md)
1092. [TeamList.test](modules/TeamList.test.md)
1093. [IterationList](modules/IterationList.md)
1094. [AllIterationsDrawer](modules/AllIterationsDrawer.md)
1095. [AllIterationsDrawer.test](modules/AllIterationsDrawer.test.md)
1096. [PlanBlockersSection](modules/PlanBlockersSection.md)
1097. [PlanIterationDrawers](modules/PlanIterationDrawers.md)
1098. [PlanScheduleSection](modules/PlanScheduleSection.md)
1099. [PlanWorkSection](modules/PlanWorkSection.md)
1100. [projectDetailShared](modules/projectDetailShared.md)
1101. [MilestoneFormDrawer](modules/MilestoneFormDrawer.md)
1102. [MilestonesSection](modules/MilestonesSection.md)
1103. [PostUpdateDrawer](modules/PostUpdateDrawer.md)
1104. [ProjectHeaderFields](modules/ProjectHeaderFields.md)
1105. [ProjectReleasesTab](modules/ProjectReleasesTab.md)
1106. [ProjectSummaryTab](modules/ProjectSummaryTab.md)
1107. [ProjectUpdatesTab](modules/ProjectUpdatesTab.md)
1108. [WorkMetricsLine](modules/WorkMetricsLine.md)
1109. [MetricCount.test](modules/MetricCount.test.md)
1110. [planningLinks.test](modules/planningLinks.test.md)
1111. [AnalyticsPage](modules/AnalyticsPage.md)
1112. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
1113. [scopedPages.test](modules/scopedPages.test.md)
1114. [AnalyticsPage.test](modules/AnalyticsPage.test.md)
1115. [OverviewPage](modules/OverviewPage.md)
1116. [GetStartedPanel.test](modules/GetStartedPanel.test.md)
1117. [OverviewPage.test](modules/OverviewPage.test.md)
1118. [PlanPage](modules/PlanPage.md)
1119. [planProgressPlacement.test](modules/planProgressPlacement.test.md)
1120. [GetStartedFlow.test](modules/GetStartedFlow.test.md)
1121. [PlanIterations.test](modules/PlanIterations.test.md)
1122. [PlanPage.test](modules/PlanPage.test.md)
1123. [ProjectDetailPage](modules/ProjectDetailPage.md)
1124. [ProjectDetailPage.test](modules/ProjectDetailPage.test.md)
1125. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
1126. [ProjectReleaseDetailPage.test](modules/ProjectReleaseDetailPage.test.md)
1127. [ProjectsPage](modules/ProjectsPage.md)
1128. [ProjectsPage.test](modules/ProjectsPage.test.md)
1129. [destinationEmptyStates.test](modules/destinationEmptyStates.test.md)
1130. [vite.config](modules/vite.config.md)
1131. [vitest.config](modules/vitest.config.md)
1132. [create_agent_actor](modules/create_agent_actor.md)
1133. [generate_workchord_keys](modules/generate_workchord_keys.md)
1134. [setup_agent_team](modules/setup_agent_team.md)
1135. [build_agent_skills](modules/build_agent_skills.md)
1136. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
1137. [android_qualification](modules/android_qualification.md)
1138. [android_web_peer](modules/android_web_peer.md)
1139. [apt_runtime](modules/apt_runtime.md)
1140. [browser_performance](modules/browser_performance.md)
1141. [browser_planning_inputs](modules/browser_planning_inputs.md)
1142. [browser_worker](modules/browser_worker.md)
1143. [browser_managed_work](modules/browser_managed_work.md)
1144. [browser_write_readback](modules/browser_write_readback.md)
1145. [check_markdown_links](modules/check_markdown_links.md)
1146. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
1147. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
1148. [ci_runtime](modules/ci_runtime.md)
1149. [classify_change_scope](modules/classify_change_scope.md)
1150. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
1151. [postgres_runtime](modules/postgres_runtime.md)
1152. [run_android_checks](modules/run_android_checks.md)
1153. [run_disposable_checks](modules/run_disposable_checks.md)
1154. [serve_disposable_api](modules/serve_disposable_api.md)
1155. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
1156. [test_apt_runtime](modules/test_apt_runtime.md)
1157. [test_check_markdown_links](modules/test_check_markdown_links.md)
1158. [test_ci_runtime](modules/test_ci_runtime.md)
1159. [test_classify_change_scope](modules/test_classify_change_scope.md)
1160. [test_native_runtimes](modules/test_native_runtimes.md)
1161. [test_wiki_lock_root_preflight](modules/test_wiki_lock_root_preflight.md)
1162. [wiki_lock_root_preflight](modules/wiki_lock_root_preflight.md)
1163. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
1164. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
1165. [generate_client_contract](modules/generate_client_contract.md)
1166. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
1167. [load_common](modules/load_common.md)
1168. [collect](modules/collect.md)
1169. [result](modules/result.md)
1170. [compare](modules/compare.md)
1171. [finalize](modules/finalize.md)
1172. [qualify](modules/qualify.md)
1173. [resilience](modules/resilience.md)
1174. [run](modules/run.md)
1175. [seal](modules/seal.md)
1176. [seed](modules/seed.md)
1177. [source_binding](modules/source_binding.md)
1178. [local_baseline](modules/local_baseline.md)
1179. [service_worksets](modules/service_worksets.md)
1180. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
1181. [isolated_rehearsal](modules/isolated_rehearsal.md)
1182. [seed_adoption_env](modules/seed_adoption_env.md)
1183. [write_deployment_record](modules/write_deployment_record.md)

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
| [agent_routing_policy](modules/agent_routing_policy.md) | `MODEL_FAILURE_CATEGORIES = frozenset`, `SERVER_OWNED_ROUTING_SNAPSHOT_SCHEMAS = frozenset`, `CONTEXT_TIER_ORDER = MappingProxyType`, `EFFORT_ORDER = MappingProxyType`, `COST_TIER_ORDER = MappingProxyType`, `LATENCY_TIER_ORDER = MappingProxyType`, `DIFFICULTY_BAND_ORDER = MappingProxyType`, `REVIEW_MODE_ORDER = MappingProxyType`, `ROUTING_SKILL_KEYS = frozenset`, `CAPABILITY_LABEL_SKILL_KEYS = MappingProxyType`, `REASON_CODE_RULES = MappingProxyType`, `ASSESSMENT_REASON_CODES = frozenset`, `VALID_ASSIGNMENT_INTENTS = MappingProxyType` |
| [agent_routing_rollout](modules/agent_routing_rollout.md) | `_BLOCKER_CODE_PATTERN = re.compile`, `_TOPOLOGY_ID_PATTERN = re.compile`, `_topology_readiness_context = ContextVar` |
| [agent_service](modules/agent_service.md) | `ALL_AGENT_SCOPES = sorted` |
| [agent_skill_bundle_service](modules/agent_skill_bundle_service.md) | `logger = logging.getLogger` |
| [agent_work_service](modules/agent_work_service.md) | `logger = logging.getLogger` |
| [assignee_recommendation_service](modules/assignee_recommendation_service.md) | `TOKEN_PATTERN = re.compile` |
| [email_settings_service](modules/email_settings_service.md) | `logger = logging.getLogger` |
| [execution_planning_window](modules/execution_planning_window.md) | `PLANNING_ONLY_FIELDS = frozenset` |
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
| [test_catalog_effort_migration](modules/test_catalog_effort_migration.md) | `_CATALOG_ROW = text` |
| [test_populated_history_migration](modules/test_populated_history_migration.md) | `PROJECTS_CREATED = datetime` |
| [test_task_postponement_migration](modules/test_task_postponement_migration.md) | `AT = datetime` |
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
| [test_agent_team_runtime_identity](modules/test_agent_team_runtime_identity.md) | `pytestmark = pytest.mark.usefixtures` |
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
| [test_team_pm_recovery](modules/test_team_pm_recovery.md) | `DATABASES = pytest.mark.parametrize` |
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
| [TaskOwnerAcceptance.test](modules/TaskOwnerAcceptance.test.md) | `service = hoisted`, `mock`, `mock`, `describe` |
| [TaskReadView.brief.test](modules/TaskReadView.brief.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `it.each(['en', 'ru'])` |
| [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskReadView.test](modules/TaskReadView.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `describe` |
| [TaskRow.test](modules/TaskRow.test.md) | `describe` |
| [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md) | `service = hoisted`, `iterations = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind`, `LOOPBACK_HOSTS = Set` |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | `service = hoisted`, `mock`, `mock`, `describe`, `it`, `describe`, `describe`, `describe` |
| [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md) | `service = hoisted`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it`, `it.each([true, false])`, `it` |
| [assigneeDisplay.test](modules/assigneeDisplay.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [taskDraftStorage.test](modules/taskDraftStorage.test.md) | `it` |
| [useDraftDismissal.test](modules/useDraftDismissal.test.md) | `it`, `describe`, `it` |
| [useSavedViewManager](modules/useSavedViewManager.md) | `t = bind` |
| [AgentManifestWorkflow.test](modules/AgentManifestWorkflow.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe`, `describe` |
| [AgentModelAdministration.test](modules/AgentModelAdministration.test.md) | `agentAccessMock = hoisted`, `adminAccessMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [ConnectAgentSteps.test](modules/ConnectAgentSteps.test.md) | `mock`, `mock`, `mock`, `service = mocked`, `teams = mocked`, `beforeEach`, `afterEach`, `describe` |
| [ConnectionSteps.test](modules/ConnectionSteps.test.md) | `describe` |
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
