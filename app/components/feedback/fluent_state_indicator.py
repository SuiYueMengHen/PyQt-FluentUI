from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentStateIndicator(QWidget, FluentWidgetBase):
    _pulse = 0.0

    def __init__(self, state: str = "online", size: int = 10, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._state = state
        self._size = size
        self.setFixedSize(size + 8, size + 8)

        self._pulse_anim = QPropertyAnimation(self, b"pulse")
        self._pulse_anim.setDuration(1500)
        self._pulse_anim.setStartValue(0.0)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setEasingCurve(QEasingCurve.InOutSine)
        self._pulse_anim.setLoopCount(-1)
        self._pulse_anim.start()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.update()

    @Property(float)
    def pulse(self):
        return self._pulse

    @pulse.setter
    def pulse(self, v):
        self._pulse = v
        self.update()

    def _state_color(self):
        tm = self._tm
        colors = {
            "online": tm.color("accent_success"),
            "offline": tm.color("fg_tertiary"),
            "busy": tm.color("accent_error"),
            "away": tm.color("accent_warning"),
            "dnd": tm.color("accent_error"),
        }
        return QColor(colors.get(self._state, colors["offline"]))

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        cx = self.width() / 2
        cy = self.height() / 2
        color = self._state_color()

        if self._state in ("online", "busy", "dnd"):
            pulse_alpha = int(40 * (1 - self._pulse))
            pulse_color = QColor(color)
            pulse_color.setAlpha(pulse_alpha)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(pulse_color))
            pulse_r = self._size / 2 + 2 + self._pulse * 3
            painter.drawEllipse(QRectF(cx - pulse_r, cy - pulse_r, pulse_r * 2, pulse_r * 2))

        painter.setPen(QPen(QColor(tm.color("bg_solid_base")), 2))
        painter.setBrush(QBrush(color))
        r = self._size / 2
        painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))

        if self._state == "busy" or self._state == "dnd":
            painter.setPen(QPen(QColor("#FFFFFF"), 1.5))
            painter.drawLine(int(cx - 3), int(cy), int(cx + 3), int(cy))
        elif self._state == "away":
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#FFFFFF"))
            painter.drawEllipse(QRectF(cx - 2, cy - 2, 4, 4))

        painter.end()

    def apply_theme(self):
        self.update()
