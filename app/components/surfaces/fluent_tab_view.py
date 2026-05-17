from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentTabView(QWidget, FluentWidgetBase):
    tab_changed = Signal(int)
    _indicator_x = 0.0

    def __init__(self, tabs: list[str] = None, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._tabs = tabs or []
        self._active = 0
        self._hovered = -1
        self.setMinimumSize(300, 200)

        self._indicator_anim = QPropertyAnimation(self, b"indicator_x")
        self._indicator_anim.setDuration(200)
        self._indicator_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def indicator_x(self):
        return self._indicator_x

    @indicator_x.setter
    def indicator_x(self, v):
        self._indicator_x = v
        self.update()

    def set_tabs(self, tabs: list[str]):
        self._tabs = tabs
        self.update()

    def set_active(self, index: int):
        if 0 <= index < len(self._tabs):
            self._active = index
            tab_w = self.width() / max(len(self._tabs), 1)
            target_x = index * tab_w
            self._indicator_anim.stop()
            self._indicator_anim.setStartValue(self._indicator_x)
            self._indicator_anim.setEndValue(float(target_x))
            self._indicator_anim.start()
            self.tab_changed.emit(index)

    def mouseMoveEvent(self, event):
        tab_w = self.width() / max(len(self._tabs), 1)
        idx = int(event.position().x() / tab_w)
        if 0 <= idx < len(self._tabs) and event.position().y() < 40:
            self._hovered = idx
        else:
            self._hovered = -1
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.position().y() < 40:
            tab_w = self.width() / max(len(self._tabs), 1)
            idx = int(event.position().x() / tab_w)
            if 0 <= idx < len(self._tabs):
                self.set_active(idx)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        if not self._tabs:
            painter.end()
            return

        tab_w = self.width() / len(self._tabs)
        header_h = 40

        painter.setPen(QPen(QColor(tm.color("stroke_divider")), 1))
        painter.drawLine(0, header_h, self.width(), header_h)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("primary")))
        painter.drawRoundedRect(QRectF(self._indicator_x + 4, header_h - 3, tab_w - 8, 3), 1.5, 1.5)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        for i, tab in enumerate(self._tabs):
            x = i * tab_w
            is_active = i == self._active
            is_hovered = i == self._hovered

            if is_hovered and not is_active:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(tm.color("nav_item_hover")))
                painter.drawRoundedRect(QRectF(x + 2, 4, tab_w - 4, header_h - 8), 4, 4)

            color = QColor(tm.color("primary")) if is_active else QColor(tm.color("fg_secondary")) if is_hovered else QColor(tm.color("fg_tertiary"))
            font.setWeight(QFont.DemiBold if is_active else QFont.Normal)
            painter.setFont(font)
            painter.setPen(color)
            painter.drawText(QRectF(x, 0, tab_w, header_h), Qt.AlignCenter, tab)

        content_rect = QRectF(8, header_h + 8, self.width() - 16, self.height() - header_h - 16)
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(content_rect, 6, 6)

        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(content_rect, Qt.AlignCenter, f"内容区域: {self._tabs[self._active] if self._active < len(self._tabs) else ''}")

        painter.end()

    def apply_theme(self):
        self.update()
