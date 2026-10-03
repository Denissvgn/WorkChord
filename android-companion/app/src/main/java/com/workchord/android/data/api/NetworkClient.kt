package com.workchord.android.data.api

import com.workchord.android.BuildConfig
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object NetworkClient {
    private var apiInstance: WorkChordApi? = null
    private var currentBaseUrl: String? = null
    private var currentTokenManager: TokenManager? = null

    fun getApi(tokenManager: TokenManager): WorkChordApi {
        val baseUrl = tokenManager.baseUrl.let {
            if (it.endsWith("/")) it else "$it/"
        }

        if (apiInstance == null || currentBaseUrl != baseUrl || currentTokenManager !== tokenManager) {
            val logging = loggingInterceptor(BuildConfig.DEBUG)

            val okHttpClient = OkHttpClient.Builder()
                .connectTimeout(15, TimeUnit.SECONDS)
                .readTimeout(20, TimeUnit.SECONDS)
                .writeTimeout(20, TimeUnit.SECONDS)
                .followRedirects(false)
                .followSslRedirects(false)
                .cookieJar(SessionCookieJar(tokenManager))
                .addInterceptor(TransportPolicyInterceptor({ tokenManager.baseUrl }, BuildConfig.DEBUG))
                .addInterceptor(AuthInterceptor(tokenManager))
                .addInterceptor(logging)
                .build()

            val retrofit = Retrofit.Builder()
                .baseUrl(baseUrl)
                .client(okHttpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .build()

            apiInstance = retrofit.create(WorkChordApi::class.java)
            currentBaseUrl = baseUrl
            currentTokenManager = tokenManager
        }

        return apiInstance!!
    }

    internal fun loggingInterceptor(
        debug: Boolean,
        logger: HttpLoggingInterceptor.Logger = HttpLoggingInterceptor.Logger.DEFAULT
    ): HttpLoggingInterceptor = HttpLoggingInterceptor(logger).apply {
        level = if (debug) HttpLoggingInterceptor.Level.BASIC else HttpLoggingInterceptor.Level.NONE
        for (header in listOf("Authorization", "Proxy-Authorization", "Cookie", "Set-Cookie", "X-Agent-API-Key", "X-CSRF-Token")) {
            redactHeader(header)
        }
    }
}
