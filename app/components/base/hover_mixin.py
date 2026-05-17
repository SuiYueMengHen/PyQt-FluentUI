from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor


class HoverMixin:
    _hover_progress = 0.0

    def init_hover_animation(self, duration=150):
        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(duration)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._hover_progress = 0.0

    def enterEvent(self, event):
        if hasattr(self, "_hover_anim"):
            self._hover_anim.stop()
            self._hover_anim.setStartValue(self._hover_progress)
            self._hover_anim.setEndValue(1.0)
            self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if hasattr(self, "_hover_anim"):
            self._hover_anim.stop()
            self._hover_anim.setStartValue(self._hover_progress)
            self._hover_anim.setEndValue(0.0)
            self._hover_anim.start()
        super().leaveEvent(event)

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, value):
        self._hover_progress = value
        self.update()

    def lerp_color(self, c1: str, c2: str, t: float) -> QColor:
        color1 = QColor(c1)
        color2 = QColor(c2)
        r = int(color1.red() + (color2.red() - color1.red()) * t)
        g = int(color1.green() + (color2.green() - color1.green()) * t)
        b = int(color1.blue() + (color2.blue() - color1.blue()) * t)
        a = int(color1.alpha() + (color2.alpha() - color1.alpha()) * t)
        return QColor(r, g, b, a)
