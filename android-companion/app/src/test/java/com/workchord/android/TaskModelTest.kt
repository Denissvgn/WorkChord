package com.workchord.android

import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class TaskModelTest {

    @Test
    fun testTaskStatusParsing() {
        assertEquals(TaskStatus.PLANNED, TaskStatus.fromString("planned"))
        assertEquals(TaskStatus.ACTIVE, TaskStatus.fromString("active"))
        assertEquals(TaskStatus.RESOLVED, TaskStatus.fromString("resolved"))
        assertEquals(TaskStatus.CLOSED, TaskStatus.fromString("closed"))
        assertEquals(TaskStatus.BLOCKED, TaskStatus.fromString("blocked"))
        assertEquals(TaskStatus.PLANNED, TaskStatus.fromString("unknown_status"))
    }

    @Test
    fun testExtractAcceptanceCriteria() {
        val markdown = """
            ## Goal
            Build features
            
            ## Acceptance criteria
            - Gradle build script configured with Kotlin
            - [x] Jetpack Compose BOM and Material3 theme
            - [ ] Application boots with MainActivity
            
            ## Verification
            Run tests
        """.trimIndent()

        val task = Task(
            id = 1,
            title = "Test Task",
            description = markdown
        )

        val criteria = task.extractAcceptanceCriteria()
        assertEquals(3, criteria.size)
        assertEquals("Gradle build script configured with Kotlin", criteria[0].text)
        assertFalse(criteria[0].isCompleted)

        assertEquals("Jetpack Compose BOM and Material3 theme", criteria[1].text)
        assertTrue(criteria[1].isCompleted)

        assertEquals("Application boots with MainActivity", criteria[2].text)
        assertFalse(criteria[2].isCompleted)
    }

    @Test
    fun testExtractGoal() {
        val markdown = """
            ## Goal
            Initialize Android Gradle Project with Jetpack Compose
            
            ## Scope
            - Gradle setup
        """.trimIndent()

        val task = Task(
            id = 1,
            title = "Scaffold",
            description = markdown
        )

        assertEquals("Initialize Android Gradle Project with Jetpack Compose", task.extractGoal())
    }
}
