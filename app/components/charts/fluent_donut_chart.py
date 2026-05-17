import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentDonutChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: list[dict] = []
        self._center_text = ""
        self._hovered_index = -1
        self.setMinimumSize(220, 220)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(800)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, data: list[dict], center_text: str = ""):
        self._data = data
        self._center_text = center_text
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
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91", "#008272", "#CA5010", "#E74856", "#00CC6A"]

    def mouseMoveEvent(self, event):
        cx, cy = self.width() / 2, self.height() / 2
        dx, dy = event.position().x() - cx, event.position().y() - cy
        dist = math.hypot(dx, dy)
        size = min(self.width(), self.height())
        outer_r = size / 2 - 20
        inner_r = outer_r * 0.6

        if dist > outer_r or dist < inner_r:
            self._hovered_index = -1
            self.update()
            return super().mouseMoveEvent(event)

        angle = math.degrees(math.atan2(-dy, dx))
        if angle < 0:
            angle += 360

        total = sum(d.get("value", 0) for d in self._data)
        if total == 0:
            return super().mouseMoveEvent(event)

        start = 0
        for i, d in enumerate(self._data):
            sweep = (d.get("value", 0) / total) * 360
            if start <= angle < start + sweep:
                self._hovered_index = i
                break
            start += sweep
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_index = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if not self._data:
            painter.end()
            return

        total = sum(d.get("value", 0) for d in self._data)
        if total == 0:
            painter.end()
            return

        cx, cy = self.width() / 2, self.height() / 2
        size = min(self.width(), self.height())
        outer_r = size / 2 - 20
        inner_r = outer_r * 0.6
        colors = self._chart_colors()

        track_pen = QPen(QColor(tm.color("bg_solid_tertiary")), outer_r - inner_r, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(track_pen)
        painter.drawEllipse(QRectF(cx - (outer_r + inner_r) / 2, cy - (outer_r + inner_r) / 2,
                                    outer_r - inner_r, outer_r - inner_r))

        pen_width = outer_r - inner_r - 2
        start_angle = 90

        for i, d in enumerate(self._data):
            value = d.get("value", 0)
            sweep = (value / total) * 360 * self._anim_progress
            color = QColor(colors[i % len(colors)])
            is_hovered = i == self._hovered_index

            pen = QPen(color.lighter(115) if is_hovered else color, pen_width, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(pen)
            mid_r = (outer_r + inner_r) / 2
            painter.drawArc(QRectF(cx - mid_r, cy - mid_r, mid_r * 2, mid_r * 2),
                            int(start_angle * 16), int(-sweep * 16))
            start_angle -= sweep

        font = QFont()
        font.setPixelSize(tm.font_size("title_large"))
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        if self._center_text:
            painter.drawText(QRectF(cx - 40, cy - 12, 80, 24), Qt.AlignCenter, self._center_text)
        else:
            painter.drawText(QRectF(cx - 40, cy - 12, 80, 24), Qt.AlignCenter, f"{total:.0f}")

        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(QRectF(cx - 40, cy + 10, 80, 16), Qt.AlignCenter, "总计")

        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        legend_y = self.height() - 16
        legend_x = 10
        for i, d in enumerate(self._data):
            name = d.get("name", f"项{i + 1}")
            color = QColor(colors[i % len(colors)])
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(legend_x, legend_y, 8, 8), 2, 2)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(legend_x + 12), int(legend_y + 9), name)
            legend_x += painter.fontMetrics().horizontalAdvance(name) + 24

        painter.end()

    def apply_theme(self):
        self.update()
