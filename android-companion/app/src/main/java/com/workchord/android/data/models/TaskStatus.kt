package com.workchord.android.data.models

import com.google.gson.annotations.SerializedName

enum class TaskStatus(val value: String, val displayName: String) {
    @SerializedName("planned")
    PLANNED("planned", "Planned"),

    @SerializedName("active")
    ACTIVE("active", "Active"),

    @SerializedName("resolved")
    RESOLVED("resolved", "Resolved"),

    @SerializedName("closed")
    CLOSED("closed", "Closed"),

    @SerializedName("blocked")
    BLOCKED("blocked", "Blocked");

    companion object {
        fun fromString(value: String?): TaskStatus {
            return entries.firstOrNull { it.value.equals(value, ignoreCase = true) } ?: PLANNED
        }
    }
}
