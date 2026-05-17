from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class TimelineItemData:
    def __init__(self, title: str, description: str = "", timestamp: str = "", status: str = "default"):
        self.title = title
        self.description = description
        self.timestamp = timestamp
        self.status = status
        self.scale = 0.0


class FluentTimeline(QWidget, FluentWidgetBase):
    itemClicked = Signal(int)
    _item_scale = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._items: list[TimelineItemData] = []
        self._dot_size = 12
        self._line_width = 2
        self._item_height = 56
        self._left_margin = 32
        self._hovered_index = -1
        self.setCursor(Qt.PointingHandCursor)

    def add_item(self, title: str, description: str = "", timestamp: str = "", status: str = "default"):
        item = TimelineItemData(title, description, timestamp, status)
        self._items.append(item)
        idx = len(self._items) - 1
        anim = QPropertyAnimation(self, b"item_scale")
        anim.setDuration(300)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutBack)
        anim.start()
        self._scale_anims = getattr(self, '_scale_anims', [])
        self._scale_anims.append(anim)
        self.setFixedHeight(max(len(self._items) * self._item_height + 20, 80))
        self.update()

    def set_item_status(self, index: int, status: str):
        if 0 <= index < len(self._items):
            self._items[index].status = status
            self.update()

    @Property(float)
    def item_scale(self):
        return self._item_scale

    @item_scale.setter
    def item_scale(self, value):
        self._item_scale = value
        self.update()

    def _item_at(self, pos) -> int:
        for i in range(len(self._items)):
            y = 10 + i * self._item_height
            if y <= pos.y() <= y + self._item_height:
                return i
        return -1

    def mouseMoveEvent(self, event):
        idx = self._item_at(event.position())
        if idx != self._hovered_index:
            self._hovered_index = idx
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        idx = self._item_at(event.position())
        if idx >= 0:
            self.itemClicked.emit(idx)
        super().mousePressEvent(event)

    def leaveEvent(self, event):
        self._hovered_index = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if not self._items:
            painter.end()
            return

        dot_r = self._dot_size / 2
        cx = self._left_margin

        for i, item in enumerate(self._items):
            y = 10 + i * self._item_height
            dot_cy = y + self._item_height / 2

            if i < len(self._items) - 1:
                next_y = 10 + (i + 1) * self._item_height
                line_start = dot_cy + dot_r + 2
                line_end = next_y + self._item_height / 2 - dot_r - 2
                painter.setPen(QPen(QColor(tm.color("stroke_divider")), self._line_width))
                painter.drawLine(int(cx), int(line_start), int(cx), int(line_end))

            status_colors = {
                "default": tm.color("fg_tertiary"),
                "active": tm.color("primary"),
                "completed": tm.color("accent_success"),
                "error": tm.color("accent_error"),
            }
            dot_color = QColor(status_colors.get(item.status, status_colors["default"]))

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(dot_color))
            painter.drawEllipse(QRectF(cx - dot_r, dot_cy - dot_r, self._dot_size, self._dot_size))

            if item.status == "completed":
                check_color = QColor(tm.color("primary_text_on"))
                pen = QPen(check_color, 2)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                painter.drawLine(int(cx - 3), int(dot_cy), int(cx - 1), int(dot_cy + 2))
                painter.drawLine(int(cx - 1), int(dot_cy + 2), int(cx + 4), int(dot_cy - 3))

            text_x = cx + dot_r + 16
            is_hovered = (i == self._hovered_index)

            font = QFont()
            font.setPixelSize(tm.font_size("body"))
            font.setWeight(QFont.DemiBold if is_hovered else QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("primary") if is_hovered else tm.color("fg_primary")))
            painter.drawText(int(text_x), int(dot_cy - 6), item.title)

            if item.description:
                font.setPixelSize(tm.font_size("caption"))
                font.setWeight(QFont.Normal)
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_secondary")))
                painter.drawText(int(text_x), int(dot_cy + 12), item.description)

            if item.timestamp:
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_tertiary")))
                ts_width = painter.fontMetrics().horizontalAdvance(item.timestamp)
                painter.drawText(self.width() - ts_width - 12, int(dot_cy + 4), item.timestamp)

        painter.end()

    def apply_theme(self):
        self.update()
