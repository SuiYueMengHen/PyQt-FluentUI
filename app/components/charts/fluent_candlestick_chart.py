from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentCandlestickChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: list[dict] = []
        self._margin = {"top": 30, "right": 20, "bottom": 40, "left": 50}
        self._hovered_index = -1
        self.setMinimumSize(350, 220)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(800)
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
        step = cw / len(self._data)
        idx = int((event.position().x() - m["left"]) / step)
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

        all_high = [d.get("high", 0) for d in self._data]
        all_low = [d.get("low", 0) for d in self._data]
        max_val = max(all_high) if all_high else 1
        min_val = min(all_low) if all_low else 0
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

        step = cw / len(self._data)
        body_w = min(step * 0.6, 20)
        up_color = QColor("#107C10")
        down_color = QColor("#D83B01")

        for i, d in enumerate(self._data):
            open_v = d.get("open", 0)
            close_v = d.get("close", 0)
            high_v = d.get("high", 0)
            low_v = d.get("low", 0)
            label = d.get("label", str(i + 1))

            bx = cx + step * i + step / 2 - body_w / 2
            is_up = close_v >= open_v
            color = up_color if is_up else down_color
            is_hovered = i == self._hovered_index
            if is_hovered:
                color = color.lighter(120)

            high_y = cy + ch - ((high_v - min_val) / val_range) * ch * self._anim_progress
            low_y = cy + ch - ((low_v - min_val) / val_range) * ch * self._anim_progress
            open_y = cy + ch - ((open_v - min_val) / val_range) * ch * self._anim_progress
            close_y = cy + ch - ((close_v - min_val) / val_range) * ch * self._anim_progress

            wick_x = cx + step * i + step / 2
            painter.setPen(QPen(color, 1.5))
            painter.drawLine(int(wick_x), int(high_y), int(wick_x), int(low_y))

            body_top = min(open_y, close_y)
            body_h = max(abs(close_y - open_y), 1)
            painter.setPen(QPen(color, 1))
            if is_up:
                painter.setBrush(QColor(tm.color("bg_solid_base")))
            else:
                painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(bx, body_top, body_w, body_h), 1, 1)

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(cx + step * i, cy + ch + 6, int(step), 24), Qt.AlignCenter, label)

            if is_hovered:
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                tooltip = f"O:{open_v} H:{high_v} L:{low_v} C:{close_v}"
                tw = painter.fontMetrics().horizontalAdvance(tooltip) + 12
                tr = QRectF(wick_x - tw / 2, high_y - 24, tw, 20)
                painter.setBrush(QColor(tm.color("bg_solid_card")))
                painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
                painter.drawRoundedRect(tr, 4, 4)
                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(tr, Qt.AlignCenter, tooltip)

        painter.end()

    def apply_theme(self):
        self.update()
