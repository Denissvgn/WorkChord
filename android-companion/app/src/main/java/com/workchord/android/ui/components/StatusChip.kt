package com.workchord.android.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import com.workchord.android.R
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.unit.dp
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.ui.theme.StatusActiveBg
import com.workchord.android.ui.theme.StatusActiveColor
import com.workchord.android.ui.theme.StatusBlockedBg
import com.workchord.android.ui.theme.StatusBlockedColor
import com.workchord.android.ui.theme.StatusClosedBg
import com.workchord.android.ui.theme.StatusClosedColor
import com.workchord.android.ui.theme.StatusPlannedBg
import com.workchord.android.ui.theme.StatusPlannedColor
import com.workchord.android.ui.theme.StatusResolvedBg
import com.workchord.android.ui.theme.StatusResolvedColor

@Composable
fun StatusChip(
    status: TaskStatus,
    modifier: Modifier = Modifier
) {
    val dark = MaterialTheme.colorScheme.surface.luminance() < 0.2f
    val textColor = when (status) {
        TaskStatus.PLANNED, TaskStatus.UNKNOWN -> if (dark) Color(0xFFCBD5E1) else Color(0xFF334155)
        TaskStatus.ACTIVE -> if (dark) Color(0xFF67E8F9) else Color(0xFF0E7490)
        TaskStatus.RESOLVED -> if (dark) Color(0xFF6EE7B7) else Color(0xFF047857)
        TaskStatus.CLOSED -> if (dark) Color(0xFFC4B5FD) else Color(0xFF6D28D9)
    }
    val bgColor = textColor.copy(alpha = 0.12f)

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(12.dp))
            .background(bgColor)
            .padding(horizontal = 8.dp, vertical = 4.dp)
    ) {
        Text(
            text = stringResource(when (status) {
                TaskStatus.PLANNED -> R.string.status_planned
                TaskStatus.ACTIVE -> R.string.status_active
                TaskStatus.RESOLVED -> R.string.status_resolved
                TaskStatus.CLOSED -> R.string.status_closed
                TaskStatus.UNKNOWN -> R.string.status_unknown
            }),
            color = textColor,
            style = MaterialTheme.typography.labelMedium
        )
    }
}
