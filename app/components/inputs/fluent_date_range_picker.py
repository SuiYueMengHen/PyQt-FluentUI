from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QDate
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentDateRangePicker(QWidget, FluentWidgetBase):
    range_changed = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._start_date = QDate.currentDate().addDays(-7)
        self._end_date = QDate.currentDate()
        self._hovered_day = (-1, -1)
        self._selecting_start = True
        self.setFixedSize(320, 300)
        self.setCursor(Qt.PointingHandCursor)

    def set_range(self, start: QDate, end: QDate):
        self._start_date = start
        self._end_date = end
        self.update()

    @Property(bool)
    def selecting_start(self):
        return self._selecting_start

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            day = self._day_at(event.position())
            if day is not None:
                ref = self._start_date if self._selecting_start else self._end_date
                clicked = QDate(ref.year(), ref.month(), day)
                if clicked.isValid():
                    if self._selecting_start:
                        self._start_date = clicked
                        self._selecting_start = False
                    else:
                        self._end_date = clicked
                        self._selecting_start = True
                        if self._end_date < self._start_date:
                            self._start_date, self._end_date = self._end_date, self._start_date
                        self.range_changed.emit(self._start_date.toString("yyyy-MM-dd"), self._end_date.toString("yyyy-MM-dd"))
                    self.update()
        super().mousePressEvent(event)

    def _day_at(self, pos):
        m = 16
        header_h = 36
        weekday_h = 24
        grid_top = header_h + weekday_h
        cell_w = (self.width() - 2 * m) / 7
        cell_h = 28

        col = int((pos.x() - m) / cell_w)
        row = int((pos.y() - grid_top) / cell_h)

        if 0 <= col < 7 and 0 <= row < 6:
            ref = self._start_date if self._selecting_start else self._end_date
            first_day = QDate(ref.year(), ref.month(), 1).dayOfWeek()
            first_weekday_offset = first_day - 1
            day = row * 7 + col - first_weekday_offset + 1
            days_in_month = ref.daysInMonth()
            if 1 <= day <= days_in_month:
                return day
        return None

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color("bg_solid_card")))

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        m = 16
        header_h = 36
        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        ref = self._start_date if self._selecting_start else self._end_date
        painter.drawText(QRectF(m, 8, self.width() - 2 * m, 24), Qt.AlignCenter, f"{ref.year()}年{ref.month()}月")

        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        cell_w = (self.width() - 2 * m) / 7
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        for i, wd in enumerate(weekdays):
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(QRectF(m + i * cell_w, header_h, cell_w, 24), Qt.AlignCenter, wd)

        cell_h = 28
        days_in_month = ref.daysInMonth()
        first_day = QDate(ref.year(), ref.month(), 1).dayOfWeek()
        start_col = first_day - 1

        for day in range(1, days_in_month + 1):
            idx = start_col + day - 1
            row = idx // 7
            col = idx % 7
            x = m + col * cell_w
            y = header_h + 24 + row * cell_h

            is_start = QDate(ref.year(), ref.month(), day) == self._start_date
            is_end = QDate(ref.year(), ref.month(), day) == self._end_date
            in_range = self._start_date <= QDate(ref.year(), ref.month(), day) <= self._end_date

            if is_start or is_end:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(tm.color("primary"))))
                painter.drawRoundedRect(QRectF(x + 2, y + 2, cell_w - 4, cell_h - 4), 4, 4)
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.setPen(QColor(tm.color("primary_text_on")))
                painter.drawText(QRectF(x, y, cell_w, cell_h), Qt.AlignCenter, str(day))
            elif in_range:
                painter.setPen(Qt.NoPen)
                bg = QColor(tm.color("primary_light"))
                bg.setAlpha(80)
                painter.setBrush(QBrush(bg))
                painter.drawRoundedRect(QRectF(x + 2, y + 2, cell_w - 4, cell_h - 4), 4, 4)
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(QRectF(x, y, cell_w, cell_h), Qt.AlignCenter, str(day))
            else:
                font.setPixelSize(tm.font_size("caption"))
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(QRectF(x, y, cell_w, cell_h), Qt.AlignCenter, str(day))

        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(QRectF(m, self.height() - 28, self.width() - 2 * m, 20), Qt.AlignCenter,
                         f"{self._start_date.toString('yyyy-MM-dd')} ~ {self._end_date.toString('yyyy-MM-dd')}")

        painter.end()

    def apply_theme(self):
        self.update()
