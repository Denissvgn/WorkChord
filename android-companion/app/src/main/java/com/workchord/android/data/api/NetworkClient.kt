package com.workchord.android.data.api

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object NetworkClient {
    private var apiInstance: WorkChordApi? = null
    private var currentBaseUrl: String? = null

    fun getApi(tokenManager: TokenManager): WorkChordApi {
        val baseUrl = tokenManager.baseUrl.let {
            if (it.endsWith("/")) it else "$it/"
        }

        if (apiInstance == null || currentBaseUrl != baseUrl) {
            val logging = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }

            val okHttpClient = OkHttpClient.Builder()
                .connectTimeout(15, TimeUnit.SECONDS)
                .readTimeout(20, TimeUnit.SECONDS)
                .writeTimeout(20, TimeUnit.SECONDS)
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
        }

        return apiInstance!!
    }
}
