from enum import Enum
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class NotificationPosition(Enum):
    TOP_RIGHT = "top_right"
    BOTTOM_RIGHT = "bottom_right"
    TOP_CENTER = "top_center"
    BOTTOM_CENTER = "bottom_center"


class FluentPositionalNotification(QWidget, FluentWidgetBase):
    closed = Signal()
    _slide_offset = 0.0
    _progress_width = 0.0

    def __init__(self, title: str = "", message: str = "", variant: str = "info",
                 position: NotificationPosition = NotificationPosition.TOP_RIGHT,
                 duration: int = 5000, parent=None):
        super().__init__(parent)
        self._title = title
        self._message = message
        self._variant = variant
        self._position = position
        self._duration = duration
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(360, 86)
        self.setCursor(Qt.PointingHandCursor)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        self._close_btn = QPushButton(self)
        self._close_btn.setFixedSize(20, 20)
        self._close_btn.move(self.width() - 28, 6)
        self._close_btn.setCursor(Qt.PointingHandCursor)
        self._close_btn.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self._close_btn.clicked.connect(self.dismiss)

        self._slide_anim = QPropertyAnimation(self, b"slide_offset")
        self._slide_anim.setDuration(300)
        self._slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._progress_anim = QPropertyAnimation(self, b"progress_width")
        self._progress_anim.setEasingCurve(QEasingCurve.Linear)

        self._dismiss_timer = QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.timeout.connect(self.dismiss)

        self._hover_pause = False
        self._remaining_duration = 0

        self._init_fluent_base()
        self._update_close_icon()

    def _update_close_icon(self):
        tm = self._tm
        icon = get_icon("close", tm.color("fg_tertiary"), 14)
        self._close_btn.setIcon(icon)
        self._close_btn.setIconSize(QSize(14, 14))

    def enterEvent(self, event):
        self._hover_pause = True
        if self._dismiss_timer.isActive():
            self._remaining_duration = self._dismiss_timer.remainingTime()
            self._dismiss_timer.stop()
        if self._progress_anim.state() == QPropertyAnimation.Running:
            self._progress_anim.pause()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_pause = False
        if self._remaining_duration > 0:
            self._dismiss_timer.start(self._remaining_duration)
        if self._progress_anim.state() == QPropertyAnimation.Paused:
            self._progress_anim.resume()
        super().leaveEvent(event)

    def show_notification(self):
        self._slide_anim.stop()
        if self._position in (NotificationPosition.TOP_RIGHT, NotificationPosition.BOTTOM_RIGHT):
            self._slide_anim.setStartValue(float(self.width()))
            self._slide_anim.setEndValue(0.0)
        elif self._position == NotificationPosition.TOP_CENTER:
            self._slide_anim.setStartValue(float(-self.height()))
            self._slide_anim.setEndValue(0.0)
        else:
            self._slide_anim.setStartValue(float(self.height()))
            self._slide_anim.setEndValue(0.0)
        self._slide_anim.start()

        self._progress_anim.stop()
        self._progress_width = float(self.width())
        self._progress_anim.setStartValue(float(self.width()))
        self._progress_anim.setEndValue(0.0)
        self._progress_anim.setDuration(self._duration)
        self._progress_anim.start()

        self._dismiss_timer.start(self._duration)
        self.show()

    def dismiss(self):
        self._progress_anim.stop()
        self._dismiss_timer.stop()
        self._slide_anim.stop()
        self._slide_anim.setStartValue(self._slide_offset)
        if self._position in (NotificationPosition.TOP_RIGHT, NotificationPosition.BOTTOM_RIGHT):
            self._slide_anim.setEndValue(float(self.width()))
        elif self._position == NotificationPosition.TOP_CENTER:
            self._slide_anim.setEndValue(float(-self.height()))
        else:
            self._slide_anim.setEndValue(float(self.height()))
        try:
            self._slide_anim.finished.disconnect(self._on_dismissed)
        except RuntimeError:
            pass
        self._slide_anim.finished.connect(self._on_dismissed)
        self._slide_anim.start()

    def _on_dismissed(self):
        self.closed.emit()
        self.hide()
        self.deleteLater()

    @Property(float)
    def slide_offset(self):
        return self._slide_offset

    @slide_offset.setter
    def slide_offset(self, v):
        self._slide_offset = v
        self._reposition()
        self.update()

    @Property(float)
    def progress_width(self):
        return self._progress_width

    @progress_width.setter
    def progress_width(self, v):
        self._progress_width = v
        self.update()

    def _reposition(self):
        parent = self.parent()
        if not parent:
            return
        manager = FluentNotificationManager()
        idx = manager.index_of(self._position, self)
        w, h = self.width(), self.height()
        gap = 8
        margin = 16

        if self._position == NotificationPosition.TOP_RIGHT:
            x = parent.width() - w - margin + self._slide_offset
            y = margin + idx * (h + gap)
        elif self._position == NotificationPosition.BOTTOM_RIGHT:
            x = parent.width() - w - margin + self._slide_offset
            y = parent.height() - (idx + 1) * (h + gap) - margin
        elif self._position == NotificationPosition.TOP_CENTER:
            x = (parent.width() - w) // 2
            y = margin + idx * (h + gap) + self._slide_offset
        else:
            x = (parent.width() - w) // 2
            y = parent.height() - (idx + 1) * (h + gap) - margin - self._slide_offset
        self.move(int(x), int(y))

    def mousePressEvent(self, event):
        self.dismiss()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        variant_colors = {
            "info": tm.color("primary"),
            "success": tm.color("accent_success"),
            "warning": tm.color("accent_warning"),
            "error": tm.color("accent_error"),
        }
        accent = QColor(variant_colors.get(self._variant, variant_colors["info"]))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        painter.setBrush(QBrush(accent))
        painter.drawRoundedRect(QRectF(0, 0, 3, self.height()), 2, 2)

        variant_icons = {
            "info": "info_circle",
            "success": "check_circle",
            "warning": "warning",
            "error": "error",
        }
        icon_name = variant_icons.get(self._variant, "info_circle")
        icon = get_icon(icon_name, accent.name(), 20)
        painter.drawPixmap(16, int((self.height() - 20) / 2) - 3, icon.pixmap(20, 20))

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(44, 12, self.width() - 80, 22), Qt.AlignLeft, self._title)

        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(QRectF(44, 36, self.width() - 80, 28), Qt.AlignLeft, self._message)

        if self._progress_width > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(accent))
            painter.drawRoundedRect(
                QRectF(3, self.height() - 3, max(self._progress_width - 3, 0), 3),
                1.5, 1.5,
            )

        painter.end()

    @staticmethod
    def self_check():
        from app.theme.theme_manager import ThemeManager
        from app.icons.icon_provider import get_icon
        tm = ThemeManager()
        errors = []
        for token in ["primary", "accent_success", "accent_warning", "accent_error",
                       "bg_solid_card", "stroke_card", "fg_primary", "fg_secondary", "fg_tertiary"]:
            try:
                tm.color(token)
            except Exception as e:
                errors.append(f"颜色token {token} 获取失败: {e}")
        for icon_name in ["info_circle", "check_circle", "warning", "error", "close"]:
            try:
                icon = get_icon(icon_name, "#000000", 20)
                if icon.isNull():
                    errors.append(f"图标 {icon_name} 加载失败")
            except Exception as e:
                errors.append(f"图标 {icon_name} 加载异常: {e}")
        if 360 < 100 or 360 > 800 or 86 < 30 or 86 > 200:
            errors.append("尺寸 fixedSize(360, 86) 不在合理范围内")
        if errors:
            return (False, "FluentPositionalNotification: " + "; ".join(errors))
        return (True, "FluentPositionalNotification: 所有检查项通过")

    def apply_theme(self):
        self._update_close_icon()
        self.update()


class FluentNotificationManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._notifications = {pos: [] for pos in NotificationPosition}
        return cls._instance

    def show(self, parent, title: str, message: str, variant: str = "info",
             position: NotificationPosition = NotificationPosition.TOP_RIGHT,
             duration: int = 5000) -> FluentPositionalNotification:
        notif = FluentPositionalNotification(title, message, variant, position, duration, parent)
        notif.closed.connect(lambda: self._on_notification_closed(position, notif))
        self._notifications[position].append(notif)
        notif._reposition()
        notif.show_notification()
        return notif

    def _on_notification_closed(self, position: NotificationPosition, notif: FluentPositionalNotification):
        if notif in self._notifications[position]:
            self._notifications[position].remove(notif)
        for n in self._notifications[position]:
            n._reposition()

    def index_of(self, position: NotificationPosition, notif: FluentPositionalNotification) -> int:
        try:
            return self._notifications[position].index(notif)
        except ValueError:
            return 0

    @classmethod
    def reset(cls):
        cls._instance = None
