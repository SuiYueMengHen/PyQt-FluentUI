from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentTreeSelect(QWidget, FluentWidgetBase):
    selected_changed = Signal(str)
    _drop_progress = 0.0

    def __init__(self, placeholder: str = "请选择", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._placeholder = placeholder
        self._tree_data: list[dict] = []
        self._selected = ""
        self._expanded: set = set()
        self._is_open = False
        self._hovered_node = ""
        self.setFixedHeight(32)
        self.setMinimumWidth(200)
        self.setCursor(Qt.PointingHandCursor)

        self._drop_anim = QPropertyAnimation(self, b"drop_progress")
        self._drop_anim.setDuration(200)
        self._drop_anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, data: list[dict]):
        self._tree_data = data

    @Property(float)
    def drop_progress(self):
        return self._drop_progress

    @drop_progress.setter
    def drop_progress(self, v):
        self._drop_progress = v
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self._is_open:
                self._is_open = True
                self._drop_anim.stop()
                self._drop_anim.setStartValue(0.0)
                self._drop_anim.setEndValue(1.0)
                self._drop_anim.start()
            else:
                node = self._node_at(event.position())
                if node:
                    if node in self._expanded:
                        self._expanded.discard(node)
                    else:
                        self._selected = node
                        self.selected_changed.emit(node)
                        self._is_open = False
                        self._drop_anim.stop()
                        self._drop_anim.setStartValue(1.0)
                        self._drop_anim.setEndValue(0.0)
                        self._drop_anim.start()
                    self.update()
        super().mousePressEvent(event)

    def _node_at(self, pos):
        return ""

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        border_color = QColor(tm.color("primary")) if self._is_open else QColor(tm.color("stroke_card"))
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 4, 4)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        if self._selected:
            painter.setPen(QColor(tm.color("fg_primary")))
            painter.drawText(QRectF(10, 0, self.width() - 30, self.height()), Qt.AlignVCenter, self._selected)
        else:
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(QRectF(10, 0, self.width() - 30, self.height()), Qt.AlignVCenter, self._placeholder)

        arrow = get_icon("chevron_down", tm.color("fg_secondary"), 12)
        painter.drawPixmap(int(self.width() - 20), int((self.height() - 12) / 2), arrow.pixmap(12, 12))

        painter.end()

    def apply_theme(self):
        self.update()
