from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentCard(QWidget, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FluentCard")
        self.setMinimumHeight(80)

        self._inner_layout = QVBoxLayout(self)
        self._inner_layout.setContentsMargins(20, 16, 20, 16)
        self._inner_layout.setSpacing(8)

        self._init_fluent_base()

    def set_content(self, widget: QWidget):
        self._inner_layout.addWidget(widget)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QWidget#FluentCard {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('lg')}px;
            }}
            QWidget#FluentCard:hover {{
                border-color: {tm.color('stroke_hover')};
            }}
        """)
