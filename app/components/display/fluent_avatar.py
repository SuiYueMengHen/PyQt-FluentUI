from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentAvatar(QLabel, FluentWidgetBase):
    def __init__(self, text: str = "", size: int = 40, parent=None):
        super().__init__(text, parent)
        self._init_fluent_base()
        self._avatar_text = text
        self._avatar_size = size
        self._online = False
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)

    @property
    def online(self):
        return self._online

    @online.setter
    def online(self, value):
        self._online = value
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(0, 0, self._avatar_size, self._avatar_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color('primary_light')))
        painter.drawEllipse(rect)

        if self._avatar_text:
            painter.setPen(QColor(tm.color('primary')))
            font = painter.font()
            font.setPixelSize(int(self._avatar_size * 0.4))
            font.setWeight(QFont.Bold)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, self._avatar_text[0].upper())

        if self._online:
            dot_size = 10
            dot_x = self._avatar_size - dot_size
            dot_y = self._avatar_size - dot_size
            painter.setBrush(QColor(tm.color('accent_success')))
            painter.setPen(QPen(QColor(tm.color('bg_solid_card')), 2))
            painter.drawEllipse(QRectF(dot_x, dot_y, dot_size, dot_size))

        painter.end()

    def apply_theme(self):
        self.setStyleSheet("background: transparent;")
        self.update()
