from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentInfoBar(QWidget, FluentWidgetBase):
    closed = Signal()
    _slide_progress = 0.0

    def __init__(self, title: str = "", content: str = "", info_type: str = "info", parent=None):
        super().__init__(parent)
        self._info_type = info_type
        self.setFixedHeight(48)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(20, 20)
        layout.addWidget(self._icon_label)

        self._title_label = QLabel(title)
        self._title_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(self._title_label)

        self._content_label = QLabel(content)
        layout.addWidget(self._content_label)

        layout.addStretch()

        self._close_btn = QPushButton()
        self._close_btn.setFixedSize(28, 28)
        self._close_btn.setCursor(Qt.PointingHandCursor)
        self._close_btn.clicked.connect(self._on_close)
        layout.addWidget(self._close_btn)

        self._slide_anim = QPropertyAnimation(self, b"slide_progress")
        self._slide_anim.setDuration(300)
        self._slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._init_fluent_base()
        self._update_icons()

    @staticmethod
    def self_check():
        from app.theme.theme_manager import ThemeManager
        from app.icons.icon_provider import get_icon
        tm = ThemeManager()
        errors = []
        for token in ["primary", "accent_success", "accent_warning", "accent_error", "fg_primary", "fg_secondary", "bg_solid_card"]:
            try:
                tm.color(token)
            except Exception as e:
                errors.append(f"颜色token {token} 获取失败: {e}")
        for icon_name in ["info_circle", "check", "warning", "error"]:
            try:
                icon = get_icon(icon_name, "#000000", 20)
                if icon.isNull():
                    errors.append(f"图标 {icon_name} 加载失败")
            except Exception as e:
                errors.append(f"图标 {icon_name} 加载异常: {e}")
        if errors:
            return (False, "FluentInfoBar: " + "; ".join(errors))
        return (True, "FluentInfoBar: 所有检查项通过")

    def _on_close(self):
        self._slide_anim.stop()
        self._slide_anim.setStartValue(self._slide_progress)
        self._slide_anim.setEndValue(0.0)
        try:
            self._slide_anim.finished.disconnect(self.deleteLater)
        except RuntimeError:
            pass
        self._slide_anim.finished.connect(self.deleteLater)
        self._slide_anim.start()
        self.closed.emit()

    def show_animated(self):
        self.show()
        self._slide_anim.stop()
        self._slide_anim.setStartValue(0.0)
        self._slide_anim.setEndValue(1.0)
        self._slide_anim.start()

    @Property(float)
    def slide_progress(self):
        return self._slide_progress

    @slide_progress.setter
    def slide_progress(self, value):
        self._slide_progress = value
        self.setFixedHeight(int(48 * value))
        self.update()

    def _update_icons(self):
        tm = self._tm
        type_icons = {
            "info": "info_circle",
            "success": "check",
            "warning": "warning",
            "error": "error",
        }
        type_colors = {
            "info": ("accent_info", "accent_info_light"),
            "success": ("accent_success", "accent_success_light"),
            "warning": ("accent_warning", "accent_warning_light"),
            "error": ("accent_error", "accent_error_light"),
        }

        icon_name = type_icons.get(self._info_type, "info_circle")
        color_key, _ = type_colors.get(self._info_type, ("accent_info", "accent_info_light"))
        self._icon_label.setPixmap(get_icon(icon_name, tm.color(color_key), 20).pixmap(20, 20))
        self._close_btn.setIcon(get_icon("close", tm.color("fg_secondary"), 12))

    def apply_theme(self):
        tm = self._tm
        type_colors = {
            "info": ("accent_info", "accent_info_light"),
            "success": ("accent_success", "accent_success_light"),
            "warning": ("accent_warning", "accent_warning_light"),
            "error": ("accent_error", "accent_error_light"),
        }
        color_key, bg_key = type_colors.get(self._info_type, ("accent_info", "accent_info_light"))
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {tm.color(bg_key)};
                border: 1px solid {tm.color(color_key)};
                border-radius: {tm.radius('md')}px;
            }}
        """)
        self._title_label.setStyleSheet(f"color: {tm.color(color_key)}; font-weight: 600; font-size: {tm.font_size('body')}px; background: transparent;")
        self._content_label.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent;")
        self._close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('bg_solid_tertiary')};
            }}
        """)
        self._update_icons()
