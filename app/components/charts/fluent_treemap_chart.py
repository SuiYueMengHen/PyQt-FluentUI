from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentTreemapChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: list[dict] = []
        self._rects: list[tuple] = []
        self._hovered_index = -1
        self.setMinimumSize(300, 200)
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(200)
        self._resize_timer.timeout.connect(self._compute_rects)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, data: list[dict]):
        self._data = data
        self._compute_rects()
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
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91", "#008272", "#CA5010", "#E74856", "#00CC6A"]

    def _compute_rects(self):
        self._rects = []
        if not self._data:
            return
        total = sum(d.get("value", 0) for d in self._data)
        if total == 0:
            return
        self._squarify(self._data, 0, 0, self.width(), self.height(), total)

    def _squarify(self, items, x, y, w, h, total):
        if not items or w <= 0 or h <= 0:
            return
        if len(items) == 1:
            self._rects.append((items[0], x, y, w, h))
            return

        half = total / 2
        running = 0
        split = 0
        for i, item in enumerate(items):
            running += item.get("value", 0)
            if running >= half:
                split = i + 1
                break
        if split == 0:
            split = 1
        if split >= len(items):
            split = len(items) - 1

        left = items[:split]
        right = items[split:]
        left_total = sum(d.get("value", 0) for d in left)
        right_total = total - left_total

        if w >= h:
            split_x = x + w * (left_total / total)
            self._squarify(left, x, y, split_x - x, h, left_total)
            self._squarify(right, split_x, y, x + w - split_x, h, right_total)
        else:
            split_y = y + h * (left_total / total)
            self._squarify(left, x, y, w, split_y - y, left_total)
            self._squarify(right, x, split_y, w, y + h - split_y, right_total)

    def resizeEvent(self, event):
        self._resize_timer.start()
        super().resizeEvent(event)

    def mouseMoveEvent(self, event):
        self._hovered_index = -1
        for i, (item, rx, ry, rw, rh) in enumerate(self._rects):
            if rx <= event.position().x() <= rx + rw and ry <= event.position().y() <= ry + rh:
                self._hovered_index = i
                break
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
        colors = self._chart_colors()
        for i, (item, rx, ry, rw, rh) in enumerate(self._rects):
            color = QColor(colors[i % len(colors)])
            is_hovered = i == self._hovered_index
            if is_hovered:
                color = color.lighter(120)

            alpha = int(255 * self._anim_progress)
            color.setAlpha(alpha)
            painter.setPen(QPen(QColor(tm.color("bg_solid_base")), 2))
            painter.setBrush(QBrush(color))
            rect = QRectF(rx, ry, rw, rh)
            painter.drawRoundedRect(rect, 4, 4)

            if rw > 40 and rh > 24:
                font = QFont()
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.setPen(QColor("#FFFFFF"))
                name = item.get("name", "")
                painter.drawText(QRectF(rx + 6, ry + 4, rw - 12, rh - 8), Qt.AlignLeft | Qt.AlignTop, name)

                if rh > 36:
                    val = item.get("value", 0)
                    font.setPixelSize(tm.font_size("body"))
                    font.setWeight(QFont.Bold)
                    painter.setFont(font)
                    painter.drawText(QRectF(rx + 6, ry + rh / 2 - 4, rw - 12, 20), Qt.AlignLeft | Qt.AlignTop, str(val))

        painter.end()

    def apply_theme(self):
        self._compute_rects()
        self.update()
