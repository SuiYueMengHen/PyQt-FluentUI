# 添加约50个专业组件计划

## 现有组件清单 (35个)

| 分类 | 已有组件 |
|------|---------|
| **按钮 (5)** | FluentButton, FluentAccentButton, FluentToggleButton, FluentHyperlink, FluentFAB |
| **输入 (14)** | FluentLineEdit, FluentTextArea, FluentPasswordEdit, FluentSearchEdit, FluentSpinBox, FluentComboBox, FluentCheckbox, FluentRadioButton, FluentSwitch, FluentSlider, FluentRating, FluentCalendar, FluentColorPicker, FluentToggleGroup |
| **导航 (6)** | FluentNavigation, FluentTabBar, FluentBreadcrumb, FluentPivot, FluentMenuBar, FluentTooltip |
| **表面 (4)** | FluentCard, FluentDialog, FluentDrawer, FluentExpander |
| **展示 (9)** | FluentAvatar, FluentTag, FluentSeparator, FluentTimeline, FluentCarousel, FluentChip, FluentGauge, FluentSparkline, FluentCountUp |
| **反馈 (7)** | FluentProgressBar, FluentProgressRing, FluentBadge, FluentInfoBar, FluentToast, FluentSkeleton, FluentWaveProgress |

## 新增组件计划 (约50个)

### 一、图表组件 (12个) — 新目录 `charts/`

| # | 组件名 | 描述 | 动效 |
|---|--------|------|------|
| 1 | FluentBarChart | 柱状图，支持多系列、堆叠 | 柱子从底部弹入 (OutBack) |
| 2 | FluentLineChart | 折线图，支持多系列、平滑曲线 | 线条从左到右绘制动画 |
| 3 | FluentPieChart | 饼图/环形图，支持标签 | 扇区旋转展开动画 |
| 4 | FluentDonutChart | 环形图，中心显示汇总值 | 扇区旋转展开 + 中心数字动画 |
| 5 | FluentAreaChart | 面积图，渐变填充 | 面积渐显动画 |
| 6 | FluentRadarChart | 雷达图，多维度对比 | 数据点从中心展开 |
| 7 | FluentScatterChart | 散点图 | 点逐个弹入 |
| 8 | FluentHeatMap | 热力图，矩阵色块 | 色块渐显 |
| 9 | FluentTreemapChart | 矩形树图 | 矩形缩放展开 |
| 10 | FluentFunnelChart | 漏斗图 | 从上到下依次展开 |
| 11 | FluentWaterfallChart | 瀑布图（涨跌柱状图） | 柱子逐个弹出 |
| 12 | FluentCandlestickChart | K线图（蜡烛图） | 从左到右绘制 |

### 二、按钮组件 (5个)

| # | 组件名 | 描述 | 动效 |
|---|--------|------|------|
| 13 | FluentIconButton | 纯图标按钮，圆形/方形 | 悬停缩放 + 涟漪 |
| 14 | FluentSplitButton | 下拉分割按钮（主操作+下拉菜单） | 下拉展开动画 |
| 15 | FluentCommandBarButton | 命令栏按钮（图标+文字+描述） | 悬停背景渐变 |
| 16 | FluentDropDownButton | 下拉选择按钮 | 下拉展开 + 选中动画 |
| 17 | FluentPillButton | 药丸形按钮（选中态填充） | 选中态滑入动画 |

### 三、输入组件 (8个)

| # | 组件名 | 描述 | 动效 |
|---|--------|------|------|
| 18 | FluentDateRangePicker | 日期范围选择器 | 日历面板滑入 |
| 19 | FluentTimePicker | 时间选择器（时/分/分滚轮） | 滚轮滑动 |
| 20 | FluentNumericInput | 数字输入框（带增减按钮） | 数值滚动动画 |
| 21 | FluentMultiSelect | 多选下拉（标签模式） | 标签弹入 + 下拉展开 |
| 22 | FluentTreeSelect | 树形选择器 | 节点展开/折叠 |
| 23 | FluentCascader | 级联选择器 | 面板逐级滑入 |
| 24 | FluentTransfer | 穿梭框（左右双列表） | 项滑入动画 |
| 25 | FluentRateRange | 范围滑块（双滑块） | 滑块跟随 + 选中区域高亮 |

### 四、导航组件 (5个)

| # | 组件名 | 描述 | 动效 |
|---|--------|------|------|
| 26 | FluentSteps | 步骤条（水平/垂直） | 当前步骤指示器滑动 |
| 27 | FluentPagination | 分页器 | 页码切换过渡 |
| 28 | FluentAnchor | 锚点导航（右侧快速定位） | 指示器滑动 |
| 29 | FluentBackTop | 回到顶部按钮 | 滚动显隐 + 点击平滑滚动 |
| 30 | FluentCommandBar | 命令栏（搜索+操作按钮组） | 搜索框展开/收起 |

### 五、表面组件 (5个)

| # | 组件名 | 描述 | 动效 |
|---|--------|------|------|
| 31 | FluentPopover | 气泡弹出框 | 缩放+淡入 |
| 32 | FluentCollapse | 折叠面板（手风琴） | 内容展开/收起动画 |
| 33 | FluentSplitPanel | 分割面板（可拖拽分割线） | 分割线拖拽 |
| 34 | FluentGroupBox | 分组框 | 边框渐变 |
| 35 | FluentTabView | 选项卡视图（内容区切换） | 内容淡入切换 |

### 六、展示组件 (8个)

| # | 组件名 | 描述 | 动效 |
|---|--------|------|------|
| 36 | FluentDataTable | 数据表格（排序/选择） | 行悬停高亮 |
| 37 | FluentStatistic | 统计数值卡片 | 数值滚动动画 |
| 38 | FluentTree | 树形控件 | 节点展开/折叠动画 |
| 39 | FluentList | 列表控件（虚拟滚动） | 项交错入场 |
| 40 | FluentDescriptions | 描述列表（键值对） | 无特殊动效 |
| 41 | FluentImageViewer | 图片查看器（缩放/旋转） | 缩放/旋转动画 |
| 42 | FluentQRCode | 二维码展示 | 无特殊动效 |
| 43 | FluentLottie | Lottie 动画播放器 | 动画播放 |

### 七、反馈组件 (7个)

| # | 组件名 | 描述 | 动效 |
|---|--------|------|------|
| 44 | FluentResult | 结果页（成功/失败/警告） | 图标弹入 + 文字淡入 |
| 45 | FluentEmpty | 空状态占位 | 插图淡入 + 微动画 |
| 46 | FluentLoadingScreen | 全屏加载 | 旋转 + 脉冲 |
| 47 | FluentNotification | 通知提醒（右上角） | 从右侧滑入 |
| 48 | FluentPopconfirm | 气泡确认框 | 缩放+淡入 |
| 49 | FluentSpinner | 旋转加载指示器（多种样式） | 旋转/脉冲/弹跳 |
| 50 | FluentStateIndicator | 状态指示器（在线/离线/忙碌） | 状态切换动画 |

### 八、新增图标 (约30个)

补充专业图表和UI所需的图标：
activity, bar_chart, bell, briefcase, check_circle, chevron_up, code, columns, cpu, credit_card, cross, download_cloud, external_link, file, git_branch, grid_3x3, hash, indent, layers, layout_grid, maximize, menu, minimize, monitor, move, package, percent, pie_chart, plus_circle, rotate

## 新增页面

| 页面 | 描述 |
|------|------|
| chart_page.py | 图表组件展示页（12个图表组件） |

## 实施策略

### 分批实施（每批约10个组件）

**批次1 — 图表核心 (12个图表组件)**
- 创建 `charts/` 目录
- 实现 12 个图表组件
- 创建 chart_page.py 展示页
- 在导航中添加"图表"入口

**批次2 — 按钮+输入 (13个)**
- 5 个按钮组件
- 8 个输入组件

**批次3 — 导航+表面 (10个)**
- 5 个导航组件
- 5 个表面组件

**批次4 — 展示+反馈 (15个)**
- 8 个展示组件
- 7 个反馈组件

**批次5 — 图标+集成**
- 30 个新 SVG 图标
- 更新所有 Gallery 页面
- 更新 main.py 导航
- 全量测试验证

### 技术规范

1. **所有组件遵循 FluentWidgetBase 模式**：继承 QWidget + FluentWidgetBase，调用 _init_fluent_base()
2. **透明背景**：setAttribute(Qt.WA_TranslucentBackground)
3. **主题支持**：每个组件实现 apply_theme()
4. **动画标准**：
   - 微交互：150-300ms，OutCubic
   - 进入动画：300-500ms，OutBack/OutCubic
   - 退出动画：200-300ms，InCubic
   - 使用 QPropertyAnimation + 自定义 Property
5. **图表绘制**：使用 QPainter + QPainterPath 自绘，不依赖 QtCharts 模块
6. **图标**：SVG 格式，currentColor，1.5px 描边，20x20 viewBox
7. **悬停/按下反馈**：所有可交互组件必须有视觉反馈
8. **无白色背景**：所有自绘组件 paintEvent 开头 fillRect(Qt.transparent)

### 文件结构

```
app/
├── components/
│   ├── charts/          # 新增目录
│   │   ├── __init__.py
│   │   ├── fluent_bar_chart.py
│   │   ├── fluent_line_chart.py
│   │   ├── fluent_pie_chart.py
│   │   ├── fluent_donut_chart.py
│   │   ├── fluent_area_chart.py
│   │   ├── fluent_radar_chart.py
│   │   ├── fluent_scatter_chart.py
│   │   ├── fluent_heat_map.py
│   │   ├── fluent_treemap_chart.py
│   │   ├── fluent_funnel_chart.py
│   │   ├── fluent_waterfall_chart.py
│   │   └── fluent_candlestick_chart.py
│   ├── buttons/         # 新增5个
│   ├── inputs/          # 新增8个
│   ├── navigation/      # 新增5个
│   ├── surfaces/        # 新增5个
│   ├── display/         # 新增8个
│   └── feedback/        # 新增7个
├── pages/
│   └── chart_page.py    # 新增
└── icons/svg/           # 新增30个
```
