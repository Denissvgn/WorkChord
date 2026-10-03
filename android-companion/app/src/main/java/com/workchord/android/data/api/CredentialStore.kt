package com.workchord.android.data.api

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.io.File
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

interface CredentialStore {
    fun read(): String?
    fun write(value: String?)
}

class EncryptedCredentialStore(context: Context, private val fileName: String = "native-session.bin") : CredentialStore {
    init { require(fileName.matches(Regex("[A-Za-z0-9_.-]+")) && fileName != "." && fileName != "..") }
    private val file = File(context.noBackupFilesDir, fileName)

    private fun key(): SecretKey {
        val store = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (store.getKey(ALIAS, null) as? SecretKey)?.let { return it }
        return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore").apply {
            init(KeyGenParameterSpec.Builder(ALIAS, KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE).build())
        }.generateKey()
    }

    @Synchronized
    override fun read(): String? {
        if (!file.exists()) return null
        return try {
            val payload = file.readBytes()
            require(payload.size > 12)
            val cipher = Cipher.getInstance("AES/GCM/NoPadding")
            cipher.init(Cipher.DECRYPT_MODE, key(), GCMParameterSpec(128, payload.copyOfRange(0, 12)))
            String(cipher.doFinal(payload.copyOfRange(12, payload.size)), Charsets.UTF_8)
        } catch (_: Exception) {
            file.delete()
            null // Invalidated device keys require a fresh sign-in.
        }
    }

    @Synchronized
    override fun write(value: String?) {
        if (value == null) {
            file.delete()
            return
        }
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, key())
        val temporary = File(file.parentFile, "$fileName.pending")
        temporary.writeBytes(cipher.iv + cipher.doFinal(value.toByteArray(Charsets.UTF_8)))
        check(temporary.renameTo(file)) { "Could not securely save the session. Sign in again." }
    }

    companion object {
        private const val ALIAS = "workchord-native-session"
    }
}
