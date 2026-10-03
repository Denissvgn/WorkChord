package com.workchord.android.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.workchord.android.R
import com.workchord.android.data.models.TaskReference
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.ui.components.StatusChip
import com.workchord.android.ui.viewmodels.MyWorkViewModel
import com.workchord.android.ui.viewmodels.TaskFilter

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyWorkScreen(viewModel: MyWorkViewModel, onTaskClick: (Int) -> Unit, modifier: Modifier = Modifier) {
    val state by viewModel.uiState.collectAsState()
    val lifecycle = LocalLifecycleOwner.current
    DisposableEffect(lifecycle, viewModel) {
        val observer = LifecycleEventObserver { _, event -> if (event == Lifecycle.Event.ON_RESUME) viewModel.refresh() }
        lifecycle.lifecycle.addObserver(observer)
        onDispose { lifecycle.lifecycle.removeObserver(observer) }
    }
    Scaffold(modifier.fillMaxSize(), topBar = {
        TopAppBar(title = { Text(stringResource(R.string.my_work_title)) }, actions = {
            IconButton(onClick = { viewModel.refresh() }, enabled = !state.isLoading && !state.isRefreshing) {
                Icon(Icons.Default.Refresh, contentDescription = stringResource(R.string.work_refresh))
            }
        })
    }) { padding ->
        LazyColumn(Modifier.fillMaxSize().padding(padding), contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)) {
            item { Text(stringResource(R.string.work_help), style = MaterialTheme.typography.bodyLarge) }
            state.fetchedAt?.let { timestamp -> item {
                Text("${state.source} · ${java.time.Instant.ofEpochMilli(timestamp)}", style = MaterialTheme.typography.bodyMedium)
            } }
            item {
                ScopeMenu(if (state.selection.projectId == null) stringResource(R.string.work_all_projects)
                    else state.projects.firstOrNull { it.id == state.selection.projectId }?.name ?: stringResource(R.string.work_selection_unavailable),
                    state.filtersSupported && !state.isLoading) { dismiss ->
                    DropdownMenuItem(text = { Text(stringResource(R.string.work_all_projects)) }, onClick = { dismiss(); viewModel.selectProject(null) })
                    state.projects.forEach { project -> DropdownMenuItem(text = { Text(project.name) }, onClick = { dismiss(); viewModel.selectProject(project.id) }) }
                }
                ScopeMenu(if (state.selection.backlogOnly) stringResource(R.string.work_backlog)
                    else if (state.selection.iterationId == null) stringResource(R.string.work_all_iterations)
                    else state.iterations.firstOrNull { it.id == state.selection.iterationId }?.name ?: stringResource(R.string.work_selection_unavailable),
                    state.filtersSupported && !state.isLoading) { dismiss ->
                    DropdownMenuItem(text = { Text(stringResource(R.string.work_all_iterations)) }, onClick = { dismiss(); viewModel.selectIteration(null) })
                    DropdownMenuItem(text = { Text(stringResource(R.string.work_backlog)) }, onClick = { dismiss(); viewModel.selectBacklog() })
                    state.iterations.filter { state.selection.projectId == null || it.projectId == null || it.projectId == state.selection.projectId }
                        .forEach { iteration -> DropdownMenuItem(text = { Text(iteration.name) }, onClick = { dismiss(); viewModel.selectIteration(iteration.id) }) }
                }
                if (state.selection.projectId != null || state.selection.iterationId != null || state.selection.backlogOnly) {
                    TextButton(onClick = { viewModel.clearScope() }, enabled = !state.isLoading) { Text(stringResource(R.string.work_clear_scope)) }
                }
            }
            item {
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(TaskFilter.entries) { filter -> FilterChip(selected = state.selectedFilter == filter,
                        onClick = { viewModel.setFilter(filter) }, label = { Text(queueTitle(filter)) }, enabled = !state.isLoading) }
                }
            }
            if (state.isLoading || state.isRefreshing) item { LinearProgressIndicator(Modifier.fillMaxWidth()) }
            state.errorMessage?.let { message -> item {
                Text(message, color = MaterialTheme.colorScheme.error)
                TextButton(onClick = { viewModel.loadData() }) { Text(stringResource(R.string.work_refresh)) }
            } }
            when (state.workState) {
                "profile_unlinked" -> item { Text(stringResource(R.string.work_profile_unlinked)) }
                "membership_required" -> item { Text(stringResource(R.string.work_no_membership)) }
            }
            if (!state.isLoading && state.errorMessage == null && state.workState == "ready" && state.visibleWork.isEmpty() && !state.hasMore) {
                item { Text(stringResource(R.string.work_no_results), style = MaterialTheme.typography.bodyLarge) }
            }
            items(state.visibleWork, key = { it.id }) { task ->
                WorkRow(task, onClick = { onTaskClick(task.id) }, onParent = { id -> onTaskClick(id) })
            }
            if (state.hasMore) item {
                Text(stringResource(R.string.work_partial), style = MaterialTheme.typography.bodyMedium)
                if (state.nextAfterId != null) OutlinedButton(onClick = { viewModel.loadMore() }, enabled = !state.isRefreshing) {
                    Text(stringResource(R.string.work_load_more))
                }
            }
        }
    }
}

@Composable
private fun queueTitle(filter: TaskFilter) = stringResource(when (filter) {
    TaskFilter.ALL -> R.string.work_all
    TaskFilter.ACTIVE -> R.string.status_active
    TaskFilter.QUEUED -> R.string.work_queued
    TaskFilter.BLOCKED -> R.string.status_blocked
    TaskFilter.RESOLVED -> R.string.work_awaiting_review
    TaskFilter.REVIEW -> R.string.work_review
})

@Composable
private fun ScopeMenu(label: String, enabled: Boolean, content: @Composable ((() -> Unit) -> Unit)) {
    var expanded by remember { mutableStateOf(false) }
    Box {
        OutlinedButton(onClick = { expanded = true }, enabled = enabled, modifier = Modifier.fillMaxWidth()) {
            Text(label, maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
        DropdownMenu(expanded, onDismissRequest = { expanded = false }) { content { expanded = false } }
    }
}

@Composable
private fun WorkRow(task: TaskReference, onClick: () -> Unit, onParent: (Int) -> Unit) {
    Column(Modifier.fillMaxWidth().clickable(onClick = onClick).padding(vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(task.title, style = MaterialTheme.typography.titleMedium, maxLines = 3, overflow = TextOverflow.Ellipsis)
        Text(listOfNotNull(task.projectName, task.iterationName ?: if (task.iterationId == null) stringResource(R.string.work_backlog)
            else stringResource(R.string.work_iteration, task.iterationId)).joinToString(" · "),
            style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        StatusChip(TaskStatus.fromString(task.status))
        if (task.status == "closed" && task.acceptanceCurrent != true) Text(stringResource(R.string.work_acceptance_unverified))
        task.blockedReason?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodyMedium) }
        task.parentId?.let { id -> TextButton(onClick = { onParent(id) }) { Text(stringResource(R.string.work_parent, id)) } }
    }
    HorizontalDivider()
}
