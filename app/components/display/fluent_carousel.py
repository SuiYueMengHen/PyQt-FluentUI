from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QBrush, QPen

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentCarousel(QWidget, FluentWidgetBase):
    currentChanged = Signal(int)
    _slide_offset = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._pages: list[QWidget] = []
        self._current_index = 0
        self._target_index = 0
        self.setFixedHeight(200)
        self.setMinimumWidth(300)

        self._slide_anim = QPropertyAnimation(self, b"slide_offset")
        self._slide_anim.setDuration(400)
        self._slide_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._slide_anim.finished.connect(self._on_slide_done)

        self._nav_layout = QHBoxLayout()
        self._nav_layout.setAlignment(Qt.AlignCenter)
        self._nav_layout.setSpacing(6)

        self._auto_timer = QTimer(self)
        self._auto_timer.timeout.connect(self.next)

        self._prev_btn = QPushButton()
        self._prev_btn.setFixedSize(28, 28)
        self._prev_btn.setCursor(Qt.PointingHandCursor)
        self._prev_btn.clicked.connect(self.prev)
        self._prev_btn.hide()

        self._next_btn = QPushButton()
        self._next_btn.setFixedSize(28, 28)
        self._next_btn.setCursor(Qt.PointingHandCursor)
        self._next_btn.clicked.connect(self.next)
        self._next_btn.hide()

    def add_page(self, widget: QWidget):
        widget.setParent(self)
        self._pages.append(widget)
        if len(self._pages) == 1:
            widget.show()
            widget.setGeometry(0, 0, self.width(), self.height() - 32)
        else:
            widget.hide()
        self._update_dots()
        self.update()

    def go_to(self, index: int):
        if index < 0 or index >= len(self._pages) or index == self._current_index:
            return
        self._target_index = index
        direction = 1 if index > self._current_index else -1

        self._pages[index].show()
        self._pages[index].setGeometry(
            direction * self.width(), 0,
            self.width(), self.height() - 32
        )

        self._slide_anim.stop()
        self._slide_anim.setStartValue(0.0)
        self._slide_anim.setEndValue(float(-direction))
        self._slide_anim.start()

    def _on_slide_done(self):
        old = self._current_index
        self._current_index = self._target_index
        for i, page in enumerate(self._pages):
            if i == self._current_index:
                page.setGeometry(0, 0, self.width(), self.height() - 32)
                page.show()
            else:
                page.hide()
        self._slide_offset = 0.0
        self.currentChanged.emit(self._current_index)
        self._update_dots()
        self.update()

    def next(self):
        if len(self._pages) <= 1:
            return
        idx = (self._current_index + 1) % len(self._pages)
        self.go_to(idx)

    def prev(self):
        if len(self._pages) <= 1:
            return
        idx = (self._current_index - 1) % len(self._pages)
        self.go_to(idx)

    def set_auto_play(self, interval: int = 3000):
        self._auto_timer.start(interval)

    def stop_auto_play(self):
        self._auto_timer.stop()

    @Property(float)
    def slide_offset(self):
        return self._slide_offset

    @slide_offset.setter
    def slide_offset(self, value):
        self._slide_offset = value
        if self._pages and 0 <= self._current_index < len(self._pages):
            current = self._pages[self._current_index]
            current.setGeometry(
                int(value * self.width()), 0,
                self.width(), self.height() - 32
            )
        if self._pages and 0 <= self._target_index < len(self._pages):
            target = self._pages[self._target_index]
            direction = 1 if self._target_index > self._current_index else -1
            target.setGeometry(
                int((value + direction) * self.width()), 0,
                self.width(), self.height() - 32
            )

    def _update_dots(self):
        pass

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for i, page in enumerate(self._pages):
            if i == self._current_index:
                page.setGeometry(0, 0, self.width(), self.height() - 32)

    def enterEvent(self, event):
        if len(self._pages) > 1:
            self._prev_btn.show()
            self._next_btn.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._prev_btn.hide()
        self._next_btn.hide()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height() - 32), tm.radius("md"), tm.radius("md"))

        dot_y = self.height() - 16
        total = len(self._pages)
        if total > 0:
            total_width = total * 8 + (total - 1) * 6
            start_x = (self.width() - total_width) / 2
            for i in range(total):
                cx = start_x + i * 14 + 4
                if i == self._current_index:
                    painter.setBrush(QColor(tm.color("primary")))
                    painter.drawEllipse(QRectF(cx - 4, dot_y - 4, 8, 8))
                else:
                    painter.setBrush(QColor(tm.color("fg_tertiary")))
                    painter.drawEllipse(QRectF(cx - 3, dot_y - 3, 6, 6))

        if self._prev_btn.isVisible():
            btn_x = 8
            btn_y = (self.height() - 32) / 2 - 14
            painter.setBrush(QColor(0, 0, 0, 80))
            painter.drawEllipse(QRectF(btn_x, btn_y, 28, 28))

        if self._next_btn.isVisible():
            btn_x = self.width() - 36
            btn_y = (self.height() - 32) / 2 - 14
            painter.setBrush(QColor(0, 0, 0, 80))
            painter.drawEllipse(QRectF(btn_x, btn_y, 28, 28))

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self._prev_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(0,0,0,0.3);
                border: none;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background: rgba(0,0,0,0.5);
            }}
        """)
        self._next_btn.setStyleSheet(self._prev_btn.styleSheet())
        self._prev_btn.setIcon(get_icon("chevron_left", "#FFFFFF", 16))
        self._next_btn.setIcon(get_icon("chevron_right", "#FFFFFF", 16))
        self.update()
