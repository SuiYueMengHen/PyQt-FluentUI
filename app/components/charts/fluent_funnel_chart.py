from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentFunnelChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: list[dict] = []
        self._hovered_index = -1
        self.setMinimumSize(250, 300)

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

    def _chart_colors(self):
        return ["#0078D4", "#2B88D8", "#4EA8E6", "#71C4F0", "#9BDBF5", "#BEE9FA"]

    def mouseMoveEvent(self, event):
        if not self._data:
            return super().mouseMoveEvent(event)
        margin_top = 20
        margin_bottom = 20
        ch = self.height() - margin_top - margin_bottom
        step_h = ch / len(self._data)
        idx = int((event.position().y() - margin_top) / step_h)
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

        max_val = max(d.get("value", 0) for d in self._data)
        if max_val == 0:
            painter.end()
            return

        margin_top = 20
        margin_bottom = 20
        margin_x = 60
        cw = self.width() - margin_x * 2
        ch = self.height() - margin_top - margin_bottom
        step_h = ch / len(self._data)
        colors = self._chart_colors()

        for i, d in enumerate(self._data):
            val = d.get("value", 0)
            ratio = val / max_val
            bar_w = cw * ratio * self._anim_progress
            x = margin_x + (cw - bar_w) / 2
            y = margin_top + i * step_h

            color = QColor(colors[i % len(colors)])
            is_hovered = i == self._hovered_index
            if is_hovered:
                color = color.lighter(120)

            path = QPainterPath()
            r = min(4, step_h / 4)
            if i < len(self._data) - 1:
                next_val = self._data[i + 1].get("value", 0)
                next_ratio = next_val / max_val
                next_bar_w = cw * next_ratio * self._anim_progress
                next_x = margin_x + (cw - next_bar_w) / 2

                path.moveTo(x, y)
                path.lineTo(x + bar_w, y)
                path.lineTo(next_x + next_bar_w, y + step_h)
                path.lineTo(next_x, y + step_h)
            else:
                path.addRoundedRect(QRectF(x, y, bar_w, step_h - 2), r, r)

            path.closeSubpath()
            painter.setPen(QPen(QColor(tm.color("bg_solid_base")), 1))
            painter.setBrush(QBrush(color))
            painter.drawPath(path)

            font = QFont()
            font.setPixelSize(tm.font_size("body"))
            font.setWeight(QFont.DemiBold)
            painter.setFont(font)
            painter.setPen(QColor("#FFFFFF") if ratio > 0.3 else QColor(tm.color("fg_primary")))
            name = d.get("name", "")
            painter.drawText(QRectF(x, y, bar_w, step_h), Qt.AlignCenter, name)

            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(0, y, margin_x - 4, step_h), Qt.AlignRight | Qt.AlignVCenter, f"{val}")

            painter.drawText(QRectF(self.width() - margin_x + 4, y, margin_x - 4, step_h), Qt.AlignLeft | Qt.AlignVCenter, f"{(val / max_val * 100):.0f}%")

        painter.end()

    def apply_theme(self):
        self.update()
