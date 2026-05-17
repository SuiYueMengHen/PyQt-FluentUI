from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentPopconfirm(QWidget, FluentWidgetBase):
    confirmed = Signal()
    cancelled = Signal()
    _scale = 0.0

    def __init__(self, title: str = "确认操作？", message: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._title = title
        self._message = message
        self.setFixedSize(260, 120)
        self.hide()

        self._scale_anim = QPropertyAnimation(self, b"scale")
        self._scale_anim.setDuration(200)
        self._scale_anim.setEasingCurve(QEasingCurve.OutCubic)

    def show_confirm(self, pos=None):
        if pos:
            self.move(pos)
        self.show()
        self._scale_anim.stop()
        self._scale_anim.setStartValue(0.8)
        self._scale_anim.setEndValue(1.0)
        self._scale_anim.start()

    def hide_confirm(self):
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(0.8)
        try:
            self._scale_anim.finished.disconnect(self.hide)
        except RuntimeError:
            pass
        self._scale_anim.finished.connect(self.hide)
        self._scale_anim.start()

    @Property(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, v):
        self._scale = v
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self._scale if self._scale > 0 else 1.0, self._scale if self._scale > 0 else 1.0)
        painter.translate(-self.width() / 2, -self.height() / 2)

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(16, 12, self.width() - 32, 24), Qt.AlignLeft, self._title)

        if self._message:
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(16, 38, self.width() - 32, 28), Qt.AlignLeft | Qt.TextWordWrap, self._message)

        btn_y = 78
        btn_h = 28
        cancel_rect = QRectF(self.width() - 170, btn_y, 72, btn_h)
        confirm_rect = QRectF(self.width() - 90, btn_y, 72, btn_h)

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
        painter.drawRoundedRect(cancel_rect, 4, 4)
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(cancel_rect, Qt.AlignCenter, "取消")

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("accent_error")))
        painter.drawRoundedRect(confirm_rect, 4, 4)
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(confirm_rect, Qt.AlignCenter, "确认")

        painter.restore()
        painter.end()

    def mousePressEvent(self, event):
        btn_y = 78
        btn_h = 28
        cancel_rect = QRectF(self.width() - 170, btn_y, 72, btn_h)
        confirm_rect = QRectF(self.width() - 90, btn_y, 72, btn_h)
        if cancel_rect.contains(event.position()):
            self.cancelled.emit()
            self.hide_confirm()
        elif confirm_rect.contains(event.position()):
            self.confirmed.emit()
            self.hide_confirm()
        super().mousePressEvent(event)

    def apply_theme(self):
        self.update()
