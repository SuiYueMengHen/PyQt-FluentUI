from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentProgressRing(QWidget, FluentWidgetBase):
    _angle = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._value = 0
        self._maximum = 100
        self._indeterminate = False
        self.setFixedSize(48, 48)

        self._spin_anim = QPropertyAnimation(self, b"angle")
        self._spin_anim.setDuration(1500)
        self._spin_anim.setStartValue(0.0)
        self._spin_anim.setEndValue(360.0)
        self._spin_anim.setLoopCount(-1)
        self._spin_anim.setEasingCurve(QEasingCurve.Linear)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = max(0, min(val, self._maximum))
        self.update()

    @property
    def indeterminate(self):
        return self._indeterminate

    @indeterminate.setter
    def indeterminate(self, val):
        self._indeterminate = val
        if val:
            self._spin_anim.start()
        else:
            self._spin_anim.stop()
        self.update()

    @Property(float)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        margin = 4
        size = min(self.width(), self.height()) - margin * 2
        rect = QRectF(margin, margin, size, size)

        pen_width = 3
        track_pen = QPen(QColor(tm.color('bg_solid_tertiary')), pen_width, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(track_pen)
        painter.drawArc(rect, 0, 360 * 16)

        progress_pen = QPen(QColor(tm.color('primary')), pen_width, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(progress_pen)

        if self._indeterminate:
            start_angle = -self._angle * 16
            span_angle = 90 * 16
            painter.drawArc(rect, int(start_angle), int(span_angle))
        else:
            progress = self._value / max(1, self._maximum)
            span_angle = int(360 * progress * 16)
            painter.drawArc(rect, 90 * 16, -span_angle)

        painter.end()

    def apply_theme(self):
        self.setStyleSheet("background: transparent;")
        self.update()

    @staticmethod
    def self_check():
        from app.theme.theme_manager import ThemeManager
        tm = ThemeManager()
        errors = []
        for token in ["primary", "bg_solid_tertiary", "fg_secondary"]:
            try:
                tm.color(token)
            except Exception as e:
                errors.append(f"颜色token {token} 获取失败: {e}")
        if errors:
            return (False, "FluentProgressRing: " + "; ".join(errors))
        return (True, "FluentProgressRing: 所有检查项通过")
