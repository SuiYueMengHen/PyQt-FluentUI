from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentList(QWidget, FluentWidgetBase):
    itemClicked = Signal(int)
    _stagger = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._items: list[str] = []
        self._row_height = 36
        self._hovered_index = -1
        self.setMinimumSize(200, 100)
        self.setCursor(Qt.PointingHandCursor)

        self._stagger_anim = QPropertyAnimation(self, b"stagger")
        self._stagger_anim.setDuration(600)
        self._stagger_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._stagger_anim.setStartValue(0.0)
        self._stagger_anim.setEndValue(1.0)

    def set_data(self, items: list[str]):
        self._items = items
        self.setFixedHeight(len(items) * self._row_height + 8)
        self._stagger_anim.stop()
        self._stagger_anim.setStartValue(0.0)
        self._stagger_anim.setEndValue(1.0)
        self._stagger_anim.start()
        self.update()

    @Property(float)
    def stagger(self):
        return self._stagger

    @stagger.setter
    def stagger(self, v):
        self._stagger = v
        self.update()

    def mouseMoveEvent(self, event):
        idx = int(event.position().y() / self._row_height)
        self._hovered_index = idx if 0 <= idx < len(self._items) else -1
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_index = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        idx = int(event.position().y() / self._row_height)
        if 0 <= idx < len(self._items):
            self.itemClicked.emit(idx)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        for i, text in enumerate(self._items):
            y = i * self._row_height + 4
            is_hovered = i == self._hovered_index

            item_progress = max(0, min(1, self._stagger * len(self._items) - i))
            if item_progress <= 0:
                continue

            if is_hovered:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(tm.color("primary_light")))
                painter.drawRoundedRect(QRectF(4, y, self.width() - 8, self._row_height - 4), 4, 4)

            painter.setPen(QColor(tm.color("primary") if is_hovered else tm.color("fg_primary")))
            alpha = int(255 * item_progress)
            painter.setPen(QColor(tm.color("primary") if is_hovered else tm.color("fg_primary")))

            painter.drawText(QRectF(16, y, self.width() - 32, self._row_height - 4), Qt.AlignVCenter | Qt.AlignLeft, text)

            if i < len(self._items) - 1:
                painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
                painter.drawLine(16, int(y + self._row_height - 4), self.width() - 16, int(y + self._row_height - 4))

        painter.end()

    def apply_theme(self):
        self.update()
