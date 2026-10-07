package com.workchord.android.ui.screens

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import com.workchord.android.R
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import com.workchord.android.ui.components.PriorityBadge
import com.workchord.android.ui.components.StatusChip
import com.workchord.android.ui.viewmodels.TaskDetailViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TaskDetailScreen(viewModel: TaskDetailViewModel, onNavigateBack: () -> Unit,
    onNavigateTask: (Int) -> Unit = {}, modifier: Modifier = Modifier) {
    val state by viewModel.uiState.collectAsState()
    val lifecycle = LocalLifecycleOwner.current
    DisposableEffect(lifecycle, viewModel) {
        val observer = LifecycleEventObserver { _, event -> if (event == Lifecycle.Event.ON_RESUME) viewModel.loadTask() }
        lifecycle.lifecycle.addObserver(observer)
        onDispose { lifecycle.lifecycle.removeObserver(observer) }
    }
    var pendingExit by remember { mutableStateOf<(() -> Unit)?>(null) }
    fun leave(action: () -> Unit) { if (state.hasUnsavedInputs) pendingExit = action else action() }
    BackHandler(state.hasUnsavedInputs) { pendingExit = onNavigateBack }
    pendingExit?.let { action -> AlertDialog(onDismissRequest = { pendingExit = null },
        title = { Text("Unsaved evidence") }, text = { Text("These changes have not been saved to the server. Stay to keep editing, or discard them before leaving.") },
        confirmButton = { TextButton(onClick = { viewModel.discardInputs { pendingExit = null; action() } }) { Text("Discard and leave") } },
        dismissButton = { TextButton(onClick = { pendingExit = null }) { Text("Stay") } }) }
    Scaffold(modifier.fillMaxSize().imePadding(), topBar = {
        TopAppBar(title = { Text(state.task?.let { "Task #${it.id}" } ?: "Task") }, navigationIcon = {
            IconButton(onClick = { leave(onNavigateBack) }) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back") }
        })
    }) { padding ->
        LazyColumn(Modifier.fillMaxSize().padding(padding), contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)) {
            if (state.isLoading || state.isUpdatingStatus) item { LinearProgressIndicator(Modifier.fillMaxWidth()) }
            state.errorMessage?.let { message -> item {
                Text(message, color = MaterialTheme.colorScheme.error)
                OutlinedButton(onClick = { viewModel.loadTask() }, enabled = !state.isUpdatingStatus) { Text("Reload current task") }
            } }
            state.successMessage?.let { item { Text(it, style = MaterialTheme.typography.bodyMedium) } }
            if (state.hasUnsavedInputs) item {
                OutlinedButton(onClick = { viewModel.saveLocalDraft() }, enabled = !state.isUpdatingStatus) { Text("Save draft on this device") }
            }
            val task = state.task
            if (task != null) {
                item {
                    Text(task.title, style = MaterialTheme.typography.headlineSmall)
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        StatusChip(task.status); PriorityBadge(task.priority)
                    }
                    Text(task.owner?.name?.let { "Owner: $it" } ?: task.ownerProfileId?.let { "Owner profile: #$it" } ?: "Unassigned human owner")
                    Text(task.effortHours?.let { "Effort: $it hours" } ?: "Unestimated")
                    task.blockedReason?.let { Text("Blocked: $it", color = MaterialTheme.colorScheme.error) }
                    task.canceledReason?.let { Text("Canceled: $it", color = MaterialTheme.colorScheme.error) }
                }
                state.detail?.ancestors.orEmpty().forEach { ancestor -> item(key = "parent-${ancestor.id}") {
                    TextButton(onClick = { leave { onNavigateTask(ancestor.id) } }) { Text("Parent #${ancestor.id} · ${ancestor.title}") }
                } }
                state.detail?.children?.items.orEmpty().forEach { child -> item(key = "child-${child.id}") {
                    TextButton(onClick = { leave { onNavigateTask(child.id) } }) { Text("Child #${child.id} · ${child.title}") }
                } }
                if (state.detail?.children?.hasMore == true) item {
                    OutlinedButton(onClick = { viewModel.loadMoreRelations(true) }, enabled = !state.isLoadingRelations && state.authoritative) {
                        Text(stringResource(R.string.more_children))
                    }
                }
                state.detail?.dependencies?.items.orEmpty().forEach { dependency -> item(key = "dependency-${dependency.id}") {
                    TextButton(onClick = { onNavigateTask(dependency.id) }) { Text("#${dependency.id} · ${dependency.title}") }
                } }
                if (state.detail?.dependencies?.hasMore == true) item {
                    OutlinedButton(onClick = { viewModel.loadMoreRelations(false) }, enabled = !state.isLoadingRelations && state.authoritative) {
                        Text(stringResource(R.string.more_dependencies))
                    }
                }
                state.relationError?.let { message -> item { Text(message, color = MaterialTheme.colorScheme.error) } }
                if (state.detail?.children?.hasMore != false || state.detail?.dependencies?.hasMore != false) item {
                    Text(stringResource(R.string.bounded_relations))
                }
                item {
                    Text("Brief", style = MaterialTheme.typography.titleLarge)
                    Text(task.brief?.goal?.takeIf { it.isNotBlank() } ?: task.description?.takeIf { it.isNotBlank() } ?: stringResource(R.string.brief_missing))
                    listOf("Context" to task.brief?.context, "Scope" to task.brief?.scope, "Exclusions" to task.brief?.exclusions,
                        "Verification" to task.brief?.verification, "Artifacts" to task.brief?.artifactExpectations)
                        .filter { !it.second.isNullOrBlank() }.forEach { (label, value) ->
                            Text(label, style = MaterialTheme.typography.titleMedium); Text(value.orEmpty())
                        }
                }
                item {
                    Text("Execution evidence", style = MaterialTheme.typography.titleLarge)
                    Text("Recorded progress is separate from independent acceptance.")
                    if (state.draft == null) OutlinedButton(onClick = { viewModel.beginEvidenceEdit() },
                        enabled = state.allowed("record_progress") && task.brief?.schemaVersion == 1) { Text("Edit evidence") }
                    if (task.brief?.schemaVersion != 1) Text(stringResource(R.string.criteria_missing))
                }
                state.acceptanceCriteria.forEach { criterion -> item(key = "criterion-${criterion.id ?: criterion.text}") {
                    val draft = state.draft?.criteria?.firstOrNull { it.criterionId == criterion.id }
                    Text(criterion.text, style = MaterialTheme.typography.titleMedium)
                    criterion.verification?.takeIf { it.isNotBlank() }?.let { Text("Verify: $it") }
                    if (draft == null) {
                        Text("Recorded state: ${criterion.state}")
                        criterion.evidence?.takeIf { it.isNotBlank() }?.let { Text(it) }
                    } else {
                        Text("Local draft · not saved", style = MaterialTheme.typography.labelLarge)
                        Row {
                            Checkbox(draft.state == "completed", onCheckedChange = { complete ->
                                criterion.id?.let { viewModel.setCriterion(it, progress = if (complete) "completed" else "pending") }
                            }, enabled = !state.isUpdatingStatus)
                            Text("Completed with evidence", Modifier.padding(top = 12.dp))
                        }
                        OutlinedTextField(draft.evidence.orEmpty(), onValueChange = { value -> criterion.id?.let { viewModel.setCriterion(it, evidence = value) } },
                            label = { Text("Criterion evidence") }, modifier = Modifier.fillMaxWidth(), minLines = 2,
                            enabled = !state.isUpdatingStatus)
                    }
                } }
                state.draft?.let { draft -> item {
                    OutlinedTextField(draft.artifacts, { viewModel.setArtifacts(it) }, label = { Text("Artifact URLs, one per line") },
                        modifier = Modifier.fillMaxWidth(), minLines = 2, enabled = !state.isUpdatingStatus)
                    Text("Draft based on task version ${draft.base.version}; current version ${task.version}.")
                    if (draft.base.version != task.version || state.conflict != null) {
                        Text("Compare the current brief above with your retained draft. Nothing has been retried automatically.")
                        OutlinedButton(onClick = { viewModel.reconcileDraft() }, enabled = state.authoritative) { Text("Keep draft with current revision") }
                    }
                    Button(onClick = { viewModel.saveProgress() }, enabled = state.allowed("record_progress") && draft.base.version == task.version) { Text("Save evidence") }
                    TextButton(onClick = { viewModel.discardDraft() }, enabled = !state.isUpdatingStatus) { Text("Discard evidence draft") }
                } }
                item {
                    Text("Work actions", style = MaterialTheme.typography.titleLarge)
                    OutlinedTextField(state.reason, { viewModel.setReason(it) }, label = { Text("Reason for action or review") },
                        modifier = Modifier.fillMaxWidth(), minLines = 2, enabled = !state.isUpdatingStatus)
                }
                for ((action, label) in listOf("start_manual" to "Start manual work", "resolve_manual" to "Resolve manual work",
                    "block" to "Block work", "unblock" to "Unblock work", "cancel" to "Cancel work", "reopen" to "Reopen work")) {
                    item(key = action) {
                        OutlinedButton(onClick = { viewModel.execute(action) }, enabled = state.allowed(action) && state.reason.isNotBlank(), modifier = Modifier.fillMaxWidth()) { Text(label) }
                        state.blockers(action).firstOrNull()?.let { Text(it.message, style = MaterialTheme.typography.bodyMedium) }
                    }
                }
                item {
                    Text("Independent review", style = MaterialTheme.typography.titleLarge)
                    OutlinedTextField(state.reviewEvidence, { viewModel.setReviewEvidence(it) }, label = { Text("Review evidence") },
                        modifier = Modifier.fillMaxWidth(), minLines = 2, enabled = !state.isUpdatingStatus)
                    Button(onClick = { viewModel.submitReview("accept") }, enabled = state.allowed("accept_review") && state.reason.isNotBlank()) { Text("Accept current evidence") }
                    OutlinedButton(onClick = { viewModel.submitReview("reject") }, enabled = state.allowed("review") && state.reason.isNotBlank()) { Text("Reject for rework") }
                    (state.blockers("accept_review") + state.blockers("review")).distinctBy { it.code }.forEach { Text(it.message) }
                    if (!state.authoritative) Text("Current acceptance is not verified while this view is unavailable or cached.")
                    else state.currentReview?.let { Text("Current verdict: ${it.verdict} · ${it.reason}") }
                        ?: Text("No current independent verdict recorded.")
                }
                state.reviews.forEach { review -> item(key = "review-${review.id}") {
                    Text("${review.verdict} · task version ${review.taskVersion} · brief ${review.briefRevision} · artifact ${review.artifactRevision}")
                    Text(review.principalId?.let { "Reviewer #$it · ${review.createdAt}" } ?: "Unattributed review · ${review.createdAt}")
                    Text(review.reason)
                    if (review.evidence.isNotBlank()) Text(review.evidence)
                } }
            } else if (!state.isLoading) item { Text("This work is not currently available.") }
        }
    }
}
