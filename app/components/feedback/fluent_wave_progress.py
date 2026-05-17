import math

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentWaveProgress(QWidget, FluentWidgetBase):
    valueChanged = Signal(float)
    _level_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._value = 0.0
        self._target_value = 0.0
        self._wave_offset = 0.0
        self.setFixedSize(120, 120)

        self._level_anim = QPropertyAnimation(self, b"level_progress")
        self._level_anim.setDuration(800)
        self._level_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._wave_timer = QTimer(self)
        self._wave_timer.timeout.connect(self._update_wave)
        self._wave_timer.start(33)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._target_value = max(0, min(100, val))
        self._level_anim.stop()
        self._level_anim.setStartValue(self._level_progress)
        self._level_anim.setEndValue(self._target_value / 100.0)
        self._level_anim.start()
        self._value = self._target_value
        self.valueChanged.emit(self._value)

    @Property(float)
    def level_progress(self):
        return self._level_progress

    @level_progress.setter
    def level_progress(self, value):
        self._level_progress = value
        self.update()

    def _update_wave(self):
        self._wave_offset += 0.08
        if self._wave_offset > 2 * math.pi:
            self._wave_offset -= 2 * math.pi
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        if not self._wave_timer.isActive():
            self._wave_timer.start(33)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._wave_timer.stop()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        size = min(self.width(), self.height())
        margin = 4
        circle_size = size - margin * 2
        cx = self.width() / 2
        cy = self.height() / 2
        circle_rect = QRectF(margin, margin, circle_size, circle_size)

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 2))
        painter.setBrush(QColor(tm.color("bg_solid_tertiary")))
        painter.drawEllipse(circle_rect)

        painter.save()
        painter.setClipRect(circle_rect)

        water_y = margin + circle_size * (1.0 - self._level_progress)

        wave_path1 = QPainterPath()
        wave_path2 = QPainterPath()

        start_x = margin - 10
        end_x = margin + circle_size + 10

        wave_path1.moveTo(start_x, self.height())
        wave_path2.moveTo(start_x, self.height())

        for x in range(int(start_x), int(end_x) + 1, 2):
            y1 = water_y + math.sin((x - start_x) * 0.03 + self._wave_offset) * 4
            y2 = water_y + math.sin((x - start_x) * 0.03 + self._wave_offset + math.pi) * 3
            wave_path1.lineTo(x, y1)
            wave_path2.lineTo(x, y2)

        wave_path1.lineTo(end_x, self.height())
        wave_path1.closeSubpath()
        wave_path2.lineTo(end_x, self.height())
        wave_path2.closeSubpath()

        primary = QColor(tm.color("primary"))
        primary.setAlpha(60)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(primary))
        painter.drawPath(wave_path2)

        primary.setAlpha(100)
        painter.setBrush(QBrush(primary))
        painter.drawPath(wave_path1)

        painter.restore()

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 2))
        painter.drawEllipse(circle_rect)

        font = QFont()
        font.setPixelSize(tm.font_size("title_large"))
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        text = f"{int(self._level_progress * 100)}%"
        painter.drawText(circle_rect, Qt.AlignCenter, text)

        painter.end()

    def apply_theme(self):
        self.update()
