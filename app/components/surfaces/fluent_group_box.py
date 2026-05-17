from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentGroupBox(QWidget, FluentWidgetBase):
    def __init__(self, title: str = "分组", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._title = title
        self._padding_top = 28
        self.setMinimumSize(200, 80)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, self._padding_top / 2, self.width(), self.height() - self._padding_top / 2), 6, 6)

        title_bg = QColor(tm.color("bg_solid_base"))
        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        tw = painter.fontMetrics().horizontalAdvance(self._title) + 16

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(title_bg))
        painter.drawRect(QRectF(12, 0, tw, self._padding_top))

        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(20, 2, tw - 16, self._padding_top - 4), Qt.AlignVCenter | Qt.AlignLeft, self._title)

        painter.end()

    def apply_theme(self):
        self.update()
