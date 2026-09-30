package com.workchord.android.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.workchord.android.data.repository.TaskRepository
import com.workchord.android.ui.screens.MyWorkScreen
import com.workchord.android.ui.screens.TaskDetailScreen
import com.workchord.android.ui.viewmodels.MyWorkViewModel
import com.workchord.android.ui.viewmodels.MyWorkViewModelFactory
import com.workchord.android.ui.viewmodels.TaskDetailViewModel
import com.workchord.android.ui.viewmodels.TaskDetailViewModelFactory

@Composable
fun AppNavigation(
    navController: NavHostController,
    taskRepository: TaskRepository,
    modifier: Modifier = Modifier
) {
    NavHost(
        navController = navController,
        startDestination = Screen.MyWork.route,
        modifier = modifier
    ) {
        composable(Screen.MyWork.route) {
            val viewModel: MyWorkViewModel = viewModel(
                factory = MyWorkViewModelFactory(taskRepository)
            )
            MyWorkScreen(
                viewModel = viewModel,
                onTaskClick = { taskId ->
                    navController.navigate(Screen.TaskDetail.createRoute(taskId))
                }
            )
        }

        composable(
            route = Screen.TaskDetail.route,
            arguments = listOf(
                navArgument("taskId") { type = NavType.IntType }
            )
        ) { backStackEntry ->
            val taskId = backStackEntry.arguments?.getInt("taskId") ?: 0
            val viewModel: TaskDetailViewModel = viewModel(
                factory = TaskDetailViewModelFactory(taskId, taskRepository)
            )
            TaskDetailScreen(
                viewModel = viewModel,
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }
    }
}
