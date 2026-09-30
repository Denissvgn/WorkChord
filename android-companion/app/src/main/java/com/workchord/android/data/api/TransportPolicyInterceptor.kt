package com.workchord.android.data.api

import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import okhttp3.Interceptor
import okhttp3.Response
import java.io.IOException

class TransportPolicyInterceptor(
    private val configuredUrl: () -> String,
    private val debug: Boolean
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        val url = request.url
        if (url.username.isNotEmpty() || url.password.isNotEmpty()) {
            throw IOException("Do not embed credentials in the WorkChord server address.")
        }
        val localDebug = debug && url.scheme == "http" &&
            url.host in setOf("10.0.2.2", "127.0.0.1", "localhost")
        if (url.scheme != "https" && !localDebug) {
            throw IOException("WorkChord requires HTTPS. Debug HTTP is limited to local development hosts.")
        }
        val configured = configuredUrl().toHttpUrlOrNull()
            ?: throw IOException("Configure a valid WorkChord server address.")
        if (configured.scheme != url.scheme || configured.host != url.host || configured.port != url.port) {
            throw IOException("The server address changed. Reconnect before sending credentials.")
        }
        return chain.proceed(request)
    }
}
