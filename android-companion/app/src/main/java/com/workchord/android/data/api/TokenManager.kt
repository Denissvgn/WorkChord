package com.workchord.android.data.api

import android.content.Context
import android.content.SharedPreferences
import com.workchord.android.BuildConfig
import com.google.gson.Gson
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull

open class TokenManager(context: Context? = null, private val store: CredentialStore? = context?.let { EncryptedCredentialStore(it) },
    private val allowDebugHttp: Boolean = BuildConfig.DEBUG) {
    private val prefs: SharedPreferences? = try {
        context?.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
    } catch (e: Exception) {
        null
    }

    private var inMemorySessionToken: String? = null
    private var inMemoryAgentApiKey: String? = null
    private var inMemoryBaseUrl: String = DEFAULT_BASE_URL
    private val gson = Gson()
    private var secrets: NativeSecrets = store?.read()?.let { gson.fromJson(it, NativeSecrets::class.java) } ?: NativeSecrets()
    private var generation = 0L
    val scopeGeneration: Long get() = generation

    @Synchronized
    private fun persist() { secrets = secrets.copy(serverUrl = baseUrl); store?.write(gson.toJson(secrets)) }

    init { secrets.serverUrl?.let { inMemoryBaseUrl = it } }

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

    open var sessionToken: String?
        get() = prefs?.getString(KEY_SESSION_TOKEN, null) ?: inMemorySessionToken
        set(value) {
            prefs?.edit()?.putString(KEY_SESSION_TOKEN, value)?.apply()
            inMemorySessionToken = value
        }

    open var agentApiKey: String?
        get() = prefs?.getString(KEY_AGENT_API_KEY, null) ?: inMemoryAgentApiKey
        set(value) {
            prefs?.edit()?.putString(KEY_AGENT_API_KEY, value)?.apply()
            inMemoryAgentApiKey = value
        }

    open var baseUrl: String
        get() = secrets.serverUrl ?: prefs?.getString(KEY_BASE_URL, DEFAULT_BASE_URL) ?: inMemoryBaseUrl
        set(value) {
            val normalized = validateServerUrl(value, allowDebugHttp)
            if (baseUrl.trimEnd('/') != normalized.trimEnd('/')) {
                clearCredentials()
            }
            prefs?.edit()?.putString(KEY_BASE_URL, normalized)?.apply()
            inMemoryBaseUrl = normalized
        }

    open fun clearCredentials() {
        generation++
        secrets = NativeSecrets()
        store?.write(null)
        sessionToken = null
        agentApiKey = null
    }

    open fun clear() {
        clearCredentials()
        prefs?.edit()?.clear()?.apply()
        inMemorySessionToken = null
        inMemoryAgentApiKey = null
        inMemoryBaseUrl = DEFAULT_BASE_URL
    }

    companion object {
        private const val PREF_NAME = "workchord_auth_prefs"
        private const val KEY_SESSION_TOKEN = "key_session_token"
        private const val KEY_AGENT_API_KEY = "key_agent_api_key"
        private const val KEY_BASE_URL = "key_base_url"
        val DEFAULT_BASE_URL = if (BuildConfig.DEBUG) "http://10.0.2.2/" else "https://localhost/"

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
