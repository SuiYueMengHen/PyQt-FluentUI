from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPixmap

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentImageViewer(QWidget, FluentWidgetBase):
    _scale = 1.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._pixmap: QPixmap = QPixmap()
        self._rotation = 0
        self._offset_x = 0
        self._offset_y = 0
        self._dragging = False
        self._drag_start = None
        self.setFixedSize(300, 240)

        self._scale_anim = QPropertyAnimation(self, b"scale")
        self._scale_anim.setDuration(200)
        self._scale_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, v):
        self._scale = v
        self.update()

    def set_image(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self._scale = 1.0
        self._rotation = 0
        self._offset_x = 0
        self._offset_y = 0
        self.update()

    def zoom_in(self):
        self._animate_scale(min(self._scale * 1.2, 5.0))

    def zoom_out(self):
        self._animate_scale(max(self._scale / 1.2, 0.1))

    def rotate(self):
        self._rotation = (self._rotation + 90) % 360
        self.update()

    def reset(self):
        self._animate_scale(1.0)
        self._rotation = 0
        self._offset_x = 0
        self._offset_y = 0
        self.update()

    def _animate_scale(self, target):
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(target)
        self._scale_anim.start()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        super().wheelEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_start = event.position()
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging and self._drag_start:
            dx = event.position().x() - self._drag_start.x()
            dy = event.position().y() - self._drag_start.y()
            self._offset_x += dx
            self._offset_y += dy
            self._drag_start = event.position()
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self._drag_start = None
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_secondary")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        cx = self.width() / 2 + self._offset_x
        cy = self.height() / 2 + self._offset_y

        painter.translate(cx, cy)
        painter.rotate(self._rotation)
        painter.scale(self._scale, self._scale)

        if self._pixmap.isNull():
            icon = get_icon("image", tm.color("fg_tertiary"), 48)
            painter.drawPixmap(-24, -24, icon.pixmap(48, 48))
            painter.resetTransform()
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(QRectF(0, self.height() - 40, self.width(), 24), Qt.AlignCenter, "暂无图片")
        else:
            scaled = self._pixmap.scaled(int(self.width() - 20), int(self.height() - 20), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(int(-scaled.width() / 2), int(-scaled.height() / 2), scaled)

        painter.resetTransform()

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_tertiary")))
        painter.drawText(QRectF(8, self.height() - 24, 100, 16), Qt.AlignLeft, f"{int(self._scale * 100)}%")

        painter.end()

    def apply_theme(self):
        self.update()
