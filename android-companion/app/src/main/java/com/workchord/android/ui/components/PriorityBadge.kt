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
import com.workchord.android.ui.theme.PriorityHighColor
import com.workchord.android.ui.theme.PriorityLowColor
import com.workchord.android.ui.theme.PriorityMediumColor

@Composable
fun PriorityBadge(
    priority: Int,
    modifier: Modifier = Modifier
) {
    val (bgColor, textColor, label) = when {
        priority >= 8 -> Triple(Color(0x22EF4444), PriorityHighColor, "P$priority High")
        priority >= 5 -> Triple(Color(0x22F59E0B), PriorityMediumColor, "P$priority Med")
        else -> Triple(Color(0x2210B981), PriorityLowColor, "P$priority Low")
    }

    Box(
        modifier = modifier
            .clip(RoundedCornerShape(6.dp))
            .background(bgColor)
            .padding(horizontal = 6.dp, vertical = 2.dp)
    ) {
        Text(
            text = label,
            color = textColor,
            style = MaterialTheme.typography.labelSmall
        )
    }
}
