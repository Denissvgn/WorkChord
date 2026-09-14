package com.workchord.android.data.models

import com.google.gson.annotations.SerializedName

data class Session(
    @SerializedName("id")
    val id: Int,
    @SerializedName("public_id")
    val publicId: String,
    @SerializedName("display_name")
    val displayName: String,
    @SerializedName("created_at")
    val createdAt: String? = null,
    @SerializedName("last_seen_at")
    val lastSeenAt: String? = null
)
