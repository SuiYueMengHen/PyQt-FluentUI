from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentChip(QWidget, FluentWidgetBase):
    clicked = Signal()
    closed = Signal()
    toggled = Signal(bool)
    _press_scale = 1.0

    def __init__(self, text: str, icon_name: str = "", variant: str = "default",
                 closable: bool = False, checkable: bool = False, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._text = text
        self._icon_name = icon_name
        self._variant = variant
        self._closable = closable
        self._checkable = checkable
        self._checked = False
        self._hovered = False
        self._height = 32
        self._padding_h = 12
        self.setCursor(Qt.PointingHandCursor)

        self._press_anim = QPropertyAnimation(self, b"press_scale")
        self._press_anim.setDuration(100)
        self._press_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._update_size()

    def _update_size(self):
        tm = self._tm
        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        from PySide6.QtGui import QFontMetrics
        fm = QFontMetrics(font)
        text_w = fm.horizontalAdvance(self._text)
        icon_w = 24 if self._icon_name else 0
        close_w = 20 if self._closable else 0
        total_w = self._padding_h + icon_w + text_w + close_w + self._padding_h + 4
        self.setFixedSize(max(total_w, 60), self._height)

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        self._checked = value
        self.toggled.emit(value)
        self.update()

    @Property(float)
    def press_scale(self):
        return self._press_scale

    @press_scale.setter
    def press_scale(self, value):
        self._press_scale = value
        self.update()

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            close_x = self.width() - 16
            if self._closable and event.position().x() >= close_x - 8:
                self.closed.emit()
                return
            if self._checkable:
                self._checked = not self._checked
                self.toggled.emit(self._checked)
            self.clicked.emit()
            self._press_anim.stop()
            self._press_anim.setStartValue(1.0)
            self._press_anim.setEndValue(0.95)
            self._press_anim.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._press_anim.stop()
        self._press_anim.setStartValue(self._press_scale)
        self._press_anim.setEndValue(1.0)
        self._press_anim.start()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        variant_colors = {
            "default": {"bg": tm.color("bg_solid_tertiary"), "fg": tm.color("fg_primary"), "border": tm.color("stroke_card")},
            "primary": {"bg": tm.color("primary_light"), "fg": tm.color("primary"), "border": tm.color("primary")},
            "success": {"bg": tm.color("accent_success_light"), "fg": tm.color("accent_success"), "border": tm.color("accent_success")},
            "warning": {"bg": tm.color("accent_warning_light"), "fg": tm.color("accent_warning"), "border": tm.color("accent_warning")},
            "error": {"bg": tm.color("accent_error_light"), "fg": tm.color("accent_error"), "border": tm.color("accent_error")},
        }
        colors = variant_colors.get(self._variant, variant_colors["default"])

        if self._checked and self._checkable:
            bg = QColor(tm.color("primary"))
            fg = QColor(tm.color("primary_text_on"))
        else:
            bg = QColor(colors["bg"])
            fg = QColor(colors["fg"])

        if self._hovered:
            bg.setAlpha(min(255, bg.alpha() + 20))

        rect = QRectF(0, 0, self.width(), self.height())
        border_color = QColor(colors["border"])
        border_color.setAlpha(80)
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(rect, self.height() / 2, self.height() / 2)

        x_offset = self._padding_h

        if self._icon_name:
            icon = get_icon(self._icon_name, fg.name() if self._checked or self._variant != "default" else tm.color("fg_secondary"), 16)
            painter.drawPixmap(int(x_offset), int((self.height() - 16) / 2), icon.pixmap(16, 16))
            x_offset += 20

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)
        painter.setPen(fg)
        painter.drawText(QRectF(x_offset, 0, self.width() - x_offset - (20 if self._closable else self._padding_h), self.height()),
                         Qt.AlignVCenter | Qt.AlignLeft, self._text)

        if self._closable:
            close_x = self.width() - 16
            close_cy = self.height() / 2
            pen = QPen(fg, 1.5)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(int(close_x - 3), int(close_cy - 3), int(close_x + 3), int(close_cy + 3))
            painter.drawLine(int(close_x + 3), int(close_cy - 3), int(close_x - 3), int(close_cy + 3))

        painter.end()

    def apply_theme(self):
        self._update_size()
        self.update()
