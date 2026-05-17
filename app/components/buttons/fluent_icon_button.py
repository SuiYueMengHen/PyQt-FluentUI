from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentIconButton(QWidget, FluentWidgetBase):
    clicked = Signal()
    _hover_progress = 0.0
    _press_progress = 0.0

    def __init__(self, icon_name: str = "", circular: bool = True, size: int = 36, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._icon_name = icon_name
        self._circular = circular
        self._size = size
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._press_anim = QPropertyAnimation(self, b"press_progress")
        self._press_anim.setDuration(100)
        self._press_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, v):
        self._hover_progress = v
        self.update()

    @Property(float)
    def press_progress(self):
        return self._press_progress

    @press_progress.setter
    def press_progress(self, v):
        self._press_progress = v
        self.update()

    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._press_anim.stop()
            self._press_anim.setStartValue(0.0)
            self._press_anim.setEndValue(1.0)
            self._press_anim.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._press_anim.stop()
            self._press_anim.setStartValue(self._press_progress)
            self._press_anim.setEndValue(0.0)
            self._press_anim.start()
            if self.rect().contains(event.position().toPoint()):
                self.clicked.emit()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        s = self._size
        r = s / 2 if self._circular else 6

        bg_alpha = int(20 + 30 * self._hover_progress)
        bg_color = QColor(tm.color("fg_primary"))
        bg_color.setAlpha(bg_alpha)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(QRectF(0, 0, s, s), r, r)

        scale = 1.0 - 0.05 * self._press_progress
        painter.save()
        painter.translate(s / 2, s / 2)
        painter.scale(scale, scale)
        painter.translate(-s / 2, -s / 2)

        icon_color = tm.color("primary") if self._hover_progress > 0.5 else tm.color("fg_secondary")
        icon = get_icon(self._icon_name, icon_color, s - 12)
        painter.drawPixmap(int(6), int(6), icon.pixmap(s - 12, s - 12))
        painter.restore()

        painter.end()

    def apply_theme(self):
        self.update()
