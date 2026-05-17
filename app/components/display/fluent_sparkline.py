import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QPainterPath, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSparkline(QWidget, FluentWidgetBase):
    valueHovered = Signal(int, float)
    _draw_progress = 0.0

    def __init__(self, data: list = None, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data = data or []
        self._positive_color = "primary"
        self._negative_color = "accent_error"
        self._hovered_index = -1
        self.setFixedSize(200, 60)

        self._draw_anim = QPropertyAnimation(self, b"draw_progress")
        self._draw_anim.setDuration(800)
        self._draw_anim.setEasingCurve(QEasingCurve.OutCubic)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, values: list):
        self._data = values
        self._draw_anim.stop()
        self._draw_anim.setStartValue(0.0)
        self._draw_anim.setEndValue(1.0)
        self._draw_anim.start()

    def set_color(self, positive: str, negative: str):
        self._positive_color = positive
        self._negative_color = negative

    @Property(float)
    def draw_progress(self):
        return self._draw_progress

    @draw_progress.setter
    def draw_progress(self, value):
        self._draw_progress = value
        self.update()

    def mouseMoveEvent(self, event):
        if len(self._data) < 2:
            return super().mouseMoveEvent(event)
        x = event.position().x()
        step = (self.width() - 16) / max(1, len(self._data) - 1)
        idx = int(round((x - 8) / step))
        idx = max(0, min(idx, len(self._data) - 1))
        if idx != self._hovered_index:
            self._hovered_index = idx
            self.valueHovered.emit(idx, self._data[idx])
            self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_index = -1
        self.update()
        super().leaveEvent(event)

    def _catmull_rom_point(self, p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        x = 0.5 * ((2 * p1[0]) +
                     (-p0[0] + p2[0]) * t +
                     (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                     (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
        y = 0.5 * ((2 * p1[1]) +
                     (-p0[1] + p2[1]) * t +
                     (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                     (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
        return (x, y)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if len(self._data) < 2:
            painter.end()
            return

        margin_x = 8
        margin_y = 8
        w = self.width() - margin_x * 2
        h = self.height() - margin_y * 2

        min_val = min(self._data)
        max_val = max(self._data)
        val_range = max_val - min_val if max_val != min_val else 1

        points = []
        step = w / max(1, len(self._data) - 1)
        for i, val in enumerate(self._data):
            x = margin_x + i * step
            y = margin_y + h - ((val - min_val) / val_range) * h
            points.append((x, y))

        visible_count = max(2, int(len(points) * self._draw_progress))
        visible_points = points[:visible_count]

        if len(visible_points) >= 2:
            line_path = QPainterPath()
            line_path.moveTo(visible_points[0][0], visible_points[0][1])

            for i in range(1, len(visible_points)):
                if len(visible_points) >= 4:
                    p0 = visible_points[max(0, i - 2)]
                    p1 = visible_points[i - 1]
                    p2 = visible_points[i]
                    p3 = visible_points[min(len(visible_points) - 1, i + 1)]
                    prev = self._catmull_rom_point(p0, p1, p2, p3, 0)
                    curr = self._catmull_rom_point(p0, p1, p2, p3, 1)
                    line_path.lineTo(curr[0], curr[1])
                else:
                    line_path.lineTo(visible_points[i][0], visible_points[i][1])

            is_positive = self._data[-1] >= self._data[0]
            color_key = self._positive_color if is_positive else self._negative_color
            line_color = QColor(tm.color(color_key))

            painter.setPen(QPen(line_color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(line_path)

            fill_path = QPainterPath(line_path)
            last_x = visible_points[-1][0]
            first_x = visible_points[0][0]
            fill_path.lineTo(last_x, margin_y + h)
            fill_path.lineTo(first_x, margin_y + h)
            fill_path.closeSubpath()

            gradient = QLinearGradient(0, margin_y, 0, margin_y + h)
            fill_color = QColor(line_color)
            fill_color.setAlpha(40)
            gradient.setColorAt(0, fill_color)
            fill_color.setAlpha(5)
            gradient.setColorAt(1, fill_color)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(gradient))
            painter.drawPath(fill_path)

        if 0 <= self._hovered_index < len(points):
            hx, hy = points[self._hovered_index]
            painter.setPen(QPen(line_color, 2))
            painter.drawLine(int(hx), margin_y, int(hx), margin_y + h)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(line_color))
            painter.drawEllipse(QRectF(hx - 4, hy - 4, 8, 8))

            painter.setBrush(QColor(tm.color("bg_solid_card")))
            painter.drawEllipse(QRectF(hx - 2, hy - 2, 4, 4))

            val_text = f"{self._data[self._hovered_index]:.1f}"
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            text_w = painter.fontMetrics().horizontalAdvance(val_text) + 8
            tooltip_rect = QRectF(hx - text_w / 2, hy - 24, text_w, 18)
            painter.setBrush(QColor(tm.color("bg_solid_card")))
            painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
            painter.drawRoundedRect(tooltip_rect, 4, 4)
            painter.setPen(QColor(tm.color("fg_primary")))
            painter.drawText(tooltip_rect, Qt.AlignCenter, val_text)

        painter.end()

    def apply_theme(self):
        self.update()
