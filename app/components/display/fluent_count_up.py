from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentCountUp(QWidget, FluentWidgetBase):
    _current_display = 0.0

    def __init__(self, end_value: float = 0, start_value: float = 0,
                 decimals: int = 0, prefix: str = "", suffix: str = "",
                 label: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._start_value = start_value
        self._end_value = end_value
        self._decimals = decimals
        self._prefix = prefix
        self._suffix = suffix
        self._label = label
        self._current_display = start_value
        self.setFixedSize(140, 70)

        self._count_anim = QPropertyAnimation(self, b"current_display")
        self._count_anim.setDuration(1200)
        self._count_anim.setEasingCurve(QEasingCurve.OutCubic)

    def start(self):
        self._count_anim.stop()
        self._count_anim.setStartValue(self._start_value)
        self._count_anim.setEndValue(self._end_value)
        self._count_anim.start()

    def set_value(self, end_value: float, start_value: float = None):
        if start_value is not None:
            self._start_value = start_value
        else:
            self._start_value = self._current_display
        self._end_value = end_value
        self.start()

    @Property(float)
    def current_display(self):
        return self._current_display

    @current_display.setter
    def current_display(self, value):
        self._current_display = value
        self.update()

    def _format_number(self, val: float) -> str:
        if self._decimals == 0:
            int_val = int(round(val))
            parts = []
            s = str(abs(int_val))
            for i, c in enumerate(reversed(s)):
                if i > 0 and i % 3 == 0:
                    parts.append(",")
                parts.append(c)
            formatted = "".join(reversed(parts))
            if int_val < 0:
                formatted = "-" + formatted
            return self._prefix + formatted + self._suffix
        else:
            formatted = f"{val:,.{self._decimals}f}"
            return self._prefix + formatted + self._suffix

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        text = self._format_number(self._current_display)

        font = QFont()
        font.setPixelSize(tm.font_size("display"))
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(0, 0, self.width(), self.height() * 0.65),
                         Qt.AlignCenter, text)

        if self._label:
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(0, self.height() * 0.6, self.width(), self.height() * 0.4),
                             Qt.AlignCenter, self._label)

        painter.end()

    def apply_theme(self):
        self.update()
