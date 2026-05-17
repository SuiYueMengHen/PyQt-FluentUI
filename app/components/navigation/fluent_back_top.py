from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentBackTop(QWidget, FluentWidgetBase):
    clicked = Signal()
    _visible_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setFixedSize(40, 40)
        self.setCursor(Qt.PointingHandCursor)
        self._is_visible = False
        self.hide()

        self._vis_anim = QPropertyAnimation(self, b"visible_progress")
        self._vis_anim.setDuration(200)
        self._vis_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def visible_progress(self):
        return self._visible_progress

    @visible_progress.setter
    def visible_progress(self, v):
        self._visible_progress = v
        self.update()

    def set_visible(self, visible: bool):
        if visible == self._is_visible:
            return
        self._is_visible = visible
        self._vis_anim.stop()
        self._vis_anim.setStartValue(self._visible_progress)
        self._vis_anim.setEndValue(1.0 if visible else 0.0)
        self._vis_anim.start()
        if visible:
            self.show()
        else:
            self._vis_anim.finished.connect(self.hide)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        alpha = int(255 * self._visible_progress)

        bg = QColor(tm.color("bg_solid_card"))
        bg.setAlpha(alpha)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(QRectF(0, 0, 40, 40), 20, 20)

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(0, 0, 40, 40), 20, 20)

        icon = get_icon("arrow_up", tm.color("fg_secondary"), 18)
        painter.setOpacity(self._visible_progress)
        painter.drawPixmap(11, 11, icon.pixmap(18, 18))
        painter.setOpacity(1.0)

        painter.end()

    def apply_theme(self):
        self.update()
