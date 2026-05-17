from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentTimePicker(QWidget, FluentWidgetBase):
    time_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._scroll_offset = 0.0
        self._animating_col = None
        self._scroll_anim = QPropertyAnimation(self, b"scroll_offset")
        self._scroll_anim.setDuration(200)
        self._scroll_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._hour = 12
        self._minute = 0
        self._second = 0
        self._dragging = None
        self._drag_start_y = 0
        self._drag_start_val = 0
        self.setFixedSize(200, 200)
        self.setCursor(Qt.PointingHandCursor)

    @Property(float)
    def scroll_offset(self):
        return self._scroll_offset

    @scroll_offset.setter
    def scroll_offset(self, value):
        self._scroll_offset = value
        self.update()

    def _start_scroll_animation(self, col, start_offset):
        self._animating_col = col
        self._scroll_anim.stop()
        self._scroll_offset = float(start_offset)
        self._scroll_anim.setStartValue(float(start_offset))
        self._scroll_anim.setEndValue(0.0)
        self._scroll_anim.start()

    def set_time(self, hour: int, minute: int, second: int = 0):
        self._hour = max(0, min(23, hour))
        self._minute = max(0, min(59, minute))
        self._second = max(0, min(59, second))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            col = self._column_at(event.position().x())
            if col is not None:
                self._dragging = col
                self._drag_start_y = event.position().y()
                if col == 0:
                    self._drag_start_val = self._hour
                elif col == 1:
                    self._drag_start_val = self._minute
                else:
                    self._drag_start_val = self._second
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging is not None:
            dy = self._drag_start_y - event.position().y()
            delta = int(dy / 20)
            fractional = (dy - delta * 20) / 20.0
            if self._dragging == 0:
                self._hour = max(0, min(23, self._drag_start_val + delta))
            elif self._dragging == 1:
                self._minute = max(0, min(59, self._drag_start_val + delta))
            else:
                self._second = max(0, min(59, self._drag_start_val + delta))
            self._animating_col = self._dragging
            self._scroll_offset = -fractional
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._dragging is not None:
            if abs(self._scroll_offset) > 0.01:
                self._start_scroll_animation(self._dragging, self._scroll_offset)
            else:
                self._animating_col = None
            self.time_changed.emit(f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}")
            self._dragging = None
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        col = self._column_at(event.position().x())
        if col is not None:
            delta = 1 if event.angleDelta().y() > 0 else -1
            old_vals = [self._hour, self._minute, self._second]
            if col == 0:
                self._hour = max(0, min(23, self._hour + delta))
            elif col == 1:
                self._minute = max(0, min(59, self._minute + delta))
            else:
                self._second = max(0, min(59, self._second + delta))
            new_vals = [self._hour, self._minute, self._second]
            if old_vals[col] != new_vals[col]:
                self._start_scroll_animation(col, delta)
            self.time_changed.emit(f"{self._hour:02d}:{self._minute:02d}:{self._second:02d}")
        super().wheelEvent(event)

    def _column_at(self, x):
        col_w = self.width() / 3
        if x < col_w:
            return 0
        elif x < col_w * 2:
            return 1
        elif x < col_w * 3:
            return 2
        return None

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bg_color = QColor(tm.color("bg_solid_card"))
        painter.fillRect(self.rect(), bg_color)

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(bg_color)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        col_w = self.width() / 3
        cy = self.height() / 2
        row_h = 36

        labels = ["时", "分", "秒"]
        values = [self._hour, self._minute, self._second]
        ranges = [24, 60, 60]

        for ci in range(3):
            cx = col_w * ci + col_w / 2

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(QRectF(col_w * ci, 8, col_w, 16), Qt.AlignCenter, labels[ci])

            scroll = self._scroll_offset if ci == self._animating_col else 0.0
            offsets = [-2, -1, 0, 1, 2] if ci == self._animating_col else [-1, 0, 1]

            for offset in offsets:
                val = (values[ci] + offset) % ranges[ci]
                y = cy + (offset + scroll) * row_h

                if y < -row_h or y > self.height() + row_h:
                    continue

                dist = abs(offset + scroll)
                alpha = max(0, int(255 * max(0, 1 - dist * 0.7)))
                is_center = dist < 0.5
                size = tm.font_size("title_large") if is_center else tm.font_size("body")
                weight = QFont.Bold if is_center else QFont.Normal

                font.setPixelSize(size)
                font.setWeight(weight)
                painter.setFont(font)
                color = QColor(tm.color("fg_primary") if is_center else tm.color("fg_tertiary"))
                color.setAlpha(alpha)
                painter.setPen(color)
                painter.drawText(QRectF(col_w * ci, y - row_h / 2, col_w, row_h), Qt.AlignCenter, f"{val:02d}")

            if ci < 2:
                sep_x = col_w * (ci + 1)
                font.setPixelSize(tm.font_size("title_large"))
                font.setWeight(QFont.Bold)
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(QRectF(sep_x - 10, cy - row_h / 2, 20, row_h), Qt.AlignCenter, ":")

        painter.setPen(Qt.NoPen)
        highlight = QColor(tm.color("primary"))
        highlight.setAlpha(20)
        painter.setBrush(QBrush(highlight))
        painter.drawRoundedRect(QRectF(4, cy - row_h / 2, self.width() - 8, row_h), 6, 6)

        painter.end()

    def apply_theme(self):
        self.update()
