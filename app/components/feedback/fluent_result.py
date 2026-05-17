from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentResult(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, status: str = "success", title: str = "", subtitle: str = "", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._status = status
        self._title = title or {"success": "操作成功", "error": "操作失败", "warning": "警告", "info": "提示"}.get(status, "")
        self._subtitle = subtitle
        self.setFixedSize(280, 200)

        self._anim = None
        QTimer.singleShot(50, self._start_anim)

    def _start_anim(self):
        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(500)
        self._anim.setEasingCurve(QEasingCurve.OutBack)
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

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        status_config = {
            "success": {"icon": "check", "color": "accent_success"},
            "error": {"icon": "close", "color": "accent_error"},
            "warning": {"icon": "warning", "color": "accent_warning"},
            "info": {"icon": "info", "color": "primary"},
        }
        config = status_config.get(self._status, status_config["info"])
        color = QColor(tm.color(config["color"]))

        scale = self._anim_progress
        icon_size = 48
        cx = self.width() / 2
        cy = 50

        painter.save()
        painter.translate(cx, cy)
        painter.scale(scale, scale)

        painter.setPen(Qt.NoPen)
        bg = QColor(color)
        bg.setAlpha(30)
        painter.setBrush(QBrush(bg))
        painter.drawEllipse(QRectF(-icon_size / 2 - 8, -icon_size / 2 - 8, icon_size + 16, icon_size + 16))

        painter.setBrush(QBrush(color))
        painter.drawEllipse(QRectF(-icon_size / 2, -icon_size / 2, icon_size, icon_size))

        icon = get_icon(config["icon"], "#FFFFFF", 24)
        painter.drawPixmap(-12, -12, icon.pixmap(24, 24))
        painter.restore()

        font = QFont()
        font.setPixelSize(tm.font_size("title_medium"))
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(0, 90, self.width(), 30), Qt.AlignCenter, self._title)

        if self._subtitle:
            font.setPixelSize(tm.font_size("body"))
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(0, 120, self.width(), 24), Qt.AlignCenter, self._subtitle)

        painter.end()

    def apply_theme(self):
        self.update()
