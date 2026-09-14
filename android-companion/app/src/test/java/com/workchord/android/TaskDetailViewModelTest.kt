package com.workchord.android

import com.workchord.android.data.models.Assignee
import com.workchord.android.data.models.Project
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.fakes.FakeTaskRepository
import com.workchord.android.ui.viewmodels.TaskDetailViewModel
import com.workchord.android.util.MainDispatcherRule
import kotlinx.coroutines.ExperimentalCoroutinesApi
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
class TaskDetailViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private lateinit var fakeRepository: FakeTaskRepository

    private val testTask = Task(
        id = 5,
        title = "Implement Android Unit Tests & Architecture Validation",
        description = """
            ## Goal
            Ensure test coverage and verify architecture contracts
            
            ## Acceptance criteria
            - [ ] Unit tests for Repositories and ViewModels
            - [x] Mock HTTP tests verifying WorkChord contracts
            - [ ] All tests passing
        """.trimIndent(),
        priority = 7,
        effortDays = 2.0,
        effortHours = 16.0,
        statusRaw = "planned",
        version = 2,
        project = Project(id = 1, name = "WorkChord Companion"),
        assignee = Assignee(id = 3, name = "Dmitry QA")
    )

    @Before
    fun setUp() {
        fakeRepository = FakeTaskRepository(
            initialTasks = listOf(testTask)
        )
    }

    @Test
    fun testInitialLoadSuccessAndAcceptanceCriteriaParsing() = runTest {
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        val state = viewModel.uiState.value
        assertFalse("isLoading should be false after load", state.isLoading)
        assertFalse("isUpdatingStatus should be false", state.isUpdatingStatus)
        assertNull("errorMessage should be null", state.errorMessage)

        assertNotNull("Task should be present", state.task)
        assertEquals(5, state.task?.id)
        assertEquals(TaskStatus.PLANNED, state.task?.status)
        assertEquals(2, state.task?.version)

        // Verify acceptance criteria parsed correctly
        assertEquals(3, state.acceptanceCriteria.size)
        assertEquals("Unit tests for Repositories and ViewModels", state.acceptanceCriteria[0].text)
        assertFalse(state.acceptanceCriteria[0].isCompleted)

        assertEquals("Mock HTTP tests verifying WorkChord contracts", state.acceptanceCriteria[1].text)
        assertTrue(state.acceptanceCriteria[1].isCompleted)

        assertEquals("All tests passing", state.acceptanceCriteria[2].text)
        assertFalse(state.acceptanceCriteria[2].isCompleted)
    }

    @Test
    fun testStartTaskTransitionsToActive() = runTest {
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        viewModel.startTask()

        val state = viewModel.uiState.value
        assertFalse(state.isUpdatingStatus)
        assertNull(state.errorMessage)
        assertNotNull(state.successMessage)
        assertTrue(state.successMessage?.contains("Active") == true)

        assertEquals(TaskStatus.ACTIVE, state.task?.status)
        assertEquals(3, state.task?.version) // Version incremented

        assertEquals(5, fakeRepository.lastUpdatedTaskId)
        assertEquals(TaskStatus.ACTIVE, fakeRepository.lastUpdatedStatus)
        assertEquals("Task started by mobile user", fakeRepository.lastReason)
        assertEquals(2, fakeRepository.lastExpectedVersion)
    }

    @Test
    fun testResolveTaskTransitionsToResolved() = runTest {
        // Set task initially to ACTIVE
        fakeRepository.setTasks(listOf(testTask.copy(statusRaw = "active")))
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        viewModel.resolveTask()

        val state = viewModel.uiState.value
        assertFalse(state.isUpdatingStatus)
        assertNull(state.errorMessage)
        assertNotNull(state.successMessage)
        assertTrue(state.successMessage?.contains("Resolved") == true)

        assertEquals(TaskStatus.RESOLVED, state.task?.status)
        assertEquals(TaskStatus.RESOLVED, fakeRepository.lastUpdatedStatus)
        assertEquals("Task marked resolved from mobile companion", fakeRepository.lastReason)
    }

    @Test
    fun testBlockTaskTransitionsToBlocked() = runTest {
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        viewModel.blockTask("Blocked on API specification")

        val state = viewModel.uiState.value
        assertFalse(state.isUpdatingStatus)
        assertNull(state.errorMessage)
        assertNotNull(state.successMessage)
        assertTrue(state.successMessage?.contains("Blocked") == true)

        assertEquals(TaskStatus.BLOCKED, state.task?.status)
        assertEquals(TaskStatus.BLOCKED, fakeRepository.lastUpdatedStatus)
        assertEquals("Blocked on API specification", fakeRepository.lastReason)
    }

    @Test
    fun testReopenTaskTransitionsToActive() = runTest {
        fakeRepository.setTasks(listOf(testTask.copy(statusRaw = "resolved")))
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        viewModel.reopenTask()

        val state = viewModel.uiState.value
        assertFalse(state.isUpdatingStatus)
        assertEquals(TaskStatus.ACTIVE, state.task?.status)
        assertEquals("Rework requested", fakeRepository.lastReason)
    }

    @Test
    fun testCloseTaskTransitionsToClosed() = runTest {
        fakeRepository.setTasks(listOf(testTask.copy(statusRaw = "resolved")))
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        viewModel.closeTask()

        val state = viewModel.uiState.value
        assertFalse(state.isUpdatingStatus)
        assertEquals(TaskStatus.CLOSED, state.task?.status)
        assertEquals("Task verified and closed", fakeRepository.lastReason)
    }

    @Test
    fun testVersionMismatchErrorHandling() = runTest {
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        // Inject simulated version mismatch conflict error in repository
        fakeRepository.updateTaskStatusResult = Result.failure(
            Exception("Version conflict: expected version 2, but remote version is 3.")
        )

        viewModel.resolveTask()

        val state = viewModel.uiState.value
        assertFalse("isUpdatingStatus should reset to false", state.isUpdatingStatus)
        assertNull("successMessage should remain null", state.successMessage)
        assertEquals(
            "Version conflict: expected version 2, but remote version is 3.",
            state.errorMessage
        )
        // Task status should remain unchanged
        assertEquals(TaskStatus.PLANNED, state.task?.status)
    }

    @Test
    fun testChecklistToggles() = runTest {
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        // Initially item 0 is false, item 1 is true, item 2 is false
        assertFalse(viewModel.uiState.value.acceptanceCriteria[0].isCompleted)
        assertTrue(viewModel.uiState.value.acceptanceCriteria[1].isCompleted)
        assertFalse(viewModel.uiState.value.acceptanceCriteria[2].isCompleted)

        // Toggle item 0 -> should become true
        viewModel.toggleAcceptanceCriterion(0)
        assertTrue(viewModel.uiState.value.acceptanceCriteria[0].isCompleted)

        // Toggle item 0 again -> should become false
        viewModel.toggleAcceptanceCriterion(0)
        assertFalse(viewModel.uiState.value.acceptanceCriteria[0].isCompleted)

        // Toggle item 1 -> should become false
        viewModel.toggleAcceptanceCriterion(1)
        assertFalse(viewModel.uiState.value.acceptanceCriteria[1].isCompleted)

        // Out of bounds toggle -> should not crash or mutate list
        viewModel.toggleAcceptanceCriterion(999)
        assertEquals(3, viewModel.uiState.value.acceptanceCriteria.size)
    }

    @Test
    fun testClearMessages() = runTest {
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)

        viewModel.startTask()
        assertNotNull(viewModel.uiState.value.successMessage)

        viewModel.clearMessages()
        assertNull(viewModel.uiState.value.successMessage)
        assertNull(viewModel.uiState.value.errorMessage)
    }

    @Test
    fun testLoadTaskFailure() = runTest {
        fakeRepository.getTaskByIdResult = Result.failure(Exception("Task 999 not found"))

        val viewModel = TaskDetailViewModel(taskId = 999, repository = fakeRepository)

        val state = viewModel.uiState.value
        assertFalse(state.isLoading)
        assertNull(state.task)
        assertEquals("Task 999 not found", state.errorMessage)
    }

    @Test
    fun testObserveExternalTaskUpdates() = runTest {
        val viewModel = TaskDetailViewModel(taskId = 5, repository = fakeRepository)
        assertEquals(TaskStatus.PLANNED, viewModel.uiState.value.task?.status)

        // Simulate background task status update in repository
        val updatedTask = testTask.copy(
            statusRaw = "active",
            description = "## Acceptance criteria\n- [x] All done!"
        )
        fakeRepository.setTasks(listOf(updatedTask))

        val state = viewModel.uiState.value
        assertEquals(TaskStatus.ACTIVE, state.task?.status)
        assertEquals(1, state.acceptanceCriteria.size)
        assertTrue(state.acceptanceCriteria[0].isCompleted)
        assertEquals("All done!", state.acceptanceCriteria[0].text)
    }
}
