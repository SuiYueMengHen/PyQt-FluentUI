from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.inputs.fluent_search_edit import FluentSearchEdit
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentCommandBar(QWidget, FluentWidgetBase):
    command_triggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setFixedHeight(44)
        self.setMinimumWidth(400)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        self._search = FluentSearchEdit()
        self._search.setFixedHeight(32)
        layout.addWidget(self._search, 1)

        self._actions: list[dict] = []
        self._action_buttons: list[QWidget] = []

    def add_action(self, icon_name: str, tooltip: str = "", key: str = ""):
        self._actions.append({"icon": icon_name, "tooltip": tooltip, "key": key or icon_name})

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 6, 6)

        x = self.width() - 12
        for action in reversed(self._actions):
            icon = get_icon(action["icon"], tm.color("fg_secondary"), 18)
            x -= 28
            painter.drawPixmap(x, int((self.height() - 18) / 2), icon.pixmap(18, 18))

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self._search.apply_theme()
        self.update()
