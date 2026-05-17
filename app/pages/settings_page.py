from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.inputs.fluent_setting_row import FluentSettingRow
from app.components.display.fluent_separator import FluentSeparator
from app.theme.theme_manager import ThemeManager


class SettingsPage(QWidget, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        self._title = QLabel("设置 Settings")
        layout.addWidget(self._title)

        self._desc = QLabel("自定义您的应用偏好设置。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._s1 = QLabel("通知")
        layout.addWidget(self._s1)

        self._notif_row = FluentSettingRow("notifications", "推送通知", "switch", default_value=True)
        layout.addWidget(self._notif_row)

        self._sound_row = FluentSettingRow("volume", "提示音量", "slider", min_val=0, max_val=100, default_value=70)
        layout.addWidget(self._sound_row)

        self._badge_row = FluentSettingRow("tag", "消息角标", "switch", default_value=True)
        layout.addWidget(self._badge_row)

        layout.addWidget(FluentSeparator())

        self._s2 = QLabel("外观")
        layout.addWidget(self._s2)

        self._dark_row = FluentSettingRow("moon", "深色模式", "switch")
        layout.addWidget(self._dark_row)

        self._lang_row = FluentSettingRow("globe", "语言", "combo", options=["中文", "English", "日本語"])
        layout.addWidget(self._lang_row)

        self._anim_row = FluentSettingRow("sparkle", "动画效果", "switch", default_value=True)
        layout.addWidget(self._anim_row)

        layout.addWidget(FluentSeparator())

        self._s3 = QLabel("隐私")
        layout.addWidget(self._s3)

        self._lock_row = FluentSettingRow("lock", "应用锁", "switch", default_value=False)
        layout.addWidget(self._lock_row)

        self._eye_row = FluentSettingRow("eye_off", "隐身模式", "switch", default_value=False)
        layout.addWidget(self._eye_row)

        layout.addWidget(FluentSeparator())

        self._s4 = QLabel("存储")
        layout.addWidget(self._s4)

        self._cache_row = FluentSettingRow("download", "缓存大小", "slider", min_val=0, max_val=500, default_value=200)
        layout.addWidget(self._cache_row)

        self._auto_row = FluentSettingRow("upload", "自动同步", "switch", default_value=True)
        layout.addWidget(self._auto_row)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

        self._init_fluent_base()

        self._dark_row.value_changed.connect(self._on_dark_mode_changed)

    def _on_dark_mode_changed(self, value):
        tm = ThemeManager()
        if isinstance(value, bool) and value != tm.is_dark:
            tm.toggle_theme()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background-color: {tm.color('bg_solid_base')};")
        self._title.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_large')}px; font-weight: 700; background: transparent;")
        self._desc.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent;")
        for w in [self._s1, self._s2, self._s3, self._s4]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
        self._dark_row.set_value(tm.is_dark)
