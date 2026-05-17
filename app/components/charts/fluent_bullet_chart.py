from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentBulletChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._measures: list[dict] = []
        self._max = 100
        self._margin = {"top": 20, "right": 30, "bottom": 10, "left": 80}
        self._row_height = 36
        self._hovered = -1
        self.setMinimumSize(350, 120)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, measures: list[dict], max_val: float = 100):
        self._measures = measures
        self._max = max_val
        self.setFixedHeight(max(len(measures) * self._row_height + self._margin["top"] + self._margin["bottom"], 80))
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
        y = event.position().y()
        idx = int((y - m["top"]) / self._row_height)
        if 0 <= idx < len(self._measures) and y >= m["top"]:
            self._hovered = idx
        else:
            self._hovered = -1
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        m = self._margin
        if not self._measures:
            painter.end()
            return

        chart_x = m["left"]
        chart_y = m["top"]
        chart_w = self.width() - m["left"] - m["right"]
        max_val = self._max or 1

        for i in range(6):
            x = chart_x + (i / 5) * chart_w
            painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1, Qt.DotLine))
            painter.drawLine(int(x), int(chart_y), int(x), int(chart_y + len(self._measures) * self._row_height))

        for i, measure in enumerate(self._measures):
            y = chart_y + i * self._row_height + 6
            h = self._row_height - 12

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(4, int(y - 2), int(m["left"] - 8), int(h + 4), Qt.AlignRight | Qt.AlignVCenter, measure.get("name", ""))

            ranges = measure.get("ranges", [self._max * 0.6, self._max * 0.8, self._max])
            range_colors = [
                QColor(tm.color("bg_solid_tertiary")),
                QColor(tm.color("bg_solid_secondary")),
                QColor(tm.color("bg_subtle")),
            ]
            prev = 0
            for ri, rv in enumerate(ranges):
                x1 = chart_x + (prev / max_val) * chart_w
                x2 = chart_x + (rv / max_val) * chart_w
                rc = range_colors[ri % len(range_colors)]
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(rc))
                painter.drawRoundedRect(QRectF(x1, y, x2 - x1, h), 3, 3)
                prev = rv

            actual = measure.get("value", 0)
            bar_w = (actual / max_val) * chart_w * self._anim_progress
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(tm.color("primary"))))
            painter.drawRoundedRect(QRectF(chart_x, y + h / 4, bar_w, h / 2), 2, 2)

            target = measure.get("target", 0)
            if target > 0:
                tx = chart_x + (target / max_val) * chart_w
                painter.setPen(QPen(QColor(tm.color("accent_error")), 2))
                painter.drawLine(int(tx), int(y), int(tx), int(y + h))

            is_hovered = i == self._hovered
            if is_hovered:
                painter.setPen(QColor(tm.color("fg_primary")))
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.drawText(int(chart_x + bar_w + 6), int(y), 80, int(h), Qt.AlignVCenter | Qt.AlignLeft, f"{actual} / {target}")

        painter.end()

    def apply_theme(self):
        self.update()
