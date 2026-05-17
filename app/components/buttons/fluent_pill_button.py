from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentPillButton(QWidget, FluentWidgetBase):
    clicked = Signal()
    _hover_progress = 0.0

    def __init__(self, text: str = "标签", selected: bool = False, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._text = text
        self._selected = selected
        self.setFixedHeight(28)
        self.setMinimumWidth(50)
        self.setCursor(Qt.PointingHandCursor)

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.update()

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, v):
        self._hover_progress = v
        self.update()

    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._selected = not self._selected
            self.clicked.emit()
            self.update()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        h = self.height()
        r = h / 2

        if self._selected:
            bg = QColor(tm.color("primary"))
            fg = QColor(tm.color("primary_text_on"))
        else:
            bg_alpha = int(10 + 20 * self._hover_progress)
            bg = QColor(tm.color("fg_primary"))
            bg.setAlpha(bg_alpha)
            fg = QColor(tm.color("fg_primary"))

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1) if not self._selected else Qt.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), h), r, r)

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.DemiBold if self._selected else QFont.Normal)
        painter.setFont(font)
        painter.setPen(fg)
        painter.drawText(QRectF(0, 0, self.width(), h), Qt.AlignCenter, self._text)

        painter.end()

    def apply_theme(self):
        self.update()

    def sizeHint(self):
        font = QFont()
        font.setPixelSize(self._tm.font_size("caption"))
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self._text)
        return QSize(max(50, text_width + 24), 28)
