from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentSearchEdit(QWidget, FluentWidgetBase):
    def __init__(self, placeholder: str = "搜索...", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._edit = QLineEdit()
        self._edit.setPlaceholderText(placeholder)
        self._edit.setFixedHeight(36)
        self._edit.setTextMargins(36, 0, 36, 0)

        self._search_icon = QPushButton()
        self._search_icon.setFixedSize(36, 36)
        self._search_icon.setCursor(Qt.ArrowCursor)

        self._clear_btn = QPushButton()
        self._clear_btn.setFixedSize(28, 28)
        self._clear_btn.setCursor(Qt.PointingHandCursor)
        self._clear_btn.clicked.connect(self._edit.clear)
        self._clear_btn.hide()
        self._edit.textChanged.connect(self._on_text_changed)

        layout.addWidget(self._search_icon, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self._edit)
        layout.addWidget(self._clear_btn, alignment=Qt.AlignRight | Qt.AlignVCenter)

        self._init_fluent_base()

    def _on_text_changed(self, text):
        self._clear_btn.setVisible(bool(text))

    def text(self):
        return self._edit.text()

    def apply_theme(self):
        tm = self._tm
        self._edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: 18px;
                color: {tm.color('fg_primary')};
                padding: 0 36px;
                font-size: {tm.font_size('body')}px;
                selection-background-color: {tm.color('primary')};
                selection-color: {tm.color('primary_text_on')};
            }}
            QLineEdit:focus {{
                border-color: {tm.color('primary')};
                border-bottom: 2px solid {tm.color('primary')};
            }}
        """)
        self._search_icon.setStyleSheet("background: transparent; border: none;")
        self._search_icon.setIcon(get_icon("search", tm.color("fg_secondary"), 16))
        self._clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('bg_solid_tertiary')};
            }}
        """)
        self._clear_btn.setIcon(get_icon("close", tm.color("fg_secondary"), 12))
