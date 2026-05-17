# Tasks

- [x] Task 1: 修复导航栏折叠动画 — 图标跳动问题
  - [x] 1.1: 重写 NavItem 布局策略：使用固定宽度容器包裹图标，折叠时仅修改 alignment 为 AlignCenter，展开时恢复 AlignLeft
  - [x] 1.2: 移除 QSpacerItem 的增删逻辑，改用 layout alignment 切换
  - [x] 1.3: 折叠时文字标签立即隐藏（setVisible(False)），不等待动画完成
  - [x] 1.4: 验证折叠/展开动画流畅无跳动

- [x] Task 2: 消除图标和组件白色背景
  - [x] 2.1: 修复 icon_provider.py — 确保 QPixmap 使用 Qt.transparent 填充，QPainter 开始前设置背景模式
  - [x] 2.2: 修复所有自绘组件（CheckBox、RadioButton、Switch、Slider、Avatar、ProgressRing、ProgressBar）的 paintEvent — 在绘制前先填充透明背景
  - [x] 2.3: 修复 NavItem 中 _icon_label 的背景 — 设置 `background: transparent;` 样式
  - [x] 2.4: 修复 icon_provider 缓存 — 主题切换时调用 clear_cache()
  - [x] 2.5: 验证所有组件在亮色/暗色模式下无白色背景

- [x] Task 3: 新增 FluentTextArea 组件
  - [x] 3.1: 创建 fluent_text_area.py — 多行文本输入，支持 placeholder、自动高度
  - [x] 3.2: 实现 apply_theme 主题适配

- [x] Task 4: 新增 FluentRating 组件
  - [x] 4.1: 创建 fluent_rating.py — 星级评分，QPainter 自绘星星，支持半星
  - [x] 4.2: 实现悬停预览和点击选择动画

- [x] Task 5: 新增 FluentToast 组件
  - [x] 5.1: 创建 fluent_toast.py — 轻量通知弹出，自动消失（3-5s）
  - [x] 5.2: 实现滑入/滑出动画

- [x] Task 6: 新增 FluentDrawer 组件
  - [x] 6.1: 创建 fluent_drawer.py — 侧边抽屉面板，从左/右/上/下边缘滑入
  - [x] 6.2: 实现遮罩层和滑入动画

- [x] Task 7: 新增 FluentSkeleton 组件
  - [x] 7.1: 创建 fluent_skeleton.py — 骨架屏占位，脉冲动画
  - [x] 7.2: 支持矩形、圆形、文本行三种形态

- [x] Task 8: 新增 FluentCalendar 组件
  - [x] 8.1: 创建 fluent_calendar.py — 日历选择，QPainter 自绘
  - [x] 8.2: 实现月份切换和日期选择

- [x] Task 9: 新增 FluentColorPicker 组件
  - [x] 9.1: 创建 fluent_color_picker.py — 颜色选择器，预设色板 + 自定义
  - [x] 9.2: 实现颜色预览和选择反馈

- [x] Task 10: 新增 FluentMenuBar 组件
  - [x] 10.1: 创建 fluent_menu_bar.py — 顶部菜单栏，下拉菜单
  - [x] 10.2: 实现菜单项悬停和点击交互

- [x] Task 11: Hero 页面添加 algorithmic-art 装饰动画
  - [x] 11.1: 创建 AnimatedBackground 组件 — 使用 QPainter 绘制流动粒子/几何图案
  - [x] 11.2: 集成到 Hero 页面作为背景层

- [x] Task 12: 更新 Gallery 展示页面
  - [x] 12.1: 更新 input_page.py — 添加 TextArea、Rating、Calendar、ColorPicker 展示
  - [x] 12.2: 更新 feedback_page.py — 添加 Toast、Skeleton 展示
  - [x] 12.3: 更新 surface_page.py — 添加 Drawer 展示
  - [x] 12.4: 更新 navigation_page.py — 添加 MenuBar 展示
  - [x] 12.5: 确认 main.py 导航项无需修改（新组件已添加到现有页面）

# Task Dependencies
- [Task 3-10] 可并行执行（互相独立的新组件）
- [Task 12] depends on [Task 3-10]（展示页依赖组件完成）
- [Task 11] 独立于其他任务
- [Task 1, 2] 优先级最高，应最先完成
