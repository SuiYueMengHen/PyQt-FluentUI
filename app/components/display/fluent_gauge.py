import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentGauge(QWidget, FluentWidgetBase):
    valueChanged = Signal(float)
    _anim_value = 0.0

    def __init__(self, min_val: float = 0, max_val: float = 100,
                 label: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._min = min_val
        self._max = max_val
        self._value = 0.0
        self._label = label
        self._color_zones: list[dict] = []
        self.setFixedSize(160, 160)

        self._value_anim = QPropertyAnimation(self, b"anim_value")
        self._value_anim.setDuration(800)
        self._value_anim.setEasingCurve(QEasingCurve.OutCubic)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = max(self._min, min(val, self._max))
        self._value_anim.stop()
        self._value_anim.setStartValue(self._anim_value)
        self._value_anim.setEndValue(self._value)
        self._value_anim.start()
        self.valueChanged.emit(self._value)

    def set_color_zones(self, zones: list):
        self._color_zones = zones

    @Property(float)
    def anim_value(self):
        return self._anim_value

    @anim_value.setter
    def anim_value(self, value):
        self._anim_value = value
        self.update()

    def _get_zone_color(self, val: float) -> str:
        tm = self._tm
        if not self._color_zones:
            return tm.color("primary")
        for zone in self._color_zones:
            if zone.get("min", self._min) <= val <= zone.get("max", self._max):
                color_key = zone.get("color", "primary")
                color_map = {
                    "success": "accent_success",
                    "warning": "accent_warning",
                    "error": "accent_error",
                    "primary": "primary",
                }
                return tm.color(color_map.get(color_key, color_key))
        return tm.color("primary")

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        margin = 12
        size = min(self.width(), self.height()) - margin * 2
        rect = QRectF(margin, margin, size, size)
        pen_width = 8

        start_angle = 135
        span_total = 270

        track_pen = QPen(QColor(tm.color("bg_solid_tertiary")), pen_width, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(track_pen)
        painter.drawArc(rect, int(start_angle * 16), int(-span_total * 16))

        progress = (self._anim_value - self._min) / max(1, self._max - self._min)
        progress = max(0, min(1, progress))
        span_angle = span_total * progress

        value_color = QColor(self._get_zone_color(self._anim_value))
        progress_pen = QPen(value_color, pen_width, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(progress_pen)
        painter.drawArc(rect, int(start_angle * 16), int(-span_angle * 16))

        for i in range(0, span_total + 1, 30):
            angle_rad = math.radians(start_angle - i)
            inner_r = size / 2 - pen_width - 4
            outer_r = size / 2 - pen_width - 8
            cx = margin + size / 2
            cy = margin + size / 2
            x1 = cx + inner_r * math.cos(angle_rad)
            y1 = cy - inner_r * math.sin(angle_rad)
            x2 = cx + outer_r * math.cos(angle_rad)
            y2 = cy - outer_r * math.sin(angle_rad)
            tick_pen = QPen(QColor(tm.color("fg_tertiary")), 1)
            painter.setPen(tick_pen)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        cx = margin + size / 2
        cy = margin + size / 2

        font = QFont()
        font.setPixelSize(tm.font_size("display"))
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        if self._max - self._min >= 100:
            display_val = f"{int(self._anim_value)}"
        else:
            display_val = f"{self._anim_value:.1f}"

        painter.drawText(QRectF(margin, margin + size * 0.25, size, size * 0.35),
                         Qt.AlignCenter, display_val)

        if self._label:
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(margin, margin + size * 0.55, size, size * 0.25),
                             Qt.AlignCenter, self._label)

        painter.end()

    def apply_theme(self):
        self.update()
