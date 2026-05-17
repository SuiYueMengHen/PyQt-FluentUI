from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentRangeSlider(QWidget, FluentWidgetBase):
    range_changed = Signal(float, float)
    _dragging = None

    def __init__(self, min_val: float = 0, max_val: float = 100, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._min = min_val
        self._max = max_val
        self._low = min_val + (max_val - min_val) * 0.2
        self._high = min_val + (max_val - min_val) * 0.8
        self.setFixedHeight(28)
        self.setMinimumWidth(200)
        self.setCursor(Qt.PointingHandCursor)

    def set_range(self, min_val: float, max_val: float):
        self._min = min_val
        self._max = max_val
        self.update()

    def set_values(self, low: float, high: float):
        self._low = max(self._min, min(self._max, low))
        self._high = max(self._low, min(self._max, high))
        self.update()

    @property
    def low(self):
        return self._low

    @property
    def high(self):
        return self._high

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = self._handle_at(event.position().x())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            x = event.position().x()
            margin = 12
            track_w = self.width() - 2 * margin
            val = self._min + ((x - margin) / track_w) * (self._max - self._min)
            val = max(self._min, min(self._max, val))
            if self._dragging == "low":
                self._low = min(val, self._high)
            else:
                self._high = max(val, self._low)
            self.range_changed.emit(self._low, self._high)
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = None
        super().mouseReleaseEvent(event)

    def _handle_at(self, x):
        margin = 12
        track_w = self.width() - 2 * margin
        low_x = margin + ((self._low - self._min) / (self._max - self._min)) * track_w
        high_x = margin + ((self._high - self._min) / (self._max - self._min)) * track_w
        if abs(x - low_x) < 10:
            return "low"
        elif abs(x - high_x) < 10:
            return "high"
        return "low" if x < (low_x + high_x) / 2 else "high"

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        margin = 12
        cy = self.height() / 2
        track_w = self.width() - 2 * margin
        track_h = 4

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
        painter.drawRoundedRect(QRectF(margin, cy - track_h / 2, track_w, track_h), 2, 2)

        low_x = margin + ((self._low - self._min) / (self._max - self._min)) * track_w
        high_x = margin + ((self._high - self._min) / (self._max - self._min)) * track_w

        painter.setBrush(QColor(tm.color("primary")))
        painter.drawRoundedRect(QRectF(low_x, cy - track_h / 2, high_x - low_x, track_h), 2, 2)

        for hx in [low_x, high_x]:
            painter.setPen(QPen(QColor(tm.color("primary")), 2))
            painter.setBrush(QColor(tm.color("bg_solid_card")))
            painter.drawEllipse(QRectF(hx - 7, cy - 7, 14, 14))

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(QRectF(low_x - 20, cy + 10, 40, 16), Qt.AlignCenter, f"{self._low:.0f}")
        painter.drawText(QRectF(high_x - 20, cy + 10, 40, 16), Qt.AlignCenter, f"{self._high:.0f}")

        painter.end()

    def apply_theme(self):
        self.update()
