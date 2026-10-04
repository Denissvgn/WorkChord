package com.workchord.android.data.models

data class EvidenceDraft(val base: Task, val criteria: List<CriterionProgress>, val artifacts: String = "")
data class SavedTaskDraft(val schemaVersion: Int = 1, val evidence: EvidenceDraft? = null,
    val reason: String = "", val reviewEvidence: String = "", val savedAt: Long)
data class TaskReadState(val detail: TaskDetail, val fetchedAt: Long, val source: String = "remote",
    val authoritative: Boolean = true, val problem: ApiProblem? = null)
