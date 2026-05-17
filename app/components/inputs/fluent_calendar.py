import math
from datetime import date, timedelta

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentCalendar(QWidget, FluentWidgetBase):
    dateSelected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_year = date.today().year
        self._current_month = date.today().month
        self._selected_date = None
        self._hovered_day = -1
        self.setFixedSize(320, 320)
        self.setCursor(Qt.PointingHandCursor)

        self._nav_bar = QWidget(self)
        self._nav_bar.setFixedHeight(40)
        nav_layout = QHBoxLayout(self._nav_bar)
        nav_layout.setContentsMargins(8, 4, 8, 4)
        nav_layout.setSpacing(4)

        self._prev_btn = QPushButton()
        self._prev_btn.setFixedSize(28, 28)
        self._prev_btn.setCursor(Qt.PointingHandCursor)
        self._prev_btn.clicked.connect(self._prev_month)
        nav_layout.addWidget(self._prev_btn)

        self._month_label = QLabel()
        self._month_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(self._month_label, 1)

        self._next_btn = QPushButton()
        self._next_btn.setFixedSize(28, 28)
        self._next_btn.setCursor(Qt.PointingHandCursor)
        self._next_btn.clicked.connect(self._next_month)
        nav_layout.addWidget(self._next_btn)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self._nav_bar)

        self._update_month_label()
        self._init_fluent_base()

    def _prev_month(self):
        if self._current_month == 1:
            self._current_month = 12
            self._current_year -= 1
        else:
            self._current_month -= 1
        self._update_month_label()
        self.update()

    def _next_month(self):
        if self._current_month == 12:
            self._current_month = 1
            self._current_year += 1
        else:
            self._current_month += 1
        self._update_month_label()
        self.update()

    def _update_month_label(self):
        month_names = [
            "", "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        self._month_label.setText(f"{month_names[self._current_month]} {self._current_year}")

    def _days_in_month(self, year, month):
        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            return 28
        if month in (4, 6, 9, 11):
            return 30
        return 31

    def _first_day_of_month(self, year, month):
        d = date(year, month, 1)
        return d.weekday()

    def _day_at(self, pos) -> int:
        grid_x = pos.x()
        grid_y = pos.y()
        nav_h = 40
        weekday_h = 28
        grid_top = nav_h + weekday_h

        if grid_y < grid_top:
            return -1

        cell_w = self.width() / 7
        cell_h = (self.height() - grid_top) / 6

        col = int(grid_x / cell_w)
        row = int((grid_y - grid_top) / cell_h)

        first_day = self._first_day_of_month(self._current_year, self._current_month)
        day_index = row * 7 + col - first_day + 1

        days = self._days_in_month(self._current_year, self._current_month)
        if 1 <= day_index <= days:
            return day_index
        return -1

    def mouseMoveEvent(self, event):
        day = self._day_at(event.position())
        if day != self._hovered_day:
            self._hovered_day = day
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            day = self._day_at(event.position())
            if day > 0:
                self._selected_date = date(self._current_year, self._current_month, day)
                self.dateSelected.emit(self._selected_date)
                self.update()
        super().mousePressEvent(event)

    def leaveEvent(self, event):
        self._hovered_day = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color("bg_solid_card")))

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.NoBrush)

        nav_h = 40
        weekday_h = 28
        grid_top = nav_h + weekday_h
        cell_w = self.width() / 7
        cell_h = (self.height() - grid_top) / 6

        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)

        for i, name in enumerate(weekdays):
            rect = QRectF(i * cell_w, nav_h, cell_w, weekday_h)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(rect, Qt.AlignCenter, name)

        first_day = self._first_day_of_month(self._current_year, self._current_month)
        days = self._days_in_month(self._current_year, self._current_month)
        today = date.today()

        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        for day in range(1, days + 1):
            idx = first_day + day - 1
            row = idx // 7
            col = idx % 7
            x = col * cell_w
            y = grid_top + row * cell_h
            cell_rect = QRectF(x, y, cell_w, cell_h)
            center = cell_rect.center()
            radius = min(cell_w, cell_h) / 2 - 2

            is_today = (self._current_year == today.year and self._current_month == today.month and day == today.day)
            is_selected = (self._selected_date and self._selected_date.year == self._current_year and self._selected_date.month == self._current_month and self._selected_date.day == day)
            is_hovered = (day == self._hovered_day)

            if is_selected:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(tm.color("primary")))
                painter.drawEllipse(center, radius, radius)
                painter.setPen(QColor(tm.color("primary_text_on")))
            elif is_hovered:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
                painter.drawEllipse(center, radius, radius)
                painter.setPen(QColor(tm.color("fg_primary")))
            else:
                painter.setPen(QColor(tm.color("fg_primary")))

            text_rect = QRectF(x, y, cell_w, cell_h)
            painter.drawText(text_rect, Qt.AlignCenter, str(day))

            if is_today and not is_selected:
                indicator_y = y + cell_h - 6
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(tm.color("primary")))
                painter.drawEllipse(center.x() - 2, indicator_y, 4, 4)

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background: {tm.color('bg_solid_card')};")
        self._nav_bar.setStyleSheet(f"background: {tm.color('bg_solid_card')};")
        self._month_label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_small')}px; font-weight: 600; background: transparent;")
        btn_style = f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('bg_solid_tertiary')};
            }}
        """
        self._prev_btn.setStyleSheet(btn_style)
        self._next_btn.setStyleSheet(btn_style)
        self._prev_btn.setIcon(get_icon("chevron_left", tm.color("fg_secondary"), 16))
        self._next_btn.setIcon(get_icon("chevron_right", tm.color("fg_secondary"), 16))
        self.update()
