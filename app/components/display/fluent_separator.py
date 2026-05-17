from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSeparator(QFrame, FluentWidgetBase):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._orientation = orientation
        if orientation == Qt.Horizontal:
            self.setFixedHeight(1)
            self.setFrameShape(QFrame.HLine)
        else:
            self.setFixedWidth(1)
            self.setFrameShape(QFrame.VLine)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {tm.color('stroke_divider')};
                border: none;
            }}
        """)
