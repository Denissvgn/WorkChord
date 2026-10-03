package com.workchord.android.data.api

import android.content.Context
import android.content.SharedPreferences
import com.workchord.android.BuildConfig
import com.google.gson.Gson
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.security.MessageDigest

open class TokenManager(context: Context? = null, private val store: CredentialStore? = context?.let { EncryptedCredentialStore(it) },
    private val allowDebugHttp: Boolean = BuildConfig.DEBUG, val draftStorage: DraftStorage? = context?.let { EncryptedDraftStorage(it) }) {
    private val prefs: SharedPreferences? = context?.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
    private var inMemoryBaseUrl: String = DEFAULT_BASE_URL
    private val gson = Gson()
    private var secrets: NativeSecrets = readSecrets()
    private fun readSecrets(): NativeSecrets {
        val raw = store?.read() ?: return NativeSecrets()
        return try {
            val decoded = gson.fromJson(raw, NativeSecrets::class.java) ?: throw IllegalArgumentException("Invalid session")
            requireNotNull(decoded.serverUrl)
            validateServerUrl(decoded.serverUrl, allowDebugHttp)
            decoded
        } catch (_: Exception) {
            store?.write(null)
            NativeSecrets()
        }
    }
    private var generation = 0L
    val scopeGeneration: Long get() = generation
    internal val requestGeneration = ThreadLocal<Long>()
    internal fun requestScopeIsCurrent() = requestGeneration.get()?.let { it == generation } ?: true
    private val invalidations = MutableStateFlow(0L)
    val sessionInvalidations = invalidations.asStateFlow()

    fun draftScope(): String? {
        val principal = principalId?.takeIf { it > 0 } ?: return null
        val value = "$baseUrl\n$principal"
        return MessageDigest.getInstance("SHA-256").digest(value.toByteArray()).joinToString("") { "%02x".format(it) }
    }
    fun invalidateSession() { try { clearCredentials() } finally { invalidations.value++ } }
    fun clearSavedDrafts() { draftScope()?.let { draftStorage?.clear(it) } }

    @Synchronized
    private fun persist() { secrets = secrets.copy(serverUrl = baseUrl); store?.write(gson.toJson(secrets)) }

    init {
        check(prefs?.edit()?.remove(KEY_SESSION_TOKEN)?.remove(KEY_AGENT_API_KEY)?.commit() != false) {
            "Could not remove obsolete credentials from device preferences."
        }
        secrets.serverUrl?.let { inMemoryBaseUrl = it }
    }

    open var nativeAccessToken: String?
        get() = secrets.accessToken
        set(value) { secrets = secrets.copy(accessToken = value); persist() }

    open var cookies: List<String>
        get() = secrets.cookies.orEmpty()
        set(value) { secrets = secrets.copy(cookies = value); persist() }

    open var csrfToken: String?
        get() = secrets.csrfToken
        set(value) { secrets = secrets.copy(csrfToken = value); persist() }

    open var pendingConnection: PendingConnection?
        get() = secrets.pending
        set(value) { secrets = secrets.copy(pending = value); persist() }

    var principalId: Int?
        get() = secrets.principalId
        set(value) {
            if (secrets.principalId != null && secrets.principalId != value) clearCredentials()
            secrets = secrets.copy(principalId = value); persist()
        }

    var workSelection: WorkSelection
        get() = secrets.selection ?: WorkSelection()
        set(value) { secrets = secrets.copy(selection = value); persist() }

    open var baseUrl: String
        get() = secrets.serverUrl ?: prefs?.getString(KEY_BASE_URL, null) ?: inMemoryBaseUrl
        set(value) {
            val normalized = validateServerUrl(value, allowDebugHttp)
            if (baseUrl.trimEnd('/') != normalized.trimEnd('/')) {
                clearCredentials()
            }
            inMemoryBaseUrl = normalized
            secrets = secrets.copy(serverUrl = normalized)
            persist()
            check(prefs?.edit()?.putString(KEY_BASE_URL, normalized)?.commit() != false) { "Could not save the server address." }
        }

    open fun clearCredentials() {
        generation++
        secrets = NativeSecrets()
        store?.write(null)
    }

    open fun clear() {
        clearCredentials()
        prefs?.edit()?.clear()?.apply()
        inMemoryBaseUrl = DEFAULT_BASE_URL
    }

    companion object {
        private const val PREF_NAME = "workchord_auth_prefs"
        private const val KEY_SESSION_TOKEN = "key_session_token"
        private const val KEY_AGENT_API_KEY = "key_agent_api_key"
        private const val KEY_BASE_URL = "key_base_url"
        val DEFAULT_BASE_URL = if (BuildConfig.DEBUG) "http://10.0.2.2/" else ""

        fun validateServerUrl(value: String, debug: Boolean): String {
            val url = value.trim().toHttpUrlOrNull() ?: throw IllegalArgumentException("Enter a valid HTTPS server address.")
            require(url.username.isEmpty() && url.password.isEmpty() && url.query == null && url.fragment == null) {
                "The server address cannot contain credentials, a query, or a fragment."
            }
            require(url.encodedPath == "/") { "Enter the server origin without an API path." }
            require(url.scheme == "https" || debug && url.host in setOf("10.0.2.2", "127.0.0.1", "localhost")) {
                "HTTPS is required. Debug HTTP is limited to local development hosts."
            }
            return url.toString()
        }
    }
}

data class NativeSecrets(val serverUrl: String? = null, val accessToken: String? = null, val cookies: List<String>? = emptyList(),
    val csrfToken: String? = null, val principalId: Int? = null, val pending: PendingConnection? = null,
    val selection: WorkSelection? = null)

data class PendingConnection(val requestId: String, val verifier: String, val verificationCode: String,
    val verificationPath: String, val expiresAt: String)

data class WorkSelection(val projectId: Int? = null, val iterationId: Int? = null,
    val backlogOnly: Boolean = false, val queue: String = "all")
