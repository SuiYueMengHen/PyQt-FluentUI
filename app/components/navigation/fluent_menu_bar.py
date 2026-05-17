from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QMenu
from PySide6.QtCore import Qt, Signal, QRectF, QPoint
from PySide6.QtGui import QPainter, QColor, QAction

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class _MenuBarItem(QWidget):
    clicked = Signal(object)

    def __init__(self, text: str, menu: QMenu = None, parent=None):
        super().__init__(parent)
        self._text = text
        self._menu = menu
        self._hovered = False
        self._tm = ThemeManager()
        self.setFixedHeight(32)
        self.setMinimumWidth(48)
        self.setCursor(Qt.PointingHandCursor)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(6)

        self._label = QLabel(text)
        layout.addWidget(self._label)

    @property
    def menu(self):
        return self._menu

    def set_menu(self, menu: QMenu):
        self._menu = menu

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._menu:
            pos = self.mapToGlobal(QPoint(0, self.height()))
            self._menu.exec(pos)
        self.clicked.emit(self)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if self._hovered:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
            painter.drawRoundedRect(QRectF(0, 2, self.width(), self.height() - 4), tm.radius("sm"), tm.radius("sm"))

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self._label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('body')}px; background: transparent;")
        self.update()


class FluentMenuBar(QWidget, FluentWidgetBase):
    menuTriggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self._items: list[_MenuBarItem] = []
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(8, 2, 8, 2)
        self._layout.setSpacing(2)
        self._layout.addStretch()

        self._init_fluent_base()

    def add_menu(self, title: str, items: list[dict] = None) -> _MenuBarItem:
        menu = QMenu(self)
        menu_items = items or []

        for item_data in menu_items:
            if item_data.get("separator"):
                menu.addSeparator()
                continue

            action = QAction(item_data.get("text", ""), self)
            if item_data.get("icon"):
                action.setIcon(get_icon(item_data["icon"], size=16))
            if item_data.get("shortcut"):
                action.setShortcut(item_data["shortcut"])
            action.triggered.connect(lambda checked, t=item_data.get("text", ""), d=item_data: self._on_action(t, d))
            menu.addAction(action)

        bar_item = _MenuBarItem(title, menu, self)
        self._items.append(bar_item)
        self._layout.insertWidget(self._layout.count() - 1, bar_item)
        return bar_item

    def _on_action(self, text: str, data: dict):
        self.menuTriggered.emit(text)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
                border-bottom: 1px solid {tm.color('stroke_divider')};
            }}
        """)
        menu_style = f"""
            QMenu {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('md')}px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 24px;
                border-radius: {tm.radius('sm')}px;
                color: {tm.color('fg_primary')};
            }}
            QMenu::item:selected {{
                background-color: {tm.color('bg_solid_tertiary')};
            }}
            QMenu::separator {{
                height: 1px;
                background: {tm.color('stroke_divider')};
                margin: 4px 8px;
            }}
        """
        for item in self._items:
            item.apply_theme()
            if item.menu:
                item.menu.setStyleSheet(menu_style)
