from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSplitPanel(QWidget, FluentWidgetBase):
    split_moved = Signal(int)

    def __init__(self, orientation: str = "horizontal", initial_ratio: float = 0.5, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._orientation = orientation
        self._ratio = initial_ratio
        self._dragging = False
        self._handle_size = 6
        self._hovered = False
        self._hover_progress = 0.0
        self._left_widget: QWidget | None = None
        self._right_widget: QWidget | None = None
        self.setMinimumSize(100, 100)

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, v):
        self._hover_progress = v
        self.update()

    def set_ratio(self, ratio: float):
        self._ratio = max(0.1, min(0.9, ratio))
        self._reposition_children()
        self.split_moved.emit(int(self._ratio * 100))
        self.update()

    @property
    def ratio(self):
        return self._ratio

    def set_left_widget(self, widget: QWidget):
        if self._left_widget:
            self._left_widget.setParent(None)
        self._left_widget = widget
        widget.setParent(self)
        self._reposition_children()

    def set_right_widget(self, widget: QWidget):
        if self._right_widget:
            self._right_widget.setParent(None)
        self._right_widget = widget
        widget.setParent(self)
        self._reposition_children()

    def _reposition_children(self):
        if self._orientation == "horizontal":
            handle_x = int(self.width() * self._ratio)
            left_w = handle_x - self._handle_size // 2
            right_x = handle_x + self._handle_size // 2
            right_w = self.width() - right_x
            if self._left_widget:
                self._left_widget.setGeometry(0, 0, max(left_w, 1), self.height())
            if self._right_widget:
                self._right_widget.setGeometry(right_x, 0, max(right_w, 1), self.height())
        else:
            handle_y = int(self.height() * self._ratio)
            top_h = handle_y - self._handle_size // 2
            bottom_y = handle_y + self._handle_size // 2
            bottom_h = self.height() - bottom_y
            if self._left_widget:
                self._left_widget.setGeometry(0, 0, self.width(), max(top_h, 1))
            if self._right_widget:
                self._right_widget.setGeometry(0, bottom_y, self.width(), max(bottom_h, 1))

    def enterEvent(self, event):
        self._hovered = True
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._is_on_handle(event.position()):
            self._dragging = True
            self.grabMouse()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._dragging:
            if self._orientation == "horizontal":
                self._ratio = max(0.1, min(0.9, event.position().x() / self.width()))
            else:
                self._ratio = max(0.1, min(0.9, event.position().y() / self.height()))
            self._reposition_children()
            self.split_moved.emit(int(self._ratio * 100))
            self.update()
        elif self._is_on_handle(event.position()):
            if self._orientation == "horizontal":
                self.setCursor(Qt.SplitHCursor)
            else:
                self.setCursor(Qt.SplitVCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._dragging:
            self._dragging = False
            self.releaseMouse()
        super().mouseReleaseEvent(event)

    def _is_on_handle(self, pos):
        if self._orientation == "horizontal":
            handle_x = self.width() * self._ratio
            return abs(pos.x() - handle_x) < self._handle_size
        else:
            handle_y = self.height() * self._ratio
            return abs(pos.y() - handle_y) < self._handle_size

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition_children()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if self._orientation == "horizontal":
            handle_x = int(self.width() * self._ratio)
            handle_rect = QRectF(handle_x - self._handle_size / 2, 0, self._handle_size, self.height())
        else:
            handle_y = int(self.height() * self._ratio)
            handle_rect = QRectF(0, handle_y - self._handle_size / 2, self.width(), self._handle_size)

        handle_color = QColor(tm.color("primary")) if self._hovered or self._dragging else QColor(tm.color("fg_tertiary"))
        handle_color.setAlpha(int(100 + 155 * self._hover_progress))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(handle_color))
        painter.drawRoundedRect(handle_rect, 3, 3)

        painter.end()

    def apply_theme(self):
        self.update()
