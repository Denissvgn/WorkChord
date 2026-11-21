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
53. [query_limits](modules/query_limits.md)
54. [runtime_telemetry](modules/runtime_telemetry.md)
55. [database_runtime](modules/database_runtime.md)
56. [maintenance](modules/maintenance.md)
57. [mutation_versions](modules/mutation_versions.md)
58. [schemas_agent_connect](modules/schemas_agent_connect.md)
59. [schemas_agent_planning](modules/schemas_agent_planning.md)
60. [agent_skill_bundle](modules/agent_skill_bundle.md)
61. [agent_team_setup](modules/agent_team_setup.md)
62. [schemas_autonomy](modules/schemas_autonomy.md)
63. [schemas_common](modules/schemas_common.md)
64. [delivery_metrics](modules/delivery_metrics.md)
65. [schemas_execution_usage](modules/schemas_execution_usage.md)
66. [schemas_github](modules/schemas_github.md)
67. [schemas_intake](modules/schemas_intake.md)
68. [schemas_label](modules/schemas_label.md)
69. [schemas_plan_share](modules/schemas_plan_share.md)
70. [planning_inputs](modules/planning_inputs.md)
71. [schemas_calendar](modules/schemas_calendar.md)
72. [schemas_saved_view](modules/schemas_saved_view.md)
73. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
74. [schemas_session](modules/schemas_session.md)
75. [snapshot](modules/snapshot.md)
76. [schemas_system_settings](modules/schemas_system_settings.md)
77. [schemas_email_settings](modules/schemas_email_settings.md)
78. [schemas_task_brief](modules/schemas_task_brief.md)
79. [schemas_llm](modules/schemas_llm.md)
80. [schemas_task_domain](modules/schemas_task_domain.md)
81. [schemas_team](modules/schemas_team.md)
82. [schemas_template](modules/schemas_template.md)
83. [schemas_time_entry](modules/schemas_time_entry.md)
84. [time_report](modules/time_report.md)
85. [schemas_work_metrics](modules/schemas_work_metrics.md)
86. [schemas_iteration](modules/schemas_iteration.md)
87. [schemas_project](modules/schemas_project.md)
88. [schemas_release](modules/schemas_release.md)
89. [security](modules/security.md)
90. [server_features](modules/server_features.md)
91. [agent_routing_policy](modules/agent_routing_policy.md)
92. [agent_routing](modules/agent_routing.md)
93. [agent_routing_rollout](modules/agent_routing_rollout.md)
94. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
95. [routers_agent_connect](modules/routers_agent_connect.md)
96. [agent_team_credentials](modules/agent_team_credentials.md)
97. [bounded_scope_reads](modules/bounded_scope_reads.md)
98. [language_service](modules/language_service.md)
99. [plan_checkpoints](modules/plan_checkpoints.md)
100. [planning_input_context](modules/planning_input_context.md)
101. [planning_issues](modules/planning_issues.md)
102. [scheduling_rules_service](modules/scheduling_rules_service.md)
103. [upgrade_service](modules/upgrade_service.md)
104. [upgrade](modules/upgrade.md)
105. [settings_read](modules/settings_read.md)
106. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
107. [sql_semantics](modules/sql_semantics.md)
108. [exceptions](modules/exceptions.md)
109. [github_links](modules/github_links.md)
110. [text_similarity](modules/text_similarity.md)
111. [time](modules/time.md)
112. [observability](modules/observability.md)
113. [app_database](modules/app_database.md)
114. [models_autonomy](modules/models_autonomy.md)
115. [models_calendar](modules/models_calendar.md)
116. [models_capacity](modules/models_capacity.md)
117. [models_database_migration](modules/models_database_migration.md)
118. [delivery_dependency](modules/delivery_dependency.md)
119. [models_discussion](modules/models_discussion.md)
120. [models_execution_usage](modules/models_execution_usage.md)
121. [models_external_link](modules/models_external_link.md)
122. [models_github](modules/models_github.md)
123. [models_identity](modules/models_identity.md)
124. [models_iteration](modules/models_iteration.md)
125. [models_label](modules/models_label.md)
126. [native_connection](modules/native_connection.md)
127. [models_outbound_webhook](modules/models_outbound_webhook.md)
128. [models_plan_share](modules/models_plan_share.md)
129. [models_release](modules/models_release.md)
130. [models_project](modules/models_project.md)
131. [models_request_source](modules/models_request_source.md)
132. [models_runtime_observation](modules/models_runtime_observation.md)
133. [models_saved_view](modules/models_saved_view.md)
134. [models_system_settings](modules/models_system_settings.md)
135. [models_task](modules/models_task.md)
136. [recovery](modules/recovery.md)
137. [models_task_brief](modules/models_task_brief.md)
138. [task_status_log](modules/task_status_log.md)
139. [team_member](modules/team_member.md)
140. [models_agent](modules/models_agent.md)
141. [delivery_observation](modules/delivery_observation.md)
142. [models_template](modules/models_template.md)
143. [models_time_entry](modules/models_time_entry.md)
144. [models_triage](modules/models_triage.md)
145. [user_session](modules/user_session.md)
146. [models___init__](modules/models___init__.md)
147. [catalog](modules/catalog.md)
148. [database_migration_canonical](modules/database_migration_canonical.md)
149. [source](modules/source.md)
150. [transfer](modules/transfer.md)
151. [cli_database_migration](modules/cli_database_migration.md)
152. [database_migration___init__](modules/database_migration___init__.md)
153. [migrations_env](modules/migrations_env.md)
154. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
155. [calendar_service](modules/calendar_service.md)
156. [calendars](modules/calendars.md)
157. [capacity_service](modules/capacity_service.md)
158. [routers_capacity](modules/routers_capacity.md)
159. [delivery_dependency_service](modules/delivery_dependency_service.md)
160. [delivery_metrics_service](modules/delivery_metrics_service.md)
161. [discussion_service](modules/discussion_service.md)
162. [identity_service](modules/identity_service.md)
163. [import_planning_service](modules/import_planning_service.md)
164. [iteration_service](modules/iteration_service.md)
165. [iterations](modules/iterations.md)
166. [label_service](modules/label_service.md)
167. [labels](modules/labels.md)
168. [native_session_service](modules/native_session_service.md)
169. [saved_view_service](modules/saved_view_service.md)
170. [session_service](modules/session_service.md)
171. [http_authority](modules/http_authority.md)
172. [routers_identity](modules/routers_identity.md)
173. [saved_views](modules/saved_views.md)
174. [routers_session](modules/routers_session.md)
175. [task_brief_service](modules/task_brief_service.md)
176. [task_context_revision_service](modules/task_context_revision_service.md)
177. [task_domain_service](modules/task_domain_service.md)
178. [task_hierarchy_service](modules/task_hierarchy_service.md)
179. [task_recovery_service](modules/task_recovery_service.md)
180. [task_timeline_service](modules/task_timeline_service.md)
181. [team_service](modules/team_service.md)
182. [routers_team](modules/routers_team.md)
183. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
184. [snapshot_service](modules/snapshot_service.md)
185. [plan_share_service](modules/plan_share_service.md)
186. [plan_shares](modules/plan_shares.md)
187. [template_service](modules/template_service.md)
188. [templates](modules/templates.md)
189. [time_entry_service](modules/time_entry_service.md)
190. [time_report_service](modules/time_report_service.md)
191. [services_work_metrics](modules/services_work_metrics.md)
192. [import_parser](modules/import_parser.md)
193. [url_policy](modules/url_policy.md)
194. [schemas_external_link](modules/schemas_external_link.md)
195. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
196. [schemas_request_source](modules/schemas_request_source.md)
197. [schemas_task](modules/schemas_task.md)
198. [schemas_gantt](modules/schemas_gantt.md)
199. [task_detail](modules/task_detail.md)
200. [schemas_triage](modules/schemas_triage.md)
201. [schemas___init__](modules/schemas___init__.md)
202. [schemas_agent](modules/schemas_agent.md)
203. [agent_run_read](modules/agent_run_read.md)
204. [schemas_runtime_observation](modules/schemas_runtime_observation.md)
205. [agent_readiness](modules/agent_readiness.md)
206. [llm_service](modules/llm_service.md)
207. [review_provenance](modules/review_provenance.md)
208. [runtime_observation_service](modules/runtime_observation_service.md)
209. [system_settings_service](modules/system_settings_service.md)
210. [routers_system_settings](modules/routers_system_settings.md)
211. [email_settings_service](modules/email_settings_service.md)
212. [routers_email_settings](modules/routers_email_settings.md)
213. [notification_service](modules/notification_service.md)
214. [outbound_webhook_service](modules/outbound_webhook_service.md)
215. [worker](modules/worker.md)
216. [outbound_webhooks](modules/outbound_webhooks.md)
217. [external_link_service](modules/external_link_service.md)
218. [github_status_service](modules/github_status_service.md)
219. [request_source_service](modules/request_source_service.md)
220. [request_sources](modules/request_sources.md)
221. [project_service](modules/project_service.md)
222. [task_detail_service](modules/task_detail_service.md)
223. [task_import_service](modules/task_import_service.md)
224. [task_service](modules/task_service.md)
225. [export](modules/export.md)
226. [snapshots](modules/snapshots.md)
227. [agent_routing_observability](modules/agent_routing_observability.md)
228. [agent_service](modules/agent_service.md)
229. [agent_skill_bundles](modules/agent_skill_bundles.md)
230. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
231. [agent_routing_service](modules/agent_routing_service.md)
232. [agent_team_setup_service](modules/agent_team_setup_service.md)
233. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
234. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
235. [execution_reconciliation](modules/execution_reconciliation.md)
236. [execution_usage_service](modules/execution_usage_service.md)
237. [routers_task_domain](modules/routers_task_domain.md)
238. [delivery_dependencies](modules/delivery_dependencies.md)
239. [routers_discussion](modules/routers_discussion.md)
240. [time_entries](modules/time_entries.md)
241. [agent_run_read_service](modules/agent_run_read_service.md)
242. [github_status_automation_service](modules/github_status_automation_service.md)
243. [release_service](modules/release_service.md)
244. [projects](modules/projects.md)
245. [scheduler_service](modules/scheduler_service.md)
246. [routers_gantt](modules/routers_gantt.md)
247. [routers_llm](modules/routers_llm.md)
248. [agent_planning_service](modules/agent_planning_service.md)
249. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
250. [tasks](modules/tasks.md)
251. [task_status_service](modules/task_status_service.md)
252. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
253. [triage_service](modules/triage_service.md)
254. [routers_triage](modules/routers_triage.md)
255. [agent_work_service](modules/agent_work_service.md)
256. [mcp_agent_tools](modules/mcp_agent_tools.md)
257. [mcp_server](modules/mcp_server.md)
258. [routers_agent](modules/routers_agent.md)
259. [routers_agent_planning](modules/routers_agent_planning.md)
260. [agent_catalog](modules/agent_catalog.md)
261. [github_webhook_service](modules/github_webhook_service.md)
262. [routers_github](modules/routers_github.md)
263. [web_intake_service](modules/web_intake_service.md)
264. [routers_intake](modules/routers_intake.md)
265. [app_main](modules/app_main.md)
266. [routers___init__](modules/routers___init__.md)
267. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
268. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
269. [test_server_acceptance](modules/test_server_acceptance.md)
270. [test_acceptance_artifacts](modules/test_acceptance_artifacts.md)
271. [test_work_package_service](modules/test_work_package_service.md)
272. [test_database_configuration](modules/test_database_configuration.md)
273. [test_deployment_topology](modules/test_deployment_topology.md)
274. [test_observability](modules/test_observability.md)
275. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
276. [test_query_boundaries](modules/test_query_boundaries.md)
277. [test_runtime_policy](modules/test_runtime_policy.md)
278. [test_schema_behavior](modules/test_schema_behavior.md)
279. [test_cutover_evidence](modules/test_cutover_evidence.md)
280. [test_documentation_boundary](modules/test_documentation_boundary.md)
281. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
282. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
283. [test_source_preflight](modules/test_source_preflight.md)
284. [test_transfer_catalog](modules/test_transfer_catalog.md)
285. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
286. [0001_wave0_probe](modules/0001_wave0_probe.md)
287. [test_allocation_identity](modules/test_allocation_identity.md)
288. [test_initial_schema](modules/test_initial_schema.md)
289. [test_profile_identity](modules/test_profile_identity.md)
290. [test_android_cleanup](modules/test_android_cleanup.md)
291. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
292. [test_load_tooling](modules/test_load_tooling.md)
293. [test_local_baseline](modules/test_local_baseline.md)
294. [test_routing_evidence](modules/test_routing_evidence.md)
295. [support_database](modules/support_database.md)
296. [delivery](modules/delivery.md)
297. [factories](modules/factories.md)
298. [faults](modules/faults.md)
299. [runtime_peer](modules/runtime_peer.md)
300. [schema](modules/schema.md)
301. [support___init__](modules/support___init__.md)
302. [conftest](modules/conftest.md)
303. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
304. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
305. [test_project_identity](modules/test_project_identity.md)
306. [test_project_identity_scope](modules/test_project_identity_scope.md)
307. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
308. [transactions](modules/transactions.md)
309. [test_agent_blocker_reason](modules/test_agent_blocker_reason.md)
310. [test_agent_key_delivery](modules/test_agent_key_delivery.md)
311. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
312. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
313. [test_agent_routing_data](modules/test_agent_routing_data.md)
314. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
315. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
316. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
317. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
318. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
319. [test_agent_routing_service](modules/test_agent_routing_service.md)
320. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
321. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
322. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
323. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
324. [test_agent_team_catalog](modules/test_agent_team_catalog.md)
325. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
326. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
327. [test_authority_migrations](modules/test_authority_migrations.md)
328. [test_capacity_contract](modules/test_capacity_contract.md)
329. [test_client_contract](modules/test_client_contract.md)
330. [test_database_harness](modules/test_database_harness.md)
331. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
332. [test_agent_runtime_recovery](modules/test_agent_runtime_recovery.md)
333. [test_agent_discovery_report](modules/test_agent_discovery_report.md)
334. [test_agent_team_setup](modules/test_agent_team_setup.md)
335. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
336. [test_agent_team_setup_stored_contract](modules/test_agent_team_setup_stored_contract.md)
337. [test_analytics_scopes](modules/test_analytics_scopes.md)
338. [test_delivery_dependencies](modules/test_delivery_dependencies.md)
339. [test_dependency_date_cascade](modules/test_dependency_date_cascade.md)
340. [test_deployment_configuration](modules/test_deployment_configuration.md)
341. [test_effective_deferral](modules/test_effective_deferral.md)
342. [test_execution_usage](modules/test_execution_usage.md)
343. [test_execution_working_dates](modules/test_execution_working_dates.md)
344. [test_harness_session_metadata](modules/test_harness_session_metadata.md)
345. [test_managed_authority](modules/test_managed_authority.md)
346. [test_allocation_recovery](modules/test_allocation_recovery.md)
347. [test_bounded_task_policy](modules/test_bounded_task_policy.md)
348. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
349. [test_mcp_tool_annotations](modules/test_mcp_tool_annotations.md)
350. [test_metric_matches](modules/test_metric_matches.md)
351. [test_mobile_contract](modules/test_mobile_contract.md)
352. [test_mutation_versions](modules/test_mutation_versions.md)
353. [test_native_connections](modules/test_native_connections.md)
354. [test_observer_sessions](modules/test_observer_sessions.md)
355. [test_agdash_link_provider](modules/test_agdash_link_provider.md)
356. [test_person_assignment_reads](modules/test_person_assignment_reads.md)
357. [test_person_run_reads](modules/test_person_run_reads.md)
358. [test_plan_checkpoints](modules/test_plan_checkpoints.md)
359. [test_plan_shares](modules/test_plan_shares.md)
360. [test_planning_input_context](modules/test_planning_input_context.md)
361. [test_planning_issues](modules/test_planning_issues.md)
362. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
363. [test_process_roles](modules/test_process_roles.md)
364. [test_profile_capacity](modules/test_profile_capacity.md)
365. [test_planning_read_models](modules/test_planning_read_models.md)
366. [test_profile_capacity_migrations](modules/test_profile_capacity_migrations.md)
367. [test_project_review_policy](modules/test_project_review_policy.md)
368. [test_project_working_timezone](modules/test_project_working_timezone.md)
369. [test_rehearsal_ownership](modules/test_rehearsal_ownership.md)
370. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
371. [test_runtime_mutation_policy](modules/test_runtime_mutation_policy.md)
372. [test_runtime_observations](modules/test_runtime_observations.md)
373. [test_saved_view_service](modules/test_saved_view_service.md)
374. [test_schedule_follows_actual_dates](modules/test_schedule_follows_actual_dates.md)
375. [test_scheduler_dependencies](modules/test_scheduler_dependencies.md)
376. [test_schedule_working_date](modules/test_schedule_working_date.md)
377. [test_server_features](modules/test_server_features.md)
378. [test_settings_read_access](modules/test_settings_read_access.md)
379. [test_shared_member_revisions](modules/test_shared_member_revisions.md)
380. [test_shared_profile_revisions](modules/test_shared_profile_revisions.md)
381. [test_strict_caller_matrix](modules/test_strict_caller_matrix.md)
382. [test_task_domain](modules/test_task_domain.md)
383. [test_acceptance_attribution](modules/test_acceptance_attribution.md)
384. [test_delivery_metrics](modules/test_delivery_metrics.md)
385. [test_human_work_queries](modules/test_human_work_queries.md)
386. [test_task_discussion](modules/test_task_discussion.md)
387. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
388. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
389. [test_task_pagination](modules/test_task_pagination.md)
390. [test_team_member_agent_connected](modules/test_team_member_agent_connected.md)
391. [test_task_assignee_kind](modules/test_task_assignee_kind.md)
392. [test_team_pm_dispatch](modules/test_team_pm_dispatch.md)
393. [test_review_provenance](modules/test_review_provenance.md)
394. [test_team_pm_recovery](modules/test_team_pm_recovery.md)
395. [test_execution_reconciliation](modules/test_execution_reconciliation.md)
396. [test_review_provenance_transports](modules/test_review_provenance_transports.md)
397. [test_manual_review_provenance](modules/test_manual_review_provenance.md)
398. [test_supervised_shadow_rework](modules/test_supervised_shadow_rework.md)
399. [test_team_topology_read](modules/test_team_topology_read.md)
400. [test_time_entries](modules/test_time_entries.md)
401. [test_time_reports](modules/test_time_reports.md)
402. [test_unscheduled_tasks](modules/test_unscheduled_tasks.md)
403. [test_verification_preview_history](modules/test_verification_preview_history.md)
404. [test_work_correctness](modules/test_work_correctness.md)
405. [test_work_delivery_links](modules/test_work_delivery_links.md)
406. [test_workflow_vocabulary](modules/test_workflow_vocabulary.md)
407. [single-page-toolbar](modules/single-page-toolbar.md)
408. [eslint.config](modules/eslint.config.md)
409. [postcss.config](modules/postcss.config.md)
410. [check-bundle-budget](modules/check-bundle-budget.md)
411. [check-query-feedback](modules/check-query-feedback.md)
412. [check-task-selection-layout](modules/check-task-selection-layout.md)
413. [find-unread-i18n-keys](modules/find-unread-i18n-keys.md)
414. [find-unused-exports](modules/find-unused-exports.md)
415. [Checkbox](modules/Checkbox.md)
416. [CollapsibleSection](modules/CollapsibleSection.md)
417. [DisabledReason](modules/DisabledReason.md)
418. [Input](modules/Input.md)
419. [Input.test](modules/Input.test.md)
420. [Select](modules/Select.md)
421. [Textarea](modules/Textarea.md)
422. [buttonStyles](modules/buttonStyles.md)
423. [Button](modules/Button.md)
424. [Button.test](modules/Button.test.md)
425. [ButtonLink](modules/ButtonLink.md)
426. [ButtonLink.test](modules/ButtonLink.test.md)
427. [dialogLayer](modules/dialogLayer.md)
428. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
429. [Modal](modules/Modal.md)
430. [ConfirmDialog](modules/ConfirmDialog.md)
431. [formControlLabels.test](modules/formControlLabels.test.md)
432. [iconButtonTooltips.test](modules/iconButtonTooltips.test.md)
433. [leaveGuardBypass](modules/leaveGuardBypass.md)
434. [UnsavedLeaveGuard](modules/UnsavedLeaveGuard.md)
435. [useConfirmDialog](modules/useConfirmDialog.md)
436. [LiveWindowStatus](modules/LiveWindowStatus.md)
437. [WorkFreshness](modules/WorkFreshness.md)
438. [toast](modules/toast.md)
439. [ToastProvider](modules/ToastProvider.md)
440. [ToastProvider.test](modules/ToastProvider.test.md)
441. [UnscheduledTasks](modules/UnscheduledTasks.md)
442. [LabelChip](modules/LabelChip.md)
443. [BrandMark](modules/BrandMark.md)
444. [ScopePicker](modules/ScopePicker.md)
445. [commandMenuEvents](modules/commandMenuEvents.md)
446. [setupGuideEvents](modules/setupGuideEvents.md)
447. [ProjectIterationsTab](modules/ProjectIterationsTab.md)
448. [projectPortfolio](modules/projectPortfolio.md)
449. [AccessKeysSummary](modules/AccessKeysSummary.md)
450. [AgentTeamManifestPreview](modules/AgentTeamManifestPreview.md)
451. [ConstraintsPanel](modules/ConstraintsPanel.md)
452. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
453. [SettingsUnsavedBar](modules/SettingsUnsavedBar.md)
454. [WithheldValuesNote](modules/WithheldValuesNote.md)
455. [protectedQueryKeys](modules/protectedQueryKeys.md)
456. [settingsFieldLabels](modules/settingsFieldLabels.md)
457. [sharedUnlock](modules/sharedUnlock.md)
458. [ReadOnlyFieldset](modules/ReadOnlyFieldset.md)
459. [AssigneeSelect](modules/AssigneeSelect.md)
460. [claimTime](modules/claimTime.md)
461. [SortableTaskItem](modules/SortableTaskItem.md)
462. [TaskCreateSections](modules/TaskCreateSections.md)
463. [TaskViewOptions](modules/TaskViewOptions.md)
464. [taskDraftStorage](modules/taskDraftStorage.md)
465. [taskDraftStorage.test](modules/taskDraftStorage.test.md)
466. [taskRowValues](modules/taskRowValues.md)
467. [taskSearchResults](modules/taskSearchResults.md)
468. [taskStateChip](modules/taskStateChip.md)
469. [useDraftDismissal](modules/useDraftDismissal.md)
470. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
471. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
472. [useTaskSelection](modules/useTaskSelection.md)
473. [ModelBindings](modules/ModelBindings.md)
474. [directoryModel](modules/directoryModel.md)
475. [directoryModel.test](modules/directoryModel.test.md)
476. [FilterBar](modules/FilterBar.md)
477. [InlineEmptyState](modules/InlineEmptyState.md)
478. [MasterProgress](modules/MasterProgress.md)
479. [MasterProgress.test](modules/MasterProgress.test.md)
480. [OverflowMenu](modules/OverflowMenu.md)
481. [PageLayout](modules/PageLayout.md)
482. [PageToolbar.layout.test](modules/PageToolbar.layout.test.md)
483. [PageToolbar](modules/PageToolbar.md)
484. [PageToolbar.test](modules/PageToolbar.test.md)
485. [SectionCard](modules/SectionCard.md)
486. [SegmentedControl](modules/SegmentedControl.md)
487. [Select.test](modules/Select.test.md)
488. [SlideOverDrawer](modules/SlideOverDrawer.md)
489. [StickyRail](modules/StickyRail.md)
490. [ViewSwitch](modules/ViewSwitch.md)
491. [index](modules/index.md)
492. [tone](modules/tone.md)
493. [projectStatusStyles](modules/projectStatusStyles.md)
494. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
495. [Pill](modules/Pill.md)
496. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
497. [tone.test](modules/tone.test.md)
498. [agentDispatch](modules/agentDispatch.md)
499. [taskRowParts](modules/taskRowParts.md)
500. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
501. [connectAgent](modules/connectAgent.md)
502. [ConnectionSteps](modules/ConnectionSteps.md)
503. [manifestLocations](modules/manifestLocations.md)
504. [manifestLocations.test](modules/manifestLocations.test.md)
505. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
506. [AgentTeamStepList](modules/AgentTeamStepList.md)
507. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
508. [statusScopes](modules/statusScopes.md)
509. [statusScopes.test](modules/statusScopes.test.md)
510. [firstRunSteps](modules/firstRunSteps.md)
511. [getStartedVisibility](modules/getStartedVisibility.md)
512. [sampleProject.fixture](modules/sampleProject.fixture.md)
513. [sampleProjectStore](modules/sampleProjectStore.md)
514. [setupReturn](modules/setupReturn.md)
515. [accountMenuRow](modules/accountMenuRow.md)
516. [credentialRemount](modules/credentialRemount.md)
517. [identityContext](modules/identityContext.md)
518. [mutationFeedback](modules/mutationFeedback.md)
519. [overviewTaskThread](modules/overviewTaskThread.md)
520. [planningMasters_masters](modules/planningMasters_masters.md)
521. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
522. [planningReturn](modules/planningReturn.md)
523. [planCheckpoints](modules/planCheckpoints.md)
524. [planCheckpoints.test](modules/planCheckpoints.test.md)
525. [planningTaskIssues](modules/planningTaskIssues.md)
526. [atRiskReasons](modules/atRiskReasons.md)
527. [AtRiskTaskReasons](modules/AtRiskTaskReasons.md)
528. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
529. [scheduleEvidence](modules/scheduleEvidence.md)
530. [useIterationPanels](modules/useIterationPanels.md)
531. [scopeStore](modules/scopeStore.md)
532. [taskTransitions](modules/taskTransitions.md)
533. [TaskRow](modules/TaskRow.md)
534. [taskTransitions.test](modules/taskTransitions.test.md)
535. [useLiveWindow](modules/useLiveWindow.md)
536. [workQueryFreshness](modules/workQueryFreshness.md)
537. [WorkRefreshStatus](modules/WorkRefreshStatus.md)
538. [workQueryFreshness.test](modules/workQueryFreshness.test.md)
539. [agentTeamSetup.ru](modules/agentTeamSetup.ru.md)
540. [emptyStates](modules/emptyStates.md)
541. [emptyStates.test](modules/emptyStates.test.md)
542. [firstRun](modules/firstRun.md)
543. [landing.en](modules/landing.en.md)
544. [landing.ru](modules/landing.ru.md)
545. [literals.ru](modules/literals.ru.md)
546. [pagination](modules/pagination.md)
547. [plan.ru](modules/plan.ru.md)
548. [planSchedule](modules/planSchedule.md)
549. [planWork](modules/planWork.md)
550. [planningInputMessages](modules/planningInputMessages.md)
551. [surfaces.ru](modules/surfaces.ru.md)
552. [teamwork.en](modules/teamwork.en.md)
553. [teamwork.ru](modules/teamwork.ru.md)
554. [timeEntries](modules/timeEntries.md)
555. [resources.en](modules/resources.en.md)
556. [agentDispatch.test](modules/agentDispatch.test.md)
557. [englishNames.test](modules/englishNames.test.md)
558. [i18n](modules/i18n.md)
559. [settingsFieldLabels.test](modules/settingsFieldLabels.test.md)
560. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
561. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
562. [triageUtils](modules/triageUtils.md)
563. [StatusPill](modules/StatusPill.md)
564. [TriageToolbar](modules/TriageToolbar.md)
565. [dateLocale](modules/dateLocale.md)
566. [InteractiveCalendar](modules/InteractiveCalendar.md)
567. [formatsAndWording.test](modules/formatsAndWording.test.md)
568. [planWork.test](modules/planWork.test.md)
569. [resources.ru](modules/resources.ru.md)
570. [i18n.test](modules/i18n.test.md)
571. [russianNames.test](modules/russianNames.test.md)
572. [schedulingDisplay](modules/schedulingDisplay.md)
573. [seedDisplay](modules/seedDisplay.md)
574. [SavedViewsControl](modules/SavedViewsControl.md)
575. [seedDisplay.test](modules/seedDisplay.test.md)
576. [workflowVocabulary.test](modules/workflowVocabulary.test.md)
577. [destinations](modules/destinations.md)
578. [legacyPaths](modules/legacyPaths.md)
579. [LegacyRedirect](modules/LegacyRedirect.md)
580. [CalendarRedirect.test](modules/CalendarRedirect.test.md)
581. [LegacyRedirect.test](modules/LegacyRedirect.test.md)
582. [legacyPaths.check.test](modules/legacyPaths.check.test.md)
583. [routeModules](modules/routeModules.md)
584. [DocumentMetadata](modules/DocumentMetadata.md)
585. [destinations.test](modules/destinations.test.md)
586. [helpContexts](modules/helpContexts.md)
587. [helpContexts.test](modules/helpContexts.test.md)
588. [scopeParams](modules/scopeParams.md)
589. [namedIteration](modules/namedIteration.md)
590. [namedIteration.test](modules/namedIteration.test.md)
591. [workScope](modules/workScope.md)
592. [useScopeLink](modules/useScopeLink.md)
593. [Breadcrumbs](modules/Breadcrumbs.md)
594. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
595. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
596. [PlanReturnBar](modules/PlanReturnBar.md)
597. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
598. [PlanningWorkflowHelpContent](modules/PlanningWorkflowHelpContent.md)
599. [TaskWorkflowHelpContent](modules/TaskWorkflowHelpContent.md)
600. [SetupReturnBar](modules/SetupReturnBar.md)
601. [useScopeLink.test](modules/useScopeLink.test.md)
602. [workScope.test](modules/workScope.test.md)
603. [scopeParams.check.test](modules/scopeParams.check.test.md)
604. [workspaces](modules/workspaces.md)
605. [workspaces.test](modules/workspaces.test.md)
606. [LandingPage](modules/LandingPage.md)
607. [NotFoundPage](modules/NotFoundPage.md)
608. [healthService](modules/healthService.md)
609. [SystemHealthPanel](modules/SystemHealthPanel.md)
610. [iterationStore](modules/iterationStore.md)
611. [iterationStore.test](modules/iterationStore.test.md)
612. [themeStore](modules/themeStore.md)
613. [BareLayout](modules/BareLayout.md)
614. [colorRoles.test](modules/colorRoles.test.md)
615. [planning-masters.test](modules/planning-masters.test.md)
616. [accessibilityInvariants](modules/accessibilityInvariants.md)
617. [modelAwareRouting](modules/modelAwareRouting.md)
618. [taskDetail](modules/taskDetail.md)
619. [lintRules.test](modules/lintRules.test.md)
620. [pageChrome](modules/pageChrome.md)
621. [renderWithProviders](modules/renderWithProviders.md)
622. [WorkRefreshStatus.test](modules/WorkRefreshStatus.test.md)
623. [UnscheduledTasks.test](modules/UnscheduledTasks.test.md)
624. [BareLayout.test](modules/BareLayout.test.md)
625. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
626. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
627. [SettingsAccessAndAbout.test](modules/SettingsAccessAndAbout.test.md)
628. [TaskRow.test](modules/TaskRow.test.md)
629. [FilterBar.test](modules/FilterBar.test.md)
630. [OverflowMenu.test](modules/OverflowMenu.test.md)
631. [PageLayout.test](modules/PageLayout.test.md)
632. [ViewSwitch.test](modules/ViewSwitch.test.md)
633. [LandingPage.test](modules/LandingPage.test.md)
634. [renderWithProviders.test](modules/renderWithProviders.test.md)
635. [routeRegistry](modules/routeRegistry.md)
636. [setup](modules/setup.md)
637. [types_agent](modules/types_agent.md)
638. [analyticsScope](modules/analyticsScope.md)
639. [types_calendar](modules/types_calendar.md)
640. [deliveryMetrics](modules/deliveryMetrics.md)
641. [emailSettings](modules/emailSettings.md)
642. [executionUsage](modules/executionUsage.md)
643. [types_gantt](modules/types_gantt.md)
644. [types_github](modules/types_github.md)
645. [types_iteration](modules/types_iteration.md)
646. [types_label](modules/types_label.md)
647. [outboundWebhook](modules/outboundWebhook.md)
648. [types_project](modules/types_project.md)
649. [types_release](modules/types_release.md)
650. [requestSource](modules/requestSource.md)
651. [savedView](modules/savedView.md)
652. [schedulingRules](modules/schedulingRules.md)
653. [EffortModifierCard](modules/EffortModifierCard.md)
654. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
655. [SchedulingPassCard](modules/SchedulingPassCard.md)
656. [schedulingSearchLabels.test](modules/schedulingSearchLabels.test.md)
657. [systemSettings](modules/systemSettings.md)
658. [types_task](modules/types_task.md)
659. [types_team](modules/types_team.md)
660. [types_template](modules/types_template.md)
661. [types_triage](modules/types_triage.md)
662. [workMetrics](modules/workMetrics.md)
663. [agentAccess](modules/agentAccess.md)
664. [useAgentAccess](modules/useAgentAccess.md)
665. [apiError](modules/apiError.md)
666. [QueryState](modules/QueryState.md)
667. [taskEditorContract](modules/taskEditorContract.md)
668. [TaskBriefEditor](modules/TaskBriefEditor.md)
669. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
670. [TriageDraftPreview](modules/TriageDraftPreview.md)
671. [MutationSuccessFeedback](modules/MutationSuccessFeedback.md)
672. [mutationFeedback.test](modules/mutationFeedback.test.md)
673. [adminAccess](modules/adminAccess.md)
674. [OperatorIdentityNotice](modules/OperatorIdentityNotice.md)
675. [useAdminAccess](modules/useAdminAccess.md)
676. [api](modules/api.md)
677. [identityService](modules/identityService.md)
678. [NativeConnectionPage](modules/NativeConnectionPage.md)
679. [NativeConnectionPage.test](modules/NativeConnectionPage.test.md)
680. [adminAccessService](modules/adminAccessService.md)
681. [AdminAccessPanel](modules/AdminAccessPanel.md)
682. [AdminAccessGate](modules/AdminAccessGate.md)
683. [AdminAccessGate.test](modules/AdminAccessGate.test.md)
684. [agentService](modules/agentService.md)
685. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
686. [useWaitingAgents](modules/useWaitingAgents.md)
687. [agentService.test](modules/agentService.test.md)
688. [deliveryMetricsService](modules/deliveryMetricsService.md)
689. [discussionService](modules/discussionService.md)
690. [emailSettingsService](modules/emailSettingsService.md)
691. [executionUsageService](modules/executionUsageService.md)
692. [ganttService](modules/ganttService.md)
693. [githubService](modules/githubService.md)
694. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
695. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
696. [labelService](modules/labelService.md)
697. [LabelSelector](modules/LabelSelector.md)
698. [outboundWebhookService](modules/outboundWebhookService.md)
699. [planShareService](modules/planShareService.md)
700. [planningInputService](modules/planningInputService.md)
701. [usePlanningObservation](modules/usePlanningObservation.md)
702. [PlanningInputBoundary](modules/PlanningInputBoundary.md)
703. [PlanningInputBoundary.test](modules/PlanningInputBoundary.test.md)
704. [calendarService](modules/calendarService.md)
705. [WorkCalendarSettings](modules/WorkCalendarSettings.md)
706. [InteractiveCalendar.test](modules/InteractiveCalendar.test.md)
707. [WorkCalendarSettings.test](modules/WorkCalendarSettings.test.md)
708. [PersonCapacity](modules/PersonCapacity.md)
709. [PersonCapacity.test](modules/PersonCapacity.test.md)
710. [exportService](modules/exportService.md)
711. [IterationImportDialog](modules/IterationImportDialog.md)
712. [iterationService](modules/iterationService.md)
713. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
714. [planProgress.test](modules/planProgress.test.md)
715. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
716. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
717. [useWorkScope](modules/useWorkScope.md)
718. [useAnalyticsScope](modules/useAnalyticsScope.md)
719. [useWorkScope.test](modules/useWorkScope.test.md)
720. [workspaceQueryPolicy](modules/workspaceQueryPolicy.md)
721. [IdentityProvider](modules/IdentityProvider.md)
722. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
723. [useLiveWindow.test](modules/useLiveWindow.test.md)
724. [workspaceQueryPolicy.test](modules/workspaceQueryPolicy.test.md)
725. [planningInputService.test](modules/planningInputService.test.md)
726. [projectService](modules/projectService.md)
727. [AddMilestoneModal](modules/AddMilestoneModal.md)
728. [SetDatesPopover](modules/SetDatesPopover.md)
729. [CreateProjectModal](modules/CreateProjectModal.md)
730. [FirstRunLanding](modules/FirstRunLanding.md)
731. [useFirstRunProgress](modules/useFirstRunProgress.md)
732. [useGetStarted](modules/useGetStarted.md)
733. [useNextSetupAction](modules/useNextSetupAction.md)
734. [NextStepEmptyState](modules/NextStepEmptyState.md)
735. [NextStepEmptyState.test](modules/NextStepEmptyState.test.md)
736. [releaseService](modules/releaseService.md)
737. [ReleaseForm](modules/ReleaseForm.md)
738. [requestSourceService](modules/requestSourceService.md)
739. [savedViewService](modules/savedViewService.md)
740. [schedulingRulesService](modules/schedulingRulesService.md)
741. [sessionService](modules/sessionService.md)
742. [snapshotService](modules/snapshotService.md)
743. [snapshotVersions.test](modules/snapshotVersions.test.md)
744. [systemSettingsService](modules/systemSettingsService.md)
745. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
746. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
747. [taskService](modules/taskService.md)
748. [DeliveryDependencies](modules/DeliveryDependencies.md)
749. [ImportTasksModal](modules/ImportTasksModal.md)
750. [MetricCount](modules/MetricCount.md)
751. [PagedTaskBrowser](modules/PagedTaskBrowser.md)
752. [PagedTaskBrowser.test](modules/PagedTaskBrowser.test.md)
753. [TaskContextSummary](modules/TaskContextSummary.md)
754. [TaskDependencySelector](modules/TaskDependencySelector.md)
755. [TaskMergeDialog](modules/TaskMergeDialog.md)
756. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
757. [TaskTextEditorModal.test](modules/TaskTextEditorModal.test.md)
758. [taskEditorSnapshot](modules/taskEditorSnapshot.md)
759. [useAgentRowFacts](modules/useAgentRowFacts.md)
760. [useTaskReviewer](modules/useTaskReviewer.md)
761. [TaskReviewer](modules/TaskReviewer.md)
762. [TaskWorkPanel](modules/TaskWorkPanel.md)
763. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
764. [TriageActionModal](modules/TriageActionModal.md)
765. [overviewBacklog](modules/overviewBacklog.md)
766. [taskDependencyVersions.test](modules/taskDependencyVersions.test.md)
767. [teamService](modules/teamService.md)
768. [TeamForm](modules/TeamForm.md)
769. [TeamForm.test](modules/TeamForm.test.md)
770. [capacityMutations](modules/capacityMutations.md)
771. [PlanQuickAddCapacity](modules/PlanQuickAddCapacity.md)
772. [PlanQuickAddCapacity.test](modules/PlanQuickAddCapacity.test.md)
773. [GanttBarInputs](modules/GanttBarInputs.md)
774. [AssigneePicker](modules/AssigneePicker.md)
775. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
776. [TaskBulkOperationsPanel.test](modules/TaskBulkOperationsPanel.test.md)
777. [TaskSelectionBar](modules/TaskSelectionBar.md)
778. [useTaskRowEdits](modules/useTaskRowEdits.md)
779. [useIterationRowData](modules/useIterationRowData.md)
780. [useTaskAssigneeDisplay](modules/useTaskAssigneeDisplay.md)
781. [TaskAssigneeDisplay](modules/TaskAssigneeDisplay.md)
782. [KanbanCard](modules/KanbanCard.md)
783. [KanbanColumn](modules/KanbanColumn.md)
784. [KanbanColumn.test](modules/KanbanColumn.test.md)
785. [ImportTeamModal](modules/ImportTeamModal.md)
786. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
787. [VacationCsvImport](modules/VacationCsvImport.md)
788. [sampleProject](modules/sampleProject.md)
789. [SampleProjectAction](modules/SampleProjectAction.md)
790. [LocalProfilePicker](modules/LocalProfilePicker.md)
791. [GetStartedPanel](modules/GetStartedPanel.md)
792. [AccountMenu](modules/AccountMenu.md)
793. [UserSessionBadge](modules/UserSessionBadge.md)
794. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
795. [IdentityProvider.test](modules/IdentityProvider.test.md)
796. [usePlanScheduleWorkloads](modules/usePlanScheduleWorkloads.md)
797. [templateService](modules/templateService.md)
798. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
799. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
800. [timeEntryService](modules/timeEntryService.md)
801. [useTimeEntries](modules/useTimeEntries.md)
802. [timeEntryService.test](modules/timeEntryService.test.md)
803. [triageService](modules/triageService.md)
804. [AppSidebar](modules/AppSidebar.md)
805. [AppSidebar.planProgress.test](modules/AppSidebar.planProgress.test.md)
806. [AppSidebar.test](modules/AppSidebar.test.md)
807. [QuickCapture](modules/QuickCapture.md)
808. [QuickCapture.test](modules/QuickCapture.test.md)
809. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
810. [usePlanningReadiness](modules/usePlanningReadiness.md)
811. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
812. [planningScope.test](modules/planningScope.test.md)
813. [workspaceApi](modules/workspaceApi.md)
814. [pageChrome.test](modules/pageChrome.test.md)
815. [copyText](modules/copyText.md)
816. [focusLifecycle](modules/focusLifecycle.md)
817. [focusLifecycle.test](modules/focusLifecycle.test.md)
818. [formatDate](modules/formatDate.md)
819. [DeliveryAnalytics](modules/DeliveryAnalytics.md)
820. [ExecutionUsagePanel](modules/ExecutionUsagePanel.md)
821. [VacationManager](modules/VacationManager.md)
822. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
823. [IterationForm](modules/IterationForm.md)
824. [IterationEditorDrawer](modules/IterationEditorDrawer.md)
825. [IterationForm.test](modules/IterationForm.test.md)
826. [ScopeBar](modules/ScopeBar.md)
827. [DeliveryAnalytics.test](modules/DeliveryAnalytics.test.md)
828. [ScopeBar.test](modules/ScopeBar.test.md)
829. [NotificationsPanel](modules/NotificationsPanel.md)
830. [PlanIterationCheckpoint](modules/PlanIterationCheckpoint.md)
831. [PlanShareSection](modules/PlanShareSection.md)
832. [PlanReviewSection](modules/PlanReviewSection.md)
833. [PlanShareSection.test](modules/PlanShareSection.test.md)
834. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
835. [ConnectedReadersPanel](modules/ConnectedReadersPanel.md)
836. [ConnectedReadersPanel.test](modules/ConnectedReadersPanel.test.md)
837. [StatusChangeControl](modules/StatusChangeControl.md)
838. [TaskDiscussion](modules/TaskDiscussion.md)
839. [TaskDiscussion.test](modules/TaskDiscussion.test.md)
840. [TimeEntriesPanel](modules/TimeEntriesPanel.md)
841. [TimeEntriesReport](modules/TimeEntriesReport.md)
842. [TimeEntriesReport.test](modules/TimeEntriesReport.test.md)
843. [TimeEntriesPanel.test](modules/TimeEntriesPanel.test.md)
844. [AgentManifestWorkflow](modules/AgentManifestWorkflow.md)
845. [AgentManifestWorkflow.test](modules/AgentManifestWorkflow.test.md)
846. [ModelCatalog](modules/ModelCatalog.md)
847. [TeamProfileManager](modules/TeamProfileManager.md)
848. [TeamDirectory](modules/TeamDirectory.md)
849. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
850. [TriageRow](modules/TriageRow.md)
851. [TriageList](modules/TriageList.md)
852. [TriageList.test](modules/TriageList.test.md)
853. [TriageSuggestions](modules/TriageSuggestions.md)
854. [planEvidence](modules/planEvidence.md)
855. [PlanSharePage](modules/PlanSharePage.md)
856. [PlanSharePage.test](modules/PlanSharePage.test.md)
857. [scopedPageRender.test](modules/scopedPageRender.test.md)
858. [graphLimitError](modules/graphLimitError.md)
859. [modelRouting](modules/modelRouting.md)
860. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
861. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
862. [ConnectAgentSteps](modules/ConnectAgentSteps.md)
863. [ConnectAgentSteps.test](modules/ConnectAgentSteps.test.md)
864. [modelRouting.test](modules/modelRouting.test.md)
865. [protectedQueries](modules/protectedQueries.md)
866. [AssignedAgentsSummary](modules/AssignedAgentsSummary.md)
867. [AssignedAgentsSummary.test](modules/AssignedAgentsSummary.test.md)
868. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
869. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
870. [AgentAccessPanel](modules/AgentAccessPanel.md)
871. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
872. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
873. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
874. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
875. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
876. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
877. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
878. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
879. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
880. [PipelineTaskEvidence](modules/PipelineTaskEvidence.md)
881. [usePipeline](modules/usePipeline.md)
882. [AgentModelAdministration](modules/AgentModelAdministration.md)
883. [PipelineTaskEvidence.test](modules/PipelineTaskEvidence.test.md)
884. [TeamPage](modules/TeamPage.md)
885. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
886. [IdentityProvider.keepRoute.test](modules/IdentityProvider.keepRoute.test.md)
887. [TeamPage.test](modules/TeamPage.test.md)
888. [TeamPage.transport.test](modules/TeamPage.transport.test.md)
889. [safeUrl](modules/safeUrl.md)
890. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
891. [ProjectRequestsTab](modules/ProjectRequestsTab.md)
892. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
893. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
894. [TaskReadView](modules/TaskReadView.md)
895. [TaskReadView.brief.test](modules/TaskReadView.brief.test.md)
896. [TaskReadView.dispatch.test](modules/TaskReadView.dispatch.test.md)
897. [TaskReadView.operatorKey.test](modules/TaskReadView.operatorKey.test.md)
898. [TaskReadView.test](modules/TaskReadView.test.md)
899. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
900. [TriageDetailPanel](modules/TriageDetailPanel.md)
901. [TriageConvertSource](modules/TriageConvertSource.md)
902. [ConvertTriageDrawer](modules/ConvertTriageDrawer.md)
903. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
904. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
905. [CommandMenu](modules/CommandMenu.md)
906. [CommandMenu.test](modules/CommandMenu.test.md)
907. [ContextHelp](modules/ContextHelp.md)
908. [AppTopNav](modules/AppTopNav.md)
909. [AppShell](modules/AppShell.md)
910. [App](modules/App.md)
911. [App.legacyRoutes.test](modules/App.legacyRoutes.test.md)
912. [AppShell.test](modules/AppShell.test.md)
913. [AppTopNav.test](modules/AppTopNav.test.md)
914. [ContextHelp.test](modules/ContextHelp.test.md)
915. [shellViewport.test](modules/shellViewport.test.md)
916. [AccountMenu.test](modules/AccountMenu.test.md)
917. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
918. [src_main](modules/src_main.md)
919. [SettingsPage](modules/SettingsPage.md)
920. [SettingsPage.calendar.test](modules/SettingsPage.calendar.test.md)
921. [SettingsPage.labels.test](modules/SettingsPage.labels.test.md)
922. [SettingsPage.readOnlyPanels.test](modules/SettingsPage.readOnlyPanels.test.md)
923. [SettingsPage.test](modules/SettingsPage.test.md)
924. [SettingsPage.unlock.test](modules/SettingsPage.unlock.test.md)
925. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
926. [taskFilterDefaults](modules/taskFilterDefaults.md)
927. [TaskFiltersBar](modules/TaskFiltersBar.md)
928. [TaskFiltersBar.test](modules/TaskFiltersBar.test.md)
929. [taskViewParams](modules/taskViewParams.md)
930. [taskViewParams.test](modules/taskViewParams.test.md)
931. [taskViewState](modules/taskViewState.md)
932. [savedViewState](modules/savedViewState.md)
933. [useSavedViewManager](modules/useSavedViewManager.md)
934. [savedViewState.test](modules/savedViewState.test.md)
935. [taskFilters](modules/taskFilters.md)
936. [taskFilters.test](modules/taskFilters.test.md)
937. [teamMemberLabels](modules/teamMemberLabels.md)
938. [InitiativeForm](modules/InitiativeForm.md)
939. [InitiativeGroupHeader](modules/InitiativeGroupHeader.md)
940. [RoadmapView](modules/RoadmapView.md)
941. [RoadmapView.test](modules/RoadmapView.test.md)
942. [sampleProject.test](modules/sampleProject.test.md)
943. [templateDefaults](modules/templateDefaults.md)
944. [ProjectForm](modules/ProjectForm.md)
945. [ProjectForm.test](modules/ProjectForm.test.md)
946. [TaskForm](modules/TaskForm.md)
947. [AssigneePicker.test](modules/AssigneePicker.test.md)
948. [GuardedTaskDrawer](modules/GuardedTaskDrawer.md)
949. [BacklogPanel](modules/BacklogPanel.md)
950. [CurrentTaskDrawer.test](modules/CurrentTaskDrawer.test.md)
951. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
952. [TaskEditDrawer](modules/TaskEditDrawer.md)
953. [GanttChart](modules/GanttChart.md)
954. [GanttChart.test](modules/GanttChart.test.md)
955. [TaskEditDrawer.test](modules/TaskEditDrawer.test.md)
956. [ProjectTaskTree](modules/ProjectTaskTree.md)
957. [ProjectTasksTab](modules/ProjectTasksTab.md)
958. [ProjectTaskTree.test](modules/ProjectTaskTree.test.md)
959. [TaskEditorDrawer.flow.test](modules/TaskEditorDrawer.flow.test.md)
960. [TaskEditorDrawer.test](modules/TaskEditorDrawer.test.md)
961. [TaskForm.test](modules/TaskForm.test.md)
962. [TaskFormSections.test](modules/TaskFormSections.test.md)
963. [CreateTriageDrawer](modules/CreateTriageDrawer.md)
964. [GanttPage](modules/GanttPage.md)
965. [GanttPage.test](modules/GanttPage.test.md)
966. [MyWorkPage](modules/MyWorkPage.md)
967. [MyWorkPage.test](modules/MyWorkPage.test.md)
968. [TriagePage](modules/TriagePage.md)
969. [TriagePage.test](modules/TriagePage.test.md)
970. [ganttChrome.test](modules/ganttChrome.test.md)
971. [visibleWork](modules/visibleWork.md)
972. [KanbanBoard](modules/KanbanBoard.md)
973. [KanbanBoard.test](modules/KanbanBoard.test.md)
974. [TaskList](modules/TaskList.md)
975. [TaskList.test](modules/TaskList.test.md)
976. [overviewSignals](modules/overviewSignals.md)
977. [PipelineView](modules/PipelineView.md)
978. [assigneeDisplay.test](modules/assigneeDisplay.test.md)
979. [overviewSignals.test](modules/overviewSignals.test.md)
980. [TasksPage](modules/TasksPage.md)
981. [backlogScope.test](modules/backlogScope.test.md)
982. [TasksPage.board.test](modules/TasksPage.board.test.md)
983. [TasksPage.pipeline.test](modules/TasksPage.pipeline.test.md)
984. [TasksPage.test](modules/TasksPage.test.md)
985. [TasksPage.toolbar.test](modules/TasksPage.toolbar.test.md)
986. [visibleWork.test](modules/visibleWork.test.md)
987. [workNumbers](modules/workNumbers.md)
988. [OnTrackSummary](modules/OnTrackSummary.md)
989. [StatusDistribution](modules/StatusDistribution.md)
990. [IterationOutlook.test](modules/IterationOutlook.test.md)
991. [CapacityTable](modules/CapacityTable.md)
992. [TeamList](modules/TeamList.md)
993. [CapacitySection](modules/CapacitySection.md)
994. [CapacitySection.test](modules/CapacitySection.test.md)
995. [IterationCapacityLine](modules/IterationCapacityLine.md)
996. [TeamList.test](modules/TeamList.test.md)
997. [IterationList](modules/IterationList.md)
998. [AllIterationsDrawer](modules/AllIterationsDrawer.md)
999. [AllIterationsDrawer.test](modules/AllIterationsDrawer.test.md)
1000. [PlanBlockersSection](modules/PlanBlockersSection.md)
1001. [PlanIterationDrawers](modules/PlanIterationDrawers.md)
1002. [PlanScheduleSection](modules/PlanScheduleSection.md)
1003. [PlanWorkSection](modules/PlanWorkSection.md)
1004. [projectDetailShared](modules/projectDetailShared.md)
1005. [MilestoneFormDrawer](modules/MilestoneFormDrawer.md)
1006. [MilestonesSection](modules/MilestonesSection.md)
1007. [PostUpdateDrawer](modules/PostUpdateDrawer.md)
1008. [ProjectHeaderFields](modules/ProjectHeaderFields.md)
1009. [ProjectReleasesTab](modules/ProjectReleasesTab.md)
1010. [ProjectSummaryTab](modules/ProjectSummaryTab.md)
1011. [ProjectUpdatesTab](modules/ProjectUpdatesTab.md)
1012. [WorkMetricsLine](modules/WorkMetricsLine.md)
1013. [MetricCount.test](modules/MetricCount.test.md)
1014. [planningLinks.test](modules/planningLinks.test.md)
1015. [AnalyticsPage](modules/AnalyticsPage.md)
1016. [ExecutionUsagePanel.test](modules/ExecutionUsagePanel.test.md)
1017. [scopedPages.test](modules/scopedPages.test.md)
1018. [AnalyticsPage.test](modules/AnalyticsPage.test.md)
1019. [OverviewPage](modules/OverviewPage.md)
1020. [GetStartedPanel.test](modules/GetStartedPanel.test.md)
1021. [OverviewPage.test](modules/OverviewPage.test.md)
1022. [PlanPage](modules/PlanPage.md)
1023. [planProgressPlacement.test](modules/planProgressPlacement.test.md)
1024. [GetStartedFlow.test](modules/GetStartedFlow.test.md)
1025. [PlanIterations.test](modules/PlanIterations.test.md)
1026. [PlanPage.test](modules/PlanPage.test.md)
1027. [ProjectDetailPage](modules/ProjectDetailPage.md)
1028. [ProjectDetailPage.test](modules/ProjectDetailPage.test.md)
1029. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
1030. [ProjectReleaseDetailPage.test](modules/ProjectReleaseDetailPage.test.md)
1031. [ProjectsPage](modules/ProjectsPage.md)
1032. [ProjectsPage.test](modules/ProjectsPage.test.md)
1033. [destinationEmptyStates.test](modules/destinationEmptyStates.test.md)
1034. [tailwind.config](modules/tailwind.config.md)
1035. [check-tailwind-classes](modules/check-tailwind-classes.md)
1036. [vite.config](modules/vite.config.md)
1037. [vitest.config](modules/vitest.config.md)
1038. [create_agent_actor](modules/create_agent_actor.md)
1039. [generate_workchord_keys](modules/generate_workchord_keys.md)
1040. [setup_agent_team](modules/setup_agent_team.md)
1041. [build_agent_skills](modules/build_agent_skills.md)
1042. [build_frontend_image_identity](modules/build_frontend_image_identity.md)
1043. [android_qualification](modules/android_qualification.md)
1044. [android_web_peer](modules/android_web_peer.md)
1045. [apt_runtime](modules/apt_runtime.md)
1046. [browser_performance](modules/browser_performance.md)
1047. [browser_planning_inputs](modules/browser_planning_inputs.md)
1048. [browser_worker](modules/browser_worker.md)
1049. [browser_managed_work](modules/browser_managed_work.md)
1050. [browser_write_readback](modules/browser_write_readback.md)
1051. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
1052. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
1053. [ci_runtime](modules/ci_runtime.md)
1054. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
1055. [postgres_runtime](modules/postgres_runtime.md)
1056. [run_android_checks](modules/run_android_checks.md)
1057. [run_disposable_checks](modules/run_disposable_checks.md)
1058. [serve_disposable_api](modules/serve_disposable_api.md)
1059. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
1060. [test_apt_runtime](modules/test_apt_runtime.md)
1061. [test_ci_runtime](modules/test_ci_runtime.md)
1062. [test_native_runtimes](modules/test_native_runtimes.md)
1063. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
1064. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
1065. [generate_client_contract](modules/generate_client_contract.md)
1066. [generate_mobile_contract_fixtures](modules/generate_mobile_contract_fixtures.md)
1067. [load_common](modules/load_common.md)
1068. [collect](modules/collect.md)
1069. [result](modules/result.md)
1070. [compare](modules/compare.md)
1071. [finalize](modules/finalize.md)
1072. [qualify](modules/qualify.md)
1073. [resilience](modules/resilience.md)
1074. [run](modules/run.md)
1075. [seal](modules/seal.md)
1076. [seed](modules/seed.md)
1077. [source_binding](modules/source_binding.md)
1078. [local_baseline](modules/local_baseline.md)
1079. [service_worksets](modules/service_worksets.md)
1080. [export_acceptance_artifacts](modules/export_acceptance_artifacts.md)
1081. [isolated_rehearsal](modules/isolated_rehearsal.md)

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
| [PersonCapacity.test](modules/PersonCapacity.test.md) | `api = hoisted`, `mock`, `beforeEach`, `it` |
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
