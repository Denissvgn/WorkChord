package com.workchord.android.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
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
    val (bgColor, textColor) = when (status) {
        TaskStatus.PLANNED -> StatusPlannedBg to StatusPlannedColor
        TaskStatus.ACTIVE -> StatusActiveBg to StatusActiveColor
        TaskStatus.RESOLVED -> StatusResolvedBg to StatusResolvedColor
        TaskStatus.CLOSED -> StatusClosedBg to StatusClosedColor
        TaskStatus.BLOCKED -> StatusBlockedBg to StatusBlockedColor
    }

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(12.dp))
            .background(bgColor)
            .padding(horizontal = 8.dp, vertical = 4.dp)
    ) {
        Text(
            text = status.displayName,
            color = textColor,
            style = MaterialTheme.typography.labelSmall
        )
    }
}
