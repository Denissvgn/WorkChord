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
    @SerializedName("status")
    val statusRaw: String = "planned",
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
    val tags: List<String> = emptyList(),
    @SerializedName("version")
    val version: Int = 1,
    @SerializedName("dependencies")
    val dependencies: List<Int> = emptyList(),
    @SerializedName("updated_at")
    val updatedAt: String? = null
) {
    val status: TaskStatus
        get() = TaskStatus.fromString(statusRaw)

    /**
     * Extracts acceptance criteria checklist items from markdown description.
     */
    fun extractAcceptanceCriteria(): List<AcceptanceCriterion> {
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
                    criteria.add(AcceptanceCriterion(trimmed.removePrefix("- [x]").removePrefix("- [X]").trim(), isCompleted = true))
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
    val isCompleted: Boolean = false
)
