from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentCheckBox(QCheckBox, FluentWidgetBase):
    _check_progress = 0.0

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self._init_fluent_base()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(32)
        self._check_anim = QPropertyAnimation(self, b"check_progress")
        self._check_anim.setDuration(200)
        self._check_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.stateChanged.connect(self._on_state_changed)

    def _on_state_changed(self, state):
        self._check_anim.stop()
        self._check_anim.setStartValue(self._check_progress)
        self._check_anim.setEndValue(1.0 if state else 0.0)
        self._check_anim.start()

    @Property(float)
    def check_progress(self):
        return self._check_progress

    @check_progress.setter
    def check_progress(self, value):
        self._check_progress = value
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        box_size = 18
        box_x = 4
        box_y = (self.height() - box_size) // 2

        box_rect = QRectF(box_x, box_y, box_size, box_size)

        if self.isChecked():
            bg_color = QColor(tm.color('primary'))
            border_color = QColor(tm.color('primary'))
        else:
            bg_color = QColor(tm.color('bg_solid_card'))
            border_color = QColor(tm.color('stroke_card'))

        painter.setPen(QPen(border_color, 1.5))
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(box_rect, 4, 4)

        if self._check_progress > 0:
            check_color = QColor(tm.color('primary_text_on'))
            pen = QPen(check_color, 2)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            cx = box_x + box_size / 2
            cy = box_y + box_size / 2
            p = self._check_progress

            x1 = cx - 4
            y1 = cy + 1
            x2 = cx - 1
            y2 = cy + 4
            x3 = cx + 5
            y3 = cy - 3

            if p <= 0.5:
                t = p / 0.5
                painter.drawLine(QPointF(x1, y1), QPointF(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
            else:
                t = (p - 0.5) / 0.5
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
                painter.drawLine(QPointF(x2, y2), QPointF(x2 + (x3 - x2) * t, y2 + (y3 - y2) * t))

        if self.text():
            text_color = QColor(tm.color('fg_primary')) if self.isEnabled() else QColor(tm.color('fg_disabled'))
            painter.setPen(text_color)
            painter.setFont(self.font())
            text_x = box_x + box_size + 8
            text_rect = QRectF(text_x, 0, self.width() - text_x, self.height())
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QCheckBox {{
                background-color: transparent;
                color: {tm.color('fg_primary')};
                font-size: {tm.font_size('body')}px;
                spacing: 0px;
            }}
            QCheckBox:disabled {{
                color: {tm.color('fg_disabled')};
            }}
        """)
