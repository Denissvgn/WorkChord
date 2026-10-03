package com.workchord.android.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.workchord.android.ui.viewmodels.SessionViewModel

@Composable
fun ServerSetupScreen(viewModel: SessionViewModel, baseUrl: String) {
    val state by viewModel.uiState.collectAsState()
    var server by remember(baseUrl) { mutableStateOf(baseUrl) }
    val context = LocalContext.current
    Column(Modifier.fillMaxSize().safeDrawingPadding().verticalScroll(rememberScrollState()).padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Text("Connect to WorkChord", style = MaterialTheme.typography.headlineSmall)
        Text("Enter your workspace server, then sign in through your browser.", style = MaterialTheme.typography.bodyLarge)
        OutlinedTextField(server, { server = it }, Modifier.fillMaxWidth(), label = { Text("Server address") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Uri), singleLine = true, enabled = !state.loading)
        OutlinedButton({ viewModel.configure(server) }, enabled = !state.loading, modifier = Modifier.fillMaxWidth()) { Text("Use this server") }
        if (state.loading) LinearProgressIndicator(Modifier.fillMaxWidth())
        state.error?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodyLarge) }
        val connection = state.connection
        if (connection != null) {
            Text("Compare this code in your browser", style = MaterialTheme.typography.titleMedium)
            Text(connection.verificationCode, style = MaterialTheme.typography.headlineMedium)
            Text("Only approve a connection you started on this device.")
            Button({ context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(baseUrl.trimEnd('/') + connection.verificationPath))) },
                enabled = !state.loading, modifier = Modifier.fillMaxWidth()) { Text("Open browser to sign in") }
            OutlinedButton({ viewModel.finishSignIn() }, enabled = !state.loading, modifier = Modifier.fillMaxWidth()) { Text("Check connection") }
        } else {
            Button({ viewModel.startSignIn() }, enabled = !state.loading && state.identity?.configured == true,
                modifier = Modifier.fillMaxWidth()) { Text("Sign in") }
            if (state.identity?.configured == false) Text("This server has no configured sign-in provider. Ask its operator to configure managed authentication.")
            TextButton({ viewModel.refresh() }, enabled = !state.loading) { Text("Retry server check") }
        }
    }
}
