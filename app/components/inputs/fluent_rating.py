from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentRating(QWidget, FluentWidgetBase):
    valueChanged = Signal(float)

    _hover_star = 0.0
    _selected_star = 0.0

    def __init__(self, max_stars: int = 5, half_star: bool = True, read_only: bool = False, parent=None):
        super().__init__(parent)
        self._max_stars = max_stars
        self._half_star = half_star
        self._read_only = read_only
        self._star_size = 24
        self._spacing = 4
        self.setFixedHeight(self._star_size + 8)
        self.setMinimumWidth(max_stars * (self._star_size + self._spacing) + 8)
        if not read_only:
            self.setCursor(Qt.PointingHandCursor)

        self._hover_anim = QPropertyAnimation(self, b"hover_star")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._selected_anim = QPropertyAnimation(self, b"selected_star")
        self._selected_anim.setDuration(200)
        self._selected_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._init_fluent_base()
    @Property(float)
    def hover_star(self):
        return self._hover_star

    @hover_star.setter
    def hover_star(self, value):
        self._hover_star = value
        self.update()

    @Property(float)
    def selected_star(self):
        return self._selected_star

    @selected_star.setter
    def selected_star(self, value):
        self._selected_star = value
        self.update()

    @property
    def value(self):
        return self._selected_star

    @value.setter
    def value(self, val):
        self._selected_star = max(0.0, min(val, self._max_stars))
        self.update()

    def _star_rect(self, index: int) -> QRectF:
        x = 4 + index * (self._star_size + self._spacing)
        y = (self.height() - self._star_size) / 2
        return QRectF(x, y, self._star_size, self._star_size)

    def _star_at(self, pos) -> float:
        for i in range(self._max_stars):
            rect = self._star_rect(i)
            if pos.x() <= rect.right():
                if self._half_star and pos.x() < rect.center().x():
                    return i + 0.5
                return float(i + 1)
        return float(self._max_stars)

    def mouseMoveEvent(self, event):
        if not self._read_only:
            self._hover_star = self._star_at(event.position())
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if not self._read_only and event.button() == Qt.LeftButton:
            new_val = self._star_at(event.position())
            self._selected_anim.stop()
            self._selected_anim.setStartValue(self._selected_star)
            self._selected_anim.setEndValue(new_val)
            self._selected_anim.start()
            self.valueChanged.emit(new_val)
        super().mousePressEvent(event)

    def leaveEvent(self, event):
        self._hover_star = 0.0
        self.update()
        super().leaveEvent(event)

    def _draw_star(self, painter: QPainter, rect: QRectF, fill: float, color: QColor, bg_color: QColor):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        cx, cy = rect.center().x(), rect.center().y()
        outer_r = rect.width() / 2
        inner_r = outer_r * 0.4

        import math
        for i in range(5):
            outer_angle = math.radians(-90 + i * 72)
            inner_angle = math.radians(-90 + i * 72 + 36)
            ox = cx + outer_r * math.cos(outer_angle)
            oy = cy + outer_r * math.sin(outer_angle)
            ix = cx + inner_r * math.cos(inner_angle)
            iy = cy + inner_r * math.sin(inner_angle)
            if i == 0:
                path.moveTo(ox, oy)
            else:
                path.lineTo(ox, oy)
            path.lineTo(ix, iy)
        path.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawPath(path)

        if fill > 0:
            clip_width = rect.width() * min(fill, 1.0)
            clip_rect = QRectF(rect.left(), rect.top(), clip_width, rect.height())
            painter.setClipRect(clip_rect)
            painter.setBrush(QBrush(color))
            painter.drawPath(path)
            painter.setClipping(False)

        painter.restore()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        active_color = QColor(tm.color("primary"))
        inactive_color = QColor(tm.color("bg_solid_tertiary"))

        display_val = self._hover_star if self._hover_star > 0 else self._selected_star

        for i in range(self._max_stars):
            rect = self._star_rect(i)
            star_fill = 0.0
            if display_val >= i + 1:
                star_fill = 1.0
            elif display_val > i:
                star_fill = display_val - i
            self._draw_star(painter, rect, star_fill, active_color, inactive_color)

        painter.end()

    def apply_theme(self):
        self.setStyleSheet("background: transparent;")
        self.update()
