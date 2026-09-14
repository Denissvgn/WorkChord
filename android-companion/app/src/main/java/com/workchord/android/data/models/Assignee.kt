package com.workchord.android.data.models

import com.google.gson.annotations.SerializedName

data class Assignee(
    @SerializedName("id")
    val id: Int,
    @SerializedName("name")
    val name: String,
    @SerializedName("email")
    val email: String? = null,
    @SerializedName("role")
    val role: String? = null
)
