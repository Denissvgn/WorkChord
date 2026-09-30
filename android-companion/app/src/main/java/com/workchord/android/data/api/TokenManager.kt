package com.workchord.android.data.api

import android.content.Context
import android.content.SharedPreferences
import com.workchord.android.BuildConfig

open class TokenManager(context: Context? = null) {
    private val prefs: SharedPreferences? = try {
        context?.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)
    } catch (e: Exception) {
        null
    }

    private var inMemorySessionToken: String? = null
    private var inMemoryAgentApiKey: String? = null
    private var inMemoryBaseUrl: String = DEFAULT_BASE_URL

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
        get() = prefs?.getString(KEY_BASE_URL, DEFAULT_BASE_URL) ?: inMemoryBaseUrl
        set(value) {
            if (baseUrl.trimEnd('/') != value.trimEnd('/')) {
                sessionToken = null
                agentApiKey = null
            }
            prefs?.edit()?.putString(KEY_BASE_URL, value)?.apply()
            inMemoryBaseUrl = value
        }

    open fun clear() {
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
    }
}
