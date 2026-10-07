package com.workchord.android

import com.workchord.android.data.models.*
import com.workchord.android.fakes.FakeTaskRepository
import com.workchord.android.ui.viewmodels.TaskDetailViewModel
import com.workchord.android.util.MainDispatcherRule
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.runTest
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class TaskDetailViewModelTest {
    @get:Rule val mainDispatcherRule = MainDispatcherRule()
    private val task = Task(72, title = "Reviewed outline", statusRaw = "active", version = 3,
        brief = TaskBrief(1, goal = "Deliver an outline", acceptanceCriteria = listOf(BriefCriterion("outline", 2, "A clear outline", "Read revision"))),
        briefRevision = 1, artifactRevision = 0, ownerProfileId = 7)
    private fun repository() = FakeTaskRepository(listOf(task))

    @Test fun unavailableActionsNeverIssueACommand() = runTest {
        val repo = repository()
        repo.actionsResult = Result.success(TaskActions(72, 3, listOf(AllowedAction("start_manual", false,
            listOf(ActionBlocker("invalid_lifecycle", "Already active")))), 0, emptyList(), emptyList()))
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        viewModel.setReason("Begin work")
        viewModel.execute("start_manual")
        assertEquals(0, repo.commandCalls)
        assertNotNull(viewModel.uiState.value.errorMessage)
    }

    @Test fun canonicalBlockAndReopenUseCurrentVersionAndOwnershipEvidence() = runTest {
        val repo = repository()
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        viewModel.setReason("Waiting for input")
        viewModel.execute("block")
        assertEquals("block", repo.lastCommand)
        assertEquals(3, repo.lastExpectedVersion)
        assertEquals("Waiting for input", viewModel.uiState.value.task!!.blockedReason)
        viewModel.setReason("Restore canceled work")
        viewModel.execute("reopen")
        assertEquals("reopen", repo.lastCommand)
        assertEquals(4, repo.lastExpectedVersion)
    }

    @Test fun completionRequiresEvidenceAndPersistsStableCriterionIdentity() = runTest {
        val repo = repository()
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        viewModel.beginEvidenceEdit()
        viewModel.setCriterion("outline", progress = "completed")
        viewModel.saveProgress()
        assertNull(repo.lastProgress)
        assertNotNull(viewModel.uiState.value.draft)
        viewModel.setCriterion("outline", evidence = "Outline revision abc123")
        viewModel.saveProgress()
        assertEquals(3, repo.lastProgress!!.expectedVersion)
        assertEquals("outline", repo.lastProgress!!.criteria.single().criterionId)
        assertEquals(2, repo.lastProgress!!.criteria.single().criterionRevision)
        assertTrue(viewModel.uiState.value.acceptanceCriteria.single().isCompleted)
        assertNull(viewModel.uiState.value.draft)
        assertNull(viewModel.uiState.value.currentReview)
    }

    @Test fun conflictPreservesDraftAndRequiresExplicitCurrentRevisionReconciliation() = runTest {
        val repo = repository()
        val current = task.copy(version = 4, title = "Changed outline")
        repo.progressResult = Result.failure(ApiProblem(409, ProblemDetail("task_version_conflict", "Changed", currentTask = current)))
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        viewModel.beginEvidenceEdit()
        viewModel.setCriterion("outline", progress = "completed", evidence = "Retained evidence")
        viewModel.saveProgress()
        assertEquals(3, viewModel.uiState.value.draft!!.base.version)
        assertEquals("Retained evidence", viewModel.uiState.value.draft!!.criteria.single().evidence)
        assertFalse(viewModel.uiState.value.authoritative)
        repo.setTasks(listOf(current))
        viewModel.loadTask()
        viewModel.reconcileDraft()
        assertEquals(4, viewModel.uiState.value.draft!!.base.version)
        repo.progressResult = null
        viewModel.saveProgress()
        assertEquals(4, repo.lastProgress!!.expectedVersion)
    }

    @Test fun changedCriterionRevisionPreventsBlindDraftReapply() = runTest {
        val repo = repository()
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        viewModel.beginEvidenceEdit()
        val changed = task.copy(version = 4, brief = task.brief!!.copy(acceptanceCriteria = listOf(BriefCriterion("outline", 3, "New requirement"))))
        repo.setTasks(listOf(changed))
        viewModel.loadTask()
        viewModel.reconcileDraft()
        assertEquals(3, viewModel.uiState.value.draft!!.base.version)
        assertTrue(viewModel.uiState.value.errorMessage!!.contains("Criteria changed"))
    }

    @Test fun independentVerdictUsesCurrentBriefAndArtifactRevisions() = runTest {
        val repo = repository()
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        viewModel.setReason("The result needs more detail")
        viewModel.setReviewEvidence("Independent comparison to the brief")
        viewModel.submitReview("reject")
        assertEquals("reject", repo.lastReview!!.verdict)
        assertEquals(1, repo.lastReview!!.briefRevision)
        assertEquals(0, repo.lastReview!!.artifactRevision)
        assertEquals("reject", viewModel.uiState.value.currentReview!!.verdict)
    }

    @Test fun mismatchedReadVersionsDisableAllMutationActions() = runTest {
        val repo = repository()
        repo.actionsResult = Result.success(TaskActions(72, 4, listOf(AllowedAction("record_progress", true)), 0, emptyList(), emptyList()))
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        assertFalse(viewModel.uiState.value.authoritative)
        assertFalse(viewModel.uiState.value.allowed("record_progress"))
        assertNotNull(viewModel.uiState.value.errorMessage)
    }

    @Test fun savedDraftRestoresAfterAuthorizedReadAndKeepsItsOriginalVersion() = runTest {
        val repo = repository()
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        viewModel.beginEvidenceEdit()
        viewModel.setCriterion("outline", evidence = "Explicitly saved local work")
        viewModel.saveLocalDraft()
        repo.setTasks(listOf(task.copy(version = 4)))
        val restored = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        assertEquals("Explicitly saved local work", restored.uiState.value.draft!!.criteria.single().evidence)
        assertEquals(3, restored.uiState.value.draft!!.base.version)
        assertEquals(4, restored.uiState.value.task!!.version)
        assertNull(repo.lastProgress)
    }

    @Test fun networkCacheIsReadOnlyButAccessLossClearsPrivateContent() = runTest {
        val repo = repository()
        val viewModel = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        val detail = viewModel.uiState.value.detail!!
        repo.cachedDetail = TaskReadState(detail, 1000)
        repo.getTaskByIdResult = Result.failure(java.io.IOException("Offline"))
        viewModel.loadTask()
        assertEquals(72, viewModel.uiState.value.task!!.id)
        assertFalse(viewModel.uiState.value.authoritative)
        assertTrue(viewModel.uiState.value.errorMessage!!.contains("Cached read-only"))
        repo.getTaskByIdResult = Result.failure(ApiProblem(403, ProblemDetail("resource_unavailable", "Access revoked")))
        viewModel.loadTask()
        assertNull(viewModel.uiState.value.task)
        assertNull(viewModel.uiState.value.detail)
        assertFalse(viewModel.uiState.value.authoritative)
    }
    @Test fun relationPagesAppendWithoutLosingDraftsAndRejectVersionChanges() = runTest {
        val repo = repository()
        val child = TaskReference(90, "Child", 1, "planned", 1, null, 72, 7)
        val detail = TaskDetail(task, emptyList(), true, TaskReferencePage(listOf(child), true, 90), TaskReferencePage(emptyList(), false, null), false)
        repo.detailResult = Result.success(detail)
        repo.detailPageResult = Result.success(detail.copy(children = TaskReferencePage(listOf(child.copy(id = 91)), false, null)))
        val model = TaskDetailViewModel(72, repo, mainDispatcherRule.testDispatcher)
        model.setReason("Keep this draft")
        model.loadMoreRelations(true)
        assertEquals(listOf(90, 91), model.uiState.value.detail!!.children.items!!.map { it.id })
        assertEquals("Keep this draft", model.uiState.value.reason)
        assertEquals(90, repo.lastChildrenCursor)
        repo.detailResult = Result.success(detail)
        model.loadTask()
        repo.detailPageResult = Result.success(detail.copy(task = task.copy(version = 4)))
        model.loadMoreRelations(true)
        assertFalse(model.uiState.value.authoritative)
        assertEquals(listOf(90), model.uiState.value.detail!!.children.items!!.map { it.id })
    }

}
