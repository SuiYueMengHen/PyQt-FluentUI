from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentBreadcrumb(QWidget, FluentWidgetBase):
    item_clicked = Signal(str)

    def __init__(self, items: list[str] = None, parent=None):
        super().__init__(parent)
        self._items = items or []
        self.setFixedHeight(32)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._init_fluent_base()

    def _build_ui(self):
        while self._layout.count():
            child = self._layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i, item_text in enumerate(self._items):
            if i > 0:
                sep = QLabel()
                tm = self._tm
                sep.setPixmap(get_icon("chevron_right", tm.color("fg_tertiary"), 12).pixmap(12, 12))
                sep.setFixedWidth(20)
                sep.setAlignment(Qt.AlignCenter)
                sep.setStyleSheet("background: transparent;")
                self._layout.addWidget(sep)

            btn = QLabel(item_text)
            btn.setCursor(Qt.PointingHandCursor)
            is_last = (i == len(self._items) - 1)
            tm = self._tm
            color = tm.color('fg_primary') if is_last else tm.color('fg_secondary')
            weight = '600' if is_last else '400'
            btn.setStyleSheet(f"color: {color}; font-size: {tm.font_size('body')}px; font-weight: {weight}; background: transparent; padding: 4px 4px;")
            self._layout.addWidget(btn)

        self._layout.addStretch()

    def set_items(self, items: list[str]):
        self._items = items
        self._build_ui()

    def apply_theme(self):
        self.setStyleSheet("background: transparent;")
        self._build_ui()
