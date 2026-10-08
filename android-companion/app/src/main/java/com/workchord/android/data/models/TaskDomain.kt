package com.workchord.android.data.models

import com.google.gson.annotations.SerializedName

data class TaskBrief(@SerializedName("schema_version") val schemaVersion: Int? = null,
    val goal: String? = null, val context: String? = null, val scope: String? = null, val exclusions: String? = null,
    @SerializedName("acceptance_criteria") val acceptanceCriteria: List<BriefCriterion>? = null,
    val verification: String? = null, @SerializedName("artifact_expectations") val artifactExpectations: String? = null)

data class BriefCriterion(val id: String, val revision: Int, val text: String, val verification: String? = null)
data class CriterionProgress(@SerializedName("criterion_id") val criterionId: String,
    @SerializedName("criterion_revision") val criterionRevision: Int, val state: String, val evidence: String? = null)
data class TaskProgress(val criteria: List<CriterionProgress>? = null, val artifacts: List<String>? = null,
    @SerializedName("brief_revision") val briefRevision: Int? = null,
    @SerializedName("artifact_revision") val artifactRevision: Int? = null)
data class ProgressRequest(@SerializedName("expected_version") val expectedVersion: Int,
    val criteria: List<CriterionProgress>, val artifacts: List<String> = emptyList())
data class ReviewRequest(@SerializedName("expected_version") val expectedVersion: Int,
    @SerializedName("brief_revision") val briefRevision: Int, @SerializedName("artifact_revision") val artifactRevision: Int,
    val verdict: String, val reason: String, val evidence: String)
data class TaskReview(val id: Int, @SerializedName("task_version") val taskVersion: Int,
    @SerializedName("brief_revision") val briefRevision: Int, @SerializedName("artifact_revision") val artifactRevision: Int,
    @SerializedName("principal_id") val principalId: Int?, val verdict: String, val reason: String, val evidence: String,
    @SerializedName("created_at") val createdAt: String)
data class CurrentTaskReview(@SerializedName("task_version") val taskVersion: Int, val review: TaskReview?)

data class ActionBlocker(val code: String, val message: String)
data class AllowedAction(val action: String, val allowed: Boolean, val blockers: List<ActionBlocker>? = null)
data class TaskActions(@SerializedName("task_id") val taskId: Int, val version: Int,
    val actions: List<AllowedAction>?, @SerializedName("claim_generation") val claimGeneration: Int? = null,
    @SerializedName("running_run_ids") val runningRunIds: List<Int>? = null,
    @SerializedName("live_assignment_ids") val liveAssignmentIds: List<Int>? = null)
data class TaskCommandRequest(val action: String, @SerializedName("expected_version") val expectedVersion: Int,
    val reason: String, @SerializedName("expected_claim_generation") val expectedClaimGeneration: Int? = null,
    @SerializedName("expected_running_run_ids") val expectedRunningRunIds: List<Int> = emptyList(),
    @SerializedName("expected_live_assignment_ids") val expectedLiveAssignmentIds: List<Int> = emptyList())

data class DomainCapabilities(@SerializedName("schema_version") val schemaVersion: Int? = null,
    val ready: Boolean? = null, val features: List<String>? = null, val reason: String? = null,
    @SerializedName("legacy_task_versions_required") val legacyTaskVersionsRequired: Boolean? = null,
    @SerializedName("current_review_projection") val currentReviewProjection: Boolean? = null) {
    fun supports(feature: String) = schemaVersion == 1 && ready == true && features?.contains(feature) == true
}

data class TaskReference(val id: Int, val title: String, val version: Int?, val status: String?,
    @SerializedName("project_id") val projectId: Int?, @SerializedName("iteration_id") val iterationId: Int?,
    @SerializedName("parent_id") val parentId: Int?, @SerializedName("owner_profile_id") val ownerProfileId: Int?,
    @SerializedName("project_name") val projectName: String? = null,
    @SerializedName("iteration_name") val iterationName: String? = null,
    @SerializedName("blocked_reason") val blockedReason: String? = null,
    @SerializedName("canceled_at") val canceledAt: String? = null,
    @SerializedName("acceptance_current") val acceptanceCurrent: Boolean? = null,
    val actions: List<AllowedAction>? = null)
data class TaskReferencePage(val items: List<TaskReference>?, @SerializedName("has_more") val hasMore: Boolean?,
    @SerializedName("next_after_id") val nextAfterId: Int?, val limit: Int? = null, val consistency: String? = null)
data class TaskDetail(val task: Task, val ancestors: List<TaskReference>?,
    @SerializedName("ancestors_complete") val ancestorsComplete: Boolean?,
    val children: TaskReferencePage, val dependencies: TaskReferencePage,
    @SerializedName("execution_context_complete") val executionContextComplete: Boolean?)
data class HumanWork(val state: String?, val queues: Map<String, List<TaskReference>>?,
    @SerializedName("has_more") val hasMore: Boolean?, @SerializedName("next_after_id") val nextAfterId: Int?)


val companionTaskCommands = setOf("start_manual", "resolve_manual", "block", "unblock", "cancel", "reopen")
