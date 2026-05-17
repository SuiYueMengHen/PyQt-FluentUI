from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentFloatingActionButton(QWidget, FluentWidgetBase):
    actionTriggered = Signal(str)
    _expand_progress = 0.0

    def __init__(self, icon_name: str = "plus", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._icon_name = icon_name
        self._actions: list[dict] = []
        self._is_expanded = False
        self._hovered = False
        self._hovered_action = -1
        self._btn_size = 48
        self.setFixedSize(200, 300)

        self._expand_anim = QPropertyAnimation(self, b"expand_progress")
        self._expand_anim.setDuration(250)
        self._expand_anim.setEasingCurve(QEasingCurve.OutCubic)

    def add_action(self, key: str, label: str, icon_name: str):
        self._actions.append({"key": key, "label": label, "icon": icon_name})
        self.update()

    def toggle_menu(self):
        self._is_expanded = not self._is_expanded
        self._expand_anim.stop()
        self._expand_anim.setStartValue(self._expand_progress)
        self._expand_anim.setEndValue(1.0 if self._is_expanded else 0.0)
        self._expand_anim.start()

    @Property(float)
    def expand_progress(self):
        return self._expand_progress

    @expand_progress.setter
    def expand_progress(self, value):
        self._expand_progress = value
        self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return super().mousePressEvent(event)

        btn_x = self.width() - self._btn_size - 8
        btn_y = self.height() - self._btn_size - 8
        btn_rect = QRectF(btn_x, btn_y, self._btn_size, self._btn_size)

        if btn_rect.contains(event.position()):
            self.toggle_menu()
            return super().mousePressEvent(event)

        if self._is_expanded:
            for i in range(len(self._actions)):
                action_y = btn_y - (len(self._actions) - i) * 40 - 8
                action_rect = QRectF(btn_x - 120, action_y, 160, 36)
                if action_rect.contains(event.position()):
                    self.actionTriggered.emit(self._actions[i]["key"])
                    self.toggle_menu()
                    return super().mousePressEvent(event)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self._hovered_action = -1
        btn_x = self.width() - self._btn_size - 8
        btn_y = self.height() - self._btn_size - 8
        btn_rect = QRectF(btn_x, btn_y, self._btn_size, self._btn_size)
        self._hovered = btn_rect.contains(event.position())

        if self._is_expanded:
            for i in range(len(self._actions)):
                action_y = btn_y - (len(self._actions) - i) * 40 - 8
                action_rect = QRectF(btn_x - 120, action_y, 160, 36)
                if action_rect.contains(event.position()):
                    self._hovered_action = i
                    break

        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._hovered_action = -1
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        btn_x = self.width() - self._btn_size - 8
        btn_y = self.height() - self._btn_size - 8
        btn_cx = btn_x + self._btn_size / 2
        btn_cy = btn_y + self._btn_size / 2

        if self._is_expanded and self._expand_progress > 0:
            overlay_alpha = int(100 * self._expand_progress)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0, overlay_alpha))
            painter.drawRect(self.rect())

        shadow_color = QColor(0, 0, 0, 40)
        for i in range(3):
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(shadow_color.red(), shadow_color.green(), shadow_color.blue(), shadow_color.alpha() - i * 10))
            painter.drawEllipse(QRectF(btn_x - i, btn_y - i, self._btn_size + i * 2, self._btn_size + i * 2))

        btn_color = QColor(tm.color("primary"))
        if self._hovered:
            btn_color = btn_color.lighter(110)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(btn_color))
        painter.drawEllipse(QRectF(btn_x, btn_y, self._btn_size, self._btn_size))

        icon = get_icon(self._icon_name, tm.color("primary_text_on"), 20)
        rotation = self._expand_progress * 45
        painter.save()
        painter.translate(btn_cx, btn_cy)
        painter.rotate(rotation)
        painter.translate(-btn_cx, -btn_cy)
        painter.drawPixmap(int(btn_cx - 10), int(btn_cy - 10), icon.pixmap(20, 20))
        painter.restore()

        if self._expand_progress > 0:
            for i, action in enumerate(self._actions):
                action_y = btn_y - (len(self._actions) - i) * 40 - 8
                alpha = min(255, int(255 * self._expand_progress))
                stagger = max(0, self._expand_progress - i * 0.1)
                if stagger <= 0:
                    continue

                action_rect = QRectF(btn_x - 120, action_y, 160, 36)
                bg = QColor(tm.color("bg_solid_card"))
                bg.setAlpha(alpha)
                if i == self._hovered_action:
                    bg = QColor(tm.color("bg_solid_tertiary"))
                    bg.setAlpha(alpha)

                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(bg))
                painter.drawRoundedRect(action_rect, tm.radius("sm"), tm.radius("sm"))

                icon = get_icon(action["icon"], tm.color("fg_primary"), 16)
                icon_alpha = min(255, int(255 * stagger))
                pm = icon.pixmap(16, 16)
                painter.drawPixmap(int(action_rect.x() + 10), int(action_rect.y() + 10), pm)

                font = QFont()
                font.setPixelSize(tm.font_size("body"))
                painter.setFont(font)
                text_color = QColor(tm.color("fg_primary"))
                text_color.setAlpha(alpha)
                painter.setPen(text_color)
                painter.drawText(QRectF(action_rect.x() + 32, action_rect.y(), action_rect.width() - 40, action_rect.height()),
                                 Qt.AlignVCenter | Qt.AlignLeft, action["label"])

        painter.end()

    def apply_theme(self):
        self.update()
