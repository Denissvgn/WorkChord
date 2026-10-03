package com.workchord.android.data.api

import okhttp3.Interceptor
import okhttp3.Response

class AuthInterceptor(private val tokenManager: TokenManager) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        val builder = originalRequest.newBuilder()
            .header("Accept", "application/json")

        // Add Agent API key if configured
        tokenManager.agentApiKey?.takeIf { it.isNotBlank() }?.let { apiKey ->
            builder.header("X-Agent-API-Key", apiKey)
        }

        tokenManager.nativeAccessToken?.takeIf { it.isNotBlank() }?.let { token ->
            builder.header("Authorization", "Bearer $token")
        }
        if (originalRequest.method !in setOf("GET", "HEAD", "OPTIONS") && tokenManager.cookies.isNotEmpty()) {
            tokenManager.csrfToken?.let { builder.header("X-CSRF-Token", it) }
        }
        return chain.proceed(builder.build())
    }
}
