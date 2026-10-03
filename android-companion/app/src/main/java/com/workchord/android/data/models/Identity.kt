package com.workchord.android.data.models

import com.google.gson.annotations.SerializedName

data class Identity(
    val authenticated: Boolean = false,
    val principal: IdentityPrincipal? = null,
    val profile: IdentityProfile? = null,
    val configured: Boolean = false,
    val mode: String? = null,
    @SerializedName("csrf_token") val csrfToken: String? = null,
    @SerializedName("authentication_error") val authenticationError: String? = null,
    @SerializedName("workspace_role") val workspaceRole: String? = null,
    val projects: Map<String, String>? = null
) {
    val humanOwnerProfileId: Int?
        get() = if (authenticated && principal?.kind == "human" && principal.id > 0) {
            profile?.id?.takeIf { it > 0 }
        } else null
}

data class IdentityPrincipal(
    val id: Int,
    val kind: String,
    @SerializedName("display_name") val displayName: String? = null
)

data class IdentityProfile(
    val id: Int,
    @SerializedName("display_name") val displayName: String? = null
)
