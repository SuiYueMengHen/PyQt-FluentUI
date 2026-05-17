from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentPagination(QWidget, FluentWidgetBase):
    pageChanged = Signal(int)
    _hovered = -1

    def __init__(self, total: int = 1, current: int = 1, page_size: int = 10, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._total_items = total
        self._current = current
        self._page_size = page_size
        self._btn_size = 32
        self.setFixedHeight(self._btn_size)
        self.setCursor(Qt.PointingHandCursor)

    @property
    def total_pages(self):
        return max(1, (self._total_items + self._page_size - 1) // self._page_size)

    def set_total(self, total: int):
        self._total_items = total
        self.update()

    def set_current(self, page: int):
        if 1 <= page <= self.total_pages:
            self._current = page
            self.pageChanged.emit(page)
            self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return super().mousePressEvent(event)
        x = event.position().x()
        btn = self._btn_size
        gap = 4
        if x < btn:
            self.set_current(max(1, self._current - 1))
            return
        offset = btn + gap
        for p in self._visible_pages():
            pw = btn if p != "..." else 24
            if offset <= x <= offset + pw:
                if isinstance(p, int):
                    self.set_current(p)
                return
            offset += pw + gap
        if x >= offset:
            self.set_current(min(self.total_pages, self._current + 1))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        x = event.position().x()
        btn = self._btn_size
        gap = 4
        self._hovered = -2
        if x < btn:
            self._hovered = -1
        offset = btn + gap
        for i, p in enumerate(self._visible_pages()):
            pw = btn if p != "..." else 24
            if offset <= x <= offset + pw:
                self._hovered = i
                break
            offset += pw + gap
        if x >= offset:
            self._hovered = -3
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = -2
        self.update()
        super().leaveEvent(event)

    def _visible_pages(self):
        tp = self.total_pages
        if tp <= 7:
            return list(range(1, tp + 1))
        pages = [1]
        if self._current > 3:
            pages.append("...")
        for p in range(max(2, self._current - 1), min(tp, self._current + 2)):
            pages.append(p)
        if self._current < tp - 2:
            pages.append("...")
        pages.append(tp)
        return pages

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        btn = self._btn_size
        gap = 4
        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        x = 0
        self._draw_nav_btn(painter, x, "<", self._hovered == -1 and self._current > 1, self._current <= 1)
        x += btn + gap

        for i, p in enumerate(self._visible_pages()):
            if p == "...":
                painter.setPen(QColor(tm.color("fg_tertiary")))
                painter.drawText(QRectF(x, 0, 24, btn), Qt.AlignCenter, "...")
                x += 24 + gap
            else:
                is_current = p == self._current
                is_hovered = self._hovered == i
                self._draw_page_btn(painter, x, str(p), is_current, is_hovered)
                x += btn + gap

        self._draw_nav_btn(painter, x, ">", self._hovered == -3 and self._current < self.total_pages, self._current >= self.total_pages)

        painter.end()

    def _draw_nav_btn(self, painter, x, text, hovered, disabled):
        tm = self._tm
        btn = self._btn_size
        r = QRectF(x, 0, btn, btn)
        bg = QColor(tm.color("bg_solid_tertiary")) if not disabled else QColor(tm.color("bg_solid_base"))
        if hovered and not disabled:
            bg = QColor(tm.color("primary_light"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(r, 4, 4)
        painter.setPen(QColor(tm.color("fg_tertiary") if disabled else tm.color("fg_primary")))
        painter.drawText(r, Qt.AlignCenter, text)

    def _draw_page_btn(self, painter, x, text, is_current, is_hovered):
        tm = self._tm
        btn = self._btn_size
        r = QRectF(x, 0, btn, btn)
        if is_current:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(tm.color("primary"))))
            painter.drawRoundedRect(r, 4, 4)
            painter.setPen(QColor(tm.color("primary_text_on")))
        elif is_hovered:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(tm.color("primary_light"))))
            painter.drawRoundedRect(r, 4, 4)
            painter.setPen(QColor(tm.color("primary")))
        else:
            painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(r, Qt.AlignCenter, text)

    def apply_theme(self):
        self.update()
