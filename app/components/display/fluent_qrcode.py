from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentQRCode(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, text: str = "Hello FluentUI", size: int = 160, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._text = text
        self._module_size = 4
        self._setFixedSize(size)
        self._matrix: list[list[int]] = []
        self._generate()

        self._anim = None
        QTimer.singleShot(50, self._start_anim)

    def _start_anim(self):
        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(400)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def _setFixedSize(self, size):
        self.setFixedSize(size, size)

    def set_text(self, text: str):
        self._text = text
        self._generate()
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def _generate(self):
        data = self._text.encode("utf-8")
        size = 25
        self._matrix = [[0] * size for _ in range(size)]

        for i in range(7):
            for j in range(7):
                if i in (0, 6) or j in (0, 6) or (2 <= i <= 4 and 2 <= j <= 4):
                    self._matrix[i][j] = 1
                    self._matrix[i][size - 1 - j] = 1
                    self._matrix[size - 1 - i][j] = 1

        for i in range(8):
            self._matrix[6][i] = 1 if i % 2 == 0 else 0
            self._matrix[i][6] = 1 if i % 2 == 0 else 0
            self._matrix[6][size - 1 - i] = 1 if i % 2 == 0 else 0
            self._matrix[size - 1 - i][6] = 1 if i % 2 == 0 else 0

        import hashlib
        h = hashlib.md5(data).hexdigest()
        for idx, ch in enumerate(h):
            row = 8 + (idx % (size - 16))
            col = 8 + ((idx * 7) % (size - 16))
            if 0 <= row < size and 0 <= col < size:
                self._matrix[row][col] = int(ch, 16) % 2

    @Property(float)
    def anim_progress(self):
        return self._anim_progress

    @anim_progress.setter
    def anim_progress(self, v):
        self._anim_progress = v
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        margin = 12
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        if not self._matrix:
            painter.end()
            return

        size = len(self._matrix)
        total_w = self.width() - 2 * margin
        cell = total_w / size
        offset_x = margin
        offset_y = margin

        fg = QColor(tm.color("fg_primary"))
        fg.setAlpha(int(255 * self._anim_progress))

        for r in range(size):
            for c in range(size):
                if self._matrix[r][c]:
                    x = offset_x + c * cell
                    y = offset_y + r * cell
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QBrush(fg))
                    painter.drawRoundedRect(QRectF(x, y, cell - 0.5, cell - 0.5), 0.5, 0.5)

        painter.end()

    def apply_theme(self):
        self.update()
