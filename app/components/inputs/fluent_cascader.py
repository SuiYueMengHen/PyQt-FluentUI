from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentCascader(QWidget, FluentWidgetBase):
    selected_changed = Signal(list)
    _drop_progress = 0.0

    def __init__(self, placeholder: str = "请选择", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._placeholder = placeholder
        self._options: list[dict] = []
        self._selected_path: list[str] = []
        self._is_open = False
        self.setFixedHeight(32)
        self.setMinimumWidth(200)
        self.setCursor(Qt.PointingHandCursor)

        self._drop_anim = QPropertyAnimation(self, b"drop_progress")
        self._drop_anim.setDuration(200)
        self._drop_anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_options(self, options: list[dict]):
        self._options = options

    @Property(float)
    def drop_progress(self):
        return self._drop_progress

    @drop_progress.setter
    def drop_progress(self, v):
        self._drop_progress = v
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_open = not self._is_open
            self._drop_anim.stop()
            self._drop_anim.setStartValue(self._drop_progress)
            self._drop_anim.setEndValue(1.0 if self._is_open else 0.0)
            self._drop_anim.start()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        border_color = QColor(tm.color("primary")) if self._is_open else QColor(tm.color("stroke_card"))
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 4, 4)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        if self._selected_path:
            text = " / ".join(self._selected_path)
            painter.setPen(QColor(tm.color("fg_primary")))
            painter.drawText(QRectF(10, 0, self.width() - 30, self.height()), Qt.AlignVCenter, text)
        else:
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(QRectF(10, 0, self.width() - 30, self.height()), Qt.AlignVCenter, self._placeholder)

        arrow = get_icon("chevron_right", tm.color("fg_secondary"), 12)
        painter.drawPixmap(int(self.width() - 20), int((self.height() - 12) / 2), arrow.pixmap(12, 12))

        painter.end()

    def apply_theme(self):
        self.update()
