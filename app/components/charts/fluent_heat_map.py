from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentHeatMap(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: list[list[float]] = []
        self._x_labels: list[str] = []
        self._y_labels: list[str] = []
        self._color_low = QColor("#E8F5E9")
        self._color_high = QColor("#1B5E20")
        self._hovered_cell = (-1, -1)
        self.setMinimumSize(300, 200)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, data: list[list[float]], x_labels: list[str] = None, y_labels: list[str] = None):
        self._data = data
        self._x_labels = x_labels or [str(i + 1) for i in range(len(data[0]) if data else 0)]
        self._y_labels = y_labels or [str(i + 1) for i in range(len(data))]
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    @Property(float)
    def anim_progress(self):
        return self._anim_progress

    @anim_progress.setter
    def anim_progress(self, v):
        self._anim_progress = v
        self.update()

    def _lerp_color(self, t: float) -> QColor:
        r = int(self._color_low.red() + (self._color_high.red() - self._color_low.red()) * t)
        g = int(self._color_low.green() + (self._color_high.green() - self._color_low.green()) * t)
        b = int(self._color_low.blue() + (self._color_high.blue() - self._color_low.blue()) * t)
        return QColor(r, g, b)

    def mouseMoveEvent(self, event):
        m = {"top": 30, "right": 20, "bottom": 30, "left": 50}
        cw = self.width() - m["left"] - m["right"]
        ch = self.height() - m["top"] - m["bottom"]
        rows = len(self._data)
        cols = len(self._data[0]) if rows > 0 else 0
        if rows == 0 or cols == 0:
            return super().mouseMoveEvent(event)
        cell_w = cw / cols
        cell_h = ch / rows
        col = int((event.position().x() - m["left"]) / cell_w)
        row = int((event.position().y() - m["top"]) / cell_h)
        if 0 <= row < rows and 0 <= col < cols:
            self._hovered_cell = (row, col)
        else:
            self._hovered_cell = (-1, -1)
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_cell = (-1, -1)
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if not self._data:
            painter.end()
            return

        m = {"top": 30, "right": 20, "bottom": 30, "left": 50}
        cx, cy = m["left"], m["top"]
        cw = self.width() - m["left"] - m["right"]
        ch = self.height() - m["top"] - m["bottom"]
        rows = len(self._data)
        cols = len(self._data[0]) if rows > 0 else 0

        if rows == 0 or cols == 0:
            painter.end()
            return

        all_vals = [v for row in self._data for v in row]
        min_val = min(all_vals)
        max_val = max(all_vals)
        val_range = max_val - min_val if max_val != min_val else 1

        cell_w = cw / cols
        cell_h = ch / rows

        for r in range(rows):
            for c in range(cols):
                val = self._data[r][c]
                t = (val - min_val) / val_range
                color = self._lerp_color(t)
                color.setAlpha(int(255 * self._anim_progress))

                is_hovered = self._hovered_cell == (r, c)
                if is_hovered:
                    color = color.lighter(130)

                painter.setPen(QPen(QColor(tm.color("bg_solid_base")), 1))
                painter.setBrush(QBrush(color))
                rect = QRectF(cx + c * cell_w, cy + r * cell_h, cell_w, cell_h)
                painter.drawRoundedRect(rect, 2, 2)

                if cell_w > 30 and cell_h > 16:
                    font = QFont()
                    font.setPixelSize(tm.font_size("caption"))
                    painter.setFont(font)
                    text_color = QColor("#FFFFFF") if t > 0.5 else QColor(tm.color("fg_primary"))
                    painter.setPen(text_color)
                    painter.drawText(rect, Qt.AlignCenter, f"{val:.0f}")

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        for c in range(cols):
            if c < len(self._x_labels):
                painter.drawText(QRectF(cx + c * cell_w, cy + ch + 4, cell_w, 20), Qt.AlignCenter, self._x_labels[c])
        for r in range(rows):
            if r < len(self._y_labels):
                painter.drawText(QRectF(0, cy + r * cell_h, m["left"] - 4, cell_h), Qt.AlignRight | Qt.AlignVCenter, self._y_labels[r])

        painter.end()

    def apply_theme(self):
        self.update()
