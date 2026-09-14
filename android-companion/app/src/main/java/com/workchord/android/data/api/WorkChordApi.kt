package com.workchord.android.data.api

import com.workchord.android.data.models.Iteration
import com.workchord.android.data.models.Project
import com.workchord.android.data.models.Session
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatusChangeRequest
import com.workchord.android.data.models.TaskStatusChangeResponse
import com.workchord.android.data.models.TaskUpdateRequest
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PUT
import retrofit2.http.Path

interface WorkChordApi {

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

    @GET("api/iterations")
    suspend fun getIterations(): Response<List<Iteration>>

    @GET("api/projects")
    suspend fun getProjects(): Response<List<Project>>
}
