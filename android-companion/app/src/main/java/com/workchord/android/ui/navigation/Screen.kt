package com.workchord.android.ui.navigation

sealed class Screen(val route: String) {
    data object MyWork : Screen("my_work")
    data object TaskDetail : Screen("task_detail/{taskId}") {
        fun createRoute(taskId: Int) = "task_detail/$taskId"
    }
}
