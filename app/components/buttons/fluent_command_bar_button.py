from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentCommandBarButton(QWidget, FluentWidgetBase):
    clicked = Signal()
    _hover_progress = 0.0

    def __init__(self, text: str = "", icon_name: str = "", description: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._text = text
        self._icon_name = icon_name
        self._description = description
        self.setFixedHeight(48)
        self.setMinimumWidth(60)
        self.setCursor(Qt.PointingHandCursor)

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, v):
        self._hover_progress = v
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
            self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        bg_alpha = int(10 + 30 * self._hover_progress)
        bg = QColor(tm.color("fg_primary"))
        bg.setAlpha(bg_alpha)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 4, 4)

        x = 8
        if self._icon_name:
            icon = get_icon(self._icon_name, tm.color("primary") if self._hover_progress > 0.5 else tm.color("fg_secondary"), 20)
            painter.drawPixmap(x, int((self.height() - 20) / 2), icon.pixmap(20, 20))
            x += 26

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        if self._description:
            painter.drawText(QRectF(x, 6, self.width() - x - 8, 18), Qt.AlignLeft | Qt.AlignTop, self._text)
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(QRectF(x, 24, self.width() - x - 8, 16), Qt.AlignLeft | Qt.AlignTop, self._description)
        else:
            painter.drawText(QRectF(x, 0, self.width() - x - 8, self.height()), Qt.AlignVCenter | Qt.AlignLeft, self._text)

        painter.end()

    def apply_theme(self):
        self.update()
