from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentWaterfallChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: list[dict] = []
        self._margin = {"top": 30, "right": 20, "bottom": 40, "left": 50}
        self._hovered_index = -1
        self.setMinimumSize(300, 200)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, data: list[dict]):
        self._data = data
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

    def mouseMoveEvent(self, event):
        m = self._margin
        cw = self.width() - m["left"] - m["right"]
        if not self._data:
            return super().mouseMoveEvent(event)
        bar_w = min(40, cw / len(self._data) - 8)
        total_w = len(self._data) * (bar_w + 8)
        start_x = m["left"] + (cw - total_w) / 2
        idx = int((event.position().x() - start_x) / (bar_w + 8))
        self._hovered_index = max(-1, min(idx, len(self._data) - 1))
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_index = -1
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

        m = self._margin
        cx, cy = m["left"], m["top"]
        cw = self.width() - m["left"] - m["right"]
        ch = self.height() - m["top"] - m["bottom"]

        running = 0
        min_val = 0
        max_val = 0
        for d in self._data:
            val = d.get("value", 0)
            if d.get("is_total", False):
                running = val
            else:
                running += val
            min_val = min(min_val, running)
            max_val = max(max_val, running)

        val_range = max_val - min_val if max_val != min_val else 1

        painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1))
        for i in range(5):
            y = cy + ch - (i / 4) * ch
            painter.drawLine(int(cx), int(y), int(cx + cw), int(y))
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            val = min_val + val_range * i / 4
            painter.drawText(0, int(y - 6), int(cx - 6), 16, Qt.AlignRight | Qt.AlignVCenter, f"{val:.0f}")

        bar_w = min(40, cw / len(self._data) - 8)
        total_w = len(self._data) * (bar_w + 8)
        start_x = cx + (cw - total_w) / 2

        running = 0
        for i, d in enumerate(self._data):
            val = d.get("value", 0)
            is_total = d.get("is_total", False)
            bx = start_x + i * (bar_w + 8)

            if is_total:
                bar_h = (val / val_range) * ch * self._anim_progress
                by = cy + ch - bar_h
                color = QColor(tm.color("fg_tertiary"))
                running = val
            else:
                prev = running
                running += val
                if val >= 0:
                    bar_h = (val / val_range) * ch * self._anim_progress
                    by = cy + ch - (running / val_range) * ch * self._anim_progress
                    color = QColor("#107C10")
                else:
                    bar_h = (-val / val_range) * ch * self._anim_progress
                    by = cy + ch - (prev / val_range) * ch * self._anim_progress
                    color = QColor("#D83B01")

            is_hovered = i == self._hovered_index
            if is_hovered:
                color = color.lighter(120)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(bx, by, bar_w, bar_h), 3, 3)

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            name = d.get("name", "")
            painter.drawText(QRectF(bx - 8, cy + ch + 6, bar_w + 16, 24), Qt.AlignCenter, name)

            if is_hovered:
                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(QRectF(bx, by - 18, bar_w, 16), Qt.AlignCenter, f"{val}")

        painter.end()

    def apply_theme(self):
        self.update()
