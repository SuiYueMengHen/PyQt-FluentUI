from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentSlider(QSlider, FluentWidgetBase):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self._init_fluent_base()
        self.setFixedHeight(24)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        track_y = self.height() / 2
        track_height = 4
        handle_size = 16

        if self.orientation() == Qt.Horizontal:
            track_rect = QRectF(0, track_y - track_height / 2, self.width(), track_height)
            progress = (self.value() - self.minimum()) / max(1, (self.maximum() - self.minimum()))
            progress_width = self.width() * progress

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(tm.color('stroke_card'))))
            painter.drawRoundedRect(track_rect, 2, 2)

            progress_rect = QRectF(0, track_y - track_height / 2, progress_width, track_height)
            painter.setBrush(QBrush(QColor(tm.color('primary'))))
            painter.drawRoundedRect(progress_rect, 2, 2)

            handle_x = progress_width - handle_size / 2
            handle_y = track_y - handle_size / 2
            painter.setBrush(QBrush(QColor(tm.color('bg_solid_card'))))
            painter.setPen(QPen(QColor(tm.color('primary')), 2))
            painter.drawEllipse(QRectF(handle_x, handle_y, handle_size, handle_size))

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QSlider {{
                background: transparent;
            }}
            QSlider::groove {{
                background: transparent;
                height: 24px;
            }}
            QSlider::handle {{
                background: transparent;
                width: 16px;
                height: 16px;
                margin: 4px 0;
            }}
        """)
