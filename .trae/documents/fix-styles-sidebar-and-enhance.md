# 修复样式加载、侧边栏动画、组件显示 & 增强交互动画

## 问题分析

### 问题1：初始打开后大量组件样式未加载
**根因分析：**
- `FluentWidgetBase._init_fluent_base()` 使用 `QTimer.singleShot(0, self.apply_theme)` 延迟应用主题，但某些情况下（如懒加载页面首次显示时），该定时器可能在组件尚未完全构建或不可见时触发，导致 `update()` 不生效
- 部分组件（如 `NavItem`）未继承 `FluentWidgetBase`，不参与主题自动更新
- `KanbanCard.sizeHint()` 返回 `super().sizeHint()` 而非自己计算的尺寸，导致布局不正确
- `FluentWordCloud` 在方法内部局部导入 `QFontMetrics`，不规范

**修复方案：**
1. 在 `FluentWidgetBase` 中增加 `showEvent` 兜底机制：如果组件首次显示时主题尚未应用，立即调用 `apply_theme()`
2. 修复 `KanbanCard.sizeHint()` 返回正确计算的尺寸
3. 将 `FluentWordCloud` 的 `QFontMetrics` 导入移至文件顶部
4. 修复 `FluentMindMap` 中 `self.sizePolicy().Expanding` 为 `QSizePolicy.Policy.Expanding`

### 问题2：侧边栏收回时图表向左移动
**根因分析：**
- `FluentNavigation` 使用 `QPropertyAnimation` 动画改变 `setFixedWidth()`，从 240px → 60px
- 侧边栏宽度变化导致 `QStackedWidget` 可用空间增大，触发当前页面的 `resizeEvent`
- 图表组件在 `resizeEvent` 中调用 `_schedule_layout()` → `QTimer.singleShot(0, self._do_layout)` 重新布局
- 由于 `singleShot(0)` 延迟极短，几乎每次宽度变化都会触发重布局，导致图表内容随侧边栏动画持续移动

**修复方案：**
1. 在所有图表/图示组件中实现防抖（debounce）机制：用 `QTimer` 替代 `QTimer.singleShot(0, ...)`，设置 150-200ms 延迟，在动画期间不触发重布局
2. 在 `FluentNavigation.toggle_collapse()` 中，动画开始前发出信号通知页面暂停布局，动画结束后恢复
3. 具体实现：为图表组件添加 `_resize_timer`，在 `resizeEvent` 中重启定时器而非立即布局

### 问题3：部分UI组件显示不完全（如思维导图）
**根因分析：**
- `FluentMindMap` 使用 `self.sizePolicy().Expanding`（语法错误，应为 `QSizePolicy.Policy.Expanding`）
- `FluentOrgChart` 和 `FluentFishbone` 使用 `setMinimumSize(600, 400)` 固定最小尺寸，不够灵活
- `FluentFishbone` 和 `FluentTimelineChart` 缺少 `resizeEvent` 重写，窗口大小变化时不会重新布局
- `FluentRelationGraph` 使用 `setMinimumSize(500, 400)` 且无 `SizePolicy.Expanding`
- 思维导图等组件在初始高度为 0 或很小时，`_do_layout()` 中 `if w < 50 or h < 50: return` 直接跳过布局

**修复方案：**
1. 修复 `FluentMindMap` 的 `setSizePolicy` 调用
2. 为 `FluentFishbone` 和 `FluentTimelineChart` 添加 `resizeEvent` 重写
3. 统一所有图示组件使用 `QSizePolicy.Policy.Expanding` + `setMinimumHeight()` 而非 `setMinimumSize()`
4. 优化 `_do_layout()` 中的尺寸检查逻辑，在尺寸不足时标记布局无效而非直接返回

### 问题4：添加更多组件，优化已有组件交互和动画
**增强方案：**

#### 4.1 提取动画混入类（消除代码重复）
- 9个图示组件都有相同的 `_anim_progress`、`_start_anim()`、`@Property(float)` 代码
- 创建 `DiagramAnimMixin` 或在 `FluentWidgetBase` 中添加动画支持
- 减少约 200 行重复代码

#### 4.2 为所有图示组件添加交互功能
- **Tooltip**：鼠标悬停在节点/元素上时显示详细信息
- **Hover 高亮**：鼠标悬停时高亮当前元素及其关联元素
- **点击事件**：节点/元素可点击，发出信号
- **动画增强**：
  - 思维导图：节点逐个展开的交错动画
  - 流程图：连线流动动画（虚线流动效果）
  - 关系图：节点悬停时放大 + 关联边高亮
  - 桑基图：悬停时高亮整条流向路径
  - 词云：悬停时单词放大 + 颜色加深
  - 时间轴：悬停时事件卡片浮起效果
  - 看板：卡片悬停阴影加深 + 轻微上浮

#### 4.3 新增图示组件
- **FluentGauge**（仪表盘）：展示进度/指标，支持多色弧段
- **FluentChordDiagram**（和弦图）：展示多组数据间的关联关系

---

## 实施步骤

### 阶段一：修复核心问题（问题1-3）

#### 步骤1：修复 FluentWidgetBase 样式加载
**文件：** `app/components/base/fluent_widget.py`
- 移除未使用的 `QObject` 导入
- 添加 `_theme_applied` 标志位
- 在 `_init_fluent_base()` 中保留 `QTimer.singleShot(0, self.apply_theme)`
- 添加 `showEvent` 兜底：如果组件首次显示时主题未应用，立即调用 `apply_theme()`
- 注意：由于 `FluentWidgetBase` 是 mixin，需要通过宿主类的 `showEvent` 实现

#### 步骤2：修复图表组件防抖机制（解决侧边栏动画问题）
**文件：** 所有图示组件（9个）+ 所有图表组件（20个）
- 为每个有 `resizeEvent` 重写的组件添加 `_resize_timer` 成员
- `resizeEvent` 中重启 `_resize_timer`（150ms 延迟），定时器触发时执行布局
- 替换所有 `QTimer.singleShot(0, self._do_layout)` 为防抖定时器

#### 步骤3：修复思维导图及其他组件显示不完全
**文件：** `fluent_mind_map.py`, `fluent_org_chart.py`, `fluent_fishbone.py`, `fluent_relation_graph.py`, `fluent_timeline_chart.py`
- 修复 `FluentMindMap` 的 `setSizePolicy` 调用
- 统一所有组件使用 `QSizePolicy.Policy.Expanding`
- 为 `FluentFishbone` 和 `FluentTimelineChart` 添加 `resizeEvent` + 防抖
- 优化布局计算中的尺寸检查

#### 步骤4：修复 KanbanCard.sizeHint() 和其他小问题
**文件：** `fluent_kanban_board.py`, `fluent_word_cloud.py`
- 修复 `KanbanCard.sizeHint()` 返回 `QSize(self.minimumWidth(), h)`
- 将 `FluentWordCloud` 的 `QFontMetrics` 导入移至文件顶部
- 在 `diagrams/__init__.py` 中导出 `KanbanCard`

### 阶段二：增强交互和动画（问题4）

#### 步骤5：创建动画混入类
**文件：** `app/components/base/diagram_anim_mixin.py`（新建）
- 提取 `_anim_progress`、`anim_progress` Property、`_start_anim()` 为混入类
- 所有图示组件改为继承该混入类

#### 步骤6：为图示组件添加 Tooltip 和 Hover 交互
**文件：** 所有图示组件
- 添加 `_hovered_node` / `_hovered_element` 追踪
- 实现 `mouseMoveEvent` 检测鼠标位置对应的元素
- 实现 `leaveEvent` 清除悬停状态
- 悬停时绘制 tooltip 信息框
- 悬停时高亮当前元素

#### 步骤7：为图示组件添加点击信号
**文件：** 所有图示组件
- 添加 `node_clicked = Signal(str)` / `element_clicked = Signal(str)` 信号
- 实现 `mousePressEvent` 检测点击的元素并发送信号

#### 步骤8：增强动画效果
**文件：** 各图示组件
- 思维导图：节点逐级展开的交错动画（按 depth 延迟）
- 流程图：连线虚线流动效果
- 关系图：节点悬停放大 + 关联边高亮
- 桑基图：悬停高亮整条流向路径
- 词云：悬停单词放大
- 时间轴：悬停事件浮起效果
- 看板：卡片悬停阴影加深

#### 步骤9：新增 FluentGauge 仪表盘组件
**文件：** `app/components/diagrams/fluent_gauge.py`（新建）
- 支持设置值、最大值、标签
- 支持多色弧段（如绿→黄→红）
- 悬停时显示精确数值 tooltip
- 值变化时有平滑动画过渡

#### 步骤10：新增 FluentChordDiagram 和弦图组件
**文件：** `app/components/diagrams/fluent_chord_diagram.py`（新建）
- 支持设置节点和连接矩阵
- 悬停时高亮关联弧段
- 渐变色弧段

#### 步骤11：更新 diagram_page.py 展示页面
**文件：** `app/pages/diagram_page.py`
- 添加 FluentGauge 和 FluentChordDiagram 的展示
- 更新 `apply_theme()` 中的标签变量列表
- 更新描述文字

#### 步骤12：更新 __init__.py 导出
**文件：** `app/components/diagrams/__init__.py`
- 导出 `KanbanCard`、`FluentGauge`、`FluentChordDiagram`

### 阶段三：测试验证

#### 步骤13：运行应用并验证所有修复
- 验证初始打开时所有组件样式正确加载
- 验证侧边栏折叠/展开时图表不移动
- 验证思维导图等组件显示完整
- 验证新增组件和交互功能正常
- 验证主题切换时所有组件正确更新
