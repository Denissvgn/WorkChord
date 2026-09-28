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
31. [20260506_0000_legacy_core_baseline](modules/20260506_0000_legacy_core_baseline.md)
32. [20260507_0001_agentic_tracing](modules/20260507_0001_agentic_tracing.md)
33. [20260507_0002_create_projects](modules/20260507_0002_create_projects.md)
34. [20260507_0003_link_tasks_projects](modules/20260507_0003_link_tasks_projects.md)
35. [20260508_0004_create_triage_items](modules/20260508_0004_create_triage_items.md)
36. [20260508_0005_create_work_templates](modules/20260508_0005_create_work_templates.md)
37. [20260508_0006_add_work_template_seed_key](modules/20260508_0006_add_work_template_seed_key.md)
38. [20260509_0007_create_label_groups](modules/20260509_0007_create_label_groups.md)
39. [20260509_0008_create_saved_views](modules/20260509_0008_create_saved_views.md)
40. [20260509_0009_add_saved_view_seed_key](modules/20260509_0009_add_saved_view_seed_key.md)
41. [20260509_0010_create_project_updates](modules/20260509_0010_create_project_updates.md)
42. [20260509_0011_create_project_milestones](modules/20260509_0011_create_project_milestones.md)
43. [20260509_0012_link_tasks_milestones](modules/20260509_0012_link_tasks_milestones.md)
44. [20260509_0013_create_initiatives](modules/20260509_0013_create_initiatives.md)
45. [20260509_0014_create_external_links](modules/20260509_0014_create_external_links.md)
46. [20260509_0015_create_github_status_automation_rules](modules/20260509_0015_create_github_status_automation_rules.md)
47. [20260509_0016_create_releases](modules/20260509_0016_create_releases.md)
48. [20260509_0017_create_request_sources](modules/20260509_0017_create_request_sources.md)
49. [20260509_0018_create_triage_classification_suggestions](modules/20260509_0018_create_triage_classification_suggestions.md)
50. [20260509_0019_create_outbound_webhooks](modules/20260509_0019_create_outbound_webhooks.md)
51. [20260509_0020_add_triage_metadata_json](modules/20260509_0020_add_triage_metadata_json.md)
52. [20260510_0021_create_team_member_profiles](modules/20260510_0021_create_team_member_profiles.md)
53. [20260510_0022_create_system_settings](modules/20260510_0022_create_system_settings.md)
54. [20260510_0023_create_user_sessions](modules/20260510_0023_create_user_sessions.md)
55. [20260515_0024_move_portfolio_ownership_to_profiles](modules/20260515_0024_move_portfolio_ownership_to_profiles.md)
56. [20260516_0025_add_project_scope_to_iterations](modules/20260516_0025_add_project_scope_to_iterations.md)
57. [20260709_0026_add_opaque_browser_sessions](modules/20260709_0026_add_opaque_browser_sessions.md)
58. [20260709_0027_add_durable_outbound_delivery_queue](modules/20260709_0027_add_durable_outbound_delivery_queue.md)
59. [20260711_0028_add_agent_skill_control_plane](modules/20260711_0028_add_agent_skill_control_plane.md)
60. [20260718_0029_add_agent_model_catalog](modules/20260718_0029_add_agent_model_catalog.md)
61. [20260718_0030_add_task_routing_assessments](modules/20260718_0030_add_task_routing_assessments.md)
62. [20260718_0031_align_postgresql_types](modules/20260718_0031_align_postgresql_types.md)
63. [20260727_0034_add_agent_run_model_trust](modules/20260727_0034_add_agent_run_model_trust.md)
64. [20260916_0039_task_deletion_fences](modules/20260916_0039_task_deletion_fences.md)
65. [query_limits](modules/query_limits.md)
66. [runtime_telemetry](modules/runtime_telemetry.md)
67. [database_runtime](modules/database_runtime.md)
68. [maintenance](modules/maintenance.md)
69. [schemas_agent_planning](modules/schemas_agent_planning.md)
70. [agent_skill_bundle](modules/agent_skill_bundle.md)
71. [agent_team_setup](modules/agent_team_setup.md)
72. [schemas_autonomy](modules/schemas_autonomy.md)
73. [schemas_common](modules/schemas_common.md)
74. [schemas_github](modules/schemas_github.md)
75. [schemas_intake](modules/schemas_intake.md)
76. [schemas_label](modules/schemas_label.md)
77. [schemas_plan_share](modules/schemas_plan_share.md)
78. [planning_inputs](modules/planning_inputs.md)
79. [schemas_calendar](modules/schemas_calendar.md)
80. [schemas_saved_view](modules/schemas_saved_view.md)
81. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
82. [schemas_session](modules/schemas_session.md)
83. [snapshot](modules/snapshot.md)
84. [schemas_system_settings](modules/schemas_system_settings.md)
85. [schemas_email_settings](modules/schemas_email_settings.md)
86. [schemas_task_brief](modules/schemas_task_brief.md)
87. [schemas_llm](modules/schemas_llm.md)
88. [schemas_task_domain](modules/schemas_task_domain.md)
89. [schemas_team](modules/schemas_team.md)
90. [schemas_template](modules/schemas_template.md)
91. [schemas_work_metrics](modules/schemas_work_metrics.md)
92. [schemas_iteration](modules/schemas_iteration.md)
93. [schemas_project](modules/schemas_project.md)
94. [schemas_release](modules/schemas_release.md)
95. [security](modules/security.md)
96. [agent_routing_policy](modules/agent_routing_policy.md)
97. [agent_routing](modules/agent_routing.md)
98. [agent_routing_rollout](modules/agent_routing_rollout.md)
99. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
100. [language_service](modules/language_service.md)
101. [scheduling_rules_service](modules/scheduling_rules_service.md)
102. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
103. [upgrade_service](modules/upgrade_service.md)
104. [upgrade](modules/upgrade.md)
105. [sql_semantics](modules/sql_semantics.md)
106. [exceptions](modules/exceptions.md)
107. [text_similarity](modules/text_similarity.md)
108. [time](modules/time.md)
109. [20260718_0032_add_database_migration_gate](modules/20260718_0032_add_database_migration_gate.md)
110. [20260719_0033_add_autonomy_control_plane](modules/20260719_0033_add_autonomy_control_plane.md)
111. [20260728_0035_add_agent_team_setup](modules/20260728_0035_add_agent_team_setup.md)
112. [20260802_0036_add_plan_shares](modules/20260802_0036_add_plan_shares.md)
113. [20260915_0037_add_authority_and_recovery](modules/20260915_0037_add_authority_and_recovery.md)
114. [20260915_0038_canonical_task_domain](modules/20260915_0038_canonical_task_domain.md)
115. [observability](modules/observability.md)
116. [app_database](modules/app_database.md)
117. [models_agent](modules/models_agent.md)
118. [models_autonomy](modules/models_autonomy.md)
119. [models_calendar](modules/models_calendar.md)
120. [models_database_migration](modules/models_database_migration.md)
121. [models_external_link](modules/models_external_link.md)
122. [models_github](modules/models_github.md)
123. [models_identity](modules/models_identity.md)
124. [models_iteration](modules/models_iteration.md)
125. [models_label](modules/models_label.md)
126. [models_outbound_webhook](modules/models_outbound_webhook.md)
127. [models_plan_share](modules/models_plan_share.md)
128. [models_release](modules/models_release.md)
129. [models_project](modules/models_project.md)
130. [models_request_source](modules/models_request_source.md)
131. [models_saved_view](modules/models_saved_view.md)
132. [models_system_settings](modules/models_system_settings.md)
133. [models_task](modules/models_task.md)
134. [recovery](modules/recovery.md)
135. [models_task_brief](modules/models_task_brief.md)
136. [task_status_log](modules/task_status_log.md)
137. [team_member](modules/team_member.md)
138. [models_template](modules/models_template.md)
139. [models_triage](modules/models_triage.md)
140. [user_session](modules/user_session.md)
141. [models___init__](modules/models___init__.md)
142. [catalog](modules/catalog.md)
143. [database_migration_canonical](modules/database_migration_canonical.md)
144. [source](modules/source.md)
145. [transfer](modules/transfer.md)
146. [cli_database_migration](modules/cli_database_migration.md)
147. [database_migration___init__](modules/database_migration___init__.md)
148. [migrations_env](modules/migrations_env.md)
149. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
150. [calendar_service](modules/calendar_service.md)
151. [calendars](modules/calendars.md)
152. [identity_service](modules/identity_service.md)
153. [iteration_service](modules/iteration_service.md)
154. [iterations](modules/iterations.md)
155. [label_service](modules/label_service.md)
156. [labels](modules/labels.md)
157. [saved_view_service](modules/saved_view_service.md)
158. [session_service](modules/session_service.md)
159. [http_authority](modules/http_authority.md)
160. [routers_identity](modules/routers_identity.md)
161. [saved_views](modules/saved_views.md)
162. [routers_session](modules/routers_session.md)
163. [task_brief_service](modules/task_brief_service.md)
164. [task_context_revision_service](modules/task_context_revision_service.md)
165. [task_domain_service](modules/task_domain_service.md)
166. [task_recovery_service](modules/task_recovery_service.md)
167. [team_service](modules/team_service.md)
168. [routers_team](modules/routers_team.md)
169. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
170. [snapshot_service](modules/snapshot_service.md)
171. [plan_share_service](modules/plan_share_service.md)
172. [plan_shares](modules/plan_shares.md)
173. [template_service](modules/template_service.md)
174. [templates](modules/templates.md)
175. [services_work_metrics](modules/services_work_metrics.md)
176. [import_parser](modules/import_parser.md)
177. [url_policy](modules/url_policy.md)
178. [schemas_external_link](modules/schemas_external_link.md)
179. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
180. [schemas_request_source](modules/schemas_request_source.md)
181. [schemas_task](modules/schemas_task.md)
182. [schemas_gantt](modules/schemas_gantt.md)
183. [task_detail](modules/task_detail.md)
184. [schemas_triage](modules/schemas_triage.md)
185. [schemas___init__](modules/schemas___init__.md)
186. [schemas_agent](modules/schemas_agent.md)
187. [agent_readiness](modules/agent_readiness.md)
188. [llm_service](modules/llm_service.md)
189. [system_settings_service](modules/system_settings_service.md)
190. [routers_system_settings](modules/routers_system_settings.md)
191. [email_settings_service](modules/email_settings_service.md)
192. [routers_email_settings](modules/routers_email_settings.md)
193. [notification_service](modules/notification_service.md)
194. [outbound_webhook_service](modules/outbound_webhook_service.md)
195. [worker](modules/worker.md)
196. [outbound_webhooks](modules/outbound_webhooks.md)
197. [external_link_service](modules/external_link_service.md)
198. [github_status_service](modules/github_status_service.md)
199. [request_source_service](modules/request_source_service.md)
200. [request_sources](modules/request_sources.md)
201. [project_service](modules/project_service.md)
202. [task_detail_service](modules/task_detail_service.md)
203. [task_import_service](modules/task_import_service.md)
204. [task_service](modules/task_service.md)
205. [export](modules/export.md)
206. [snapshots](modules/snapshots.md)
207. [routers_task_domain](modules/routers_task_domain.md)
208. [agent_routing_observability](modules/agent_routing_observability.md)
209. [agent_service](modules/agent_service.md)
210. [agent_skill_bundles](modules/agent_skill_bundles.md)
211. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
212. [agent_routing_service](modules/agent_routing_service.md)
213. [agent_team_setup_service](modules/agent_team_setup_service.md)
214. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
215. [backlog_snapshot_service](modules/backlog_snapshot_service.md)
216. [github_status_automation_service](modules/github_status_automation_service.md)
217. [release_service](modules/release_service.md)
218. [projects](modules/projects.md)
219. [scheduler_service](modules/scheduler_service.md)
220. [routers_gantt](modules/routers_gantt.md)
221. [routers_llm](modules/routers_llm.md)
222. [agent_planning_service](modules/agent_planning_service.md)
223. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
224. [tasks](modules/tasks.md)
225. [task_status_service](modules/task_status_service.md)
226. [hierarchy_repair_service](modules/hierarchy_repair_service.md)
227. [triage_service](modules/triage_service.md)
228. [routers_triage](modules/routers_triage.md)
229. [agent_work_service](modules/agent_work_service.md)
230. [mcp_agent_tools](modules/mcp_agent_tools.md)
231. [mcp_server](modules/mcp_server.md)
232. [routers_agent](modules/routers_agent.md)
233. [routers_agent_planning](modules/routers_agent_planning.md)
234. [agent_catalog](modules/agent_catalog.md)
235. [github_webhook_service](modules/github_webhook_service.md)
236. [routers_github](modules/routers_github.md)
237. [web_intake_service](modules/web_intake_service.md)
238. [routers_intake](modules/routers_intake.md)
239. [app_main](modules/app_main.md)
240. [routers___init__](modules/routers___init__.md)
241. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
242. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
243. [test_server_acceptance](modules/test_server_acceptance.md)
244. [test_work_package_service](modules/test_work_package_service.md)
245. [test_database_configuration](modules/test_database_configuration.md)
246. [test_deployment_topology](modules/test_deployment_topology.md)
247. [test_observability](modules/test_observability.md)
248. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
249. [test_query_boundaries](modules/test_query_boundaries.md)
250. [test_runtime_policy](modules/test_runtime_policy.md)
251. [test_schema_behavior](modules/test_schema_behavior.md)
252. [test_cutover_evidence](modules/test_cutover_evidence.md)
253. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
254. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
255. [test_source_preflight](modules/test_source_preflight.md)
256. [test_transfer_catalog](modules/test_transfer_catalog.md)
257. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
258. [0001_wave0_probe](modules/0001_wave0_probe.md)
259. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
260. [test_load_tooling](modules/test_load_tooling.md)
261. [support_database](modules/support_database.md)
262. [delivery](modules/delivery.md)
263. [factories](modules/factories.md)
264. [faults](modules/faults.md)
265. [schema](modules/schema.md)
266. [support___init__](modules/support___init__.md)
267. [conftest](modules/conftest.md)
268. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
269. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
270. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
271. [transactions](modules/transactions.md)
272. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
273. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
274. [test_agent_routing_data](modules/test_agent_routing_data.md)
275. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
276. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
277. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
278. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
279. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
280. [test_agent_routing_service](modules/test_agent_routing_service.md)
281. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
282. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
283. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
284. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
285. [test_agent_team_setup](modules/test_agent_team_setup.md)
286. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
287. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
288. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
289. [test_authority_migrations](modules/test_authority_migrations.md)
290. [test_capacity_contract](modules/test_capacity_contract.md)
291. [test_client_contract](modules/test_client_contract.md)
292. [test_database_harness](modules/test_database_harness.md)
293. [test_delivery_scenarios](modules/test_delivery_scenarios.md)
294. [test_managed_authority](modules/test_managed_authority.md)
295. [test_identity_lifecycle](modules/test_identity_lifecycle.md)
296. [test_plan_shares](modules/test_plan_shares.md)
297. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
298. [test_process_roles](modules/test_process_roles.md)
299. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
300. [test_saved_view_service](modules/test_saved_view_service.md)
301. [test_task_domain](modules/test_task_domain.md)
302. [test_task_domain_integrity](modules/test_task_domain_integrity.md)
303. [test_task_domain_migrations](modules/test_task_domain_migrations.md)
304. [test_work_correctness](modules/test_work_correctness.md)
305. [eslint.config](modules/eslint.config.md)
306. [postcss.config](modules/postcss.config.md)
307. [Button](modules/Button.md)
308. [Button.test](modules/Button.test.md)
309. [Checkbox](modules/Checkbox.md)
310. [CollapsibleSection](modules/CollapsibleSection.md)
311. [Input](modules/Input.md)
312. [Input.test](modules/Input.test.md)
313. [dialogLayer](modules/dialogLayer.md)
314. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
315. [Modal](modules/Modal.md)
316. [ConfirmDialog](modules/ConfirmDialog.md)
317. [useConfirmDialog](modules/useConfirmDialog.md)
318. [WorkFreshness](modules/WorkFreshness.md)
319. [toast](modules/toast.md)
320. [ToastProvider](modules/ToastProvider.md)
321. [Breadcrumbs](modules/Breadcrumbs.md)
322. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
323. [commandMenuEvents](modules/commandMenuEvents.md)
324. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
325. [SortableTaskItem](modules/SortableTaskItem.md)
326. [useDraftDismissal](modules/useDraftDismissal.md)
327. [DraftDismissalDialog](modules/DraftDismissalDialog.md)
328. [useDraftDismissal.test](modules/useDraftDismissal.test.md)
329. [InlineEmptyState](modules/InlineEmptyState.md)
330. [MasterProgress](modules/MasterProgress.md)
331. [MasterProgress.test](modules/MasterProgress.test.md)
332. [OverflowMenu](modules/OverflowMenu.md)
333. [PageLayout](modules/PageLayout.md)
334. [SectionCard](modules/SectionCard.md)
335. [SlideOverDrawer](modules/SlideOverDrawer.md)
336. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
337. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
338. [StickyRail](modules/StickyRail.md)
339. [index](modules/index.md)
340. [overviewTaskThread](modules/overviewTaskThread.md)
341. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
342. [planningReturn](modules/planningReturn.md)
343. [PlanReturnBar](modules/PlanReturnBar.md)
344. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
345. [workQueryFreshness](modules/workQueryFreshness.md)
346. [resources.en](modules/resources.en.md)
347. [i18n](modules/i18n.md)
348. [dateLocale](modules/dateLocale.md)
349. [InteractiveCalendar](modules/InteractiveCalendar.md)
350. [resources.ru](modules/resources.ru.md)
351. [i18n.test](modules/i18n.test.md)
352. [routeModules](modules/routeModules.md)
353. [DocumentMetadata](modules/DocumentMetadata.md)
354. [workspaces](modules/workspaces.md)
355. [helpContexts](modules/helpContexts.md)
356. [workspaces.test](modules/workspaces.test.md)
357. [LandingPage](modules/LandingPage.md)
358. [NotFoundPage](modules/NotFoundPage.md)
359. [healthService](modules/healthService.md)
360. [SystemHealthPanel](modules/SystemHealthPanel.md)
361. [iterationStore](modules/iterationStore.md)
362. [themeStore](modules/themeStore.md)
363. [planning-masters.test](modules/planning-masters.test.md)
364. [accessibilityInvariants](modules/accessibilityInvariants.md)
365. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
366. [renderWithProviders](modules/renderWithProviders.md)
367. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
368. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
369. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
370. [OverflowMenu.test](modules/OverflowMenu.test.md)
371. [renderWithProviders.test](modules/renderWithProviders.test.md)
372. [setup](modules/setup.md)
373. [types_calendar](modules/types_calendar.md)
374. [types_label](modules/types_label.md)
375. [outboundWebhook](modules/outboundWebhook.md)
376. [requestSource](modules/requestSource.md)
377. [savedView](modules/savedView.md)
378. [schedulingRules](modules/schedulingRules.md)
379. [ConstraintsPanel](modules/ConstraintsPanel.md)
380. [schedulingDisplay](modules/schedulingDisplay.md)
381. [EffortModifierCard](modules/EffortModifierCard.md)
382. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
383. [SchedulingPassCard](modules/SchedulingPassCard.md)
384. [systemSettings](modules/systemSettings.md)
385. [emailSettings](modules/emailSettings.md)
386. [types_team](modules/types_team.md)
387. [types_task](modules/types_task.md)
388. [types_triage](modules/types_triage.md)
389. [KanbanCard](modules/KanbanCard.md)
390. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
391. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
392. [tone](modules/tone.md)
393. [KanbanColumn](modules/KanbanColumn.md)
394. [Pill](modules/Pill.md)
395. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
396. [tone.test](modules/tone.test.md)
397. [attentionRanking](modules/attentionRanking.md)
398. [attentionRanking.test](modules/attentionRanking.test.md)
399. [planningTaskIssues](modules/planningTaskIssues.md)
400. [planningMasters_masters](modules/planningMasters_masters.md)
401. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
402. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
403. [types_agent](modules/types_agent.md)
404. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
405. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
406. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
407. [statusScopes](modules/statusScopes.md)
408. [statusScopes.test](modules/statusScopes.test.md)
409. [modelAwareRouting](modules/modelAwareRouting.md)
410. [types_github](modules/types_github.md)
411. [types_template](modules/types_template.md)
412. [seedDisplay](modules/seedDisplay.md)
413. [workMetrics](modules/workMetrics.md)
414. [WorkMetricsLine](modules/WorkMetricsLine.md)
415. [types_iteration](modules/types_iteration.md)
416. [types_gantt](modules/types_gantt.md)
417. [types_project](modules/types_project.md)
418. [projectStatusStyles](modules/projectStatusStyles.md)
419. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
420. [types_release](modules/types_release.md)
421. [agentAccess](modules/agentAccess.md)
422. [useAgentAccess](modules/useAgentAccess.md)
423. [apiError](modules/apiError.md)
424. [QueryState](modules/QueryState.md)
425. [taskEditorContract](modules/taskEditorContract.md)
426. [TaskBriefEditor](modules/TaskBriefEditor.md)
427. [TaskBriefEditor.test](modules/TaskBriefEditor.test.md)
428. [taskDraftStorage](modules/taskDraftStorage.md)
429. [adminAccess](modules/adminAccess.md)
430. [api](modules/api.md)
431. [identityService](modules/identityService.md)
432. [identityContext](modules/identityContext.md)
433. [useAdminAccess](modules/useAdminAccess.md)
434. [AdminAccessPanel](modules/AdminAccessPanel.md)
435. [AdminAccessGate](modules/AdminAccessGate.md)
436. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
437. [agentService](modules/agentService.md)
438. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
439. [agentService.test](modules/agentService.test.md)
440. [calendarService](modules/calendarService.md)
441. [emailSettingsService](modules/emailSettingsService.md)
442. [exportService](modules/exportService.md)
443. [ganttService](modules/ganttService.md)
444. [githubService](modules/githubService.md)
445. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
446. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
447. [iterationService](modules/iterationService.md)
448. [IterationSelector](modules/IterationSelector.md)
449. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
450. [SidebarIterationCard](modules/SidebarIterationCard.md)
451. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
452. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
453. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
454. [labelService](modules/labelService.md)
455. [LabelSelector](modules/LabelSelector.md)
456. [outboundWebhookService](modules/outboundWebhookService.md)
457. [planShareService](modules/planShareService.md)
458. [projectService](modules/projectService.md)
459. [releaseService](modules/releaseService.md)
460. [ReleaseForm](modules/ReleaseForm.md)
461. [requestSourceService](modules/requestSourceService.md)
462. [savedViewService](modules/savedViewService.md)
463. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
464. [AppSidebar](modules/AppSidebar.md)
465. [AppSidebar.test](modules/AppSidebar.test.md)
466. [schedulingRulesService](modules/schedulingRulesService.md)
467. [sessionService](modules/sessionService.md)
468. [snapshotService](modules/snapshotService.md)
469. [systemSettingsService](modules/systemSettingsService.md)
470. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
471. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
472. [taskService](modules/taskService.md)
473. [ImportTasksModal](modules/ImportTasksModal.md)
474. [TaskContextSummary](modules/TaskContextSummary.md)
475. [TaskDependencySelector](modules/TaskDependencySelector.md)
476. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
477. [TaskWorkPanel](modules/TaskWorkPanel.md)
478. [TaskWorkPanel.test](modules/TaskWorkPanel.test.md)
479. [teamService](modules/teamService.md)
480. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
481. [TaskFiltersBar](modules/TaskFiltersBar.md)
482. [taskFilterDefaults](modules/taskFilterDefaults.md)
483. [ImportTeamModal](modules/ImportTeamModal.md)
484. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
485. [TeamForm](modules/TeamForm.md)
486. [TeamForm.test](modules/TeamForm.test.md)
487. [TeamProfileManager](modules/TeamProfileManager.md)
488. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
489. [IdentityProvider](modules/IdentityProvider.md)
490. [UserSessionBadge](modules/UserSessionBadge.md)
491. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
492. [CalendarPage](modules/CalendarPage.md)
493. [templateService](modules/templateService.md)
494. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
495. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
496. [triageService](modules/triageService.md)
497. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
498. [usePlanningReadiness](modules/usePlanningReadiness.md)
499. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
500. [copyText](modules/copyText.md)
501. [focusLifecycle](modules/focusLifecycle.md)
502. [focusLifecycle.test](modules/focusLifecycle.test.md)
503. [formatDate](modules/formatDate.md)
504. [TaskStatusFlow](modules/TaskStatusFlow.md)
505. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
506. [IterationForm](modules/IterationForm.md)
507. [IterationForm.test](modules/IterationForm.test.md)
508. [IterationList](modules/IterationList.md)
509. [NotificationsPanel](modules/NotificationsPanel.md)
510. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
511. [StatusChangeControl](modules/StatusChangeControl.md)
512. [VacationManager](modules/VacationManager.md)
513. [TeamList](modules/TeamList.md)
514. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
515. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
516. [AnalyticsPage](modules/AnalyticsPage.md)
517. [IterationsPage](modules/IterationsPage.md)
518. [PlanMasterPage](modules/PlanMasterPage.md)
519. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
520. [PlanPage](modules/PlanPage.md)
521. [PlanPage.test](modules/PlanPage.test.md)
522. [PlanSharePage](modules/PlanSharePage.md)
523. [PlanSharePage.test](modules/PlanSharePage.test.md)
524. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
525. [TeamPage](modules/TeamPage.md)
526. [modelRouting](modules/modelRouting.md)
527. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
528. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
529. [modelRouting.test](modules/modelRouting.test.md)
530. [protectedQueries](modules/protectedQueries.md)
531. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
532. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
533. [AgentAccessPanel](modules/AgentAccessPanel.md)
534. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
535. [AgentModelAdministration](modules/AgentModelAdministration.md)
536. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
537. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
538. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
539. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
540. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
541. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
542. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
543. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
544. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
545. [AgentPipelinePage](modules/AgentPipelinePage.md)
546. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
547. [safeUrl](modules/safeUrl.md)
548. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
549. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
550. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
551. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
552. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
553. [OverviewPage](modules/OverviewPage.md)
554. [OverviewPage.test](modules/OverviewPage.test.md)
555. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
556. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
557. [CommandMenu](modules/CommandMenu.md)
558. [CommandMenu.test](modules/CommandMenu.test.md)
559. [ContextHelp](modules/ContextHelp.md)
560. [AppTopNav](modules/AppTopNav.md)
561. [AppShell](modules/AppShell.md)
562. [App](modules/App.md)
563. [AppShell.test](modules/AppShell.test.md)
564. [AppTopNav.test](modules/AppTopNav.test.md)
565. [ContextHelp.test](modules/ContextHelp.test.md)
566. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
567. [src_main](modules/src_main.md)
568. [SettingsPage](modules/SettingsPage.md)
569. [SettingsPage.test](modules/SettingsPage.test.md)
570. [taskFilters](modules/taskFilters.md)
571. [taskFilters.test](modules/taskFilters.test.md)
572. [teamMemberLabels](modules/teamMemberLabels.md)
573. [InitiativeForm](modules/InitiativeForm.md)
574. [RoadmapPage](modules/RoadmapPage.md)
575. [RoadmapPage.test](modules/RoadmapPage.test.md)
576. [templateDefaults](modules/templateDefaults.md)
577. [ProjectForm](modules/ProjectForm.md)
578. [TaskForm](modules/TaskForm.md)
579. [TaskEditModal](modules/TaskEditModal.md)
580. [GanttChart](modules/GanttChart.md)
581. [GanttChart.test](modules/GanttChart.test.md)
582. [GuardedTaskModal](modules/GuardedTaskModal.md)
583. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
584. [ProjectTaskTree](modules/ProjectTaskTree.md)
585. [TaskForm.test](modules/TaskForm.test.md)
586. [GanttPage](modules/GanttPage.md)
587. [GanttPage.test](modules/GanttPage.test.md)
588. [ProjectDetailPage](modules/ProjectDetailPage.md)
589. [ProjectsPage](modules/ProjectsPage.md)
590. [ProjectsPage.test](modules/ProjectsPage.test.md)
591. [TriagePage](modules/TriagePage.md)
592. [visibleWork](modules/visibleWork.md)
593. [KanbanBoard](modules/KanbanBoard.md)
594. [KanbanBoard.test](modules/KanbanBoard.test.md)
595. [TaskList](modules/TaskList.md)
596. [SavedViewsControl](modules/SavedViewsControl.md)
597. [TaskList.test](modules/TaskList.test.md)
598. [TasksPage](modules/TasksPage.md)
599. [TasksPage.test](modules/TasksPage.test.md)
600. [visibleWork.test](modules/visibleWork.test.md)
601. [tailwind.config](modules/tailwind.config.md)
602. [vite.config](modules/vite.config.md)
603. [vitest.config](modules/vitest.config.md)
604. [create_agent_actor](modules/create_agent_actor.md)
605. [generate_workchord_keys](modules/generate_workchord_keys.md)
606. [setup_agent_team](modules/setup_agent_team.md)
607. [build_agent_skills](modules/build_agent_skills.md)
608. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
609. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
610. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
611. [run_android_checks](modules/run_android_checks.md)
612. [run_disposable_checks](modules/run_disposable_checks.md)
613. [serve_disposable_api](modules/serve_disposable_api.md)
614. [serve_disposable_oidc](modules/serve_disposable_oidc.md)
615. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
616. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
617. [generate_client_contract](modules/generate_client_contract.md)
618. [load_common](modules/load_common.md)
619. [collect](modules/collect.md)
620. [result](modules/result.md)
621. [compare](modules/compare.md)
622. [finalize](modules/finalize.md)
623. [qualify](modules/qualify.md)
624. [resilience](modules/resilience.md)
625. [run](modules/run.md)
626. [seal](modules/seal.md)
627. [seed](modules/seed.md)

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
| [app_main](modules/app_main.md) | `settings = get_settings`, `app = FastAPI`, `app.include_router`, `app.include_router`, `app.add_middleware`, `app.add_middleware`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `mount_mcp_http` |
| [maintenance](modules/maintenance.md) | `SAFE_HTTP_METHODS = frozenset`, `_CORRELATION_ID_PATTERN = re.compile` |
| [mcp_agent_tools](modules/mcp_agent_tools.md) | `_AGENT_ASSIGNMENT_CREATE_ADAPTER = TypeAdapter`, `_AGENT_ASSIGNMENT_UPDATE_ADAPTER = TypeAdapter`, `_AGENT_WORK_BEGIN_ADAPTER = TypeAdapter` |
| [mcp_server](modules/mcp_server.md) | `_http_agent_key = ContextVar`, `mcp = create_mcp_server` |
| [migrations_env](modules/migrations_env.md) | `settings = get_settings`, `database_configuration = parse_database_configuration`, `config.set_main_option`, `fileConfig`, `run_migrations_offline`, `run_migrations_online` |
| [recovery](modules/recovery.md) | `event.listen` |
| [models_release](modules/models_release.md) | `release_tasks = Table` |
| [observability](modules/observability.md) | `logger = logging.getLogger` |
| [routers_agent](modules/routers_agent.md) | `router = APIRouter`, `logger = logging.getLogger` |
| [agent_catalog](modules/agent_catalog.md) | `router = APIRouter` |
| [routers_agent_planning](modules/routers_agent_planning.md) | `router = APIRouter` |
| [agent_skill_bundles](modules/agent_skill_bundles.md) | `router = APIRouter`, `well_known_router = APIRouter` |
| [calendars](modules/calendars.md) | `router = APIRouter` |
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
| [test_postgresql_migrations](modules/test_postgresql_migrations.md) | `ALIGNMENT_MIGRATION = importlib.import_module` |
| [test_load_seed_postgresql](modules/test_load_seed_postgresql.md) | `sys.path.insert` |
| [test_load_tooling](modules/test_load_tooling.md) | `sys.path.insert` |
| [support_database](modules/support_database.md) | `TEST_DATABASE_PATTERN = re.compile`, `TEST_RUNTIME_ROLE_PATTERN = re.compile`, `DEFAULT_POSTGRES_HOSTS = frozenset`, `ADMIN_DATABASES = frozenset` |
| [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md) | `_PROVISION_SPEC = importlib.util.spec_from_file_location`, `provision_actor = importlib.util.module_from_spec`, `_PROVISION_SPEC.loader.exec_module` |
| [test_agent_routing_service](modules/test_agent_routing_service.md) | `pytestmark = pytest.mark.usefixtures` |
| [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md) | `pytestmark = pytest.mark.usefixtures`, `_FIXED_NOW = datetime` |
| [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md) | `SPEC = importlib.util.spec_from_file_location`, `setup_agent_team = importlib.util.module_from_spec`, `SPEC.loader.exec_module` |
| [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md) | `FIXED_NOW = datetime` |
| [App](modules/App.md) | `OverviewPage = lazy`, `LandingPage = lazy`, `PlanPage = lazy`, `PlanMasterPage = lazy`, `PlanSharePage = lazy`, `CalendarPage = lazy`, `IterationsPage = lazy`, `TeamPage = lazy`, `TasksPage = lazy`, `TriagePage = lazy`, `ProjectsPage = lazy`, `ProjectDetailPage = lazy`, `ProjectReleaseDetailPage = lazy`, `RoadmapPage = lazy`, `GanttPage = lazy`, `AnalyticsPage = lazy`, `SettingsPage = lazy`, `AgentPipelinePage = lazy`, `AgentTeamSetupMasterPage = lazy`, `NotFoundPage = lazy` |
| [UserSessionBadge.test](modules/UserSessionBadge.test.md) | `sessionServiceMock = hoisted`, `mock`, `describe` |
| [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md) | `describe` |
| [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md) | `agentServiceMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `dispatchableRoster = map`, `describe` |
| [TaskRoutingPanel](modules/TaskRoutingPanel.md) | `SKILL_CATALOG_READ_SCOPES = Set`, `TEAM_ASSIGNMENT_READ_SCOPES = Set` |
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
| [CommandMenu.test](modules/CommandMenu.test.md) | `describe` |
| [ContextHelp.test](modules/ContextHelp.test.md) | `describe` |
| [SidebarIterationCard.test](modules/SidebarIterationCard.test.md) | `planningReadinessMock = hoisted`, `mock`, `describe` |
| [PlanReturnBar.test](modules/PlanReturnBar.test.md) | `describe` |
| [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md) | `describe` |
| [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md) | `describe` |
| [ProjectForm](modules/ProjectForm.md) | `projectStatusValues = map`, `projectHealthValues = map` |
| [ProjectTaskTree](modules/ProjectTaskTree.md) | `t = bind` |
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
| [SavedViewsControl](modules/SavedViewsControl.md) | `t = bind` |
| [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md) | `describe` |
| [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md) | `t = bind` |
| [TaskBriefEditor.test](modules/TaskBriefEditor.test.md) | `describe` |
| [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md) | `t = bind` |
| [TaskDependencySelector](modules/TaskDependencySelector.md) | `t = bind` |
| [TaskForm.test](modules/TaskForm.test.md) | `api = hoisted`, `mock`, `describe` |
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind` |
| [TaskWorkPanel.test](modules/TaskWorkPanel.test.md) | `service = hoisted`, `mock`, `mock`, `describe` |
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
| [identityContext](modules/identityContext.md) | `IdentityContext = createContext` |
| [attentionRanking.test](modules/attentionRanking.test.md) | `describe`, `describe` |
| [planningMasters_masters.test](modules/planningMasters_masters.test.md) | `describe` |
| [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md) | `describe` |
| [planningNavigationInvalidation](modules/planningNavigationInvalidation.md) | `READINESS_INPUT_QUERY_ROOTS = Set` |
| [planningTaskIssues.test](modules/planningTaskIssues.test.md) | `describe` |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | `describe` |
| [i18n.test](modules/i18n.test.md) | `describe` |
| [src_main](modules/src_main.md) | `queryClient = QueryClient`, `installPlanningNavigationInvalidation`, `installWorkFreshness`, `router = createBrowserRouter`, `render` |
| [workspaces.test](modules/workspaces.test.md) | `describe` |
| [workspaces](modules/workspaces.md) | `PRIMARY_NAV_ITEMS = flatMap` |
| [AgentPipelinePage.test](modules/AgentPipelinePage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
| [AgentPipelinePage](modules/AgentPipelinePage.md) | `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set`, `TASK_STATUSES = Set` |
| [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md) | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe` |
| [GanttPage.test](modules/GanttPage.test.md) | `ganttServiceMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |
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
| [iterationStore](modules/iterationStore.md) | `useIterationStore = create<IterationStore>()` |
| [themeStore](modules/themeStore.md) | `useThemeStore = create<ThemeState>()` |
| [planning-masters.test](modules/planning-masters.test.md) | `planningMastersCss = readFileSync`, `agentTeamMasterSource = readFileSync`, `describe` |
| [accessibilityInvariants.test](modules/accessibilityInvariants.test.md) | `describe` |
| [renderWithProviders.test](modules/renderWithProviders.test.md) | `describe` |
| [setup](modules/setup.md) | `afterEach` |
| [focusLifecycle.test](modules/focusLifecycle.test.md) | `describe` |
| [modelRouting.test](modules/modelRouting.test.md) | `describe` |
| [modelRouting](modules/modelRouting.md) | `ADVANCED_REASON_CODES = Set`, `INDEPENDENT_REASON_CODES = Set`, `STANDARD_REVIEW_REASON_CODES = Set` |
| [selectWorkNowTasks](modules/selectWorkNowTasks.md) | `doneStatuses = Set` |
| [taskFilters.test](modules/taskFilters.test.md) | `describe` |
| [teamMemberLabels](modules/teamMemberLabels.md) | `t = bind` |
| [visibleWork.test](modules/visibleWork.test.md) | `it`, `it`, `it` |
| [build_agent_skills](modules/build_agent_skills.md) | `SEMVER_RE = re.compile`, `SKILL_NAME_RE = re.compile`, `COMPATIBILITY_RE = re.compile`, `MARKDOWN_LINK_RE = re.compile`, `URL_RE = re.compile` |
| [check_postgresql_documentation](modules/check_postgresql_documentation.md) | `LINK_PATTERN = re.compile`, `SHELL_FENCE_PATTERN = re.compile`, `LIVE_SQLITE_COPY_PATTERN = re.compile` |
| [serve_disposable_oidc](modules/serve_disposable_oidc.md) | `url = assert_safe_test_database_url`, `key = rsa.generate_private_key`, `jwk = json.loads`, `jwk['kid'] = 'disposable-key'`, `app = FastAPI` |
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
