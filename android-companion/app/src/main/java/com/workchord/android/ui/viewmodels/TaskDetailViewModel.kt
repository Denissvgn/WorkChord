package com.workchord.android.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.workchord.android.data.models.AcceptanceCriterion
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.data.models.TaskCommandRequest
import com.workchord.android.data.models.TaskDetail
import com.workchord.android.data.repository.TaskRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class TaskDetailUiState(
    val isLoading: Boolean = false,
    val isUpdatingStatus: Boolean = false,
    val task: Task? = null,
    val detail: TaskDetail? = null,
    val acceptanceCriteria: List<AcceptanceCriterion> = emptyList(),
    val errorMessage: String? = null,
    val successMessage: String? = null
)

class TaskDetailViewModel(
    private val taskId: Int,
    private val repository: TaskRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(TaskDetailUiState(isLoading = true))
    val uiState: StateFlow<TaskDetailUiState> = _uiState.asStateFlow()

    init {
        loadTask()
        observeTask()
    }

    private fun observeTask() {
        viewModelScope.launch {
            repository.observeTask(taskId).collect { updatedTask ->
                if (updatedTask != null) {
                    _uiState.update {
                        it.copy(
                            task = updatedTask,
                            acceptanceCriteria = updatedTask.extractAcceptanceCriteria()
                        )
                    }
                }
            }
        }
    }

    fun loadTask() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null) }
            val result = repository.getTaskDetail(taskId)
            result.fold(
                onSuccess = { detail ->
                    val task = detail.task
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            task = task,
                            detail = detail,
                            acceptanceCriteria = task.extractAcceptanceCriteria(),
                            errorMessage = null
                        )
                    }
                },
                onFailure = { exception ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            errorMessage = exception.localizedMessage ?: "Failed to load task details"
                        )
                    }
                }
            )
        }
    }

    fun startTask() {
        transitionStatus(TaskStatus.ACTIVE, "Task started by mobile user")
    }

    fun resolveTask() {
        transitionStatus(TaskStatus.RESOLVED, "Task marked resolved from mobile companion")
    }

    fun blockTask(reason: String = "Blocked pending investigation") {
        val task = _uiState.value.task ?: return
        val version = task.authoritativeVersion ?: return
        viewModelScope.launch {
            _uiState.update { it.copy(isUpdatingStatus = true, errorMessage = null) }
            repository.executeCommand(task.id, TaskCommandRequest("block", version, reason)).fold(
                onSuccess = { updated -> _uiState.update { it.copy(task = updated, isUpdatingStatus = false, successMessage = "Work is blocked") } },
                onFailure = { error -> _uiState.update { it.copy(isUpdatingStatus = false, errorMessage = error.localizedMessage) } })
        }
    }

    fun reopenTask() {
        transitionStatus(TaskStatus.ACTIVE, "Rework requested")
    }

    fun closeTask() {
        transitionStatus(TaskStatus.CLOSED, "Task verified and closed")
    }

    private fun transitionStatus(newStatus: TaskStatus, reason: String) {
        val currentTask = _uiState.value.task ?: return
        viewModelScope.launch {
            _uiState.update { it.copy(isUpdatingStatus = true, errorMessage = null, successMessage = null) }
            val result = repository.updateTaskStatus(
                taskId = currentTask.id,
                newStatus = newStatus,
                reason = reason,
                expectedVersion = currentTask.version
            )
            result.fold(
                onSuccess = { updatedTask ->
                    _uiState.update {
                        it.copy(
                            isUpdatingStatus = false,
                            task = updatedTask,
                            acceptanceCriteria = updatedTask.extractAcceptanceCriteria(),
                            successMessage = "Status transitioned to ${newStatus.displayName}"
                        )
                    }
                },
                onFailure = { exception ->
                    _uiState.update {
                        it.copy(
                            isUpdatingStatus = false,
                            errorMessage = exception.localizedMessage ?: "Status transition failed"
                        )
                    }
                }
            )
        }
    }

    fun toggleAcceptanceCriterion(index: Int) {
        if (index !in _uiState.value.acceptanceCriteria.indices) return
        _uiState.update { it.copy(errorMessage = "Criterion completion requires a canonical criterion and persisted execution evidence.") }
    }

    fun clearMessages() {
        _uiState.update { it.copy(errorMessage = null, successMessage = null) }
    }
}
