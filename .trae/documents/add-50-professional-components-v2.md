# 添加约50个专业组件 — 完整实施计划

## 当前状态总结

### 已有组件 (原始35个 + 新增33个 = 68个组件文件)

| 分类 | 原始组件 | 新增已创建 | 新增未创建 | Gallery集成状态 |
|------|---------|-----------|-----------|----------------|
| 图表 (12) | 0 | 12 (全部) | 0 | ✅ 已集成到 chart_page |
| 按钮 (11) | 5 | 6 | 0 | ❌ 6个未集成 |
| 输入 (14+8) | 14 | 0 | 8 | ✅ 原始14已集成 |
| 导航 (6+3) | 6 | 2 | 3 | ❌ 2个未集成 |
| 表面 (4+3) | 4 | 2 | 3 | ❌ 2个未集成 |
| 展示 (9+4) | 9 | 4 | 4 | ❌ 4个未集成 |
| 反馈 (7+7) | 7 | 7 | 1 | ❌ 7个未集成 |

**关键问题**：
- 22个已创建组件未集成到Gallery页面
- 19个计划组件尚未创建文件
- 需要更多图表类型满足"大量图表"需求

---

## 新增组件计划 (19个待创建 + 12个额外新增 = 31个新组件)

### 一、输入组件 (8个 — 来自原计划)

| # | 组件名 | 文件名 | 描述 | 核心实现 |
|---|--------|--------|------|---------|
| 1 | FluentDateRangePicker | fluent_date_range_picker.py | 日期范围选择器 | 双日历面板 + 范围高亮 |
| 2 | FluentTimePicker | fluent_time_picker.py | 时间选择器 | 滚轮式时/分/秒选择 |
| 3 | FluentNumericInput | fluent_numeric_input.py | 数字输入框 | 带增减按钮 + 数值滚动动画 |
| 4 | FluentMultiSelect | fluent_multi_select.py | 多选下拉 | 标签模式 + 下拉勾选列表 |
| 5 | FluentTreeSelect | fluent_tree_select.py | 树形选择器 | 下拉树 + 节点展开折叠 |
| 6 | FluentCascader | fluent_cascader.py | 级联选择器 | 多级面板逐级滑入 |
| 7 | FluentTransfer | fluent_transfer.py | 穿梭框 | 左右双列表 + 按钮穿梭 |
| 8 | FluentRangeSlider | fluent_range_slider.py | 范围滑块 | 双滑块 + 选中区域高亮 |

### 二、导航组件 (3个 — 来自原计划)

| # | 组件名 | 文件名 | 描述 | 核心实现 |
|---|--------|--------|------|---------|
| 9 | FluentAnchor | fluent_anchor.py | 锚点导航 | 右侧指示器 + 点击平滑滚动 |
| 10 | FluentBackTop | fluent_back_top.py | 回到顶部 | 滚动显隐 + 点击平滑回顶 |
| 11 | FluentCommandBar | fluent_command_bar.py | 命令栏 | 搜索框 + 操作按钮组 |

### 三、表面组件 (3个 — 来自原计划)

| # | 组件名 | 文件名 | 描述 | 核心实现 |
|---|--------|--------|------|---------|
| 12 | FluentPopover | fluent_popover.py | 气泡弹出框 | 缩放+淡入动画 + 箭头指向 |
| 13 | FluentSplitPanel | fluent_split_panel.py | 分割面板 | 可拖拽分割线 + 比例动画 |
| 14 | FluentTabView | fluent_tab_view.py | 选项卡视图 | 内容区淡入切换 + 指示器滑动 |

### 四、展示组件 (4个 — 来自原计划)

| # | 组件名 | 文件名 | 描述 | 核心实现 |
|---|--------|--------|------|---------|
| 15 | FluentDataTable | fluent_data_table.py | 数据表格 | 排序/选择/行悬停高亮 |
| 16 | FluentImageViewer | fluent_image_viewer.py | 图片查看器 | 缩放/旋转/拖拽查看 |
| 17 | FluentQRCode | fluent_qrcode.py | 二维码展示 | QPainter 绘制二维码矩阵 |
| 18 | FluentCalendarHeatmap | fluent_calendar_heatmap.py | 日历热力图 | 年度日历 + 每日色块 |

### 五、反馈组件 (1个 — 来自原计划)

| # | 组件名 | 文件名 | 描述 | 核心实现 |
|---|--------|--------|------|---------|
| 19 | FluentLoadingScreen | fluent_loading_screen.py | 全屏加载 | 旋转 + 脉冲 + 进度提示 |

### 六、额外图表组件 (8个 — 新增，满足"大量图表"需求)

| # | 组件名 | 文件名 | 描述 | 核心实现 |
|---|--------|--------|------|---------|
| 20 | FluentBubbleChart | fluent_bubble_chart.py | 气泡图 | 三维数据(x,y,size) + 悬停放大 |
| 21 | FluentRoseChart | fluent_rose_chart.py | 玫瑰图/南丁格尔图 | 扇区半径不等 + 旋转展开 |
| 22 | FluentGanttChart | fluent_gantt_chart.py | 甘特图 | 时间轴 + 任务条 + 依赖线 |
| 23 | FluentBulletChart | fluent_bullet_chart.py | 子弹图 | 目标线 + 实际值条 + 范围带 |
| 24 | FluentRadialBarChart | fluent_radial_bar_chart.py | 玉玦图/径向柱状图 | 圆弧条 + 百分比动画 |
| 25 | FluentStackedBarChart | fluent_stacked_bar_chart.py | 堆叠柱状图 | 多系列堆叠 + 悬停tooltip |
| 26 | FluentMixedChart | fluent_mixed_chart.py | 混合图表 | 柱+线叠加 + 双Y轴 |
| 27 | FluentSlopeChart | fluent_slope_chart.py | 斜率图 | 两列对比 + 连线 + 标签 |

### 七、额外专业组件 (4个 — 新增)

| # | 组件名 | 文件名 | 描述 | 核心实现 |
|---|--------|--------|------|---------|
| 28 | FluentAutoComplete | fluent_auto_complete.py | 自动补全输入 | 下拉建议列表 + 模糊匹配 |
| 29 | FluentMentionInput | fluent_mention_input.py | @提及输入 | 弹出用户列表 + 高亮标签 |
| 30 | FluentFlipCard | fluent_flip_card.py | 翻转卡片 | 正反面 + 3D翻转动画 |
| 31 | FluentTour | fluent_tour.py | 新手引导 | 高亮目标区域 + 步骤提示 |

---

## Gallery 页面集成计划

### 需要更新的页面

| 页面文件 | 需新增展示的组件 |
|---------|----------------|
| button_page.py | IconButton, SplitButton, CommandBarButton, DropDownButton, PillButton, FAB (6个) |
| input_page.py | DateRangePicker, TimePicker, NumericInput, MultiSelect, TreeSelect, Cascader, Transfer, RangeSlider, AutoComplete, MentionInput (10个) |
| navigation_page.py | Pagination, Steps, Anchor, BackTop, CommandBar (5个) |
| surface_page.py | Collapse, GroupBox, Popover, SplitPanel, TabView, FlipCard (6个) |
| display_page.py | Descriptions, List, Statistic, Tree, DataTable, ImageViewer, QRCode, CalendarHeatmap (8个) |
| feedback_page.py | Empty, Notification, Popconfirm, Result, Spinner, StateIndicator, Tooltip, LoadingScreen, Tour (9个) |
| chart_page.py | BubbleChart, RoseChart, GanttChart, BulletChart, RadialBarChart, StackedBarChart, MixedChart, SlopeChart (8个) |

---

## 新增 SVG 图标 (约15个)

| 图标名 | 用途 |
|--------|------|
| chevron_up | 向上箭头 |
| file | 文件 |
| indent | 缩进 |
| hash | 井号 |
| git_branch | 分支 |
| percent | 百分比 |
| plus_circle | 加号圆圈 |
| rotate | 旋转 |
| maximize | 最大化 |
| minimize | 最小化 |
| briefcase | 公文包 |
| check_circle | 勾选圆圈 |
| target | 目标 |
| milestone | 里程碑 |
| at_sign | @符号 |

---

## 实施步骤 (6个批次)

### 批次1: 创建8个额外图表组件 + 更新chart_page
1. 创建 `fluent_bubble_chart.py` — 气泡图
2. 创建 `fluent_rose_chart.py` — 玫瑰图
3. 创建 `fluent_gantt_chart.py` — 甘特图
4. 创建 `fluent_bullet_chart.py` — 子弹图
5. 创建 `fluent_radial_bar_chart.py` — 玉玦图
6. 创建 `fluent_stacked_bar_chart.py` — 堆叠柱状图
7. 创建 `fluent_mixed_chart.py` — 混合图表
8. 创建 `fluent_slope_chart.py` — 斜率图
9. 更新 `chart_page.py` — 添加8个新图表展示
10. 更新 `charts/__init__.py`

### 批次2: 创建8个输入组件 + 2个额外输入组件
1. 创建 `fluent_date_range_picker.py`
2. 创建 `fluent_time_picker.py`
3. 创建 `fluent_numeric_input.py`
4. 创建 `fluent_multi_select.py`
5. 创建 `fluent_tree_select.py`
6. 创建 `fluent_cascader.py`
7. 创建 `fluent_transfer.py`
8. 创建 `fluent_range_slider.py`
9. 创建 `fluent_auto_complete.py`
10. 创建 `fluent_mention_input.py`

### 批次3: 创建3个导航 + 3个表面 + 4个额外组件
1. 创建 `fluent_anchor.py`
2. 创建 `fluent_back_top.py`
3. 创建 `fluent_command_bar.py`
4. 创建 `fluent_popover.py`
5. 创建 `fluent_split_panel.py`
6. 创建 `fluent_tab_view.py`
7. 创建 `fluent_flip_card.py`
8. 创建 `fluent_tour.py`
9. 创建 `fluent_loading_screen.py`

### 批次4: 创建4个展示组件
1. 创建 `fluent_data_table.py`
2. 创建 `fluent_image_viewer.py`
3. 创建 `fluent_qrcode.py`
4. 创建 `fluent_calendar_heatmap.py`

### 批次5: 创建15个SVG图标 + 更新所有Gallery页面
1. 创建15个新SVG图标
2. 更新 `button_page.py` — 集成6个新按钮组件
3. 更新 `input_page.py` — 集成10个新输入组件
4. 更新 `navigation_page.py` — 集成5个新导航组件
5. 更新 `surface_page.py` — 集成6个新表面组件
6. 更新 `display_page.py` — 集成8个新展示组件
7. 更新 `feedback_page.py` — 集成9个新反馈组件

### 批次6: 集成测试 + 修复
1. 运行应用验证所有组件
2. 修复主题切换问题
3. 修复动画问题
4. 修复布局问题
5. 确保所有组件在亮/暗模式下正常显示

---

## 技术规范

### 组件开发规范
1. **继承模式**: `class FluentXxx(QWidget, FluentWidgetBase)`
2. **初始化**: 调用 `self._init_fluent_base()`
3. **透明背景**: `self.setAttribute(Qt.WA_TranslucentBackground)`
4. **主题支持**: 实现 `apply_theme()` 方法
5. **自绘组件**: `paintEvent` 开头 `painter.fillRect(self.rect(), Qt.transparent)`
6. **悬停反馈**: 所有可交互组件必须有视觉反馈 (hover_progress 动画)

### 动画规范 (遵循 ui-ux-pro-max)
- **微交互**: 150-300ms, OutCubic
- **进入动画**: 300-500ms, OutBack/OutCubic
- **退出动画**: 200-300ms, InCubic
- **使用 QPropertyAnimation + 自定义 Property**

### 图表规范 (遵循 ui-ux-pro-max Charts & Data)
- **图例**: 始终显示图例，位置靠近图表
- **交互**: 悬停显示数据值 tooltip
- **坐标轴**: 标注单位，可读刻度
- **空数据**: 显示有意义的空状态
- **动画**: 入场动画尊重 reduced-motion
- **颜色**: 使用无障碍配色，不依赖颜色唯一传达信息
- **网格线**: 低对比度 (fg_tertiary)，不与数据竞争

### 图标规范
- SVG 格式, currentColor, 1.5px 描边, 20x20 viewBox
- 一致的描边宽度
- 统一的视觉风格 (线性/outline)

---

## 组件总数统计

| 分类 | 原始 | 已创建新增 | 待创建新增 | 总计 |
|------|------|-----------|-----------|------|
| 图表 | 0 | 12 | 8 | **20** |
| 按钮 | 5 | 6 | 0 | **11** |
| 输入 | 14 | 0 | 10 | **24** |
| 导航 | 6 | 2 | 3 | **11** |
| 表面 | 4 | 2 | 4 | **10** |
| 展示 | 9 | 4 | 4 | **17** |
| 反馈 | 7 | 7 | 2 | **16** |
| **总计** | **45** | **33** | **31** | **109** |

新增组件总数: 33(已创建) + 31(待创建) = **64个新增组件**
其中图表组件: 20个 (满足"大量图表"需求)
