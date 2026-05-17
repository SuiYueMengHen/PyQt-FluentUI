from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentTour(QWidget, FluentWidgetBase):
    finished = Signal()
    _fade_progress = 0.0

    def __init__(self, steps: list[dict] = None, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._steps = steps or []
        self._current = 0
        self._is_active = False
        self.hide()

        self._fade_anim = QPropertyAnimation(self, b"fade_progress")
        self._fade_anim.setDuration(200)
        self._fade_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def fade_progress(self):
        return self._fade_progress

    @fade_progress.setter
    def fade_progress(self, v):
        self._fade_progress = v
        self.update()

    def set_steps(self, steps: list[dict]):
        self._steps = steps

    def start(self):
        self._current = 0
        self._is_active = True
        self.show()
        self._fade_anim.stop()
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.start()

    def next_step(self):
        self._current += 1
        if self._current >= len(self._steps):
            self.stop()
        else:
            self.update()

    def prev_step(self):
        self._current = max(0, self._current - 1)
        self.update()

    def stop(self):
        self._is_active = False
        self._fade_anim.stop()
        self._fade_anim.setStartValue(self._fade_progress)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.finished.connect(self._finish_stop)
        self._fade_anim.start()

    def _finish_stop(self):
        self.hide()
        self.finished.emit()
        try:
            self._fade_anim.finished.disconnect()
        except Exception:
            pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.next_step()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        if not self._is_active or not self._steps:
            return

        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        overlay = QColor(0, 0, 0, int(120 * self._fade_progress))
        painter.fillRect(self.rect(), overlay)

        step = self._steps[self._current] if self._current < len(self._steps) else self._steps[-1]
        target = step.get("target_rect", QRectF(50, 50, 200, 100))
        title = step.get("title", "")
        desc = step.get("description", "")

        painter.setCompositionMode(QPainter.CompositionMode_CompositionMode_SourceOver)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 0, 0)
        hole = QPainterPath()
        hole.addRoundedRect(target, 8, 8)
        cut_path = path - hole
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, int(120 * self._fade_progress)))
        painter.drawPath(cut_path)

        painter.setPen(QPen(QColor(tm.color("primary")), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(target, 8, 8)

        tip_x = target.x()
        tip_y = target.y() + target.height() + 12
        tip_w = 260
        tip_h = 80

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(tip_x, tip_y, tip_w, tip_h), 8, 8)

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(tip_x, tip_y, tip_w, tip_h), 8, 8)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(tip_x + 12, tip_y + 8, tip_w - 24, 22), Qt.AlignLeft, title)

        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(QRectF(tip_x + 12, tip_y + 32, tip_w - 24, 28), Qt.AlignLeft | Qt.TextWordWrap, desc)

        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_tertiary")))
        painter.drawText(QRectF(tip_x + 12, tip_y + 58, tip_w - 24, 16), Qt.AlignLeft, f"{self._current + 1} / {len(self._steps)}")

        painter.end()

    def apply_theme(self):
        self.update()
