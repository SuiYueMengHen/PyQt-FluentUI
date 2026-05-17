from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.navigation.fluent_breadcrumb import FluentBreadcrumb
from app.components.navigation.fluent_tab_bar import FluentTabBar
from app.components.navigation.fluent_pivot import FluentPivot
from app.components.navigation.fluent_menu_bar import FluentMenuBar
from app.components.navigation.fluent_pagination import FluentPagination
from app.components.navigation.fluent_steps import FluentSteps
from app.components.navigation.fluent_anchor import FluentAnchor
from app.components.navigation.fluent_back_top import FluentBackTop
from app.components.navigation.fluent_command_bar import FluentCommandBar
from app.components.display.fluent_separator import FluentSeparator
from app.theme.theme_manager import ThemeManager


class NavigationPage(QWidget, FluentWidgetBase):
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

        self._title = QLabel("导航 Navigation")
        layout.addWidget(self._title)

        self._desc = QLabel("导航组件用于在应用内进行页面切换和层级定位，共11种导航组件。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._s1 = QLabel("面包屑 Breadcrumb")
        layout.addWidget(self._s1)
        layout.addWidget(FluentBreadcrumb(["首页", "组件", "导航", "面包屑"]))

        layout.addWidget(FluentSeparator())

        self._s2 = QLabel("标签栏 Tab Bar")
        layout.addWidget(self._s2)
        layout.addWidget(FluentTabBar(["全部", "进行中", "已完成", "已取消"]))

        layout.addSpacing(16)

        self._s3 = QLabel("枢轴切换 Pivot")
        layout.addWidget(self._s3)
        layout.addWidget(FluentPivot(["概览", "详情", "统计", "设置"]))

        layout.addWidget(FluentSeparator())

        self._s4 = QLabel("菜单栏 Menu Bar")
        layout.addWidget(self._s4)

        menu_bar = FluentMenuBar()
        menu_bar.add_menu("文件", [
            {"text": "新建", "shortcut": "Ctrl+N"},
            {"text": "打开", "shortcut": "Ctrl+O"},
            {"separator": True},
            {"text": "保存", "shortcut": "Ctrl+S"},
            {"text": "另存为", "shortcut": "Ctrl+Shift+S"},
        ])
        menu_bar.add_menu("编辑", [
            {"text": "撤销", "shortcut": "Ctrl+Z"},
            {"text": "重做", "shortcut": "Ctrl+Y"},
            {"separator": True},
            {"text": "剪切", "shortcut": "Ctrl+X"},
            {"text": "复制", "shortcut": "Ctrl+C"},
            {"text": "粘贴", "shortcut": "Ctrl+V"},
        ])
        menu_bar.add_menu("视图", [
            {"text": "放大", "shortcut": "Ctrl++"},
            {"text": "缩小", "shortcut": "Ctrl+-"},
            {"separator": True},
            {"text": "全屏", "shortcut": "F11"},
        ])
        layout.addWidget(menu_bar)

        layout.addWidget(FluentSeparator())

        self._s5 = QLabel("分页 Pagination")
        layout.addWidget(self._s5)
        pagination = FluentPagination(total=100, current=1, page_size=10)
        layout.addWidget(pagination)

        layout.addWidget(FluentSeparator())

        self._s6 = QLabel("步骤条 Steps")
        layout.addWidget(self._s6)
        steps = FluentSteps(items=[
            {"title": "选择配置", "description": "选择基础配置"},
            {"title": "编辑模板", "description": "自定义模板内容"},
            {"title": "预览确认", "description": "预览并确认"},
            {"title": "完成", "description": "创建完成"},
        ])
        steps.set_current(1)
        layout.addWidget(steps)

        layout.addWidget(FluentSeparator())

        self._s7 = QLabel("锚点导航 Anchor")
        layout.addWidget(self._s7)
        anchor_row = QHBoxLayout()
        anchor = FluentAnchor()
        anchor.set_items([
            {"key": "basic", "text": "基础用法"},
            {"key": "advanced", "text": "高级设置"},
            {"key": "api", "text": "API 文档"},
            {"key": "faq", "text": "常见问题"},
        ])
        anchor_row.addWidget(anchor)
        anchor_row.addStretch()
        layout.addLayout(anchor_row)

        layout.addWidget(FluentSeparator())

        self._s8 = QLabel("回到顶部 BackTop / 命令栏 CommandBar")
        layout.addWidget(self._s8)
        cmd_bar = FluentCommandBar()
        cmd_bar.add_action("home", "首页")
        cmd_bar.add_action("settings", "设置")
        cmd_bar.add_action("bell", "通知")
        layout.addWidget(cmd_bar)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background-color: {tm.color('bg_solid_base')};")
        self._title.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_large')}px; font-weight: 700; background: transparent;")
        self._desc.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent; line-height: 1.5;")
        for w in [self._s1, self._s2, self._s3, self._s4, self._s5, self._s6, self._s7, self._s8]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
