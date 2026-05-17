import math
import random

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QFont, QFontMetrics

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class WordItem:
    def __init__(self, text: str, weight: float):
        self.text = text
        self.weight = weight
        self.x = 0.0
        self.y = 0.0
        self.font_size = 0
        self.color_key = ""
        self.text_width = 0.0
        self.text_height = 0.0


class FluentWordCloud(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._words: list[WordItem] = []
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(250)
        self._anim = None
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(200)
        self._resize_timer.timeout.connect(self._relayout)
        self._hovered_idx = -1
        self.setMouseTracking(True)
        QTimer.singleShot(50, self._start_anim)

    def _start_anim(self):
        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    @Property(float)
    def anim_progress(self):
        return self._anim_progress

    @anim_progress.setter
    def anim_progress(self, v):
        self._anim_progress = v
        self.update()

    def set_data(self, words: list[dict]):
        self._words = []
        if not words:
            return
        max_weight = max(w.get("weight", 1) for w in words)
        min_weight = min(w.get("weight", 1) for w in words)
        weight_range = max_weight - min_weight if max_weight != min_weight else 1

        _COLORS = ["primary", "accent_success", "accent_warning", "accent_error", "accent_info"]

        rng = random.Random(42)
        for i, w in enumerate(words):
            item = WordItem(w.get("text", ""), w.get("weight", 1))
            t = (item.weight - min_weight) / weight_range
            item.font_size = int(12 + t * 28)
            item.color_key = _COLORS[i % len(_COLORS)]
            self._words.append(item)

        self._layout_words(rng)
        self.update()

    def _relayout(self):
        if self._words:
            rng = random.Random(42)
            self._layout_words(rng)
            self.update()

    def _layout_words(self, rng: random.Random):
        if not self._words:
            return
        w = self.width()
        h = self.height()
        if w < 50 or h < 50:
            return

        cx, cy = w / 2, h / 2
        sorted_words = sorted(self._words, key=lambda x: -x.weight)

        placed = []
        for item in sorted_words:
            fm = QFont()
            fm.setPixelSize(item.font_size)
            fm.setWeight(QFont.DemiBold)
            metrics = QFontMetrics(fm)
            tw = metrics.horizontalAdvance(item.text)
            th = item.font_size
            item.text_width = tw
            item.text_height = th

            angle = 0
            radius = 0
            found = False
            for attempt in range(200):
                x = cx + radius * math.cos(angle) - tw / 2
                y = cy + radius * math.sin(angle) - th / 2

                rect = QRectF(x, y, tw, th)
                overlap = False
                for p_rect in placed:
                    if rect.intersects(p_rect):
                        overlap = True
                        break

                if not overlap and 4 < x and x + tw < w - 4 and 4 < y and y + th < h - 4:
                    item.x = x
                    item.y = y
                    placed.append(rect)
                    found = True
                    break

                angle += 0.5
                radius += 0.8

            if not found:
                item.x = rng.uniform(10, w - tw - 10)
                item.y = rng.uniform(10, h - th - 10)
                placed.append(QRectF(item.x, item.y, tw, th))

    def _word_at(self, pos):
        for i, item in enumerate(self._words):
            rect = QRectF(item.x, item.y, item.text_width, item.text_height)
            if rect.contains(pos):
                return i
        return -1

    def mouseMoveEvent(self, event):
        self._hovered_idx = self._word_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_idx = -1
        self.update()
        super().leaveEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._words:
            self._resize_timer.start()

    def paintEvent(self, event):
        if not self._words:
            return
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setOpacity(self._anim_progress)

        for i, item in enumerate(self._words):
            is_hovered = (i == self._hovered_idx)
            font = QFont()
            font.setPixelSize(item.font_size + (4 if is_hovered else 0))
            font.setWeight(QFont.DemiBold)
            painter.setFont(font)
            color = QColor(tm.color(item.color_key))
            if is_hovered:
                color = color.lighter(130)
            painter.setPen(color)
            painter.drawText(QRectF(item.x, item.y, 300, item.font_size + 8), Qt.AlignLeft | Qt.AlignVCenter, item.text)

        if self._hovered_idx >= 0:
            item = self._words[self._hovered_idx]
            text = f"{item.text}: {item.weight:.0f}"
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(text) + 16
            th = 24
            tx = item.x + item.text_width / 2 - tw / 2
            ty = item.y - th - 6
            if ty < 0:
                ty = item.y + item.text_height + 6

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(tm.color("bg_solid_card")))
            painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
            painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
            painter.setPen(QColor(tm.color("fg_primary")))
            painter.drawText(QRectF(tx, ty, tw, th), Qt.AlignCenter, text)

        painter.end()

    def apply_theme(self):
        self.update()
