package com.workchord.android

import com.workchord.android.data.api.AuthInterceptor
import com.workchord.android.data.api.NetworkClient
import com.workchord.android.data.api.TokenManager
import com.workchord.android.data.api.TransportPolicyInterceptor
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.logging.HttpLoggingInterceptor
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.Assert.*
import org.junit.Test
import java.io.IOException

class NetworkSecurityTest {
    @Test
    fun releaseRejectsHttpBeforeCredentialsAreSent() {
        MockWebServer().use { server ->
            server.start()
            val tokens = TokenManager().apply {
                baseUrl = server.url("/").toString()
                sessionToken = "private-session"
                agentApiKey = "private-agent-key"
            }
            val client = OkHttpClient.Builder()
                .addInterceptor(TransportPolicyInterceptor({ tokens.baseUrl }, false))
                .addInterceptor(AuthInterceptor(tokens)).build()
            try {
                client.newCall(Request.Builder().url(server.url("/api/auth/me")).build()).execute()
                fail("Cleartext release traffic must be rejected")
            } catch (error: IOException) {
                assertTrue(error.message.orEmpty().contains("HTTPS"))
            }
            assertEquals(0, server.requestCount)
        }
    }

    @Test
    fun debugPermitsLocalHttpButRejectsRemoteHttpAndChangedOrigins() {
        MockWebServer().use { server ->
            server.start()
            val client = OkHttpClient.Builder()
                .addInterceptor(TransportPolicyInterceptor({ server.url("/").toString() }, true)).build()
            server.enqueue(MockResponse().setBody("local response"))
            client.newCall(Request.Builder().url(server.url("/")).build()).execute().use { assertEquals(200, it.code) }
            val remote = OkHttpClient.Builder()
                .addInterceptor(TransportPolicyInterceptor({ "http://example.invalid/" }, true)).build()
            try {
                remote.newCall(Request.Builder().url("http://example.invalid/").build()).execute()
                fail("Remote HTTP must remain blocked in debug")
            } catch (error: IOException) {
                assertTrue(error.message.orEmpty().contains("HTTPS"))
            }
            val changed = OkHttpClient.Builder()
                .addInterceptor(TransportPolicyInterceptor({ "https://other.example/" }, true)).build()
            try {
                changed.newCall(Request.Builder().url(server.url("/")).build()).execute()
                fail("A cached client must not send credentials to an old server")
            } catch (error: IOException) {
                assertTrue(error.message.orEmpty().contains("address changed"))
            }
            assertEquals(1, server.requestCount)
        }
    }

    @Test
    fun loggingNeverWritesCredentialsOrTaskBodies() {
        for (debug in listOf(false, true)) {
            MockWebServer().use { server ->
                server.start()
                val messages = mutableListOf<String>()
                val logging = NetworkClient.loggingInterceptor(debug, object : HttpLoggingInterceptor.Logger {
                    override fun log(message: String) { messages.add(message) }
                })
                assertEquals(if (debug) HttpLoggingInterceptor.Level.BASIC else HttpLoggingInterceptor.Level.NONE, logging.level)
                val client = OkHttpClient.Builder().addInterceptor(logging).build()
                server.enqueue(MockResponse().setHeader("Set-Cookie", "private-response-cookie").setBody("private-response-body"))
                val request = Request.Builder().url(server.url("/api/tasks"))
                    .header("Cookie", "private-session").header("X-Agent-API-Key", "private-agent-key")
                    .header("Authorization", "Bearer private-bearer")
                    .post("private-task-body".toRequestBody("application/json".toMediaType())).build()
                client.newCall(request).execute().close()
                assertFalse(messages.joinToString().contains("private-"))
                if (!debug) assertTrue(messages.isEmpty())
                if (debug) {
                    logging.level = HttpLoggingInterceptor.Level.HEADERS
                    server.enqueue(MockResponse().setHeader("Set-Cookie", "private-response-cookie"))
                    client.newCall(request).execute().close()
                    assertFalse(messages.joinToString().contains("private-"))
                }
            }
        }
    }

    @Test
    fun changingServersClearsCredentials() {
        val tokens = TokenManager().apply {
            sessionToken = "private-session"
            agentApiKey = "private-agent-key"
        }
        tokens.baseUrl = "https://new.example/"
        assertNull(tokens.sessionToken)
        assertNull(tokens.agentApiKey)
        assertEquals(if (BuildConfig.DEBUG) "http://10.0.2.2/" else "https://localhost/", TokenManager.DEFAULT_BASE_URL)
    }
}
