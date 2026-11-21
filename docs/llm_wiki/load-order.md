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
52. [20261120_0018_review_provenance](modules/20261120_0018_review_provenance.md)
53. [20261121_0019_execution_planning_window](modules/20261121_0019_execution_planning_window.md)
54. [20261121_0020_annual_calendar_coverage](modules/20261121_0020_annual_calendar_coverage.md)
55. [query_limits](modules/query_limits.md)
56. [runtime_telemetry](modules/runtime_telemetry.md)
57. [database_runtime](modules/database_runtime.md)
58. [maintenance](modules/maintenance.md)
59. [mutation_versions](modules/mutation_versions.md)
60. [schemas_agent_connect](modules/schemas_agent_connect.md)
61. [schemas_agent_planning](modules/schemas_agent_planning.md)
62. [agent_skill_bundle](modules/agent_skill_bundle.md)
63. [agent_team_setup](modules/agent_team_setup.md)
64. [schemas_autonomy](modules/schemas_autonomy.md)
65. [schemas_common](modules/schemas_common.md)
66. [delivery_metrics](modules/delivery_metrics.md)
67. [schemas_execution_usage](modules/schemas_execution_usage.md)
68. [schemas_github](modules/schemas_github.md)
69. [schemas_intake](modules/schemas_intake.md)
70. [schemas_label](modules/schemas_label.md)
71. [schemas_plan_share](modules/schemas_plan_share.md)
72. [planning_inputs](modules/planning_inputs.md)
73. [schemas_calendar](modules/schemas_calendar.md)
74. [schemas_review_evidence](modules/schemas_review_evidence.md)
75. [schemas_saved_view](modules/schemas_saved_view.md)
76. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
77. [schemas_session](modules/schemas_session.md)
78. [snapshot](modules/snapshot.md)
79. [schemas_system_settings](modules/schemas_system_settings.md)
80. [schemas_email_settings](modules/schemas_email_settings.md)
81. [schemas_task_brief](modules/schemas_task_brief.md)
82. [schemas_llm](modules/schemas_llm.md)
83. [schemas_task_domain](modules/schemas_task_domain.md)
84. [schemas_team](modules/schemas_team.md)
85. [schemas_template](modules/schemas_template.md)
86. [schemas_time_entry](modules/schemas_time_entry.md)
87. [time_report](modules/time_report.md)
88. [schemas_work_metrics](modules/schemas_work_metrics.md)
89. [schemas_iteration](modules/schemas_iteration.md)
90. [schemas_project](modules/schemas_project.md)
91. [schemas_release](modules/schemas_release.md)
92. [security](modules/security.md)
93. [server_features](modules/server_features.md)
94. [agent_routing_policy](modules/agent_routing_policy.md)
95. [agent_routing](modules/agent_routing.md)
96. [agent_routing_rollout](modules/agent_routing_rollout.md)
97. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
98. [routers_agent_connect](modules/routers_agent_connect.md)
99. [agent_team_credentials](modules/agent_team_credentials.md)
100. [bounded_scope_reads](modules/bounded_scope_reads.md)
101. [language_service](modules/language_service.md)
102. [plan_checkpoints](modules/plan_checkpoints.md)
103. [planning_input_context](modules/planning_input_context.md)
104. [planning_issues](modules/planning_issues.md)
105. [scheduling_rules_service](modules/scheduling_rules_service.md)
106. [upgrade_service](modules/upgrade_service.md)
107. [upgrade](modules/upgrade.md)
108. [settings_read](modules/settings_read.md)
109. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
110. [sql_semantics](modules/sql_semantics.md)
111. [exceptions](modules/exceptions.md)
112. [github_links](modules/github_links.md)
113. [text_similarity](modules/text_similarity.md)
114. [time](modules/time.md)
115. [observability](modules/observability.md)
116. [app_database](modules/app_database.md)
117. [models_autonomy](modules/models_autonomy.md)
118. [models_calendar](modules/models_calendar.md)
119. [models_capacity](modules/models_capacity.md)
120. [models_database_migration](modules/models_database_migration.md)
121. [delivery_dependency](modules/delivery_dependency.md)
122. [models_discussion](modules/models_discussion.md)
123. [models_execution_usage](modules/models_execution_usage.md)
124. [models_external_link](modules/models_external_link.md)
125. [models_github](modules/models_github.md)
126. [models_identity](modules/models_identity.md)
127. [models_iteration](modules/models_iteration.md)
128. [models_label](modules/models_label.md)
129. [native_connection](modules/native_connection.md)
130. [models_outbound_webhook](modules/models_outbound_webhook.md)
131. [models_plan_share](modules/models_plan_share.md)
132. [models_release](modules/models_release.md)
133. [models_project](modules/models_project.md)
134. [models_request_source](modules/models_request_source.md)
135. [models_runtime_observation](modules/models_runtime_observation.md)
136. [models_saved_view](modules/models_saved_view.md)
137. [models_system_settings](modules/models_system_settings.md)
138. [models_task](modules/models_task.md)
139. [recovery](modules/recovery.md)
140. [models_task_brief](modules/models_task_brief.md)
141. [task_status_log](modules/task_status_log.md)
142. [team_member](modules/team_member.md)
143. [models_agent](modules/models_agent.md)
144. [delivery_observation](modules/delivery_observation.md)
145. [models_template](modules/models_template.md)
146. [models_time_entry](modules/models_time_entry.md)
147. [models_triage](modules/models_triage.md)
148. [user_session](modules/user_session.md)
149. [models___init__](modules/models___init__.md)
150. [catalog](modules/catalog.md)
151. [database_migration_canonical](modules/database_migration_canonical.md)
152. [source](modules/source.md)
153. [transfer](modules/transfer.md)
154. [cli_database_migration](modules/cli_database_migration.md)
155. [database_migration___init__](modules/database_migration___init__.md)
156. [migrations_env](modules/migrations_env.md)
157. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
158. [calendar_rules](modules/calendar_rules.md)
159. [calendar_service](modules/calendar_service.md)
160. [calendars](modules/calendars.md)
161. [capacity_service](modules/capacity_service.md)
162. [routers_capacity](modules/routers_capacity.md)
163. [delivery_dependency_service](modules/delivery_dependency_service.md)
164. [delivery_metrics_service](modules/delivery_metrics_service.md)
165. [discussion_service](modules/discussion_service.md)
166. [execution_planning_window](modules/execution_planning_window.md)
167. [allocation_removal](modules/allocation_removal.md)
168. [identity_service](modules/identity_service.md)
169. [import_planning_service](modules/import_planning_service.md)
170. [iteration_service](modules/iteration_service.md)
171. [iterations](modules/iterations.md)
172. [label_service](modules/label_service.md)
173. [labels](modules/labels.md)
174. [native_session_service](modules/native_session_service.md)
175. [saved_view_service](modules/saved_view_service.md)
176. [session_service](modules/session_service.md)
177. [http_authority](modules/http_authority.md)
178. [routers_identity](modules/routers_identity.md)
179. [saved_views](modules/saved_views.md)
180. [routers_session](modules/routers_session.md)
181. [task_brief_service](modules/task_brief_service.md)
182. [task_context_revision_service](modules/task_context_revision_service.md)
183. [task_domain_service](modules/task_domain_service.md)
184. [task_hierarchy_service](modules/task_hierarchy_service.md)
185. [task_recovery_service](modules/task_recovery_service.md)
186. [task_timeline_service](modules/task_timeline_service.md)
187. [team_service](modules/team_service.md)
188. [routers_team](modules/routers_team.md)
189. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
190. [snapshot_service](modules/snapshot_service.md)
191. [plan_share_service](modules/plan_share_service.md)
192. [plan_shares](modules/plan_shares.md)
193. [template_service](modules/template_service.md)
194. [templates](modules/templates.md)
195. [time_entry_service](modules/time_entry_service.md)
196. [time_report_service](modules/time_report_service.md)
197. [services_work_metrics](modules/services_work_metrics.md)
198. [import_parser](modules/import_parser.md)
199. [url_policy](modules/url_policy.md)
200. [schemas_external_link](modules/schemas_external_link.md)
201. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
202. [schemas_request_source](modules/schemas_request_source.md)
203. [schemas_task](modules/schemas_task.md)
204. [schemas_gantt](modules/schemas_gantt.md)
205. [task_detail](modules/task_detail.md)
206. [schemas_triage](modules/schemas_triage.md)
207. [schemas___init__](modules/schemas___init__.md)
208. [schemas_agent](modules/schemas_agent.md)
209. [agent_run_read](modules/agent_run_read.md)
210. [schemas_runtime_observation](modules/schemas_runtime_observation.md)
211. [agent_readiness](modules/agent_readiness.md)
212. [llm_service](modules/llm_service.md)
213. [review_provenance](modules/review_provenance.md)
214. [runtime_observation_service](modules/runtime_observation_service.md)
215. [system_settings_service](modules/system_settings_service.md)
216. [routers_system_settings](modules/routers_system_settings.md)
217. [email_settings_service](modules/email_settings_service.md)
218. [routers_email_settings](modules/routers_email_settings.md)
219. [notification_service](modules/notification_service.md)
220. [outbound_webhook_service](modules/outbound_webhook_service.md)
221. [worker](modules/worker.md)
222. [outbound_webhooks](modules/outbound_webhooks.md)
223. [external_link_service](modules/external_link_service.md)
224. [github_status_service](modules/github_status_service.md)
225. [request_source_service](modules/request_source_service.md)
226. [request_sources](modules/request_sources.md)
227. [project_service](modules/project_service.md)
228. [task_detail_service](modules/task_detail_service.md)
229. [task_import_service](modules/task_import_service.md)
230. [task_service](modules/task_service.md)
231. [export](modules/export.md)
232. [snapshots](modules/snapshots.md)
233. [agent_routing_observability](modules/agent_routing_observability.md)
234. [agent_service](modules/agent_service.md)
235. [agent_skill_bundles](modules/agent_skill_bundles.md)
236. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
237. [agent_routing_service](modules/agent_routing_service.md)
238. [agent_team_setup_service](modules/agent_team_setup_service.md)
239. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
240. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
241. [execution_reconciliation](modules/execution_reconciliation.md)
242. [execution_usage_service](modules/execution_usage_service.md)
243. [routers_task_domain](modules/routers_task_domain.md)
244. [delivery_dependencies](modules/delivery_dependencies.md)
245. [routers_discussion](modules/routers_discussion.md)
246. [time_entries](modules/time_entries.md)
247. [agent_run_read_service](modules/agent_run_read_service.md)
248. [github_status_automation_service](modules/github_status_automation_service.md)
249. [release_service](modules/release_service.md)
250. [projects](modules/projects.md)
251. [services_review_evidence](modules/services_review_evidence.md)
252. [scheduler_service](modules/scheduler_service.md)
253. [routers_gantt](modules/routers_gantt.md)
254. [routers_llm](modules/routers_llm.md)
255. [agent_planning_service](modules/agent_planning_service.md)
256. [planning_window_reconciliation](modules/planning_window_reconciliation.md)
257. [retained_planning_output](modules/retained_planning_output.md)
258. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
259. [tasks](modules/tasks.md)
260. [task_status_service](modules/task_status_service.md)
261. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
262. [triage_service](modules/triage_service.md)
263. [routers_triage](modules/routers_triage.md)
264. [agent_work_service](modules/agent_work_service.md)
265. [mcp_agent_tools](modules/mcp_agent_tools.md)
266. [mcp_server](modules/mcp_server.md)
267. [routers_agent](modules/routers_agent.md)
268. [routers_agent_planning](modules/routers_agent_planning.md)
269. [agent_catalog](modules/agent_catalog.md)
270. [github_webhook_service](modules/github_webhook_service.md)
271. [routers_github](modules/routers_github.md)
272. [web_intake_service](modules/web_intake_service.md)
273. [routers_intake](modules/routers_intake.md)
274. [app_main](modules/app_main.md)
275. [routers___init__](modules/routers___init__.md)
276. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
277. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
278. [test_server_acceptance](modules/test_server_acceptance.md)
279. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
280. [test_work_package_service](modules/test_work_package_service.md)
281. [test_database_configuration](modules/test_database_configuration.md)
282. [test_deployment_topology](modules/test_deployment_topology.md)
283. [test_observability](modules/test_observability.md)
284. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
285. [test_query_boundaries](modules/test_query_boundaries.md)
286. [test_runtime_policy](modules/test_runtime_policy.md)
287. [test_schema_behavior](modules/test_schema_behavior.md)
288. [test_cutover_evidence](modules/test_cutover_evidence.md)
289. [test_documentation_boundary](modules/test_documentation_boundary.md)
290. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
291. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
292. [test_source_preflight](modules/test_source_preflight.md)
293. [test_transfer_catalog](modules/test_transfer_catalog.md)
294. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
295. [0001_wave0_probe](modules/0001_wave0_probe.md)
296. [test_allocation_identity](modules/test_allocation_identity.md)
297. [test_annual_calendar_migration](modules/test_annual_calendar_migration.md)
298. [test_initial_schema](modules/test_initial_schema.md)
299. [test_profile_identity](modules/test_profile_identity.md)
300. [test_android_cleanup](modules/test_android_cleanup.md)
301. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
302. [test_load_tooling](modules/test_load_tooling.md)
303. [test_local_baseline](modules/test_local_baseline.md)
304. [test_routing_evidence](modules/test_routing_evidence.md)
305. [support_database](modules/support_database.md)
306. [delivery](modules/delivery.md)
307. [factories](modules/factories.md)
308. [faults](modules/faults.md)
309. [runtime_peer](modules/runtime_peer.md)
310. [schema](modules/schema.md)
311. [support___init__](modules/support___init__.md)
312. [conftest](modules/conftest.md)
313. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
314. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
315. [test_project_identity](modules/test_project_identity.md)
316. [test_project_identity_scope](modules/test_project_identity_scope.md)
317. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
318. [transactions](modules/transactions.md)
319. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
320. [test_agent_key_delivery](modules/test_agent_key_delivery.md)
321. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
322. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
323. [test_agent_routing_data](modules/test_agent_routing_data.md)
324. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
325. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
326. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
327. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
328. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
329. [test_agent_routing_service](modules/test_agent_routing_service.md)
330. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
331. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
332. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
333. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
334. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
335. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
336. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
337. [test_authority_migrations](modules/test_authority_migrations.md)
338. [test_capacity_contract](modules/test_capacity_contract.md)
339. [test_client_contract](modules/test_client_contract.md)
340. [test_database_harness](modules/test_database_harness.md)
341. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
342. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
343. [test_agent_discovery_report](modules/test_agent_discovery_report.md)
344. [test_agent_team_setup](modules/test_agent_team_setup.md)
345. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
346. [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md)
347. [test_analytics_scopes](modules/test_analytics_scopes.md)
348. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
349. [test_dependency_date_cascade](modules/test_dependency_date_cascade.md)
350. [test_deployment_configuration](modules/test_deployment_configuration.md)
351. [test_effective_deferral](modules/test_effective_deferral.md)
352. [test_execution_usage](modules/test_execution_usage.md)
353. [test_execution_working_dates](modules/test_execution_working_dates.md)
354. [test_harness_session_metadata](modules/test_harness_session_metadata.md)
355. [test_managed_authority](modules/test_managed_authority.md)
356. [test_allocation_recovery](modules/test_allocation_recovery.md)
357. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
358. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
359. [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md)
360. [test_metric_matches](modules/test_metric_matches.md)
361. [test_mobile_contract](modules/test_mobile_contract.md)
362. [test_mutation_versions](modules/test_mutation_versions.md)
363. [test_native_connections](modules/test_native_connections.md)
364. [test_observer_sessions](modules/test_observer_sessions.md)
365. [test_agdash_link_provider](modules/test_agdash_link_provider.md)
366. [test_person_assignment_reads](modules/test_person_assignment_reads.md)
367. [test_person_run_reads](modules/test_person_run_reads.md)
368. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
369. [test_plan_shares](modules/test_plan_shares.md)
370. [test_planning_input_context](modules/test_planning_input_context.md)
371. [test_planning_issues](modules/test_planning_issues.md)
372. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
373. [test_process_roles](modules/test_process_roles.md)
374. [test_profile_capacity](modules/test_profile_capacity.md)
375. [test_annual_calendar_coverage](modules/test_annual_calendar_coverage.md)
376. [test_planning_read_models](modules/test_planning_read_models.md)
377. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
378. [test_project_review_policy](modules/test_project_review_policy.md)
379. [test_project_working_timezone](modules/test_project_working_timezone.md)
380. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
381. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
382. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
383. [test_runtime_observations](modules/test_runtime_observations.md)
384. [test_saved_view_service](modules/test_saved_view_service.md)
385. [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md)
386. [test_scheduler_dependencies](modules/test_scheduler_dependencies.md)
387. [test_schedule_working_date](modules/test_schedule_working_date.md)
388. [test_server_features](modules/test_server_features.md)
389. [test_settings_read_access](modules/test_settings_read_access.md)
390. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
391. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
392. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
393. [test_task_domain](modules/test_task_domain.md)
394. [test_acceptance_attribution](modules/test_acceptance_attribution.md)
395. [test_delivery_metrics](modules/test_delivery_metrics.md)
396. [test_human_work_queries](modules/test_human_work_queries.md)
397. [test_task_discussion](modules/test_task_discussion.md)
398. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
399. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
400. [test_task_pagination](modules/test_task_pagination.md)
401. [test_team_member_agent_connected](modules/test_team_member_agent_connected.md)
402. [test_task_assignee_kind](modules/test_task_assignee_kind.md)
403. [test_team_pm_dispatch](modules/test_team_pm_dispatch.md)
404. [test_review_provenance](modules/test_review_provenance.md)
405. [test_scoped_review_evidence](modules/test_scoped_review_evidence.md)
406. [test_routing_preview_size](modules/test_routing_preview_size.md)
407. [test_team_pm_recovery](modules/test_team_pm_recovery.md)
408. [test_execution_reconciliation](modules/test_execution_reconciliation.md)
409. [test_review_provenance_transports](modules/test_review_provenance_transports.md)
410. [test_execution_planning_window](modules/test_execution_planning_window.md)
411. [test_annual_calendar_work_control](modules/test_annual_calendar_work_control.md)
412. [test_manual_review_provenance](modules/test_manual_review_provenance.md)
413. [test_pm_forecast_calendar](modules/test_pm_forecast_calendar.md)
414. [test_supervised_shadow_rework](modules/test_supervised_shadow_rework.md)
415. [test_team_topology_read](modules/test_team_topology_read.md)
416. [test_time_entries](modules/test_time_entries.md)
417. [test_time_reports](modules/test_time_reports.md)
418. [test_unscheduled_tasks](modules/test_unscheduled_tasks.md)
419. [test_unused_allocation](modules/test_unused_allocation.md)
420. [test_verification_preview_history](modules/test_verification_preview_history.md)
421. [test_work_correctness](modules/test_work_correctness.md)
422. [test_work_delivery_links](modules/test_work_delivery_links.md)
423. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
424. [single-page-toolbar](modules/single-page-toolbar.md)
425. [eslint.config](modules/eslint.config.md)
426. [postcss.config](modules/postcss.config.md)
427. [check-bundle-budget](modules/check-bundle-budget.md)
428. [check-query-feedback](modules/check-query-feedback.md)
429. [check-task-selection-layout](modules/check-task-selection-layout.md)
430. [find-unread-i18n-keys](modules/find-unread-i18n-keys.md)
431. [find-unused-exports](modules/find-unused-exports.md)
432. [Checkbox](modules/Checkbox.md)
433. [CollapsibleSection](modules/CollapsibleSection.md)
434. [DisabledReason](modules/DisabledReason.md)
435. [Input](modules/Input.md)
436. [Input.test](modules/Input.test.md)
437. [Select](modules/Select.md)
438. [Textarea](modules/Textarea.md)
439. [buttonStyles](modules/buttonStyles.md)
440. [Button](modules/Button.md)
441. [Button.test](modules/Button.test.md)
442. [ButtonLink](modules/ButtonLink.md)
443. [ButtonLink.test](modules/ButtonLink.test.md)
444. [dialogLayer](modules/dialogLayer.md)
445. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
446. [Modal](modules/Modal.md)
447. [ConfirmDialog](modules/ConfirmDialog.md)
448. [formControlLabels.test](modules/formControlLabels.test.md)
449. [iconButtonTooltips.test](modules/iconButtonTooltips.test.md)
450. [leaveGuardBypass](modules/leaveGuardBypass.md)
451. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
452. [useConfirmDialog](modules/useConfirmDialog.md)
453. [LiveWindowStatus](modules/LiveWindowStatus.md)
454. [WorkFreshness](modules/WorkFreshness.md)
455. [toast](modules/toast.md)
456. [ToastProvider](modules/ToastProvider.md)
457. [ToastProvider.test](modules/ToastProvider.test.md)
458. [UnscheduledTasks](modules/UnscheduledTasks.md)
459. [AnnualCalendarFields](modules/AnnualCalendarFields.md)
460. [LabelChip](modules/LabelChip.md)
461. [BrandMark](modules/BrandMark.md)
462. [ScopePicker](modules/ScopePicker.md)
463. [commandMenuEvents](modules/commandMenuEvents.md)
464. [setupGuideEvents](modules/setupGuideEvents.md)
465. [ProjectIterationsTab](modules/ProjectIterationsTab.md)
466. [projectPortfolio](modules/projectPortfolio.md)
467. [AccessKeysSummary](modules/AccessKeysSummary.md)
468. [AgentTeamManifestPreview](modules/AgentTeamManifestPreview.md)
469. [ConstraintsPanel](modules/ConstraintsPanel.md)
470. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
471. [SettingsUnsavedBar](modules/SettingsUnsavedBar.md)
472. [WithheldValuesNote](modules/WithheldValuesNote.md)
473. [protectedQueryKeys](modules/protectedQueryKeys.md)
474. [settingsFieldLabels](modules/settingsFieldLabels.md)
475. [sharedUnlock](modules/sharedUnlock.md)
476. [ReadOnlyFieldset](modules/ReadOnlyFieldset.md)
477. [AssigneeSelect](modules/AssigneeSelect.md)
478. [claimTime](modules/claimTime.md)
479. [SortableTaskItem](modules/SortableTaskItem.md)
480. [TaskCreateSections](modules/TaskCreateSections.md)
481. [TaskViewOptions](modules/TaskViewOptions.md)
482. [taskDraftStorage](modules/taskDraftStorage.md)
483. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
484. [taskRowValues](modules/taskRowValues.md)
485. [taskSearchResults](modules/taskSearchResults.md)
486. [taskStateChip](modules/taskStateChip.md)
487. [useDraftDismissal](modules/useDraftDismissal.md)
488. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
489. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
490. [useTaskSelection](modules/useTaskSelection.md)
491. [ModelBindings](modules/ModelBindings.md)
492. [directoryModel](modules/directoryModel.md)
493. [directoryModel.test](modules/directoryModel.test.md)
494. [FilterBar](modules/FilterBar.md)
495. [InlineEmptyState](modules/InlineEmptyState.md)
496. [MasterProgress](modules/MasterProgress.md)
497. [MasterProgress.test](modules/MasterProgress.test.md)
498. [OverflowMenu](modules/OverflowMenu.md)
499. [PageLayout](modules/PageLayout.md)
500. [PageToolbar.layout.test](modules/PageToolbar.layout.test.md)
501. [PageToolbar](modules/PageToolbar.md)
502. [PageToolbar.test](modules/PageToolbar.test.md)
503. [SectionCard](modules/SectionCard.md)
504. [SegmentedControl](modules/SegmentedControl.md)
505. [Select.test](modules/Select.test.md)
506. [SlideOverDrawer](modules/SlideOverDrawer.md)
507. [StickyRail](modules/StickyRail.md)
508. [ViewSwitch](modules/ViewSwitch.md)
509. [index](modules/index.md)
510. [tone](modules/tone.md)
511. [projectStatusStyles](modules/projectStatusStyles.md)
512. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
513. [Pill](modules/Pill.md)
514. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
515. [tone.test](modules/tone.test.md)
516. [agentDispatch](modules/agentDispatch.md)
517. [taskRowParts](modules/taskRowParts.md)
518. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
519. [connectAgent](modules/connectAgent.md)
520. [ConnectionSteps](modules/ConnectionSteps.md)
521. [manifestLocations](modules/manifestLocations.md)
522. [manifestLocations.test](modules/manifestLocations.test.md)
523. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
524. [AgentTeamStepList](modules/AgentTeamStepList.md)
525. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
526. [statusScopes](modules/statusScopes.md)
527. [statusScopes.test](modules/statusScopes.test.md)
528. [firstRunSteps](modules/firstRunSteps.md)
529. [getStartedVisibility](modules/getStartedVisibility.md)
530. [sampleProject.fixture](modules/sampleProject.fixture.md)
531. [sampleProjectStore](modules/sampleProjectStore.md)
532. [setupReturn](modules/setupReturn.md)
533. [accountMenuRow](modules/accountMenuRow.md)
534. [credentialRemount](modules/credentialRemount.md)
535. [identityContext](modules/identityContext.md)
536. [mutationFeedback](modules/mutationFeedback.md)
537. [overviewTaskThread](modules/overviewTaskThread.md)
538. [planningMasters_masters](modules/planningMasters_masters.md)
539. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
540. [planningReturn](modules/planningReturn.md)
541. [planCheckpoints](modules/planCheckpoints.md)
542. [planCheckpoints.test](modules/planCheckpoints.test.md)
543. [planningTaskIssues](modules/planningTaskIssues.md)
544. [atRiskReasons](modules/atRiskReasons.md)
545. [AtRiskTaskReasons](modules/AtRiskTaskReasons.md)
546. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
547. [scheduleEvidence](modules/scheduleEvidence.md)
548. [useIterationPanels](modules/useIterationPanels.md)
549. [scopeStore](modules/scopeStore.md)
550. [taskTransitions](modules/taskTransitions.md)
551. [TaskRow](modules/TaskRow.md)
552. [taskTransitions.test](modules/taskTransitions.test.md)
553. [useLiveWindow](modules/useLiveWindow.md)
554. [workQueryFreshness](modules/workQueryFreshness.md)
555. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
556. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
557. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
558. [emptyStates](modules/emptyStates.md)
559. [emptyStates.test](modules/emptyStates.test.md)
560. [firstRun](modules/firstRun.md)
561. [landing.en](modules/landing.en.md)
562. [landing.ru](modules/landing.ru.md)
563. [literals.ru](modules/literals.ru.md)
564. [pagination](modules/pagination.md)
565. [plan.ru](modules/plan.ru.md)
566. [planSchedule](modules/planSchedule.md)
567. [planWork](modules/planWork.md)
568. [planningInputMessages](modules/planningInputMessages.md)
569. [surfaces.ru](modules/surfaces.ru.md)
570. [teamwork.en](modules/teamwork.en.md)
571. [teamwork.ru](modules/teamwork.ru.md)
572. [timeEntries](modules/timeEntries.md)
573. [resources.en](modules/resources.en.md)
574. [agentDispatch.test](modules/agentDispatch.test.md)
575. [englishNames.test](modules/englishNames.test.md)
576. [i18n](modules/i18n.md)
577. [settingsFieldLabels.test](modules/settingsFieldLabels.test.md)
578. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
579. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
580. [triageUtils](modules/triageUtils.md)
581. [StatusPill](modules/StatusPill.md)
582. [TriageToolbar](modules/TriageToolbar.md)
583. [dateLocale](modules/dateLocale.md)
584. [InteractiveCalendar](modules/InteractiveCalendar.md)
585. [formatsAndWording.test](modules/formatsAndWording.test.md)
586. [planWork.test](modules/planWork.test.md)
587. [resources.ru](modules/resources.ru.md)
588. [i18n.test](modules/i18n.test.md)
589. [russianNames.test](modules/russianNames.test.md)
590. [schedulingDisplay](modules/schedulingDisplay.md)
591. [seedDisplay](modules/seedDisplay.md)
592. [SavedViewsControl](modules/SavedViewsControl.md)
593. [seedDisplay.test](modules/seedDisplay.test.md)
594. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
595. [destinations](modules/destinations.md)
596. [legacyPaths](modules/legacyPaths.md)
597. [LegacyRedirect](modules/LegacyRedirect.md)
598. [CalendarRedirect.test](modules/CalendarRedirect.test.md)
599. [LegacyRedirect.test](modules/LegacyRedirect.test.md)
600. [legacyPaths.check.test](modules/legacyPaths.check.test.md)
601. [routeModules](modules/routeModules.md)
602. [DocumentMetadata](modules/DocumentMetadata.md)
603. [destinations.test](modules/destinations.test.md)
604. [helpContexts](modules/helpContexts.md)
605. [helpContexts.test](modules/helpContexts.test.md)
606. [scopeParams](modules/scopeParams.md)
607. [namedIteration](modules/namedIteration.md)
608. [namedIteration.test](modules/namedIteration.test.md)
609. [workScope](modules/workScope.md)
610. [useScopeLink](modules/useScopeLink.md)
611. [Breadcrumbs](modules/Breadcrumbs.md)
612. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
613. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
614. [PlanReturnBar](modules/PlanReturnBar.md)
615. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
616. [PlanningWorkflowHelpContent](modules/PlanningWorkflowHelpContent.md)
617. [TaskWorkflowHelpContent](modules/TaskWorkflowHelpContent.md)
618. [SetupReturnBar](modules/SetupReturnBar.md)
619. [useScopeLink.test](modules/useScopeLink.test.md)
620. [workScope.test](modules/workScope.test.md)
621. [scopeParams.check.test](modules/scopeParams.check.test.md)
622. [workspaces](modules/workspaces.md)
623. [workspaces.test](modules/workspaces.test.md)
624. [LandingPage](modules/LandingPage.md)
625. [NotFoundPage](modules/NotFoundPage.md)
626. [healthService](modules/healthService.md)
627. [SystemHealthPanel](modules/SystemHealthPanel.md)
628. [iterationStore](modules/iterationStore.md)
629. [iterationStore.test](modules/iterationStore.test.md)
630. [themeStore](modules/themeStore.md)
631. [BareLayout](modules/BareLayout.md)
632. [colorRoles.test](modules/colorRoles.test.md)
633. [planning-masters.test](modules/planning-masters.test.md)
634. [accessibilityInvariants](modules/accessibilityInvariants.md)
635. [modelAwareRouting](modules/modelAwareRouting.md)
636. [taskDetail](modules/taskDetail.md)
637. [lintRules.test](modules/lintRules.test.md)
638. [pageChrome](modules/pageChrome.md)
639. [renderWithProviders](modules/renderWithProviders.md)
640. [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md)
641. [UnscheduledTasks.test](modules/UnscheduledTasks.test.md)
642. [BareLayout.test](modules/BareLayout.test.md)
643. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
644. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
645. [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md)
646. [TaskRow.test](modules/TaskRow.test.md)
647. [FilterBar.test](modules/FilterBar.test.md)
648. [OverflowMenu.test](modules/OverflowMenu.test.md)
649. [PageLayout.test](modules/PageLayout.test.md)
650. [ViewSwitch.test](modules/ViewSwitch.test.md)
651. [LandingPage.test](modules/LandingPage.test.md)
652. [renderWithProviders.test](modules/renderWithProviders.test.md)
653. [routeRegistry](modules/routeRegistry.md)
654. [setup](modules/setup.md)
655. [types_agent](modules/types_agent.md)
656. [analyticsScope](modules/analyticsScope.md)
657. [types_calendar](modules/types_calendar.md)
658. [deliveryMetrics](modules/deliveryMetrics.md)
659. [emailSettings](modules/emailSettings.md)
660. [executionUsage](modules/executionUsage.md)
661. [types_gantt](modules/types_gantt.md)
662. [types_github](modules/types_github.md)
663. [types_iteration](modules/types_iteration.md)
664. [types_label](modules/types_label.md)
665. [outboundWebhook](modules/outboundWebhook.md)
666. [types_project](modules/types_project.md)
667. [types_release](modules/types_release.md)
668. [requestSource](modules/requestSource.md)
669. [savedView](modules/savedView.md)
670. [schedulingRules](modules/schedulingRules.md)
671. [EffortModifierCard](modules/EffortModifierCard.md)
672. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
673. [SchedulingPassCard](modules/SchedulingPassCard.md)
674. [schedulingSearchLabels.test](modules/schedulingSearchLabels.test.md)
675. [systemSettings](modules/systemSettings.md)
676. [types_task](modules/types_task.md)
677. [types_team](modules/types_team.md)
678. [types_template](modules/types_template.md)
679. [types_triage](modules/types_triage.md)
680. [workMetrics](modules/workMetrics.md)
681. [agentAccess](modules/agentAccess.md)
682. [useAgentAccess](modules/useAgentAccess.md)
683. [apiError](modules/apiError.md)
684. [QueryState](modules/QueryState.md)
685. [taskEditorContract](modules/taskEditorContract.md)
686. [TaskBriefEditor](modules/TaskBriefEditor.md)
687. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
688. [TriageDraftPreview](modules/TriageDraftPreview.md)
689. [MutationSuccessFeedback](modules/MutationSuccessFeedback.md)
690. [mutationFeedback.test](modules/mutationFeedback.test.md)
691. [adminAccess](modules/adminAccess.md)
692. [OperatorIdentityNotice](modules/OperatorIdentityNotice.md)
693. [useAdminAccess](modules/useAdminAccess.md)
694. [api](modules/api.md)
695. [identityService](modules/identityService.md)
696. [NativeConnectionPage](modules/NativeConnectionPage.md)
697. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
698. [adminAccessService](modules/adminAccessService.md)
699. [AdminAccessPanel](modules/AdminAccessPanel.md)
700. [AdminAccessGate](modules/AdminAccessGate.md)
701. [AdminAccessGate.test](modules/AdminAccessGate.test.md)
702. [agentService](modules/agentService.md)
703. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
704. [useWaitingAgents](modules/useWaitingAgents.md)
705. [agentService.test](modules/agentService.test.md)
706. [deliveryMetricsService](modules/deliveryMetricsService.md)
707. [discussionService](modules/discussionService.md)
708. [emailSettingsService](modules/emailSettingsService.md)
709. [executionUsageService](modules/executionUsageService.md)
710. [ganttService](modules/ganttService.md)
711. [githubService](modules/githubService.md)
712. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
713. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
714. [labelService](modules/labelService.md)
715. [LabelSelector](modules/LabelSelector.md)
716. [outboundWebhookService](modules/outboundWebhookService.md)
717. [planShareService](modules/planShareService.md)
718. [planningInputService](modules/planningInputService.md)
719. [usePlanningObservation](modules/usePlanningObservation.md)
720. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
721. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
722. [calendarService](modules/calendarService.md)
723. [WorkCalendarSettings](modules/WorkCalendarSettings.md)
724. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
725. [WorkCalendarSettings.test](modules/WorkCalendarSettings.test.md)
726. [PersonCapacity](modules/PersonCapacity.md)
727. [PersonCapacity.test](modules/PersonCapacity.test.md)
728. [exportService](modules/exportService.md)
729. [IterationImportDialog](modules/IterationImportDialog.md)
730. [iterationService](modules/iterationService.md)
731. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
732. [planProgress.test](modules/planProgress.test.md)
733. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
734. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
735. [useWorkScope](modules/useWorkScope.md)
736. [useAnalyticsScope](modules/useAnalyticsScope.md)
737. [useWorkScope.test](modules/useWorkScope.test.md)
738. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
739. [IdentityProvider](modules/IdentityProvider.md)
740. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
741. [useLiveWindow.test](modules/useLiveWindow.test.md)
742. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
743. [planningInputService.test](modules/planningInputService.test.md)
744. [projectService](modules/projectService.md)
745. [AddMilestoneModal](modules/AddMilestoneModal.md)
746. [SetDatesPopover](modules/SetDatesPopover.md)
747. [CreateProjectModal](modules/CreateProjectModal.md)
748. [FirstRunLanding](modules/FirstRunLanding.md)
749. [useFirstRunProgress](modules/useFirstRunProgress.md)
750. [useGetStarted](modules/useGetStarted.md)
751. [useNextSetupAction](modules/useNextSetupAction.md)
752. [NextStepEmptyState](modules/NextStepEmptyState.md)
753. [NextStepEmptyState.test](modules/NextStepEmptyState.test.md)
754. [releaseService](modules/releaseService.md)
755. [ReleaseForm](modules/ReleaseForm.md)
756. [requestSourceService](modules/requestSourceService.md)
757. [savedViewService](modules/savedViewService.md)
758. [schedulingRulesService](modules/schedulingRulesService.md)
759. [sessionService](modules/sessionService.md)
760. [snapshotService](modules/snapshotService.md)
761. [snapshotVersions.test](modules/snapshotVersions.test.md)
762. [systemSettingsService](modules/systemSettingsService.md)
763. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
764. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
765. [taskService](modules/taskService.md)
766. [DeliveryDependencies](modules/DeliveryDependencies.md)
767. [ImportTasksModal](modules/ImportTasksModal.md)
768. [MetricCount](modules/MetricCount.md)
769. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
770. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
771. [TaskContextSummary](modules/TaskContextSummary.md)
772. [TaskDependencySelector](modules/TaskDependencySelector.md)
773. [TaskMergeDialog](modules/TaskMergeDialog.md)
774. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
775. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
776. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
777. [useAgentRowFacts](modules/useAgentRowFacts.md)
778. [useTaskReviewer](modules/useTaskReviewer.md)
779. [TaskReviewer](modules/TaskReviewer.md)
780. [TaskWorkPanel](modules/TaskWorkPanel.md)
781. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
782. [TriageActionModal](modules/TriageActionModal.md)
783. [overviewBacklog](modules/overviewBacklog.md)
784. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
785. [teamService](modules/teamService.md)
786. [TeamForm](modules/TeamForm.md)
787. [TeamForm.test](modules/TeamForm.test.md)
788. [capacityMutations](modules/capacityMutations.md)
789. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
790. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
791. [GanttBarInputs](modules/GanttBarInputs.md)
792. [AssigneePicker](modules/AssigneePicker.md)
793. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
794. [TaskBulkOperationsPanel.test](modules/TaskBulkOperationsPanel.test.md)
795. [TaskSelectionBar](modules/TaskSelectionBar.md)
796. [useTaskRowEdits](modules/useTaskRowEdits.md)
797. [useIterationRowData](modules/useIterationRowData.md)
798. [useTaskAssigneeDisplay](modules/useTaskAssigneeDisplay.md)
799. [TaskAssigneeDisplay](modules/TaskAssigneeDisplay.md)
800. [KanbanCard](modules/KanbanCard.md)
801. [KanbanColumn](modules/KanbanColumn.md)
802. [KanbanColumn.test](modules/KanbanColumn.test.md)
803. [ImportTeamModal](modules/ImportTeamModal.md)
804. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
805. [VacationCsvImport](modules/VacationCsvImport.md)
806. [sampleProject](modules/sampleProject.md)
807. [SampleProjectAction](modules/SampleProjectAction.md)
808. [LocalProfilePicker](modules/LocalProfilePicker.md)
809. [GetStartedPanel](modules/GetStartedPanel.md)
810. [AccountMenu](modules/AccountMenu.md)
811. [UserSessionBadge](modules/UserSessionBadge.md)
812. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
813. [IdentityProvider.test](modules/IdentityProvider.test.md)
814. [usePlanScheduleWorkloads](modules/usePlanScheduleWorkloads.md)
815. [templateService](modules/templateService.md)
816. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
817. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
818. [timeEntryService](modules/timeEntryService.md)
819. [useTimeEntries](modules/useTimeEntries.md)
820. [timeEntryService.test](modules/timeEntryService.test.md)
821. [triageService](modules/triageService.md)
822. [AppSidebar](modules/AppSidebar.md)
823. [AppSidebar.planProgress.test](modules/AppSidebar.planProgress.test.md)
824. [AppSidebar.test](modules/AppSidebar.test.md)
825. [QuickCapture](modules/QuickCapture.md)
826. [QuickCapture.test](modules/QuickCapture.test.md)
827. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
828. [usePlanningReadiness](modules/usePlanningReadiness.md)
829. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
830. [planningScope.test](modules/planningScope.test.md)
831. [workspaceApi](modules/workspaceApi.md)
832. [pageChrome.test](modules/pageChrome.test.md)
833. [copyText](modules/copyText.md)
834. [focusLifecycle](modules/focusLifecycle.md)
835. [focusLifecycle.test](modules/focusLifecycle.test.md)
836. [formatDate](modules/formatDate.md)
837. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
838. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
839. [VacationManager](modules/VacationManager.md)
840. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
841. [IterationForm](modules/IterationForm.md)
842. [IterationEditorDrawer](modules/IterationEditorDrawer.md)
843. [IterationForm.test](modules/IterationForm.test.md)
844. [ScopeBar](modules/ScopeBar.md)
845. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
846. [ScopeBar.test](modules/ScopeBar.test.md)
847. [NotificationsPanel](modules/NotificationsPanel.md)
848. [PlanIterationCheckpoint](modules/PlanIterationCheckpoint.md)
849. [PlanShareSection](modules/PlanShareSection.md)
850. [PlanReviewSection](modules/PlanReviewSection.md)
851. [PlanShareSection.test](modules/PlanShareSection.test.md)
852. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
853. [ConnectedReadersPanel](modules/ConnectedReadersPanel.md)
854. [ConnectedReadersPanel.test](modules/ConnectedReadersPanel.test.md)
855. [StatusChangeControl](modules/StatusChangeControl.md)
856. [TaskDiscussion](modules/TaskDiscussion.md)
857. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
858. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
859. [TimeEntriesReport](modules/TimeEntriesReport.md)
860. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
861. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
862. [AgentManifestWorkflow](modules/AgentManifestWorkflow.md)
863. [AgentManifestWorkflow.test](modules/AgentManifestWorkflow.test.md)
864. [ModelCatalog](modules/ModelCatalog.md)
865. [TeamProfileManager](modules/TeamProfileManager.md)
866. [TeamDirectory](modules/TeamDirectory.md)
867. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
868. [TriageRow](modules/TriageRow.md)
869. [TriageList](modules/TriageList.md)
870. [TriageList.test](modules/TriageList.test.md)
871. [TriageSuggestions](modules/TriageSuggestions.md)
872. [planEvidence](modules/planEvidence.md)
873. [PlanSharePage](modules/PlanSharePage.md)
874. [PlanSharePage.test](modules/PlanSharePage.test.md)
875. [scopedPageRender.test](modules/scopedPageRender.test.md)
876. [graphLimitError](modules/graphLimitError.md)
877. [modelRouting](modules/modelRouting.md)
878. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
879. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
880. [ConnectAgentSteps](modules/ConnectAgentSteps.md)
881. [ConnectAgentSteps.test](modules/ConnectAgentSteps.test.md)
882. [modelRouting.test](modules/modelRouting.test.md)
883. [protectedQueries](modules/protectedQueries.md)
884. [AssignedAgentsSummary](modules/AssignedAgentsSummary.md)
885. [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md)
886. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
887. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
888. [AgentAccessPanel](modules/AgentAccessPanel.md)
889. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
890. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
891. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
892. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
893. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
894. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
895. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
896. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
897. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
898. [PipelineTaskEvidence](modules/PipelineTaskEvidence.md)
899. [usePipeline](modules/usePipeline.md)
900. [AgentModelAdministration](modules/AgentModelAdministration.md)
901. [PipelineTaskEvidence.test](modules/PipelineTaskEvidence.test.md)
902. [TeamPage](modules/TeamPage.md)
903. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
904. [IdentityProvider.keepRoute.test](modules/IdentityProvider.keepRoute.test.md)
905. [TeamPage.test](modules/TeamPage.test.md)
906. [TeamPage.transport.test](modules/TeamPage.transport.test.md)
907. [safeUrl](modules/safeUrl.md)
908. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
909. [ProjectRequestsTab](modules/ProjectRequestsTab.md)
910. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
911. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
912. [TaskReadView](modules/TaskReadView.md)
913. [TaskReadView.brief.test](modules/TaskReadView.brief.test.md)
914. [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md)
915. [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md)
916. [TaskReadView.test](modules/TaskReadView.test.md)
917. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
918. [TriageDetailPanel](modules/TriageDetailPanel.md)
919. [TriageConvertSource](modules/TriageConvertSource.md)
920. [ConvertTriageDrawer](modules/ConvertTriageDrawer.md)
921. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
922. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
923. [CommandMenu](modules/CommandMenu.md)
924. [CommandMenu.test](modules/CommandMenu.test.md)
925. [ContextHelp](modules/ContextHelp.md)
926. [AppTopNav](modules/AppTopNav.md)
927. [AppShell](modules/AppShell.md)
928. [App](modules/App.md)
929. [App.legacyRoutes.test](modules/App.legacyRoutes.test.md)
930. [AppShell.test](modules/AppShell.test.md)
931. [AppTopNav.test](modules/AppTopNav.test.md)
932. [ContextHelp.test](modules/ContextHelp.test.md)
933. [shellViewport.test](modules/shellViewport.test.md)
934. [AccountMenu.test](modules/AccountMenu.test.md)
935. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
936. [src_main](modules/src_main.md)
937. [SettingsPage](modules/SettingsPage.md)
938. [SettingsPage.calendar.test](modules/SettingsPage.calendar.test.md)
939. [SettingsPage.labels.test](modules/SettingsPage.labels.test.md)
940. [SettingsPage.readOnlyPanels.test](modules/SettingsPage.readOnlyPanels.test.md)
941. [SettingsPage.test](modules/SettingsPage.test.md)
942. [SettingsPage.unlock.test](modules/SettingsPage.unlock.test.md)
943. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
944. [taskFilterDefaults](modules/taskFilterDefaults.md)
945. [TaskFiltersBar](modules/TaskFiltersBar.md)
946. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
947. [taskViewParams](modules/taskViewParams.md)
948. [taskViewParams.test](modules/taskViewParams.test.md)
949. [taskViewState](modules/taskViewState.md)
950. [savedViewState](modules/savedViewState.md)
951. [useSavedViewManager](modules/useSavedViewManager.md)
952. [savedViewState.test](modules/savedViewState.test.md)
953. [taskFilters](modules/taskFilters.md)
954. [taskFilters.test](modules/taskFilters.test.md)
955. [teamMemberLabels](modules/teamMemberLabels.md)
956. [InitiativeForm](modules/InitiativeForm.md)
957. [InitiativeGroupHeader](modules/InitiativeGroupHeader.md)
958. [RoadmapView](modules/RoadmapView.md)
959. [RoadmapView.test](modules/RoadmapView.test.md)
960. [sampleProject.test](modules/sampleProject.test.md)
961. [templateDefaults](modules/templateDefaults.md)
962. [ProjectForm](modules/ProjectForm.md)
963. [ProjectForm.test](modules/ProjectForm.test.md)
964. [TaskForm](modules/TaskForm.md)
965. [AssigneePicker.test](modules/AssigneePicker.test.md)
966. [GuardedTaskDrawer](modules/GuardedTaskDrawer.md)
967. [BacklogPanel](modules/BacklogPanel.md)
968. [CurrentTaskDrawer.test](modules/CurrentTaskDrawer.test.md)
969. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
970. [TaskEditDrawer](modules/TaskEditDrawer.md)
971. [GanttChart](modules/GanttChart.md)
972. [GanttChart.test](modules/GanttChart.test.md)
973. [TaskEditDrawer.test](modules/TaskEditDrawer.test.md)
974. [ProjectTaskTree](modules/ProjectTaskTree.md)
975. [ProjectTasksTab](modules/ProjectTasksTab.md)
976. [ProjectTaskTree.test](modules/ProjectTaskTree.test.md)
977. [TaskEditorDrawer.flow.test](modules/TaskEditorDrawer.flow.test.md)
978. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
979. [TaskForm.test](modules/TaskForm.test.md)
980. [TaskFormSections.test](modules/TaskFormSections.test.md)
981. [CreateTriageDrawer](modules/CreateTriageDrawer.md)
982. [GanttPage](modules/GanttPage.md)
983. [GanttPage.test](modules/GanttPage.test.md)
984. [MyWorkPage](modules/MyWorkPage.md)
985. [MyWorkPage.test](modules/MyWorkPage.test.md)
986. [TriagePage](modules/TriagePage.md)
987. [TriagePage.test](modules/TriagePage.test.md)
988. [ganttChrome.test](modules/ganttChrome.test.md)
989. [visibleWork](modules/visibleWork.md)
990. [KanbanBoard](modules/KanbanBoard.md)
991. [KanbanBoard.test](modules/KanbanBoard.test.md)
992. [TaskList](modules/TaskList.md)
993. [TaskList.test](modules/TaskList.test.md)
994. [overviewSignals](modules/overviewSignals.md)
995. [PipelineView](modules/PipelineView.md)
996. [assigneeDisplay.test](modules/assigneeDisplay.test.md)
997. [overviewSignals.test](modules/overviewSignals.test.md)
998. [TasksPage](modules/TasksPage.md)
999. [backlogScope.test](modules/backlogScope.test.md)
1000. [TasksPage.board.test](modules/TasksPage.board.test.md)
1001. [TasksPage.pipeline.test](modules/TasksPage.pipeline.test.md)
1002. [TasksPage.test](modules/TasksPage.test.md)
1003. [TasksPage.toolbar.test](modules/TasksPage.toolbar.test.md)
1004. [visibleWork.test](modules/visibleWork.test.md)
1005. [workNumbers](modules/workNumbers.md)
1006. [OnTrackSummary](modules/OnTrackSummary.md)
1007. [StatusDistribution](modules/StatusDistribution.md)
1008. [IterationOutlook.test](modules/IterationOutlook.test.md)
1009. [CapacityTable](modules/CapacityTable.md)
1010. [TeamList](modules/TeamList.md)
1011. [CapacitySection](modules/CapacitySection.md)
1012. [CapacitySection.test](modules/CapacitySection.test.md)
1013. [IterationCapacityLine](modules/IterationCapacityLine.md)
1014. [TeamList.test](modules/TeamList.test.md)
1015. [IterationList](modules/IterationList.md)
1016. [AllIterationsDrawer](modules/AllIterationsDrawer.md)
1017. [AllIterationsDrawer.test](modules/AllIterationsDrawer.test.md)
1018. [PlanBlockersSection](modules/PlanBlockersSection.md)
1019. [PlanIterationDrawers](modules/PlanIterationDrawers.md)
1020. [PlanScheduleSection](modules/PlanScheduleSection.md)
1021. [PlanWorkSection](modules/PlanWorkSection.md)
1022. [projectDetailShared](modules/projectDetailShared.md)
1023. [MilestoneFormDrawer](modules/MilestoneFormDrawer.md)
1024. [MilestonesSection](modules/MilestonesSection.md)
1025. [PostUpdateDrawer](modules/PostUpdateDrawer.md)
1026. [ProjectHeaderFields](modules/ProjectHeaderFields.md)
1027. [ProjectReleasesTab](modules/ProjectReleasesTab.md)
1028. [ProjectSummaryTab](modules/ProjectSummaryTab.md)
1029. [ProjectUpdatesTab](modules/ProjectUpdatesTab.md)
1030. [WorkMetricsLine](modules/WorkMetricsLine.md)
1031. [MetricCount.test](modules/MetricCount.test.md)
1032. [planningLinks.test](modules/planningLinks.test.md)
1033. [AnalyticsPage](modules/AnalyticsPage.md)
1034. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
1035. [scopedPages.test](modules/scopedPages.test.md)
1036. [AnalyticsPage.test](modules/AnalyticsPage.test.md)
1037. [OverviewPage](modules/OverviewPage.md)
1038. [GetStartedPanel.test](modules/GetStartedPanel.test.md)
1039. [OverviewPage.test](modules/OverviewPage.test.md)
1040. [PlanPage](modules/PlanPage.md)
1041. [planProgressPlacement.test](modules/planProgressPlacement.test.md)
1042. [GetStartedFlow.test](modules/GetStartedFlow.test.md)
1043. [PlanIterations.test](modules/PlanIterations.test.md)
1044. [PlanPage.test](modules/PlanPage.test.md)
1045. [ProjectDetailPage](modules/ProjectDetailPage.md)
1046. [ProjectDetailPage.test](modules/ProjectDetailPage.test.md)
1047. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
1048. [ProjectReleaseDetailPage.test](modules/ProjectReleaseDetailPage.test.md)
1049. [ProjectsPage](modules/ProjectsPage.md)
1050. [ProjectsPage.test](modules/ProjectsPage.test.md)
1051. [destinationEmptyStates.test](modules/destinationEmptyStates.test.md)
1052. [tailwind.config](modules/tailwind.config.md)
1053. [check-tailwind-classes](modules/check-tailwind-classes.md)
1054. [vite.config](modules/vite.config.md)
1055. [vitest.config](modules/vitest.config.md)
1056. [create_agent_actor](modules/create_agent_actor.md)
1057. [generate_workchord_keys](modules/generate_workchord_keys.md)
1058. [setup_agent_team](modules/setup_agent_team.md)
1059. [build_agent_skills](modules/build_agent_skills.md)
1060. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
1061. [android_qualification](modules/android_qualification.md)
1062. [android_web_peer](modules/android_web_peer.md)
1063. [apt_runtime](modules/apt_runtime.md)
1064. [browser_performance](modules/browser_performance.md)
1065. [browser_planning_inputs](modules/browser_planning_inputs.md)
1066. [browser_worker](modules/browser_worker.md)
1067. [browser_managed_work](modules/browser_managed_work.md)
1068. [browser_write_readback](modules/browser_write_readback.md)
1069. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
1070. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
1071. [ci_runtime](modules/ci_runtime.md)
1072. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
1073. [postgres_runtime](modules/postgres_runtime.md)
1074. [run_android_checks](modules/run_android_checks.md)
1075. [run_disposable_checks](modules/run_disposable_checks.md)
1076. [serve_disposable_api](modules/serve_disposable_api.md)
1077. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
1078. [test_apt_runtime](modules/test_apt_runtime.md)
1079. [test_ci_runtime](modules/test_ci_runtime.md)
1080. [test_native_runtimes](modules/test_native_runtimes.md)
1081. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
1082. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
1083. [generate_client_contract](modules/generate_client_contract.md)
1084. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
1085. [load_common](modules/load_common.md)
1086. [collect](modules/collect.md)
1087. [result](modules/result.md)
1088. [compare](modules/compare.md)
1089. [finalize](modules/finalize.md)
1090. [qualify](modules/qualify.md)
1091. [resilience](modules/resilience.md)
1092. [run](modules/run.md)
1093. [seal](modules/seal.md)
1094. [seed](modules/seed.md)
1095. [source_binding](modules/source_binding.md)
1096. [local_baseline](modules/local_baseline.md)
1097. [service_worksets](modules/service_worksets.md)
1098. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
1099. [isolated_rehearsal](modules/isolated_rehearsal.md)

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
| [planning_window_reconciliation](modules/planning_window_reconciliation.md) | `_SNAPSHOT_CACHE = OrderedDict`, `_CACHE_LOCK = Lock` |
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
| [test_agent_team_setup](modules/test_agent_team_setup.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md) | `SPEC = importlib.util.spec_from_file_location`, `setup_agent_team = importlib.util.module_from_spec`, `SPEC.loader.exec_module` |
| [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md) | `FIXED_NOW = datetime` |
| [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_dependency_date_cascade](modules/test_dependency_date_cascade.md) | `PLANNED_START = date`, `LATER_START = date` |
| [test_execution_reconciliation](modules/test_execution_reconciliation.md) | `database_engines = pytest.mark.parametrize` |
| [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md) | `READ_NAME = re.compile` |
| [test_native_connections](modules/test_native_connections.md) | `CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b'=').decode` |
| [test_observer_sessions](modules/test_observer_sessions.md) | `CHALLENGE = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b'=').decode`, `OBSERVER_CAP = timedelta`, `PERSON_CAP = timedelta` |
| [test_plan_checkpoints](modules/test_plan_checkpoints.md) | `READY = dict` |
| [test_review_provenance](modules/test_review_provenance.md) | `database_engines = pytest.mark.parametrize` |
| [test_review_provenance_transports](modules/test_review_provenance_transports.md) | `databases = pytest.mark.parametrize` |
| [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md) | `TODAY = date`, `NOW = datetime.fromisoformat` |
| [test_team_topology_read](modules/test_team_topology_read.md) | `pytestmark = pytest.mark.usefixtures` |
| [single-page-toolbar](modules/single-page-toolbar.md) | `CALL = Symbol`, `DYNAMIC = Symbol`, `ALL = Symbol`, `WRAPPERS = Set`, `ELEMENT_FACTORIES = Set`, `MUTATING_METHODS = Set`, `PER_ITEM_METHODS = Set`, `exportCache = Map` |
| [check-bundle-budget](modules/check-bundle-budget.md) | `BUDGETS = freeze` |
| [check-query-feedback](modules/check-query-feedback.md) | `HOOK_KINDS = Map` |
| [check-tailwind-classes](modules/check-tailwind-classes.md) | `semanticRoots = Set`, `colorUtilityPrefixes = sort`, `colorUtilitySource = join`, `semanticRootSource = join`, `semanticClassPattern = RegExp`, `legacyClassPattern = RegExp`, `rawPaletteClassPattern = RegExp`, `darkVariantClassPattern = RegExp`, `arbitraryColorClassPattern = RegExp`, `translucentSemanticTextPattern = RegExp`, `semanticColorNames = Set` |
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
| [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md) | `afterEach`, `it` |
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
| [AssigneePicker.test](modules/AssigneePicker.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [CurrentTaskDrawer.test](modules/CurrentTaskDrawer.test.md) | `service = hoisted`, `mock`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it` |
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
| [TaskFormSections.test](modules/TaskFormSections.test.md) | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `teamMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `it`, `it`, `it`, `describe`, `describe`, `describe` |
| [TaskReadView.brief.test](modules/TaskReadView.brief.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `it.each(['en', 'ru'])` |
| [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
| [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [TaskReadView.test](modules/TaskReadView.test.md) | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `describe` |
| [TaskRow.test](modules/TaskRow.test.md) | `describe` |
| [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md) | `service = hoisted`, `iterations = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind`, `LOOPBACK_HOSTS = Set` |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | `service = hoisted`, `mock`, `mock`, `describe`, `it`, `describe`, `describe` |
| [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md) | `service = hoisted`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it`, `it.each([true, false])`, `it` |
| [assigneeDisplay.test](modules/assigneeDisplay.test.md) | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |
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
| [TasksPage.toolbar.test](modules/TasksPage.toolbar.test.md) | `workScopeMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `css = readFileSync`, `describe`, `describe` |
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
