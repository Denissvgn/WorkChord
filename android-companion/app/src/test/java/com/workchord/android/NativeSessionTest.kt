package com.workchord.android

import com.workchord.android.data.api.*
import okhttp3.Cookie
import okhttp3.HttpUrl.Companion.toHttpUrl
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.Assert.*
import org.junit.Test

class NativeSessionTest {
    @Test
    fun cookiePathRotationExpiryAndOriginArePreserved() {
        val tokens = TokenManager(allowDebugHttp = true).apply { baseUrl = "http://localhost:8080/" }
        val jar = SessionCookieJar(tokens)
        val source = "http://localhost:8080/api/auth/me".toHttpUrl()
        jar.saveFromResponse(source, listOf(Cookie.parse(source, "custom_session=first; Path=/api/; Max-Age=3600; HttpOnly")!!))
        assertEquals("first", jar.loadForRequest(source).single().value)
        assertTrue(jar.loadForRequest("http://localhost:8080/assets/file".toHttpUrl()).isEmpty())
        assertTrue(jar.loadForRequest("http://localhost:8081/api/auth/me".toHttpUrl()).isEmpty())
        jar.saveFromResponse(source, listOf(Cookie.parse(source, "custom_session=rotated; Path=/api/; Max-Age=3600")!!))
        assertEquals("rotated", jar.loadForRequest(source).single().value)
        jar.saveFromResponse(source, listOf(Cookie.parse(source, "custom_session=; Path=/api/; Max-Age=0")!!))
        assertTrue(jar.loadForRequest(source).isEmpty())
        jar.saveFromResponse(source, listOf(Cookie.parse(source, "future=allowed; Path=/private/; Max-Age=3600")!!))
        assertEquals("allowed", jar.loadForRequest("http://localhost:8080/private/task".toHttpUrl()).single().value)
        tokens.baseUrl = "https://other.example/"
        assertTrue(tokens.cookies.isEmpty())
        assertTrue(jar.loadForRequest(source).isEmpty())
    }

    @Test
    fun secureCookiesNeverLeaveThroughHttp() {
        val tokens = TokenManager().apply { baseUrl = "https://workspace.example/" }
        val jar = SessionCookieJar(tokens)
        val url = "https://workspace.example/api/auth/me".toHttpUrl()
        jar.saveFromResponse(url, listOf(Cookie.parse(url, "private=secret; Path=/; Secure; HttpOnly; Max-Age=60")!!))
        assertEquals("secret", jar.loadForRequest(url).single().value)
        assertTrue(jar.loadForRequest("http://workspace.example/api/auth/me".toHttpUrl()).isEmpty())
    }

    @Test
    fun nativeBearerAndCookiesUseTheirActualTransportContracts() {
        MockWebServer().use { server ->
            server.start()
            val tokens = TokenManager(allowDebugHttp = true).apply { baseUrl = server.url("/").toString() }
            val client = OkHttpClient.Builder().cookieJar(SessionCookieJar(tokens)).addInterceptor(AuthInterceptor(tokens)).build()
            server.enqueue(MockResponse().addHeader("Set-Cookie", "custom_identity=opaque; Path=/api/; Max-Age=3600").setBody("{}"))
            client.newCall(Request.Builder().url(server.url("/api/auth/me")).build()).execute().close()
            assertNull(server.takeRequest().getHeader("Cookie"))
            server.enqueue(MockResponse().setBody("{}"))
            client.newCall(Request.Builder().url(server.url("/api/auth/me")).build()).execute().close()
            assertEquals("custom_identity=opaque", server.takeRequest().getHeader("Cookie"))
            tokens.clearCredentials()
            tokens.nativeAccessToken = "native-only"
            server.enqueue(MockResponse().setBody("{}"))
            client.newCall(Request.Builder().url(server.url("/api/auth/me")).build()).execute().close()
            val request = server.takeRequest()
            assertEquals("Bearer native-only", request.getHeader("Authorization"))
            assertNull(request.getHeader("Cookie"))
        }
    }

    @Test
    fun credentialsPersistTogetherAndClearOnAccountOrServerChanges() {
        val store = object : CredentialStore {
            var value: String? = null
            override fun read() = value
            override fun write(value: String?) { this.value = value }
        }
        val first = TokenManager(store = store)
        first.baseUrl = "https://workspace.example/"
        first.nativeAccessToken = "opaque"
        first.principalId = 19
        first.workSelection = WorkSelection(projectId = 9, iterationId = 12, queue = "review")
        first.pendingConnection = PendingConnection("request", "proof", "ABCD-EFGH", "/mobile/connect?request=request", "future")
        val reopened = TokenManager(store = store)
        assertEquals("opaque", reopened.nativeAccessToken)
        assertNotNull(reopened.pendingConnection)
        assertEquals(first.workSelection, reopened.workSelection)
        reopened.principalId = 20
        assertNull(reopened.nativeAccessToken)
        assertNull(reopened.pendingConnection)
        assertEquals(20, reopened.principalId)
        assertEquals(WorkSelection(), reopened.workSelection)
        reopened.nativeAccessToken = "second-account"
        reopened.baseUrl = "https://different.example/"
        assertNull(reopened.nativeAccessToken)
        assertNull(reopened.principalId)
    }

    @Test
    fun serverConfigurationRejectsCredentialUrlsAndUntrustedCleartext() {
        for (url in listOf("http://remote.example", "https://user:password@workspace.example", "https://workspace.example/api/",
            "https://workspace.example/?secret=value", "https://workspace.example/#fragment")) {
            try { TokenManager.validateServerUrl(url, false); fail("Unsafe address accepted: $url") }
            catch (_: IllegalArgumentException) { }
        }
        assertEquals("https://workspace.example/", TokenManager.validateServerUrl(" https://workspace.example ", false))
        assertEquals("http://10.0.2.2:8001/", TokenManager.validateServerUrl("http://10.0.2.2:8001", true))
    }
}
