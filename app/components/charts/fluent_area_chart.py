from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath, QLinearGradient

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentAreaChart(QWidget, FluentWidgetBase):
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
        return ["#0078D4", "#107C10", "#D83B01", "#5C2D91"]

    def mouseMoveEvent(self, event):
        m = self._margin
        cw = self.width() - m["left"] - m["right"]
        n = max(1, len(self._categories) - 1)
        step = cw / n
        idx = int(round((event.position().x() - m["left"]) / step))
        self._hovered_index = max(0, min(idx, len(self._categories) - 1))
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
        min_val = min(min(all_vals) if all_vals else 0, 0)
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
            vis = points[:visible]

            line_path = QPainterPath()
            line_path.moveTo(vis[0][0], vis[0][1])
            for i in range(1, len(vis)):
                line_path.lineTo(vis[i][0], vis[i][1])

            fill_path = QPainterPath(line_path)
            fill_path.lineTo(vis[-1][0], cy + ch)
            fill_path.lineTo(vis[0][0], cy + ch)
            fill_path.closeSubpath()

            gradient = QLinearGradient(0, cy, 0, cy + ch)
            fill_color = QColor(color)
            fill_color.setAlpha(50)
            gradient.setColorAt(0, fill_color)
            fill_color.setAlpha(5)
            gradient.setColorAt(1, fill_color)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(gradient))
            painter.drawPath(fill_path)

            painter.setPen(QPen(color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(line_path)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            for px, py in vis:
                painter.drawEllipse(QRectF(px - 3, py - 3, 6, 6))

        if 0 <= self._hovered_index < len(self._categories):
            hx = cx + (cw / max(1, len(self._categories) - 1)) * self._hovered_index
            painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1, Qt.DashLine))
            painter.drawLine(int(hx), int(cy), int(hx), int(cy + ch))

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
