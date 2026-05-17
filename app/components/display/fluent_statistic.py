from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentStatistic(QWidget, FluentWidgetBase):
    _anim_value = 0.0

    def __init__(self, value: float = 0, title: str = "", prefix: str = "", suffix: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._title = title
        self._prefix = prefix
        self._suffix = suffix
        self._target = value
        self.setFixedSize(160, 80)

        self._value_anim = QPropertyAnimation(self, b"anim_value")
        self._value_anim.setDuration(1000)
        self._value_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._value_anim.setStartValue(0.0)
        self._value_anim.setEndValue(float(value))
        QTimer.singleShot(50, self._value_anim.start)

    @Property(float)
    def anim_value(self):
        return self._anim_value

    @anim_value.setter
    def anim_value(self, v):
        self._anim_value = v
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(QRectF(16, 10, self.width() - 32, 18), Qt.AlignLeft, self._title)

        font.setPixelSize(tm.font_size("title_large"))
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        val_text = f"{self._prefix}{int(self._anim_value):,}{self._suffix}"
        painter.drawText(QRectF(16, 32, self.width() - 32, 36), Qt.AlignLeft, val_text)

        painter.end()

    def apply_theme(self):
        self.update()
