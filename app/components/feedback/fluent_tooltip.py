from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentTooltip(QWidget, FluentWidgetBase):
    _opacity = 0.0

    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._text = text
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        self._label = QLabel(text)
        self._label.setWordWrap(True)
        layout.addWidget(self._label)

        self._fade_anim = QPropertyAnimation(self, b"opacity")
        self._fade_anim.setDuration(150)
        self._fade_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)
        self.update()

    def show_tooltip(self, pos):
        self.move(pos)
        self.show()
        self._fade_anim.stop()
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.start()

    def hide_tooltip(self):
        self._fade_anim.stop()
        self._fade_anim.setStartValue(self._opacity)
        self._fade_anim.setEndValue(0.0)
        try:
            self._fade_anim.finished.disconnect(self.hide)
        except RuntimeError:
            pass
        self._fade_anim.finished.connect(self.hide)
        self._fade_anim.start()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('sm')}px;
            }}
        """)
        self._label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('caption')}px; background: transparent;")
