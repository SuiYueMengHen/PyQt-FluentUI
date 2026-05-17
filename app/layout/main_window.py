from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QPen, QCursor

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.navigation.fluent_navigation import FluentNavigation
from app.components.surfaces.fluent_user_info_overlay import FluentUserInfoOverlay
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class _TitleBarButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_close = False
        self._is_hovered = False

    def enterEvent(self, event):
        self._is_hovered = True
        if self._is_close:
            self._update_close_icon()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_hovered = False
        if self._is_close:
            self._update_close_icon()
        super().leaveEvent(event)

    def _update_close_icon(self):
        tm = ThemeManager()
        if self._is_hovered:
            color = tm.color("titlebar_button_close_fg")
        else:
            color = tm.color("fg_secondary")
        self.setIcon(get_icon("close", color, 14))


class TitleBar(QWidget, FluentWidgetBase):
    theme_toggled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)
        self._drag_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 8, 0)
        layout.setSpacing(8)

        self._title = QLabel("FluentUI Gallery")
        layout.addWidget(self._title)
        layout.addStretch()

        self._theme_btn = QPushButton()
        self._theme_btn.setFixedSize(36, 36)
        self._theme_btn.setCursor(Qt.PointingHandCursor)
        self._theme_btn.clicked.connect(self.theme_toggled.emit)
        layout.addWidget(self._theme_btn)

        self._max_btn = QPushButton()
        self._max_btn.setFixedSize(36, 36)
        self._max_btn.setCursor(Qt.PointingHandCursor)
        self._max_btn.clicked.connect(self._on_maximize)
        layout.addWidget(self._max_btn)

        self._close_btn = _TitleBarButton()
        self._close_btn._is_close = True
        self._close_btn.setFixedSize(36, 36)
        self._close_btn.setCursor(Qt.PointingHandCursor)
        self._close_btn.clicked.connect(self._on_close)
        layout.addWidget(self._close_btn)

        self._init_fluent_base()

    def _on_maximize(self):
        if self.window():
            if self.window().isMaximized():
                self.window().showNormal()
            else:
                self.window().showMaximized()
            self._update_maximize_icon()

    def _update_maximize_icon(self):
        tm = ThemeManager()
        if self.window() and self.window().isMaximized():
            icon_name = "minimize"
        else:
            icon_name = "maximize"
        self._max_btn.setIcon(get_icon(icon_name, tm.color("fg_secondary"), 14))

    def _on_close(self):
        if self.window():
            self.window().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def showEvent(self, event):
        super().showEvent(event)
        self._fluent_show_event(event)

    def apply_theme(self):
        tm = ThemeManager()
        self.setStyleSheet(f"background-color: {tm.color('titlebar_bg')};")
        self._title.setStyleSheet(f"color: {tm.color('titlebar_fg')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")

        icon_name = "moon" if not tm.is_dark else "sun"
        self._theme_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {tm.radius('sm')}px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('titlebar_button_hover')};
            }}
        """)
        self._theme_btn.setIcon(get_icon(icon_name, tm.color("fg_secondary"), 16))

        self._max_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {tm.radius('sm')}px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('titlebar_button_hover')};
            }}
        """)
        self._update_maximize_icon()

        self._close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {tm.radius('sm')}px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('titlebar_button_close_hover')};
            }}
        """)
        self._close_btn.setIcon(get_icon("close", tm.color("fg_secondary"), 14))


class MainWindow(QWidget, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(1100, 700)
        self.resize(1200, 800)
        self._pages = {}
        self._lazy_pages = {}

        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        self._title_bar = TitleBar(self)
        self._title_bar.theme_toggled.connect(self._toggle_theme)
        self._main_layout.addWidget(self._title_bar)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self._nav = FluentNavigation(self)
        self._nav.item_clicked.connect(self._on_nav_clicked)
        self._nav.profile_clicked.connect(self._show_user_info)
        body_layout.addWidget(self._nav)

        self._stack = QStackedWidget()
        body_layout.addWidget(self._stack, 1)

        self._user_overlay = FluentUserInfoOverlay(parent=body)
        self._user_overlay.theme_btn_clicked.connect(self._toggle_theme)

        self._main_layout.addWidget(body, 1)

        self._init_fluent_base()

    def _show_user_info(self):
        self._user_overlay.open_overlay()

    def add_page(self, key: str, label: str, icon_name: str, page: QWidget,
                 children: list[dict] | None = None):
        self._pages[key] = page
        self._nav.add_item(key, label, icon_name, children)
        self._stack.addWidget(page)

    def add_lazy_page(self, key: str, label: str, icon_name: str, page_factory,
                      children: list[dict] | None = None):
        self._lazy_pages[key] = page_factory
        self._nav.add_item(key, label, icon_name, children)

    def add_nav_separator(self, title: str = ""):
        self._nav.add_separator(title)

    def _on_nav_clicked(self, key: str):
        if key in self._pages:
            self._stack.setCurrentWidget(self._pages[key])
        elif key in self._lazy_pages:
            page = self._lazy_pages[key]()
            self._pages[key] = page
            del self._lazy_pages[key]
            self._stack.addWidget(page)
            self._stack.setCurrentWidget(page)

    def _toggle_theme(self):
        tm = ThemeManager()
        tm.toggle_theme()

    def showEvent(self, event):
        super().showEvent(event)
        self._fluent_show_event(event)

    def apply_theme(self):
        tm = ThemeManager()
        self.setStyleSheet(f"background-color: {tm.color('bg_solid_base')};")
