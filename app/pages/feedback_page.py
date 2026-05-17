from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QPushButton, QTextEdit
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.feedback.fluent_progress_bar import FluentProgressBar
from app.components.feedback.fluent_progress_ring import FluentProgressRing
from app.components.feedback.fluent_badge import FluentBadge
from app.components.feedback.fluent_info_bar import FluentInfoBar
from app.components.feedback.fluent_toast import FluentToast
from app.components.feedback.fluent_skeleton import FluentSkeleton
from app.components.feedback.fluent_wave_progress import FluentWaveProgress
from app.components.feedback.fluent_empty import FluentEmpty
from app.components.feedback.fluent_notification import FluentNotification
from app.components.feedback.fluent_popconfirm import FluentPopconfirm
from app.components.feedback.fluent_result import FluentResult
from app.components.feedback.fluent_spinner import FluentSpinner
from app.components.feedback.fluent_state_indicator import FluentStateIndicator
from app.components.feedback.fluent_tooltip import FluentTooltip
from app.components.feedback.fluent_loading_screen import FluentLoadingScreen
from app.components.feedback.fluent_positional_notification import FluentPositionalNotification, FluentNotificationManager, NotificationPosition
from app.components.buttons.fluent_button import FluentButton
from app.components.display.fluent_separator import FluentSeparator
from app.theme.theme_manager import ThemeManager


class FeedbackPage(QWidget, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        self._title = QLabel("反馈 Feedback")
        layout.addWidget(self._title)

        self._desc = QLabel("反馈组件用于向用户传达操作状态和系统信息，共16种反馈组件。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._s1 = QLabel("进度条 Progress Bar / 环形进度 Progress Ring")
        layout.addWidget(self._s1)

        p1 = FluentProgressBar()
        p1.value = 65
        layout.addWidget(p1)

        p2 = FluentProgressBar()
        p2.indeterminate = True
        layout.addWidget(p2)

        ring_row = QHBoxLayout()
        ring_row.setSpacing(24)
        r1 = FluentProgressRing()
        r1.value = 75
        ring_row.addWidget(r1)
        r2 = FluentProgressRing()
        r2.indeterminate = True
        ring_row.addWidget(r2)
        ring_row.addStretch()
        layout.addLayout(ring_row)

        layout.addWidget(FluentSeparator())

        self._s2 = QLabel("徽章 Badge / 状态指示器 StateIndicator")
        layout.addWidget(self._s2)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(12)
        badge_row.addWidget(FluentBadge("默认"))
        badge_row.addWidget(FluentBadge("3", "primary"))
        badge_row.addWidget(FluentBadge("新", "success"))
        badge_row.addWidget(FluentBadge("!", "warning"))
        badge_row.addWidget(FluentBadge("99+", "error"))
        badge_row.addStretch()
        layout.addLayout(badge_row)

        state_row = QHBoxLayout()
        state_row.setSpacing(12)
        state_row.addWidget(FluentStateIndicator("online"))
        state_row.addWidget(QLabel("在线"))
        state_row.addWidget(FluentStateIndicator("busy"))
        state_row.addWidget(QLabel("忙碌"))
        state_row.addWidget(FluentStateIndicator("offline"))
        state_row.addWidget(QLabel("离线"))
        state_row.addStretch()
        layout.addLayout(state_row)

        layout.addWidget(FluentSeparator())

        self._s3 = QLabel("信息条 InfoBar / 通知 Toast")
        layout.addWidget(self._s3)

        self._info_container = QVBoxLayout()
        layout.addLayout(self._info_container)

        info_btn_row = QHBoxLayout()
        info_btn_row.setSpacing(12)
        for info_type, label in [("info", "信息"), ("success", "成功"), ("warning", "警告"), ("error", "错误")]:
            btn = FluentButton(label)
            btn.clicked.connect(lambda checked, t=info_type: self._show_info_bar(t))
            info_btn_row.addWidget(btn)
        info_btn_row.addStretch()
        layout.addLayout(info_btn_row)

        toast_btn_row = QHBoxLayout()
        toast_btn_row.setSpacing(12)
        for toast_type, label in [("info", "信息"), ("success", "成功"), ("warning", "警告"), ("error", "错误")]:
            btn = FluentButton(label)
            btn.clicked.connect(lambda checked, t=toast_type: self._show_toast(t))
            toast_btn_row.addWidget(btn)
        toast_btn_row.addStretch()
        layout.addLayout(toast_btn_row)

        layout.addWidget(FluentSeparator())

        self._s4 = QLabel("骨架屏 Skeleton / 加载动画 Spinner")
        layout.addWidget(self._s4)

        skeleton_container = QWidget()
        skeleton_container.setStyleSheet("background: transparent;")
        skeleton_layout = QVBoxLayout(skeleton_container)
        skeleton_layout.setContentsMargins(0, 0, 0, 0)
        skeleton_layout.setSpacing(12)

        skeleton_rect_row = QHBoxLayout()
        skeleton_rect_row.setSpacing(12)
        skeleton_rect_row.addWidget(FluentSkeleton("rect", 200, 20))
        skeleton_rect_row.addWidget(FluentSkeleton("rect", 120, 20))
        skeleton_rect_row.addStretch()
        skeleton_layout.addLayout(skeleton_rect_row)
        skeleton_layout.addWidget(FluentSkeleton("text", 300, 60))
        layout.addWidget(skeleton_container)

        spinner_row = QHBoxLayout()
        spinner_row.setSpacing(16)
        spinner_row.addWidget(FluentSpinner(24))
        spinner_row.addWidget(FluentSpinner(32))
        spinner_row.addWidget(FluentSpinner(48))
        spinner_row.addStretch()
        layout.addLayout(spinner_row)

        layout.addWidget(FluentSeparator())

        self._s5 = QLabel("波浪进度 WaveProgress")
        layout.addWidget(self._s5)

        wave_row = QHBoxLayout()
        wave_row.setSpacing(24)
        wp1 = FluentWaveProgress()
        wp1.value = 65
        wave_row.addWidget(wp1)
        wp2 = FluentWaveProgress()
        wp2.value = 30
        wave_row.addWidget(wp2)
        wp3 = FluentWaveProgress()
        wp3.value = 88
        wave_row.addWidget(wp3)
        wave_row.addStretch()
        layout.addLayout(wave_row)

        layout.addWidget(FluentSeparator())

        self._s6 = QLabel("空状态 Empty / 结果页 Result")
        layout.addWidget(self._s6)

        empty_result_row = QHBoxLayout()
        empty_result_row.setSpacing(16)
        empty = FluentEmpty("暂无数据", "请添加新内容后查看")
        empty_result_row.addWidget(empty, 1)

        result = FluentResult("success", "操作成功", "您的请求已成功处理")
        empty_result_row.addWidget(result, 1)
        layout.addLayout(empty_result_row)

        layout.addWidget(FluentSeparator())

        self._s7 = QLabel("气泡确认 Popconfirm / 提示 Tooltip")
        layout.addWidget(self._s7)

        pop_row = QHBoxLayout()
        pop_row.setSpacing(16)
        popconfirm = FluentPopconfirm("确定要删除吗？", "此操作不可撤销", self)
        pop_row.addWidget(popconfirm)

        tooltip_btn = FluentButton("悬停查看提示")
        tooltip_btn.setToolTip("这是一个工具提示")
        pop_row.addWidget(tooltip_btn)
        pop_row.addStretch()
        layout.addLayout(pop_row)

        layout.addWidget(FluentSeparator())

        self._s8 = QLabel("通知 Notification")
        layout.addWidget(self._s8)

        notif_row = QHBoxLayout()
        notif_row.setSpacing(12)
        for ntype, label in [("info", "信息通知"), ("success", "成功通知"), ("warning", "警告通知"), ("error", "错误通知")]:
            btn = FluentButton(label)
            btn.clicked.connect(lambda checked, t=ntype: self._show_notification(t))
            notif_row.addWidget(btn)
        notif_row.addStretch()
        layout.addLayout(notif_row)

        layout.addWidget(FluentSeparator())

        self._s9 = QLabel("多位置通知 Positional Notification")
        layout.addWidget(self._s9)

        pos_row1 = QHBoxLayout()
        pos_row1.setSpacing(12)
        for pos, label in [(NotificationPosition.TOP_RIGHT, "右上角"), (NotificationPosition.BOTTOM_RIGHT, "右下角")]:
            btn = FluentButton(label)
            btn.clicked.connect(lambda checked, p=pos: self._show_positional_notification(p))
            pos_row1.addWidget(btn)
        pos_row1.addStretch()
        layout.addLayout(pos_row1)

        pos_row2 = QHBoxLayout()
        pos_row2.setSpacing(12)
        for pos, label in [(NotificationPosition.TOP_CENTER, "顶部居中"), (NotificationPosition.BOTTOM_CENTER, "底部居中")]:
            btn = FluentButton(label)
            btn.clicked.connect(lambda checked, p=pos: self._show_positional_notification(p))
            pos_row2.addWidget(btn)
        pos_row2.addStretch()
        layout.addLayout(pos_row2)

        layout.addWidget(FluentSeparator())

        self._s10 = QLabel("组件自检 Self Check")
        layout.addWidget(self._s10)

        self._check_btn = FluentButton("运行自检")
        self._check_btn.clicked.connect(self._run_self_check)
        layout.addWidget(self._check_btn)

        self._check_result = QTextEdit()
        self._check_result.setReadOnly(True)
        self._check_result.setMaximumHeight(200)
        layout.addWidget(self._check_result)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _show_info_bar(self, info_type: str):
        titles = {"info": "提示", "success": "成功", "warning": "警告", "error": "错误"}
        contents = {
            "info": "这是一条信息提示。",
            "success": "操作已成功完成！",
            "warning": "请注意，此操作可能需要确认。",
            "error": "操作失败，请重试。",
        }
        bar = FluentInfoBar(titles.get(info_type, ""), contents.get(info_type, ""), info_type, self)
        self._info_container.addWidget(bar)
        bar.show_animated()

    def _show_toast(self, toast_type: str):
        titles = {"info": "提示", "success": "成功", "warning": "警告", "error": "错误"}
        contents = {
            "info": "这是一条信息通知。",
            "success": "操作已成功完成！",
            "warning": "请注意，此操作可能需要确认。",
            "error": "操作失败，请重试。",
        }
        FluentToast.show_toast_message(
            self.window(),
            titles.get(toast_type, ""),
            contents.get(toast_type, ""),
            toast_type,
        )

    def _show_notification(self, ntype: str):
        titles = {"info": "信息", "success": "成功", "warning": "警告", "error": "错误"}
        contents = {
            "info": "这是一条信息通知。",
            "success": "操作已成功完成！",
            "warning": "请注意，此操作可能需要确认。",
            "error": "操作失败，请重试。",
        }
        FluentNotification.show_notification(
            self.window(),
            titles.get(ntype, ""),
            contents.get(ntype, ""),
            ntype,
        )

    def _show_positional_notification(self, position: NotificationPosition):
        pos_names = {
            NotificationPosition.TOP_RIGHT: "右上角",
            NotificationPosition.BOTTOM_RIGHT: "右下角",
            NotificationPosition.TOP_CENTER: "顶部居中",
            NotificationPosition.BOTTOM_CENTER: "底部居中",
        }
        manager = FluentNotificationManager()
        manager.show(
            self.window(),
            "通知",
            f"这是一条来自{pos_names.get(position, '')}的通知。",
            "info",
            position,
        )

    def _run_self_check(self):
        from app.components.feedback.fluent_notification import FluentNotification
        from app.components.feedback.fluent_toast import FluentToast
        from app.components.feedback.fluent_positional_notification import FluentPositionalNotification
        from app.components.feedback.fluent_info_bar import FluentInfoBar
        from app.components.feedback.fluent_progress_bar import FluentProgressBar
        from app.components.feedback.fluent_progress_ring import FluentProgressRing
        from app.components.navigation.fluent_user_profile import FluentUserProfile
        from app.components.surfaces.fluent_subscription_card import FluentSubscriptionCard
        from app.components.surfaces.fluent_user_info_overlay import FluentUserInfoOverlay
        from app.icons.icon_provider import get_icon, get_pixmap, _cache, _svg_bytes_cache
        from app.theme.theme_manager import ThemeManager

        checks = [
            FluentNotification.self_check,
            FluentToast.self_check,
            FluentPositionalNotification.self_check,
            FluentInfoBar.self_check,
            FluentProgressBar.self_check,
            FluentProgressRing.self_check,
            FluentUserProfile.self_check,
            FluentSubscriptionCard.self_check,
            FluentUserInfoOverlay.self_check,
        ]
        results = []
        for check_fn in checks:
            try:
                ok, msg = check_fn()
                prefix = "✓" if ok else "✗"
                results.append(f"{prefix} {msg}")
            except Exception as e:
                results.append(f"✗ 自检异常: {e}")

        tm = ThemeManager()
        try:
            icon = get_icon("crown", "#0078D4", 20)
            results.append(f"{'✓' if not icon.isNull() else '✗'} 图标缓存: {len(_cache)} 个QIcon, {len(_svg_bytes_cache)} 个SVG字节缓存")
        except Exception as e:
            results.append(f"✗ 图标缓存检查异常: {e}")

        try:
            colors_ok = True
            missing = []
            for token in ["primary", "fg_primary", "fg_secondary", "bg_solid_base", "bg_solid_card", "stroke_card", "accent_success", "accent_warning", "accent_error"]:
                try:
                    tm.color(token)
                except Exception:
                    colors_ok = False
                    missing.append(token)
            if colors_ok:
                results.append("✓ 主题颜色系统: 9个核心token全部可用")
            else:
                results.append(f"✗ 主题颜色系统: 缺失 {', '.join(missing)}")
        except Exception as e:
            results.append(f"✗ 主题颜色检查异常: {e}")

        self._check_result.setPlainText("\n".join(results))

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background-color: {tm.color('bg_solid_base')};")
        self._title.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_large')}px; font-weight: 700; background: transparent;")
        self._desc.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent; line-height: 1.5;")
        for w in [self._s1, self._s2, self._s3, self._s4, self._s5, self._s6, self._s7, self._s8, self._s9, self._s10]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
        self._check_result.setStyleSheet(f"background-color: {tm.color('bg_solid_card')}; color: {tm.color('fg_primary')}; border: 1px solid {tm.color('stroke_card')}; border-radius: 6px; font-family: Consolas, monospace; font-size: 13px; padding: 8px;")
