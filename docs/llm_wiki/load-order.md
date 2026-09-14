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
22. [database_config](modules/database_config.md)
23. [config](modules/config.md)
24. [database_migration_manifest](modules/database_migration_manifest.md)
25. [database_migration_cutover](modules/database_migration_cutover.md)
26. [cli_cutover](modules/cli_cutover.md)
27. [database_migration_closeout](modules/database_migration_closeout.md)
28. [cli_closeout](modules/cli_closeout.md)
29. [20260506_0000_legacy_core_baseline](modules/20260506_0000_legacy_core_baseline.md)
30. [20260507_0001_agentic_tracing](modules/20260507_0001_agentic_tracing.md)
31. [20260507_0002_create_projects](modules/20260507_0002_create_projects.md)
32. [20260507_0003_link_tasks_projects](modules/20260507_0003_link_tasks_projects.md)
33. [20260508_0004_create_triage_items](modules/20260508_0004_create_triage_items.md)
34. [20260508_0005_create_work_templates](modules/20260508_0005_create_work_templates.md)
35. [20260508_0006_add_work_template_seed_key](modules/20260508_0006_add_work_template_seed_key.md)
36. [20260509_0007_create_label_groups](modules/20260509_0007_create_label_groups.md)
37. [20260509_0008_create_saved_views](modules/20260509_0008_create_saved_views.md)
38. [20260509_0009_add_saved_view_seed_key](modules/20260509_0009_add_saved_view_seed_key.md)
39. [20260509_0010_create_project_updates](modules/20260509_0010_create_project_updates.md)
40. [20260509_0011_create_project_milestones](modules/20260509_0011_create_project_milestones.md)
41. [20260509_0012_link_tasks_milestones](modules/20260509_0012_link_tasks_milestones.md)
42. [20260509_0013_create_initiatives](modules/20260509_0013_create_initiatives.md)
43. [20260509_0014_create_external_links](modules/20260509_0014_create_external_links.md)
44. [20260509_0015_create_github_status_automation_rules](modules/20260509_0015_create_github_status_automation_rules.md)
45. [20260509_0016_create_releases](modules/20260509_0016_create_releases.md)
46. [20260509_0017_create_request_sources](modules/20260509_0017_create_request_sources.md)
47. [20260509_0018_create_triage_classification_suggestions](modules/20260509_0018_create_triage_classification_suggestions.md)
48. [20260509_0019_create_outbound_webhooks](modules/20260509_0019_create_outbound_webhooks.md)
49. [20260509_0020_add_triage_metadata_json](modules/20260509_0020_add_triage_metadata_json.md)
50. [20260510_0021_create_team_member_profiles](modules/20260510_0021_create_team_member_profiles.md)
51. [20260510_0022_create_system_settings](modules/20260510_0022_create_system_settings.md)
52. [20260510_0023_create_user_sessions](modules/20260510_0023_create_user_sessions.md)
53. [20260515_0024_move_portfolio_ownership_to_profiles](modules/20260515_0024_move_portfolio_ownership_to_profiles.md)
54. [20260516_0025_add_project_scope_to_iterations](modules/20260516_0025_add_project_scope_to_iterations.md)
55. [20260709_0026_add_opaque_browser_sessions](modules/20260709_0026_add_opaque_browser_sessions.md)
56. [20260709_0027_add_durable_outbound_delivery_queue](modules/20260709_0027_add_durable_outbound_delivery_queue.md)
57. [20260711_0028_add_agent_skill_control_plane](modules/20260711_0028_add_agent_skill_control_plane.md)
58. [20260718_0029_add_agent_model_catalog](modules/20260718_0029_add_agent_model_catalog.md)
59. [20260718_0030_add_task_routing_assessments](modules/20260718_0030_add_task_routing_assessments.md)
60. [20260718_0031_align_postgresql_types](modules/20260718_0031_align_postgresql_types.md)
61. [20260727_0034_add_agent_run_model_trust](modules/20260727_0034_add_agent_run_model_trust.md)
62. [query_limits](modules/query_limits.md)
63. [runtime_telemetry](modules/runtime_telemetry.md)
64. [database_runtime](modules/database_runtime.md)
65. [maintenance](modules/maintenance.md)
66. [schemas_agent_planning](modules/schemas_agent_planning.md)
67. [agent_skill_bundle](modules/agent_skill_bundle.md)
68. [agent_team_setup](modules/agent_team_setup.md)
69. [schemas_autonomy](modules/schemas_autonomy.md)
70. [schemas_calendar](modules/schemas_calendar.md)
71. [schemas_common](modules/schemas_common.md)
72. [schemas_github](modules/schemas_github.md)
73. [schemas_intake](modules/schemas_intake.md)
74. [schemas_iteration](modules/schemas_iteration.md)
75. [schemas_label](modules/schemas_label.md)
76. [schemas_llm](modules/schemas_llm.md)
77. [schemas_plan_share](modules/schemas_plan_share.md)
78. [schemas_release](modules/schemas_release.md)
79. [schemas_saved_view](modules/schemas_saved_view.md)
80. [schemas_scheduling_rules](modules/schemas_scheduling_rules.md)
81. [schemas_session](modules/schemas_session.md)
82. [snapshot](modules/snapshot.md)
83. [schemas_system_settings](modules/schemas_system_settings.md)
84. [schemas_email_settings](modules/schemas_email_settings.md)
85. [schemas_team](modules/schemas_team.md)
86. [schemas_project](modules/schemas_project.md)
87. [schemas_template](modules/schemas_template.md)
88. [security](modules/security.md)
89. [agent_routing_policy](modules/agent_routing_policy.md)
90. [agent_routing](modules/agent_routing.md)
91. [agent_routing_rollout](modules/agent_routing_rollout.md)
92. [agent_skill_bundle_service](modules/agent_skill_bundle_service.md)
93. [language_service](modules/language_service.md)
94. [scheduling_rules_service](modules/scheduling_rules_service.md)
95. [routers_scheduling_rules](modules/routers_scheduling_rules.md)
96. [upgrade_service](modules/upgrade_service.md)
97. [upgrade](modules/upgrade.md)
98. [sql_semantics](modules/sql_semantics.md)
99. [exceptions](modules/exceptions.md)
100. [text_similarity](modules/text_similarity.md)
101. [time](modules/time.md)
102. [20260718_0032_add_database_migration_gate](modules/20260718_0032_add_database_migration_gate.md)
103. [20260719_0033_add_autonomy_control_plane](modules/20260719_0033_add_autonomy_control_plane.md)
104. [20260728_0035_add_agent_team_setup](modules/20260728_0035_add_agent_team_setup.md)
105. [20260802_0036_add_plan_shares](modules/20260802_0036_add_plan_shares.md)
106. [observability](modules/observability.md)
107. [app_database](modules/app_database.md)
108. [models_agent](modules/models_agent.md)
109. [models_autonomy](modules/models_autonomy.md)
110. [models_calendar](modules/models_calendar.md)
111. [models_database_migration](modules/models_database_migration.md)
112. [models_external_link](modules/models_external_link.md)
113. [models_github](modules/models_github.md)
114. [models_iteration](modules/models_iteration.md)
115. [models_label](modules/models_label.md)
116. [models_outbound_webhook](modules/models_outbound_webhook.md)
117. [models_plan_share](modules/models_plan_share.md)
118. [models_release](modules/models_release.md)
119. [models_project](modules/models_project.md)
120. [models_request_source](modules/models_request_source.md)
121. [models_saved_view](modules/models_saved_view.md)
122. [models_system_settings](modules/models_system_settings.md)
123. [models_task](modules/models_task.md)
124. [task_status_log](modules/task_status_log.md)
125. [team_member](modules/team_member.md)
126. [models_template](modules/models_template.md)
127. [models_triage](modules/models_triage.md)
128. [user_session](modules/user_session.md)
129. [models___init__](modules/models___init__.md)
130. [catalog](modules/catalog.md)
131. [database_migration_canonical](modules/database_migration_canonical.md)
132. [source](modules/source.md)
133. [transfer](modules/transfer.md)
134. [cli_database_migration](modules/cli_database_migration.md)
135. [database_migration___init__](modules/database_migration___init__.md)
136. [migrations_env](modules/migrations_env.md)
137. [agent_profile_catalog_service](modules/agent_profile_catalog_service.md)
138. [calendar_service](modules/calendar_service.md)
139. [calendars](modules/calendars.md)
140. [iteration_service](modules/iteration_service.md)
141. [iterations](modules/iterations.md)
142. [label_service](modules/label_service.md)
143. [labels](modules/labels.md)
144. [saved_view_service](modules/saved_view_service.md)
145. [session_service](modules/session_service.md)
146. [saved_views](modules/saved_views.md)
147. [routers_session](modules/routers_session.md)
148. [task_context_revision_service](modules/task_context_revision_service.md)
149. [team_service](modules/team_service.md)
150. [routers_team](modules/routers_team.md)
151. [assignee_recommendation_service](modules/assignee_recommendation_service.md)
152. [snapshot_service](modules/snapshot_service.md)
153. [plan_share_service](modules/plan_share_service.md)
154. [plan_shares](modules/plan_shares.md)
155. [template_service](modules/template_service.md)
156. [templates](modules/templates.md)
157. [import_parser](modules/import_parser.md)
158. [url_policy](modules/url_policy.md)
159. [schemas_external_link](modules/schemas_external_link.md)
160. [schemas_outbound_webhook](modules/schemas_outbound_webhook.md)
161. [schemas_request_source](modules/schemas_request_source.md)
162. [schemas_task](modules/schemas_task.md)
163. [schemas_gantt](modules/schemas_gantt.md)
164. [schemas_triage](modules/schemas_triage.md)
165. [schemas___init__](modules/schemas___init__.md)
166. [schemas_agent](modules/schemas_agent.md)
167. [agent_readiness](modules/agent_readiness.md)
168. [llm_service](modules/llm_service.md)
169. [system_settings_service](modules/system_settings_service.md)
170. [routers_system_settings](modules/routers_system_settings.md)
171. [email_settings_service](modules/email_settings_service.md)
172. [routers_email_settings](modules/routers_email_settings.md)
173. [notification_service](modules/notification_service.md)
174. [outbound_webhook_service](modules/outbound_webhook_service.md)
175. [worker](modules/worker.md)
176. [outbound_webhooks](modules/outbound_webhooks.md)
177. [external_link_service](modules/external_link_service.md)
178. [github_status_service](modules/github_status_service.md)
179. [request_source_service](modules/request_source_service.md)
180. [request_sources](modules/request_sources.md)
181. [project_service](modules/project_service.md)
182. [task_import_service](modules/task_import_service.md)
183. [task_service](modules/task_service.md)
184. [export](modules/export.md)
185. [snapshots](modules/snapshots.md)
186. [agent_routing_observability](modules/agent_routing_observability.md)
187. [agent_service](modules/agent_service.md)
188. [agent_skill_bundles](modules/agent_skill_bundles.md)
189. [agent_model_catalog_service](modules/agent_model_catalog_service.md)
190. [agent_routing_service](modules/agent_routing_service.md)
191. [agent_team_setup_service](modules/agent_team_setup_service.md)
192. [autonomy_work_package_service](modules/autonomy_work_package_service.md)
193. [github_status_automation_service](modules/github_status_automation_service.md)
194. [release_service](modules/release_service.md)
195. [projects](modules/projects.md)
196. [scheduler_service](modules/scheduler_service.md)
197. [routers_gantt](modules/routers_gantt.md)
198. [routers_llm](modules/routers_llm.md)
199. [agent_planning_service](modules/agent_planning_service.md)
200. [task_bulk_operation_service](modules/task_bulk_operation_service.md)
201. [tasks](modules/tasks.md)
202. [task_status_service](modules/task_status_service.md)
203. [triage_service](modules/triage_service.md)
204. [routers_triage](modules/routers_triage.md)
205. [agent_work_service](modules/agent_work_service.md)
206. [mcp_agent_tools](modules/mcp_agent_tools.md)
207. [mcp_server](modules/mcp_server.md)
208. [routers_agent](modules/routers_agent.md)
209. [routers_agent_planning](modules/routers_agent_planning.md)
210. [agent_catalog](modules/agent_catalog.md)
211. [github_webhook_service](modules/github_webhook_service.md)
212. [routers_github](modules/routers_github.md)
213. [web_intake_service](modules/web_intake_service.md)
214. [routers_intake](modules/routers_intake.md)
215. [app_main](modules/app_main.md)
216. [routers___init__](modules/routers___init__.md)
217. [test_autonomy_foundation](modules/test_autonomy_foundation.md)
218. [test_autonomy_migrations](modules/test_autonomy_migrations.md)
219. [test_server_acceptance](modules/test_server_acceptance.md)
220. [test_work_package_service](modules/test_work_package_service.md)
221. [test_database_configuration](modules/test_database_configuration.md)
222. [test_deployment_topology](modules/test_deployment_topology.md)
223. [test_observability](modules/test_observability.md)
224. [test_postgresql_documentation](modules/test_postgresql_documentation.md)
225. [test_query_boundaries](modules/test_query_boundaries.md)
226. [test_runtime_policy](modules/test_runtime_policy.md)
227. [test_schema_behavior](modules/test_schema_behavior.md)
228. [test_cutover_evidence](modules/test_cutover_evidence.md)
229. [test_postgresql_closeout](modules/test_postgresql_closeout.md)
230. [test_postgresql_transfer](modules/test_postgresql_transfer.md)
231. [test_source_preflight](modules/test_source_preflight.md)
232. [test_transfer_catalog](modules/test_transfer_catalog.md)
233. [postgresql_migrations_env](modules/postgresql_migrations_env.md)
234. [0001_wave0_probe](modules/0001_wave0_probe.md)
235. [test_load_seed_postgresql](modules/test_load_seed_postgresql.md)
236. [test_load_tooling](modules/test_load_tooling.md)
237. [support_database](modules/support_database.md)
238. [factories](modules/factories.md)
239. [faults](modules/faults.md)
240. [schema](modules/schema.md)
241. [support___init__](modules/support___init__.md)
242. [conftest](modules/conftest.md)
243. [test_postgresql_concurrency](modules/test_postgresql_concurrency.md)
244. [test_postgresql_migrations](modules/test_postgresql_migrations.md)
245. [test_sqlite_migrations](modules/test_sqlite_migrations.md)
246. [test_agent_model_catalog_api](modules/test_agent_model_catalog_api.md)
247. [test_agent_routing_contract](modules/test_agent_routing_contract.md)
248. [test_agent_routing_data](modules/test_agent_routing_data.md)
249. [test_agent_routing_harness](modules/test_agent_routing_harness.md)
250. [test_agent_routing_history_surfaces](modules/test_agent_routing_history_surfaces.md)
251. [test_agent_routing_migrations](modules/test_agent_routing_migrations.md)
252. [test_agent_routing_observability](modules/test_agent_routing_observability.md)
253. [test_agent_routing_rollout](modules/test_agent_routing_rollout.md)
254. [test_agent_routing_service](modules/test_agent_routing_service.md)
255. [test_agent_routing_wave3_contract](modules/test_agent_routing_wave3_contract.md)
256. [test_agent_routing_wave6_qualification](modules/test_agent_routing_wave6_qualification.md)
257. [test_agent_run_trust_compatibility](modules/test_agent_run_trust_compatibility.md)
258. [test_agent_skill_routing_guidance](modules/test_agent_skill_routing_guidance.md)
259. [test_agent_team_setup](modules/test_agent_team_setup.md)
260. [test_agent_team_setup_cli](modules/test_agent_team_setup_cli.md)
261. [test_agent_team_setup_qualification](modules/test_agent_team_setup_qualification.md)
262. [test_agent_work_routing_lineage](modules/test_agent_work_routing_lineage.md)
263. [test_capacity_contract](modules/test_capacity_contract.md)
264. [test_database_harness](modules/test_database_harness.md)
265. [test_plan_shares](modules/test_plan_shares.md)
266. [test_postgresql_lifecycle](modules/test_postgresql_lifecycle.md)
267. [test_process_roles](modules/test_process_roles.md)
268. [test_runtime_boundaries](modules/test_runtime_boundaries.md)
269. [test_saved_view_service](modules/test_saved_view_service.md)
270. [eslint.config](modules/eslint.config.md)
271. [postcss.config](modules/postcss.config.md)
272. [Button](modules/Button.md)
273. [Button.test](modules/Button.test.md)
274. [Checkbox](modules/Checkbox.md)
275. [CollapsibleSection](modules/CollapsibleSection.md)
276. [Input](modules/Input.md)
277. [Input.test](modules/Input.test.md)
278. [dialogLayer](modules/dialogLayer.md)
279. [FullscreenWorkspace](modules/FullscreenWorkspace.md)
280. [Modal](modules/Modal.md)
281. [ConfirmDialog](modules/ConfirmDialog.md)
282. [useConfirmDialog](modules/useConfirmDialog.md)
283. [toast](modules/toast.md)
284. [ToastProvider](modules/ToastProvider.md)
285. [Breadcrumbs](modules/Breadcrumbs.md)
286. [RouteErrorBoundary](modules/RouteErrorBoundary.md)
287. [commandMenuEvents](modules/commandMenuEvents.md)
288. [SettingsGoalHelpContent](modules/SettingsGoalHelpContent.md)
289. [SortableTaskItem](modules/SortableTaskItem.md)
290. [InlineEmptyState](modules/InlineEmptyState.md)
291. [MasterProgress](modules/MasterProgress.md)
292. [MasterProgress.test](modules/MasterProgress.test.md)
293. [OverflowMenu](modules/OverflowMenu.md)
294. [PageLayout](modules/PageLayout.md)
295. [SectionCard](modules/SectionCard.md)
296. [SlideOverDrawer](modules/SlideOverDrawer.md)
297. [PlanningWorkflowGuide](modules/PlanningWorkflowGuide.md)
298. [TaskWorkflowGuide](modules/TaskWorkflowGuide.md)
299. [StickyRail](modules/StickyRail.md)
300. [index](modules/index.md)
301. [overviewTaskThread](modules/overviewTaskThread.md)
302. [OverviewTaskReturnBar](modules/OverviewTaskReturnBar.md)
303. [planningReturn](modules/planningReturn.md)
304. [PlanReturnBar](modules/PlanReturnBar.md)
305. [PlanningWorkbenchFrame](modules/PlanningWorkbenchFrame.md)
306. [resources.en](modules/resources.en.md)
307. [i18n](modules/i18n.md)
308. [dateLocale](modules/dateLocale.md)
309. [InteractiveCalendar](modules/InteractiveCalendar.md)
310. [resources.ru](modules/resources.ru.md)
311. [i18n.test](modules/i18n.test.md)
312. [routeModules](modules/routeModules.md)
313. [DocumentMetadata](modules/DocumentMetadata.md)
314. [workspaces](modules/workspaces.md)
315. [helpContexts](modules/helpContexts.md)
316. [workspaces.test](modules/workspaces.test.md)
317. [LandingPage](modules/LandingPage.md)
318. [NotFoundPage](modules/NotFoundPage.md)
319. [healthService](modules/healthService.md)
320. [SystemHealthPanel](modules/SystemHealthPanel.md)
321. [iterationStore](modules/iterationStore.md)
322. [themeStore](modules/themeStore.md)
323. [planning-masters.test](modules/planning-masters.test.md)
324. [accessibilityInvariants](modules/accessibilityInvariants.md)
325. [accessibilityInvariants.test](modules/accessibilityInvariants.test.md)
326. [renderWithProviders](modules/renderWithProviders.md)
327. [PlanReturnBar.test](modules/PlanReturnBar.test.md)
328. [PlanningWorkbenchFrame.test](modules/PlanningWorkbenchFrame.test.md)
329. [PlanningWorkflowGuide.test](modules/PlanningWorkflowGuide.test.md)
330. [OverflowMenu.test](modules/OverflowMenu.test.md)
331. [renderWithProviders.test](modules/renderWithProviders.test.md)
332. [setup](modules/setup.md)
333. [types_calendar](modules/types_calendar.md)
334. [types_iteration](modules/types_iteration.md)
335. [types_label](modules/types_label.md)
336. [outboundWebhook](modules/outboundWebhook.md)
337. [requestSource](modules/requestSource.md)
338. [savedView](modules/savedView.md)
339. [schedulingRules](modules/schedulingRules.md)
340. [ConstraintsPanel](modules/ConstraintsPanel.md)
341. [schedulingDisplay](modules/schedulingDisplay.md)
342. [EffortModifierCard](modules/EffortModifierCard.md)
343. [EffortModifierCard.test](modules/EffortModifierCard.test.md)
344. [SchedulingPassCard](modules/SchedulingPassCard.md)
345. [systemSettings](modules/systemSettings.md)
346. [emailSettings](modules/emailSettings.md)
347. [types_team](modules/types_team.md)
348. [types_task](modules/types_task.md)
349. [types_triage](modules/types_triage.md)
350. [KanbanCard](modules/KanbanCard.md)
351. [TaskAgentReadinessBadge](modules/TaskAgentReadinessBadge.md)
352. [TaskAgentReadinessBadge.test](modules/TaskAgentReadinessBadge.test.md)
353. [tone](modules/tone.md)
354. [KanbanColumn](modules/KanbanColumn.md)
355. [Pill](modules/Pill.md)
356. [StatusSegmentStrip](modules/StatusSegmentStrip.md)
357. [tone.test](modules/tone.test.md)
358. [attentionRanking](modules/attentionRanking.md)
359. [attentionRanking.test](modules/attentionRanking.test.md)
360. [planningTaskIssues](modules/planningTaskIssues.md)
361. [planningMasters_masters](modules/planningMasters_masters.md)
362. [planningMasters_masters.test](modules/planningMasters_masters.test.md)
363. [planningTaskIssues.test](modules/planningTaskIssues.test.md)
364. [types_agent](modules/types_agent.md)
365. [agentTeamSetup_manifest](modules/agentTeamSetup_manifest.md)
366. [agentTeamSetup_masters](modules/agentTeamSetup_masters.md)
367. [agentTeamSetup_masters.test](modules/agentTeamSetup_masters.test.md)
368. [statusScopes](modules/statusScopes.md)
369. [statusScopes.test](modules/statusScopes.test.md)
370. [modelAwareRouting](modules/modelAwareRouting.md)
371. [types_gantt](modules/types_gantt.md)
372. [types_github](modules/types_github.md)
373. [types_project](modules/types_project.md)
374. [projectStatusStyles](modules/projectStatusStyles.md)
375. [projectStatusStyles.test](modules/projectStatusStyles.test.md)
376. [types_release](modules/types_release.md)
377. [types_template](modules/types_template.md)
378. [seedDisplay](modules/seedDisplay.md)
379. [agentAccess](modules/agentAccess.md)
380. [useAgentAccess](modules/useAgentAccess.md)
381. [apiError](modules/apiError.md)
382. [QueryState](modules/QueryState.md)
383. [taskEditorContract](modules/taskEditorContract.md)
384. [adminAccess](modules/adminAccess.md)
385. [useAdminAccess](modules/useAdminAccess.md)
386. [AdminAccessPanel](modules/AdminAccessPanel.md)
387. [AdminAccessGate](modules/AdminAccessGate.md)
388. [AdminAccessPanel.test](modules/AdminAccessPanel.test.md)
389. [api](modules/api.md)
390. [agentService](modules/agentService.md)
391. [useAgentTeamReadiness](modules/useAgentTeamReadiness.md)
392. [agentService.test](modules/agentService.test.md)
393. [calendarService](modules/calendarService.md)
394. [emailSettingsService](modules/emailSettingsService.md)
395. [exportService](modules/exportService.md)
396. [ganttService](modules/ganttService.md)
397. [githubService](modules/githubService.md)
398. [GitHubSettingsPanel](modules/GitHubSettingsPanel.md)
399. [GitHubSettingsPanel.test](modules/GitHubSettingsPanel.test.md)
400. [iterationService](modules/iterationService.md)
401. [IterationSelector](modules/IterationSelector.md)
402. [usePlanningNavigationSummary](modules/usePlanningNavigationSummary.md)
403. [SidebarIterationCard](modules/SidebarIterationCard.md)
404. [SidebarIterationCard.test](modules/SidebarIterationCard.test.md)
405. [planningNavigationInvalidation](modules/planningNavigationInvalidation.md)
406. [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md)
407. [labelService](modules/labelService.md)
408. [LabelSelector](modules/LabelSelector.md)
409. [outboundWebhookService](modules/outboundWebhookService.md)
410. [planShareService](modules/planShareService.md)
411. [projectService](modules/projectService.md)
412. [releaseService](modules/releaseService.md)
413. [ReleaseForm](modules/ReleaseForm.md)
414. [requestSourceService](modules/requestSourceService.md)
415. [savedViewService](modules/savedViewService.md)
416. [SavedViewDashboardCards](modules/SavedViewDashboardCards.md)
417. [AppSidebar](modules/AppSidebar.md)
418. [AppSidebar.test](modules/AppSidebar.test.md)
419. [schedulingRulesService](modules/schedulingRulesService.md)
420. [sessionService](modules/sessionService.md)
421. [UserSessionBadge](modules/UserSessionBadge.md)
422. [UserSessionBadge.test](modules/UserSessionBadge.test.md)
423. [snapshotService](modules/snapshotService.md)
424. [systemSettingsService](modules/systemSettingsService.md)
425. [InterfaceLanguageSettings](modules/InterfaceLanguageSettings.md)
426. [SystemLanguageProvider](modules/SystemLanguageProvider.md)
427. [taskService](modules/taskService.md)
428. [ImportTasksModal](modules/ImportTasksModal.md)
429. [TaskDependencySelector](modules/TaskDependencySelector.md)
430. [TaskTextEditorModal](modules/TaskTextEditorModal.md)
431. [teamService](modules/teamService.md)
432. [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md)
433. [TaskFiltersBar](modules/TaskFiltersBar.md)
434. [taskFilterDefaults](modules/taskFilterDefaults.md)
435. [ImportTeamModal](modules/ImportTeamModal.md)
436. [ImportTeamModal.test](modules/ImportTeamModal.test.md)
437. [TeamForm](modules/TeamForm.md)
438. [TeamForm.test](modules/TeamForm.test.md)
439. [TeamProfileManager](modules/TeamProfileManager.md)
440. [TeamProfileManager.test](modules/TeamProfileManager.test.md)
441. [CalendarPage](modules/CalendarPage.md)
442. [templateService](modules/templateService.md)
443. [TemplateLabelSettings](modules/TemplateLabelSettings.md)
444. [TemplateLabelSettings.test](modules/TemplateLabelSettings.test.md)
445. [triageService](modules/triageService.md)
446. [AssigneeRecommendationsPanel](modules/AssigneeRecommendationsPanel.md)
447. [usePlanningReadiness](modules/usePlanningReadiness.md)
448. [usePlanningReadiness.test](modules/usePlanningReadiness.test.md)
449. [copyText](modules/copyText.md)
450. [focusLifecycle](modules/focusLifecycle.md)
451. [focusLifecycle.test](modules/focusLifecycle.test.md)
452. [formatDate](modules/formatDate.md)
453. [TaskStatusFlow](modules/TaskStatusFlow.md)
454. [ScheduleExplanationDetails](modules/ScheduleExplanationDetails.md)
455. [IterationForm](modules/IterationForm.md)
456. [IterationForm.test](modules/IterationForm.test.md)
457. [IterationList](modules/IterationList.md)
458. [NotificationsPanel](modules/NotificationsPanel.md)
459. [ProjectIterationsSection](modules/ProjectIterationsSection.md)
460. [ProjectTaskTree](modules/ProjectTaskTree.md)
461. [StatusChangeControl](modules/StatusChangeControl.md)
462. [VacationManager](modules/VacationManager.md)
463. [TeamList](modules/TeamList.md)
464. [AgentTeamSetupMasterPage](modules/AgentTeamSetupMasterPage.md)
465. [AgentTeamSetupMasterPage.test](modules/AgentTeamSetupMasterPage.test.md)
466. [AnalyticsPage](modules/AnalyticsPage.md)
467. [IterationsPage](modules/IterationsPage.md)
468. [PlanMasterPage](modules/PlanMasterPage.md)
469. [PlanMasterPage.test](modules/PlanMasterPage.test.md)
470. [PlanPage](modules/PlanPage.md)
471. [PlanPage.test](modules/PlanPage.test.md)
472. [PlanSharePage](modules/PlanSharePage.md)
473. [PlanSharePage.test](modules/PlanSharePage.test.md)
474. [ProjectReleaseDetailPage](modules/ProjectReleaseDetailPage.md)
475. [TeamPage](modules/TeamPage.md)
476. [modelRouting](modules/modelRouting.md)
477. [RoutingCandidateComparison](modules/RoutingCandidateComparison.md)
478. [RoutingCandidateComparison.test](modules/RoutingCandidateComparison.test.md)
479. [modelRouting.test](modules/modelRouting.test.md)
480. [protectedQueries](modules/protectedQueries.md)
481. [TaskRoutingPanel](modules/TaskRoutingPanel.md)
482. [TaskRoutingPanel.test](modules/TaskRoutingPanel.test.md)
483. [AgentAccessPanel](modules/AgentAccessPanel.md)
484. [AgentAccessPanel.test](modules/AgentAccessPanel.test.md)
485. [AgentModelAdministration](modules/AgentModelAdministration.md)
486. [AgentModelAdministration.test](modules/AgentModelAdministration.test.md)
487. [EmailSettingsPanel](modules/EmailSettingsPanel.md)
488. [EmailSettingsPanel.test](modules/EmailSettingsPanel.test.md)
489. [OutboundWebhooksPanel](modules/OutboundWebhooksPanel.md)
490. [OutboundWebhooksPanel.test](modules/OutboundWebhooksPanel.test.md)
491. [RuntimeConfigSettings](modules/RuntimeConfigSettings.md)
492. [RuntimeConfigSettings.test](modules/RuntimeConfigSettings.test.md)
493. [SchedulingRulesSettings](modules/SchedulingRulesSettings.md)
494. [SchedulingRulesSettings.test](modules/SchedulingRulesSettings.test.md)
495. [AgentPipelinePage](modules/AgentPipelinePage.md)
496. [AgentPipelinePage.test](modules/AgentPipelinePage.test.md)
497. [safeUrl](modules/safeUrl.md)
498. [RequestSourceLinksPanel](modules/RequestSourceLinksPanel.md)
499. [RequestSourceLinksPanel.test](modules/RequestSourceLinksPanel.test.md)
500. [TaskTimelinePanel](modules/TaskTimelinePanel.md)
501. [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md)
502. [selectWorkNowTasks](modules/selectWorkNowTasks.md)
503. [OverviewPage](modules/OverviewPage.md)
504. [OverviewPage.test](modules/OverviewPage.test.md)
505. [singleKeyShortcutPreference](modules/singleKeyShortcutPreference.md)
506. [useSingleKeyShortcutPreference](modules/useSingleKeyShortcutPreference.md)
507. [CommandMenu](modules/CommandMenu.md)
508. [CommandMenu.test](modules/CommandMenu.test.md)
509. [ContextHelp](modules/ContextHelp.md)
510. [AppTopNav](modules/AppTopNav.md)
511. [AppShell](modules/AppShell.md)
512. [App](modules/App.md)
513. [AppShell.test](modules/AppShell.test.md)
514. [AppTopNav.test](modules/AppTopNav.test.md)
515. [ContextHelp.test](modules/ContextHelp.test.md)
516. [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md)
517. [src_main](modules/src_main.md)
518. [SettingsPage](modules/SettingsPage.md)
519. [SettingsPage.test](modules/SettingsPage.test.md)
520. [taskFilters](modules/taskFilters.md)
521. [KanbanBoard](modules/KanbanBoard.md)
522. [KanbanBoard.test](modules/KanbanBoard.test.md)
523. [taskFilters.test](modules/taskFilters.test.md)
524. [teamMemberLabels](modules/teamMemberLabels.md)
525. [InitiativeForm](modules/InitiativeForm.md)
526. [RoadmapPage](modules/RoadmapPage.md)
527. [RoadmapPage.test](modules/RoadmapPage.test.md)
528. [templateDefaults](modules/templateDefaults.md)
529. [ProjectForm](modules/ProjectForm.md)
530. [TaskForm](modules/TaskForm.md)
531. [TaskEditModal](modules/TaskEditModal.md)
532. [GanttChart](modules/GanttChart.md)
533. [GanttChart.test](modules/GanttChart.test.md)
534. [TaskEditorDrawer](modules/TaskEditorDrawer.md)
535. [TaskList](modules/TaskList.md)
536. [SavedViewsControl](modules/SavedViewsControl.md)
537. [TaskList.test](modules/TaskList.test.md)
538. [GanttPage](modules/GanttPage.md)
539. [GanttPage.test](modules/GanttPage.test.md)
540. [ProjectDetailPage](modules/ProjectDetailPage.md)
541. [ProjectsPage](modules/ProjectsPage.md)
542. [ProjectsPage.test](modules/ProjectsPage.test.md)
543. [TasksPage](modules/TasksPage.md)
544. [TasksPage.test](modules/TasksPage.test.md)
545. [TriagePage](modules/TriagePage.md)
546. [tailwind.config](modules/tailwind.config.md)
547. [vite.config](modules/vite.config.md)
548. [vitest.config](modules/vitest.config.md)
549. [create_agent_actor](modules/create_agent_actor.md)
550. [generate_workchord_keys](modules/generate_workchord_keys.md)
551. [setup_agent_team](modules/setup_agent_team.md)
552. [build_agent_skills](modules/build_agent_skills.md)
553. [check_model_aware_routing_closeout](modules/check_model_aware_routing_closeout.md)
554. [check_postgresql_documentation](modules/check_postgresql_documentation.md)
555. [installed_wheel_postgresql_qualification](modules/installed_wheel_postgresql_qualification.md)
556. [generate_agent_team_contract](modules/generate_agent_team_contract.md)
557. [generate_agent_team_report_contract](modules/generate_agent_team_report_contract.md)
558. [load_common](modules/load_common.md)
559. [collect](modules/collect.md)
560. [result](modules/result.md)
561. [compare](modules/compare.md)
562. [finalize](modules/finalize.md)
563. [qualify](modules/qualify.md)
564. [resilience](modules/resilience.md)
565. [run](modules/run.md)
566. [seal](modules/seal.md)
567. [seed](modules/seed.md)

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
| [app_main](modules/app_main.md) | `settings = get_settings`, `app = FastAPI`, `app.add_middleware`, `app.add_middleware`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `app.include_router`, `mount_mcp_http` |
| [maintenance](modules/maintenance.md) | `SAFE_HTTP_METHODS = frozenset`, `_CORRELATION_ID_PATTERN = re.compile` |
| [mcp_agent_tools](modules/mcp_agent_tools.md) | `_AGENT_ASSIGNMENT_CREATE_ADAPTER = TypeAdapter`, `_AGENT_ASSIGNMENT_UPDATE_ADAPTER = TypeAdapter`, `_AGENT_WORK_BEGIN_ADAPTER = TypeAdapter` |
| [mcp_server](modules/mcp_server.md) | `_http_agent_key = ContextVar`, `mcp = create_mcp_server` |
| [migrations_env](modules/migrations_env.md) | `settings = get_settings`, `database_configuration = parse_database_configuration`, `config.set_main_option`, `fileConfig`, `run_migrations_offline`, `run_migrations_online` |
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
| [TaskBulkOperationsPanel](modules/TaskBulkOperationsPanel.md) | `t = bind` |
| [TaskDependencySelector](modules/TaskDependencySelector.md) | `t = bind` |
| [TaskList.test](modules/TaskList.test.md) | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel.test](modules/TaskTimelinePanel.test.md) | `taskServiceMock = hoisted`, `mock`, `mock`, `describe` |
| [TaskTimelinePanel](modules/TaskTimelinePanel.md) | `t = bind` |
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
| [attentionRanking.test](modules/attentionRanking.test.md) | `describe`, `describe` |
| [planningMasters_masters.test](modules/planningMasters_masters.test.md) | `describe` |
| [planningNavigationInvalidation.test](modules/planningNavigationInvalidation.test.md) | `describe` |
| [planningNavigationInvalidation](modules/planningNavigationInvalidation.md) | `READINESS_INPUT_QUERY_ROOTS = Set` |
| [planningTaskIssues.test](modules/planningTaskIssues.test.md) | `describe` |
| [usePlanningReadiness.test](modules/usePlanningReadiness.test.md) | `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `describe` |
| [useSingleKeyShortcutPreference.test](modules/useSingleKeyShortcutPreference.test.md) | `describe` |
| [i18n.test](modules/i18n.test.md) | `describe` |
| [src_main](modules/src_main.md) | `queryClient = QueryClient`, `installPlanningNavigationInvalidation`, `render` |
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
| [api](modules/api.md) | `api = create`, `use` |
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
| [build_agent_skills](modules/build_agent_skills.md) | `SEMVER_RE = re.compile`, `SKILL_NAME_RE = re.compile`, `COMPATIBILITY_RE = re.compile`, `MARKDOWN_LINK_RE = re.compile`, `URL_RE = re.compile` |
| [check_postgresql_documentation](modules/check_postgresql_documentation.md) | `LINK_PATTERN = re.compile`, `SHELL_FENCE_PATTERN = re.compile`, `LIVE_SQLITE_COPY_PATTERN = re.compile` |
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
