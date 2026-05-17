from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentLineEdit(QLineEdit, FluentWidgetBase):
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(36)
        self.setTextMargins(12, 0, 12, 0)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('md')}px;
                color: {tm.color('fg_primary')};
                padding: 0 12px;
                font-size: {tm.font_size('body')}px;
                selection-background-color: {tm.color('primary')};
                selection-color: {tm.color('primary_text_on')};
            }}
            QLineEdit:focus {{
                border-color: {tm.color('primary')};
                border-bottom: 2px solid {tm.color('primary')};
            }}
            QLineEdit:disabled {{
                background-color: {tm.color('bg_solid_tertiary')};
                color: {tm.color('fg_disabled')};
                border-color: {tm.color('stroke_divider')};
            }}
        """)
