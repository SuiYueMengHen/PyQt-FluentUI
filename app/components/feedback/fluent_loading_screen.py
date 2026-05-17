from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentLoadingScreen(QWidget, FluentWidgetBase):
    _rotation = 0.0
    _pulse = 0.0

    def __init__(self, text: str = "加载中...", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._text = text
        self.setFixedSize(200, 200)

        self._rotate_anim = QPropertyAnimation(self, b"rotation")
        self._rotate_anim.setDuration(1000)
        self._rotate_anim.setStartValue(0.0)
        self._rotate_anim.setEndValue(360.0)
        self._rotate_anim.setLoopCount(-1)
        self._rotate_anim.setEasingCurve(QEasingCurve.Linear)

        self._pulse_anim = QPropertyAnimation(self, b"pulse")
        self._pulse_anim.setDuration(800)
        self._pulse_anim.setStartValue(0.0)
        self._pulse_anim.setEndValue(1.0)
        self._pulse_anim.setLoopCount(-1)
        self._pulse_anim.setEasingCurve(QEasingCurve.InOutSine)

    @Property(float)
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, v):
        self._rotation = v
        self.update()

    @Property(float)
    def pulse(self):
        return self._pulse

    @pulse.setter
    def pulse(self, v):
        self._pulse = v
        self.update()

    def start_loading(self):
        self._rotate_anim.start()
        self._pulse_anim.start()
        self.show()

    def stop_loading(self):
        self._rotate_anim.stop()
        self._pulse_anim.stop()
        self.hide()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        cx = self.width() / 2
        cy = self.height() / 2 - 16

        bg = QColor(tm.color("bg_solid_base"))
        bg.setAlpha(int(200 + 55 * self._pulse))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 12, 12)

        painter.translate(cx, cy)
        painter.rotate(self._rotation)

        r = 24
        pen_w = 3
        arc_len = 270

        painter.setPen(QPen(QColor(tm.color("primary")), pen_w, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(QRectF(-r, -r, r * 2, r * 2), 0, int(arc_len * 16))

        painter.setPen(QPen(QColor(tm.color("bg_solid_tertiary")), pen_w, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(QRectF(-r, -r, r * 2, r * 2), int(arc_len * 16), int((360 - arc_len) * 16))

        painter.rotate(-self._rotation)
        painter.translate(-cx, -cy)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(0, cy + 36, self.width(), 24), Qt.AlignCenter, self._text)

        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        alpha = int(128 + 127 * self._pulse)
        sub_color = QColor(tm.color("fg_tertiary"))
        sub_color.setAlpha(alpha)
        painter.setPen(sub_color)
        painter.drawText(QRectF(0, cy + 58, self.width(), 20), Qt.AlignCenter, "请稍候...")

        painter.end()

    def apply_theme(self):
        self.update()
