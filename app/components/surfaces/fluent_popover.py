from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygonF

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentPopover(QWidget, FluentWidgetBase):
    closed = Signal()
    _scale_progress = 0.0

    def __init__(self, title: str = "", content: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._title = title
        self._content = content
        self._arrow_side = "top"
        self.setFixedSize(240, 120)
        self.hide()

        self._scale_anim = QPropertyAnimation(self, b"scale_progress")
        self._scale_anim.setDuration(200)
        self._scale_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def scale_progress(self):
        return self._scale_progress

    @scale_progress.setter
    def scale_progress(self, v):
        self._scale_progress = v
        self.update()

    def show_popover(self, anchor_pos=None, arrow_side: str = "top"):
        self._arrow_side = arrow_side
        if anchor_pos:
            if arrow_side == "top":
                self.move(int(anchor_pos.x() - self.width() / 2), int(anchor_pos.y() + 10))
            elif arrow_side == "bottom":
                self.move(int(anchor_pos.x() - self.width() / 2), int(anchor_pos.y() - self.height() - 10))
            elif arrow_side == "left":
                self.move(int(anchor_pos.x() + 10), int(anchor_pos.y() - self.height() / 2))
            elif arrow_side == "right":
                self.move(int(anchor_pos.x() - self.width() - 10), int(anchor_pos.y() - self.height() / 2))
        self.show()
        self._scale_anim.stop()
        self._scale_anim.setStartValue(0.0)
        self._scale_anim.setEndValue(1.0)
        self._scale_anim.start()

    def hide_popover(self):
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale_progress)
        self._scale_anim.setEndValue(0.0)
        self._scale_anim.finished.connect(self._finish_hide)
        self._scale_anim.start()

    def _finish_hide(self):
        self.hide()
        self.closed.emit()
        try:
            self._scale_anim.finished.disconnect()
        except Exception:
            pass

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        s = self._scale_progress
        cx = self.width() / 2
        cy = self.height() / 2
        painter.translate(cx, cy)
        painter.scale(s, s)
        painter.translate(-cx, -cy)

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(4, 4, self.width() - 8, self.height() - 8), 8, 8)

        arrow_size = 8
        if self._arrow_side == "top":
            arrow = QPolygonF([QPointF(cx - arrow_size, 4), QPointF(cx, -4), QPointF(cx + arrow_size, 4)])
        elif self._arrow_side == "bottom":
            arrow = QPolygonF([QPointF(cx - arrow_size, self.height() - 4), QPointF(cx, self.height() + 4), QPointF(cx + arrow_size, self.height() - 4)])
        elif self._arrow_side == "left":
            arrow = QPolygonF([QPointF(4, cy - arrow_size), QPointF(-4, cy), QPointF(4, cy + arrow_size)])
        else:
            arrow = QPolygonF([QPointF(self.width() - 4, cy - arrow_size), QPointF(self.width() + 4, cy), QPointF(self.width() - 4, cy + arrow_size)])
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawPolygon(arrow)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(16, 16, self.width() - 32, 24), Qt.AlignLeft, self._title)

        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(QRectF(16, 44, self.width() - 32, self.height() - 60), Qt.AlignLeft | Qt.TextWordWrap, self._content)

        painter.end()

    def apply_theme(self):
        self.update()
