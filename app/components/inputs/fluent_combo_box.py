from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentComboBox(QComboBox, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setFixedHeight(36)
        self.setMinimumWidth(120)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('md')}px;
                color: {tm.color('fg_primary')};
                padding: 0 32px 0 12px;
                font-size: {tm.font_size('body')}px;
            }}
            QComboBox:focus {{
                border: 2px solid {tm.color('primary')};
            }}
            QComboBox::drop-down {{
                background-color: transparent;
                border: none;
                width: 32px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid {tm.color('fg_secondary')};
                margin-right: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('md')}px;
                color: {tm.color('fg_primary')};
                selection-background-color: {tm.color('primary_light')};
                selection-color: {tm.color('primary')};
                padding: 4px;
                outline: none;
                margin: 0;
            }}
            QComboBox QAbstractItemView::item {{
                padding: 8px 12px;
                border-radius: {tm.radius('sm')}px;
                min-height: 28px;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: {tm.color('bg_solid_tertiary')};
            }}
        """)
