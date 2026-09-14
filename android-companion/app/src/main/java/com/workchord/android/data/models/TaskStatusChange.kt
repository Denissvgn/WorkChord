package com.workchord.android.data.models

import com.google.gson.annotations.SerializedName

data class TaskStatusChangeRequest(
    @SerializedName("status")
    val status: String,
    @SerializedName("reason")
    val reason: String? = null,
    @SerializedName("expected_version")
    val expectedVersion: Int? = null
)

data class CascadeUpdateInfo(
    @SerializedName("task_id")
    val taskId: Int,
    @SerializedName("task_title")
    val taskTitle: String? = null,
    @SerializedName("old_start_date")
    val oldStartDate: String? = null,
    @SerializedName("new_start_date")
    val newStartDate: String? = null,
    @SerializedName("old_end_date")
    val oldEndDate: String? = null,
    @SerializedName("new_end_date")
    val newEndDate: String? = null
)

data class TaskStatusChangeResponse(
    @SerializedName("task")
    val task: Task,
    @SerializedName("cascade_updates")
    val cascadeUpdates: List<CascadeUpdateInfo> = emptyList(),
    @SerializedName("notifications_sent")
    val notificationsSent: Boolean = false
)

data class TaskUpdateRequest(
    @SerializedName("title")
    val title: String? = null,
    @SerializedName("description")
    val description: String? = null,
    @SerializedName("priority")
    val priority: Int? = null,
    @SerializedName("effort_hours")
    val effortHours: Double? = null,
    @SerializedName("assignee_id")
    val assigneeId: Int? = null,
    @SerializedName("expected_version")
    val expectedVersion: Int? = null
)
