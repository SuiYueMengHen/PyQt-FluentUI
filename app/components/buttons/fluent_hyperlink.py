from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentHyperlink(QPushButton, FluentWidgetBase):
    def __init__(self, text: str = "", url: str = "", parent=None):
        super().__init__(text, parent)
        self._url = url
        self._init_fluent_base()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(32)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {tm.radius('sm')}px;
                color: {tm.color('primary')};
                padding: 4px 8px;
                font-size: {tm.font_size('body')}px;
                text-decoration: none;
            }}
            QPushButton:hover {{
                text-decoration: underline;
                background-color: {tm.color('primary_light')};
            }}
            QPushButton:pressed {{
                color: {tm.color('primary_pressed')};
            }}
            QPushButton:disabled {{
                color: {tm.color('fg_disabled')};
            }}
        """)
