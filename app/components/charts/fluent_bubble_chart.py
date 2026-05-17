from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentBubbleChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._series: list[dict] = []
        self._margin = {"top": 30, "right": 20, "bottom": 40, "left": 50}
        self._hovered = -1
        self.setMinimumSize(300, 250)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, series: list[dict]):
        self._series = series
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    @Property(float)
    def anim_progress(self):
        return self._anim_progress

    @anim_progress.setter
    def anim_progress(self, v):
        self._anim_progress = v
        self.update()

    def _chart_colors(self):
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91", "#008272", "#CA5010", "#486860", "#8A5966"]

    def mouseMoveEvent(self, event):
        self._hovered = self._bubble_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -1
        self.update()
        super().leaveEvent(event)

    def _bubble_at(self, pos):
        m = self._margin
        chart_w = self.width() - m["left"] - m["right"]
        chart_h = self.height() - m["top"] - m["bottom"]
        all_data = [d for s in self._series for d in s.get("data", [])]
        if not all_data:
            return -1
        max_x = max(d[0] for d in all_data) or 1
        max_y = max(d[1] for d in all_data) or 1
        max_r = max(d[2] for d in all_data) or 1
        idx = 0
        for si, series in enumerate(self._series):
            for di, (x, y, r) in enumerate(series.get("data", [])):
                cx = m["left"] + (x / max_x) * chart_w
                cy = m["top"] + chart_h - (y / max_y) * chart_h
                radius = (r / max_r) * 30 + 8
                dx = pos.x() - cx
                dy = pos.y() - cy
                if dx * dx + dy * dy <= radius * radius:
                    return idx
                idx += 1
        return -1

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        m = self._margin
        chart_x = m["left"]
        chart_y = m["top"]
        chart_w = self.width() - m["left"] - m["right"]
        chart_h = self.height() - m["top"] - m["bottom"]

        if not self._series:
            painter.end()
            return

        all_data = [d for s in self._series for d in s.get("data", [])]
        if not all_data:
            painter.end()
            return

        max_x = max(d[0] for d in all_data) or 1
        max_y = max(d[1] for d in all_data) or 1
        max_r = max(d[2] for d in all_data) or 1

        painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1))
        for i in range(5):
            y = chart_y + chart_h - (i / 4) * chart_h
            painter.drawLine(int(chart_x), int(y), int(chart_x + chart_w), int(y))
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            val = max_y * i / 4
            painter.drawText(0, int(y - 6), int(chart_x - 6), 16, Qt.AlignRight | Qt.AlignVCenter, f"{val:.0f}")

        colors = self._chart_colors()
        idx = 0
        for si, series in enumerate(self._series):
            color = QColor(colors[si % len(colors)])
            for di, (x, y, r) in enumerate(series.get("data", [])):
                cx = chart_x + (x / max_x) * chart_w
                cy = chart_y + chart_h - (y / max_y) * chart_h
                radius = (r / max_r) * 30 + 8
                radius *= self._anim_progress

                is_hovered = idx == self._hovered
                c = QColor(color)
                if is_hovered:
                    c = c.lighter(130)
                c.setAlpha(int(180 * self._anim_progress))

                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(c))
                painter.drawEllipse(QRectF(cx - radius, cy - radius, radius * 2, radius * 2))

                if is_hovered:
                    painter.setPen(QColor(tm.color("fg_primary")))
                    font = QFont()
                    font.setPixelSize(tm.font_size("caption"))
                    painter.setFont(font)
                    painter.drawText(int(cx - 30), int(cy - radius - 16), 60, 16, Qt.AlignCenter, f"({x},{y}) r={r}")

                idx += 1

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        legend_x = chart_x
        legend_y = 4
        for si, series in enumerate(self._series):
            name = series.get("name", f"系列{si + 1}")
            color = QColor(colors[si % len(colors)])
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(legend_x, legend_y, 10, 10), 2, 2)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(legend_x + 14), int(legend_y + 10), name)
            legend_x += painter.fontMetrics().horizontalAdvance(name) + 28

        painter.end()

    def apply_theme(self):
        self.update()
