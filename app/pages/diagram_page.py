from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.display.fluent_separator import FluentSeparator
from app.components.diagrams.fluent_mind_map import FluentMindMap
from app.components.diagrams.fluent_flowchart import FluentFlowchart
from app.components.diagrams.fluent_org_chart import FluentOrgChart
from app.components.diagrams.fluent_fishbone import FluentFishbone
from app.components.diagrams.fluent_relation_graph import FluentRelationGraph
from app.components.diagrams.fluent_kanban_board import FluentKanbanBoard, KanbanCard
from app.components.diagrams.fluent_sankey_diagram import FluentSankeyDiagram
from app.components.diagrams.fluent_word_cloud import FluentWordCloud
from app.components.diagrams.fluent_timeline_chart import FluentTimelineChart
from app.components.diagrams.fluent_gauge import FluentGauge
from app.components.diagrams.fluent_chord_diagram import FluentChordDiagram
from app.theme.theme_manager import ThemeManager


class DiagramPage(QWidget, FluentWidgetBase):
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

        self._title = QLabel("图表 Diagrams")
        layout.addWidget(self._title)

        self._desc = QLabel("图表组件用于展示思维导图、流程图、组织架构图、鱼骨图、关系图、看板、桑基图、词云、时间轴、仪表盘、和弦图等结构化信息，共11种图表组件。支持悬停高亮、点击交互和丰富的动画效果。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._s1 = QLabel("思维导图 MindMap")
        layout.addWidget(self._s1)

        mind_map = FluentMindMap()
        mind_map.setMinimumHeight(320)
        mind_map.set_data({
            "text": "FluentUI",
            "children": [
                {"text": "按钮", "children": [
                    {"text": "基础按钮"},
                    {"text": "强调按钮"},
                    {"text": "图标按钮"},
                ]},
                {"text": "输入", "children": [
                    {"text": "文本框"},
                    {"text": "选择器"},
                    {"text": "滑块"},
                ]},
                {"text": "导航", "children": [
                    {"text": "标签栏"},
                    {"text": "面包屑"},
                    {"text": "步骤条"},
                ]},
                {"text": "反馈", "children": [
                    {"text": "进度条"},
                    {"text": "通知"},
                    {"text": "提示"},
                ]},
            ]
        })
        layout.addWidget(mind_map)

        layout.addWidget(FluentSeparator())

        self._s2 = QLabel("流程图 Flowchart")
        layout.addWidget(self._s2)

        flowchart = FluentFlowchart()
        flowchart.setMinimumHeight(350)
        start = flowchart.add_node("开始", "stadium")
        input_n = flowchart.add_node("输入数据", "parallelogram")
        process = flowchart.add_node("处理数据", "rect")
        decision = flowchart.add_node("是否有效?", "diamond")
        output_n = flowchart.add_node("输出结果", "parallelogram")
        end_n = flowchart.add_node("结束", "stadium")
        retry = flowchart.add_node("重试", "rounded")

        flowchart.add_edge(start, input_n)
        flowchart.add_edge(input_n, process)
        flowchart.add_edge(process, decision)
        flowchart.add_edge(decision, output_n, "是")
        flowchart.add_edge(decision, retry, "否")
        flowchart.add_edge(retry, input_n)
        flowchart.add_edge(output_n, end_n)
        flowchart.auto_layout()
        layout.addWidget(flowchart)

        layout.addWidget(FluentSeparator())

        self._s3 = QLabel("组织架构图 OrgChart")
        layout.addWidget(self._s3)

        org_chart = FluentOrgChart()
        org_chart.setMinimumHeight(320)
        org_chart.set_data({
            "name": "CEO", "title": "首席执行官",
            "children": [
                {"name": "CTO", "title": "技术总监", "children": [
                    {"name": "前端主管", "title": "前端开发"},
                    {"name": "后端主管", "title": "后端开发"},
                ]},
                {"name": "CFO", "title": "财务总监", "children": [
                    {"name": "会计主管", "title": "财务管理"},
                    {"name": "审计主管", "title": "审计合规"},
                ]},
                {"name": "COO", "title": "运营总监", "children": [
                    {"name": "市场主管", "title": "市场营销"},
                    {"name": "客服主管", "title": "客户服务"},
                ]},
            ]
        })
        layout.addWidget(org_chart)

        layout.addWidget(FluentSeparator())

        self._s4 = QLabel("鱼骨图 Fishbone")
        layout.addWidget(self._s4)

        fishbone = FluentFishbone()
        fishbone.setMinimumHeight(320)
        fishbone.set_data("产品质量", [
            {"name": "人员", "causes": ["培训不足", "经验欠缺", "态度问题"]},
            {"name": "机器", "causes": ["设备老化", "维护不当", "精度不够"]},
            {"name": "材料", "causes": ["供应商问题", "检验不严", "存储不当"]},
            {"name": "方法", "causes": ["流程缺陷", "标准不明", "操作不当"]},
            {"name": "环境", "causes": ["温度湿度", "洁净度差", "照明不足"]},
            {"name": "测量", "causes": ["仪器误差", "方法不当", "频率不够"]},
        ])
        layout.addWidget(fishbone)

        layout.addWidget(FluentSeparator())

        self._s5 = QLabel("关系图 RelationGraph")
        layout.addWidget(self._s5)

        relation = FluentRelationGraph()
        relation.setMinimumHeight(350)

        n0 = relation.add_node("用户", "group_a", 30)
        n1 = relation.add_node("订单", "group_b", 26)
        n2 = relation.add_node("商品", "group_b", 28)
        n3 = relation.add_node("支付", "group_c", 22)
        n4 = relation.add_node("物流", "group_c", 22)
        n5 = relation.add_node("评价", "group_a", 20)
        n6 = relation.add_node("库存", "group_b", 20)
        n7 = relation.add_node("客服", "group_a", 18)

        relation.add_edge(n0, n1, 2.0, "下单")
        relation.add_edge(n1, n2, 1.5, "包含")
        relation.add_edge(n1, n3, 2.0, "支付")
        relation.add_edge(n2, n6, 1.0, "扣减")
        relation.add_edge(n3, n4, 1.5, "发货")
        relation.add_edge(n0, n5, 1.0, "评价")
        relation.add_edge(n4, n5, 0.5, "签收")
        relation.add_edge(n0, n7, 0.8, "咨询")
        relation.add_edge(n2, n4, 0.5)
        relation.force_layout(50)
        layout.addWidget(relation)

        layout.addWidget(FluentSeparator())

        self._s6 = QLabel("看板 KanbanBoard")
        layout.addWidget(self._s6)

        kanban = FluentKanbanBoard()
        kanban.setMinimumHeight(350)

        todo_col = kanban.add_column("待办", "accent_warning")
        doing_col = kanban.add_column("进行中", "primary")
        done_col = kanban.add_column("已完成", "accent_success")

        todo_col.add_card(KanbanCard("1", "设计评审", "与团队讨论新功能方案", "设计", "accent_warning"))
        todo_col.add_card(KanbanCard("2", "编写文档", "更新API接口文档", "文档", "accent_info"))
        doing_col.add_card(KanbanCard("3", "开发登录页", "实现OAuth2.0认证", "开发", "primary"))
        done_col.add_card(KanbanCard("4", "环境配置", "搭建CI/CD流水线", "运维", "accent_success"))
        done_col.add_card(KanbanCard("5", "需求分析", "完成用户调研报告", "分析", "accent_info"))
        layout.addWidget(kanban)

        layout.addWidget(FluentSeparator())

        self._s7 = QLabel("桑基图 SankeyDiagram")
        layout.addWidget(self._s7)

        sankey = FluentSankeyDiagram()
        sankey.setMinimumHeight(300)
        s0 = sankey.add_node("能源总输入", 100, 0)
        s1 = sankey.add_node("电力", 40, 1)
        s2 = sankey.add_node("热力", 35, 1)
        s3 = sankey.add_node("交通", 25, 1)
        s4 = sankey.add_node("工业", 50, 2)
        s5 = sankey.add_node("民用", 30, 2)
        s6 = sankey.add_node("商业", 20, 2)
        sankey.add_link(s0, s1, 40)
        sankey.add_link(s0, s2, 35)
        sankey.add_link(s0, s3, 25)
        sankey.add_link(s1, s4, 20)
        sankey.add_link(s1, s5, 12)
        sankey.add_link(s1, s6, 8)
        sankey.add_link(s2, s4, 20)
        sankey.add_link(s2, s5, 10)
        sankey.add_link(s2, s6, 5)
        sankey.add_link(s3, s4, 10)
        sankey.add_link(s3, s5, 8)
        sankey.add_link(s3, s6, 7)
        sankey.auto_layout()
        layout.addWidget(sankey)

        layout.addWidget(FluentSeparator())

        self._s8 = QLabel("词云 WordCloud")
        layout.addWidget(self._s8)

        word_cloud = FluentWordCloud()
        word_cloud.setMinimumHeight(280)
        word_cloud.set_data([
            {"text": "Python", "weight": 100},
            {"text": "Qt", "weight": 80},
            {"text": "Fluent", "weight": 90},
            {"text": "UI", "weight": 70},
            {"text": "组件", "weight": 60},
            {"text": "主题", "weight": 50},
            {"text": "动画", "weight": 55},
            {"text": "图表", "weight": 65},
            {"text": "导航", "weight": 40},
            {"text": "按钮", "weight": 45},
            {"text": "输入", "weight": 35},
            {"text": "反馈", "weight": 30},
            {"text": "布局", "weight": 38},
            {"text": "样式", "weight": 42},
            {"text": "交互", "weight": 48},
            {"text": "响应式", "weight": 28},
            {"text": "暗色模式", "weight": 52},
            {"text": "图标", "weight": 33},
            {"text": "信号", "weight": 25},
            {"text": "属性", "weight": 22},
        ])
        layout.addWidget(word_cloud)

        layout.addWidget(FluentSeparator())

        self._s9 = QLabel("时间轴 TimelineChart")
        layout.addWidget(self._s9)

        timeline = FluentTimelineChart()
        timeline.setMinimumHeight(400)
        timeline.set_data([
            {"title": "项目启动", "description": "确定项目范围和目标", "date": "2024-01", "color_key": "accent_success"},
            {"title": "需求分析", "description": "完成用户调研和需求文档", "date": "2024-02", "color_key": "accent_info"},
            {"title": "设计阶段", "description": "UI设计和架构设计", "date": "2024-03", "color_key": "primary"},
            {"title": "开发阶段", "description": "前后端并行开发", "date": "2024-04", "color_key": "primary"},
            {"title": "测试发现严重Bug", "description": "需要修复后重新测试", "date": "2024-05", "color_key": "accent_error"},
            {"title": "修复完成", "description": "所有严重Bug已修复", "date": "2024-06", "color_key": "accent_success"},
            {"title": "上线发布", "description": "v1.0正式发布", "date": "2024-07", "color_key": "accent_success"},
        ])
        layout.addWidget(timeline)

        layout.addWidget(FluentSeparator())

        self._s10 = QLabel("仪表盘 Gauge")
        layout.addWidget(self._s10)

        gauge_row = QWidget()
        gauge_layout = QHBoxLayout(gauge_row)
        gauge_layout.setContentsMargins(0, 0, 0, 0)
        gauge_layout.setSpacing(16)

        gauge1 = FluentGauge()
        gauge1.setMinimumHeight(220)
        gauge1.setMinimumWidth(200)
        gauge1.set_label("CPU")
        gauge1.set_unit("%")
        gauge1.set_max_value(100)
        gauge1.add_segment(0, 60, "accent_success", "正常")
        gauge1.add_segment(60, 80, "accent_warning", "警告")
        gauge1.add_segment(80, 100, "accent_error", "危险")
        gauge1.set_value(72)
        gauge_layout.addWidget(gauge1)

        gauge2 = FluentGauge()
        gauge2.setMinimumHeight(220)
        gauge2.setMinimumWidth(200)
        gauge2.set_label("内存")
        gauge2.set_unit("GB")
        gauge2.set_max_value(64)
        gauge2.add_segment(0, 32, "accent_success", "正常")
        gauge2.add_segment(32, 48, "accent_warning", "警告")
        gauge2.add_segment(48, 64, "accent_error", "危险")
        gauge2.set_value(45)
        gauge_layout.addWidget(gauge2)

        gauge3 = FluentGauge()
        gauge3.setMinimumHeight(220)
        gauge3.setMinimumWidth(200)
        gauge3.set_label("磁盘")
        gauge3.set_unit("%")
        gauge3.set_max_value(100)
        gauge3.add_segment(0, 70, "accent_success", "正常")
        gauge3.add_segment(70, 90, "accent_warning", "警告")
        gauge3.add_segment(90, 100, "accent_error", "危险")
        gauge3.set_value(58)
        gauge_layout.addWidget(gauge3)

        layout.addWidget(gauge_row)

        layout.addWidget(FluentSeparator())

        self._s11 = QLabel("和弦图 ChordDiagram")
        layout.addWidget(self._s11)

        chord = FluentChordDiagram()
        chord.setMinimumHeight(350)
        c0 = chord.add_node("前端", 30)
        c1 = chord.add_node("后端", 35)
        c2 = chord.add_node("数据库", 25)
        c3 = chord.add_node("缓存", 20)
        c4 = chord.add_node("消息队列", 15)
        chord.add_link(c0, c1, 3.0)
        chord.add_link(c1, c2, 4.0)
        chord.add_link(c1, c3, 2.5)
        chord.add_link(c2, c3, 2.0)
        chord.add_link(c1, c4, 1.5)
        chord.add_link(c0, c3, 1.0)
        chord.add_link(c2, c4, 1.0)
        layout.addWidget(chord)

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
        for w in [self._s1, self._s2, self._s3, self._s4, self._s5, self._s6, self._s7, self._s8, self._s9, self._s10, self._s11]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
