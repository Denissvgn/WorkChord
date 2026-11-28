# test_task_routing_consistency Module

**Path:** `backend/tests/test_task_routing_consistency.py`

## Description

A task's first rung, escalation and reviewer stay consistent with its assignee and review policy.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_agent_tools` |
| `app.authority` | `Authority`, `AuthorityError` |
| `app.main` | `app` |
| `app.mcp_server` | `mcp` |
| `app.models.agent` | `AgentActor`, `AgentModelBinding`, `AgentModelCatalogEntry`, `TaskEvent`, `TaskEvent` |
| `app.models.identity` | `Principal` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.services.manual_provenance_service` | `EVENT_TYPE`, `SCHEMA`, `recorded_provenances` |
| `app.services.task_routing_service` | `parse_text_routing` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select`, `update` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_task_routing_consistency.py"]
    n1 --> n0
    click n1 "../modules/test_task_routing_consistency.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_client` | `()` | — | — |
| `routing_scope` | *(async)* `(factory, scenario, *, policy = True, mode = 'refuse')` | — | Two worker rows from two vendors and one verifier per vendor, in the scenario's first iteration. |
| `gpt_routing` | `(profiles)` | — | — |
| `brief` | `(routing = None, **fields)` | — | — |
| `create_task` | *(async)* `(client, scenario, assignee_id, routing, title = 'Routed work')` | — | — |
| `test_routing_is_validated_structure_and_the_brief_renders_it` | *(async)* `(delivery_store)` | — | — |
| `test_reassignment_to_another_vendor_is_refused_with_a_consistent_routing` | *(async)* `(delivery_store)` | — | — |
| `test_warn_mode_saves_the_reassignment_and_answers_with_the_suggestion` | *(async)* `(delivery_store)` | — | — |
| `test_without_the_publisher_policy_only_the_first_rung_must_follow_the_assignee` | *(async)* `(delivery_store)` | — | — |
| `test_bulk_cross_vendor_reassignment_leaves_every_task_consistent` | *(async)* `(delivery_store)` | — | — |
| `write_text_brief` | *(async)* `(client, scenario, members, context = TEXT_CONTEXT, verification = TEXT_VERIFICATION)` | — | — |
| `test_text_routing_converts_without_loss` | *(async)* `(delivery_store)` | — | — |
| `test_conversion_without_routing_text_changes_nothing` | *(async)* `(delivery_store)` | — | — |
| `test_ambiguous_text_routing_stays_as_text_until_the_caller_settles_it` | *(async)* `(delivery_store)` | — | — |
| `test_remaining_routing_text_is_converted_into_an_existing_routing` | *(async)* `(delivery_store)` | — | — |
| `catalog_entries_for_parser` | `(*extra)` | — | — |
| `test_parser_reads_the_inline_ladder_format` | `()` | — | — |
| `test_parser_matches_only_an_exact_key_or_alias_at_its_stated_effort` | `()` | — | — |
| `test_parser_tidies_only_the_line_a_sentence_left` | `()` | — | — |
| `record_manual_provenance` | *(async)* `(factory, task_id, executor)` | — | — |
| `current_provenance` | *(async)* `(factory, task_id)` | — | — |
| `test_routing_changes_keep_progress_and_evidence_of_resolved_work` | *(async)* `(delivery_store)` | — | — |
| `test_routing_changes_clear_acceptance_on_both_write_paths` | *(async)* `(delivery_store)` | — | — |
| `test_empty_routing_is_stored_as_no_routing` | *(async)* `(delivery_store)` | — | — |
| `test_conversion_preview_says_when_applying_resets_progress` | *(async)* `(delivery_store)` | — | — |
| `test_recorded_contributor_publishers_bind_the_reviewer` | *(async)* `(delivery_store)` | — | — |
| `test_reviewer_without_a_verifier_and_disabled_rungs_are_repaired` | *(async)* `(delivery_store)` | — | — |
| `test_suggestion_warns_when_the_new_first_rung_is_weaker` | *(async)* `(delivery_store)` | — | — |
| `test_removing_routing_during_a_reassignment_is_an_issue_under_the_policy` | *(async)* `(delivery_store)` | — | — |
| `test_routing_conflict_mode_is_an_operator_setting` | *(async)* `(delivery_store)` | — | — |
| `test_mcp_tools_check_and_convert_routing` | *(async)* `(delivery_store)` | — | — |
