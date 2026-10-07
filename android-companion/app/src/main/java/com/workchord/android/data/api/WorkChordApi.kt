package com.workchord.android.data.api

import com.workchord.android.data.models.Iteration
import com.workchord.android.data.models.Identity
import com.workchord.android.data.models.Project
import com.workchord.android.data.models.ProjectPage
import com.workchord.android.data.models.IterationPage
import com.workchord.android.data.models.Session
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatusChangeRequest
import com.workchord.android.data.models.TaskStatusChangeResponse
import com.workchord.android.data.models.TaskUpdateRequest
import com.workchord.android.data.models.TaskActions
import com.workchord.android.data.models.TaskCommandRequest
import com.workchord.android.data.models.TaskDetail
import com.workchord.android.data.models.DomainCapabilities
import com.workchord.android.data.models.ProgressRequest
import com.workchord.android.data.models.ReviewRequest
import com.workchord.android.data.models.TaskReview
import com.workchord.android.data.models.CurrentTaskReview
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PUT
import retrofit2.http.POST
import retrofit2.http.Query
import com.workchord.android.data.models.HumanWork
import com.workchord.android.data.models.TaskReferencePage
import retrofit2.http.Path

interface WorkChordApi {

    @POST("api/auth/native-connections/start")
    suspend fun startNativeConnection(@Body request: NativeStartRequest): Response<NativeStartResponse>

    @POST("api/auth/native-connections/exchange")
    suspend fun exchangeNativeConnection(@Body request: NativeExchangeRequest): Response<NativeTokenResponse>

    @POST("api/auth/logout")
    suspend fun logout(): Response<Map<String, Boolean>>

    @GET("api/tasks/capabilities")
    suspend fun getCapabilities(): Response<DomainCapabilities>

    @GET("api/tasks/my-work")
    suspend fun getMyWork(@Query("project_id") projectId: Int? = null, @Query("iteration_id") iterationId: Int? = null,
        @Query("backlog_only") backlogOnly: Boolean = false, @Query("after_id") afterId: Int = 0,
        @Query("limit") limit: Int = 50): Response<HumanWork>

    @GET("api/tasks/review-queue")
    suspend fun getReviewQueue(@Query("project_id") projectId: Int? = null, @Query("iteration_id") iterationId: Int? = null,
        @Query("backlog_only") backlogOnly: Boolean = false, @Query("after_id") afterId: Int = 0,
        @Query("limit") limit: Int = 50): Response<TaskReferencePage>

    @GET("api/tasks/{id}/detail")
    suspend fun getTaskDetail(@Path("id") taskId: Int,
        @Query("children_after_id") childrenAfterId: Int = 0,
        @Query("dependencies_after_id") dependenciesAfterId: Int = 0): Response<TaskDetail>

    @GET("api/tasks/{id}/actions")
    suspend fun getTaskActions(@Path("id") taskId: Int): Response<TaskActions>

    @POST("api/tasks/{id}/commands")
    suspend fun executeTaskCommand(@Path("id") taskId: Int, @Body request: TaskCommandRequest): Response<Task>

    @POST("api/tasks/{id}/progress")
    suspend fun recordProgress(@Path("id") taskId: Int, @Body request: ProgressRequest): Response<Task>

    @POST("api/tasks/{id}/review")
    suspend fun reviewTask(@Path("id") taskId: Int, @Body request: ReviewRequest): Response<Task>

    @GET("api/tasks/{id}/reviews")
    suspend fun getReviews(@Path("id") taskId: Int): Response<List<TaskReview>>

    @GET("api/tasks/{id}/reviews/current")
    suspend fun getCurrentReview(@Path("id") taskId: Int): Response<CurrentTaskReview>

    @GET("api/auth/me")
    suspend fun getIdentity(): Response<Identity>

    @GET("api/session/whoami")
    suspend fun getSessionWhoami(): Response<Session>

    @GET("api/iterations/{id}/tasks")
    suspend fun getIterationTasks(
        @Path("id") iterationId: Int
    ): Response<List<Task>>

    @GET("api/tasks/{id}")
    suspend fun getTaskById(
        @Path("id") taskId: Int
    ): Response<Task>

    @PUT("api/tasks/{id}")
    suspend fun updateTask(
        @Path("id") taskId: Int,
        @Body request: TaskUpdateRequest
    ): Response<Task>

    @PUT("api/tasks/{id}/status")
    suspend fun changeTaskStatus(
        @Path("id") taskId: Int,
        @Body request: TaskStatusChangeRequest
    ): Response<TaskStatusChangeResponse>

    @GET("api/iterations/page")
    suspend fun getIterationPage(@Query("after_id") afterId: Int = 0, @Query("upper_id") upperId: Int? = null): Response<IterationPage>

    @GET("api/iterations")
    suspend fun getIterations(): Response<List<Iteration>>

    @GET("api/projects/page")
    suspend fun getProjectPage(@Query("after_id") afterId: Int = 0, @Query("upper_id") upperId: Int? = null): Response<ProjectPage>

    @GET("api/projects")
    suspend fun getProjects(): Response<List<Project>>
}

data class NativeStartRequest(@com.google.gson.annotations.SerializedName("code_challenge") val codeChallenge: String)
data class NativeStartResponse(@com.google.gson.annotations.SerializedName("request_id") val requestId: String,
    @com.google.gson.annotations.SerializedName("verification_code") val verificationCode: String,
    @com.google.gson.annotations.SerializedName("verification_path") val verificationPath: String,
    @com.google.gson.annotations.SerializedName("expires_at") val expiresAt: String)
data class NativeExchangeRequest(@com.google.gson.annotations.SerializedName("request_id") val requestId: String,
    @com.google.gson.annotations.SerializedName("code_verifier") val codeVerifier: String)
data class NativeTokenResponse(val status: String? = null,
    @com.google.gson.annotations.SerializedName("access_token") val accessToken: String? = null,
    @com.google.gson.annotations.SerializedName("token_type") val tokenType: String? = null,
    @com.google.gson.annotations.SerializedName("expires_at") val expiresAt: String? = null)
