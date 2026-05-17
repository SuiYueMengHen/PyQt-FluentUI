import random
from datetime import date, timedelta

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentCalendarHeatmap(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._data: dict[str, int] = {}
        self._max_val = 1
        self._hovered_day = ""
        self.setFixedSize(780, 140)

        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def anim_progress(self):
        return self._anim_progress

    @anim_progress.setter
    def anim_progress(self, v):
        self._anim_progress = v
        self.update()

    def set_data(self, data: dict[str, int]):
        self._data = data
        self._max_val = max(data.values()) if data else 1
        self._max_val = max(self._max_val, 1)
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def generate_sample_data(self):
        today = date.today()
        start = today - timedelta(days=364)
        data = {}
        for i in range(365):
            d = start + timedelta(days=i)
            val = random.choices([0, 1, 2, 3, 4], weights=[30, 25, 20, 15, 10])[0]
            if val > 0:
                data[d.isoformat()] = val
        self.set_data(data)

    def mouseMoveEvent(self, event):
        self._hovered_day = self._day_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_day = ""
        self.update()
        super().leaveEvent(event)

    def _day_at(self, pos):
        m_left = 32
        m_top = 24
        cell = 13
        gap = 3
        col = int((pos.x() - m_left) / (cell + gap))
        row = int((pos.y() - m_top) / (cell + gap))
        if 0 <= row < 7 and 0 <= col < 53:
            today = date.today()
            start = date(today.year - 1, today.month, today.day)
            d = start + timedelta(weeks=col, days=row)
            return d.isoformat()
        return ""

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        m_left = 32
        m_top = 24
        cell = 13
        gap = 3

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_tertiary")))

        weekdays = ["一", "", "三", "", "五", "", "日"]
        for i, wd in enumerate(weekdays):
            if wd:
                painter.drawText(QRectF(0, m_top + i * (cell + gap), m_left - 4, cell), Qt.AlignRight | Qt.AlignVCenter, wd)

        months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
        today = date.today()
        start = date(today.year - 1, today.month, today.day)
        prev_month = -1
        for col in range(53):
            d = start + timedelta(weeks=col)
            if d.month != prev_month:
                painter.setPen(QColor(tm.color("fg_tertiary")))
                painter.drawText(int(m_left + col * (cell + gap)), 16, months[d.month - 1])
                prev_month = d.month

        for col in range(53):
            for row in range(7):
                d = start + timedelta(weeks=col, days=row)
                if d > today:
                    continue
                key = d.isoformat()
                val = self._data.get(key, 0)
                x = m_left + col * (cell + gap)
                y = m_top + row * (cell + gap)

                if val == 0:
                    bg = QColor(tm.color("bg_solid_tertiary"))
                    bg.setAlpha(int(80 * self._anim_progress))
                else:
                    intensity = val / self._max_val
                    bg = QColor(tm.color("primary"))
                    bg.setAlpha(int((60 + 195 * intensity) * self._anim_progress))

                is_hovered = key == self._hovered_day
                if is_hovered:
                    bg = bg.lighter(140)

                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(bg))
                painter.drawRoundedRect(QRectF(x, y, cell, cell), 2, 2)

                if is_hovered:
                    painter.setPen(QColor(tm.color("fg_primary")))
                    font.setPixelSize(tm.font_size("caption"))
                    painter.setFont(font)
                    painter.drawText(int(x - 20), int(y - 12), 80, 16, Qt.AlignCenter, f"{key}: {val}")

        levels = ["少", "中", "多", "很多"]
        legend_x = self.width() - 200
        legend_y = self.height() - 16
        painter.setPen(QColor(tm.color("fg_tertiary")))
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.drawText(int(legend_x), int(legend_y + 4), "少")
        legend_x += 20
        for i, alpha in enumerate([60, 120, 180, 240]):
            c = QColor(tm.color("primary"))
            c.setAlpha(alpha)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(c))
            painter.drawRoundedRect(QRectF(legend_x, legend_y, cell, cell), 2, 2)
            legend_x += cell + 4
        painter.setPen(QColor(tm.color("fg_tertiary")))
        painter.drawText(int(legend_x), int(legend_y + 4), "多")

        painter.end()

    def apply_theme(self):
        self.update()
