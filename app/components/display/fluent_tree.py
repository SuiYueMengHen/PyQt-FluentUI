from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentTreeItem:
    def __init__(self, text: str, icon: str = "", children: list = None, expanded: bool = False):
        self.text = text
        self.icon = icon
        self.children = children or []
        self.expanded = expanded
        self.depth = 0
        self._expand_anim = 0.0


class FluentTree(QWidget, FluentWidgetBase):
    itemClicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._items: list[FluentTreeItem] = []
        self._hovered_item = None
        self._row_height = 28
        self.setMinimumSize(200, 100)
        self.setCursor(Qt.PointingHandCursor)

    def set_data(self, items: list[FluentTreeItem]):
        self._items = items
        self._update_depths(self._items, 0)
        self.setFixedHeight(max(self._count_visible() * self._row_height + 8, 60))
        self.update()

    def _update_depths(self, items, depth):
        for item in items:
            item.depth = depth
            self._update_depths(item.children, depth + 1)

    def _count_visible(self):
        count = 0
        for item in self._items:
            count += self._count_item(item)
        return count

    def _count_item(self, item):
        count = 1
        if item.expanded:
            for child in item.children:
                count += self._count_item(child)
        return count

    def _item_at_y(self, y) -> FluentTreeItem:
        row = int(y / self._row_height)
        flat = self._flatten(self._items)
        if 0 <= row < len(flat):
            return flat[row]
        return None

    def _flatten(self, items) -> list:
        result = []
        for item in items:
            result.append(item)
            if item.expanded:
                result.extend(self._flatten(item.children))
        return result

    def mouseMoveEvent(self, event):
        self._hovered_item = self._item_at_y(event.position().y())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_item = None
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        item = self._item_at_y(event.position().y())
        if item:
            if item.children:
                item.expanded = not item.expanded
                self.setFixedHeight(max(self._count_visible() * self._row_height + 8, 60))
            self.itemClicked.emit(item.text)
            self.update()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        flat = self._flatten(self._items)
        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        for i, item in enumerate(flat):
            y = i * self._row_height
            is_hovered = item == self._hovered_item

            if is_hovered:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(tm.color("primary_light")))
                painter.drawRoundedRect(QRectF(4, y + 2, self.width() - 8, self._row_height - 4), 4, 4)

            indent = 16 + item.depth * 20

            if item.children:
                arrow = "▼" if item.expanded else "▶"
                painter.setPen(QColor(tm.color("fg_tertiary")))
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.drawText(QRectF(indent - 14, y, 14, self._row_height), Qt.AlignCenter, arrow)
                font.setPixelSize(tm.font_size("body"))
                painter.setFont(font)

            if item.icon:
                icon = get_icon(item.icon, tm.color("fg_secondary"), 16)
                painter.drawPixmap(int(indent), int(y + (self._row_height - 16) / 2), icon.pixmap(16, 16))
                indent += 20

            painter.setPen(QColor(tm.color("primary") if is_hovered else tm.color("fg_primary")))
            painter.drawText(QRectF(indent, y, self.width() - indent - 8, self._row_height), Qt.AlignVCenter | Qt.AlignLeft, item.text)

        painter.end()

    def apply_theme(self):
        self.update()
