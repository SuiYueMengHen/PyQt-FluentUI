from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QPushButton
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentNotification(QWidget, FluentWidgetBase):
    closed = Signal()
    _slide_x = 0.0
    _progress_width = 0.0

    def __init__(self, title: str = "", message: str = "", variant: str = "info", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._title = title
        self._message = message
        self._variant = variant
        self._duration = 5000
        self.setFixedSize(320, 78)
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
        self._update_close_icon()

        self._slide_anim = QPropertyAnimation(self, b"slide_x")
        self._slide_anim.setDuration(300)
        self._slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._progress_anim = QPropertyAnimation(self, b"progress_width")
        self._progress_anim.setEasingCurve(QEasingCurve.Linear)

        self._dismiss_timer = QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.timeout.connect(self.dismiss)

        self._remaining_duration = 0

    def _update_close_icon(self):
        tm = self._tm
        icon = get_icon("close", tm.color("fg_tertiary"), 14)
        self._close_btn.setIcon(icon)
        self._close_btn.setIconSize(QSize(14, 14))

    def _start_slide_in(self, duration: int = 5000):
        self._duration = duration
        self._slide_anim.stop()
        self._slide_anim.setStartValue(float(self.width()))
        self._slide_anim.setEndValue(0.0)
        self._slide_anim.start()

        self._progress_anim.stop()
        self._progress_width = float(self.width())
        self._progress_anim.setStartValue(float(self.width()))
        self._progress_anim.setEndValue(0.0)
        self._progress_anim.setDuration(duration)
        self._progress_anim.start()

        self._dismiss_timer.start(duration)
        self.show()

    def dismiss(self):
        self._progress_anim.stop()
        self._dismiss_timer.stop()
        self._slide_anim.stop()
        self._slide_anim.setStartValue(self._slide_x)
        self._slide_anim.setEndValue(float(self.width()))
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
    def slide_x(self):
        return self._slide_x

    @slide_x.setter
    def slide_x(self, v):
        self._slide_x = v
        if self.parent():
            self.move(int(self.parent().width() - self.width() - 16 + v), self.y())
        else:
            self.move(int(v), self.y())
        self.update()

    @Property(float)
    def progress_width(self):
        return self._progress_width

    @progress_width.setter
    def progress_width(self, v):
        self._progress_width = v
        self.update()

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

        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(16, 10, self.width() - 48, 22), Qt.AlignLeft, self._title)

        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.Normal)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_secondary")))
        painter.drawText(QRectF(16, 34, self.width() - 48, 28), Qt.AlignLeft, self._message)

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
        for icon_name in ["close"]:
            try:
                icon = get_icon(icon_name, "#000000", 14)
                if icon.isNull():
                    errors.append(f"图标 {icon_name} 加载失败")
            except Exception as e:
                errors.append(f"图标 {icon_name} 加载异常: {e}")
        if 320 < 100 or 320 > 800 or 78 < 30 or 78 > 200:
            errors.append("尺寸 fixedSize(320, 78) 不在合理范围内")
        if errors:
            return (False, "FluentNotification: " + "; ".join(errors))
        return (True, "FluentNotification: 所有检查项通过")

    def apply_theme(self):
        self._update_close_icon()
        self.update()

    @staticmethod
    def show_notification(parent, title: str = "", message: str = "", variant: str = "info", duration: int = 5000):
        notif = FluentNotification(title, message, variant, parent)
        if parent:
            x = parent.width() - notif.width() - 16
            y = 16
            notif.move(x, y)
        notif._start_slide_in(duration)
        return notif
