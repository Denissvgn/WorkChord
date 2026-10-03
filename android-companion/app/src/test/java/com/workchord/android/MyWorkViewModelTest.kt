package com.workchord.android

import com.workchord.android.data.models.Identity
import com.workchord.android.data.models.IdentityPrincipal
import com.workchord.android.data.models.IdentityProfile
import com.workchord.android.data.models.Session
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.fakes.FakeTaskRepository
import com.workchord.android.ui.viewmodels.MyWorkViewModel
import com.workchord.android.ui.viewmodels.TaskFilter
import com.workchord.android.util.MainDispatcherRule
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Rule
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class MyWorkViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private lateinit var fakeRepository: FakeTaskRepository

    private val sampleTasks = listOf(
        Task(
            id = 1,
            title = "Active Development Task",
            description = "## Goal\nImplement feature",
            statusRaw = "active",
            priority = 9,
            version = 1
        ),
        Task(
            id = 2,
            title = "Planned Backlog Task",
            description = "## Goal\nPlan next sprint",
            statusRaw = "planned",
            priority = 5,
            version = 1
        ),
        Task(
            id = 3,
            title = "Blocked Task",
            description = "## Goal\nWait for dependency",
            statusRaw = "planned",
            blockedReason = "Waiting for an unavailable prerequisite",
            priority = 6,
            version = 1
        ),
        Task(
            id = 4,
            title = "Resolved Task",
            description = "## Goal\nTesting complete",
            statusRaw = "resolved",
            priority = 7,
            version = 2
        ),
        Task(
            id = 5,
            title = "Closed Task",
            description = "## Goal\nShipped to prod",
            statusRaw = "closed",
            priority = 4,
            version = 3
        )
    ).map { it.copy(ownerProfileId = 7) }

    private val sampleSession = Session(
        id = 3,
        publicId = "usr_dmitry",
        displayName = "Dmitry QA"
    )

    @Before
    fun setUp() {
        fakeRepository = FakeTaskRepository(
            initialTasks = sampleTasks,
            initialSession = sampleSession
        ).apply { identityResult = Result.success(Identity(true, IdentityPrincipal(3, "human"), IdentityProfile(7))) }
    }

    @Test
    fun testInitialLoadSuccessAndCategorisation() = runTest {
        val viewModel = MyWorkViewModel(fakeRepository)

        val state = viewModel.uiState.value
        assertFalse("isLoading should be false after load", state.isLoading)
        assertFalse("isRefreshing should be false", state.isRefreshing)
        assertNull("errorMessage should be null", state.errorMessage)

        // Session verification
        assertNotNull("Session should be loaded", state.session)
        assertEquals("Dmitry QA", state.session?.displayName)

        // Task counts & categorisation verification
        assertEquals(5, state.allTasks.size)

        // Active tasks (status == ACTIVE)
        assertEquals(1, state.activeTasks.size)
        assertEquals(1, state.activeTasks[0].id)
        assertEquals(TaskStatus.ACTIVE, state.activeTasks[0].status)

        // Planned tasks include explicit blockage as a separate facet.
        assertEquals(2, state.assignedQueue.size)
        assertTrue(state.assignedQueue.any { it.id == 2 && it.status == TaskStatus.PLANNED })
        assertTrue(state.assignedQueue.any { it.id == 3 && it.blockedReason != null })

        // Resolved tasks (status == RESOLVED || status == CLOSED)
        assertEquals(2, state.resolvedTasks.size)
        assertTrue(state.resolvedTasks.any { it.id == 4 && it.status == TaskStatus.RESOLVED })
        assertTrue(state.resolvedTasks.any { it.id == 5 && it.status == TaskStatus.CLOSED })

        // Default filter
        assertEquals(TaskFilter.ALL, state.selectedFilter)
    }

    @Test
    fun testTaskFilteringByTabs() = runTest {
        val viewModel = MyWorkViewModel(fakeRepository)

        assertEquals(TaskFilter.ALL, viewModel.uiState.value.selectedFilter)

        viewModel.setFilter(TaskFilter.ACTIVE)
        assertEquals(TaskFilter.ACTIVE, viewModel.uiState.value.selectedFilter)

        viewModel.setFilter(TaskFilter.QUEUED)
        assertEquals(TaskFilter.QUEUED, viewModel.uiState.value.selectedFilter)

        viewModel.setFilter(TaskFilter.RESOLVED)
        assertEquals(TaskFilter.RESOLVED, viewModel.uiState.value.selectedFilter)

        viewModel.setFilter(TaskFilter.ALL)
        assertEquals(TaskFilter.ALL, viewModel.uiState.value.selectedFilter)
    }

    @Test
    fun testLoadDataFailureSetsErrorBanner() = runTest {
        fakeRepository.fetchTasksResult = Result.failure(Exception("Unable to reach WorkChord API server"))

        val viewModel = MyWorkViewModel(fakeRepository)

        val state = viewModel.uiState.value
        assertFalse(state.isLoading)
        assertEquals("Unable to reach WorkChord API server", state.errorMessage)
    }

    @Test
    fun testClearErrorRemovesErrorBanner() = runTest {
        fakeRepository.fetchTasksResult = Result.failure(Exception("Connection timeout"))

        val viewModel = MyWorkViewModel(fakeRepository)
        assertEquals("Connection timeout", viewModel.uiState.value.errorMessage)

        viewModel.clearError()
        assertNull("Error message should be cleared", viewModel.uiState.value.errorMessage)
    }

    @Test
    fun testRefreshSuccess() = runTest {
        val viewModel = MyWorkViewModel(fakeRepository)
        assertEquals(5, viewModel.uiState.value.allTasks.size)

        // Update repository data
        val updatedTasks = sampleTasks.filter { it.id != 2 }
        fakeRepository.fetchTasksResult = Result.success(updatedTasks)

        viewModel.refresh()

        val state = viewModel.uiState.value
        assertFalse("isRefreshing should be reset", state.isRefreshing)
        assertNull(state.errorMessage)
        assertEquals(4, state.allTasks.size)
        assertEquals(1, state.assignedQueue.size)
    }

    @Test
    fun testRefreshFailureSetsErrorMessage() = runTest {
        val viewModel = MyWorkViewModel(fakeRepository)

        fakeRepository.fetchTasksResult = Result.failure(Exception("HTTP 502 Bad Gateway"))

        viewModel.refresh()

        val state = viewModel.uiState.value
        assertFalse(state.isRefreshing)
        assertEquals("HTTP 502 Bad Gateway", state.errorMessage)
    }

    @Test
    fun testObserveRepositoryTasksUpdatesUiStateReactivity() = runTest {
        val viewModel = MyWorkViewModel(fakeRepository)
        assertEquals(1, viewModel.uiState.value.activeTasks.size)

        // Simulate external state transition in repository (Task 2 becomes ACTIVE)
        val modifiedList = sampleTasks.map { task ->
            if (task.id == 2) task.copy(statusRaw = "active") else task
        }
        fakeRepository.setTasks(modifiedList)

        // UI state should reactively update via cachedTasks Flow collector
        val state = viewModel.uiState.value
        assertEquals(2, state.activeTasks.size)
        assertEquals(1, state.assignedQueue.size)
    }

    @Test
    fun testEmptyTaskStateEmissions() = runTest {
        fakeRepository.setTasks(emptyList())
        val viewModel = MyWorkViewModel(fakeRepository)

        val state = viewModel.uiState.value
        assertFalse(state.isLoading)
        assertTrue(state.allTasks.isEmpty())
        assertTrue(state.activeTasks.isEmpty())
        assertTrue(state.assignedQueue.isEmpty())
        assertTrue(state.resolvedTasks.isEmpty())
        assertNull(state.errorMessage)
    }
    @Test
    fun onlyTheAuthenticatedLinkedOwnerIsShownIncludingNestedWork() = runTest {
        fakeRepository.setTasks(sampleTasks + listOf(
            Task(id = 20, title = "Other owner", ownerProfileId = 8),
            Task(id = 21, title = "Unowned"),
            Task(id = 22, title = "Guest ID is not ownership", ownerProfileId = sampleSession.id),
            Task(id = 23, title = "Group", children = listOf(Task(id = 24, title = "Owned child", ownerProfileId = 7))),
            Task(id = 25, title = "Canceled", ownerProfileId = 7, canceledAt = "2026-01-01T00:00:00Z")
        ))
        val model = MyWorkViewModel(fakeRepository)
        assertEquals(setOf(1, 2, 3, 4, 5, 24), model.uiState.value.allTasks.map { it.id }.toSet())
        fakeRepository.identityResult = Result.success(Identity(true, IdentityPrincipal(9, "human"), IdentityProfile(8)))
        model.refresh()
        assertEquals(listOf(20), model.uiState.value.allTasks.map { it.id })
    }

    @Test
    fun failedIdentityAndUnlinkedGuestsNeverReuseCachedTasks() = runTest {
        val model = MyWorkViewModel(fakeRepository)
        assertEquals(5, model.uiState.value.allTasks.size)
        fakeRepository.identityResult = Result.failure(Exception("Session expired"))
        model.refresh()
        assertEquals("Session expired", model.uiState.value.errorMessage)
        assertTrue(model.uiState.value.allTasks.isEmpty())
        assertNull(model.uiState.value.session)
        fakeRepository.setTasks(sampleTasks.map { it.copy(title = "Changed while signed out") })
        assertTrue(model.uiState.value.allTasks.isEmpty())
        fakeRepository.identityResult = Result.success(Identity())
        model.refresh()
        assertTrue(model.uiState.value.allTasks.isEmpty())
        assertNotNull(model.uiState.value.errorMessage)
        assertEquals(1, fakeRepository.fetchTasksCallCount)
    }

    @Test
    fun absentProfileAndAgentIdentityDoNotGrantHumanOwnership() = runTest {
        for (identity in listOf(Identity(true, IdentityPrincipal(3, "human")),
            Identity(true, IdentityPrincipal(3, "agent"), IdentityProfile(7)))) {
            fakeRepository.identityResult = Result.success(identity)
            val model = MyWorkViewModel(fakeRepository)
            assertTrue(model.uiState.value.allTasks.isEmpty())
            assertNotNull(model.uiState.value.errorMessage)
        }
        assertEquals(0, fakeRepository.fetchTasksCallCount)
    }

}
