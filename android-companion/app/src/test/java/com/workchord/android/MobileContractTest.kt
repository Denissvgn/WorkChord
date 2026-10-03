package com.workchord.android

import com.google.gson.Gson
import com.google.gson.JsonObject
import com.google.gson.annotations.SerializedName
import com.workchord.android.data.models.*
import okhttp3.Cookie
import okhttp3.HttpUrl.Companion.toHttpUrl
import org.junit.Assert.*
import org.junit.Test

class MobileContractTest {
    private val gson = Gson()
    private val root = gson.fromJson(javaClass.classLoader!!.getResourceAsStream("mobile-contract-v1.json")!!.bufferedReader(), JsonObject::class.java)
    private val examples = root.getAsJsonObject("examples")

    @Test
    fun nestedAndBacklogTasksKeepCanonicalCriteriaUnitsAndNulls() {
        val parent = gson.fromJson(examples["nested_task"], Task::class.java)
        assertEquals(0.25, parent.effortDays!!, 0.00001)
        assertEquals(1.5, parent.effortHours!!, 0.00001)
        assertEquals(6.0, parent.nominalDayHours!!, 0.00001)
        val task = parent.children!!.single()
        assertNull(task.iterationId)
        assertNull(task.startDate)
        assertNull(task.effortHours)
        assertEquals(4, task.ownerProfileId)
        assertEquals("Waiting for feedback", task.blockedReason)
        assertEquals(TaskStatus.ACTIVE, task.status)
        val criterion = task.extractAcceptanceCriteria().single()
        assertEquals("outline", criterion.id)
        assertEquals(2, criterion.revision)
        assertEquals("Open the saved outline", criterion.verification)
        assertEquals("Outline revision abc123", criterion.evidence)
        assertTrue(criterion.isCompleted)
        assertEquals("Deliver a reviewed outline", task.extractGoal())
        assertFalse(task.copy(artifactRevision = 3).extractAcceptanceCriteria().single().isCompleted)
        assertFalse(task.copy(briefRevision = 4).extractAcceptanceCriteria().single().isCompleted)
    }

    @Test
    fun legacyPayloadsRemainReadableWithoutInventingEvidence() {
        val task = gson.fromJson(examples["legacy_task"], Task::class.java)
        assertEquals(TaskStatus.PLANNED, task.status)
        assertEquals(5, task.iterationId)
        assertNull(task.brief)
        assertFalse(task.extractAcceptanceCriteria().single().isCompleted)
        assertNull(task.extractAcceptanceCriteria().single().id)
        val incomplete = gson.fromJson("{\"id\":9,\"title\":\"Incomplete\"}", Task::class.java)
        assertEquals(TaskStatus.UNKNOWN, incomplete.status)
        assertNull(incomplete.authoritativeVersion)
        assertEquals(TaskStatus.UNKNOWN, TaskStatus.fromString("blocked"))
        assertEquals(TaskStatus.UNKNOWN, TaskStatus.fromString("future_status"))
    }

    @Test
    fun unsupportedCapabilitiesAndBriefVersionsStayUnknown() {
        val unknown = gson.fromJson("{\"schema_version\":2,\"ready\":true,\"features\":[\"task-actions-v1\"]}", DomainCapabilities::class.java)
        assertFalse(unknown.supports("task-actions-v1"))
        assertFalse(gson.fromJson("{}", DomainCapabilities::class.java).supports("task-actions-v1"))
        val task = gson.fromJson(examples["backlog_task"], Task::class.java)
        assertTrue(task.copy(brief = task.brief!!.copy(schemaVersion = 2)).extractAcceptanceCriteria().isEmpty())
    }

    @Test
    fun boundedDetailActionsStatusCascadesAndReviewDeserialize() {
        val detail = gson.fromJson(examples["detail"], TaskDetail::class.java)
        assertEquals(71, detail.ancestors!!.single().id)
        assertEquals(true, detail.ancestorsComplete)
        assertEquals(true, detail.dependencies.hasMore)
        assertEquals(72, detail.dependencies.nextAfterId)
        assertEquals(false, detail.executionContextComplete)
        val actions = gson.fromJson(examples["actions"], TaskActions::class.java)
        assertEquals(7, actions.version)
        assertFalse(actions.actions!!.first().allowed)
        assertEquals("dependencies_incomplete", actions.actions.first().blockers!!.single().code)
        val changed = gson.fromJson(examples["status_change"], TaskStatusChangeResponse::class.java)
        assertEquals(8, changed.task.version)
        assertEquals(TaskStatus.RESOLVED, changed.task.status)
        assertEquals("2026-10-05", changed.cascadeUpdates!!.single().newStartDate)
        val review = gson.fromJson(examples["review"], TaskReview::class.java)
        assertEquals("reject", review.verdict)
        assertEquals(2, review.artifactRevision)
    }

    @Test
    fun structuredConflictAndActualServerCookieRemainIntact() {
        val conflict = ApiProblem.parse(409, examples["conflict"].toString())
        assertEquals("task_version_conflict", conflict.problem.code)
        assertEquals(7, conflict.problem.expectedVersion)
        assertEquals(8, conflict.problem.currentTask!!.version)
        assertTrue(ApiProblem.parse(422, "{\"detail\":[{\"msg\":\"Invalid inputs\"}]}").message!!.contains("Review"))
        val validation = ApiProblem.parse(422, "{\"detail\":[{\"loc\":[\"body\",\"expected_version\"],\"type\":\"greater_than_equal\",\"msg\":\"Version must be positive\"}]}")
        assertEquals("expected_version", validation.validationIssues.single().loc!!.last().asString)
        val sample = examples.getAsJsonObject("cookie")
        val cookie = Cookie.parse("https://workspace.example/api/auth/me".toHttpUrl(), sample["header"].asString)!!
        assertEquals(sample["name"].asString, cookie.name)
        assertTrue(cookie.httpOnly)
        assertTrue(cookie.secure)
        assertEquals("/api", cookie.path)
    }

    @Test
    fun declaredDtoFieldsMatchBackendSchema() {
        val schemas = root.getAsJsonObject("contract").getAsJsonObject("components").getAsJsonObject("schemas")
        for ((type, schema) in listOf(Task::class.java to "TaskResponse", TaskBrief::class.java to "TaskBrief",
            BriefCriterion::class.java to "BriefCriterion", TaskDetail::class.java to "TaskDetailResponse",
            TaskReference::class.java to "TaskReference", TaskReferencePage::class.java to "TaskReferencePage",
            TaskActions::class.java to "TaskActionsResponse", AllowedAction::class.java to "TaskActionAvailability",
            CriterionProgress::class.java to "CriterionProgress", ProgressRequest::class.java to "ProgressWrite",
            ReviewRequest::class.java to "TaskReviewWrite", TaskReview::class.java to "TaskReviewResponse")) {
            val fields = schemas.getAsJsonObject(schema).getAsJsonObject("properties").keySet()
            for (field in type.declaredFields.filter { !java.lang.reflect.Modifier.isStatic(it.modifiers) }) {
                val wireName = field.getAnnotation(SerializedName::class.java)?.value ?: field.name
                // My Work enriches a reference with action availability separately.
                if (type == TaskReference::class.java && wireName == "actions") continue
                assertTrue("${type.simpleName}.$wireName is absent from $schema", fields.contains(wireName))
            }
        }
    }
}
