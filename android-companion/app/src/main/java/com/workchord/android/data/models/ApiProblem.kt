package com.workchord.android.data.models

import com.google.gson.Gson
import com.google.gson.JsonElement
import com.google.gson.annotations.SerializedName

data class ProblemDetail(val code: String? = null, val message: String? = null,
    @SerializedName("current_version") val currentVersion: Int? = null,
    @SerializedName("expected_version") val expectedVersion: Int? = null,
    @SerializedName("current_task") val currentTask: Task? = null,
    @SerializedName("current_revision") val currentRevision: Int? = null,
    @SerializedName("current_revisions") val currentRevisions: Map<String, Int>? = null)

data class ValidationIssue(val loc: List<JsonElement>?, val msg: String?, val type: String?)

class ApiProblem(val statusCode: Int, val problem: ProblemDetail, val validationIssues: List<ValidationIssue> = emptyList()) : Exception(problem.message ?: "Request failed ($statusCode)") {
    companion object {
        fun parse(status: Int, body: String?): ApiProblem {
            val gson = Gson()
            val root = runCatching { gson.fromJson(body, JsonElement::class.java) }.getOrNull()
            val detail = root?.takeIf { it.isJsonObject }?.asJsonObject?.get("detail")
            val parsed = if (detail?.isJsonObject == true) runCatching { gson.fromJson(detail, ProblemDetail::class.java) }.getOrNull() else null
            val message = if (detail?.isJsonPrimitive == true && detail.asJsonPrimitive.isString) detail.asString else null
            val issues = if (detail?.isJsonArray == true) runCatching {
                gson.fromJson(detail, Array<ValidationIssue>::class.java).toList()
            }.getOrDefault(emptyList()) else emptyList()
            return ApiProblem(status, parsed ?: ProblemDetail(message = message ?: when (status) {
                401 -> "Sign in again to restore your session."
                403 -> "Your account cannot access this work."
                404 -> "This work was deleted or is no longer accessible."
                409 -> "This work changed. Reload and compare before submitting again."
                422 -> "The server rejected these values. Review your inputs."
                else -> "The server could not complete the request ($status)."
            }), issues)
        }
    }
}
