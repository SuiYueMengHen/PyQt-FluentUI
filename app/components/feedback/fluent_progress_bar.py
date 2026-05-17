from PySide6.QtWidgets import QWidget, QProgressBar
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentProgressBar(QWidget, FluentWidgetBase):
    _indeterminate_pos = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._value = 0
        self._maximum = 100
        self._indeterminate = False
        self.setFixedHeight(4)

        self._indeterminate_anim = QPropertyAnimation(self, b"indeterminate_pos")
        self._indeterminate_anim.setDuration(1500)
        self._indeterminate_anim.setStartValue(0.0)
        self._indeterminate_anim.setEndValue(1.0)
        self._indeterminate_anim.setLoopCount(-1)
        self._indeterminate_anim.setEasingCurve(QEasingCurve.InOutCubic)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = max(0, min(val, self._maximum))
        self.update()

    @property
    def maximum(self):
        return self._maximum

    @maximum.setter
    def maximum(self, val):
        self._maximum = val
        self.update()

    @property
    def indeterminate(self):
        return self._indeterminate

    @indeterminate.setter
    def indeterminate(self, val):
        self._indeterminate = val
        if val:
            self._indeterminate_anim.start()
        else:
            self._indeterminate_anim.stop()
        self.update()

    @Property(float)
    def indeterminate_pos(self):
        return self._indeterminate_pos

    @indeterminate_pos.setter
    def indeterminate_pos(self, value):
        self._indeterminate_pos = value
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        track_rect = QRectF(0, 0, self.width(), self.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color('bg_solid_tertiary')))
        painter.drawRoundedRect(track_rect, 2, 2)

        if self._indeterminate:
            bar_width = self.width() * 0.3
            start = (self.width() - bar_width) * self._indeterminate_pos
            bar_rect = QRectF(start, 0, bar_width, self.height())
            painter.setBrush(QColor(tm.color('primary')))
            painter.drawRoundedRect(bar_rect, 2, 2)
        else:
            progress = self._value / max(1, self._maximum)
            bar_width = self.width() * progress
            bar_rect = QRectF(0, 0, bar_width, self.height())
            painter.setBrush(QColor(tm.color('primary')))
            painter.drawRoundedRect(bar_rect, 2, 2)

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
            return (False, "FluentProgressBar: " + "; ".join(errors))
        return (True, "FluentProgressBar: 所有检查项通过")
