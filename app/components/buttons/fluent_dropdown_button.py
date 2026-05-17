from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentDropDownButton(QWidget, FluentWidgetBase):
    clicked = Signal(str)
    _hover_progress = 0.0

    def __init__(self, text: str = "选择", icon_name: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._text = text
        self._icon_name = icon_name
        self._items: list[str] = []
        self._selected = ""
        self.setFixedHeight(32)
        self.setMinimumWidth(100)
        self.setCursor(Qt.PointingHandCursor)

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    def add_item(self, text: str):
        self._items.append(text)

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, v):
        self._hover_progress = v
        self.update()

    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._show_menu()
        super().mousePressEvent(event)

    def _show_menu(self):
        if not self._items:
            return
        menu = QMenu(self)
        for item in self._items:
            action = menu.addAction(item)
            if item == self._selected:
                font = action.font()
                font.setBold(True)
                action.setFont(font)
            action.triggered.connect(lambda checked, t=item: self._select(t))
        pos = self.mapToGlobal(0, self.height())
        menu.exec(pos)

    def _select(self, text: str):
        self._selected = text
        self._text = text
        self.clicked.emit(text)
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        border_color = QColor(tm.color("stroke_card"))
        if self._hover_progress > 0.5:
            border_color = QColor(tm.color("primary"))

        bg = QColor(tm.color("bg_solid_card"))
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 4, 4)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        x = 10
        if self._icon_name:
            icon = get_icon(self._icon_name, tm.color("fg_secondary"), 14)
            painter.drawPixmap(x, int((self.height() - 14) / 2), icon.pixmap(14, 14))
            x += 18

        painter.drawText(QRectF(x, 0, self.width() - x - 24, self.height()), Qt.AlignVCenter | Qt.AlignLeft, self._text)

        arrow = get_icon("chevron_down", tm.color("fg_secondary"), 12)
        painter.drawPixmap(int(self.width() - 20), int((self.height() - 12) / 2), arrow.pixmap(12, 12))

        painter.end()

    def apply_theme(self):
        self.update()

    def sizeHint(self):
        font = QFont()
        font.setPixelSize(self._tm.font_size("body"))
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self._text)
        return QSize(max(100, text_width + 44), 32)
