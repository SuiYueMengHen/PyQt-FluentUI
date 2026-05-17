from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentNumericInput(QWidget, FluentWidgetBase):
    value_changed = Signal(float)
    _anim_value = 0.0

    def __init__(self, value: float = 0, step: float = 1, decimals: int = 0, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._value = value
        self._step = step
        self._decimals = decimals
        self._min = -999999
        self._max = 999999
        self.setFixedSize(140, 32)
        self.setCursor(Qt.PointingHandCursor)

        self._anim = QPropertyAnimation(self, b"anim_value")
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_range(self, min_val: float, max_val: float):
        self._min = min_val
        self._max = max_val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = max(self._min, min(self._max, v))
        self.value_changed.emit(self._value)
        self.update()

    @Property(float)
    def anim_value(self):
        return self._anim_value

    @anim_value.setter
    def anim_value(self, v):
        self._anim_value = v
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            btn_w = 28
            if event.position().x() <= btn_w:
                self._animate_to(self._value - self._step)
            elif event.position().x() >= self.width() - btn_w:
                self._animate_to(self._value + self._step)
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        delta = self._step if event.angleDelta().y() > 0 else -self._step
        self._animate_to(self._value + delta)
        super().wheelEvent(event)

    def _animate_to(self, target):
        target = max(self._min, min(self._max, target))
        self._anim.stop()
        self._anim.setStartValue(float(self._value))
        self._anim.setEndValue(float(target))
        self._anim.finished.connect(lambda: self._finish_anim(target))
        self._anim.start()

    def _finish_anim(self, target):
        self._value = target
        self.value_changed.emit(self._value)
        try:
            self._anim.finished.disconnect()
        except Exception:
            pass

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        border_color = QColor(tm.color("stroke_card"))
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 4, 4)

        btn_w = 28
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
        painter.drawRoundedRect(QRectF(0, 0, btn_w, self.height()), 4, 4)

        painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
        painter.drawRoundedRect(QRectF(self.width() - btn_w, 0, btn_w, self.height()), 4, 4)

        minus_icon = get_icon("minus", tm.color("fg_secondary"), 14)
        painter.drawPixmap(7, int((self.height() - 14) / 2), minus_icon.pixmap(14, 14))

        plus_icon = get_icon("plus", tm.color("fg_secondary"), 14)
        painter.drawPixmap(int(self.width() - btn_w + 7), int((self.height() - 14) / 2), plus_icon.pixmap(14, 14))

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        display_val = self._anim_value if self._anim.state() == QPropertyAnimation.Running else self._value
        if self._decimals > 0:
            text = f"{display_val:.{self._decimals}f}"
        else:
            text = f"{int(display_val)}"

        painter.drawText(QRectF(btn_w, 0, self.width() - 2 * btn_w, self.height()), Qt.AlignCenter, text)

        painter.end()

    def apply_theme(self):
        self.update()
