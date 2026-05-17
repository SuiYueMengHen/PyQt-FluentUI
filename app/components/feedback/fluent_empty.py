from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentEmpty(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, title: str = "暂无数据", subtitle: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._title = title
        self._subtitle = subtitle
        self.setFixedSize(200, 160)

        self._anim = None
        QTimer.singleShot(50, self._start_anim)

    def _start_anim(self):
        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
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

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        cx = self.width() / 2
        cy = 50
        alpha = int(255 * self._anim_progress)

        box_color = QColor(tm.color("fg_tertiary"))
        box_color.setAlpha(alpha)
        painter.setPen(QPen(box_color, 2, Qt.DashLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(cx - 30, cy - 20, 60, 40), 6, 6)

        lid_color = QColor(tm.color("fg_tertiary"))
        lid_color.setAlpha(alpha)
        painter.setPen(QPen(lid_color, 2, Qt.DashLine))
        painter.drawLine(int(cx - 35), int(cy - 20), int(cx + 35), int(cy - 20))

        painter.setPen(Qt.NoPen)
        dot_color = QColor(tm.color("fg_tertiary"))
        dot_color.setAlpha(alpha)
        painter.setBrush(QBrush(dot_color))
        painter.drawEllipse(QRectF(cx - 3, cy - 28, 6, 6))

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        text_color = QColor(tm.color("fg_secondary"))
        text_color.setAlpha(alpha)
        painter.setPen(text_color)
        painter.drawText(QRectF(0, 90, self.width(), 24), Qt.AlignCenter, self._title)

        if self._subtitle:
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            sub_color = QColor(tm.color("fg_tertiary"))
            sub_color.setAlpha(alpha)
            painter.setPen(sub_color)
            painter.drawText(QRectF(0, 114, self.width(), 20), Qt.AlignCenter, self._subtitle)

        painter.end()

    def apply_theme(self):
        self.update()
