from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentPasswordEdit(QWidget, FluentWidgetBase):
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self._visible = False
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._edit = QLineEdit()
        self._edit.setPlaceholderText(placeholder)
        self._edit.setEchoMode(QLineEdit.Password)
        self._edit.setFixedHeight(36)
        self._edit.setTextMargins(12, 0, 36, 0)

        self._toggle_btn = QPushButton()
        self._toggle_btn.setFixedSize(36, 36)
        self._toggle_btn.setCursor(Qt.PointingHandCursor)
        self._toggle_btn.clicked.connect(self._toggle_visibility)

        layout.addWidget(self._edit)
        layout.addWidget(self._toggle_btn, alignment=Qt.AlignRight | Qt.AlignVCenter)

        self._init_fluent_base()
        self._update_toggle_icon()

    def _toggle_visibility(self):
        self._visible = not self._visible
        self._edit.setEchoMode(QLineEdit.Normal if self._visible else QLineEdit.Password)
        self._update_toggle_icon()

    def _update_toggle_icon(self):
        tm = self._tm
        icon_name = "eye_off" if self._visible else "eye"
        self._toggle_btn.setIcon(get_icon(icon_name, tm.color("fg_secondary"), 16))

    def text(self):
        return self._edit.text()

    def setText(self, text):
        self._edit.setText(text)

    def apply_theme(self):
        tm = self._tm
        self._edit.setStyleSheet(f"""
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
        """)
        self._toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {tm.radius('sm')}px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('bg_solid_tertiary')};
            }}
        """)
        self._update_toggle_icon()
