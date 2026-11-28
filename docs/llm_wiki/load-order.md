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
64. [20261127_0030_task_supersession](modules/20261127_0030_task_supersession.md)
65. [20261127_0031_routing_qualification_keys](modules/20261127_0031_routing_qualification_keys.md)
66. [20261127_0032_routing_calibration_contracts](modules/20261127_0032_routing_calibration_contracts.md)
67. [20261127_0033_project_routing_conflict_mode](modules/20261127_0033_project_routing_conflict_mode.md)
68. [query_limits](modules/query_limits.md)
69. [refusal_next_steps](modules/refusal_next_steps.md)
70. [runtime_telemetry](modules/runtime_telemetry.md)
71. [database_runtime](modules/database_runtime.md)
72. [app_maintenance](modules/app_maintenance.md)
73. [mutation_versions](modules/mutation_versions.md)
74. [schemas_agent_connect](modules/schemas_agent_connect.md)
75. [schemas_agent_planning](modules/schemas_agent_planning.md)
76. [agent_skill_bundle](modules/agent_skill_bundle.md)
77. [agent_team_setup](modules/agent_team_setup.md)
78. [schemas_autonomy](modules/schemas_autonomy.md)
79. [schemas_common](modules/schemas_common.md)
80. [schemas_delivery_dependency](modules/schemas_delivery_dependency.md)
81. [delivery_metrics](modules/delivery_metrics.md)
82. [schemas_execution_usage](modules/schemas_execution_usage.md)
83. [schemas_github](modules/schemas_github.md)
84. [import_review](modules/import_review.md)
85. [schemas_intake](modules/schemas_intake.md)
86. [schemas_label](modules/schemas_label.md)
87. [schemas_maintenance](modules/schemas_maintenance.md)
88. [manual_provenance](modules/manual_provenance.md)
89. [schemas_plan_share](modules/schemas_plan_share.md)
90. [planning_inputs](modules/planning_inputs.md)
91. [schemas_calendar](modules/schemas_calendar.md)
92. [schemas_review_evidence](modules/schemas_review_evidence.md)
93. [schemas_saved_view](modules/schemas_saved_view.md)
94. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
95. [schemas_session](modules/schemas_session.md)
96. [snapshot](modules/snapshot.md)
97. [schemas_system_settings](modules/schemas_system_settings.md)
98. [schemas_email_settings](modules/schemas_email_settings.md)
99. [schemas_task_domain](modules/schemas_task_domain.md)
100. [schemas_task_replacement](modules/schemas_task_replacement.md)
101. [task_routing](modules/task_routing.md)
102. [schemas_task_brief](modules/schemas_task_brief.md)
103. [schemas_llm](modules/schemas_llm.md)
104. [schemas_team](modules/schemas_team.md)
105. [schemas_template](modules/schemas_template.md)
106. [schemas_time_entry](modules/schemas_time_entry.md)
107. [time_report](modules/time_report.md)
108. [schemas_work_metrics](modules/schemas_work_metrics.md)
109. [schemas_iteration](modules/schemas_iteration.md)
110. [schemas_project](modules/schemas_project.md)
111. [schemas_release](modules/schemas_release.md)
112. [security](modules/security.md)
113. [server_features](modules/server_features.md)
114. [agent_routing_policy](modules/agent_routing_policy.md)
115. [agent_routing](modules/agent_routing.md)
116. [schemas_routing_calibration](modules/schemas_routing_calibration.md)
117. [schemas_routing_qualification](modules/schemas_routing_qualification.md)
118. [agent_routing_rollout](modules/agent_routing_rollout.md)
119. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
120. [routers_agent_connect](modules/routers_agent_connect.md)
121. [agent_team_credentials](modules/agent_team_credentials.md)
122. [bounded_scope_reads](modules/bounded_scope_reads.md)
123. [import_review_service](modules/import_review_service.md)
124. [language_service](modules/language_service.md)
125. [plan_checkpoints](modules/plan_checkpoints.md)
126. [planning_input_context](modules/planning_input_context.md)
127. [planning_issues](modules/planning_issues.md)
128. [scheduling_rules_service](modules/scheduling_rules_service.md)
129. [upgrade_service](modules/upgrade_service.md)
130. [upgrade](modules/upgrade.md)
131. [settings_read](modules/settings_read.md)
132. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
133. [sql_semantics](modules/sql_semantics.md)
134. [exceptions](modules/exceptions.md)
135. [github_links](modules/github_links.md)
136. [text_similarity](modules/text_similarity.md)
137. [time](modules/time.md)
138. [observability](modules/observability.md)
139. [app_database](modules/app_database.md)
140. [models_autonomy](modules/models_autonomy.md)
141. [models_calendar](modules/models_calendar.md)
142. [models_capacity](modules/models_capacity.md)
143. [models_database_migration](modules/models_database_migration.md)
144. [models_delivery_dependency](modules/models_delivery_dependency.md)
145. [models_discussion](modules/models_discussion.md)
146. [models_execution_usage](modules/models_execution_usage.md)
147. [models_external_link](modules/models_external_link.md)
148. [models_github](modules/models_github.md)
149. [models_identity](modules/models_identity.md)
150. [models_iteration](modules/models_iteration.md)
151. [models_label](modules/models_label.md)
152. [models_maintenance](modules/models_maintenance.md)
153. [native_connection](modules/native_connection.md)
154. [models_outbound_webhook](modules/models_outbound_webhook.md)
155. [models_plan_share](modules/models_plan_share.md)
156. [models_release](modules/models_release.md)
157. [models_project](modules/models_project.md)
158. [models_request_source](modules/models_request_source.md)
159. [models_routing_calibration](modules/models_routing_calibration.md)
160. [models_routing_qualification](modules/models_routing_qualification.md)
161. [models_runtime_observation](modules/models_runtime_observation.md)
162. [models_saved_view](modules/models_saved_view.md)
163. [models_system_settings](modules/models_system_settings.md)
164. [models_task](modules/models_task.md)
165. [recovery](modules/recovery.md)
166. [models_task_brief](modules/models_task_brief.md)
167. [models_task_postponement](modules/models_task_postponement.md)
168. [models_task_replacement](modules/models_task_replacement.md)
169. [task_status_log](modules/task_status_log.md)
170. [team_member](modules/team_member.md)
171. [models_agent](modules/models_agent.md)
172. [delivery_observation](modules/delivery_observation.md)
173. [models_template](modules/models_template.md)
174. [models_time_entry](modules/models_time_entry.md)
175. [models_triage](modules/models_triage.md)
176. [user_session](modules/user_session.md)
177. [models___init__](modules/models___init__.md)
178. [catalog](modules/catalog.md)
179. [database_migration_canonical](modules/database_migration_canonical.md)
180. [source](modules/source.md)
181. [transfer](modules/transfer.md)
182. [cli_database_migration](modules/cli_database_migration.md)
183. [database_migration___init__](modules/database_migration___init__.md)
184. [migrations_env](modules/migrations_env.md)
185. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
186. [calendar_rules](modules/calendar_rules.md)
187. [calendar_service](modules/calendar_service.md)
188. [calendars](modules/calendars.md)
189. [capacity_adjustments](modules/capacity_adjustments.md)
190. [capacity_service](modules/capacity_service.md)
191. [routers_capacity](modules/routers_capacity.md)
192. [delivery_dependency_service](modules/delivery_dependency_service.md)
193. [delivery_metrics_service](modules/delivery_metrics_service.md)
194. [dependency_order](modules/dependency_order.md)
195. [discussion_service](modules/discussion_service.md)
196. [execution_planning_window](modules/execution_planning_window.md)
197. [allocation_removal](modules/allocation_removal.md)
198. [identity_service](modules/identity_service.md)
199. [import_planning_service](modules/import_planning_service.md)
200. [iteration_date_move](modules/iteration_date_move.md)
201. [iteration_service](modules/iteration_service.md)
202. [iterations](modules/iterations.md)
203. [label_service](modules/label_service.md)
204. [labels](modules/labels.md)
205. [manual_provenance_service](modules/manual_provenance_service.md)
206. [native_session_service](modules/native_session_service.md)
207. [saved_view_service](modules/saved_view_service.md)
208. [session_service](modules/session_service.md)
209. [http_authority](modules/http_authority.md)
210. [routers_identity](modules/routers_identity.md)
211. [saved_views](modules/saved_views.md)
212. [routers_session](modules/routers_session.md)
213. [task_brief_service](modules/task_brief_service.md)
214. [task_context_revision_service](modules/task_context_revision_service.md)
215. [task_display_state](modules/task_display_state.md)
216. [task_domain_service](modules/task_domain_service.md)
217. [task_hierarchy_service](modules/task_hierarchy_service.md)
218. [task_postponement_service](modules/task_postponement_service.md)
219. [task_reactivation_service](modules/task_reactivation_service.md)
220. [task_recovery_service](modules/task_recovery_service.md)
221. [task_replacement_service](modules/task_replacement_service.md)
222. [task_routing_service](modules/task_routing_service.md)
223. [task_timeline_service](modules/task_timeline_service.md)
224. [team_service](modules/team_service.md)
225. [routers_team](modules/routers_team.md)
226. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
227. [snapshot_service](modules/snapshot_service.md)
228. [plan_share_service](modules/plan_share_service.md)
229. [plan_shares](modules/plan_shares.md)
230. [template_service](modules/template_service.md)
231. [templates](modules/templates.md)
232. [time_entry_service](modules/time_entry_service.md)
233. [time_report_service](modules/time_report_service.md)
234. [services_work_metrics](modules/services_work_metrics.md)
235. [capacity_transfers](modules/capacity_transfers.md)
236. [import_parser](modules/import_parser.md)
237. [url_policy](modules/url_policy.md)
238. [schemas_external_link](modules/schemas_external_link.md)
239. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
240. [schemas_request_source](modules/schemas_request_source.md)
241. [review_provenance](modules/review_provenance.md)
242. [system_settings_service](modules/system_settings_service.md)
243. [routers_system_settings](modules/routers_system_settings.md)
244. [email_settings_service](modules/email_settings_service.md)
245. [routers_email_settings](modules/routers_email_settings.md)
246. [notification_service](modules/notification_service.md)
247. [outbound_webhook_service](modules/outbound_webhook_service.md)
248. [worker](modules/worker.md)
249. [outbound_webhooks](modules/outbound_webhooks.md)
250. [external_link_service](modules/external_link_service.md)
251. [github_status_service](modules/github_status_service.md)
252. [github_reconciliation_service](modules/github_reconciliation_service.md)
253. [request_source_service](modules/request_source_service.md)
254. [request_sources](modules/request_sources.md)
255. [project_service](modules/project_service.md)
256. [task_status_service](modules/task_status_service.md)
257. [source_link_policy](modules/source_link_policy.md)
258. [schemas_task](modules/schemas_task.md)
259. [schemas_gantt](modules/schemas_gantt.md)
260. [schemas_task_postponement](modules/schemas_task_postponement.md)
261. [task_detail](modules/task_detail.md)
262. [schemas_triage](modules/schemas_triage.md)
263. [schemas___init__](modules/schemas___init__.md)
264. [schemas_agent](modules/schemas_agent.md)
265. [agent_run_read](modules/agent_run_read.md)
266. [schemas_runtime_observation](modules/schemas_runtime_observation.md)
267. [agent_readiness](modules/agent_readiness.md)
268. [llm_service](modules/llm_service.md)
269. [runtime_observation_service](modules/runtime_observation_service.md)
270. [task_detail_service](modules/task_detail_service.md)
271. [task_import_service](modules/task_import_service.md)
272. [task_service](modules/task_service.md)
273. [export](modules/export.md)
274. [snapshots](modules/snapshots.md)
275. [agent_routing_observability](modules/agent_routing_observability.md)
276. [agent_service](modules/agent_service.md)
277. [agent_skill_bundles](modules/agent_skill_bundles.md)
278. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
279. [agent_routing_service](modules/agent_routing_service.md)
280. [agent_team_setup_service](modules/agent_team_setup_service.md)
281. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
282. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
283. [execution_reconciliation](modules/execution_reconciliation.md)
284. [execution_usage_service](modules/execution_usage_service.md)
285. [routers_task_domain](modules/routers_task_domain.md)
286. [delivery_dependencies](modules/delivery_dependencies.md)
287. [routers_discussion](modules/routers_discussion.md)
288. [time_entries](modules/time_entries.md)
289. [agent_run_read_service](modules/agent_run_read_service.md)
290. [github_status_automation_service](modules/github_status_automation_service.md)
291. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
292. [maintenance_window_service](modules/maintenance_window_service.md)
293. [maintenance_windows](modules/maintenance_windows.md)
294. [release_service](modules/release_service.md)
295. [projects](modules/projects.md)
296. [services_review_evidence](modules/services_review_evidence.md)
297. [routing_qualification_key_service](modules/routing_qualification_key_service.md)
298. [routing_calibration_contract_service](modules/routing_calibration_contract_service.md)
299. [scheduler_service](modules/scheduler_service.md)
300. [routers_gantt](modules/routers_gantt.md)
301. [routers_llm](modules/routers_llm.md)
302. [agent_planning_service](modules/agent_planning_service.md)
303. [planning_window_reconciliation](modules/planning_window_reconciliation.md)
304. [retained_planning_output](modules/retained_planning_output.md)
305. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
306. [tasks](modules/tasks.md)
307. [triage_service](modules/triage_service.md)
308. [routers_triage](modules/routers_triage.md)
309. [agent_work_service](modules/agent_work_service.md)
310. [mcp_agent_tools](modules/mcp_agent_tools.md)
311. [mcp_server](modules/mcp_server.md)
312. [routers_agent](modules/routers_agent.md)
313. [routers_agent_planning](modules/routers_agent_planning.md)
314. [agent_catalog](modules/agent_catalog.md)
315. [github_webhook_service](modules/github_webhook_service.md)
316. [routers_github](modules/routers_github.md)
317. [web_intake_service](modules/web_intake_service.md)
318. [routers_intake](modules/routers_intake.md)
319. [app_main](modules/app_main.md)
320. [routers___init__](modules/routers___init__.md)
321. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
322. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
323. [test_server_acceptance](modules/test_server_acceptance.md)
324. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
325. [test_work_package_service](modules/test_work_package_service.md)
326. [test_database_configuration](modules/test_database_configuration.md)
327. [test_deployment_topology](modules/test_deployment_topology.md)
328. [test_observability](modules/test_observability.md)
329. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
330. [test_query_boundaries](modules/test_query_boundaries.md)
331. [test_runtime_policy](modules/test_runtime_policy.md)
332. [test_schema_behavior](modules/test_schema_behavior.md)
333. [test_wal_archive_retention](modules/test_wal_archive_retention.md)
334. [test_cutover_evidence](modules/test_cutover_evidence.md)
335. [test_documentation_boundary](modules/test_documentation_boundary.md)
336. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
337. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
338. [test_source_preflight](modules/test_source_preflight.md)
339. [test_transfer_catalog](modules/test_transfer_catalog.md)
340. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
341. [0001_wave0_probe](modules/0001_wave0_probe.md)
342. [test_allocation_identity](modules/test_allocation_identity.md)
343. [test_annual_calendar_migration](modules/test_annual_calendar_migration.md)
344. [test_capacity_adjustment_migration](modules/test_capacity_adjustment_migration.md)
345. [test_catalog_effort_migration](modules/test_catalog_effort_migration.md)
346. [test_delivery_target_branch_migration](modules/test_delivery_target_branch_migration.md)
347. [test_initial_schema](modules/test_initial_schema.md)
348. [test_profile_identity](modules/test_profile_identity.md)
349. [test_project_routing_conflict_mode_migration](modules/test_project_routing_conflict_mode_migration.md)
350. [test_review_record_kind_migration](modules/test_review_record_kind_migration.md)
351. [test_routing_calibration_contracts_migration](modules/test_routing_calibration_contracts_migration.md)
352. [test_routing_qualification_keys_migration](modules/test_routing_qualification_keys_migration.md)
353. [test_runtime_identity_migration](modules/test_runtime_identity_migration.md)
354. [test_task_postponement_migration](modules/test_task_postponement_migration.md)
355. [test_task_replacement_migration](modules/test_task_replacement_migration.md)
356. [test_task_supersession_migration](modules/test_task_supersession_migration.md)
357. [test_android_cleanup](modules/test_android_cleanup.md)
358. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
359. [test_load_tooling](modules/test_load_tooling.md)
360. [test_local_baseline](modules/test_local_baseline.md)
361. [test_routing_evidence](modules/test_routing_evidence.md)
362. [support_database](modules/support_database.md)
363. [delivery](modules/delivery.md)
364. [factories](modules/factories.md)
365. [faults](modules/faults.md)
366. [runtime_peer](modules/runtime_peer.md)
367. [schema](modules/schema.md)
368. [support___init__](modules/support___init__.md)
369. [conftest](modules/conftest.md)
370. [test_github_closure_concurrency](modules/test_github_closure_concurrency.md)
371. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
372. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
373. [test_project_identity](modules/test_project_identity.md)
374. [test_project_identity_scope](modules/test_project_identity_scope.md)
375. [test_populated_history_migration](modules/test_populated_history_migration.md)
376. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
377. [test_upgrade_current_database_history](modules/test_upgrade_current_database_history.md)
378. [transactions](modules/transactions.md)
379. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
380. [test_agent_key_delivery](modules/test_agent_key_delivery.md)
381. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
382. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
383. [test_agent_routing_data](modules/test_agent_routing_data.md)
384. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
385. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
386. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
387. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
388. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
389. [test_agent_routing_service](modules/test_agent_routing_service.md)
390. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
391. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
392. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
393. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
394. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
395. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
396. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
397. [test_authority_migrations](modules/test_authority_migrations.md)
398. [test_capacity_contract](modules/test_capacity_contract.md)
399. [test_client_contract](modules/test_client_contract.md)
400. [test_database_harness](modules/test_database_harness.md)
401. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
402. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
403. [test_agent_discovery_report](modules/test_agent_discovery_report.md)
404. [test_agent_team_setup](modules/test_agent_team_setup.md)
405. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
406. [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md)
407. [test_agent_team_runtime_identity](modules/test_agent_team_runtime_identity.md)
408. [test_analytics_scopes](modules/test_analytics_scopes.md)
409. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
410. [test_dependency_date_cascade](modules/test_dependency_date_cascade.md)
411. [test_deployment_configuration](modules/test_deployment_configuration.md)
412. [test_deployment_record](modules/test_deployment_record.md)
413. [test_effective_deferral](modules/test_effective_deferral.md)
414. [test_execution_usage](modules/test_execution_usage.md)
415. [test_execution_working_dates](modules/test_execution_working_dates.md)
416. [test_gantt_iteration_project](modules/test_gantt_iteration_project.md)
417. [test_github_reconciliation](modules/test_github_reconciliation.md)
418. [test_delivery_merge_prerequisites](modules/test_delivery_merge_prerequisites.md)
419. [test_harness_session_metadata](modules/test_harness_session_metadata.md)
420. [test_intake_source_link](modules/test_intake_source_link.md)
421. [test_managed_authority](modules/test_managed_authority.md)
422. [test_allocation_recovery](modules/test_allocation_recovery.md)
423. [test_assignment_paging](modules/test_assignment_paging.md)
424. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
425. [test_delivery_prerequisite_tools](modules/test_delivery_prerequisite_tools.md)
426. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
427. [test_managed_worker_discovery](modules/test_managed_worker_discovery.md)
428. [test_mcp_proxy_host_header](modules/test_mcp_proxy_host_header.md)
429. [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md)
430. [test_metric_matches](modules/test_metric_matches.md)
431. [test_mobile_contract](modules/test_mobile_contract.md)
432. [test_mutation_versions](modules/test_mutation_versions.md)
433. [test_native_connections](modules/test_native_connections.md)
434. [test_observer_sessions](modules/test_observer_sessions.md)
435. [test_agdash_link_provider](modules/test_agdash_link_provider.md)
436. [test_owner_override_acceptance](modules/test_owner_override_acceptance.md)
437. [test_person_assignment_reads](modules/test_person_assignment_reads.md)
438. [test_person_run_reads](modules/test_person_run_reads.md)
439. [test_pipeline_active_outside_run](modules/test_pipeline_active_outside_run.md)
440. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
441. [test_plan_import_dry_run](modules/test_plan_import_dry_run.md)
442. [test_plan_shares](modules/test_plan_shares.md)
443. [test_planning_input_context](modules/test_planning_input_context.md)
444. [test_planning_issues](modules/test_planning_issues.md)
445. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
446. [test_postponed_out_of_scheduling](modules/test_postponed_out_of_scheduling.md)
447. [test_postponement_agent_tools](modules/test_postponement_agent_tools.md)
448. [test_process_roles](modules/test_process_roles.md)
449. [test_profile_capacity](modules/test_profile_capacity.md)
450. [test_annual_calendar_coverage](modules/test_annual_calendar_coverage.md)
451. [test_planning_read_models](modules/test_planning_read_models.md)
452. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
453. [test_profile_seed_key_binding](modules/test_profile_seed_key_binding.md)
454. [test_project_review_policy](modules/test_project_review_policy.md)
455. [test_project_working_timezone](modules/test_project_working_timezone.md)
456. [test_readiness_detail](modules/test_readiness_detail.md)
457. [test_refusal_next_steps](modules/test_refusal_next_steps.md)
458. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
459. [test_routing_calibration_contracts](modules/test_routing_calibration_contracts.md)
460. [test_routing_qualification_keys](modules/test_routing_qualification_keys.md)
461. [test_run_detail_execution_provenance](modules/test_run_detail_execution_provenance.md)
462. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
463. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
464. [test_runtime_observations](modules/test_runtime_observations.md)
465. [test_saved_dependency_order](modules/test_saved_dependency_order.md)
466. [test_saved_view_service](modules/test_saved_view_service.md)
467. [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md)
468. [test_maintenance_window](modules/test_maintenance_window.md)
469. [test_scheduler_dependencies](modules/test_scheduler_dependencies.md)
470. [test_schedule_working_date](modules/test_schedule_working_date.md)
471. [test_scheduler_free_days](modules/test_scheduler_free_days.md)
472. [test_server_features](modules/test_server_features.md)
473. [test_settings_read_access](modules/test_settings_read_access.md)
474. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
475. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
476. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
477. [test_task_domain](modules/test_task_domain.md)
478. [test_acceptance_attribution](modules/test_acceptance_attribution.md)
479. [test_delivery_metrics](modules/test_delivery_metrics.md)
480. [test_human_work_queries](modules/test_human_work_queries.md)
481. [test_task_discussion](modules/test_task_discussion.md)
482. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
483. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
484. [test_task_pagination](modules/test_task_pagination.md)
485. [test_task_postponement](modules/test_task_postponement.md)
486. [test_task_reactivation](modules/test_task_reactivation.md)
487. [test_task_routing_consistency](modules/test_task_routing_consistency.md)
488. [test_task_supersession](modules/test_task_supersession.md)
489. [test_team_member_agent_connected](modules/test_team_member_agent_connected.md)
490. [test_task_assignee_kind](modules/test_task_assignee_kind.md)
491. [test_team_pm_dispatch](modules/test_team_pm_dispatch.md)
492. [test_review_provenance](modules/test_review_provenance.md)
493. [test_capacity_adjustments](modules/test_capacity_adjustments.md)
494. [test_capacity_transfers](modules/test_capacity_transfers.md)
495. [test_iteration_date_move](modules/test_iteration_date_move.md)
496. [test_scoped_review_evidence](modules/test_scoped_review_evidence.md)
497. [test_routing_preview_focus](modules/test_routing_preview_focus.md)
498. [test_routing_preview_size](modules/test_routing_preview_size.md)
499. [test_routing_preview_team_scope](modules/test_routing_preview_team_scope.md)
500. [test_team_pm_recovery](modules/test_team_pm_recovery.md)
501. [test_execution_reconciliation](modules/test_execution_reconciliation.md)
502. [test_review_provenance_transports](modules/test_review_provenance_transports.md)
503. [test_execution_planning_window](modules/test_execution_planning_window.md)
504. [test_annual_calendar_work_control](modules/test_annual_calendar_work_control.md)
505. [test_manual_provenance_record](modules/test_manual_provenance_record.md)
506. [test_manual_review_provenance](modules/test_manual_review_provenance.md)
507. [test_planning_only_edit_fence](modules/test_planning_only_edit_fence.md)
508. [test_planning_window_digest_validation](modules/test_planning_window_digest_validation.md)
509. [test_pm_forecast_calendar](modules/test_pm_forecast_calendar.md)
510. [test_shadow_review_independence](modules/test_shadow_review_independence.md)
511. [test_supervised_shadow_rework](modules/test_supervised_shadow_rework.md)
512. [test_task_replacement](modules/test_task_replacement.md)
513. [test_replacement_carried_provenance](modules/test_replacement_carried_provenance.md)
514. [test_team_topology_read](modules/test_team_topology_read.md)
515. [test_terminal_task_states](modules/test_terminal_task_states.md)
516. [test_time_entries](modules/test_time_entries.md)
517. [test_time_reports](modules/test_time_reports.md)
518. [test_unscheduled_tasks](modules/test_unscheduled_tasks.md)
519. [test_unused_allocation](modules/test_unused_allocation.md)
520. [test_verification_preview_history](modules/test_verification_preview_history.md)
521. [test_verifier_presence](modules/test_verifier_presence.md)
522. [test_work_correctness](modules/test_work_correctness.md)
523. [test_work_delivery_links](modules/test_work_delivery_links.md)
524. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
525. [single-page-toolbar](modules/single-page-toolbar.md)
526. [eslint.config](modules/eslint.config.md)
527. [check-bundle-budget](modules/check-bundle-budget.md)
528. [check-query-feedback](modules/check-query-feedback.md)
529. [check-tailwind-classes](modules/check-tailwind-classes.md)
530. [check-task-selection-layout](modules/check-task-selection-layout.md)
531. [find-unread-i18n-keys](modules/find-unread-i18n-keys.md)
532. [find-unused-exports](modules/find-unused-exports.md)
533. [Checkbox](modules/Checkbox.md)
534. [CollapsibleSection](modules/CollapsibleSection.md)
535. [DisabledReason](modules/DisabledReason.md)
536. [Input](modules/Input.md)
537. [Input.test](modules/Input.test.md)
538. [Select](modules/Select.md)
539. [Textarea](modules/Textarea.md)
540. [buttonStyles](modules/buttonStyles.md)
541. [Button](modules/Button.md)
542. [Button.test](modules/Button.test.md)
543. [ButtonLink](modules/ButtonLink.md)
544. [ButtonLink.test](modules/ButtonLink.test.md)
545. [dialogLayer](modules/dialogLayer.md)
546. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
547. [Modal](modules/Modal.md)
548. [ConfirmDialog](modules/ConfirmDialog.md)
549. [formControlLabels.test](modules/formControlLabels.test.md)
550. [iconButtonTooltips.test](modules/iconButtonTooltips.test.md)
551. [leaveGuardBypass](modules/leaveGuardBypass.md)
552. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
553. [useConfirmDialog](modules/useConfirmDialog.md)
554. [LiveWindowStatus](modules/LiveWindowStatus.md)
555. [WorkFreshness](modules/WorkFreshness.md)
556. [toast](modules/toast.md)
557. [ToastProvider](modules/ToastProvider.md)
558. [ToastProvider.test](modules/ToastProvider.test.md)
559. [unscheduledReason](modules/unscheduledReason.md)
560. [UnscheduledTasks](modules/UnscheduledTasks.md)
561. [AnnualCalendarFields](modules/AnnualCalendarFields.md)
562. [LabelChip](modules/LabelChip.md)
563. [BrandMark](modules/BrandMark.md)
564. [ScopePicker](modules/ScopePicker.md)
565. [commandMenuEvents](modules/commandMenuEvents.md)
566. [setupGuideEvents](modules/setupGuideEvents.md)
567. [ProjectIterationsTab](modules/ProjectIterationsTab.md)
568. [projectPortfolio](modules/projectPortfolio.md)
569. [AccessKeysSummary](modules/AccessKeysSummary.md)
570. [AgentTeamManifestPreview](modules/AgentTeamManifestPreview.md)
571. [ConstraintsPanel](modules/ConstraintsPanel.md)
572. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
573. [SettingsUnsavedBar](modules/SettingsUnsavedBar.md)
574. [WithheldValuesNote](modules/WithheldValuesNote.md)
575. [protectedQueryKeys](modules/protectedQueryKeys.md)
576. [settingsFieldLabels](modules/settingsFieldLabels.md)
577. [sharedUnlock](modules/sharedUnlock.md)
578. [ReadOnlyFieldset](modules/ReadOnlyFieldset.md)
579. [AssigneeSelect](modules/AssigneeSelect.md)
580. [claimTime](modules/claimTime.md)
581. [RefusalNextStepNote](modules/RefusalNextStepNote.md)
582. [SortableTaskItem](modules/SortableTaskItem.md)
583. [TaskCreateSections](modules/TaskCreateSections.md)
584. [TaskViewOptions](modules/TaskViewOptions.md)
585. [taskDraftStorage](modules/taskDraftStorage.md)
586. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
587. [taskRowValues](modules/taskRowValues.md)
588. [taskViewSession](modules/taskViewSession.md)
589. [useDraftDismissal](modules/useDraftDismissal.md)
590. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
591. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
592. [useTaskSelection](modules/useTaskSelection.md)
593. [ModelBindings](modules/ModelBindings.md)
594. [directoryModel](modules/directoryModel.md)
595. [directoryModel.test](modules/directoryModel.test.md)
596. [FilterBar](modules/FilterBar.md)
597. [InlineEmptyState](modules/InlineEmptyState.md)
598. [MasterProgress](modules/MasterProgress.md)
599. [MasterProgress.test](modules/MasterProgress.test.md)
600. [OverflowMenu](modules/OverflowMenu.md)
601. [PageLayout](modules/PageLayout.md)
602. [PageToolbar.layout.test](modules/PageToolbar.layout.test.md)
603. [PageToolbar](modules/PageToolbar.md)
604. [PageToolbar.test](modules/PageToolbar.test.md)
605. [SectionCard](modules/SectionCard.md)
606. [SegmentedControl](modules/SegmentedControl.md)
607. [Select.test](modules/Select.test.md)
608. [SlideOverDrawer](modules/SlideOverDrawer.md)
609. [StickyRail](modules/StickyRail.md)
610. [ViewSwitch](modules/ViewSwitch.md)
611. [index](modules/index.md)
612. [tone](modules/tone.md)
613. [projectStatusStyles](modules/projectStatusStyles.md)
614. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
615. [Pill](modules/Pill.md)
616. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
617. [tone.test](modules/tone.test.md)
618. [agentDispatch](modules/agentDispatch.md)
619. [taskRowParts](modules/taskRowParts.md)
620. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
621. [connectAgent](modules/connectAgent.md)
622. [manifestLocations](modules/manifestLocations.md)
623. [manifestLocations.test](modules/manifestLocations.test.md)
624. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
625. [AgentTeamStepList](modules/AgentTeamStepList.md)
626. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
627. [statusScopes](modules/statusScopes.md)
628. [statusScopes.test](modules/statusScopes.test.md)
629. [firstRunSteps](modules/firstRunSteps.md)
630. [getStartedVisibility](modules/getStartedVisibility.md)
631. [sampleProject.fixture](modules/sampleProject.fixture.md)
632. [sampleProjectStore](modules/sampleProjectStore.md)
633. [setupReturn](modules/setupReturn.md)
634. [accountMenuRow](modules/accountMenuRow.md)
635. [credentialRemount](modules/credentialRemount.md)
636. [identityContext](modules/identityContext.md)
637. [useProjectEditAccess](modules/useProjectEditAccess.md)
638. [mutationFeedback](modules/mutationFeedback.md)
639. [overviewTaskThread](modules/overviewTaskThread.md)
640. [planningMasters_masters](modules/planningMasters_masters.md)
641. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
642. [planningReturn](modules/planningReturn.md)
643. [planCheckpoints](modules/planCheckpoints.md)
644. [planCheckpoints.test](modules/planCheckpoints.test.md)
645. [planningTaskIssues](modules/planningTaskIssues.md)
646. [atRiskReasons](modules/atRiskReasons.md)
647. [AtRiskTaskReasons](modules/AtRiskTaskReasons.md)
648. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
649. [scheduleEvidence](modules/scheduleEvidence.md)
650. [useIterationPanels](modules/useIterationPanels.md)
651. [scopeStore](modules/scopeStore.md)
652. [taskTransitions](modules/taskTransitions.md)
653. [taskTransitions.test](modules/taskTransitions.test.md)
654. [useLiveWindow](modules/useLiveWindow.md)
655. [workQueryFreshness](modules/workQueryFreshness.md)
656. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
657. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
658. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
659. [emptyStates](modules/emptyStates.md)
660. [emptyStates.test](modules/emptyStates.test.md)
661. [firstRun](modules/firstRun.md)
662. [landing.en](modules/landing.en.md)
663. [landing.ru](modules/landing.ru.md)
664. [literals.ru](modules/literals.ru.md)
665. [pagination](modules/pagination.md)
666. [plan.ru](modules/plan.ru.md)
667. [planSchedule](modules/planSchedule.md)
668. [planWork](modules/planWork.md)
669. [planningInputMessages](modules/planningInputMessages.md)
670. [surfaces.ru](modules/surfaces.ru.md)
671. [teamwork.en](modules/teamwork.en.md)
672. [teamwork.ru](modules/teamwork.ru.md)
673. [timeEntries](modules/timeEntries.md)
674. [resources.en](modules/resources.en.md)
675. [agentDispatch.test](modules/agentDispatch.test.md)
676. [englishNames.test](modules/englishNames.test.md)
677. [i18n](modules/i18n.md)
678. [settingsFieldLabels.test](modules/settingsFieldLabels.test.md)
679. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
680. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
681. [triageUtils](modules/triageUtils.md)
682. [StatusPill](modules/StatusPill.md)
683. [TriageToolbar](modules/TriageToolbar.md)
684. [dateLocale](modules/dateLocale.md)
685. [InteractiveCalendar](modules/InteractiveCalendar.md)
686. [formatsAndWording.test](modules/formatsAndWording.test.md)
687. [planWork.test](modules/planWork.test.md)
688. [resources.ru](modules/resources.ru.md)
689. [i18n.test](modules/i18n.test.md)
690. [russianNames.test](modules/russianNames.test.md)
691. [schedulingDisplay](modules/schedulingDisplay.md)
692. [seedDisplay](modules/seedDisplay.md)
693. [SavedViewsControl](modules/SavedViewsControl.md)
694. [seedDisplay.test](modules/seedDisplay.test.md)
695. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
696. [destinations](modules/destinations.md)
697. [legacyPaths](modules/legacyPaths.md)
698. [LegacyRedirect](modules/LegacyRedirect.md)
699. [CalendarRedirect.test](modules/CalendarRedirect.test.md)
700. [LegacyRedirect.test](modules/LegacyRedirect.test.md)
701. [legacyPaths.check.test](modules/legacyPaths.check.test.md)
702. [routeModules](modules/routeModules.md)
703. [DocumentMetadata](modules/DocumentMetadata.md)
704. [destinations.test](modules/destinations.test.md)
705. [helpContexts](modules/helpContexts.md)
706. [helpContexts.test](modules/helpContexts.test.md)
707. [scopeParams](modules/scopeParams.md)
708. [namedIteration](modules/namedIteration.md)
709. [namedIteration.test](modules/namedIteration.test.md)
710. [workScope](modules/workScope.md)
711. [useScopeLink](modules/useScopeLink.md)
712. [Breadcrumbs](modules/Breadcrumbs.md)
713. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
714. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
715. [PlanReturnBar](modules/PlanReturnBar.md)
716. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
717. [PlanningWorkflowHelpContent](modules/PlanningWorkflowHelpContent.md)
718. [TaskWorkflowHelpContent](modules/TaskWorkflowHelpContent.md)
719. [SetupReturnBar](modules/SetupReturnBar.md)
720. [useScopeLink.test](modules/useScopeLink.test.md)
721. [workScope.test](modules/workScope.test.md)
722. [scopeParams.check.test](modules/scopeParams.check.test.md)
723. [workspaces](modules/workspaces.md)
724. [workspaces.test](modules/workspaces.test.md)
725. [LandingPage](modules/LandingPage.md)
726. [NotFoundPage](modules/NotFoundPage.md)
727. [healthService](modules/healthService.md)
728. [SystemHealthPanel](modules/SystemHealthPanel.md)
729. [iterationStore](modules/iterationStore.md)
730. [iterationStore.test](modules/iterationStore.test.md)
731. [themeStore](modules/themeStore.md)
732. [BareLayout](modules/BareLayout.md)
733. [colorRoles.test](modules/colorRoles.test.md)
734. [planning-masters.test](modules/planning-masters.test.md)
735. [accessibilityInvariants](modules/accessibilityInvariants.md)
736. [modelAwareRouting](modules/modelAwareRouting.md)
737. [taskDetail](modules/taskDetail.md)
738. [lintRules.test](modules/lintRules.test.md)
739. [pageChrome](modules/pageChrome.md)
740. [renderWithProviders](modules/renderWithProviders.md)
741. [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md)
742. [UnscheduledTasks.test](modules/UnscheduledTasks.test.md)
743. [BareLayout.test](modules/BareLayout.test.md)
744. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
745. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
746. [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md)
747. [FilterBar.test](modules/FilterBar.test.md)
748. [OverflowMenu.test](modules/OverflowMenu.test.md)
749. [PageLayout.test](modules/PageLayout.test.md)
750. [ViewSwitch.test](modules/ViewSwitch.test.md)
751. [LandingPage.test](modules/LandingPage.test.md)
752. [renderWithProviders.test](modules/renderWithProviders.test.md)
753. [routeRegistry](modules/routeRegistry.md)
754. [setup](modules/setup.md)
755. [types_agent](modules/types_agent.md)
756. [analyticsScope](modules/analyticsScope.md)
757. [types_calendar](modules/types_calendar.md)
758. [deliveryMetrics](modules/deliveryMetrics.md)
759. [emailSettings](modules/emailSettings.md)
760. [executionUsage](modules/executionUsage.md)
761. [types_gantt](modules/types_gantt.md)
762. [types_github](modules/types_github.md)
763. [types_iteration](modules/types_iteration.md)
764. [types_label](modules/types_label.md)
765. [outboundWebhook](modules/outboundWebhook.md)
766. [types_project](modules/types_project.md)
767. [types_release](modules/types_release.md)
768. [requestSource](modules/requestSource.md)
769. [savedView](modules/savedView.md)
770. [schedulingRules](modules/schedulingRules.md)
771. [EffortModifierCard](modules/EffortModifierCard.md)
772. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
773. [SchedulingPassCard](modules/SchedulingPassCard.md)
774. [schedulingSearchLabels.test](modules/schedulingSearchLabels.test.md)
775. [systemSettings](modules/systemSettings.md)
776. [types_task](modules/types_task.md)
777. [types_team](modules/types_team.md)
778. [types_template](modules/types_template.md)
779. [types_triage](modules/types_triage.md)
780. [workMetrics](modules/workMetrics.md)
781. [agentAccess](modules/agentAccess.md)
782. [useAgentAccess](modules/useAgentAccess.md)
783. [apiError](modules/apiError.md)
784. [QueryState](modules/QueryState.md)
785. [taskEditorContract](modules/taskEditorContract.md)
786. [TaskBriefEditor](modules/TaskBriefEditor.md)
787. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
788. [TriageDraftPreview](modules/TriageDraftPreview.md)
789. [MutationSuccessFeedback](modules/MutationSuccessFeedback.md)
790. [mutationFeedback.test](modules/mutationFeedback.test.md)
791. [adminAccess](modules/adminAccess.md)
792. [OperatorIdentityNotice](modules/OperatorIdentityNotice.md)
793. [useAdminAccess](modules/useAdminAccess.md)
794. [api](modules/api.md)
795. [identityService](modules/identityService.md)
796. [NativeConnectionPage](modules/NativeConnectionPage.md)
797. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
798. [adminAccessService](modules/adminAccessService.md)
799. [AdminAccessPanel](modules/AdminAccessPanel.md)
800. [AdminAccessGate](modules/AdminAccessGate.md)
801. [AdminAccessGate.test](modules/AdminAccessGate.test.md)
802. [agentService](modules/agentService.md)
803. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
804. [useWaitingAgents](modules/useWaitingAgents.md)
805. [agentService.test](modules/agentService.test.md)
806. [deliveryMetricsService](modules/deliveryMetricsService.md)
807. [discussionService](modules/discussionService.md)
808. [emailSettingsService](modules/emailSettingsService.md)
809. [executionUsageService](modules/executionUsageService.md)
810. [ganttService](modules/ganttService.md)
811. [githubService](modules/githubService.md)
812. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
813. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
814. [labelService](modules/labelService.md)
815. [LabelSelector](modules/LabelSelector.md)
816. [outboundWebhookService](modules/outboundWebhookService.md)
817. [planShareService](modules/planShareService.md)
818. [planningInputService](modules/planningInputService.md)
819. [usePlanningObservation](modules/usePlanningObservation.md)
820. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
821. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
822. [calendarService](modules/calendarService.md)
823. [WorkCalendarSettings](modules/WorkCalendarSettings.md)
824. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
825. [WorkCalendarSettings.test](modules/WorkCalendarSettings.test.md)
826. [PersonCapacity](modules/PersonCapacity.md)
827. [PersonCapacity.test](modules/PersonCapacity.test.md)
828. [exportService](modules/exportService.md)
829. [IterationImportDialog](modules/IterationImportDialog.md)
830. [iterationService](modules/iterationService.md)
831. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
832. [planProgress.test](modules/planProgress.test.md)
833. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
834. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
835. [useWorkScope](modules/useWorkScope.md)
836. [useAnalyticsScope](modules/useAnalyticsScope.md)
837. [useWorkScope.test](modules/useWorkScope.test.md)
838. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
839. [IdentityProvider](modules/IdentityProvider.md)
840. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
841. [useLiveWindow.test](modules/useLiveWindow.test.md)
842. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
843. [planningInputService.test](modules/planningInputService.test.md)
844. [projectService](modules/projectService.md)
845. [AddMilestoneModal](modules/AddMilestoneModal.md)
846. [SetDatesPopover](modules/SetDatesPopover.md)
847. [CreateProjectModal](modules/CreateProjectModal.md)
848. [FirstRunLanding](modules/FirstRunLanding.md)
849. [useFirstRunProgress](modules/useFirstRunProgress.md)
850. [useGetStarted](modules/useGetStarted.md)
851. [useNextSetupAction](modules/useNextSetupAction.md)
852. [NextStepEmptyState](modules/NextStepEmptyState.md)
853. [NextStepEmptyState.test](modules/NextStepEmptyState.test.md)
854. [releaseService](modules/releaseService.md)
855. [requestSourceService](modules/requestSourceService.md)
856. [savedViewService](modules/savedViewService.md)
857. [schedulingRulesService](modules/schedulingRulesService.md)
858. [sessionService](modules/sessionService.md)
859. [snapshotService](modules/snapshotService.md)
860. [snapshotVersions.test](modules/snapshotVersions.test.md)
861. [systemSettingsService](modules/systemSettingsService.md)
862. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
863. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
864. [taskService](modules/taskService.md)
865. [DeliveryDependencies](modules/DeliveryDependencies.md)
866. [DeliveryDependencies.test](modules/DeliveryDependencies.test.md)
867. [ImportTasksModal](modules/ImportTasksModal.md)
868. [MetricCount](modules/MetricCount.md)
869. [TaskContextSummary](modules/TaskContextSummary.md)
870. [TaskDependencySelector](modules/TaskDependencySelector.md)
871. [TaskMergeDialog](modules/TaskMergeDialog.md)
872. [TaskOwnerAcceptance](modules/TaskOwnerAcceptance.md)
873. [TaskPostponeForm](modules/TaskPostponeForm.md)
874. [TaskRecordProvenance](modules/TaskRecordProvenance.md)
875. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
876. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
877. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
878. [useAgentRowFacts](modules/useAgentRowFacts.md)
879. [useTaskReviewer](modules/useTaskReviewer.md)
880. [TaskReviewer](modules/TaskReviewer.md)
881. [TriageActionModal](modules/TriageActionModal.md)
882. [overviewBacklog](modules/overviewBacklog.md)
883. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
884. [teamService](modules/teamService.md)
885. [TeamForm](modules/TeamForm.md)
886. [TeamForm.test](modules/TeamForm.test.md)
887. [capacityMutations](modules/capacityMutations.md)
888. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
889. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
890. [GanttBarInputs](modules/GanttBarInputs.md)
891. [AssigneePicker](modules/AssigneePicker.md)
892. [useTaskRowEdits](modules/useTaskRowEdits.md)
893. [useIterationRowData](modules/useIterationRowData.md)
894. [useTaskAssigneeDisplay](modules/useTaskAssigneeDisplay.md)
895. [TaskAssigneeDisplay](modules/TaskAssigneeDisplay.md)
896. [ImportTeamModal](modules/ImportTeamModal.md)
897. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
898. [VacationCsvImport](modules/VacationCsvImport.md)
899. [sampleProject](modules/sampleProject.md)
900. [SampleProjectAction](modules/SampleProjectAction.md)
901. [LocalProfilePicker](modules/LocalProfilePicker.md)
902. [GetStartedPanel](modules/GetStartedPanel.md)
903. [AccountMenu](modules/AccountMenu.md)
904. [UserSessionBadge](modules/UserSessionBadge.md)
905. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
906. [IdentityProvider.test](modules/IdentityProvider.test.md)
907. [usePlanScheduleWorkloads](modules/usePlanScheduleWorkloads.md)
908. [templateService](modules/templateService.md)
909. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
910. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
911. [timeEntryService](modules/timeEntryService.md)
912. [useTimeEntries](modules/useTimeEntries.md)
913. [timeEntryService.test](modules/timeEntryService.test.md)
914. [triageService](modules/triageService.md)
915. [AppSidebar](modules/AppSidebar.md)
916. [AppSidebar.planProgress.test](modules/AppSidebar.planProgress.test.md)
917. [AppSidebar.test](modules/AppSidebar.test.md)
918. [QuickCapture](modules/QuickCapture.md)
919. [QuickCapture.test](modules/QuickCapture.test.md)
920. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
921. [usePlanningReadiness](modules/usePlanningReadiness.md)
922. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
923. [planningScope.test](modules/planningScope.test.md)
924. [workspaceApi](modules/workspaceApi.md)
925. [pageChrome.test](modules/pageChrome.test.md)
926. [apiError.routing.test](modules/apiError.routing.test.md)
927. [copyText](modules/copyText.md)
928. [focusLifecycle](modules/focusLifecycle.md)
929. [focusLifecycle.test](modules/focusLifecycle.test.md)
930. [formatDate](modules/formatDate.md)
931. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
932. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
933. [VacationManager](modules/VacationManager.md)
934. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
935. [IterationForm](modules/IterationForm.md)
936. [IterationEditorDrawer](modules/IterationEditorDrawer.md)
937. [IterationForm.test](modules/IterationForm.test.md)
938. [ScopeBar](modules/ScopeBar.md)
939. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
940. [ScopeBar.test](modules/ScopeBar.test.md)
941. [NotificationsPanel](modules/NotificationsPanel.md)
942. [PlanIterationCheckpoint](modules/PlanIterationCheckpoint.md)
943. [PlanShareSection](modules/PlanShareSection.md)
944. [PlanReviewSection](modules/PlanReviewSection.md)
945. [PlanShareSection.test](modules/PlanShareSection.test.md)
946. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
947. [ConnectedReadersPanel](modules/ConnectedReadersPanel.md)
948. [ConnectedReadersPanel.test](modules/ConnectedReadersPanel.test.md)
949. [GitHubReconciliationPanel](modules/GitHubReconciliationPanel.md)
950. [GitHubReconciliationPanel.test](modules/GitHubReconciliationPanel.test.md)
951. [TaskDiscussion](modules/TaskDiscussion.md)
952. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
953. [TaskPostponementPanel](modules/TaskPostponementPanel.md)
954. [TaskReviewHistory](modules/TaskReviewHistory.md)
955. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
956. [TimeEntriesReport](modules/TimeEntriesReport.md)
957. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
958. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
959. [ModelCatalog](modules/ModelCatalog.md)
960. [RuntimeIdentity](modules/RuntimeIdentity.md)
961. [AgentManifestWorkflow](modules/AgentManifestWorkflow.md)
962. [AgentManifestWorkflow.test](modules/AgentManifestWorkflow.test.md)
963. [ConnectionSteps](modules/ConnectionSteps.md)
964. [ConnectionSteps.test](modules/ConnectionSteps.test.md)
965. [TeamProfileManager](modules/TeamProfileManager.md)
966. [TeamDirectory](modules/TeamDirectory.md)
967. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
968. [TriageRow](modules/TriageRow.md)
969. [TriageList](modules/TriageList.md)
970. [TriageList.test](modules/TriageList.test.md)
971. [TriageSuggestions](modules/TriageSuggestions.md)
972. [planEvidence](modules/planEvidence.md)
973. [PlanSharePage](modules/PlanSharePage.md)
974. [PlanSharePage.test](modules/PlanSharePage.test.md)
975. [scopedPageRender.test](modules/scopedPageRender.test.md)
976. [graphLimitError](modules/graphLimitError.md)
977. [modelRouting](modules/modelRouting.md)
978. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
979. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
980. [ConnectAgentSteps](modules/ConnectAgentSteps.md)
981. [ConnectAgentSteps.test](modules/ConnectAgentSteps.test.md)
982. [modelRouting.test](modules/modelRouting.test.md)
983. [protectedQueries](modules/protectedQueries.md)
984. [AssignedAgentsSummary](modules/AssignedAgentsSummary.md)
985. [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md)
986. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
987. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
988. [AgentAccessPanel](modules/AgentAccessPanel.md)
989. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
990. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
991. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
992. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
993. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
994. [QualificationKeysPanel](modules/QualificationKeysPanel.md)
995. [QualificationKeysPanel.test](modules/QualificationKeysPanel.test.md)
996. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
997. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
998. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
999. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
1000. [PipelineTaskEvidence](modules/PipelineTaskEvidence.md)
1001. [usePipeline](modules/usePipeline.md)
1002. [AgentModelAdministration](modules/AgentModelAdministration.md)
1003. [PipelineTaskEvidence.test](modules/PipelineTaskEvidence.test.md)
1004. [TeamPage](modules/TeamPage.md)
1005. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
1006. [IdentityProvider.keepRoute.test](modules/IdentityProvider.keepRoute.test.md)
1007. [TeamPage.test](modules/TeamPage.test.md)
1008. [TeamPage.transport.test](modules/TeamPage.transport.test.md)
1009. [routingCheck](modules/routingCheck.md)
1010. [RoutingCheckNotice](modules/RoutingCheckNotice.md)
1011. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
1012. [TaskBulkOperationsPanel.test](modules/TaskBulkOperationsPanel.test.md)
1013. [TaskBulkReassign.test](modules/TaskBulkReassign.test.md)
1014. [TaskReassign](modules/TaskReassign.md)
1015. [TaskRoutingSummary](modules/TaskRoutingSummary.md)
1016. [TaskSelectionBar](modules/TaskSelectionBar.md)
1017. [safeUrl](modules/safeUrl.md)
1018. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
1019. [ProjectRequestsTab](modules/ProjectRequestsTab.md)
1020. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
1021. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
1022. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
1023. [TriageDetailPanel](modules/TriageDetailPanel.md)
1024. [TriageConvertSource](modules/TriageConvertSource.md)
1025. [ConvertTriageDrawer](modules/ConvertTriageDrawer.md)
1026. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
1027. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
1028. [ContextHelp](modules/ContextHelp.md)
1029. [AppTopNav](modules/AppTopNav.md)
1030. [AppTopNav.test](modules/AppTopNav.test.md)
1031. [ContextHelp.test](modules/ContextHelp.test.md)
1032. [shellViewport.test](modules/shellViewport.test.md)
1033. [AccountMenu.test](modules/AccountMenu.test.md)
1034. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
1035. [SettingsPage](modules/SettingsPage.md)
1036. [SettingsPage.calendar.test](modules/SettingsPage.calendar.test.md)
1037. [SettingsPage.labels.test](modules/SettingsPage.labels.test.md)
1038. [SettingsPage.readOnlyPanels.test](modules/SettingsPage.readOnlyPanels.test.md)
1039. [SettingsPage.unlock.test](modules/SettingsPage.unlock.test.md)
1040. [taskFilterDefaults](modules/taskFilterDefaults.md)
1041. [TaskFiltersBar](modules/TaskFiltersBar.md)
1042. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
1043. [taskViewParams](modules/taskViewParams.md)
1044. [taskViewParams.test](modules/taskViewParams.test.md)
1045. [taskViewState](modules/taskViewState.md)
1046. [savedViewState](modules/savedViewState.md)
1047. [useSavedViewManager](modules/useSavedViewManager.md)
1048. [savedViewState.test](modules/savedViewState.test.md)
1049. [taskFilters](modules/taskFilters.md)
1050. [taskFilters.test](modules/taskFilters.test.md)
1051. [taskState](modules/taskState.md)
1052. [ReleaseForm](modules/ReleaseForm.md)
1053. [KanbanStoppedLane](modules/KanbanStoppedLane.md)
1054. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
1055. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
1056. [StatusChangeControl](modules/StatusChangeControl.md)
1057. [TaskSupersedeForm](modules/TaskSupersedeForm.md)
1058. [TaskWorkPanel](modules/TaskWorkPanel.md)
1059. [TaskOwnerAcceptance.test](modules/TaskOwnerAcceptance.test.md)
1060. [TaskPostponement.test](modules/TaskPostponement.test.md)
1061. [TaskReadView](modules/TaskReadView.md)
1062. [TaskReadView.brief.test](modules/TaskReadView.brief.test.md)
1063. [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md)
1064. [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md)
1065. [TaskReadView.test](modules/TaskReadView.test.md)
1066. [TaskReassign.test](modules/TaskReassign.test.md)
1067. [TaskRefusalNextSteps.test](modules/TaskRefusalNextSteps.test.md)
1068. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
1069. [taskSearchResults](modules/taskSearchResults.md)
1070. [CommandMenu](modules/CommandMenu.md)
1071. [AppShell](modules/AppShell.md)
1072. [App](modules/App.md)
1073. [App.legacyRoutes.test](modules/App.legacyRoutes.test.md)
1074. [AppShell.test](modules/AppShell.test.md)
1075. [CommandMenu.test](modules/CommandMenu.test.md)
1076. [taskStateChip](modules/taskStateChip.md)
1077. [KanbanCard](modules/KanbanCard.md)
1078. [KanbanColumn](modules/KanbanColumn.md)
1079. [KanbanColumn.test](modules/KanbanColumn.test.md)
1080. [TaskRow](modules/TaskRow.md)
1081. [StoppedWork.test](modules/StoppedWork.test.md)
1082. [TaskRow.test](modules/TaskRow.test.md)
1083. [src_main](modules/src_main.md)
1084. [SettingsPage.test](modules/SettingsPage.test.md)
1085. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
1086. [teamMemberLabels](modules/teamMemberLabels.md)
1087. [InitiativeForm](modules/InitiativeForm.md)
1088. [InitiativeGroupHeader](modules/InitiativeGroupHeader.md)
1089. [RoadmapView](modules/RoadmapView.md)
1090. [RoadmapView.test](modules/RoadmapView.test.md)
1091. [sampleProject.test](modules/sampleProject.test.md)
1092. [templateDefaults](modules/templateDefaults.md)
1093. [ProjectForm](modules/ProjectForm.md)
1094. [ProjectForm.test](modules/ProjectForm.test.md)
1095. [TaskForm](modules/TaskForm.md)
1096. [AssigneePicker.test](modules/AssigneePicker.test.md)
1097. [GuardedTaskDrawer](modules/GuardedTaskDrawer.md)
1098. [BacklogPanel](modules/BacklogPanel.md)
1099. [CurrentTaskDrawer.test](modules/CurrentTaskDrawer.test.md)
1100. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
1101. [TaskEditDrawer](modules/TaskEditDrawer.md)
1102. [GanttChart](modules/GanttChart.md)
1103. [GanttChart.test](modules/GanttChart.test.md)
1104. [TaskEditDrawer.test](modules/TaskEditDrawer.test.md)
1105. [ProjectTaskTree](modules/ProjectTaskTree.md)
1106. [ProjectTasksTab](modules/ProjectTasksTab.md)
1107. [ProjectTaskTree.test](modules/ProjectTaskTree.test.md)
1108. [TaskEditorDrawer.flow.test](modules/TaskEditorDrawer.flow.test.md)
1109. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
1110. [TaskForm.test](modules/TaskForm.test.md)
1111. [TaskFormSections.test](modules/TaskFormSections.test.md)
1112. [CreateTriageDrawer](modules/CreateTriageDrawer.md)
1113. [GanttPage](modules/GanttPage.md)
1114. [GanttPage.test](modules/GanttPage.test.md)
1115. [MyWorkPage](modules/MyWorkPage.md)
1116. [MyWorkPage.test](modules/MyWorkPage.test.md)
1117. [TriagePage](modules/TriagePage.md)
1118. [TriagePage.test](modules/TriagePage.test.md)
1119. [ganttChrome.test](modules/ganttChrome.test.md)
1120. [visibleWork](modules/visibleWork.md)
1121. [KanbanBoard](modules/KanbanBoard.md)
1122. [KanbanBoard.stopped.test](modules/KanbanBoard.stopped.test.md)
1123. [KanbanBoard.test](modules/KanbanBoard.test.md)
1124. [TaskList](modules/TaskList.md)
1125. [TaskList.test](modules/TaskList.test.md)
1126. [overviewSignals](modules/overviewSignals.md)
1127. [PipelineView](modules/PipelineView.md)
1128. [assigneeDisplay.test](modules/assigneeDisplay.test.md)
1129. [overviewSignals.test](modules/overviewSignals.test.md)
1130. [TasksPage](modules/TasksPage.md)
1131. [backlogScope.test](modules/backlogScope.test.md)
1132. [TasksPage.board.test](modules/TasksPage.board.test.md)
1133. [TasksPage.pipeline.test](modules/TasksPage.pipeline.test.md)
1134. [TasksPage.test](modules/TasksPage.test.md)
1135. [TasksPage.toolbar.test](modules/TasksPage.toolbar.test.md)
1136. [visibleWork.test](modules/visibleWork.test.md)
1137. [workNumbers](modules/workNumbers.md)
1138. [OnTrackSummary](modules/OnTrackSummary.md)
1139. [StatusDistribution](modules/StatusDistribution.md)
1140. [IterationOutlook.test](modules/IterationOutlook.test.md)
1141. [CapacityTable](modules/CapacityTable.md)
1142. [TeamList](modules/TeamList.md)
1143. [CapacitySection](modules/CapacitySection.md)
1144. [CapacitySection.test](modules/CapacitySection.test.md)
1145. [IterationCapacityLine](modules/IterationCapacityLine.md)
1146. [TeamList.test](modules/TeamList.test.md)
1147. [IterationList](modules/IterationList.md)
1148. [AllIterationsDrawer](modules/AllIterationsDrawer.md)
1149. [AllIterationsDrawer.test](modules/AllIterationsDrawer.test.md)
1150. [PlanBlockersSection](modules/PlanBlockersSection.md)
1151. [PlanIterationDrawers](modules/PlanIterationDrawers.md)
1152. [PlanScheduleSection](modules/PlanScheduleSection.md)
1153. [PlanWorkSection](modules/PlanWorkSection.md)
1154. [projectDetailShared](modules/projectDetailShared.md)
1155. [MilestoneFormDrawer](modules/MilestoneFormDrawer.md)
1156. [MilestonesSection](modules/MilestonesSection.md)
1157. [PostUpdateDrawer](modules/PostUpdateDrawer.md)
1158. [ProjectHeaderFields](modules/ProjectHeaderFields.md)
1159. [ProjectReleasesTab](modules/ProjectReleasesTab.md)
1160. [ProjectSummaryTab](modules/ProjectSummaryTab.md)
1161. [ProjectUpdatesTab](modules/ProjectUpdatesTab.md)
1162. [WorkMetricsLine](modules/WorkMetricsLine.md)
1163. [StoppedWorkCounts.test](modules/StoppedWorkCounts.test.md)
1164. [MetricCount.test](modules/MetricCount.test.md)
1165. [planningLinks.test](modules/planningLinks.test.md)
1166. [AnalyticsPage](modules/AnalyticsPage.md)
1167. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
1168. [scopedPages.test](modules/scopedPages.test.md)
1169. [AnalyticsPage.test](modules/AnalyticsPage.test.md)
1170. [OverviewPage](modules/OverviewPage.md)
1171. [GetStartedPanel.test](modules/GetStartedPanel.test.md)
1172. [OverviewPage.test](modules/OverviewPage.test.md)
1173. [PlanPage](modules/PlanPage.md)
1174. [planProgressPlacement.test](modules/planProgressPlacement.test.md)
1175. [GetStartedFlow.test](modules/GetStartedFlow.test.md)
1176. [PlanIterations.test](modules/PlanIterations.test.md)
1177. [PlanPage.test](modules/PlanPage.test.md)
1178. [ProjectDetailPage](modules/ProjectDetailPage.md)
1179. [ProjectDetailPage.test](modules/ProjectDetailPage.test.md)
1180. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
1181. [ProjectReleaseDetailPage.test](modules/ProjectReleaseDetailPage.test.md)
1182. [ProjectsPage](modules/ProjectsPage.md)
1183. [ProjectsPage.test](modules/ProjectsPage.test.md)
1184. [destinationEmptyStates.test](modules/destinationEmptyStates.test.md)
1185. [vite.config](modules/vite.config.md)
1186. [vitest.config](modules/vitest.config.md)
1187. [create_agent_actor](modules/create_agent_actor.md)
1188. [generate_workchord_keys](modules/generate_workchord_keys.md)
1189. [setup_agent_team](modules/setup_agent_team.md)
1190. [build_agent_skills](modules/build_agent_skills.md)
1191. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
1192. [android_qualification](modules/android_qualification.md)
1193. [android_web_peer](modules/android_web_peer.md)
1194. [apt_runtime](modules/apt_runtime.md)
1195. [browser_performance](modules/browser_performance.md)
1196. [browser_planning_inputs](modules/browser_planning_inputs.md)
1197. [browser_worker](modules/browser_worker.md)
1198. [browser_managed_work](modules/browser_managed_work.md)
1199. [browser_write_readback](modules/browser_write_readback.md)
1200. [check_markdown_links](modules/check_markdown_links.md)
1201. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
1202. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
1203. [ci_runtime](modules/ci_runtime.md)
1204. [classify_change_scope](modules/classify_change_scope.md)
1205. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
1206. [postgres_runtime](modules/postgres_runtime.md)
1207. [run_android_checks](modules/run_android_checks.md)
1208. [run_disposable_checks](modules/run_disposable_checks.md)
1209. [serve_disposable_api](modules/serve_disposable_api.md)
1210. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
1211. [test_apt_runtime](modules/test_apt_runtime.md)
1212. [test_check_markdown_links](modules/test_check_markdown_links.md)
1213. [test_ci_runtime](modules/test_ci_runtime.md)
1214. [test_classify_change_scope](modules/test_classify_change_scope.md)
1215. [test_native_runtimes](modules/test_native_runtimes.md)
1216. [test_wiki_lock_root_preflight](modules/test_wiki_lock_root_preflight.md)
1217. [wiki_lock_root_preflight](modules/wiki_lock_root_preflight.md)
1218. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
1219. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
1220. [generate_client_contract](modules/generate_client_contract.md)
1221. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
1222. [load_common](modules/load_common.md)
1223. [collect](modules/collect.md)
1224. [result](modules/result.md)
1225. [compare](modules/compare.md)
1226. [finalize](modules/finalize.md)
1227. [qualify](modules/qualify.md)
1228. [resilience](modules/resilience.md)
1229. [run](modules/run.md)
1230. [seal](modules/seal.md)
1231. [seed](modules/seed.md)
1232. [source_binding](modules/source_binding.md)
1233. [local_baseline](modules/local_baseline.md)
1234. [service_worksets](modules/service_worksets.md)
1235. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
1236. [isolated_rehearsal](modules/isolated_rehearsal.md)
1237. [seed_adoption_env](modules/seed_adoption_env.md)
1238. [write_deployment_record](modules/write_deployment_record.md)

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
| [models_task_replacement](modules/models_task_replacement.md) | `Task.successor_task_id = column_property`, `Task.successor_kind = column_property` |
| [team_member](modules/team_member.md) | `TeamMember.assignee_kind = column_property` |
| [observability](modules/observability.md) | `logger = logging.getLogger` |
| [refusal_next_steps](modules/refusal_next_steps.md) | `_RECORD_PROVENANCE = _step`, `_ASSIGN_INDEPENDENT_VERIFIER = _step`, `_READY_TEAM_ACTOR = _step`, `NOT_REFUSAL_CODES = frozenset` |
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
| [agent_team_setup_service](modules/agent_team_setup_service.md) | `CALLER_PRESENCE_BLOCKERS = frozenset` |
| [agent_work_service](modules/agent_work_service.md) | `logger = logging.getLogger` |
| [assignee_recommendation_service](modules/assignee_recommendation_service.md) | `TOKEN_PATTERN = re.compile` |
| [email_settings_service](modules/email_settings_service.md) | `logger = logging.getLogger` |
| [execution_planning_window](modules/execution_planning_window.md) | `PLANNING_ONLY_FIELDS = frozenset` |
| [github_status_service](modules/github_status_service.md) | `logger = logging.getLogger` |
| [import_review_service](modules/import_review_service.md) | `_DIGEST_PATTERN = re.compile` |
| [language_service](modules/language_service.md) | `_CYRILLIC_RE = re.compile`, `_LATIN_RE = re.compile`, `logger = logging.getLogger` |
| [llm_service](modules/llm_service.md) | `logger = logging.getLogger` |
| [maintenance_window_service](modules/maintenance_window_service.md) | `MAX_WINDOW = timedelta` |
| [notification_service](modules/notification_service.md) | `logger = logging.getLogger` |
| [outbound_webhook_service](modules/outbound_webhook_service.md) | `logger = logging.getLogger` |
| [planning_window_reconciliation](modules/planning_window_reconciliation.md) | `_EVIDENCE_DIGEST = re.compile`, `_SNAPSHOT_CACHE = OrderedDict`, `_CACHE_LOCK = Lock` |
| [routing_calibration_contract_service](modules/routing_calibration_contract_service.md) | `_REVIEW_CLOCK_SKEW = timedelta` |
| [scheduler_service](modules/scheduler_service.md) | `logger = logging.getLogger` |
| [scheduling_rules_service](modules/scheduling_rules_service.md) | `logger = logging.getLogger`, `CONDITION_PATTERN = re.compile` |
| [session_service](modules/session_service.md) | `_SESSION_TOKEN_PATTERN = re.compile` |
| [snapshot_service](modules/snapshot_service.md) | `SNAPSHOTS_DIR = Path`, `SNAPSHOT_REASON_PATTERN = re.compile`, `SNAPSHOT_FILENAME_PATTERN = re.compile` |
| [system_settings_service](modules/system_settings_service.md) | `logger = logging.getLogger`, `LEGACY_EMAIL_SETTINGS_FILE = Path` |
| [task_display_state](modules/task_display_state.md) | `STORED_STATES = tuple` |
| [task_reactivation_service](modules/task_reactivation_service.md) | `logger = logging.getLogger` |
| [task_replacement_service](modules/task_replacement_service.md) | `logger = logging.getLogger` |
| [task_routing_service](modules/task_routing_service.md) | `_TEXT_ROUTING = re.compile`, `_FIRST_SENTENCE = re.compile`, `_INLINE = re.compile`, `_MOVES = re.compile`, `_REVIEWER = re.compile`, `_INDEPENDENT = re.compile` |
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
| [test_routing_calibration_contracts_migration](modules/test_routing_calibration_contracts_migration.md) | `_CONTRACT_ROW = text` |
| [test_routing_qualification_keys_migration](modules/test_routing_qualification_keys_migration.md) | `_CATALOG_ROW = text`, `_KEY_ROW = text` |
| [test_task_postponement_migration](modules/test_task_postponement_migration.md) | `AT = datetime` |
| [test_task_supersession_migration](modules/test_task_supersession_migration.md) | `MIGRATION = importlib.import_module` |
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
| [test_refusal_next_steps](modules/test_refusal_next_steps.md) | `CODE_SHAPE = re.compile` |
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
| [StoppedWorkCounts.test](modules/StoppedWorkCounts.test.md) | `mock`, `beforeEach`, `describe` |
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
| [UnscheduledTasks.test](modules/UnscheduledTasks.test.md) | `it`, `it`, `it`, `it` |
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
| [QualificationKeysPanel.test](modules/QualificationKeysPanel.test.md) | `agentServiceMock = hoisted`, `mock`, `describe` |
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
| [KanbanBoard.stopped.test](modules/KanbanBoard.stopped.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [KanbanBoard.test](modules/KanbanBoard.test.md) | `dragState = hoisted`, `taskServiceMock = hoisted`, `teamServiceMock = hoisted`, `planningMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [KanbanColumn.test](modules/KanbanColumn.test.md) | `mock`, `mock`, `describe`, `describe` |
| [MetricCount.test](modules/MetricCount.test.md) | `service = hoisted`, `mock`, `describe` |
| [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md) | `lookup = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it` |
| [PersonCapacity.test](modules/PersonCapacity.test.md) | `api = hoisted`, `mock`, `beforeEach`, `it`, `it` |
| [PipelineTaskEvidence](modules/PipelineTaskEvidence.md) | `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set` |
| [PipelineView](modules/PipelineView.md) | `HUMAN_GATED_STAGES = Set` |
| [QuickCapture.test](modules/QuickCapture.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it` |
| [SavedViewsControl](modules/SavedViewsControl.md) | `t = bind` |
| [StoppedWork.test](modules/StoppedWork.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `describe`, `describe`, `describe`, `describe` |
| [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md) | `describe` |
| [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md) | `t = bind` |
| [TaskBriefEditor.test](modules/TaskBriefEditor.test.md) | `describe` |
| [TaskBulkOperationsPanel.test](modules/TaskBulkOperationsPanel.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskBulkReassign.test](modules/TaskBulkReassign.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [TaskDependencySelector](modules/TaskDependencySelector.md) | `t = bind` |
| [TaskDiscussion.test](modules/TaskDiscussion.test.md) | `service = hoisted`, `mock`, `describe` |
| [TaskEditorDrawer.flow.test](modules/TaskEditorDrawer.flow.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `describe`, `describe` |
| [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `it` |
| [TaskFiltersBar.test](modules/TaskFiltersBar.test.md) | `mock`, `mock`, `mock`, `describe` |
| [TaskForm.test](modules/TaskForm.test.md) | `api = hoisted`, `mock`, `describe`, `describe` |
| [TaskFormSections.test](modules/TaskFormSections.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `teamMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `it`, `it`, `it`, `describe`, `describe`, `describe` |
| [TaskOwnerAcceptance.test](modules/TaskOwnerAcceptance.test.md) | `service = hoisted`, `mock`, `mock`, `describe` |
| [TaskPostponement.test](modules/TaskPostponement.test.md) | `service = hoisted`, `mock`, `mock`, `beforeEach`, `describe`, `describe`, `describe` |
| [TaskReadView.brief.test](modules/TaskReadView.brief.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `it.each(['en', 'ru'])` |
| [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskReadView.test](modules/TaskReadView.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `describe`, `describe` |
| [TaskReassign.test](modules/TaskReassign.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `describe` |
| [TaskRefusalNextSteps.test](modules/TaskRefusalNextSteps.test.md) | `service = hoisted`, `mock`, `mock`, `describe`, `describe` |
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
| [planningTaskIssues.test](modules/planningTaskIssues.test.md) | `describe`, `describe`, `describe` |
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
| [MyWorkPage.test](modules/MyWorkPage.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `it`, `it`, `it`, `it`, `it.each(['active', 'review', 'inbox'])`, `describe`, `describe`, `it.each(['active', 'queued', 'blocked', 'awaiting_review', 'review'])`, `it`, `it.each(['active', 'inbox'])`, `it`, `it`, `it` |
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
| [apiError.routing.test](modules/apiError.routing.test.md) | `describe` |
| [focusLifecycle.test](modules/focusLifecycle.test.md) | `describe` |
| [modelRouting.test](modules/modelRouting.test.md) | `describe` |
| [modelRouting](modules/modelRouting.md) | `ADVANCED_REASON_CODES = Set`, `INDEPENDENT_REASON_CODES = Set`, `STANDARD_REVIEW_REASON_CODES = Set` |
| [savedViewState.test](modules/savedViewState.test.md) | `describe` |
| [taskFilters.test](modules/taskFilters.test.md) | `describe`, `describe`, `describe`, `describe`, `describe` |
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
| `create_task` | factory | [test_task_routing_consistency](modules/test_task_routing_consistency.md) |
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
