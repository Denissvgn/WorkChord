package com.workchord.android

import android.app.Application
import com.workchord.android.data.api.NetworkClient
import com.workchord.android.data.api.TokenManager
import com.workchord.android.data.repository.TaskRepository
import com.workchord.android.data.repository.TaskRepositoryImpl

class WorkChordApplication : Application() {

    lateinit var tokenManager: TokenManager
        private set

    lateinit var taskRepository: TaskRepository
        private set

    override fun onCreate() {
        super.onCreate()
        tokenManager = TokenManager(this)
        reconnect()
    }

    fun reconnect() {
        val api = NetworkClient.getApi(tokenManager)
        taskRepository = TaskRepositoryImpl(api, tokenManager)
    }
}
