import math

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QConicalGradient

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class GaugeSegment:
    def __init__(self, from_val: float, to_val: float, color_key: str, label: str = ""):
        self.from_val = from_val
        self.to_val = to_val
        self.color_key = color_key
        self.label = label


class FluentGauge(QWidget, FluentWidgetBase):
    _anim_progress = 0.0
    value_changed = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(200)
        self.setMinimumWidth(200)

        self._value = 0.0
        self._max_value = 100.0
        self._label = ""
        self._unit = ""
        self._segments: list[GaugeSegment] = []
        self._start_angle = 225
        self._span_angle = 270
        self._thickness = 16

        self._anim = None
        self._hovered = False
        self.setMouseTracking(True)
        QTimer.singleShot(50, self._start_anim)

    def _start_anim(self):
        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(800)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
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

    def set_value(self, value: float, animate: bool = True):
        old = self._value
        self._value = min(value, self._max_value)
        if animate and old != self._value:
            self._anim = QPropertyAnimation(self, b"anim_progress")
            self._anim.setDuration(600)
            self._anim.setEasingCurve(QEasingCurve.OutCubic)
            self._anim.setStartValue(old / self._max_value)
            self._anim.setEndValue(self._value / self._max_value)
            self._anim.start()
        else:
            self._anim_progress = self._value / self._max_value
            self.update()
        self.value_changed.emit(self._value)

    def set_max_value(self, max_value: float):
        self._max_value = max_value
        self.update()

    def set_label(self, label: str):
        self._label = label
        self.update()

    def set_unit(self, unit: str):
        self._unit = unit
        self.update()

    def add_segment(self, from_val: float, to_val: float, color_key: str, label: str = ""):
        self._segments.append(GaugeSegment(from_val, to_val, color_key, label))
        self.update()

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        w = self.width()
        h = self.height()
        size = min(w, h)
        cx = w / 2
        cy = h / 2
        radius = size / 2 - self._thickness - 10

        bg_rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
        bg_pen = QPen(QColor(tm.color("stroke_card")), self._thickness, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(bg_rect, int(self._start_angle * 16), int(-self._span_angle * 16))

        if self._segments:
            for seg in self._segments:
                seg_start = self._start_angle - (seg.from_val / self._max_value) * self._span_angle
                seg_span = -((seg.to_val - seg.from_val) / self._max_value) * self._span_angle
                seg_color = QColor(tm.color(seg.color_key))
                seg_color.setAlpha(60)
                seg_pen = QPen(seg_color, self._thickness, Qt.SolidLine, Qt.RoundCap)
                painter.setPen(seg_pen)
                painter.drawArc(bg_rect, int(seg_start * 16), int(seg_span * 16))

        progress = self._anim_progress
        value_angle = -progress * self._span_angle

        if self._segments:
            active_seg = None
            for seg in self._segments:
                if seg.from_val <= self._value <= seg.to_val:
                    active_seg = seg
                    break
            if active_seg:
                value_color = QColor(tm.color(active_seg.color_key))
            else:
                value_color = QColor(tm.color("primary"))
        else:
            value_color = QColor(tm.color("primary"))

        if self._hovered:
            value_color = value_color.lighter(115)

        value_pen = QPen(value_color, self._thickness, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(value_pen)
        painter.drawArc(bg_rect, int(self._start_angle * 16), int(value_angle * 16))

        end_angle_rad = math.radians(self._start_angle + value_angle)
        dot_x = cx + radius * math.cos(end_angle_rad)
        dot_y = cy - radius * math.sin(end_angle_rad)
        dot_r = self._thickness / 2 + 2
        painter.setPen(Qt.NoPen)
        painter.setBrush(value_color)
        painter.drawEllipse(QRectF(dot_x - dot_r, dot_y - dot_r, dot_r * 2, dot_r * 2))

        inner_r = radius - self._thickness / 2 - 8
        glow = QColor(value_color)
        glow.setAlpha(15)
        painter.setBrush(glow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(cx - inner_r, cy - inner_r, inner_r * 2, inner_r * 2))

        font = QFont()
        font.setPixelSize(int(size * 0.18))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        display_val = f"{self._value:.0f}" if self._value == int(self._value) else f"{self._value:.1f}"
        value_rect = QRectF(cx - radius, cy - size * 0.08, radius * 2, size * 0.2)
        painter.drawText(value_rect, Qt.AlignCenter, display_val)

        if self._unit:
            font.setPixelSize(int(size * 0.08))
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            unit_rect = QRectF(cx - radius, cy + size * 0.08, radius * 2, size * 0.1)
            painter.drawText(unit_rect, Qt.AlignCenter, self._unit)

        if self._label:
            font.setPixelSize(int(size * 0.07))
            font.setWeight(QFont.Medium)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            label_rect = QRectF(cx - radius, cy - size * 0.25, radius * 2, size * 0.1)
            painter.drawText(label_rect, Qt.AlignCenter, self._label)

        if self._hovered:
            text = f"{self._label}: {display_val}{self._unit}" if self._label else f"{display_val}{self._unit}"
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(text) + 16
            th = 24
            tx = cx - tw / 2
            ty = 4

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(tm.color("bg_solid_card")))
            painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
            painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
            painter.setPen(QColor(tm.color("fg_primary")))
            painter.drawText(QRectF(tx, ty, tw, th), Qt.AlignCenter, text)

        painter.end()

    def apply_theme(self):
        self.update()
