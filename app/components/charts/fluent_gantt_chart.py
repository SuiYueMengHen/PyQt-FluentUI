from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentGanttChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._tasks: list[dict] = []
        self._row_height = 32
        self._margin = {"top": 30, "right": 20, "bottom": 10, "left": 100}
        self._hovered = -1
        self.setMinimumSize(400, 200)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, tasks: list[dict]):
        self._tasks = tasks
        self.setFixedHeight(max(len(tasks) * self._row_height + self._margin["top"] + self._margin["bottom"] + 10, 100))
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
        m = self._margin
        y = event.position().y()
        idx = int((y - m["top"]) / self._row_height)
        if 0 <= idx < len(self._tasks) and y >= m["top"]:
            self._hovered = idx
        else:
            self._hovered = -1
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        m = self._margin
        if not self._tasks:
            painter.end()
            return

        all_starts = [t.get("start", 0) for t in self._tasks]
        all_ends = [t.get("end", 0) for t in self._tasks]
        min_t = min(all_starts) if all_starts else 0
        max_t = max(all_ends) if all_ends else 1
        span = max_t - min_t or 1

        chart_x = m["left"]
        chart_y = m["top"]
        chart_w = self.width() - m["left"] - m["right"]
        chart_h = self.height() - m["top"] - m["bottom"]

        painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1, Qt.DotLine))
        for i in range(6):
            x = chart_x + (i / 5) * chart_w
            painter.drawLine(int(x), int(chart_y), int(x), int(chart_y + chart_h))
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            val = min_t + span * i / 5
            painter.drawText(int(x - 20), int(chart_y - 6), 40, 16, Qt.AlignCenter, f"{val:.0f}")

        colors = self._chart_colors()
        for i, task in enumerate(self._tasks):
            y = chart_y + i * self._row_height + 4
            h = self._row_height - 8

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(4, int(y), int(m["left"] - 8), int(h), Qt.AlignRight | Qt.AlignVCenter, task.get("name", ""))

            start = task.get("start", 0)
            end = task.get("end", 0)
            x1 = chart_x + ((start - min_t) / span) * chart_w
            x2 = chart_x + ((end - min_t) / span) * chart_w
            bar_w = (x2 - x1) * self._anim_progress

            color = QColor(colors[i % len(colors)])
            is_hovered = i == self._hovered
            if is_hovered:
                color = color.lighter(120)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(x1, y, bar_w, h), 4, 4)

            if is_hovered:
                painter.setPen(QColor(tm.color("fg_primary")))
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.drawText(int(x1 + bar_w + 6), int(y), 80, int(h), Qt.AlignVCenter | Qt.AlignLeft, f"{start}-{end}")

        painter.end()

    def apply_theme(self):
        self.update()
