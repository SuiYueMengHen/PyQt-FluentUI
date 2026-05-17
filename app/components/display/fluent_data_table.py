from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentDataTable(QWidget, FluentWidgetBase):
    row_clicked = Signal(int)
    sort_changed = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._columns: list[dict] = []
        self._rows: list[list] = []
        self._sort_col = -1
        self._sort_order = "asc"
        self._hovered_row = -1
        self._selected_row = -1
        self._header_h = 36
        self._row_h = 32
        self.setMinimumSize(300, 150)

    def set_data(self, columns: list[dict], rows: list[list]):
        self._columns = columns
        self._rows = rows
        self.setFixedHeight(max(self._header_h + len(rows) * self._row_h + 4, 100))
        self.update()

    def mouseMoveEvent(self, event):
        y = event.position().y()
        if y > self._header_h:
            idx = int((y - self._header_h) / self._row_h)
            self._hovered_row = idx if idx < len(self._rows) else -1
        else:
            self._hovered_row = -1
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_row = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            y = event.position().y()
            x = event.position().x()
            if y <= self._header_h:
                col_w = self.width() / max(len(self._columns), 1)
                col = int(x / col_w)
                if 0 <= col < len(self._columns) and self._columns[col].get("sortable", False):
                    if self._sort_col == col:
                        self._sort_order = "desc" if self._sort_order == "asc" else "asc"
                    else:
                        self._sort_col = col
                        self._sort_order = "asc"
                    self.sort_changed.emit(self._columns[col].get("key", ""), self._sort_order)
                    self.update()
            else:
                idx = int((y - self._header_h) / self._row_h)
                if 0 <= idx < len(self._rows):
                    self._selected_row = idx
                    self.row_clicked.emit(idx)
                    self.update()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 6, 6)

        if not self._columns:
            painter.end()
            return

        col_w = self.width() / len(self._columns)
        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_secondary")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self._header_h), 6, 6)
        painter.fillRect(QRectF(0, self._header_h // 2, self.width(), self._header_h // 2), QColor(tm.color("bg_solid_secondary")))

        for i, col in enumerate(self._columns):
            x = i * col_w
            painter.setPen(QColor(tm.color("fg_secondary")))
            font.setWeight(QFont.DemiBold)
            painter.setFont(font)
            text = col.get("title", "")
            if i == self._sort_col:
                text += " ↑" if self._sort_order == "asc" else " ↓"
            painter.drawText(QRectF(x + 12, 0, col_w - 24, self._header_h), Qt.AlignVCenter | Qt.AlignLeft, text)

        font.setWeight(QFont.Normal)
        painter.setFont(font)
        for ri, row in enumerate(self._rows):
            y = self._header_h + ri * self._row_h
            is_hovered = ri == self._hovered_row
            is_selected = ri == self._selected_row

            if is_selected:
                painter.setPen(Qt.NoPen)
                sel_bg = QColor(tm.color("primary_light"))
                sel_bg.setAlpha(80)
                painter.setBrush(QBrush(sel_bg))
                painter.drawRoundedRect(QRectF(2, y + 1, self.width() - 4, self._row_h - 2), 3, 3)
            elif is_hovered:
                painter.setPen(Qt.NoPen)
                hover_bg = QColor(tm.color("nav_item_hover"))
                painter.setBrush(QBrush(hover_bg))
                painter.drawRoundedRect(QRectF(2, y + 1, self.width() - 4, self._row_h - 2), 3, 3)

            for ci, cell in enumerate(row):
                x = ci * col_w
                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(QRectF(x + 12, y, col_w - 24, self._row_h), Qt.AlignVCenter | Qt.AlignLeft, str(cell))

            if ri < len(self._rows) - 1:
                painter.setPen(QPen(QColor(tm.color("stroke_divider")), 1))
                painter.drawLine(int(12), int(y + self._row_h), int(self.width() - 12), int(y + self._row_h))

        painter.end()

    def apply_theme(self):
        self.update()
