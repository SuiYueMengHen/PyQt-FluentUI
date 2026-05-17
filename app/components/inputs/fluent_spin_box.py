from PySide6.QtWidgets import QSpinBox
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSpinBox(QSpinBox, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setFixedHeight(36)
        self.setMinimum(0)
        self.setMaximum(9999)
        self.setAlignment(Qt.AlignCenter)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QSpinBox {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('md')}px;
                color: {tm.color('primary')};
                padding: 0 8px;
                font-size: {tm.font_size('body')}px;
            }}
            QSpinBox:focus {{
                border: 2px solid {tm.color('primary')};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: transparent;
                border: none;
                width: 24px;
                border-radius: 4px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {tm.color('bg_solid_tertiary')};
                border-radius: 4px;
            }}
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {{
                background-color: {tm.color('bg_solid_secondary')};
                border-radius: 4px;
            }}
            QSpinBox::up-button:disabled, QSpinBox::down-button:disabled {{
                opacity: 0.4;
            }}
            QSpinBox::up-arrow {{
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-bottom: 6px solid {tm.color('fg_secondary')};
            }}
            QSpinBox::up-arrow:hover {{
                border-bottom: 6px solid {tm.color('primary')};
            }}
            QSpinBox::up-arrow:disabled {{
                border-bottom: 6px solid {tm.color('fg_disabled')};
            }}
            QSpinBox::down-arrow {{
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid {tm.color('fg_secondary')};
            }}
            QSpinBox::down-arrow:hover {{
                border-top: 6px solid {tm.color('primary')};
            }}
            QSpinBox::down-arrow:disabled {{
                border-top: 6px solid {tm.color('fg_disabled')};
            }}
        """)
