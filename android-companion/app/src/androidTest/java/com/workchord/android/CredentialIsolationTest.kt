package com.workchord.android

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import com.workchord.android.data.api.TokenManager
import com.workchord.android.data.api.EncryptedCredentialStore
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File

@RunWith(AndroidJUnit4::class)
class CredentialIsolationTest {
    @Test
    fun keystorePersistenceIsPrivateAndAccountChangesClearAuthority() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val prefs = context.getSharedPreferences("workchord_auth_prefs", 0)
        prefs.edit().putString("key_agent_api_key", "obsolete-synthetic-key")
            .putString("key_session_token", "obsolete-synthetic-session").commit()
        val tokens = TokenManager(context)
        tokens.clear()
        tokens.baseUrl = "https://fixture.invalid/"
        tokens.nativeAccessToken = "synthetic-native-secret"
        tokens.principalId = 19
        val stored = File(context.noBackupFilesDir, "native-session.bin")
        assertTrue(stored.exists())
        assertFalse(stored.readText().contains("synthetic-native-secret"))
        assertFalse(prefs.contains("key_agent_api_key"))
        assertFalse(prefs.contains("key_session_token"))
        assertEquals("synthetic-native-secret", TokenManager(context).nativeAccessToken)
        val scope = requireNotNull(tokens.draftScope())
        tokens.draftStorage!!.write(scope, 72, "synthetic-private-draft")
        val draft = File(context.noBackupFilesDir, "draft-$scope-72.bin")
        assertFalse(draft.readText().contains("synthetic-private-draft"))
        assertEquals("synthetic-private-draft", tokens.draftStorage.read(scope, 72))
        tokens.principalId = 20
        assertNull(tokens.nativeAccessToken)
        assertNotEquals(scope, tokens.draftScope())
        tokens.principalId = 19
        tokens.clearSavedDrafts()
        assertFalse(draft.exists())
        tokens.clear()
        assertFalse(stored.exists())
    }

    @Test
    fun invalidCiphertextIsDiscardedWithoutRestoringCredentials() {
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val store = EncryptedCredentialStore(context, "storage-probe.bin")
        store.write("synthetic-secret")
        val file = File(context.noBackupFilesDir, "storage-probe.bin")
        file.writeBytes(byteArrayOf(1, 2, 3))
        assertNull(store.read())
        assertFalse(file.exists())
    }
}
