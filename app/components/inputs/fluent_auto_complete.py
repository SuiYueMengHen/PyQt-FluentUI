from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentAutoComplete(QWidget, FluentWidgetBase):
    text_changed = Signal(str)
    selected = Signal(str)
    _drop_progress = 0.0

    def __init__(self, placeholder: str = "搜索...", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._placeholder = placeholder
        self._text = ""
        self._suggestions: list[str] = []
        self._filtered: list[str] = []
        self._is_open = False
        self._hovered_idx = -1
        self.setFixedHeight(32)
        self.setMinimumWidth(200)
        self.setCursor(Qt.IBeamCursor)

        self._drop_anim = QPropertyAnimation(self, b"drop_progress")
        self._drop_anim.setDuration(150)
        self._drop_anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_suggestions(self, items: list[str]):
        self._suggestions = items

    @Property(float)
    def drop_progress(self):
        return self._drop_progress

    @drop_progress.setter
    def drop_progress(self, v):
        self._drop_progress = v
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace and self._text:
            self._text = self._text[:-1]
            self._filter()
        elif event.key() == Qt.Key_Down and self._filtered:
            self._hovered_idx = min(self._hovered_idx + 1, len(self._filtered) - 1)
            self.update()
        elif event.key() == Qt.Key_Up and self._filtered:
            self._hovered_idx = max(self._hovered_idx - 1, 0)
            self.update()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter) and 0 <= self._hovered_idx < len(self._filtered):
            self._text = self._filtered[self._hovered_idx]
            self.selected.emit(self._text)
            self._is_open = False
            self.update()
        elif event.text() and event.text().isprintable():
            self._text += event.text()
            self._filter()
        else:
            super().keyPressEvent(event)

    def _filter(self):
        self.text_changed.emit(self._text)
        if self._text:
            self._filtered = [s for s in self._suggestions if self._text.lower() in s.lower()][:8]
            self._is_open = bool(self._filtered)
            self._hovered_idx = 0
        else:
            self._filtered = []
            self._is_open = False
        self.update()

    def mousePressEvent(self, event):
        if self._is_open and event.position().y() > self.height():
            idx = int((event.position().y() - self.height()) / 28)
            if 0 <= idx < len(self._filtered):
                self._text = self._filtered[idx]
                self.selected.emit(self._text)
                self._is_open = False
                self.update()
        else:
            self.setFocus()
        super().mousePressEvent(event)

    def focusOutEvent(self, event):
        self._is_open = False
        self.update()
        super().focusOutEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        border_color = QColor(tm.color("primary")) if self._is_open or self.hasFocus() else QColor(tm.color("stroke_card"))
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 4, 4)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        if self._text:
            painter.setPen(QColor(tm.color("fg_primary")))
            painter.drawText(QRectF(10, 0, self.width() - 20, self.height()), Qt.AlignVCenter, self._text)
            cursor_x = 10 + painter.fontMetrics().horizontalAdvance(self._text)
            if self.hasFocus():
                painter.setPen(QColor(tm.color("primary")))
                painter.drawLine(int(cursor_x), 8, int(cursor_x), int(self.height() - 8))
        else:
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(QRectF(10, 0, self.width() - 20, self.height()), Qt.AlignVCenter, self._placeholder)

        painter.end()

    def apply_theme(self):
        self.update()
