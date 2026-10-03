package com.workchord.android.data.models

import com.google.gson.annotations.SerializedName

data class Task(
    @SerializedName("id")
    val id: Int,
    @SerializedName("iteration_id")
    val iterationId: Int? = null,
    @SerializedName("project_id")
    val projectId: Int? = null,
    @SerializedName("milestone_id")
    val milestoneId: Int? = null,
    @SerializedName("parent_id")
    val parentId: Int? = null,
    @SerializedName("title")
    val title: String,
    @SerializedName("description")
    val description: String? = null,
    @SerializedName("priority")
    val priority: Int = 5,
    @SerializedName("effort_days")
    val effortDays: Double? = null,
    @SerializedName("effort_hours")
    val effortHours: Double? = null,
    @SerializedName("project")
    val project: Project? = null,
    @SerializedName("assignee")
    val assignee: Assignee? = null,
    @SerializedName("owner_profile_id")
    val ownerProfileId: Int? = null,
    @SerializedName("children")
    val children: List<Task>? = null,
    @SerializedName("is_composite")
    val isComposite: Boolean = false,
    @SerializedName("canceled_at")
    val canceledAt: String? = null,
    @SerializedName("blocked_reason") val blockedReason: String? = null,
    @SerializedName("canceled_reason") val canceledReason: String? = null,
    @SerializedName("iteration_revision") val iterationRevision: Int? = null,
    @SerializedName("nominal_day_hours") val nominalDayHours: Double? = null,
    @SerializedName("estimate_provenance") val estimateProvenance: String? = null,
    @SerializedName("ownership_provenance") val ownershipProvenance: String? = null,
    @SerializedName("execution_mode") val executionMode: String? = null,
    val owner: Assignee? = null,
    val brief: TaskBrief? = null,
    @SerializedName("brief_revision") val briefRevision: Int? = null,
    @SerializedName("artifact_revision") val artifactRevision: Int? = null,
    val progress: TaskProgress? = null,
    @SerializedName("accepted_at") val acceptedAt: String? = null,
    @SerializedName("baseline_start_date") val baselineStartDate: String? = null,
    @SerializedName("baseline_end_date") val baselineEndDate: String? = null,
    @SerializedName("started_at") val startedAt: String? = null,
    @SerializedName("resolved_at") val resolvedAt: String? = null,
    @SerializedName("status")
    val statusRaw: String = "unknown",
    @SerializedName("start_date")
    val startDate: String? = null,
    @SerializedName("end_date")
    val endDate: String? = null,
    @SerializedName("actual_start_date")
    val actualStartDate: String? = null,
    @SerializedName("actual_end_date")
    val actualEndDate: String? = null,
    @SerializedName("is_overdue")
    val isOverdue: Boolean = false,
    @SerializedName("is_delayed")
    val isDelayed: Boolean = false,
    @SerializedName("tags")
    val tags: List<String>? = null,
    @SerializedName("version")
    val version: Int? = null,
    @SerializedName("dependencies")
    val dependencies: List<Int>? = null,
    @SerializedName("updated_at")
    val updatedAt: String? = null
) {
    val status: TaskStatus
        get() = TaskStatus.fromString(statusRaw)

    val authoritativeVersion: Int? get() = version?.takeIf { it > 0 }

    /**
     * Extracts acceptance criteria checklist items from markdown description.
     */
    fun extractAcceptanceCriteria(): List<AcceptanceCriterion> {
        if (brief != null) {
            if (brief.schemaVersion != 1) return emptyList()
            val currentProgress = progress?.takeIf { briefRevision != null && artifactRevision != null &&
                it.briefRevision == briefRevision && it.artifactRevision == artifactRevision }
            return brief.acceptanceCriteria.orEmpty().map { criterion ->
                val recorded = currentProgress?.criteria.orEmpty().firstOrNull { it.criterionId == criterion.id && it.criterionRevision == criterion.revision }
                AcceptanceCriterion(criterion.text, recorded?.state == "completed" && !recorded.evidence.isNullOrBlank(), criterion.id, criterion.revision,
                    criterion.verification, recorded?.evidence, recorded?.state ?: "pending")
            }
        }
        if (description.isNullOrBlank()) return emptyList()

        val lines = description.lines()
        val criteria = mutableListOf<AcceptanceCriterion>()
        var inAcceptanceSection = false

        for (line in lines) {
            val trimmed = line.trim()
            if (trimmed.startsWith("## Acceptance criteria", ignoreCase = true)) {
                inAcceptanceSection = true
                continue
            } else if (trimmed.startsWith("## ") && inAcceptanceSection) {
                break
            }

            if (inAcceptanceSection) {
                if (trimmed.startsWith("- [x]", ignoreCase = true)) {
                    criteria.add(AcceptanceCriterion(trimmed.removePrefix("- [x]").removePrefix("- [X]").trim()))
                } else if (trimmed.startsWith("- [ ]", ignoreCase = true)) {
                    criteria.add(AcceptanceCriterion(trimmed.removePrefix("- [ ]").trim(), isCompleted = false))
                } else if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
                    criteria.add(AcceptanceCriterion(trimmed.drop(2).trim(), isCompleted = false))
                }
            }
        }
        return criteria
    }

    /**
     * Extracts high level goal/summary from description.
     */
    fun extractGoal(): String? {
        if (brief != null) return brief.goal?.takeIf { brief.schemaVersion == 1 && it.isNotBlank() }
        if (description.isNullOrBlank()) return null
        val lines = description.lines()
        var inGoal = false
        val goalLines = mutableListOf<String>()
        for (line in lines) {
            val trimmed = line.trim()
            if (trimmed.startsWith("## Goal", ignoreCase = true)) {
                inGoal = true
                continue
            } else if (trimmed.startsWith("## ") && inGoal) {
                break
            }
            if (inGoal && trimmed.isNotEmpty()) {
                goalLines.add(trimmed)
            }
        }
        return if (goalLines.isNotEmpty()) goalLines.joinToString(" ") else null
    }
}

data class AcceptanceCriterion(
    val text: String,
    val isCompleted: Boolean = false,
    val id: String? = null,
    val revision: Int? = null,
    val verification: String? = null,
    val evidence: String? = null,
    val state: String = "pending"
)
