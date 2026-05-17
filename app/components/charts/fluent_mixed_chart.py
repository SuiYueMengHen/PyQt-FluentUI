from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentMixedChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._categories: list[str] = []
        self._bar_series: list[dict] = []
        self._line_series: list[dict] = []
        self._bar_width = 28
        self._bar_gap = 8
        self._group_gap = 20
        self._margin = {"top": 30, "right": 50, "bottom": 40, "left": 50}
        self._hovered = (-1, -1, "")
        self.setMinimumSize(400, 250)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, categories: list[str], bar_series: list[dict], line_series: list[dict]):
        self._categories = categories
        self._bar_series = bar_series
        self._line_series = line_series
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

    def _bar_colors(self):
        return ["#0078D4", "#107C10", "#D83B01"]

    def _line_colors(self):
        return ["#CA5010", "#5C2D91", "#008272"]

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

        if not self._categories:
            painter.end()
            return

        bar_max = 1
        for s in self._bar_series:
            for v in s.get("data", []):
                bar_max = max(bar_max, v)

        line_max = 1
        for s in self._line_series:
            for v in s.get("data", []):
                line_max = max(line_max, v)

        painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1))
        for i in range(5):
            y = chart_y + chart_h - (i / 4) * chart_h
            painter.drawLine(int(chart_x), int(y), int(chart_x + chart_w), int(y))
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            val = bar_max * i / 4
            painter.drawText(0, int(y - 6), int(chart_x - 6), 16, Qt.AlignRight | Qt.AlignVCenter, f"{val:.0f}")

        for i in range(5):
            y = chart_y + chart_h - (i / 4) * chart_h
            val = line_max * i / 4
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(int(chart_x + chart_w + 6), int(y - 6), int(m["right"] - 6), 16, Qt.AlignLeft | Qt.AlignVCenter, f"{val:.0f}")

        n_groups = len(self._categories)
        n_bar_series = len(self._bar_series)
        group_w = n_bar_series * (self._bar_width + self._bar_gap) - self._bar_gap if n_bar_series > 0 else 0
        total_w = n_groups * group_w + (n_groups - 1) * self._group_gap
        start_x = chart_x + (chart_w - total_w) / 2

        bar_colors = self._bar_colors()
        for gi in range(n_groups):
            gx = start_x + gi * (group_w + self._group_gap)
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(gx), int(chart_y + chart_h + 8), int(group_w), 24, Qt.AlignCenter, self._categories[gi])

            for si, series in enumerate(self._bar_series):
                data = series.get("data", [])
                if gi >= len(data):
                    continue
                val = data[gi]
                bar_h = (val / bar_max) * chart_h * self._anim_progress
                bx = gx + si * (self._bar_width + self._bar_gap)
                by = chart_y + chart_h - bar_h
                color = QColor(bar_colors[si % len(bar_colors)])
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawRoundedRect(QRectF(bx, by, self._bar_width, bar_h), 3, 3)

        line_colors = self._line_colors()
        for si, series in enumerate(self._line_series):
            data = series.get("data", [])
            if not data:
                continue
            color = QColor(line_colors[si % len(line_colors)])
            path = QPainterPath()
            points = []
            for di, val in enumerate(data):
                if di >= n_groups:
                    break
                x = start_x + di * (group_w + self._group_gap) + group_w / 2
                y = chart_y + chart_h - (val / line_max) * chart_h * self._anim_progress
                points.append((x, y))
            if points:
                path.moveTo(points[0][0], points[0][1])
                for px, py in points[1:]:
                    path.lineTo(px, py)
                painter.setPen(QPen(color, 2))
                painter.setBrush(Qt.NoBrush)
                painter.drawPath(path)
                for px, py in points:
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QBrush(color))
                    painter.drawEllipse(QRectF(px - 3, py - 3, 6, 6))

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        legend_x = chart_x
        legend_y = 4
        for si, series in enumerate(self._bar_series):
            name = series.get("name", f"柱{si + 1}")
            color = QColor(bar_colors[si % len(bar_colors)])
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(legend_x, legend_y, 10, 10), 2, 2)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(legend_x + 14), int(legend_y + 10), name)
            legend_x += painter.fontMetrics().horizontalAdvance(name) + 28
        for si, series in enumerate(self._line_series):
            name = series.get("name", f"线{si + 1}")
            color = QColor(line_colors[si % len(line_colors)])
            painter.setPen(QPen(color, 2))
            painter.drawLine(int(legend_x), int(legend_y + 5), int(legend_x + 10), int(legend_y + 5))
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(legend_x + 14), int(legend_y + 10), name)
            legend_x += painter.fontMetrics().horizontalAdvance(name) + 28

        painter.end()

    def apply_theme(self):
        self.update()
