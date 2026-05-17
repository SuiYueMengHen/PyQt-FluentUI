# 导航栏折叠修复 & 图标背景消除 & 新增组件 Spec

## Why
侧边导航栏折叠时图标突然向右跳动，且图标/自绘组件存在白色背景，严重影响视觉质量。同时需要增加更多 Fluent 风格组件以完善 Gallery 展示。

## What Changes
- 修复导航栏折叠动画：图标在宽度变化过程中应始终居中，无跳动
- 消除所有图标和自绘组件的白色/不透明背景，确保透明
- 新增 Fluent 风格组件：FluentTextArea、FluentDatePicker、FluentTimePicker、FluentRating、FluentColorPicker、FluentMenuBar、FluentToast、FluentDrawer、FluentSkeleton、FluentCalendar
- 新增 Gallery 展示页面以展示新组件
- 在 Hero 页面添加 algorithmic-art 风格的装饰性动画背景

## Impact
- Affected code: `fluent_navigation.py`, `icon_provider.py`, `fluent_widget.py`, `fluent_checkbox.py`, `fluent_switch.py`, `fluent_avatar.py`, `fluent_slider.py`, `fluent_radio_button.py`, 所有自绘组件
- Affected pages: `hero_page.py`, 新增展示页面

## ADDED Requirements

### Requirement: 导航栏折叠动画修复
导航栏折叠时 SHALL 实现平滑宽度过渡动画，图标 SHALL 在动画过程中始终水平居中于导航项区域，无突然位移。

#### Scenario: 折叠导航栏
- **WHEN** 用户点击折叠按钮
- **THEN** 导航栏宽度从 240px 平滑过渡到 60px（300ms OutCubic）
- **AND** 图标在整个动画过程中保持水平居中
- **AND** 文字标签在动画开始时立即隐藏
- **AND** 无图标跳动或位移

#### Scenario: 展开导航栏
- **WHEN** 用户再次点击折叠按钮
- **THEN** 导航栏宽度从 60px 平滑过渡到 240px
- **AND** 文字标签在动画接近完成时淡入显示
- **AND** 图标位置从居中平滑过渡到左对齐

### Requirement: 图标和组件透明背景
所有 SVG 图标和自绘组件 SHALL 具有完全透明的背景，不得出现白色或不透明背景色块。

#### Scenario: 图标显示
- **WHEN** 任何组件显示 SVG 图标
- **THEN** 图标背景 SHALL 完全透明
- **AND** 仅图标笔画/填充可见

#### Scenario: 自绘组件显示
- **WHEN** 自绘组件（CheckBox、Switch、RadioButton、Slider、Avatar、ProgressRing）渲染时
- **THEN** 组件自身区域外 SHALL 完全透明
- **AND** 不应有任何不透明背景填充

### Requirement: 新增组件
系统 SHALL 提供以下新增 Fluent 风格组件：

1. **FluentTextArea** — 多行文本输入框，支持自动高度调整
2. **FluentRating** — 星级评分组件，支持半星和只读模式
3. **FluentToast** — 轻量级通知弹出，自动消失
4. **FluentDrawer** — 侧边抽屉面板，从边缘滑入
5. **FluentSkeleton** — 骨架屏占位组件，脉冲动画
6. **FluentCalendar** — 日历选择组件
7. **FluentColorPicker** — 颜色选择器
8. **FluentMenuBar** — 顶部菜单栏

### Requirement: Hero 页面装饰动画
Hero 页面 SHALL 包含基于 algorithmic-art 风格的装饰性动画背景，使用 QPainter 绘制流动粒子或几何图案。

#### Scenario: Hero 页面加载
- **WHEN** 用户导航到 Hero 页面
- **THEN** 页面背景 SHALL 显示流动的几何装饰动画
- **AND** 动画 SHALL 使用主题色系
- **AND** 动画 SHALL 不影响页面交互性能

## MODIFIED Requirements

### Requirement: NavItem 布局
NavItem 的布局 SHALL 使用居中对齐策略：展开时图标左对齐+文字，折叠时图标水平居中。折叠/展开切换 SHALL 通过修改 layout alignment 而非增删 spacer 实现，避免布局跳变。

### Requirement: icon_provider 缓存策略
icon_provider 的缓存 SHALL 在主题切换时自动清除，确保图标颜色随主题更新。缓存 key SHALL 包含颜色值以确保不同颜色的同一图标被正确缓存。
