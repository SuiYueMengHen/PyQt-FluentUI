from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentAnchor(QWidget, FluentWidgetBase):
    anchor_clicked = Signal(str)
    _indicator_y = 0.0

    def __init__(self, items: list[dict] = None, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._items = items or []
        self._active = ""
        self._hovered = ""
        self.setFixedWidth(120)
        self.setMinimumHeight(100)

        self._indicator_anim = QPropertyAnimation(self, b"indicator_y")
        self._indicator_anim.setDuration(200)
        self._indicator_anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_items(self, items: list[dict]):
        self._items = items
        if items:
            self._active = items[0].get("key", "")
        self.setFixedHeight(max(len(items) * 32 + 16, 60))
        self.update()

    @Property(float)
    def indicator_y(self):
        return self._indicator_y

    @indicator_y.setter
    def indicator_y(self, v):
        self._indicator_y = v
        self.update()

    def set_active(self, key: str):
        self._active = key
        idx = next((i for i, item in enumerate(self._items) if item.get("key") == key), 0)
        target_y = 8 + idx * 32
        self._indicator_anim.stop()
        self._indicator_anim.setStartValue(self._indicator_y)
        self._indicator_anim.setEndValue(float(target_y))
        self._indicator_anim.start()

    def mouseMoveEvent(self, event):
        idx = int((event.position().y() - 8) / 32)
        if 0 <= idx < len(self._items):
            self._hovered = self._items[idx].get("key", "")
        else:
            self._hovered = ""
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = ""
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            idx = int((event.position().y() - 8) / 32)
            if 0 <= idx < len(self._items):
                key = self._items[idx].get("key", "")
                self.set_active(key)
                self.anchor_clicked.emit(key)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("primary")))
        painter.drawRoundedRect(QRectF(0, self._indicator_y, 3, 24), 1.5, 1.5)

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)

        for i, item in enumerate(self._items):
            y = 8 + i * 32
            key = item.get("key", "")
            text = item.get("text", "")
            is_active = key == self._active
            is_hovered = key == self._hovered

            if is_hovered and not is_active:
                painter.setPen(Qt.NoPen)
                hover_bg = QColor(tm.color("nav_item_hover"))
                painter.setBrush(QBrush(hover_bg))
                painter.drawRoundedRect(QRectF(8, y, self.width() - 16, 28), 4, 4)

            color = QColor(tm.color("primary")) if is_active else QColor(tm.color("fg_secondary")) if is_hovered else QColor(tm.color("fg_tertiary"))
            painter.setPen(color)
            painter.drawText(QRectF(12, y, self.width() - 20, 28), Qt.AlignVCenter | Qt.AlignLeft, text)

        painter.end()

    def apply_theme(self):
        self.update()
