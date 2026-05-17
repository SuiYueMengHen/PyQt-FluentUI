from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class TimelineEvent:
    def __init__(self, date: str, title: str, description: str = "", color_key: str = "primary"):
        self.date = date
        self.title = title
        self.description = description
        self.color_key = color_key
        self.y = 0.0


class FluentTimelineChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0
    event_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._events: list[TimelineEvent] = []
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(200)
        self._anim = None
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(200)
        self._resize_timer.timeout.connect(self._do_layout)
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

    def set_data(self, events: list[dict]):
        self._events = []
        for e in events:
            self._events.append(TimelineEvent(
                date=e.get("date", ""),
                title=e.get("title", ""),
                description=e.get("description", ""),
                color_key=e.get("color_key", "primary"),
            ))
        self._do_layout()
        self.update()

    def _do_layout(self):
        if not self._events:
            return
        y = 20
        for event in self._events:
            event.y = y
            y += 80
        min_h = y + 20
        if self.minimumHeight() < min_h:
            self.setMinimumHeight(min_h)
        self.update()

    def _event_at(self, pos):
        for i, event in enumerate(self._events):
            rect = QRectF(80, event.y, self.width() - 100, 60)
            if rect.contains(pos):
                return i
        return -1

    def mouseMoveEvent(self, event):
        self._hovered_idx = self._event_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_idx = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            idx = self._event_at(event.position())
            if idx >= 0:
                self.event_clicked.emit(self._events[idx].title)
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._events:
            self._resize_timer.start()

    def paintEvent(self, event):
        if not self._events:
            return
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setOpacity(self._anim_progress)

        line_x = 60
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 2))
        painter.drawLine(line_x, 10, line_x, int(self._events[-1].y) + 50)

        for i, event in enumerate(self._events):
            is_hovered = (i == self._hovered_idx)
            color = QColor(tm.color(event.color_key))

            dot_r = 8 if is_hovered else 6
            glow = QColor(color)
            glow.setAlpha(40 if is_hovered else 20)
            painter.setPen(Qt.NoPen)
            painter.setBrush(glow)
            painter.drawEllipse(QRectF(line_x - dot_r - 4, event.y + 16 - dot_r - 4, (dot_r + 4) * 2, (dot_r + 4) * 2))
            painter.setBrush(color)
            painter.drawEllipse(QRectF(line_x - dot_r, event.y + 16 - dot_r, dot_r * 2, dot_r * 2))

            font = QFont()
            font.setPixelSize(tm.font_size("caption") - 2)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(0, event.y + 8, 50, 20), Qt.AlignRight | Qt.AlignVCenter, event.date)

            card_x = 80
            card_w = self.width() - 100
            card_h = 56
            card_rect = QRectF(card_x, event.y + 2, card_w, card_h)

            if is_hovered:
                shadow = QColor(color)
                shadow.setAlpha(20)
                painter.setPen(Qt.NoPen)
                painter.setBrush(shadow)
                painter.drawRoundedRect(QRectF(card_x - 2, event.y, card_w + 4, card_h + 4), 8, 8)

            painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
            painter.setBrush(QColor(tm.color("bg_solid_card")))
            painter.drawRoundedRect(card_rect, 6, 6)

            left_bar = QRectF(card_x, event.y + 2, 4, card_h)
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawRoundedRect(left_bar, 2, 2)

            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.DemiBold)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_primary")))
            title_rect = QRectF(card_x + 12, event.y + 6, card_w - 20, 22)
            painter.drawText(title_rect, Qt.AlignLeft | Qt.AlignVCenter, event.title)

            if event.description:
                font.setPixelSize(tm.font_size("caption") - 2)
                font.setWeight(QFont.Normal)
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_secondary")))
                desc_rect = QRectF(card_x + 12, event.y + 28, card_w - 20, 20)
                painter.drawText(desc_rect, Qt.AlignLeft | Qt.AlignVCenter, event.description)

        painter.end()

    def apply_theme(self):
        self.update()
