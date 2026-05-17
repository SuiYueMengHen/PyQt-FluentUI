from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentToggleButton(QPushButton, FluentWidgetBase):
    _checked_progress = 0.0

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self._init_fluent_base()
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(36)
        self._checked_anim = QPropertyAnimation(self, b"checked_progress")
        self._checked_anim.setDuration(200)
        self._checked_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.toggled.connect(self.onToggle)

    def sizeHint(self):
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        return QSize(max(80, text_width + 40), 36)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('md')}px;
                color: {tm.color('fg_primary')};
                padding: 0 20px;
                font-size: {tm.font_size('body')}px;
                font-weight: 500;
            }}
            QPushButton:checked {{
                background-color: {tm.color('primary_light')};
                border-color: {tm.color('primary')};
                color: {tm.color('primary')};
            }}
            QPushButton:disabled {{
                background-color: {tm.color('bg_solid_tertiary')};
                color: {tm.color('fg_disabled')};
            }}
        """)

    def onToggle(self, checked):
        self._checked_anim.stop()
        self._checked_anim.setStartValue(self._checked_progress)
        self._checked_anim.setEndValue(1.0 if checked else 0.0)
        self._checked_anim.start()

    @Property(float)
    def checked_progress(self):
        return self._checked_progress

    @checked_progress.setter
    def checked_progress(self, value):
        self._checked_progress = value
        self.update()
