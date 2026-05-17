from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPixmap

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon, get_pixmap
from app.theme.theme_manager import ThemeManager
from app.components.inputs.fluent_setting_row import FluentSettingRow


class FluentUserInfoOverlay(QWidget, FluentWidgetBase):
    closed = Signal()
    opened = Signal()
    theme_btn_clicked = Signal()
    _slide_progress = 0.0

    def __init__(self, username: str = "Fluent User", role: str = "Free",
                 email: str = "user@fluent.ui", parent=None):
        super().__init__(parent)
        self._username = username
        self._role = role
        self._email = email
        self._drawer_width = 320
        self._is_open = False
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        self.hide()

        self._panel = QWidget(self)
        self._panel.setFixedWidth(self._drawer_width)
        self._panel.setAutoFillBackground(False)

        panel_layout = QVBoxLayout(self._panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        panel_layout.setSpacing(16)

        close_row = QHBoxLayout()
        close_row.addStretch()
        self._close_btn = QPushButton()
        self._close_btn.setFixedSize(32, 32)
        self._close_btn.setCursor(Qt.PointingHandCursor)
        self._close_btn.clicked.connect(self.close_overlay)
        close_row.addWidget(self._close_btn)
        panel_layout.addLayout(close_row)

        self._avatar_label = QLabel()
        self._avatar_label.setFixedSize(72, 72)
        self._avatar_label.setAlignment(Qt.AlignCenter)
        self._avatar_label.setStyleSheet("background: transparent;")
        panel_layout.addWidget(self._avatar_label, 0, Qt.AlignHCenter)

        self._name_label = QLabel(username)
        self._name_label.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(self._name_label)

        self._role_label = QLabel(role)
        self._role_label.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(self._role_label)

        self._email_label = QLabel(email)
        self._email_label.setAlignment(Qt.AlignCenter)
        panel_layout.addWidget(self._email_label)

        from app.components.display.fluent_separator import FluentSeparator
        panel_layout.addWidget(FluentSeparator())

        self._notif_row = FluentSettingRow(icon_name="notifications", label="通知", control="switch")
        self._notif_row.value_changed.connect(lambda v: None)
        panel_layout.addWidget(self._notif_row)

        self._volume_row = FluentSettingRow(icon_name="volume", label="音量", control="slider", min_val=0, max_val=100, default_value=80)
        self._volume_row.value_changed.connect(lambda v: None)
        panel_layout.addWidget(self._volume_row)

        self._lang_row = FluentSettingRow(icon_name="globe", label="语言", control="combo", options=["中文", "English", "日本語"])
        self._lang_row.value_changed.connect(lambda v: None)
        panel_layout.addWidget(self._lang_row)

        self._dark_mode_row = FluentSettingRow(icon_name="moon", label="深色模式", control="switch")
        self._dark_mode_row.value_changed.connect(lambda v: self.theme_btn_clicked.emit())
        panel_layout.addWidget(self._dark_mode_row)

        self._logout_btn = QPushButton("  退出登录")
        self._logout_btn.setCursor(Qt.PointingHandCursor)
        self._logout_btn.setFixedHeight(36)
        panel_layout.addWidget(self._logout_btn)

        panel_layout.addStretch()

        self._slide_anim = QPropertyAnimation(self, b"slide_progress")
        self._slide_anim.setDuration(300)
        self._slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._init_fluent_base()
        self._generate_avatar()

    def _generate_avatar(self):
        tm = self._tm
        pm = get_pixmap("user", tm.color("primary"), 72)
        if not pm.isNull():
            from app.components.navigation.fluent_user_profile import _clip_circle_pixmap
            clipped = _clip_circle_pixmap(pm, 72)
            self._avatar_label.setPixmap(clipped)
        else:
            fallback = QPixmap(72, 72)
            fallback.fill(QColor(tm.color("primary")))
            from app.components.navigation.fluent_user_profile import _clip_circle_pixmap
            clipped = _clip_circle_pixmap(fallback, 72)
            self._avatar_label.setPixmap(clipped)

    @Property(float)
    def slide_progress(self):
        return self._slide_progress

    @slide_progress.setter
    def slide_progress(self, value):
        self._slide_progress = value
        self._update_geometry()
        self.update()

    def open_overlay(self):
        self._is_open = True
        self.show()
        self.raise_()
        self._update_geometry()
        self._dark_mode_row.set_value(self._tm.is_dark)
        self._slide_anim.stop()
        self._slide_anim.setStartValue(self._slide_progress)
        self._slide_anim.setEndValue(1.0)
        self._slide_anim.start()
        self.opened.emit()

    def close_overlay(self):
        self._is_open = False
        self._slide_anim.stop()
        self._slide_anim.setStartValue(self._slide_progress)
        self._slide_anim.setEndValue(0.0)
        try:
            self._slide_anim.finished.disconnect(self._on_closed)
        except RuntimeError:
            pass
        self._slide_anim.finished.connect(self._on_closed)
        self._slide_anim.start()

    def _on_closed(self):
        try:
            self._slide_anim.finished.disconnect(self._on_closed)
        except RuntimeError:
            pass
        self.hide()
        self.closed.emit()

    def _update_geometry(self):
        if not self.parent():
            return
        parent_rect = self.parent().rect()
        self.setGeometry(parent_rect)
        x = -self._drawer_width + self._drawer_width * self._slide_progress
        self._panel.setGeometry(int(x), 0, self._drawer_width, self.height())

    def resizeEvent(self, event):
        self._update_geometry()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        panel_rect = self._panel.geometry()
        if not panel_rect.contains(event.pos()):
            self.close_overlay()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        overlay_alpha = int(255 * 0.4 * self._slide_progress)
        painter.setBrush(QColor(0, 0, 0, overlay_alpha))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        panel_rect = QRectF(self._panel.geometry())
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(panel_rect, 0, 0)

        painter.end()

    @staticmethod
    def self_check():
        from app.theme.theme_manager import ThemeManager
        from app.icons.icon_provider import get_icon
        tm = ThemeManager()
        errors = []
        for token in ["primary", "fg_primary", "fg_secondary", "bg_solid_card", "stroke_card", "nav_item_hover", "stroke_hover", "accent_error"]:
            try:
                tm.color(token)
            except Exception as e:
                errors.append(f"颜色token {token} 获取失败: {e}")
        for icon_name in ["close", "lock", "user"]:
            try:
                icon = get_icon(icon_name, "#000000", 20)
                if icon.isNull():
                    errors.append(f"图标 {icon_name} 加载失败")
            except Exception as e:
                errors.append(f"图标 {icon_name} 加载异常: {e}")
        row_ok, row_msg = FluentSettingRow.self_check()
        if not row_ok:
            errors.append(row_msg)
        if errors:
            return (False, "FluentUserInfoOverlay: " + "; ".join(errors))
        return (True, "FluentUserInfoOverlay: 所有检查项通过")

    def apply_theme(self):
        tm = self._tm
        self._panel.setStyleSheet("QWidget { background-color: transparent; }")

        self._close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('nav_item_hover')};
            }}
        """)
        self._close_btn.setIcon(get_icon("close", tm.color("fg_secondary"), 14))

        self._name_label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: 20px; font-weight: 700; background: transparent;")
        self._role_label.setStyleSheet(f"color: {tm.color('primary')}; font-size: {tm.font_size('body')}px; font-weight: 500; background: transparent;")
        self._email_label.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('caption')}px; background: transparent;")

        self._notif_row.apply_theme()
        self._volume_row.apply_theme()
        self._lang_row.apply_theme()
        self._dark_mode_row.apply_theme()

        self._logout_btn.setIcon(get_icon("lock", tm.color("accent_error"), 16))
        self._logout_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 1px solid {tm.color('accent_error')};
                border-radius: {tm.radius('md')}px;
                color: {tm.color('accent_error')};
                font-size: {tm.font_size('body')}px;
                text-align: left;
                padding-left: 12px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('accent_error')}22;
            }}
        """)

        self._generate_avatar()
        self.update()
