from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentToggleGroup(QWidget, FluentWidgetBase):
    selectionChanged = Signal(int)
    _indicator_x = 0.0

    def __init__(self, items: list = None, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._items = items or []
        self._current_index = 0
        self._hovered_index = -1
        self._item_width = 80
        self._height = 36
        self.setFixedHeight(self._height)
        self.setMinimumWidth(len(self._items) * self._item_width + 8)

        self._indicator_anim = QPropertyAnimation(self, b"indicator_x")
        self._indicator_anim.setDuration(250)
        self._indicator_anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_current(self, index: int):
        if index < 0 or index >= len(self._items) or index == self._current_index:
            return
        self._current_index = index
        target_x = 4 + index * self._item_width
        self._indicator_anim.stop()
        self._indicator_anim.setStartValue(self._indicator_x)
        self._indicator_anim.setEndValue(float(target_x))
        self._indicator_anim.start()
        self.selectionChanged.emit(index)

    @property
    def current_index(self):
        return self._current_index

    @Property(float)
    def indicator_x(self):
        return self._indicator_x

    @indicator_x.setter
    def indicator_x(self, value):
        self._indicator_x = value
        self.update()

    def _index_at(self, pos) -> int:
        x = pos.x() - 4
        idx = int(x / self._item_width)
        if 0 <= idx < len(self._items):
            return idx
        return -1

    def mouseMoveEvent(self, event):
        idx = self._index_at(event.position())
        if idx != self._hovered_index:
            self._hovered_index = idx
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        idx = self._index_at(event.position())
        if idx >= 0:
            self.set_current(idx)
        super().mousePressEvent(event)

    def leaveEvent(self, event):
        self._hovered_index = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        bg_rect = QRectF(0, 0, self.width(), self.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
        painter.drawRoundedRect(bg_rect, self._height / 2, self._height / 2)

        indicator_rect = QRectF(self._indicator_x, 2, self._item_width, self._height - 4)
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(indicator_rect, (self._height - 4) / 2, (self._height - 4) / 2)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        for i, item in enumerate(self._items):
            text = item.get("text", "") if isinstance(item, dict) else str(item)
            icon_name = item.get("icon", "") if isinstance(item, dict) else ""
            x = 4 + i * self._item_width

            if i == self._current_index:
                painter.setPen(QColor(tm.color("primary")))
                font.setWeight(QFont.DemiBold)
            elif i == self._hovered_index:
                painter.setPen(QColor(tm.color("fg_primary")))
                font.setWeight(QFont.Normal)
            else:
                painter.setPen(QColor(tm.color("fg_secondary")))
                font.setWeight(QFont.Normal)
            painter.setFont(font)

            text_rect = QRectF(x, 0, self._item_width, self.height())
            if icon_name:
                icon = get_icon(icon_name, painter.pen().color().name(), 16)
                painter.drawPixmap(int(x + (self._item_width - 16 - painter.fontMetrics().horizontalAdvance(text)) / 2 - 10),
                                   int((self.height() - 16) / 2), icon.pixmap(16, 16))
            painter.drawText(text_rect, Qt.AlignCenter, text)

        painter.end()

    def apply_theme(self):
        self._indicator_x = 4 + self._current_index * self._item_width
        self.update()
