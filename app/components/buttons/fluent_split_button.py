from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QMenu
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentSplitButton(QWidget, FluentWidgetBase):
    clicked = Signal()
    menuTriggered = Signal(str)
    _hover_progress = 0.0

    def __init__(self, text: str = "操作", icon_name: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._text = text
        self._icon_name = icon_name
        self._menu_items: list[str] = []
        self._hovered_main = False
        self._hovered_arrow = False
        self.setFixedHeight(32)
        self.setMinimumWidth(100)
        self.setCursor(Qt.PointingHandCursor)

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    def add_menu_item(self, text: str):
        self._menu_items.append(text)

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, v):
        self._hover_progress = v
        self.update()

    def _main_rect(self):
        return QRectF(0, 0, self.width() - 28, self.height())

    def _arrow_rect(self):
        return QRectF(self.width() - 28, 0, 28, self.height())

    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered_main = False
        self._hovered_arrow = False
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        self._hovered_main = self._main_rect().contains(event.position())
        self._hovered_arrow = self._arrow_rect().contains(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._arrow_rect().contains(event.position()):
                self._show_menu()
            elif self._main_rect().contains(event.position()):
                self.clicked.emit()
        super().mousePressEvent(event)

    def _show_menu(self):
        if not self._menu_items:
            return
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { border-radius: 6px; padding: 4px; }")
        for item in self._menu_items:
            action = menu.addAction(item)
            action.triggered.connect(lambda checked, t=item: self.menuTriggered.emit(t))
        pos = self.mapToGlobal(int(self._arrow_rect().bottomLeft().x()), int(self._arrow_rect().bottomLeft().y()))
        menu.exec(pos)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        main_rect = self._main_rect()
        arrow_rect = self._arrow_rect()

        bg = QColor(tm.color("primary"))
        bg_hover = QColor(tm.color("primary")).lighter(110)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_hover if self._hovered_main else bg))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 4, 4)

        painter.setPen(QPen(QColor(tm.color("primary")).darker(110), 1))
        painter.drawLine(int(arrow_rect.left()), 6, int(arrow_rect.left()), int(self.height() - 6))

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("primary_text_on")))

        x_offset = 10
        if self._icon_name:
            icon = get_icon(self._icon_name, tm.color("primary_text_on"), 14)
            painter.drawPixmap(x_offset, int((self.height() - 14) / 2), icon.pixmap(14, 14))
            x_offset += 18

        painter.drawText(QRectF(x_offset, 0, main_rect.width() - x_offset - 4, self.height()), Qt.AlignVCenter | Qt.AlignLeft, self._text)

        arrow_icon = get_icon("chevron_down", tm.color("primary_text_on"), 12)
        painter.drawPixmap(int(arrow_rect.center().x() - 6), int(arrow_rect.center().y() - 6), arrow_icon.pixmap(12, 12))

        painter.end()

    def apply_theme(self):
        self.update()
