package com.workchord.android.data.api

import okhttp3.Interceptor
import okhttp3.Response
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import java.io.IOException

class AuthInterceptor(private val tokenManager: TokenManager) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val generation = tokenManager.scopeGeneration
        val originalRequest = chain.request()
        val configured = tokenManager.baseUrl.toHttpUrlOrNull()
        if (configured == null || configured.scheme != originalRequest.url.scheme ||
            configured.host != originalRequest.url.host || configured.port != originalRequest.url.port) {
            throw IOException("The server address changed. Reconnect before sending credentials.")
        }
        val builder = originalRequest.newBuilder()
            .header("Accept", "application/json")

        tokenManager.nativeAccessToken?.takeIf { it.isNotBlank() }?.let { token ->
            builder.header("Authorization", "Bearer $token")
        }
        if (originalRequest.method !in setOf("GET", "HEAD", "OPTIONS") && tokenManager.cookies.isNotEmpty()) {
            tokenManager.csrfToken?.let { builder.header("X-CSRF-Token", it) }
        }
        tokenManager.requestGeneration.set(generation)
        return try {
            if (!tokenManager.requestScopeIsCurrent()) throw IOException("Account changed. Reload before sending credentials.")
            chain.proceed(builder.build())
        }
        finally { tokenManager.requestGeneration.remove() }
    }
}
