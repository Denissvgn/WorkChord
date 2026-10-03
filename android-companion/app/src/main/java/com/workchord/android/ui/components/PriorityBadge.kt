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
import com.workchord.android.ui.theme.PriorityHighColor
import com.workchord.android.ui.theme.PriorityLowColor
import com.workchord.android.ui.theme.PriorityMediumColor

@Composable
fun PriorityBadge(
    priority: Int,
    modifier: Modifier = Modifier
) {
    val dark = MaterialTheme.colorScheme.surface.luminance() < 0.2f
    val (textColor, label) = when {
        priority <= 3 -> (if (dark) Color(0xFFFCA5A5) else Color(0xFFB91C1C)) to stringResource(R.string.priority_high, priority)
        priority <= 6 -> (if (dark) Color(0xFFFCD34D) else Color(0xFF92400E)) to stringResource(R.string.priority_medium, priority)
        else -> (if (dark) Color(0xFF6EE7B7) else Color(0xFF047857)) to stringResource(R.string.priority_low, priority)
    }
    val bgColor = textColor.copy(alpha = 0.12f)

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(6.dp))
            .background(bgColor)
            .padding(horizontal = 6.dp, vertical = 2.dp)
    ) {
        Text(
            text = label,
            color = textColor,
            style = MaterialTheme.typography.labelMedium
        )
    }
}
