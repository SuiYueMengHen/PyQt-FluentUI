from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentFlipCard(QWidget, FluentWidgetBase):
    clicked = Signal()
    _flip_progress = 0.0

    def __init__(self, front_text: str = "正面", back_text: str = "背面", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._front_text = front_text
        self._back_text = back_text
        self._is_flipped = False
        self.setFixedSize(200, 140)
        self.setCursor(Qt.PointingHandCursor)

        self._flip_anim = QPropertyAnimation(self, b"flip_progress")
        self._flip_anim.setDuration(400)
        self._flip_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def flip_progress(self):
        return self._flip_progress

    @flip_progress.setter
    def flip_progress(self, v):
        self._flip_progress = v
        self.update()

    def flip(self):
        self._flip_anim.stop()
        self._flip_anim.setStartValue(self._flip_progress)
        self._flip_anim.setEndValue(1.0 if not self._is_flipped else 0.0)
        self._flip_anim.start()
        self._is_flipped = not self._is_flipped

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.flip()
            self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        cx = self.width() / 2
        cy = self.height() / 2

        progress = self._flip_progress
        if progress <= 0.5:
            scale_x = 1.0 - progress * 2
            is_front = True
        else:
            scale_x = (progress - 0.5) * 2
            is_front = False

        painter.translate(cx, cy)
        painter.scale(max(scale_x, 0.01), 1.0)
        painter.translate(-cx, -cy)

        if is_front:
            bg = QColor(tm.color("bg_solid_card"))
            fg = QColor(tm.color("fg_primary"))
            text = self._front_text
            border = QColor(tm.color("stroke_card"))
        else:
            bg = QColor(tm.color("primary"))
            fg = QColor(tm.color("primary_text_on"))
            text = self._back_text
            border = QColor(tm.color("primary"))

        painter.setPen(QPen(border, 1))
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 10, 10)

        font = QFont()
        font.setPixelSize(tm.font_size("title_medium"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(fg)
        painter.drawText(QRectF(0, 0, self.width(), self.height()), Qt.AlignCenter, text)

        painter.end()

    def apply_theme(self):
        self.update()
