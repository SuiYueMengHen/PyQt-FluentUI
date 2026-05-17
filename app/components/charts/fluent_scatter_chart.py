from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentScatterChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._series: list[dict] = []
        self._margin = {"top": 30, "right": 20, "bottom": 40, "left": 50}
        self._hovered_point = (-1, -1)
        self.setMinimumSize(300, 200)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_data(self, series: list[dict]):
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
        ch = self.height() - m["top"] - m["bottom"]

        all_x = [p[0] for s in self._series for p in s.get("data", [])]
        all_y = [p[1] for s in self._series for p in s.get("data", [])]
        if not all_x or not all_y:
            return super().mouseMoveEvent(event)

        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        x_range = x_max - x_min if x_max != x_min else 1
        y_range = y_max - y_min if y_max != y_min else 1

        best = (-1, -1)
        best_dist = 20
        for si, series in enumerate(self._series):
            for pi, point in enumerate(series.get("data", [])):
                px = m["left"] + ((point[0] - x_min) / x_range) * cw
                py = m["top"] + ch - ((point[1] - y_min) / y_range) * ch
                dist = ((event.position().x() - px) ** 2 + (event.position().y() - py) ** 2) ** 0.5
                if dist < best_dist:
                    best_dist = dist
                    best = (si, pi)

        self._hovered_point = best
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_point = (-1, -1)
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

        all_x = [p[0] for s in self._series for p in s.get("data", [])]
        all_y = [p[1] for s in self._series for p in s.get("data", [])]
        if not all_x or not all_y:
            painter.end()
            return

        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        x_range = x_max - x_min if x_max != x_min else 1
        y_range = y_max - y_min if y_max != y_min else 1

        painter.setPen(QPen(QColor(tm.color("fg_tertiary")), 1))
        for i in range(5):
            y = cy + ch - (i / 4) * ch
            painter.drawLine(int(cx), int(y), int(cx + cw), int(y))
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            val = y_min + y_range * i / 4
            painter.drawText(0, int(y - 6), int(cx - 6), 16, Qt.AlignRight | Qt.AlignVCenter, f"{val:.0f}")

        colors = self._chart_colors()
        for si, series in enumerate(self._series):
            color = QColor(colors[si % len(colors)])
            for pi, point in enumerate(series.get("data", [])):
                px = cx + ((point[0] - x_min) / x_range) * cw
                py = cy + ch - ((point[1] - y_min) / y_range) * ch
                r = 5 * self._anim_progress
                is_hovered = self._hovered_point == (si, pi)

                if is_hovered:
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QColor(color.red(), color.green(), color.blue(), 40))
                    painter.drawEllipse(QRectF(px - 12, py - 12, 24, 24))

                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color.lighter(115) if is_hovered else color))
                painter.drawEllipse(QRectF(px - r, py - r, r * 2, r * 2))

                if is_hovered:
                    font = QFont()
                    font.setPixelSize(tm.font_size("caption"))
                    painter.setFont(font)
                    tooltip = f"({point[0]:.1f}, {point[1]:.1f})"
                    tw = painter.fontMetrics().horizontalAdvance(tooltip) + 12
                    tr = QRectF(px - tw / 2, py - 28, tw, 20)
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
            painter.drawEllipse(QRectF(lx + 2, 6, 8, 8))
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(int(lx + 14), 14, name)
            lx += painter.fontMetrics().horizontalAdvance(name) + 28

        painter.end()

    def apply_theme(self):
        self.update()
