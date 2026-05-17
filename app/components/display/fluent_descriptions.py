from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentDescriptions(QWidget, FluentWidgetBase):
    def __init__(self, data: list = None, columns: int = 2, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data = data or []
        self._columns = columns
        self._row_height = 36
        self._label_width = 100
        self.setMinimumWidth(300)
        self.setFixedHeight(max((len(self._data) + columns - 1) // columns * self._row_height + 8, 40))

    def set_data(self, data: list, columns: int = 2):
        self._data = data
        self._columns = columns
        self.setFixedHeight(max((len(self._data) + columns - 1) // columns * self._row_height + 8, 40))
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if not self._data:
            painter.end()
            return

        col_w = self.width() / self._columns
        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        for i, item in enumerate(self._data):
            col = i % self._columns
            row = i // self._columns
            x = col * col_w
            y = row * self._row_height

            label = item.get("label", "") if isinstance(item, dict) else str(item)
            value = item.get("value", "") if isinstance(item, dict) else ""

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
            painter.drawRect(QRectF(x, y, self._label_width, self._row_height))

            font.setWeight(QFont.DemiBold)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(x + 12, y, self._label_width - 16, self._row_height), Qt.AlignVCenter | Qt.AlignLeft, label)

            painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
            painter.drawLine(int(x + self._label_width), int(y + 4), int(x + self._label_width), int(y + self._row_height - 4))

            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_primary")))
            val_w = col_w - self._label_width
            painter.drawText(QRectF(x + self._label_width + 12, y, val_w - 16, self._row_height), Qt.AlignVCenter | Qt.AlignLeft, str(value))

            painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
            painter.drawLine(int(x + 8), int(y + self._row_height - 1), int(x + col_w - 8), int(y + self._row_height - 1))

        painter.end()

    def apply_theme(self):
        self.update()
