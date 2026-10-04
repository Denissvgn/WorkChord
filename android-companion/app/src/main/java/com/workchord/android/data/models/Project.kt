package com.workchord.android.data.models

import com.google.gson.annotations.SerializedName

data class Project(
    @SerializedName("id")
    val id: Int,
    @SerializedName("name")
    val name: String,
    @SerializedName("description")
    val description: String? = null,
    @SerializedName("status")
    val status: String? = null,
    @SerializedName("health")
    val health: String? = null
)

data class Iteration(
    @SerializedName("id")
    val id: Int,
    @SerializedName("name")
    val name: String,
    @SerializedName("project_id")
    val projectId: Int? = null,
    @SerializedName("project")
    val project: Project? = null,
    @SerializedName("start_date")
    val startDate: String? = null,
    @SerializedName("end_date")
    val endDate: String? = null,
    @SerializedName("working_days")
    val workingDays: Int? = null
)
