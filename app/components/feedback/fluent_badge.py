from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentBadge(QLabel, FluentWidgetBase):
    def __init__(self, text: str = "", badge_type: str = "default", parent=None):
        super().__init__(text, parent)
        self._init_fluent_base()
        self._badge_type = badge_type
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(20)
        self.setMinimumWidth(20)
        self.setContentsMargins(6, 0, 6, 0)

    def apply_theme(self):
        tm = self._tm
        type_colors = {
            "default": (tm.color('bg_solid_tertiary'), tm.color('fg_primary')),
            "primary": (tm.color('primary'), tm.color('primary_text_on')),
            "success": (tm.color('accent_success_light'), tm.color('accent_success')),
            "warning": (tm.color('accent_warning_light'), tm.color('accent_warning')),
            "error": (tm.color('accent_error_light'), tm.color('accent_error')),
        }
        bg, fg = type_colors.get(self._badge_type, type_colors["default"])
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border: none;
                border-radius: 10px;
                font-size: {tm.font_size('caption')}px;
                font-weight: 600;
                padding: 0 6px;
            }}
        """)
