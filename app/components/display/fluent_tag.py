from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, Signal

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentTag(QWidget, FluentWidgetBase):
    closed = Signal()

    def __init__(self, text: str = "", tag_type: str = "default", closable: bool = False, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._tag_type = tag_type
        self._closable = closable
        self.setFixedHeight(28)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 6, 0)
        layout.setSpacing(4)

        self._label = QLabel(text)
        layout.addWidget(self._label)

        if closable:
            self._close_btn = QPushButton()
            self._close_btn.setFixedSize(18, 18)
            self._close_btn.setCursor(Qt.PointingHandCursor)
            self._close_btn.clicked.connect(self._on_close)
            layout.addWidget(self._close_btn)

    def _on_close(self):
        self.closed.emit()
        self.setParent(None)
        self.deleteLater()

    def apply_theme(self):
        tm = self._tm
        type_colors = {
            "default": (tm.color('bg_solid_tertiary'), tm.color('fg_primary')),
            "primary": (tm.color('primary_light'), tm.color('primary')),
            "success": (tm.color('accent_success_light'), tm.color('accent_success')),
            "warning": (tm.color('accent_warning_light'), tm.color('accent_warning')),
            "error": (tm.color('accent_error_light'), tm.color('accent_error')),
        }
        bg, fg = type_colors.get(self._tag_type, type_colors["default"])
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg};
                border: none;
                border-radius: 14px;
            }}
        """)
        self._label.setStyleSheet(f"color: {fg}; font-size: {tm.font_size('caption')}px; font-weight: 500; background: transparent;")
        if self._closable:
            self._close_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: 9px;
                }}
                QPushButton:hover {{
                    background-color: {tm.color('bg_solid_tertiary')};
                }}
            """)
            self._close_btn.setIcon(get_icon("close", fg, 10))
