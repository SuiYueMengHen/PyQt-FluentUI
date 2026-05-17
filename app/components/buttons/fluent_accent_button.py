from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentAccentButton(QPushButton, FluentWidgetBase):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(36)
        self.setMinimumWidth(80)
        self._init_fluent_base()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {tm.color('primary')};
                border: none;
                border-radius: {tm.radius('md')}px;
                color: {tm.color('primary_text_on')};
                padding: 0 20px;
                font-size: {tm.font_size('body')}px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {tm.color('primary_hover')};
            }}
            QPushButton:pressed {{
                background-color: {tm.color('primary_pressed')};
            }}
            QPushButton:disabled {{
                background-color: {tm.color('fg_disabled')};
                color: {tm.color('bg_solid_card')};
            }}
        """)

    def sizeHint(self):
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        return QSize(max(80, text_width + 40), 36)
