package com.workchord.android

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.compose.runtime.*
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import com.workchord.android.ui.screens.ServerSetupScreen
import com.workchord.android.ui.viewmodels.SessionViewModel
import androidx.navigation.compose.rememberNavController
import com.workchord.android.ui.navigation.AppNavigation
import com.workchord.android.ui.theme.WorkChordTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val app = application as WorkChordApplication

        setContent {
            WorkChordTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val session: SessionViewModel = viewModel(factory = object : ViewModelProvider.Factory {
                        @Suppress("UNCHECKED_CAST")
                        override fun <T : ViewModel> create(modelClass: Class<T>): T = SessionViewModel(app.tokenManager) as T
                    })
                    val state by session.uiState.collectAsState()
                    if (state.identity?.authenticated == true) {
                        key(state.scope) {
                            val repository = remember(state.scope) { app.reconnect(); app.taskRepository }
                            val navController = rememberNavController()
                            Column {
                                TextButton(onClick = { session.logout() }, enabled = !state.loading) {
                                    Text("${state.identity?.principal?.displayName ?: "Signed in"} · Sign out")
                                }
                                AppNavigation(navController = navController, taskRepository = repository,
                                    modifier = Modifier.weight(1f))
                            }
                        }
                    } else ServerSetupScreen(session, app.tokenManager.baseUrl)
                }
            }
        }
    }
}
