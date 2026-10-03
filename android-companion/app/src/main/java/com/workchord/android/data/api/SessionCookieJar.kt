package com.workchord.android.data.api

import okhttp3.Cookie
import okhttp3.CookieJar
import okhttp3.HttpUrl
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull

class SessionCookieJar(private val tokens: TokenManager) : CookieJar {
    private fun sameOrigin(url: HttpUrl): Boolean {
        val configured = tokens.baseUrl.toHttpUrlOrNull() ?: return false
        return configured.scheme == url.scheme && configured.host == url.host && configured.port == url.port
    }

    @Synchronized
    override fun saveFromResponse(url: HttpUrl, cookies: List<Cookie>) {
        if (!sameOrigin(url)) return
        val current = tokens.cookies.mapNotNull { Cookie.parse(url, it) }.toMutableList()
        for (cookie in cookies) {
            current.removeAll { it.name == cookie.name && it.domain == cookie.domain && it.path == cookie.path }
            if (cookie.expiresAt > System.currentTimeMillis()) current.add(cookie)
        }
        tokens.cookies = current.filter { it.expiresAt > System.currentTimeMillis() }.map { it.toString() }
    }

    @Synchronized
    override fun loadForRequest(url: HttpUrl): List<Cookie> {
        if (!sameOrigin(url)) return emptyList()
        return tokens.cookies.mapNotNull { Cookie.parse(url, it) }
            .filter { it.expiresAt > System.currentTimeMillis() && it.matches(url) }
    }
}
