from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class TabButton(QWidget):
    clicked = Signal(int)

    def __init__(self, text: str, index: int, parent=None):
        super().__init__(parent)
        self._text = text
        self._index = index
        self._active = False
        self._hover_progress = 0.0
        self._tm = ThemeManager()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)
        self.setMinimumWidth(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)

        self._label = QLabel(text)
        layout.addWidget(self._label)

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self._update_style()
        self.update()

    def _update_style(self):
        tm = self._tm
        color = tm.color('primary') if self._active else tm.color('fg_secondary')
        weight = '600' if self._active else '400'
        self._label.setStyleSheet(f"color: {color}; font-size: {tm.font_size('body')}px; font-weight: {weight}; background: transparent;")

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, value):
        self._hover_progress = value
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
        self.clicked.emit(self._index)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        if self._active:
            tm = self._tm
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(tm.color('primary')))
            indicator = QRectF(8, self.height() - 3, self.width() - 16, 3)
            painter.drawRoundedRect(indicator, 1.5, 1.5)
            painter.end()

    def apply_theme(self):
        self._update_style()


class FluentTabBar(QWidget, FluentWidgetBase):
    current_changed = Signal(int)

    def __init__(self, tabs: list[str] = None, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._current_index = 0
        self._tab_buttons: list[TabButton] = []

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addStretch()

        if tabs:
            for tab in tabs:
                self.add_tab(tab)

    def add_tab(self, text: str):
        index = len(self._tab_buttons)
        btn = TabButton(text, index, self)
        btn.clicked.connect(self._on_tab_clicked)
        self._layout.insertWidget(self._layout.count() - 1, btn)
        self._tab_buttons.append(btn)
        if index == 0:
            btn.active = True

    def _on_tab_clicked(self, index: int):
        if self._current_index != index:
            self._current_index = index
            for i, btn in enumerate(self._tab_buttons):
                btn.active = (i == index)
            self.current_changed.emit(index)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background: transparent; border-bottom: 1px solid {tm.color('stroke_divider')};")
        for btn in self._tab_buttons:
            btn.apply_theme()
