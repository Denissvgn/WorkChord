package com.workchord.android

import android.security.NetworkSecurityPolicy
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.workchord.android.data.api.NetworkClient
import com.workchord.android.data.api.TokenManager
import okhttp3.logging.HttpLoggingInterceptor
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ReleaseBehaviorTest {
    @Test
    fun exactReleaseConfigurationRejectsCleartextAndNetworkLogging() {
        assertFalse(BuildConfig.DEBUG)
        assertFalse(NetworkSecurityPolicy.getInstance().isCleartextTrafficPermitted)
        assertFalse(NetworkSecurityPolicy.getInstance().isCleartextTrafficPermitted("localhost"))
        assertEquals(HttpLoggingInterceptor.Level.NONE, NetworkClient.loggingInterceptor(false).level)
        try {
            TokenManager.validateServerUrl("http://localhost:4173/", BuildConfig.DEBUG)
            fail("Release credentials must not be sent through cleartext")
        } catch (_: IllegalArgumentException) { }
    }
}
