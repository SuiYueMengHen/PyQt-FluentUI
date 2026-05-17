from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSlopeChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: list[dict] = []
        self._left_label: str = "Before"
        self._right_label: str = "After"
        self._margin = {"top": 40, "right": 60, "bottom": 30, "left": 60}
        self._hovered = -1
        self.setMinimumSize(300, 250)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, data: list[dict], left_label: str = "Before", right_label: str = "After"):
        self._data = data
        self._left_label = left_label
        self._right_label = right_label
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

    def _chart_colors(self):
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91", "#008272", "#CA5010", "#486860", "#8A5966"]

    def mouseMoveEvent(self, event):
        self._hovered = self._line_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -1
        self.update()
        super().leaveEvent(event)

    def _line_at(self, pos):
        if not self._data:
            return -1
        m = self._margin
        chart_x = m["left"]
        chart_y = m["top"]
        chart_w = self.width() - m["left"] - m["right"]
        chart_h = self.height() - m["top"] - m["bottom"]
        all_vals = [d.get("left", 0) for d in self._data] + [d.get("right", 0) for d in self._data]
        max_val = max(all_vals) if all_vals else 1
        max_val = max(max_val, 1)
        for i, d in enumerate(self._data):
            left_y = chart_y + chart_h - (d.get("left", 0) / max_val) * chart_h
            right_y = chart_y + chart_h - (d.get("right", 0) / max_val) * chart_h
            mid_x = chart_x + chart_w / 2
            mid_y = (left_y + right_y) / 2
            dx = pos.x() - mid_x
            dy = pos.y() - mid_y
            if abs(dx) < chart_w / 2 and abs(dy) < 20:
                return i
        return -1

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        m = self._margin
        chart_x = m["left"]
        chart_y = m["top"]
        chart_w = self.width() - m["left"] - m["right"]
        chart_h = self.height() - m["top"] - m["bottom"]

        if not self._data:
            painter.end()
            return

        all_vals = [d.get("left", 0) for d in self._data] + [d.get("right", 0) for d in self._data]
        max_val = max(all_vals) if all_vals else 1
        max_val = max(max_val, 1)

        painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1))
        painter.drawLine(int(chart_x), int(chart_y), int(chart_x), int(chart_y + chart_h))
        painter.drawLine(int(chart_x + chart_w), int(chart_y), int(chart_x + chart_w), int(chart_y + chart_h))

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(int(chart_x - 40), int(chart_y - 20), 80, 20, Qt.AlignCenter, self._left_label)
        painter.drawText(int(chart_x + chart_w - 40), int(chart_y - 20), 80, 20, Qt.AlignCenter, self._right_label)

        colors = self._chart_colors()
        for i, d in enumerate(self._data):
            left_y = chart_y + chart_h - (d.get("left", 0) / max_val) * chart_h
            right_y = chart_y + chart_h - (d.get("right", 0) / max_val) * chart_h
            is_hovered = i == self._hovered

            color = QColor(colors[i % len(colors)])
            if is_hovered:
                color = color.lighter(120)
                pen_w = 3
            else:
                color.setAlpha(160)
                pen_w = 2

            painter.setPen(QPen(color, pen_w))
            painter.drawLine(int(chart_x), int(left_y), int(chart_x + chart_w), int(right_y))

            for px, py, val in [(chart_x, left_y, d.get("left", 0)), (chart_x + chart_w, right_y, d.get("right", 0))]:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawEllipse(QRectF(px - 4, py - 4, 8, 8))

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))

            name = d.get("name", "")
            painter.drawText(int(chart_x - m["left"] + 4), int(left_y - 8), int(m["left"] - 8), 16, Qt.AlignRight | Qt.AlignVCenter, name)
            painter.drawText(int(chart_x + chart_w + 6), int(right_y - 8), int(m["right"] - 6), 16, Qt.AlignLeft | Qt.AlignVCenter, name)

            if is_hovered:
                painter.setPen(QColor(tm.color("fg_primary")))
                font.setWeight(QFont.DemiBold)
                painter.setFont(font)
                painter.drawText(int(chart_x - m["left"] + 4), int(left_y + 6), int(m["left"] - 8), 16, Qt.AlignRight | Qt.AlignVCenter, f"{d.get('left', 0)}")
                painter.drawText(int(chart_x + chart_w + 6), int(right_y + 6), int(m["right"] - 6), 16, Qt.AlignLeft | Qt.AlignVCenter, f"{d.get('right', 0)}")

        painter.end()

    def apply_theme(self):
        self.update()
