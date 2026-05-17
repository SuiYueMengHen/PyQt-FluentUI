import random

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.display.fluent_separator import FluentSeparator
from app.components.charts.fluent_bar_chart import FluentBarChart
from app.components.charts.fluent_line_chart import FluentLineChart
from app.components.charts.fluent_pie_chart import FluentPieChart
from app.components.charts.fluent_donut_chart import FluentDonutChart
from app.components.charts.fluent_area_chart import FluentAreaChart
from app.components.charts.fluent_radar_chart import FluentRadarChart
from app.components.charts.fluent_scatter_chart import FluentScatterChart
from app.components.charts.fluent_heat_map import FluentHeatMap
from app.components.charts.fluent_treemap_chart import FluentTreemapChart
from app.components.charts.fluent_funnel_chart import FluentFunnelChart
from app.components.charts.fluent_waterfall_chart import FluentWaterfallChart
from app.components.charts.fluent_candlestick_chart import FluentCandlestickChart
from app.components.charts.fluent_bubble_chart import FluentBubbleChart
from app.components.charts.fluent_rose_chart import FluentRoseChart
from app.components.charts.fluent_gantt_chart import FluentGanttChart
from app.components.charts.fluent_bullet_chart import FluentBulletChart
from app.components.charts.fluent_radial_bar_chart import FluentRadialBarChart
from app.components.charts.fluent_stacked_bar_chart import FluentStackedBarChart
from app.components.charts.fluent_mixed_chart import FluentMixedChart
from app.components.charts.fluent_slope_chart import FluentSlopeChart
from app.theme.theme_manager import ThemeManager


class ChartPage(QWidget, FluentWidgetBase):
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

        self._title = QLabel("图表 Charts")
        layout.addWidget(self._title)

        self._desc = QLabel("专业的数据可视化图表组件，支持丰富的交互和动画效果。共20种图表类型，覆盖常见数据可视化场景。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._s1 = QLabel("柱状图 Bar Chart")
        layout.addWidget(self._s1)
        bar = FluentBarChart()
        bar.setFixedHeight(280)
        bar.set_data(
            ["1月", "2月", "3月", "4月", "5月", "6月"],
            [
                {"name": "收入", "data": [120, 200, 150, 80, 70, 110]},
                {"name": "支出", "data": [80, 120, 90, 60, 50, 80]},
            ]
        )
        layout.addWidget(bar)

        layout.addWidget(FluentSeparator())

        self._s2 = QLabel("折线图 Line Chart")
        layout.addWidget(self._s2)
        line = FluentLineChart()
        line.setFixedHeight(280)
        line.set_data(
            ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
            [
                {"name": "访问量", "data": [820, 932, 901, 934, 1290, 1330, 1320]},
                {"name": "注册量", "data": [220, 182, 191, 234, 290, 330, 310]},
            ]
        )
        layout.addWidget(line)

        layout.addWidget(FluentSeparator())

        self._s3 = QLabel("饼图 Pie Chart / 环形图 Donut Chart")
        layout.addWidget(self._s3)
        pie_row = QHBoxLayout()
        pie_row.setSpacing(24)

        pie = FluentPieChart()
        pie.setFixedSize(300, 300)
        pie.set_data([
            {"name": "直接访问", "value": 335},
            {"name": "邮件营销", "value": 210},
            {"name": "联盟广告", "value": 274},
            {"name": "视频广告", "value": 135},
            {"name": "搜索引擎", "value": 400},
        ])
        pie_row.addWidget(pie)

        donut = FluentDonutChart()
        donut.setFixedSize(300, 300)
        donut.set_data([
            {"name": "桌面端", "value": 45},
            {"name": "移动端", "value": 35},
            {"name": "平板", "value": 20},
        ], "100")
        pie_row.addWidget(donut)
        pie_row.addStretch()
        layout.addLayout(pie_row)

        layout.addWidget(FluentSeparator())

        self._s4 = QLabel("面积图 Area Chart")
        layout.addWidget(self._s4)
        area = FluentAreaChart()
        area.setFixedHeight(250)
        area.set_data(
            ["1月", "2月", "3月", "4月", "5月", "6月", "7月"],
            [
                {"name": "用户增长", "data": [140, 232, 101, 264, 90, 340, 250]},
                {"name": "活跃用户", "data": [120, 182, 191, 234, 290, 330, 310]},
            ]
        )
        layout.addWidget(area)

        layout.addWidget(FluentSeparator())

        self._s5 = QLabel("雷达图 Radar Chart")
        layout.addWidget(self._s5)
        radar = FluentRadarChart()
        radar.setFixedSize(300, 300)
        radar.set_data(
            ["销售", "管理", "技术", "客服", "研发", "市场"],
            [
                {"name": "预算分配", "data": [80, 60, 90, 70, 85, 75]},
                {"name": "实际开销", "data": [70, 75, 80, 65, 70, 80]},
            ]
        )
        layout.addWidget(radar)

        layout.addWidget(FluentSeparator())

        self._s6 = QLabel("散点图 Scatter Chart")
        layout.addWidget(self._s6)
        scatter = FluentScatterChart()
        scatter.setFixedHeight(250)
        scatter.set_data([
            {"name": "系列A", "data": [(random.uniform(10, 90), random.uniform(10, 90)) for _ in range(20)]},
            {"name": "系列B", "data": [(random.uniform(20, 80), random.uniform(20, 80)) for _ in range(15)]},
        ])
        layout.addWidget(scatter)

        layout.addWidget(FluentSeparator())

        self._s7 = QLabel("热力图 Heat Map")
        layout.addWidget(self._s7)
        heat = FluentHeatMap()
        heat.setFixedHeight(220)
        heat.set_data(
            [[random.randint(0, 100) for _ in range(7)] for _ in range(5)],
            ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
            ["上午", "中午", "下午", "傍晚", "夜间"],
        )
        layout.addWidget(heat)

        layout.addWidget(FluentSeparator())

        self._s8 = QLabel("矩形树图 Treemap / 漏斗图 Funnel")
        layout.addWidget(self._s8)
        tf_row = QHBoxLayout()
        tf_row.setSpacing(24)

        treemap = FluentTreemapChart()
        treemap.setFixedSize(300, 250)
        treemap.set_data([
            {"name": "技术", "value": 40},
            {"name": "市场", "value": 25},
            {"name": "运营", "value": 15},
            {"name": "设计", "value": 12},
            {"name": "人事", "value": 8},
        ])
        tf_row.addWidget(treemap)

        funnel = FluentFunnelChart()
        funnel.setFixedSize(250, 280)
        funnel.set_data([
            {"name": "展现", "value": 100},
            {"name": "点击", "value": 80},
            {"name": "访问", "value": 60},
            {"name": "咨询", "value": 40},
            {"name": "成交", "value": 20},
        ])
        tf_row.addWidget(funnel)
        tf_row.addStretch()
        layout.addLayout(tf_row)

        layout.addWidget(FluentSeparator())

        self._s9 = QLabel("瀑布图 Waterfall / K线图 Candlestick")
        layout.addWidget(self._s9)
        wc_row = QHBoxLayout()
        wc_row.setSpacing(24)

        waterfall = FluentWaterfallChart()
        waterfall.setFixedSize(350, 250)
        waterfall.set_data([
            {"name": "收入", "value": 100, "is_total": True},
            {"name": "工资", "value": -30},
            {"name": "租金", "value": -20},
            {"name": "其他", "value": -10},
            {"name": "结余", "value": 40, "is_total": True},
        ])
        wc_row.addWidget(waterfall)

        candle = FluentCandlestickChart()
        candle.setFixedSize(350, 250)
        candle.set_data([
            {"label": "3/1", "open": 20, "close": 25, "high": 28, "low": 18},
            {"label": "3/2", "open": 25, "close": 22, "high": 27, "low": 20},
            {"label": "3/3", "open": 22, "close": 28, "high": 30, "low": 21},
            {"label": "3/4", "open": 28, "close": 24, "high": 29, "low": 22},
            {"label": "3/5", "open": 24, "close": 30, "high": 32, "low": 23},
            {"label": "3/6", "open": 30, "close": 26, "high": 33, "low": 25},
            {"label": "3/7", "open": 26, "close": 32, "high": 35, "low": 24},
        ])
        wc_row.addWidget(candle)
        wc_row.addStretch()
        layout.addLayout(wc_row)

        layout.addWidget(FluentSeparator())

        self._s10 = QLabel("气泡图 Bubble Chart")
        layout.addWidget(self._s10)
        bubble = FluentBubbleChart()
        bubble.setFixedHeight(280)
        bubble.set_data([
            {"name": "产品A", "data": [(10, 30, 15), (25, 50, 25), (40, 70, 10), (60, 40, 20)]},
            {"name": "产品B", "data": [(15, 60, 20), (35, 35, 30), (55, 80, 15), (75, 55, 25)]},
        ])
        layout.addWidget(bubble)

        layout.addWidget(FluentSeparator())

        self._s11 = QLabel("玫瑰图 Rose Chart / 玉玦图 Radial Bar Chart")
        layout.addWidget(self._s11)
        rose_radial_row = QHBoxLayout()
        rose_radial_row.setSpacing(24)

        rose = FluentRoseChart()
        rose.setFixedSize(280, 280)
        rose.set_data([
            {"name": "销售", "value": 40},
            {"name": "管理", "value": 25},
            {"name": "技术", "value": 35},
            {"name": "客服", "value": 20},
            {"name": "研发", "value": 30},
            {"name": "市场", "value": 28},
        ])
        rose_radial_row.addWidget(rose)

        radial = FluentRadialBarChart()
        radial.setFixedSize(280, 280)
        radial.set_data([
            {"name": "完成率", "value": 85},
            {"name": "满意度", "value": 72},
            {"name": "增长率", "value": 58},
            {"name": "转化率", "value": 91},
        ])
        rose_radial_row.addWidget(radial)
        rose_radial_row.addStretch()
        layout.addLayout(rose_radial_row)

        layout.addWidget(FluentSeparator())

        self._s12 = QLabel("甘特图 Gantt Chart")
        layout.addWidget(self._s12)
        gantt = FluentGanttChart()
        gantt.set_data([
            {"name": "需求分析", "start": 1, "end": 5},
            {"name": "UI设计", "start": 3, "end": 8},
            {"name": "前端开发", "start": 6, "end": 14},
            {"name": "后端开发", "start": 7, "end": 16},
            {"name": "测试", "start": 13, "end": 18},
            {"name": "部署上线", "start": 17, "end": 20},
        ])
        layout.addWidget(gantt)

        layout.addWidget(FluentSeparator())

        self._s13 = QLabel("子弹图 Bullet Chart")
        layout.addWidget(self._s13)
        bullet = FluentBulletChart()
        bullet.set_data([
            {"name": "收入", "value": 75, "target": 85, "ranges": [50, 80, 100]},
            {"name": "利润", "value": 60, "target": 70, "ranges": [40, 65, 100]},
            {"name": "满意度", "value": 88, "target": 90, "ranges": [60, 80, 100]},
        ], max_val=100)
        layout.addWidget(bullet)

        layout.addWidget(FluentSeparator())

        self._s14 = QLabel("堆叠柱状图 Stacked Bar Chart")
        layout.addWidget(self._s14)
        stacked = FluentStackedBarChart()
        stacked.setFixedHeight(280)
        stacked.set_data(
            ["Q1", "Q2", "Q3", "Q4"],
            [
                {"name": "产品A", "data": [120, 200, 150, 180]},
                {"name": "产品B", "data": [80, 120, 90, 110]},
                {"name": "产品C", "data": [60, 80, 70, 90]},
            ]
        )
        layout.addWidget(stacked)

        layout.addWidget(FluentSeparator())

        self._s15 = QLabel("混合图表 Mixed Chart (柱+线)")
        layout.addWidget(self._s15)
        mixed = FluentMixedChart()
        mixed.setFixedHeight(280)
        mixed.set_data(
            ["1月", "2月", "3月", "4月", "5月", "6月"],
            bar_series=[
                {"name": "销售额", "data": [120, 200, 150, 80, 70, 110]},
            ],
            line_series=[
                {"name": "增长率", "data": [80, 130, 110, 60, 50, 95]},
            ]
        )
        layout.addWidget(mixed)

        layout.addWidget(FluentSeparator())

        self._s16 = QLabel("斜率图 Slope Chart")
        layout.addWidget(self._s16)
        slope = FluentSlopeChart()
        slope.setFixedHeight(280)
        slope.set_data([
            {"name": "产品A", "left": 30, "right": 65},
            {"name": "产品B", "left": 55, "right": 40},
            {"name": "产品C", "left": 80, "right": 90},
            {"name": "产品D", "left": 45, "right": 70},
            {"name": "产品E", "left": 70, "right": 50},
        ], left_label="2023年", right_label="2024年")
        layout.addWidget(slope)

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
        for w in [self._s1, self._s2, self._s3, self._s4, self._s5, self._s6, self._s7, self._s8, self._s9,
                  self._s10, self._s11, self._s12, self._s13, self._s14, self._s15, self._s16]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
