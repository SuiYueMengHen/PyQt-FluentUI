from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.surfaces.fluent_card import FluentCard
from app.components.buttons.fluent_accent_button import FluentAccentButton
from app.components.buttons.fluent_button import FluentButton
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager
from app.pages.animated_background import AnimatedBackground


class HeroFeatureCard(FluentCard):
    def __init__(self, icon_name: str, title: str, description: str, parent=None):
        super().__init__(parent)
        self._icon_name = icon_name
        self._title = title
        self._description = description
        self.setMinimumHeight(120)
        self.setCursor(Qt.PointingHandCursor)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(32, 32)
        self._inner_layout.addWidget(self._icon_label)

        self._title_label = QLabel(title)
        self._inner_layout.addWidget(self._title_label)

        self._desc_label = QLabel(description)
        self._desc_label.setWordWrap(True)
        self._inner_layout.addWidget(self._desc_label)

        self._update_style()

    def _update_style(self):
        tm = self._tm
        self._icon_label.setPixmap(get_icon(self._icon_name, tm.color("primary"), 32).pixmap(32, 32))
        self._title_label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
        self._desc_label.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent; line-height: 1.5;")

    def apply_theme(self):
        super().apply_theme()
        self._update_style()


class HeroPage(QWidget, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()

        self._animated_bg = AnimatedBackground(self)
        self._animated_bg.lower()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(32)

        hero_header = QWidget()
        hero_header_layout = QVBoxLayout(hero_header)
        hero_header_layout.setContentsMargins(0, 0, 0, 0)
        hero_header_layout.setSpacing(16)

        self._hero_title = QLabel("FluentUI Gallery")
        hero_header_layout.addWidget(self._hero_title)

        self._hero_subtitle = QLabel("基于 PySide6 构建的现代化 Fluent Design 风格组件库\n所有组件均为自制，支持亮色/暗色主题切换")
        self._hero_subtitle.setWordWrap(True)
        hero_header_layout.addWidget(self._hero_subtitle)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self._explore_btn = FluentAccentButton("浏览组件")
        btn_row.addWidget(self._explore_btn)

        self._theme_btn = FluentButton("切换主题")
        self._theme_btn.clicked.connect(self._toggle_theme)
        btn_row.addWidget(self._theme_btn)

        btn_row.addStretch()
        hero_header_layout.addLayout(btn_row)

        layout.addWidget(hero_header)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        features = [
            ("palette", "精美组件", "30+ 自制 Fluent 风格组件，覆盖按钮、输入、导航、反馈等场景"),
            ("sun", "主题切换", "内置亮色/暗色主题，一键切换，所有组件实时响应"),
            ("grid", "组件画廊", "完整的组件 Gallery 展示，交互式预览每个组件"),
            ("terminal", "现代设计", "遵循 Fluent Design System，圆角、阴影、动画一应俱全"),
        ]

        for icon, title, desc in features:
            card = HeroFeatureCard(icon, title, desc)
            cards_row.addWidget(card, 1)

        layout.addLayout(cards_row)
        layout.addStretch()

    def _toggle_theme(self):
        tm = self._tm
        tm.toggle_theme()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._animated_bg.setGeometry(0, 0, self.width(), self.height())

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background-color: {tm.color('bg_solid_base')};")
        self._hero_title.setStyleSheet(f"""
            color: {tm.color('fg_primary')};
            font-size: {tm.font_size('display')}px;
            font-weight: 700;
            background: transparent;
        """)
        self._hero_subtitle.setStyleSheet(f"""
            color: {tm.color('fg_secondary')};
            font-size: {tm.font_size('body')}px;
            background: transparent;
            line-height: 1.6;
        """)
