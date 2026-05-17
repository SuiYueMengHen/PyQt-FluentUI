from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class PivotItem(QWidget):
    clicked = Signal(int)

    def __init__(self, text: str, index: int, parent=None):
        super().__init__(parent)
        self._text = text
        self._index = index
        self._active = False
        self._tm = ThemeManager()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(36)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)

        self._label = QLabel(text)
        layout.addWidget(self._label)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self._update_style()
        self.update()

    def _update_style(self):
        tm = self._tm
        color = tm.color('primary') if self._active else tm.color('fg_secondary')
        weight = '600' if self._active else '400'
        self._label.setStyleSheet(f"color: {color}; font-size: {tm.font_size('body')}px; font-weight: {weight}; background: transparent;")

    def mousePressEvent(self, event):
        self.clicked.emit(self._index)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        if self._active:
            tm = self._tm
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(tm.color('primary')))
            indicator = QRectF(8, self.height() - 2, self.width() - 16, 2)
            painter.drawRoundedRect(indicator, 1, 1)
            painter.end()

    def apply_theme(self):
        self._update_style()


class FluentPivot(QWidget, FluentWidgetBase):
    current_changed = Signal(int)

    def __init__(self, items: list[str] = None, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._current_index = 0
        self._items: list[PivotItem] = []

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addStretch()

        if items:
            for item in items:
                self.add_item(item)

    def add_item(self, text: str):
        index = len(self._items)
        item = PivotItem(text, index, self)
        item.clicked.connect(self._on_item_clicked)
        self._layout.insertWidget(self._layout.count() - 1, item)
        self._items.append(item)
        if index == 0:
            item.active = True

    def _on_item_clicked(self, index: int):
        if self._current_index != index:
            self._current_index = index
            for i, item in enumerate(self._items):
                item.active = (i == index)
            self.current_changed.emit(index)

    def apply_theme(self):
        self.setStyleSheet("background: transparent;")
        for item in self._items:
            item.apply_theme()
