package com.workchord.android.data.api

import android.content.Context

interface DraftStorage {
    fun read(scope: String, taskId: Int): String?
    fun write(scope: String, taskId: Int, value: String?)
    fun clear(scope: String)
}

class EncryptedDraftStorage(private val context: Context) : DraftStorage {
    private fun name(scope: String, taskId: Int): String {
        require(scope.matches(Regex("[a-f0-9]{64}")) && taskId > 0)
        return "draft-$scope-$taskId.bin"
    }
    override fun read(scope: String, taskId: Int) = EncryptedCredentialStore(context, name(scope, taskId)).read()
    override fun write(scope: String, taskId: Int, value: String?) = EncryptedCredentialStore(context, name(scope, taskId)).write(value)
    override fun clear(scope: String) {
        require(scope.matches(Regex("[a-f0-9]{64}")))
        context.noBackupFilesDir.listFiles().orEmpty().filter { it.name.startsWith("draft-$scope-") }.forEach { file ->
            check(file.delete() || !file.exists()) { "Could not clear the private saved draft." }
        }
    }
}
