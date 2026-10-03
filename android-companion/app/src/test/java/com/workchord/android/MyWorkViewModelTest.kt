package com.workchord.android

import com.workchord.android.data.api.WorkSelection
import com.workchord.android.data.models.*
import com.workchord.android.fakes.FakeTaskRepository
import com.workchord.android.ui.viewmodels.MyWorkViewModel
import com.workchord.android.ui.viewmodels.TaskFilter
import com.workchord.android.util.MainDispatcherRule
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class MyWorkViewModelTest {
    @get:Rule val mainDispatcherRule = MainDispatcherRule()
    private fun reference(id: Int, parent: Int? = null) = TaskReference(id, "Work $id", 3, "planned", 9, null, parent, 7,
        projectName = "Other delivery")
    private fun repository() = FakeTaskRepository().apply {
        identityResult = Result.success(Identity(true, IdentityPrincipal(19, "human", "Person"), IdentityProfile(7, "Owner")))
        myWorkResult = Result.success(HumanWork("ready", mapOf("queued" to listOf(reference(72, 71))), false, null))
    }

    @Test fun actualHumanQueueIncludesNestedBacklogOutsideFirstIteration() = runTest {
        val repo = repository()
        val viewModel = MyWorkViewModel(repo)
        assertEquals(72, viewModel.uiState.value.visibleWork.single().id)
        assertEquals(71, viewModel.uiState.value.visibleWork.single().parentId)
        assertNull(repo.lastFetchIterationId)
        assertEquals(WorkSelection(), repo.lastSelection)
    }

    @Test fun projectAndBacklogSelectionsSurviveRefreshAndArePersisted() = runTest {
        val repo = repository()
        val viewModel = MyWorkViewModel(repo)
        viewModel.selectProject(9)
        viewModel.selectBacklog()
        viewModel.refresh()
        assertEquals(9, repo.lastSelection!!.projectId)
        assertTrue(repo.lastSelection!!.backlogOnly)
        assertEquals(repo.lastSelection, repo.workSelection)
        assertEquals(9, MyWorkViewModel(repo).uiState.value.selection.projectId)
    }

    @Test fun paginationUsesReturnedCursorAndDeduplicatesVersions() = runTest {
        val repo = repository()
        repo.myWorkResult = Result.success(HumanWork("ready", mapOf("queued" to listOf(reference(72))), true, 72))
        val viewModel = MyWorkViewModel(repo)
        repo.myWorkResult = Result.success(HumanWork("ready", mapOf("queued" to listOf(reference(72).copy(version = 4), reference(73))), false, null))
        viewModel.loadMore()
        assertEquals(72, repo.lastAfterId)
        assertEquals(listOf(72, 73), viewModel.uiState.value.visibleWork.map { it.id })
        assertEquals(4, viewModel.uiState.value.visibleWork.first().version)
    }

    @Test fun reviewQueueIsSeparateAndAvailableToAnUnlinkedHuman() = runTest {
        val repo = repository()
        repo.identityResult = Result.success(Identity(true, IdentityPrincipal(19, "human"), null))
        repo.myWorkResult = Result.success(HumanWork("profile_unlinked", emptyMap(), false, null))
        repo.reviewQueueResult = Result.success(TaskReferencePage(listOf(reference(80).copy(status = "resolved", ownerProfileId = 8)), false, null))
        val viewModel = MyWorkViewModel(repo)
        assertEquals("profile_unlinked", viewModel.uiState.value.workState)
        assertTrue(viewModel.uiState.value.visibleWork.isEmpty())
        viewModel.setFilter(TaskFilter.REVIEW)
        assertEquals(80, viewModel.uiState.value.visibleWork.single().id)
    }

    @Test fun missingIdentityOrRevokedSelectionCannotShowPrivateWork() = runTest {
        val repo = repository()
        val viewModel = MyWorkViewModel(repo)
        assertTrue(viewModel.uiState.value.visibleWork.isNotEmpty())
        repo.projectsResult = Result.success(emptyList())
        viewModel.selectProject(9)
        assertTrue(viewModel.uiState.value.visibleWork.isEmpty())
        assertTrue(viewModel.uiState.value.errorMessage!!.contains("no longer accessible"))
        repo.identityResult = Result.success(Identity())
        viewModel.refresh()
        assertTrue(viewModel.uiState.value.visibleWork.isEmpty())
        assertTrue(viewModel.uiState.value.projects.isEmpty())
        assertNull(viewModel.uiState.value.identity)
        assertTrue(viewModel.uiState.value.errorMessage!!.contains("Sign in"))
    }

    @Test fun unsupportedCapabilityDoesNotFallBackToTeamIterationTasks() = runTest {
        val repo = repository()
        repo.capabilitiesResult = Result.success(DomainCapabilities(2, true, listOf("human-my-work-v1")))
        val viewModel = MyWorkViewModel(repo)
        assertTrue(viewModel.uiState.value.visibleWork.isEmpty())
        assertEquals(0, repo.fetchTasksCallCount)
        assertNull(repo.lastFetchIterationId)
    }

    @Test fun unsupportedSavedFiltersCanBeClearedWithoutLosingAccountScope() = runTest {
        val repo = repository()
        repo.workSelection = WorkSelection(projectId = 9)
        repo.capabilitiesResult = Result.success(DomainCapabilities(1, true, listOf("human-my-work-v1")))
        val viewModel = MyWorkViewModel(repo)
        assertTrue(viewModel.uiState.value.errorMessage!!.contains("saved work filters"))
        assertTrue(viewModel.uiState.value.visibleWork.isEmpty())
        viewModel.clearScope()
        assertEquals(72, viewModel.uiState.value.visibleWork.single().id)
        assertNull(repo.lastSelection!!.projectId)
        assertEquals(19, viewModel.uiState.value.identity!!.principal!!.id)
    }

    @Test fun temporaryFailureShowsDatedCacheAndForbiddenRefreshRemovesIt() = runTest {
        val repo = repository()
        val viewModel = MyWorkViewModel(repo)
        repo.myWorkResult = Result.failure(java.io.IOException("Offline"))
        viewModel.refresh()
        assertEquals("cache", viewModel.uiState.value.source)
        assertNotNull(viewModel.uiState.value.fetchedAt)
        assertEquals(72, viewModel.uiState.value.visibleWork.single().id)
        repo.myWorkResult = Result.failure(ApiProblem(403, ProblemDetail("resource_unavailable", "Revoked")))
        viewModel.refresh()
        assertEquals("unavailable", viewModel.uiState.value.source)
        assertTrue(viewModel.uiState.value.visibleWork.isEmpty())
    }
}
