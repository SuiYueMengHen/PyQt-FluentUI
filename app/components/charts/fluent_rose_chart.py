import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentRoseChart(QWidget, FluentWidgetBase):
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
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91", "#008272", "#CA5010", "#486860", "#8A5966"]

    def mouseMoveEvent(self, event):
        self._hovered = self._sector_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -1
        self.update()
        super().leaveEvent(event)

    def _sector_at(self, pos):
        if not self._data:
            return -1
        cx = self.width() / 2
        cy = self.height() / 2
        dx = pos.x() - cx
        dy = pos.y() - cy
        dist = math.sqrt(dx * dx + dy * dy)
        max_val = max(d.get("value", 0) for d in self._data) or 1
        max_r = min(self.width(), self.height()) / 2 - 30
        angle = (math.degrees(math.atan2(-dy, dx)) + 360) % 360
        start = 0
        total = sum(d.get("value", 0) for d in self._data) or 1
        for i, d in enumerate(self._data):
            sweep = (d.get("value", 0) / total) * 360
            r = (d.get("value", 0) / max_val) * max_r
            if start <= angle < start + sweep and dist <= r:
                return i
            start += sweep
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
        max_val = max(d.get("value", 0) for d in self._data) or 1
        max_r = min(self.width(), self.height()) / 2 - 30
        total = sum(d.get("value", 0) for d in self._data) or 1
        colors = self._chart_colors()

        start_angle = 0
        for i, d in enumerate(self._data):
            val = d.get("value", 0)
            sweep = (val / total) * 360
            r = (val / max_val) * max_r * self._anim_progress

            color = QColor(colors[i % len(colors)])
            is_hovered = i == self._hovered
            if is_hovered:
                color = color.lighter(120)

            painter.setPen(QPen(QColor(tm.color("bg_solid_card")), 2))
            painter.setBrush(QBrush(color))
            painter.drawPie(QRectF(cx - r, cy - r, r * 2, r * 2), int(start_angle * 16), int(sweep * 16))

            if is_hovered:
                mid_angle = math.radians(start_angle + sweep / 2)
                label_r = r + 16
                lx = cx + math.cos(mid_angle) * label_r
                ly = cy - math.sin(mid_angle) * label_r
                font = QFont()
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(int(lx - 30), int(ly - 8), 60, 16, Qt.AlignCenter, f"{d.get('name', '')}: {val}")

            start_angle += sweep

        painter.end()

    def apply_theme(self):
        self.update()
