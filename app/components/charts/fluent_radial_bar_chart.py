import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentRadialBarChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: list[dict] = []
        self._hovered = -1
        self.setMinimumSize(250, 250)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(700)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, data: list[dict]):
        self._data = data
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
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91", "#008272", "#CA5010"]

    def mouseMoveEvent(self, event):
        self._hovered = self._arc_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -1
        self.update()
        super().leaveEvent(event)

    def _arc_at(self, pos):
        if not self._data:
            return -1
        cx = self.width() / 2
        cy = self.height() / 2
        dx = pos.x() - cx
        dy = pos.y() - cy
        dist = math.sqrt(dx * dx + dy * dy)
        n = len(self._data)
        bar_width = 16
        gap = 6
        max_r = min(self.width(), self.height()) / 2 - 20
        for i in range(n - 1, -1, -1):
            r = max_r - i * (bar_width + gap)
            if abs(dist - r) < bar_width / 2 + 2:
                return i
        return -1

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if not self._data:
            painter.end()
            return

        cx = self.width() / 2
        cy = self.height() / 2
        n = len(self._data)
        bar_width = 16
        gap = 6
        max_r = min(self.width(), self.height()) / 2 - 20
        colors = self._chart_colors()

        for i, d in enumerate(self._data):
            r = max_r - i * (bar_width + gap)
            pct = d.get("value", 0) / 100.0
            name = d.get("name", "")

            bg_color = QColor(tm.color("bg_solid_tertiary"))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(bg_color))
            painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))

            color = QColor(colors[i % len(colors)])
            is_hovered = i == self._hovered
            if is_hovered:
                color = color.lighter(120)

            start_angle = 90 * 16
            span_angle = int(-pct * 360 * 16 * self._anim_progress)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawArc(QRectF(cx - r, cy - r, r * 2, r * 2), start_angle, span_angle)

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(cx + r + 8), int(cy - i * (bar_width + gap) - bar_width / 2 + 4), 80, 16, Qt.AlignLeft | Qt.AlignVCenter, f"{name} {d.get('value', 0)}%")

        painter.end()

    def apply_theme(self):
        self.update()
