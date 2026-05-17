import random

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.display.fluent_avatar import FluentAvatar
from app.components.display.fluent_tag import FluentTag
from app.components.display.fluent_separator import FluentSeparator
from app.components.display.fluent_timeline import FluentTimeline
from app.components.display.fluent_carousel import FluentCarousel
from app.components.display.fluent_chip import FluentChip
from app.components.display.fluent_gauge import FluentGauge
from app.components.display.fluent_sparkline import FluentSparkline
from app.components.display.fluent_count_up import FluentCountUp
from app.components.display.fluent_descriptions import FluentDescriptions
from app.components.display.fluent_list import FluentList
from app.components.display.fluent_statistic import FluentStatistic
from app.components.display.fluent_tree import FluentTree, FluentTreeItem
from app.components.display.fluent_data_table import FluentDataTable
from app.components.display.fluent_image_viewer import FluentImageViewer
from app.components.display.fluent_qrcode import FluentQRCode
from app.components.display.fluent_calendar_heatmap import FluentCalendarHeatmap
from app.theme.theme_manager import ThemeManager


class DisplayPage(QWidget, FluentWidgetBase):
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

        self._title = QLabel("展示 Display")
        layout.addWidget(self._title)

        self._desc = QLabel("展示组件用于呈现用户信息、内容标签、数据可视化等，共17种展示组件。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._s1 = QLabel("头像 Avatar")
        layout.addWidget(self._s1)

        avatar_row = QHBoxLayout()
        avatar_row.setSpacing(16)
        av1 = FluentAvatar("张", 40)
        avatar_row.addWidget(av1)
        avatar_row.addWidget(QLabel("张三"))
        av2 = FluentAvatar("李", 48)
        av2.online = True
        avatar_row.addWidget(av2)
        avatar_row.addWidget(QLabel("李四 (在线)"))
        av3 = FluentAvatar("王", 56)
        avatar_row.addWidget(av3)
        avatar_row.addWidget(QLabel("王五"))
        avatar_row.addStretch()
        layout.addLayout(avatar_row)

        layout.addWidget(FluentSeparator())

        self._s2 = QLabel("标签 Tag / 芯片 Chip")
        layout.addWidget(self._s2)

        tag_row1 = QHBoxLayout()
        tag_row1.setSpacing(8)
        tag_row1.addWidget(FluentTag("默认"))
        tag_row1.addWidget(FluentTag("主要", "primary"))
        tag_row1.addWidget(FluentTag("成功", "success"))
        tag_row1.addWidget(FluentTag("警告", "warning"))
        tag_row1.addWidget(FluentTag("错误", "error"))
        tag_row1.addStretch()
        layout.addLayout(tag_row1)

        chip_row = QHBoxLayout()
        chip_row.setSpacing(8)
        chip_row.addWidget(FluentChip("默认芯片"))
        chip_row.addWidget(FluentChip("主要", variant="primary"))
        chip_row.addWidget(FluentChip("成功", variant="success", icon_name="check"))
        chip_row.addWidget(FluentChip("警告", variant="warning", closable=True))
        chip_row.addWidget(FluentChip("可选中", checkable=True, icon_name="star"))
        chip_row.addStretch()
        layout.addLayout(chip_row)

        layout.addWidget(FluentSeparator())

        self._s3 = QLabel("时间线 Timeline")
        layout.addWidget(self._s3)

        timeline_container = QWidget()
        timeline_container.setStyleSheet("background: transparent;")
        tl_layout = QHBoxLayout(timeline_container)
        tl_layout.setContentsMargins(0, 0, 0, 0)

        timeline = FluentTimeline()
        timeline.add_item("项目启动", "完成项目规划", "2024-01", "completed")
        timeline.add_item("设计阶段", "UI/UX 设计中", "2024-03", "completed")
        timeline.add_item("开发阶段", "前端开发进行中", "2024-06", "active")
        timeline.add_item("测试阶段", "待开始", "2024-09", "default")
        timeline.add_item("正式发布", "计划中", "2024-12", "default")
        tl_layout.addWidget(timeline)
        tl_layout.addStretch()
        layout.addWidget(timeline_container)

        layout.addWidget(FluentSeparator())

        self._s4 = QLabel("仪表盘 Gauge / 数字动画 CountUp / 统计数值 Statistic")
        layout.addWidget(self._s4)

        gauge_row = QHBoxLayout()
        gauge_row.setSpacing(24)

        gauge1 = FluentGauge(0, 100, "CPU")
        gauge1.value = 72
        gauge1.set_color_zones([
            {"min": 0, "max": 50, "color": "success"},
            {"min": 50, "max": 80, "color": "warning"},
            {"min": 80, "max": 100, "color": "error"},
        ])
        gauge_row.addWidget(gauge1)

        gauge2 = FluentGauge(0, 100, "内存")
        gauge2.value = 45
        gauge2.set_color_zones([
            {"min": 0, "max": 60, "color": "success"},
            {"min": 60, "max": 85, "color": "warning"},
            {"min": 85, "max": 100, "color": "error"},
        ])
        gauge_row.addWidget(gauge2)

        stat_container = QWidget()
        stat_container.setStyleSheet("background: transparent;")
        stat_layout = QVBoxLayout(stat_container)
        stat_layout.setContentsMargins(0, 0, 0, 0)
        stat_layout.setSpacing(8)

        stat1 = FluentStatistic(value=12847, title="活跃用户", suffix="人")
        stat_layout.addWidget(stat1)
        stat2 = FluentStatistic(value=99.9, title="可用率", suffix="%")
        stat_layout.addWidget(stat2)

        gauge_row.addWidget(stat_container)
        gauge_row.addStretch()
        layout.addLayout(gauge_row)

        layout.addWidget(FluentSeparator())

        self._s5 = QLabel("迷你图表 Sparkline")
        layout.addWidget(self._s5)

        spark_row = QHBoxLayout()
        spark_row.setSpacing(16)

        data1 = [random.uniform(20, 80) for _ in range(20)]
        spark1 = FluentSparkline(data1)
        spark1.data = data1
        spark_row.addWidget(spark1)

        data2 = [random.uniform(10, 90) for _ in range(20)]
        spark2 = FluentSparkline(data2)
        spark2.data = data2
        spark2.set_color("accent_success", "accent_error")
        spark_row.addWidget(spark2)

        spark_row.addStretch()
        layout.addLayout(spark_row)

        layout.addWidget(FluentSeparator())

        self._s6 = QLabel("轮播 Carousel")
        layout.addWidget(self._s6)

        carousel_container = QWidget()
        carousel_container.setStyleSheet("background: transparent;")
        carousel_layout = QHBoxLayout(carousel_container)
        carousel_layout.setContentsMargins(0, 0, 0, 0)

        carousel = FluentCarousel()
        for i, (color, text) in enumerate([("#0078D4", "页面 1 — 欢迎"), ("#107C10", "页面 2 — 组件"), ("#D83B01", "页面 3 — 动效"), ("#5C2D91", "页面 4 — 主题")]):
            page = QLabel(text)
            page.setAlignment(Qt.AlignCenter)
            page.setStyleSheet(f"background-color: {color}; color: white; font-size: 18px; border-radius: 8px;")
            carousel.add_page(page)
        carousel.set_auto_play(4000)
        carousel_layout.addWidget(carousel)
        layout.addWidget(carousel_container)

        layout.addWidget(FluentSeparator())

        self._s7 = QLabel("描述列表 Descriptions / 列表 List / 树形控件 Tree")
        layout.addWidget(self._s7)

        dlt_row = QHBoxLayout()
        dlt_row.setSpacing(16)

        desc = FluentDescriptions(data=[
            {"label": "用户名", "value": "张三"},
            {"label": "邮箱", "value": "zhangsan@example.com"},
            {"label": "角色", "value": "管理员"},
            {"label": "状态", "value": "在线"},
        ])
        dlt_row.addWidget(desc, 1)

        flist = FluentList()
        flist.set_data(["项目 A - 进行中", "项目 B - 已完成", "项目 C - 待开始", "项目 D - 进行中"])
        dlt_row.addWidget(flist, 1)

        tree = FluentTree()
        tree.set_data([
            FluentTreeItem("根节点", children=[
                FluentTreeItem("子节点 1", children=[
                    FluentTreeItem("叶子 1-1"),
                    FluentTreeItem("叶子 1-2"),
                ]),
                FluentTreeItem("子节点 2"),
            ]),
        ])
        dlt_row.addWidget(tree, 1)

        layout.addLayout(dlt_row)

        layout.addWidget(FluentSeparator())

        self._s8 = QLabel("数据表格 DataTable")
        layout.addWidget(self._s8)

        table = FluentDataTable()
        table.set_data(
            columns=[
                {"key": "name", "title": "姓名", "sortable": True},
                {"key": "age", "title": "年龄", "sortable": True},
                {"key": "role", "title": "角色"},
                {"key": "status", "title": "状态"},
            ],
            rows=[
                ["张三", 28, "管理员", "在线"],
                ["李四", 32, "编辑", "离线"],
                ["王五", 25, "用户", "在线"],
                ["赵六", 30, "编辑", "忙碌"],
            ]
        )
        layout.addWidget(table)

        layout.addWidget(FluentSeparator())

        self._s9 = QLabel("图片查看器 ImageViewer / 二维码 QRCode")
        layout.addWidget(self._s9)

        iv_qr_row = QHBoxLayout()
        iv_qr_row.setSpacing(24)
        iv_qr_row.addWidget(FluentImageViewer())
        iv_qr_row.addWidget(FluentQRCode("Hello FluentUI!", 160))
        iv_qr_row.addStretch()
        layout.addLayout(iv_qr_row)

        layout.addWidget(FluentSeparator())

        self._s10 = QLabel("日历热力图 CalendarHeatmap")
        layout.addWidget(self._s10)

        heatmap = FluentCalendarHeatmap()
        heatmap.generate_sample_data()
        layout.addWidget(heatmap)

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
        for w in [self._s1, self._s2, self._s3, self._s4, self._s5, self._s6, self._s7, self._s8, self._s9, self._s10]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
