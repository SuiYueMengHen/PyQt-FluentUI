import math

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSpinner(QWidget, FluentWidgetBase):
    _angle = 0.0

    def __init__(self, size: int = 32, style: str = "ring", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._style = style
        self.setFixedSize(size, size)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def _tick(self):
        self._angle = (self._angle + 8) % 360
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        if not self._timer.isActive():
            self._timer.start(30)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        cx, cy = self.width() / 2, self.height() / 2
        r = min(self.width(), self.height()) / 2 - 3

        if self._style == "ring":
            track_pen = QPen(QColor(tm.color("bg_solid_tertiary")), 3, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(track_pen)
            painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))

            progress_pen = QPen(QColor(tm.color("primary")), 3, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(progress_pen)
            painter.drawArc(QRectF(cx - r, cy - r, r * 2, r * 2), int(self._angle * 16), int(-270 * 16))

        elif self._style == "dots":
            for i in range(8):
                angle = math.radians(self._angle + i * 45)
                dx = cx + r * 0.7 * math.cos(angle)
                dy = cy + r * 0.7 * math.sin(angle)
                alpha = int(255 * (1 - i / 8))
                color = QColor(tm.color("primary"))
                color.setAlpha(alpha)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                dot_r = 2 + (1 - i / 8) * 1.5
                painter.drawEllipse(QRectF(dx - dot_r, dy - dot_r, dot_r * 2, dot_r * 2))

        elif self._style == "pulse":
            t = (self._angle % 360) / 360
            scale = 0.6 + 0.4 * abs(math.sin(t * math.pi * 2))
            alpha = int(100 + 155 * abs(math.sin(t * math.pi * 2)))
            color = QColor(tm.color("primary"))
            color.setAlpha(alpha)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            sr = r * scale
            painter.drawEllipse(QRectF(cx - sr, cy - sr, sr * 2, sr * 2))

        painter.end()

    def apply_theme(self):
        self.update()
