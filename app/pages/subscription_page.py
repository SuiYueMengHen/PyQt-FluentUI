from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.surfaces.fluent_subscription_card import FluentSubscriptionCard
from app.components.display.fluent_separator import FluentSeparator
from app.theme.theme_manager import ThemeManager


class SubscriptionPage(QWidget, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        self._title = QLabel("会员订阅 Subscription")
        layout.addWidget(self._title)

        self._desc = QLabel("选择适合您的计划，解锁更多功能。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        cards_row = QHBoxLayout()
        cards_row.setSpacing(24)
        cards_row.setAlignment(Qt.AlignHCenter)

        free_features = [
            {"name": "基础组件访问", "included": True},
            {"name": "5个项目", "included": True},
            {"name": "1GB 存储空间", "included": True},
            {"name": "社区支持", "included": True},
            {"name": "高级图表", "included": False},
            {"name": "优先技术支持", "included": False},
        ]
        self._free_card = FluentSubscriptionCard("免费", "¥0", "/永久", free_features, False)
        cards_row.addWidget(self._free_card)

        pro_features = [
            {"name": "全部组件访问", "included": True},
            {"name": "无限项目", "included": True},
            {"name": "50GB 存储空间", "included": True},
            {"name": "邮件支持", "included": True},
            {"name": "高级图表", "included": True},
            {"name": "优先技术支持", "included": False},
        ]
        self._pro_card = FluentSubscriptionCard("专业版", "¥29", "/月", pro_features, True)
        cards_row.addWidget(self._pro_card)

        enterprise_features = [
            {"name": "全部组件访问", "included": True},
            {"name": "无限项目", "included": True},
            {"name": "无限存储空间", "included": True},
            {"name": "7×24 专属支持", "included": True},
            {"name": "高级图表", "included": True},
            {"name": "优先技术支持", "included": True},
        ]
        self._enterprise_card = FluentSubscriptionCard("企业版", "¥99", "/月", enterprise_features, False)
        cards_row.addWidget(self._enterprise_card)

        cards_row.addStretch()
        layout.addLayout(cards_row)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

        self._init_fluent_base()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background-color: {tm.color('bg_solid_base')};")
        self._title.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_large')}px; font-weight: 700; background: transparent;")
        self._desc.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent; line-height: 1.5;")
