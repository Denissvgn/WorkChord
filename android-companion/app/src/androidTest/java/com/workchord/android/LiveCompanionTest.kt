package com.workchord.android

import android.content.Intent
import android.net.Uri
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createEmptyComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.uiautomator.By
import androidx.test.uiautomator.Until
import androidx.test.uiautomator.UiDevice
import com.workchord.android.data.api.TokenManager
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import org.json.JSONArray
import org.junit.Assert.*
import org.junit.Assume.assumeTrue
import org.junit.Rule
import org.junit.Test
import org.junit.After
import org.junit.runner.RunWith
import java.io.File
import java.util.concurrent.TimeUnit

/** Opt-in cross-app checks confined to the safety-fenced synthetic HTTP fixture. */
@RunWith(AndroidJUnit4::class)
class LiveCompanionTest {
    @get:Rule val app = createEmptyComposeRule()
    private val instrumentation get() = InstrumentationRegistry.getInstrumentation()
    private val device get() = UiDevice.getInstance(instrumentation)
    private val context get() = instrumentation.targetContext
    private val tokens get() = (context.applicationContext as WorkChordApplication).tokenManager
    private val origin = "http://localhost:4173"
    private lateinit var nonce: String
    private val http = OkHttpClient.Builder().connectTimeout(3, TimeUnit.SECONDS).readTimeout(5, TimeUnit.SECONDS).build()

    private fun qualify() {
        val arguments = InstrumentationRegistry.getArguments()
        assumeTrue("A disposable live fixture must be selected explicitly", arguments.getString("fixtureOrigin") == origin)
        nonce = requireNotNull(arguments.getString("fixtureNonce"))
        val deadline = android.os.SystemClock.elapsedRealtime() + 15000
        var ready = false
        while (!ready && android.os.SystemClock.elapsedRealtime() < deadline) {
            ready = runCatching {
                http.newCall(Request.Builder().url("$origin/api/auth/me").build()).execute().use {
                    it.isSuccessful && it.header("X-WorkChord-Fixture") == nonce
                }
            }.getOrDefault(false)
            if (!ready) android.os.SystemClock.sleep(250)
        }
        check(ready) { "The marked disposable application is unavailable; no writes are allowed." }
        launchApp()
    }
    private fun launchApp() {
        context.startActivity(context.packageManager.getLaunchIntentForPackage("com.workchord.android")!!.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
    }
    @After
    fun captureFinalSemantics() {
        runCatching { println(app.onAllNodes(isRoot()).onFirst().printToString()) }
        runCatching {
            app.onNode(hasScrollToNodeAction()).performScrollToIndex(0)
            println(app.onAllNodes(isRoot()).onFirst().printToString())
        }
    }
    private fun request(path: String, method: String = "GET", body: JSONObject? = null): Pair<Int, JSONObject> {
        val builder = Request.Builder().url(origin + path).header("X-Fixture-Key", nonce)
        tokens.nativeAccessToken?.let { builder.header("Authorization", "Bearer $it") }
        if (method != "GET") builder.method(method, (body ?: JSONObject()).toString().toRequestBody("application/json".toMediaType()))
        return http.newCall(builder.build()).execute().use { response ->
            assertEquals(nonce, response.header("X-WorkChord-Fixture"))
            response.code to JSONObject(response.body!!.string())
        }
    }
    private fun current(id: Int) = request("/api/tasks/$id").also { assertEquals(200, it.first) }.second
    private fun waitText(text: String) { app.waitUntil(15000) { app.onAllNodesWithText(text).fetchSemanticsNodes().isNotEmpty() } }
    private fun click(text: String) {
        println("Native control: $text")
        try {
            app.waitUntil(15000) { app.onAllNodes(hasText(text) and isEnabled()).fetchSemanticsNodes().isNotEmpty() }
            app.onNodeWithText(text).performClick()
        } catch (error: Throwable) {
            println(app.onAllNodes(isRoot()).onFirst().printToString())
            println(app.onAllNodes(isRoot()).onLast().printToString())
            throw error
        }
    }
    private fun scroll(text: String) { app.onNode(hasScrollToNodeAction()).performScrollToNode(hasText(text)); app.waitForIdle() }
    private fun field(label: String, value: String) {
        try {
            app.waitUntil(15000) {
                runCatching {
                    scroll(label)
                    app.onAllNodes(hasText(label) and hasSetTextAction() and isEnabled()).fetchSemanticsNodes().isNotEmpty()
                }.getOrDefault(false)
            }
            app.onNodeWithText(label).performTextReplacement(value)
        } catch (error: Throwable) {
            println(app.onAllNodes(isRoot()).onFirst().printToString())
            throw error
        }
    }
    private fun browserClick(text: String) {
        val node = device.wait(Until.findObject(By.text(text)), 15000) ?: error("Browser control missing: $text")
        node.click()
    }
    private fun signIn(person: String) {
        if (tokens.nativeAccessToken != null) {
            val me = request("/api/auth/me").second
            if (me.optJSONObject("principal")?.optString("display_name") == person) return
        }
        click("Sign in")
        click("Open browser to sign in")
        // The isolated emulator may show Chrome's first-run consent once.
        for (label in listOf("Use without an account", "Accept & continue", "No thanks", "Got it")) {
            device.wait(Until.findObject(By.text(label)), 1000)?.click()
        }
        if (device.wait(Until.findObject(By.clazz("android.widget.CheckBox")), 1500) != null &&
            !device.hasObject(By.text("Your device will sign in as $person."))) {
            browserClick("Account and access")
            browserClick("Sign out")
            check(device.wait(Until.hasObject(By.text("Sign in to WorkChord")), 15000)) {
                "Browser logout did not clear the previous account."
            }
        }
        if (device.wait(Until.findObject(By.clazz("android.widget.CheckBox")), 1500) == null) {
            browserClick("Sign in")
            browserClick("Continue as $person")
        }
        val checkbox = device.wait(Until.findObject(By.clazz("android.widget.CheckBox")), 15000)
            ?: error("Explicit browser device consent missing")
        checkbox.click()
        browserClick("Approve connection")
        assertTrue(device.wait(Until.hasObject(By.text("Connection approved. Return to your device and check the connection.")), 15000))
        launchApp()
        click("Check connection")
        waitText("My Work")
        assertEquals(person, request("/api/auth/me").second.getJSONObject("principal").getString("display_name"))
    }
    private fun openTask(id: Int, title: String = "Nested leaf") {
        instrumentation.runOnMainSync {
            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("workchord://task/$id"))
                .setPackage("com.workchord.android").addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP or Intent.FLAG_ACTIVITY_NEW_TASK))
        }
        waitText("Task #$id")
        waitText(title)
    }
    private fun fault(id: Int, status: Int) {
        assertEquals(200, request("/api/tasks/$id/_fixture/read-fault", "POST", JSONObject().put("task_id", id).put("status", status)).first)
    }

    @Test
    fun browserApprovalCanonicalEvidenceConflictAndReadRecovery() {
        qualify()
        app.waitForIdle()
        app.onNodeWithText("Server address").performTextReplacement(origin)
        click("Use this server")
        signIn("Alice")
        click("All accessible projects")
        click("Orchard")
        assertFalse(app.onAllNodesWithText("Harbor").fetchSemanticsNodes().isNotEmpty())
        val work = request("/api/tasks/my-work").second.getJSONObject("queues")
        val queued = work.getJSONArray("queued")
        val id = (0 until queued.length()).map { queued.getJSONObject(it) }.single { it.getString("title") == "Nested leaf" }.getInt("id")
        val brief = JSONObject("""{"schema_version":1,"goal":"Verify native evidence persistence","scope":"Synthetic nested work only","acceptance_criteria":[{"id":"native-readback","revision":1,"text":"Evidence survives a current server read","verification":"Read the current task through HTTP"}],"verification":"Compare saved evidence through HTTP"}""")
        assertEquals(200, request("/api/tasks/$id", "PUT", JSONObject().put("expected_version", current(id).getInt("version")).put("brief", brief)).first)
        openTask(id)
        scroll("Edit evidence"); click("Edit evidence")
        field("Criterion evidence", "Synthetic native evidence retained through a competing edit")
        app.onNode(isToggleable()).performScrollTo()
        if (app.onAllNodes(isToggleable() and isOff()).fetchSemanticsNodes().isNotEmpty()) app.onNode(isToggleable()).performClick()
        app.onNode(isToggleable()).assertIsOn()
        val changed = request("/api/tasks/$id", "PUT", JSONObject().put("expected_version", current(id).getInt("version")).put("priority", if (current(id).getInt("priority") == 3) 4 else 3))
        assertEquals(200, changed.first)
        scroll("Save evidence"); click("Save evidence")
        scroll("Reload current task"); click("Reload current task")
        scroll("Keep draft with current revision"); click("Keep draft with current revision")
        scroll("Save evidence"); click("Save evidence")
        app.waitUntil(15000) { current(id).optJSONObject("progress")?.optJSONArray("criteria")?.optJSONObject(0)?.optString("state") == "completed" }
        assertTrue(current(id).isNull("accepted_at"))
        val progress = current(id).getJSONObject("progress").getJSONArray("criteria").getJSONObject(0)
        assertTrue(progress.getString("evidence").contains("Synthetic native evidence"))
        fault(id, 503)
        device.pressHome()
        launchApp()
        app.onNode(hasScrollToNodeAction()).performScrollToIndex(0)
        waitText("Reload current task")
        assertTrue(app.onAllNodes(hasText("Cached read-only data", substring = true)).fetchSemanticsNodes().isNotEmpty())
        fault(id, 0)
        click("Reload current task")
        waitText("Nested leaf")
        field("Reason for action or review", "Explicitly saved device-only draft")
        scroll("Save draft on this device"); click("Save draft on this device")
        app.waitUntil(10000) { File(instrumentation.targetContext.noBackupFilesDir, "draft-${tokens.draftScope()}-$id.bin").exists() }
        File(instrumentation.targetContext.noBackupFilesDir, "live-task-id").writeText(id.toString())
    }

    @Test
    fun reopenedProcessRestoresAuthorizedDraftAndRevocationClearsPrivateView() {
        qualify()
        val idFile = File(instrumentation.targetContext.noBackupFilesDir, "live-task-id")
        assumeTrue("Run the sign-in/evidence scenario in a separate process first", idFile.exists())
        val id = idFile.readText().toInt()
        waitText("My Work")
        openTask(id)
        scroll("Reason for action or review")
        app.onNodeWithText("Explicitly saved device-only draft").assertExists()
        assertEquals("Explicitly saved device-only draft", TokenManager(instrumentation.targetContext).draftStorage!!.read(requireNotNull(tokens.draftScope()), id)?.let { JSONObject(it).getString("reason") })
        fault(id, 403)
        device.pressHome()
        launchApp()
        waitText("This work is not currently available.")
        app.onNodeWithText("Nested leaf").assertDoesNotExist()
        fault(id, 0)
        app.onNodeWithText("Alice · Sign out").performClick()
        waitText("Connect to WorkChord")
        assertNull(tokens.nativeAccessToken)
        idFile.delete()
    }
    private fun command(label: String, reason: String) {
        field("Reason for action or review", reason)
        scroll(label); click(label)
    }
    private fun completedEvidence(text: String, id: Int) {
        scroll("Edit evidence"); click("Edit evidence")
        field("Criterion evidence", text)
        app.onNode(isToggleable()).performScrollTo()
        if (app.onAllNodes(isToggleable() and isOff()).fetchSemanticsNodes().isNotEmpty()) app.onNode(isToggleable()).performClick()
        app.onNode(isToggleable()).assertIsOn()
        scroll("Save evidence"); click("Save evidence")
        app.waitUntil(15000) { current(id).optJSONObject("progress")?.optJSONArray("criteria")?.optJSONObject(0)?.optString("evidence") == text }
    }
    private fun signOut(person: String) {
        click("$person · Sign out")
        waitText("Connect to WorkChord")
        assertNull(tokens.nativeAccessToken)
    }

    @Test
    fun manualActionsAndSeparateReviewerRejectReworkAndAccept() {
        qualify()
        signIn("Alice")
        val queues = request("/api/tasks/my-work").second.getJSONObject("queues")
        val references = queues.keys().asSequence().flatMap { key ->
            val page = queues.getJSONArray(key)
            (0 until page.length()).asSequence().map { page.getJSONObject(it) }
        }.toList()
        val id = references.single { it.getString("title") == "Nested leaf" }.getInt("id")
        openTask(id)
        if (current(id).getString("status") == "planned") command("Start manual work", "Begin bounded synthetic manual work")
        app.waitUntil(15000) { current(id).getString("status") == "active" }
        command("Block work", "Await explicit synthetic prerequisite")
        app.waitUntil(15000) { !current(id).isNull("blocked_reason") }
        command("Unblock work", "Synthetic prerequisite now satisfied")
        app.waitUntil(15000) { current(id).isNull("blocked_reason") }
        command("Cancel work", "Exercise controlled cancellation")
        app.waitUntil(15000) { !current(id).isNull("canceled_at") }
        command("Reopen work", "Resume explicitly after cancellation")
        app.waitUntil(15000) { current(id).isNull("canceled_at") }
        if (current(id).getString("status") == "planned") command("Start manual work", "Resume manual work with current authority")
        completedEvidence("Synthetic first revision pending independent verification", id)
        command("Resolve manual work", "First revision submitted for independent review")
        app.waitUntil(15000) { current(id).getString("status") == "resolved" }
        scroll("Accept current evidence")
        app.onNodeWithText("Accept current evidence").assertIsNotEnabled()
        signOut("Alice")
        signIn("Charlie")
        openTask(id)
        field("Review evidence", "Independent synthetic reviewer requests clearer readback")
        command("Reject for rework", "Insufficient explanation in the first revision")
        app.waitUntil(15000) { current(id).getString("status") == "active" }
        assertEquals("reject", request("/api/tasks/$id/reviews/current").second.getJSONObject("review").getString("verdict"))
        signOut("Charlie")
        signIn("Alice")
        openTask(id)
        completedEvidence("Corrected synthetic evidence: current HTTP readback and canonical criterion revision verified", id)
        command("Resolve manual work", "Corrected revision ready for independent verification")
        app.waitUntil(15000) { current(id).getString("status") == "resolved" }
        signOut("Alice")
        signIn("Charlie")
        openTask(id)
        field("Review evidence", "Corrected criterion evidence and current revisions independently read back")
        command("Accept current evidence", "Independent reviewer accepts the corrected revision")
        app.waitUntil(15000) { current(id).getString("status") == "closed" }
        val verdict = request("/api/tasks/$id/reviews/current").second.getJSONObject("review")
        assertEquals("accept", verdict.getString("verdict"))
        assertEquals(request("/api/auth/me").second.getJSONObject("principal").getInt("id"), verdict.getInt("principal_id"))
        assertFalse(current(id).isNull("accepted_at"))
        signOut("Charlie")
    }

    private fun currentSessionId(): String {
        val builder = Request.Builder().url("$origin/api/auth/sessions")
            .header("Authorization", "Bearer " + requireNotNull(tokens.nativeAccessToken))
        return http.newCall(builder.build()).execute().use {
            assertEquals(nonce, it.header("X-WorkChord-Fixture"))
            assertEquals(200, it.code)
            val rows = JSONArray(it.body!!.string())
            (0 until rows.length()).map { index -> rows.getJSONObject(index) }.single { row -> row.getBoolean("current") }.getString("public_id")
        }
    }

    @Test
    fun nativeRotationRevocationAndAuthorizedDraftRecovery() {
        qualify()
        signIn("Alice")
        val originalToken = requireNotNull(tokens.nativeAccessToken)
        val originalSession = currentSessionId()
        val rotated = request("/api/auth/native-token", "POST")
        assertEquals(200, rotated.first)
        tokens.nativeAccessToken = rotated.second.getString("access_token")
        assertNotEquals(originalToken, tokens.nativeAccessToken)
        assertEquals(200, request("/api/auth/sessions/$originalSession", "DELETE").first)
        http.newCall(Request.Builder().url("$origin/api/projects").header("Authorization", "Bearer $originalToken").build()).execute().use {
            assertEquals(nonce, it.header("X-WorkChord-Fixture"))
            assertEquals(401, it.code)
        }
        assertEquals("Alice", request("/api/auth/me").second.getJSONObject("principal").getString("display_name"))
        val queued = request("/api/tasks/my-work").second.getJSONObject("queues").getJSONArray("queued")
        val id = (0 until queued.length()).map { queued.getJSONObject(it) }.single { it.getString("title") == "Planned" }.getInt("id")
        openTask(id, "Planned")
        field("Reason for action or review", "Protected draft during actual session revocation")
        scroll("Save draft on this device"); click("Save draft on this device")
        val savedScope = requireNotNull(tokens.draftScope())
        app.waitUntil(10000) { File(context.noBackupFilesDir, "draft-$savedScope-$id.bin").exists() }
        val currentSession = currentSessionId()
        assertEquals(200, request("/api/auth/sessions/$currentSession", "DELETE").first)
        device.pressHome()
        launchApp()
        waitText("Connect to WorkChord")
        assertNull(tokens.nativeAccessToken)
        assertTrue(File(context.noBackupFilesDir, "draft-$savedScope-$id.bin").exists())
        signIn("Alice")
        openTask(id, "Planned")
        scroll("Reason for action or review")
        waitText("Protected draft during actual session revocation")
        signOut("Alice")
        assertFalse(File(context.noBackupFilesDir, "draft-$savedScope-$id.bin").exists())
    }

    @Test
    fun networkInterruptionLocksCurrentWorkAndRecoversLocalInputs() {
        qualify()
        assumeTrue("A host-controlled network interruption must be explicitly selected",
            InstrumentationRegistry.getArguments().getString("networkControl") == "enabled")
        signIn("Alice")
        val queued = request("/api/tasks/my-work").second.getJSONObject("queues").getJSONArray("queued")
        val id = (0 until queued.length()).map { queued.getJSONObject(it) }.single { it.getString("title") == "Planned" }.getInt("id")
        openTask(id, "Planned")
        field("Reason for action or review", "Protected draft during a real network interruption")
        scroll("Save draft on this device"); click("Save draft on this device")
        val marker = File(context.noBackupFilesDir, "network-stage.txt")
        fun awaitStage(expected: String) {
            val until = android.os.SystemClock.elapsedRealtime() + 60000
            while (marker.readText() != expected && android.os.SystemClock.elapsedRealtime() < until) android.os.SystemClock.sleep(100)
            check(marker.readText() == expected) { "The controlled network stage did not complete." }
        }
        marker.writeText("ready")
        awaitStage("offline")
        device.pressHome(); launchApp()
        app.onNode(hasScrollToNodeAction()).performScrollToIndex(0)
        app.waitUntil(30000) { app.onAllNodes(hasText("Cached read-only data", substring = true)).fetchSemanticsNodes().isNotEmpty() }
        scroll("Start manual work")
        app.onNodeWithText("Start manual work").assertIsNotEnabled()
        marker.writeText("observed_offline")
        awaitStage("restored")
        scroll("Reload current task"); click("Reload current task")
        scroll("Reason for action or review")
        waitText("Protected draft during a real network interruption")
        app.onNodeWithText("Protected draft during a real network interruption").assertExists()
        scroll("Start manual work")
        app.waitUntil(15000) { app.onAllNodes(hasText("Start manual work") and isEnabled()).fetchSemanticsNodes().isNotEmpty() }
        assertEquals("planned", current(id).getString("status"))
        marker.writeText("done")
        signOut("Alice")
        marker.delete()
    }

    @Test
    fun actualWebEditorAndNativeDraftProduceRecoverableConflict() {
        qualify()
        assumeTrue("A separate web editor must be explicitly selected",
            InstrumentationRegistry.getArguments().getString("webPeerControl") == "enabled")
        signIn("Alice")
        val queues = request("/api/tasks/my-work").second.getJSONObject("queues").getJSONArray("queued")
        val planned = (0 until queues.length()).map { queues.getJSONObject(it) }.single { it.getString("title") == "Planned" }
        val iteration = current(planned.getInt("id")).getInt("iteration_id")
        val profile = request("/api/auth/me").second.getJSONObject("profile").getInt("id")
        val brief = JSONObject().put("schema_version", 1).put("goal", "Verify simultaneous browser and native edits")
            .put("scope", "Synthetic peer deliverable only").put("verification", "Read back canonical criterion evidence")
            .put("acceptance_criteria", JSONArray().put(JSONObject().put("id", "native-web-peer").put("revision", 1)
                .put("text", "Retained evidence survives a browser edit")))
        val created = request("/api/iterations/$iteration/tasks", "POST", JSONObject().put("title", "Native peer work")
            .put("project_id", planned.getInt("project_id")).put("owner_profile_id", profile).put("effort_hours", 2).put("brief", brief))
        assertEquals(201, created.first)
        val id = created.second.getInt("id")
        openTask(id, "Native peer work")
        scroll("Edit evidence"); click("Edit evidence")
        field("Criterion evidence", "Retained native evidence during an actual web editor update")
        app.onNode(isToggleable()).performScrollTo().performClick().assertIsOn()
        val marker = File(context.noBackupFilesDir, "web-peer-stage.txt")
        marker.writeText(id.toString())
        val until = android.os.SystemClock.elapsedRealtime() + 90000
        while (marker.readText() != "saved" && android.os.SystemClock.elapsedRealtime() < until) android.os.SystemClock.sleep(100)
        check(marker.readText() == "saved") { "The controlled web editor did not save." }
        scroll("Save evidence"); click("Save evidence")
        scroll("Reload current task"); click("Reload current task")
        scroll("Keep draft with current revision"); click("Keep draft with current revision")
        scroll("Save evidence"); click("Save evidence")
        app.waitUntil(15000) { current(id).optJSONObject("progress")?.optJSONArray("criteria")?.optJSONObject(0)?.optString("state") == "completed" }
        assertTrue(current(id).isNull("accepted_at"))
        signOut("Alice")
        marker.delete()
    }

    @Test
    @androidx.test.filters.SdkSuppress(minSdkVersion = 33)
    fun captureCompanionPresentation() {
        assumeTrue("Presentation capture must be explicitly selected",
            InstrumentationRegistry.getArguments().getString("presentationControl") == "enabled")
        qualify()
        if (tokens.baseUrl.trimEnd('/') != origin) {
            app.onNodeWithText("Server address").performTextReplacement(origin)
            click("Use this server")
        }
        val locales = context.getSystemService(android.app.LocaleManager::class.java)
        locales.applicationLocales = android.os.LocaleList.getEmptyLocaleList()
        device.executeShellCommand("cmd uimode night no")
        device.setOrientationNatural()
        try {
        val output = File(context.getExternalFilesDir(null), "presentation").apply { mkdirs() }
        fun capture(name: String) {
            device.waitForIdle(2000)
            app.waitForIdle()
            android.os.SystemClock.sleep(350)
            check(device.takeScreenshot(File(output, name + ".png")))
        }
        capture("setup-portrait")
        signIn("Alice")
        if (app.onAllNodesWithContentDescription("Back").fetchSemanticsNodes().isNotEmpty()) app.onNodeWithContentDescription("Back").performClick()
        waitText("My Work")
        capture("work-portrait")
        device.setOrientationLeft()
        waitText("My Work")
        capture("work-landscape")
        device.setOrientationNatural()
        waitText("My Work")
        val queues = request("/api/tasks/my-work").second.getJSONObject("queues").getJSONArray("queued")
        val id = (0 until queues.length()).map { queues.getJSONObject(it) }.single { it.getString("title") == "Planned" }.getInt("id")
        openTask(id, "Planned")
        capture("detail-portrait")
        device.executeShellCommand("cmd uimode night yes")
        waitText("Planned")
        capture("detail-dark")
        device.executeShellCommand("cmd uimode night no")
        device.pressBack()
        waitText("My Work")
        locales.applicationLocales = android.os.LocaleList.forLanguageTags("ru")
        waitText("Моя работа")
        capture("work-russian")
        locales.applicationLocales = android.os.LocaleList.getEmptyLocaleList()
        waitText("My Work")
        signOut("Alice")
        } finally {
            locales.applicationLocales = android.os.LocaleList.getEmptyLocaleList()
            device.executeShellCommand("cmd uimode night no")
            device.setOrientationNatural()
            device.unfreezeRotation()
        }
    }

}
