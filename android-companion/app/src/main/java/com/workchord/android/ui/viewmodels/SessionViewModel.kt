package com.workchord.android.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.workchord.android.data.api.*
import com.workchord.android.data.models.Identity
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.drop
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.security.MessageDigest
import java.security.SecureRandom
import java.util.Base64
import kotlin.coroutines.coroutineContext

data class SessionUiState(val loading: Boolean = true, val identity: Identity? = null,
    val connection: PendingConnection? = null, val error: String? = null, val scope: Long = 0)

class SessionViewModel(private val tokens: TokenManager, private val api: () -> WorkChordApi = { NetworkClient.getApi(tokens) }) : ViewModel() {
    private val state = MutableStateFlow(SessionUiState())
    val uiState = state.asStateFlow()
    private var operation: Job? = null

    init {
        refresh()
        viewModelScope.launch { tokens.sessionInvalidations.drop(1).collect { refresh() } }
    }

    private fun work(action: suspend () -> Unit) {
        operation?.cancel()
        operation = viewModelScope.launch {
        state.value = state.value.copy(loading = true, error = null)
        try { withContext(Dispatchers.IO) { action() } }
        catch (error: CancellationException) { throw error }
        catch (error: Exception) { state.value = state.value.copy(loading = false, error = error.localizedMessage ?: "Could not connect. Retry when your server is available.") }
        }
    }

    fun configure(server: String) = work {
        tokens.baseUrl = server
        state.value = SessionUiState(loading = true, scope = tokens.scopeGeneration)
        loadIdentity()
    }

    fun refresh() = work { loadIdentity() }

    private suspend fun loadIdentity() {
        if (tokens.baseUrl.isBlank()) {
            state.value = SessionUiState(false, error = "Enter your workspace server address.", scope = tokens.scopeGeneration)
            return
        }
        val response = api().getIdentity()
        coroutineContext.ensureActive()
        if (response.code() in setOf(401, 403)) {
            try { tokens.clearCredentials() }
            finally { state.value = SessionUiState(false, scope = tokens.scopeGeneration) }
        }
        if (!response.isSuccessful) throw IllegalStateException("Could not verify the session (${response.code()}). Sign in again.")
        val identity = response.body() ?: throw IllegalStateException("The server returned an incomplete identity.")
        if (!identity.authenticated && (tokens.nativeAccessToken != null || tokens.principalId != null)) tokens.clearCredentials()
        else {
            tokens.principalId = identity.principal?.id
            tokens.csrfToken = identity.csrfToken
        }
        state.value = SessionUiState(false, identity, tokens.pendingConnection, scope = tokens.scopeGeneration)
    }

    fun startSignIn() = work {
        val verifier = Base64.getUrlEncoder().withoutPadding().encodeToString(ByteArray(32).also { SecureRandom().nextBytes(it) })
        val challenge = Base64.getUrlEncoder().withoutPadding().encodeToString(MessageDigest.getInstance("SHA-256").digest(verifier.toByteArray()))
        val response = api().startNativeConnection(NativeStartRequest(challenge))
        coroutineContext.ensureActive()
        if (!response.isSuccessful) throw IllegalStateException("Could not start sign-in (${response.code()}). Check the server configuration.")
        val connection = response.body() ?: throw IllegalStateException("The server returned an incomplete connection.")
        require(connection.verificationPath.startsWith("/mobile/connect?")) { "The server returned an unsupported sign-in location." }
        tokens.pendingConnection = PendingConnection(connection.requestId, verifier, connection.verificationCode,
            connection.verificationPath, connection.expiresAt)
        state.value = state.value.copy(loading = false, connection = tokens.pendingConnection)
    }

    fun finishSignIn() = work {
        val pending = tokens.pendingConnection ?: throw IllegalStateException("Start sign-in again.")
        val response = api().exchangeNativeConnection(NativeExchangeRequest(pending.requestId, pending.verifier))
        coroutineContext.ensureActive()
        if (!response.isSuccessful) {
            if (response.code() in setOf(401, 404, 410)) tokens.pendingConnection = null
            state.value = state.value.copy(connection = tokens.pendingConnection)
            throw IllegalStateException("This connection could not be completed (${response.code()}). Start sign-in again.")
        }
        val grant = response.body() ?: throw IllegalStateException("The server returned an incomplete session.")
        if (grant.status == "pending") throw IllegalStateException("Confirm the matching code in your browser, then check again.")
        require(grant.tokenType == "Bearer" && !grant.accessToken.isNullOrBlank()) { "The server returned an unsupported session." }
        tokens.clearCredentials()
        tokens.nativeAccessToken = grant.accessToken
        loadIdentity()
    }

    fun logout() = work {
        try {
            tokens.clearSavedDrafts()
            val response = api().logout()
            if (!response.isSuccessful && response.code() != 401) throw IllegalStateException("Could not revoke the server session (${response.code()}).")
        } finally {
            coroutineContext.ensureActive()
            try { tokens.clearCredentials() }
            finally { state.value = SessionUiState(false, scope = tokens.scopeGeneration) }
        }
    }
}
