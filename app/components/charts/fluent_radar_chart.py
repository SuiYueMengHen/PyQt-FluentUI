import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentRadarChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._series: list[dict] = []
        self._dimensions: list[str] = []
        self.setMinimumSize(250, 250)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, dimensions: list[str], series: list[dict]):
        self._dimensions = dimensions
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
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91"]

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if not self._dimensions or not self._series:
            painter.end()
            return

        cx, cy = self.width() / 2, self.height() / 2
        radius = min(self.width(), self.height()) / 2 - 40
        n = len(self._dimensions)
        angle_step = 2 * math.pi / n

        for level in range(1, 5):
            r = radius * level / 4
            path = QPainterPath()
            for i in range(n):
                angle = -math.pi / 2 + i * angle_step
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            path.closeSubpath()
            painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)

        for i in range(n):
            angle = -math.pi / 2 + i * angle_step
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1))
            painter.drawLine(int(cx), int(cy), int(x), int(y))

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            lx = cx + (radius + 16) * math.cos(angle)
            ly = cy + (radius + 16) * math.sin(angle)
            painter.drawText(QRectF(lx - 30, ly - 8, 60, 16), Qt.AlignCenter, self._dimensions[i])

        colors = self._chart_colors()
        for si, series in enumerate(self._series):
            data = series.get("data", [])
            if len(data) != n:
                continue
            color = QColor(colors[si % len(colors)])

            fill_path = QPainterPath()
            for i in range(n):
                val = data[i] * self._anim_progress
                r = radius * val / 100
                angle = -math.pi / 2 + i * angle_step
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                if i == 0:
                    fill_path.moveTo(x, y)
                else:
                    fill_path.lineTo(x, y)
            fill_path.closeSubpath()

            fill_color = QColor(color)
            fill_color.setAlpha(40)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(fill_color))
            painter.drawPath(fill_path)

            painter.setPen(QPen(color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(fill_path)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            for i in range(n):
                val = data[i] * self._anim_progress
                r = radius * val / 100
                angle = -math.pi / 2 + i * angle_step
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                painter.drawEllipse(QRectF(x - 3, y - 3, 6, 6))

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        lx = 10
        for si, series in enumerate(self._series):
            name = series.get("name", f"系列{si + 1}")
            color = QColor(colors[si % len(colors)])
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(lx, 4, 10, 10), 2, 2)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(lx + 14), 14, name)
            lx += painter.fontMetrics().horizontalAdvance(name) + 28

        painter.end()

    def apply_theme(self):
        self.update()
