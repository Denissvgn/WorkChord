package com.workchord.android

import com.workchord.android.data.api.AuthInterceptor
import com.workchord.android.data.api.SessionCookieJar
import com.workchord.android.data.api.TokenManager
import com.workchord.android.data.api.WorkChordApi
import com.workchord.android.data.models.Assignee
import com.workchord.android.data.models.Project
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.data.models.TaskUpdateRequest
import com.workchord.android.data.repository.TaskRepository
import com.workchord.android.data.repository.TaskRepositoryImpl
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.take
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import okhttp3.OkHttpClient
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

@OptIn(ExperimentalCoroutinesApi::class)
class TaskRepositoryTest {

    private lateinit var mockWebServer: MockWebServer
    private lateinit var api: WorkChordApi
    private lateinit var tokenManager: TokenManager
    private lateinit var repository: TaskRepository
    private val testDispatcher = UnconfinedTestDispatcher()

    @Before
    fun setUp() {
        mockWebServer = MockWebServer()
        mockWebServer.start()

        tokenManager = TokenManager(allowDebugHttp = true).apply {
            baseUrl = mockWebServer.url("/").toString()
            agentApiKey = "test-agent-key-123"
        }

        val okHttpClient = OkHttpClient.Builder()
            .connectTimeout(2, TimeUnit.SECONDS)
            .readTimeout(2, TimeUnit.SECONDS)
            .cookieJar(SessionCookieJar(tokenManager))
            .addInterceptor(AuthInterceptor(tokenManager))
            .build()

        api = Retrofit.Builder()
            .baseUrl(mockWebServer.url("/"))
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(WorkChordApi::class.java)

        repository = TaskRepositoryImpl(
            api = api,
            tokenManager = tokenManager,
            ioDispatcher = testDispatcher
        )
    }

    @After
    fun tearDown() {
        mockWebServer.shutdown()
    }

    @Test
    fun unsupportedStatusOrMissingVersionCannotIssueAMutation() = runTest(testDispatcher) {
        mockWebServer.enqueue(MockResponse().setBody("""[
            {"id":99,"title":"Future work","status":"future_status","version":7},
            {"id":100,"title":"Incomplete work","status":"planned"}
        ]"""))
        assertTrue(repository.fetchTasks(1).isSuccess)
        val unsupported = repository.updateTaskStatus(99, TaskStatus.ACTIVE, "Start", 7)
        assertTrue(unsupported.isFailure)
        assertEquals("unsupported_task_status", (unsupported.exceptionOrNull() as com.workchord.android.data.models.ApiProblem).problem.code)
        val unknownVersion = repository.updateTaskStatus(100, TaskStatus.ACTIVE, "Start", null)
        assertEquals("task_version_required", (unknownVersion.exceptionOrNull() as com.workchord.android.data.models.ApiProblem).problem.code)
        assertTrue(repository.updateTask(100, TaskUpdateRequest(title = "Unversioned draft")).isFailure)
        assertEquals(1, mockWebServer.requestCount)
    }

    @Test
    fun mismatchedCommandResponseCannotBeReportedAsASavedTask() = runTest(testDispatcher) {
        mockWebServer.enqueue(MockResponse().setBody("{\"id\":999,\"title\":\"Other work\",\"status\":\"active\",\"version\":4}"))
        val result = repository.executeCommand(72, com.workchord.android.data.models.TaskCommandRequest("start_manual", 3, "Begin work"))
        assertTrue(result.isFailure)
        assertEquals("unverified_write_response", (result.exceptionOrNull() as com.workchord.android.data.models.ApiProblem).problem.code)
        assertTrue(repository.cachedTasks.first().isEmpty())
    }

    @Test
    fun testGetWhoAmISuccess() = runTest(testDispatcher) {
        val sessionJson = """
            {
                "id": 3,
                "public_id": "usr_dmitry_qa",
                "display_name": "Dmitry QA",
                "created_at": "2026-08-15T00:00:00Z"
            }
        """.trimIndent()

        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(sessionJson))

        val result = repository.getWhoAmI()

        assertTrue(result.isSuccess)
        val session = result.getOrNull()
        assertNotNull(session)
        assertEquals(3, session?.id)
        assertEquals("usr_dmitry_qa", session?.publicId)
        assertEquals("Dmitry QA", session?.displayName)

        val recordedRequest = mockWebServer.takeRequest()
        assertEquals("/api/session/whoami", recordedRequest.path)
        assertEquals("GET", recordedRequest.method)
        assertEquals("test-agent-key-123", recordedRequest.getHeader("X-Agent-API-Key"))
    }

    @Test
    fun testGetWhoAmIUnauthorizedError() = runTest(testDispatcher) {
        mockWebServer.enqueue(MockResponse().setResponseCode(401).setBody("{\"error\":\"Unauthorized\"}"))

        val result = repository.getWhoAmI()

        assertTrue(result.isFailure)
        assertTrue(result.exceptionOrNull()?.message?.contains("401") == true)
    }

    @Test
    fun testFetchTasksSuccessAndPopulatesCache() = runTest(testDispatcher) {
        val tasksJson = """
            [
                {
                    "id": 1,
                    "title": "Task 1",
                    "description": "## Goal\nFirst Task",
                    "status": "active",
                    "priority": 8,
                    "version": 1
                },
                {
                    "id": 2,
                    "title": "Task 2",
                    "description": "## Goal\nSecond Task",
                    "status": "planned",
                    "priority": 5,
                    "version": 1
                }
            ]
        """.trimIndent()

        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(tasksJson))

        val result = repository.fetchTasks(iterationId = 1)

        assertTrue(result.isSuccess)
        val tasks = result.getOrNull()
        assertNotNull(tasks)
        assertEquals(2, tasks?.size)
        assertEquals("Task 1", tasks?.get(0)?.title)
        assertEquals(TaskStatus.ACTIVE, tasks?.get(0)?.status)
        assertEquals("Task 2", tasks?.get(1)?.title)
        assertEquals(TaskStatus.PLANNED, tasks?.get(1)?.status)

        // Verify cachedTasks Flow emission
        val cached = repository.cachedTasks.first()
        assertEquals(2, cached.size)
        assertEquals(1, cached[0].id)
        assertEquals(2, cached[1].id)

        val recordedRequest = mockWebServer.takeRequest()
        assertEquals("/api/iterations/1/tasks", recordedRequest.path)
        assertEquals("GET", recordedRequest.method)
    }

    @Test
    fun testFetchTasksServerError() = runTest(testDispatcher) {
        mockWebServer.enqueue(MockResponse().setResponseCode(500).setBody("Internal Server Error"))

        val result = repository.fetchTasks(iterationId = 1)

        assertTrue(result.isFailure)
        assertTrue(result.exceptionOrNull()?.message?.contains("Failed to fetch tasks") == true)
    }

    @Test
    fun testGetTaskByIdRemoteSuccessAndUpdatesCache() = runTest(testDispatcher) {
        val taskJson = """
            {
                "id": 5,
                "title": "Implement Unit Tests",
                "description": "## Acceptance criteria\n- [x] Repositories tested\n- [ ] ViewModels tested",
                "status": "active",
                "priority": 7,
                "version": 2,
                "project": {
                    "id": 1,
                    "name": "WorkChord Companion"
                },
                "assignee": {
                    "id": 3,
                    "name": "Dmitry QA"
                }
            }
        """.trimIndent()

        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(taskJson))

        val result = repository.getTaskById(5)

        assertTrue(result.isSuccess)
        val task = result.getOrNull()
        assertNotNull(task)
        assertEquals(5, task?.id)
        assertEquals("Implement Unit Tests", task?.title)
        assertEquals(TaskStatus.ACTIVE, task?.status)
        assertEquals(2, task?.version)
        assertEquals("WorkChord Companion", task?.project?.name)
        assertEquals("Dmitry QA", task?.assignee?.name)

        val criteria = task?.extractAcceptanceCriteria()
        assertEquals(2, criteria?.size)
        assertFalse(criteria?.get(0)?.isCompleted == true)
        assertFalse(criteria?.get(1)?.isCompleted == true)

        // Verify local cache updated
        val cached = repository.cachedTasks.first()
        assertEquals(1, cached.size)
        assertEquals(5, cached[0].id)

        val recordedRequest = mockWebServer.takeRequest()
        assertEquals("/api/tasks/5", recordedRequest.path)
    }

    @Test
    fun testGetTaskByIdOfflineFallbackToCacheOnNetworkFailure() = runTest(testDispatcher) {
        // Step 1: Pre-populate cache via fetchTasks
        val initialTasks = """
            [
                {
                    "id": 5,
                    "title": "Cached Task",
                    "status": "planned",
                    "version": 1
                }
            ]
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(initialTasks))
        repository.fetchTasks(iterationId = 1)
        mockWebServer.takeRequest()

        // Step 2: Now network fails on getTaskById
        mockWebServer.enqueue(MockResponse().setResponseCode(503).setBody("Service Unavailable"))

        val result = repository.getTaskById(5)

        // Should return the cached task gracefully
        assertTrue(result.isSuccess)
        val task = result.getOrNull()
        assertNotNull(task)
        assertEquals(5, task?.id)
        assertEquals("Cached Task", task?.title)
    }

    @Test
    fun testGetTaskByIdNotFoundWithEmptyCacheFails() = runTest(testDispatcher) {
        mockWebServer.enqueue(MockResponse().setResponseCode(404).setBody("Task not found"))

        val result = repository.getTaskById(999)

        assertTrue(result.isFailure)
        assertTrue(result.exceptionOrNull()?.message?.contains("404") == true)
    }

    @Test
    fun testUpdateTaskStatusSuccessAndUpdatesCache() = runTest(testDispatcher) {
        // Pre-populate task in cache
        val initialJson = """
            [
                {
                    "id": 5,
                    "title": "Scaffold Unit Tests",
                    "status": "active",
                    "version": 2
                }
            ]
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(initialJson))
        repository.fetchTasks(iterationId = 1)
        mockWebServer.takeRequest()

        // Response for status change
        val statusChangeResponseJson = """
            {
                "task": {
                    "id": 5,
                    "title": "Scaffold Unit Tests",
                    "status": "resolved",
                    "version": 3
                },
                "cascade_updates": [],
                "notifications_sent": true
            }
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(statusChangeResponseJson))

        val result = repository.updateTaskStatus(
            taskId = 5,
            newStatus = TaskStatus.RESOLVED,
            reason = "Unit tests completed and verified",
            expectedVersion = 2
        )

        assertTrue(result.isSuccess)
        val updated = result.getOrNull()
        assertNotNull(updated)
        assertEquals(TaskStatus.RESOLVED, updated?.status)
        assertEquals(3, updated?.version)

        // Verify local cache updated with the new task state
        val cached = repository.cachedTasks.first()
        val cachedTask5 = cached.first { it.id == 5 }
        assertEquals(TaskStatus.RESOLVED, cachedTask5.status)
        assertEquals(3, cachedTask5.version)

        // Verify request payload
        val recordedRequest = mockWebServer.takeRequest()
        assertEquals("/api/tasks/5/status", recordedRequest.path)
        assertEquals("PUT", recordedRequest.method)
        val body = recordedRequest.body.readUtf8()
        assertTrue(body.contains("\"status\":\"resolved\""))
        assertTrue(body.contains("\"reason\":\"Unit tests completed and verified\""))
        assertTrue(body.contains("\"expected_version\":2"))
    }

    @Test
    fun testUpdateTaskStatusUsesCachedVersionWhenExpectedVersionIsNull() = runTest(testDispatcher) {
        // Pre-populate cache with version = 4
        val initialJson = """
            [
                {
                    "id": 10,
                    "title": "Task 10",
                    "status": "planned",
                    "version": 4
                }
            ]
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(initialJson))
        repository.fetchTasks(iterationId = 1)
        mockWebServer.takeRequest()

        val responseJson = """
            {
                "task": {
                    "id": 10,
                    "title": "Task 10",
                    "status": "active",
                    "version": 5
                },
                "cascade_updates": []
            }
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(responseJson))

        val result = repository.updateTaskStatus(
            taskId = 10,
            newStatus = TaskStatus.ACTIVE,
            reason = "Started",
            expectedVersion = null // Should use cached version (4)
        )

        assertTrue(result.isSuccess)
        val recordedRequest = mockWebServer.takeRequest()
        val body = recordedRequest.body.readUtf8()
        assertTrue(body.contains("\"expected_version\":4"))
    }

    @Test
    fun testUpdateTaskStatusConflictVersionMismatch() = runTest(testDispatcher) {
        val conflictErrorJson = """
            {
                "detail": {
                    "code": "task_version_conflict",
                    "message": "Task version conflict: expected 1, current 3.",
                    "expected_version": 1,
                    "current_task": {"id": 5, "version": 3}
                }
            }
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(409).setBody(conflictErrorJson))

        val result = repository.updateTaskStatus(
            taskId = 5,
            newStatus = TaskStatus.RESOLVED,
            expectedVersion = 1
        )

        assertTrue(result.isFailure)
        val errorMsg = result.exceptionOrNull()?.message
        assertNotNull(errorMsg)
        assertTrue(errorMsg?.contains("version_conflict") == true || errorMsg?.contains("Failed to update status") == true)
    }

    @Test
    fun testUpdateTaskMetadataSuccess() = runTest(testDispatcher) {
        val updatedTaskJson = """
            {
                "id": 5,
                "title": "Updated Title",
                "description": "Updated Description",
                "priority": 9,
                "effort_hours": 20.0,
                "version": 3
            }
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(updatedTaskJson))

        val updateRequest = TaskUpdateRequest(
            title = "Updated Title",
            description = "Updated Description",
            priority = 9,
            effortHours = 20.0,
            expectedVersion = 2
        )

        val result = repository.updateTask(5, updateRequest)

        assertTrue(result.isSuccess)
        val updated = result.getOrNull()
        assertNotNull(updated)
        assertEquals("Updated Title", updated?.title)
        assertEquals(9, updated?.priority)
        assertEquals(20.0, updated?.effortHours)

        val recordedRequest = mockWebServer.takeRequest()
        assertEquals("/api/tasks/5", recordedRequest.path)
        assertEquals("PUT", recordedRequest.method)
    }

    @Test
    fun testObserveTaskFlow() = runTest(testDispatcher) {
        // Step 1: Initial tasks fetch
        val initialJson = """
            [
                {
                    "id": 5,
                    "title": "Initial Task",
                    "status": "planned",
                    "version": 1
                }
            ]
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(initialJson))
        repository.fetchTasks(iterationId = 1)
        mockWebServer.takeRequest()

        // Step 2: Observe task 5
        val observedFirst = repository.observeTask(5).first()
        assertNotNull(observedFirst)
        assertEquals("Initial Task", observedFirst?.title)
        assertEquals(TaskStatus.PLANNED, observedFirst?.status)

        // Step 3: Update task 5
        val updatedJson = """
            {
                "task": {
                    "id": 5,
                    "title": "Initial Task",
                    "status": "active",
                    "version": 2
                }
            }
        """.trimIndent()
        mockWebServer.enqueue(MockResponse().setResponseCode(200).setBody(updatedJson))
        repository.updateTaskStatus(5, TaskStatus.ACTIVE, "Start")

        val observedSecond = repository.observeTask(5).first()
        assertEquals(TaskStatus.ACTIVE, observedSecond?.status)
    }

    @Test
    fun testAuthInterceptorAttachesTokenAndCapturesCookie() = runTest(testDispatcher) {
        tokenManager.nativeAccessToken = "existing_native_token_xyz"
        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setHeader("Set-Cookie", "workchord_session=new_refreshed_token_abc; Path=/; HttpOnly")
                .setBody("{\"id\":1,\"public_id\":\"usr_1\",\"display_name\":\"User\"}")
        )

        repository.getWhoAmI()

        val recordedRequest = mockWebServer.takeRequest()
        assertEquals("Bearer existing_native_token_xyz", recordedRequest.getHeader("Authorization"))
        assertEquals(null, recordedRequest.getHeader("Cookie"))
        assertEquals("workchord_session=new_refreshed_token_abc", tokenManager.cookies.single().substringBefore(';'))
    }
    @Test
    fun identityComesFromAuthenticatedEndpointAndClearsPriorCache() = runTest(testDispatcher) {
        mockWebServer.enqueue(MockResponse().setBody("[{\"id\":1,\"title\":\"Old work\",\"status\":\"planned\"}]"))
        repository.fetchTasks(1)
        mockWebServer.takeRequest()
        mockWebServer.enqueue(MockResponse().setBody("""
            {"authenticated":true,"principal":{"id":19,"kind":"human","display_name":"Person"},"profile":{"id":7}}
        """.trimIndent()))
        val identity = repository.getIdentity().getOrThrow()
        assertEquals("/api/auth/me", mockWebServer.takeRequest().path)
        assertEquals(7, identity.humanOwnerProfileId)
        assertTrue(repository.cachedTasks.first().isEmpty())
    }

}
