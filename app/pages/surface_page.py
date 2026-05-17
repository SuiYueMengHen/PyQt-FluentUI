from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.surfaces.fluent_card import FluentCard
from app.components.surfaces.fluent_expander import FluentExpander
from app.components.surfaces.fluent_dialog import FluentDialog
from app.components.surfaces.fluent_drawer import FluentDrawer
from app.components.surfaces.fluent_collapse import FluentCollapse
from app.components.surfaces.fluent_group_box import FluentGroupBox
from app.components.surfaces.fluent_popover import FluentPopover
from app.components.surfaces.fluent_split_panel import FluentSplitPanel
from app.components.surfaces.fluent_tab_view import FluentTabView
from app.components.surfaces.fluent_flip_card import FluentFlipCard
from app.components.buttons.fluent_button import FluentButton
from app.components.buttons.fluent_accent_button import FluentAccentButton
from app.components.display.fluent_separator import FluentSeparator
from app.theme.theme_manager import ThemeManager


class SurfacePage(QWidget, FluentWidgetBase):
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

        self._title = QLabel("表面 Surfaces")
        layout.addWidget(self._title)

        self._desc = QLabel("表面组件用于承载内容和组织信息层级，共10种表面组件。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._s1 = QLabel("卡片 Card")
        layout.addWidget(self._s1)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        card1 = FluentCard()
        card1_layout = QVBoxLayout()
        card1_layout.setSpacing(8)
        card1_layout.addWidget(QLabel("基础卡片"))
        card1_layout.addWidget(QLabel("这是一个 Fluent 风格的卡片组件，具有圆角和微阴影。"))
        card1.set_content(QWidget())
        card1.layout().addLayout(card1_layout)
        cards_row.addWidget(card1, 1)

        card2 = FluentCard()
        card2_layout = QVBoxLayout()
        card2_layout.setSpacing(8)
        card2_layout.addWidget(QLabel("交互卡片"))
        card2_layout.addWidget(QLabel("鼠标悬停时卡片会有微妙的视觉反馈。"))
        card2_layout.addWidget(FluentAccentButton("了解更多"))
        card2.set_content(QWidget())
        card2.layout().addLayout(card2_layout)
        cards_row.addWidget(card2, 1)

        layout.addLayout(cards_row)

        layout.addWidget(FluentSeparator())

        self._s2 = QLabel("展开面板 Expander")
        layout.addWidget(self._s2)

        exp1 = FluentExpander("什么是 Fluent Design?")
        exp1_content = QLabel("Fluent Design System 是微软的设计语言，强调光效、深度、动效、材质和缩放五大核心元素。")
        exp1_content.setWordWrap(True)
        exp1.set_content_widget(exp1_content)

        exp2 = FluentExpander("如何切换主题?")
        exp2_content = QLabel("点击标题栏右侧的太阳/月亮图标即可在亮色和暗色主题之间切换。")
        exp2_content.setWordWrap(True)
        exp2.set_content_widget(exp2_content)

        layout.addWidget(exp1)
        layout.addWidget(exp2)

        layout.addWidget(FluentSeparator())

        self._s3 = QLabel("折叠面板 Collapse / 分组框 GroupBox")
        layout.addWidget(self._s3)

        for title in ["面板一", "面板二", "面板三"]:
            c = FluentCollapse(title)
            layout.addWidget(c)

        layout.addWidget(FluentGroupBox("用户信息"))

        layout.addWidget(FluentSeparator())

        self._s4 = QLabel("对话框 Dialog / 抽屉 Drawer")
        layout.addWidget(self._s4)

        dialog_row = QHBoxLayout()
        dialog_row.setSpacing(12)

        self._dialog_btn = FluentButton("打开对话框")
        self._dialog_btn.clicked.connect(self._show_dialog)
        dialog_row.addWidget(self._dialog_btn)

        self._left_drawer_btn = FluentButton("打开左侧抽屉")
        self._left_drawer_btn.clicked.connect(self._show_left_drawer)
        dialog_row.addWidget(self._left_drawer_btn)

        self._right_drawer_btn = FluentButton("打开右侧抽屉")
        self._right_drawer_btn.clicked.connect(self._show_right_drawer)
        dialog_row.addWidget(self._right_drawer_btn)

        dialog_row.addStretch()
        layout.addLayout(dialog_row)

        self._left_drawer = FluentDrawer("left", 280, self)
        left_content = QWidget()
        left_content.setStyleSheet("background: transparent;")
        left_layout = QVBoxLayout(left_content)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)
        left_layout.addWidget(QLabel("左侧导航"))
        left_layout.addWidget(QLabel("菜单项 1"))
        left_layout.addWidget(QLabel("菜单项 2"))
        left_layout.addWidget(QLabel("菜单项 3"))
        left_layout.addStretch()
        self._left_drawer.set_content(left_content)

        self._right_drawer = FluentDrawer("right", 280, self)
        right_content = QWidget()
        right_content.setStyleSheet("background: transparent;")
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)
        right_layout.addWidget(QLabel("属性面板"))
        right_layout.addWidget(QLabel("设置项 1"))
        right_layout.addWidget(QLabel("设置项 2"))
        right_layout.addStretch()
        self._right_drawer.set_content(right_content)

        layout.addWidget(FluentSeparator())

        self._s5 = QLabel("选项卡视图 TabView")
        layout.addWidget(self._s5)
        tab_view = FluentTabView(["概览", "详情", "设置"])
        layout.addWidget(tab_view)

        layout.addWidget(FluentSeparator())

        self._s6 = QLabel("分割面板 SplitPanel")
        layout.addWidget(self._s6)
        split = FluentSplitPanel("horizontal", 0.4)
        split.setFixedHeight(120)
        layout.addWidget(split)

        layout.addWidget(FluentSeparator())

        self._s7 = QLabel("翻转卡片 FlipCard")
        layout.addWidget(self._s7)
        flip_row = QHBoxLayout()
        flip_row.setSpacing(16)
        flip_row.addWidget(FluentFlipCard("点击翻转", "已翻转!"))
        flip_row.addWidget(FluentFlipCard("正面内容", "背面内容"))
        flip_row.addStretch()
        layout.addLayout(flip_row)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _show_dialog(self):
        dialog = FluentDialog("确认操作", "这是一个 Fluent 风格的对话框组件。您确定要执行此操作吗？", self)
        dialog.exec()

    def _show_left_drawer(self):
        self._left_drawer.open_drawer()

    def _show_right_drawer(self):
        self._right_drawer.open_drawer()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background-color: {tm.color('bg_solid_base')};")
        self._title.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_large')}px; font-weight: 700; background: transparent;")
        self._desc.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent; line-height: 1.5;")
        for w in [self._s1, self._s2, self._s3, self._s4, self._s5, self._s6, self._s7]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
