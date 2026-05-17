import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentLineChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._series: list[dict] = []
        self._categories: list[str] = []
        self._margin = {"top": 30, "right": 20, "bottom": 40, "left": 50}
        self._hovered_index = -1
        self.setMinimumSize(300, 200)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(800)
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
        m = self._margin
        chart_w = self.width() - m["left"] - m["right"]
        n = max(1, len(self._categories) - 1)
        step = chart_w / n
        idx = int(round((event.position().x() - m["left"]) / step))
        idx = max(0, min(idx, len(self._categories) - 1))
        if idx != self._hovered_index:
            self._hovered_index = idx
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
        m = self._margin
        cx, cy = m["left"], m["top"]
        cw = self.width() - m["left"] - m["right"]
        ch = self.height() - m["top"] - m["bottom"]

        if not self._categories or not self._series:
            painter.end()
            return

        all_vals = [v for s in self._series for v in s.get("data", [])]
        max_val = max(all_vals) if all_vals else 1
        min_val = min(all_vals) if all_vals else 0
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

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        n = len(self._categories)
        for i, cat in enumerate(self._categories):
            x = cx + (cw / max(1, n - 1)) * i if n > 1 else cx + cw / 2
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(x - 20), int(cy + ch + 8), 40, 24, Qt.AlignCenter, cat)

        colors = self._chart_colors()
        for si, series in enumerate(self._series):
            data = series.get("data", [])
            if len(data) < 2:
                continue
            color = QColor(colors[si % len(colors)])
            points = []
            for i, val in enumerate(data):
                x = cx + (cw / max(1, len(data) - 1)) * i
                y = cy + ch - ((val - min_val) / val_range) * ch
                points.append((x, y))

            visible = max(2, int(len(points) * self._anim_progress))
            vis_points = points[:visible]

            path = QPainterPath()
            path.moveTo(vis_points[0][0], vis_points[0][1])
            for i in range(1, len(vis_points)):
                if i < len(vis_points) - 1:
                    xc = (vis_points[i][0] + vis_points[i + 1][0]) / 2
                    yc = (vis_points[i][1] + vis_points[i + 1][1]) / 2
                    path.quadTo(vis_points[i][0], vis_points[i][1], xc, yc)
                else:
                    path.lineTo(vis_points[i][0], vis_points[i][1])

            painter.setPen(QPen(color, 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            for px, py in vis_points:
                painter.drawEllipse(QRectF(px - 3, py - 3, 6, 6))

        if 0 <= self._hovered_index < len(self._categories):
            hx = cx + (cw / max(1, n - 1)) * self._hovered_index if n > 1 else cx + cw / 2
            painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1, Qt.DashLine))
            painter.drawLine(int(hx), int(cy), int(hx), int(cy + ch))

            for si, series in enumerate(self._series):
                data = series.get("data", [])
                if self._hovered_index >= len(data):
                    continue
                val = data[self._hovered_index]
                hy = cy + ch - ((val - min_val) / val_range) * ch
                color = QColor(colors[si % len(colors)])
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawEllipse(QRectF(hx - 5, hy - 5, 10, 10))
                painter.setBrush(QColor(tm.color("bg_solid_card")))
                painter.drawEllipse(QRectF(hx - 3, hy - 3, 6, 6))

                tooltip = f"{series.get('name', '')}: {val}"
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                tw = painter.fontMetrics().horizontalAdvance(tooltip) + 12
                tr = QRectF(hx - tw / 2, hy - 26, tw, 20)
                painter.setBrush(QColor(tm.color("bg_solid_card")))
                painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
                painter.drawRoundedRect(tr, 4, 4)
                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(tr, Qt.AlignCenter, tooltip)

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        lx = cx
        for si, series in enumerate(self._series):
            name = series.get("name", f"系列{si + 1}")
            color = QColor(colors[si % len(colors)])
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(lx, 4, 10, 10), 2, 2)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(lx + 14), 14, name)
            lx += painter.fontMetrics().horizontalAdvance(name) + 28

        painter.end()

    def apply_theme(self):
        self.update()
