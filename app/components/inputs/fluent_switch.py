from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSwitch(QWidget, FluentWidgetBase):
    checkedChanged = Signal(bool)
    _thumb_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._checked = False
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(44, 24)
        self._thumb_anim = QPropertyAnimation(self, b"thumb_progress")
        self._thumb_anim.setDuration(200)
        self._thumb_anim.setEasingCurve(QEasingCurve.OutCubic)

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        if self._checked != value:
            self._checked = value
            self._thumb_anim.stop()
            self._thumb_anim.setStartValue(self._thumb_progress)
            self._thumb_anim.setEndValue(1.0 if value else 0.0)
            self._thumb_anim.start()
            self.checkedChanged.emit(value)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        self.checked = checked

    def mousePressEvent(self, event):
        self.checked = not self._checked
        super().mousePressEvent(event)

    @Property(float)
    def thumb_progress(self):
        return self._thumb_progress

    @thumb_progress.setter
    def thumb_progress(self, value):
        self._thumb_progress = value
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        track_rect = QRectF(0, 0, 44, 24)

        if self._checked:
            track_color = QColor(tm.color('primary'))
        else:
            track_color = QColor(tm.color('stroke_card'))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(track_rect, 12, 12)

        thumb_margin = 3
        thumb_size = 18
        min_x = thumb_margin
        max_x = 44 - thumb_margin - thumb_size
        thumb_x = min_x + (max_x - min_x) * self._thumb_progress
        thumb_y = (24 - thumb_size) / 2

        thumb_color = QColor(tm.color('bg_solid_card'))
        painter.setBrush(QBrush(thumb_color))
        painter.drawEllipse(QRectF(thumb_x, thumb_y, thumb_size, thumb_size))

        painter.end()

    def apply_theme(self):
        self.setStyleSheet("background: transparent;")
        self.update()
