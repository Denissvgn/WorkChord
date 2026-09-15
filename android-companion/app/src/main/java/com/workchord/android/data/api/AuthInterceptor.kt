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

        // The backend's opaque browser session is carried in its named cookie.
        tokenManager.sessionToken?.takeIf { it.isNotBlank() }?.let { token ->
            builder.header("Cookie", "workchord_session=$token")
        }

        val response = chain.proceed(builder.build())

        // Extract and persist session cookies if present
        val cookies = response.headers("Set-Cookie")
        for (cookie in cookies) {
            if (cookie.startsWith("workchord_session=")) {
                val token = cookie.substringAfter("workchord_session=").substringBefore(";")
                if (token.isNotBlank()) {
                    tokenManager.sessionToken = token
                }
            }
        }

        return response
    }
}
