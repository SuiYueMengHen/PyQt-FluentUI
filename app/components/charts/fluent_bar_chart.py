from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentBarChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._series: list[dict] = []
        self._categories: list[str] = []
        self._bar_width = 24
        self._bar_gap = 8
        self._group_gap = 20
        self._margin = {"top": 30, "right": 20, "bottom": 40, "left": 50}
        self._hovered_bar = (-1, -1)
        self.setMinimumSize(300, 200)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, categories: list[str], series: list[dict]):
        self._categories = categories
        self._series = series
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
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91", "#008272", "#CA5010"]

    def mouseMoveEvent(self, event):
        self._hovered_bar = self._bar_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_bar = (-1, -1)
        self.update()
        super().leaveEvent(event)

    def _bar_at(self, pos):
        m = self._margin
        chart_x = m["left"]
        chart_y = m["top"]
        chart_w = self.width() - m["left"] - m["right"]
        chart_h = self.height() - m["top"] - m["bottom"]

        if not self._categories or not self._series:
            return (-1, -1)

        n_groups = len(self._categories)
        n_series = len(self._series)
        group_w = n_series * (self._bar_width + self._bar_gap) - self._bar_gap
        total_w = n_groups * group_w + (n_groups - 1) * self._group_gap
        start_x = chart_x + (chart_w - total_w) / 2

        for gi in range(n_groups):
            gx = start_x + gi * (group_w + self._group_gap)
            for si in range(n_series):
                bx = gx + si * (self._bar_width + self._bar_gap)
                if bx <= pos.x() <= bx + self._bar_width and chart_y <= pos.y() <= chart_y + chart_h:
                    return (gi, si)
        return (-1, -1)

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

        if not self._categories or not self._series:
            painter.end()
            return

        all_vals = [v for s in self._series for v in s.get("data", [])]
        max_val = max(all_vals) if all_vals else 1
        max_val = max(max_val, 1)

        painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1))
        for i in range(5):
            y = chart_y + chart_h - (i / 4) * chart_h
            painter.drawLine(int(chart_x), int(y), int(chart_x + chart_w), int(y))
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            val = max_val * i / 4
            painter.drawText(0, int(y - 6), int(chart_x - 6), 16, Qt.AlignRight | Qt.AlignVCenter, f"{val:.0f}")

        colors = self._chart_colors()
        n_groups = len(self._categories)
        n_series = len(self._series)
        group_w = n_series * (self._bar_width + self._bar_gap) - self._bar_gap
        total_w = n_groups * group_w + (n_groups - 1) * self._group_gap
        start_x = chart_x + (chart_w - total_w) / 2

        for gi in range(n_groups):
            gx = start_x + gi * (group_w + self._group_gap)

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(gx), int(chart_y + chart_h + 8), int(group_w), 24, Qt.AlignCenter, self._categories[gi])

            for si, series in enumerate(self._series):
                data = series.get("data", [])
                if gi >= len(data):
                    continue
                val = data[gi]
                bar_h = (val / max_val) * chart_h * self._anim_progress
                bx = gx + si * (self._bar_width + self._bar_gap)
                by = chart_y + chart_h - bar_h

                color = QColor(colors[si % len(colors)])
                is_hovered = self._hovered_bar == (gi, si)
                if is_hovered:
                    color = color.lighter(120)

                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                rect = QRectF(bx, by, self._bar_width, bar_h)
                painter.drawRoundedRect(rect, 3, 3)

                if is_hovered:
                    painter.setPen(QColor(tm.color("fg_primary")))
                    font.setPixelSize(tm.font_size("caption"))
                    painter.setFont(font)
                    painter.drawText(int(bx - 8), int(by - 18), int(self._bar_width + 16), 16, Qt.AlignCenter, f"{val}")

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        legend_x = chart_x
        legend_y = 4
        for si, series in enumerate(self._series):
            name = series.get("name", f"系列{si + 1}")
            color = QColor(colors[si % len(colors)])
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(legend_x, legend_y, 10, 10), 2, 2)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(legend_x + 14), int(legend_y + 10), name)
            legend_x += painter.fontMetrics().horizontalAdvance(name) + 28

        painter.end()

    def apply_theme(self):
        self.update()
