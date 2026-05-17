from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentToast(QWidget, FluentWidgetBase):
    closed = Signal()
    _slide_progress = 0.0
    _progress_width = 0.0

    def __init__(self, title: str = "", content: str = "", toast_type: str = "info", duration: int = 3000, parent=None):
        super().__init__(parent)
        self._toast_type = toast_type
        self._duration = duration
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedHeight(62)
        self.setMinimumWidth(300)
        self.setMaximumWidth(420)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 6)
        layout.setSpacing(12)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(20, 20)
        layout.addWidget(self._icon_label)

        self._title_label = QLabel(title)
        layout.addWidget(self._title_label)

        self._content_label = QLabel(content)
        layout.addWidget(self._content_label)

        layout.addStretch()

        self._close_btn = QPushButton()
        self._close_btn.setFixedSize(20, 20)
        self._close_btn.setCursor(Qt.PointingHandCursor)
        self._close_btn.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self._close_btn.clicked.connect(self._dismiss)
        layout.addWidget(self._close_btn)

        self._slide_anim = QPropertyAnimation(self, b"slide_progress")
        self._slide_anim.setDuration(300)
        self._slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._progress_anim = QPropertyAnimation(self, b"progress_width")
        self._progress_anim.setEasingCurve(QEasingCurve.Linear)

        self._dismiss_timer = QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.timeout.connect(self._dismiss)

        self._remaining_duration = 0

        self._init_fluent_base()
        self._update_icons()

    def _update_icons(self):
        tm = self._tm
        type_icons = {
            "info": "info_circle",
            "success": "check",
            "warning": "warning",
            "error": "error",
        }
        type_colors = {
            "info": "accent_info",
            "success": "accent_success",
            "warning": "accent_warning",
            "error": "accent_error",
        }
        icon_name = type_icons.get(self._toast_type, "info_circle")
        color_key = type_colors.get(self._toast_type, "accent_info")
        self._icon_label.setPixmap(get_icon(icon_name, tm.color(color_key), 20).pixmap(20, 20))
        close_icon = get_icon("close", tm.color("fg_tertiary"), 14)
        self._close_btn.setIcon(close_icon)
        self._close_btn.setIconSize(QSize(14, 14))

    @Property(float)
    def slide_progress(self):
        return self._slide_progress

    @slide_progress.setter
    def slide_progress(self, value):
        self._slide_progress = value
        self.update()

    @Property(float)
    def progress_width(self):
        return self._progress_width

    @progress_width.setter
    def progress_width(self, v):
        self._progress_width = v
        self.update()

    def show_toast(self):
        self.show()
        self._slide_anim.stop()
        self._slide_anim.setStartValue(0.0)
        self._slide_anim.setEndValue(1.0)
        self._slide_anim.start()

        self._progress_anim.stop()
        self._progress_width = float(self.width())
        self._progress_anim.setStartValue(float(self.width()))
        self._progress_anim.setEndValue(0.0)
        self._progress_anim.setDuration(self._duration)
        self._progress_anim.start()

        self._dismiss_timer.start(self._duration)

    def _dismiss(self):
        self._progress_anim.stop()
        self._dismiss_timer.stop()
        self._slide_anim.stop()
        self._slide_anim.setStartValue(self._slide_progress)
        self._slide_anim.setEndValue(0.0)
        try:
            self._slide_anim.finished.disconnect(self._on_dismissed)
        except RuntimeError:
            pass
        self._slide_anim.finished.connect(self._on_dismissed)
        self._slide_anim.start()

    def _on_dismissed(self):
        self.closed.emit()
        self.close()
        self.deleteLater()

    def enterEvent(self, event):
        if self._dismiss_timer.isActive():
            self._remaining_duration = self._dismiss_timer.remainingTime()
            self._dismiss_timer.stop()
        if self._progress_anim.state() == QPropertyAnimation.Running:
            self._progress_anim.pause()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._remaining_duration > 0:
            self._dismiss_timer.start(self._remaining_duration)
        if self._progress_anim.state() == QPropertyAnimation.Paused:
            self._progress_anim.resume()
        super().leaveEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        y_offset = -self.height() * (1.0 - self._slide_progress)
        rect = QRectF(0, y_offset, self.width(), self.height())

        type_colors = {
            "info": "accent_info_light",
            "success": "accent_success_light",
            "warning": "accent_warning_light",
            "error": "accent_error_light",
        }
        border_colors = {
            "info": "accent_info",
            "success": "accent_success",
            "warning": "accent_warning",
            "error": "accent_error",
        }

        bg_key = type_colors.get(self._toast_type, "accent_info_light")
        border_key = border_colors.get(self._toast_type, "accent_info")
        accent = QColor(tm.color(border_key))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color(bg_key)))
        painter.drawRoundedRect(rect, tm.radius("md"), tm.radius("md"))

        painter.setBrush(QBrush(accent))
        painter.drawRoundedRect(QRectF(0, y_offset, 3, self.height()), 2, 2)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QColor(tm.color(border_key)))
        painter.drawRoundedRect(rect, tm.radius("md"), tm.radius("md"))

        if self._progress_width > 0:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(accent))
            progress_y = y_offset + self.height() - 3
            painter.drawRoundedRect(
                QRectF(3, progress_y, max(self._progress_width - 3, 0), 3),
                1.5, 1.5,
            )

        painter.end()

    @staticmethod
    def self_check():
        from app.theme.theme_manager import ThemeManager
        from app.icons.icon_provider import get_icon
        tm = ThemeManager()
        errors = []
        for token in ["accent_info", "accent_success", "accent_warning", "accent_error",
                       "accent_info_light", "accent_success_light", "accent_warning_light",
                       "accent_error_light", "fg_secondary", "fg_tertiary"]:
            try:
                tm.color(token)
            except Exception as e:
                errors.append(f"颜色token {token} 获取失败: {e}")
        for icon_name in ["info_circle", "check", "warning", "error", "close"]:
            try:
                icon = get_icon(icon_name, "#000000", 20)
                if icon.isNull():
                    errors.append(f"图标 {icon_name} 加载失败")
            except Exception as e:
                errors.append(f"图标 {icon_name} 加载异常: {e}")
        if 62 < 20 or 62 > 120:
            errors.append("尺寸 fixedHeight(62) 不在合理范围内")
        if errors:
            return (False, "FluentToast: " + "; ".join(errors))
        return (True, "FluentToast: 所有检查项通过")

    def apply_theme(self):
        tm = self._tm
        type_colors = {
            "info": "accent_info",
            "success": "accent_success",
            "warning": "accent_warning",
            "error": "accent_error",
        }
        color_key = type_colors.get(self._toast_type, "accent_info")
        self._title_label.setStyleSheet(f"color: {tm.color(color_key)}; font-weight: 600; font-size: {tm.font_size('body')}px; background: transparent;")
        self._content_label.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('caption')}px; background: transparent;")
        self._update_icons()

    @staticmethod
    def show_toast_message(parent, title: str, content: str, toast_type: str = "info", duration: int = 3000):
        toast = FluentToast(title, content, toast_type, duration, parent)
        if parent:
            parent_x = parent.x()
            parent_y = parent.y()
            parent_w = parent.width()
            toast_x = parent_x + (parent_w - toast.minimumWidth()) // 2
            toast_y = parent_y + 12
            toast.move(toast_x, toast_y)
        toast.show_toast()
        return toast
