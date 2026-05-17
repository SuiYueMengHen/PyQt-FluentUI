from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentButton(QPushButton, FluentWidgetBase):
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
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('md')}px;
                color: {tm.color('fg_primary')};
                padding: 0 20px;
                font-size: {tm.font_size('body')}px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {tm.color('bg_solid_tertiary')};
                border-color: {tm.color('stroke_hover')};
            }}
            QPushButton:pressed {{
                background-color: {tm.color('bg_solid_tertiary')};
                border-color: {tm.color('primary')};
            }}
            QPushButton:disabled {{
                background-color: {tm.color('bg_solid_tertiary')};
                color: {tm.color('fg_disabled')};
                border-color: {tm.color('stroke_divider')};
            }}
        """)

    def sizeHint(self):
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        return QSize(max(80, text_width + 40), 36)
