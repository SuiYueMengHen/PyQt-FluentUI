from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentSteps(QWidget, FluentWidgetBase):
    currentChanged = Signal(int)
    _indicator_pos = 0.0

    def __init__(self, items: list = None, vertical: bool = False, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._items = items or []
        self._current = 0
        self._vertical = vertical
        self._step_size = 28
        self.setFixedHeight(60 if not vertical else max(len(self._items) * 60, 60))

        self._indicator_anim = QPropertyAnimation(self, b"indicator_pos")
        self._indicator_anim.setDuration(300)
        self._indicator_anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_current(self, index: int):
        if 0 <= index < len(self._items):
            self._current = index
            self._indicator_anim.stop()
            self._indicator_anim.setStartValue(self._indicator_pos)
            self._indicator_anim.setEndValue(float(index))
            self._indicator_anim.start()
            self.currentChanged.emit(index)

    @Property(float)
    def indicator_pos(self):
        return self._indicator_pos

    @indicator_pos.setter
    def indicator_pos(self, v):
        self._indicator_pos = v
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        n = len(self._items)
        if n == 0:
            painter.end()
            return

        step_w = self.width() / n if not self._vertical else self.width()
        step_h = 60 if self._vertical else self.height()

        for i, item in enumerate(self._items):
            text = item if isinstance(item, str) else item.get("text", "")
            desc = item.get("desc", "") if isinstance(item, dict) else ""

            if not self._vertical:
                cx = step_w * i + step_w / 2
                cy = self._step_size / 2 + 4
            else:
                cx = self._step_size / 2 + 4
                cy = step_h * i + step_h / 2

            if i < n - 1:
                if not self._vertical:
                    line_x1 = cx + self._step_size / 2 + 4
                    line_x2 = step_w * (i + 1) + step_w / 2 - self._step_size / 2 - 4
                    line_y = cy
                    color = QColor(tm.color("primary")) if i < self._current else QColor(tm.color("stroke_card"))
                    painter.setPen(QPen(color, 2))
                    painter.drawLine(int(line_x1), int(line_y), int(line_x2), int(line_y))
                else:
                    line_x = cx
                    line_y1 = cy + self._step_size / 2 + 4
                    line_y2 = step_h * (i + 1) + step_h / 2 - self._step_size / 2 - 4
                    color = QColor(tm.color("primary")) if i < self._current else QColor(tm.color("stroke_card"))
                    painter.setPen(QPen(color, 2))
                    painter.drawLine(int(line_x), int(line_y1), int(line_x), int(line_y2))

            if i < self._current:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(tm.color("primary"))))
                painter.drawEllipse(QRectF(cx - self._step_size / 2, cy - self._step_size / 2, self._step_size, self._step_size))
                check = get_icon("check", tm.color("primary_text_on"), 16)
                painter.drawPixmap(int(cx - 8), int(cy - 8), check.pixmap(16, 16))
            elif i == self._current:
                painter.setPen(QPen(QColor(tm.color("primary")), 2))
                painter.setBrush(QBrush(QColor(tm.color("primary_light"))))
                painter.drawEllipse(QRectF(cx - self._step_size / 2, cy - self._step_size / 2, self._step_size, self._step_size))
                font = QFont()
                font.setPixelSize(tm.font_size("body"))
                font.setWeight(QFont.Bold)
                painter.setFont(font)
                painter.setPen(QColor(tm.color("primary")))
                painter.drawText(QRectF(cx - self._step_size / 2, cy - self._step_size / 2, self._step_size, self._step_size), Qt.AlignCenter, str(i + 1))
            else:
                painter.setPen(QPen(QColor(tm.color("stroke_card")), 2))
                painter.setBrush(QBrush(QColor(tm.color("bg_solid_card"))))
                painter.drawEllipse(QRectF(cx - self._step_size / 2, cy - self._step_size / 2, self._step_size, self._step_size))
                font = QFont()
                font.setPixelSize(tm.font_size("body"))
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_tertiary")))
                painter.drawText(QRectF(cx - self._step_size / 2, cy - self._step_size / 2, self._step_size, self._step_size), Qt.AlignCenter, str(i + 1))

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.DemiBold if i <= self._current else QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("primary") if i <= self._current else tm.color("fg_tertiary")))

            if not self._vertical:
                painter.drawText(QRectF(step_w * i, cy + self._step_size / 2 + 4, step_w, 20), Qt.AlignCenter, text)
            else:
                painter.drawText(QRectF(cx + self._step_size / 2 + 8, cy - 10, self.width() - cx - self._step_size / 2 - 8, 20), Qt.AlignLeft | Qt.AlignVCenter, text)

        painter.end()

    def apply_theme(self):
        self.update()
