from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSkeleton(QWidget, FluentWidgetBase):
    _opacity = 0.3

    def __init__(self, shape: str = "rect", width: int = 200, height: int = 20, parent=None):
        super().__init__(parent)
        self._shape = shape
        self.setFixedSize(width, height)

        self._init_fluent_base()
        self._pulse_anim = QPropertyAnimation(self, b"pulse_opacity")
        self._pulse_anim.setDuration(800)
        self._pulse_anim.setStartValue(0.3)
        self._pulse_anim.setEndValue(0.8)
        self._pulse_anim.setEasingCurve(QEasingCurve.InOutSine)
        self._pulse_anim.setLoopCount(-1)
        self._pulse_anim.start()

    @Property(float)
    def pulse_opacity(self):
        return self._opacity

    @pulse_opacity.setter
    def pulse_opacity(self, value):
        self._opacity = value
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        if self._pulse_anim.state() != QPropertyAnimation.Running:
            self._pulse_anim.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self._pulse_anim.pause()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        base_color = QColor(tm.color("bg_solid_tertiary"))
        base_color.setAlphaF(self._opacity)

        painter.setPen(Qt.NoPen)
        painter.setBrush(base_color)

        if self._shape == "circle":
            radius = min(self.width(), self.height()) / 2
            painter.drawEllipse(QRectF(0, 0, self.width(), self.height()))
        elif self._shape == "text":
            line_height = 10
            spacing = 6
            y = 4
            while y + line_height <= self.height() - 4:
                is_last = (y + line_height + spacing + line_height) > (self.height() - 4)
                w = self.width() * 0.7 if is_last else self.width() - 8
                rect = QRectF(4, y, w, line_height)
                painter.drawRoundedRect(rect, 4, 4)
                y += line_height + spacing
        else:
            painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), tm.radius("sm"), tm.radius("sm"))

        painter.end()

    def apply_theme(self):
        self.setStyleSheet("background: transparent;")
        self.update()
