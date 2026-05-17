import math
import random

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.theme.theme_manager import ThemeManager


class AnimatedBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tm = ThemeManager()
        self._particles = []
        self._seed = random.Random(42)
        self._init_particles()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_frame)
        self._timer.start(33)

    def _init_particles(self):
        for _ in range(25):
            self._particles.append({
                'x': self._seed.uniform(0, 1),
                'y': self._seed.uniform(0, 1),
                'vx': self._seed.uniform(-0.0003, 0.0003),
                'vy': self._seed.uniform(-0.0003, 0.0003),
                'r': self._seed.uniform(2, 5),
            })

    def _update_frame(self):
        for p in self._particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            if p['x'] < 0 or p['x'] > 1:
                p['vx'] *= -1
            if p['y'] < 0 or p['y'] > 1:
                p['vy'] *= -1
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        if not self._timer.isActive():
            self._timer.start(33)

    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        primary = QColor(tm.color('primary'))
        primary.setAlpha(25)
        pen = QPen(primary, 1)
        painter.setPen(pen)
        for i, p1 in enumerate(self._particles):
            for p2 in self._particles[i + 1:]:
                dist = math.hypot((p1['x'] - p2['x']) * w, (p1['y'] - p2['y']) * h)
                if dist < 150:
                    alpha = int(25 * (1 - dist / 150))
                    primary.setAlpha(alpha)
                    pen.setColor(primary)
                    painter.setPen(pen)
                    painter.drawLine(
                        int(p1['x'] * w), int(p1['y'] * h),
                        int(p2['x'] * w), int(p2['y'] * h),
                    )

        dot_color = QColor(tm.color('primary'))
        dot_color.setAlpha(60)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(dot_color))
        for p in self._particles:
            painter.drawEllipse(
                QRectF(p['x'] * w - p['r'], p['y'] * h - p['r'], p['r'] * 2, p['r'] * 2)
            )

        painter.end()
