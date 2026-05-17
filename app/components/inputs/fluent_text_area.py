from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentTextArea(QPlainTextEdit, FluentWidgetBase):
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(80)
        self.setMaximumHeight(200)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.textChanged.connect(self._auto_resize)
        self._init_fluent_base()

    def _auto_resize(self):
        doc = self.document()
        doc.setTextWidth(self.viewport().width())
        new_height = min(max(doc.size().height() + 20, 80), 200)
        self.setFixedHeight(int(new_height))

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: transparent;
                border: none;
                border-bottom: 2px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('sm')}px {tm.radius('sm')}px 0 0;
                color: {tm.color('fg_primary')};
                padding: 8px 12px;
                font-size: {tm.font_size('body')}px;
                selection-background-color: {tm.color('primary')};
                selection-color: {tm.color('primary_text_on')};
            }}
            QPlainTextEdit:focus {{
                border-bottom: 2px solid {tm.color('primary')};
            }}
            QPlainTextEdit:disabled {{
                color: {tm.color('fg_disabled')};
                border-bottom-color: {tm.color('stroke_divider')};
            }}
            QPlainTextEdit::placeholder {{
                color: {tm.color('fg_tertiary')};
            }}
        """)
