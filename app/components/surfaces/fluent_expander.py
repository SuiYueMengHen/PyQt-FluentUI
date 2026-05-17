from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QPainter, QColor, QTransform

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentExpander(QWidget, FluentWidgetBase):
    _expand_progress = 0.0

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._expanded = False
        self._title = title
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        self._header = QWidget()
        self._header.setFixedHeight(44)
        self._header.setCursor(Qt.PointingHandCursor)
        header_layout = QHBoxLayout(self._header)
        header_layout.setContentsMargins(16, 0, 16, 0)

        self._arrow_label = QLabel()
        self._arrow_label.setFixedSize(20, 20)
        header_layout.addWidget(self._arrow_label)

        self._title_label = QLabel(title)
        header_layout.addWidget(self._title_label)
        header_layout.addStretch()

        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(16, 0, 16, 16)
        self._content_layout.setSpacing(8)
        self._content.setMaximumHeight(0)

        self._main_layout.addWidget(self._header)
        self._main_layout.addWidget(self._content)

        self._expand_anim = QPropertyAnimation(self, b"expand_progress")
        self._expand_anim.setDuration(250)
        self._expand_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._init_fluent_base()
        self._update_arrow()

    def set_content_widget(self, widget: QWidget):
        self._content_layout.addWidget(widget)

    def mousePressEvent(self, event):
        if self._header.underMouse():
            self._toggle()
        super().mousePressEvent(event)

    def _toggle(self):
        self._expanded = not self._expanded
        self._expand_anim.stop()
        self._expand_anim.setStartValue(self._expand_progress)
        self._expand_anim.setEndValue(1.0 if self._expanded else 0.0)
        self._expand_anim.start()
        self._update_arrow()

    @Property(float)
    def expand_progress(self):
        return self._expand_progress

    @expand_progress.setter
    def expand_progress(self, value):
        self._expand_progress = value
        content_height = self._content.sizeHint().height()
        self._content.setMaximumHeight(int(content_height * value))

    def _update_arrow(self):
        tm = self._tm
        icon = get_icon("chevron_right", tm.color("fg_secondary"), 16)
        pixmap = icon.pixmap(16, 16)
        if self._expanded:
            transform = QTransform()
            transform.rotate(90)
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self._arrow_label.setPixmap(pixmap)
        self._arrow_label.setStyleSheet("background: transparent;")

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background: {tm.color('bg_solid_card')}; border: 1px solid {tm.color('stroke_card')}; border-radius: {tm.radius('lg')}px;")
        self._header.setStyleSheet(f"background: transparent; border-radius: {tm.radius('lg')}px;")
        self._title_label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('body')}px; font-weight: 600; background: transparent;")
        self._content.setStyleSheet("background: transparent;")
        self._update_arrow()
