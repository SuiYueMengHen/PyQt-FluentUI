from PySide6.QtWidgets import QRadioButton
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentRadioButton(QRadioButton, FluentWidgetBase):
    _dot_progress = 0.0

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self._init_fluent_base()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(32)
        self._dot_anim = QPropertyAnimation(self, b"dot_progress")
        self._dot_anim.setDuration(200)
        self._dot_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.toggled.connect(self._on_toggled)

    def _on_toggled(self, checked):
        self._dot_anim.stop()
        self._dot_anim.setStartValue(self._dot_progress)
        self._dot_anim.setEndValue(1.0 if checked else 0.0)
        self._dot_anim.start()

    @Property(float)
    def dot_progress(self):
        return self._dot_progress

    @dot_progress.setter
    def dot_progress(self, value):
        self._dot_progress = value
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        circle_size = 18
        cx = 4 + circle_size / 2
        cy = self.height() / 2

        outer_rect = QRectF(cx - circle_size / 2, cy - circle_size / 2, circle_size, circle_size)

        if self.isChecked():
            border_color = QColor(tm.color('primary'))
        else:
            border_color = QColor(tm.color('stroke_card'))

        painter.setPen(QPen(border_color, 1.5))
        painter.setBrush(QBrush(QColor(tm.color('bg_solid_card'))))
        painter.drawEllipse(outer_rect)

        if self._dot_progress > 0:
            dot_radius = 4 * self._dot_progress
            dot_color = QColor(tm.color('primary'))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(dot_color))
            painter.drawEllipse(QRectF(cx - dot_radius, cy - dot_radius, dot_radius * 2, dot_radius * 2))

        if self.text():
            text_color = QColor(tm.color('fg_primary')) if self.isEnabled() else QColor(tm.color('fg_disabled'))
            painter.setPen(text_color)
            painter.setFont(self.font())
            text_x = 4 + circle_size + 8
            text_rect = QRectF(text_x, 0, self.width() - text_x, self.height())
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QRadioButton {{
                background-color: transparent;
                color: {tm.color('fg_primary')};
                font-size: {tm.font_size('body')}px;
                spacing: 0px;
            }}
            QRadioButton:disabled {{
                color: {tm.color('fg_disabled')};
            }}
        """)
