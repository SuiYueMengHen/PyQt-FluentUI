# 主题切换修复 & 组件报错修复 & UI 全面增强 Spec

## Why
多个组件在白天黑夜模式切换时存在逻辑冲突；大量组件 paintEvent 中 `fillRect(Qt.transparent)` 导致 QBackingStore::endPaint() 报错；选择控件/数值组件/多选下拉/锚点导航等频繁报错；日历/日期范围/时间选择器存在交互缺陷和视觉问题；侧边栏导航缺少二级导航、折叠动画不流畅；通知组件视觉效果差且缺少停留进度条。

## What Changes
- 修复主题切换逻辑冲突，确保所有组件正确响应主题变化
- 修复所有 paintEvent 中 QPainter 生命周期管理，消除 QBackingStore::endPaint() 报错
- 修复选择控件（ComboBox）、数值组件（SpinBox）报错
- 重做 SpinBox 上下按钮样式，支持主题模式
- 修复下拉框黑边问题
- 修复日历选择器年份月份显示位置（移至顶部）
- 修复日期范围选择器交互错误（点击日期与选中不一致）
- 为时间选择器添加动画效果
- 为侧边栏导航选中状态蓝色条添加动画效果
- 修复侧边栏折叠时图标跳动问题
- 实现侧边栏二级导航（展开/收缩/动效）
- 修复多选下拉报错并完善功能
- 修复锚点导航报错
- 美化所有通知组件并添加停留时间进度条
- 确保按钮文字全部显示

## Impact
- Affected code: `fluent_widget.py`, `theme_manager.py`, `fluent_navigation.py`, `fluent_combo_box.py`, `fluent_spin_box.py`, `fluent_calendar.py`, `fluent_date_range_picker.py`, `fluent_time_picker.py`, `fluent_multi_select.py`, `fluent_anchor.py`, `fluent_notification.py`, `fluent_positional_notification.py`, `fluent_toast.py`, `fluent_button.py`, `fluent_accent_button.py`, `fluent_toggle_button.py`, `fluent_icon_button.py`, `fluent_pill_button.py`, `fluent_dropdown_button.py`, `fluent_split_button.py`, `fluent_fab.py`, `fluent_command_bar_button.py`, `fluent_user_profile.py`, 所有包含 paintEvent 的组件
- **BREAKING**: NavItem 布局结构变更（支持二级导航），FluentMultiSelect 接口变更（完善下拉面板）

## ADDED Requirements

### Requirement: 主题切换逻辑一致性
所有 Fluent 组件 SHALL 在主题切换时正确更新视觉状态，无残留旧主题样式。

#### Scenario: 主题切换
- **WHEN** 用户切换白天/黑夜模式
- **THEN** 所有可见组件 SHALL 立即更新为新主题的配色
- **AND** 无组件残留旧主题颜色
- **AND** 无 QBackingStore 报错

#### Scenario: 主题切换期间动画
- **WHEN** 主题切换时某组件正在播放动画
- **THEN** 动画 SHALL 平滑过渡到新主题配色
- **AND** 不产生视觉闪烁或报错

### Requirement: QPainter 生命周期管理
所有包含 paintEvent 的组件 SHALL 正确管理 QPainter 生命周期，消除 QBackingStore::endPaint() 报错。

#### Scenario: paintEvent 执行
- **WHEN** 任何组件的 paintEvent 被调用
- **THEN** QPainter SHALL 在函数退出前调用 end() 或使用上下文管理器
- **AND** 不使用 `fillRect(self.rect(), Qt.transparent)` 填充透明背景
- **AND** 不在 WA_TranslucentBackground 组件上用透明色填充

### Requirement: 按钮文字完整显示
所有包含文字的按钮 SHALL 确保文字完整显示，不被截断。

#### Scenario: 按钮文字显示
- **WHEN** 按钮包含文字内容
- **THEN** 按钮 SHALL 自动扩展宽度以完整显示文字
- **AND** 最小宽度 SHALL 不小于文字宽度 + padding
- **AND** 如果空间不足，文字使用省略号而非直接截断

### Requirement: SpinBox 上下按钮样式重做
FluentSpinBox 的上下按钮 SHALL 使用 Fluent Design 风格，支持白天黑夜模式。

#### Scenario: SpinBox 上下按钮显示
- **WHEN** SpinBox 渲染时
- **THEN** 上下按钮 SHALL 使用主题色系渲染
- **AND** 悬停时按钮背景变为主题浅色
- **AND** 按下时按钮背景变为主题深色
- **AND** 箭头使用 SVG 图标而非 CSS border 三角形
- **AND** 按钮有圆角

#### Scenario: SpinBox 主题切换
- **WHEN** 主题从亮色切换到暗色
- **THEN** 上下按钮颜色 SHALL 立即更新为暗色主题配色

### Requirement: 日历选择器年份月份顶部显示
FluentCalendar 的年份和月份 SHALL 显示在日历顶部，而非绘制在背景中。

#### Scenario: 日历顶部导航
- **WHEN** 日历渲染时
- **THEN** 年份和月份 SHALL 显示在日历最顶部的导航栏中
- **AND** 导航栏包含左箭头、年月文字、右箭头
- **AND** 点击左右箭头可切换月份
- **AND** 年月文字清晰可读，不与日期网格重叠

### Requirement: 日期范围选择器交互修复
FluentDateRangePicker 点击的日期 SHALL 与实际选中的日期一致。

#### Scenario: 点击日期
- **WHEN** 用户点击日历中的某一天
- **THEN** 选中的日期 SHALL 与用户点击的日期完全一致
- **AND** 起始日期和结束日期正确标记

#### Scenario: 日期范围选择
- **WHEN** 用户先点击起始日期再点击结束日期
- **THEN** 两个日期之间的范围 SHALL 正确高亮
- **AND** 起始日期不晚于结束日期

### Requirement: 时间选择器动画效果
FluentTimePicker SHALL 在值改变时显示平滑的滚动动画效果。

#### Scenario: 时间值改变
- **WHEN** 用户通过鼠标拖拽或滚轮改变时间值
- **THEN** 数字 SHALL 平滑滚动到新值
- **AND** 滚动动画使用 OutCubic 缓动
- **AND** 动画时长 200ms

#### Scenario: TimePicker 修复类变量 bug
- **WHEN** 多个 TimePicker 实例同时存在
- **THEN** 每个实例 SHALL 有独立的滚动偏移量
- **AND** 不共享 `_scroll_offset` 类变量

### Requirement: 侧边栏选中状态蓝色条动画
侧边栏导航项选中时，左侧蓝色指示条 SHALL 有平滑的位置过渡动画。

#### Scenario: 切换选中项
- **WHEN** 用户从一个导航项切换到另一个
- **THEN** 蓝色指示条 SHALL 从旧位置平滑滑动到新位置
- **AND** 动画使用 OutCubic 缓动，时长 250ms
- **AND** 指示条高度与导航项高度一致

### Requirement: 侧边栏折叠图标不跳动
侧边栏折叠/展开过程中，图标 SHALL 始终保持在左侧位置，不出现右移再左移的跳动。

#### Scenario: 折叠过程
- **WHEN** 侧边栏从展开状态开始折叠
- **THEN** 图标 SHALL 始终保持在左侧固定位置
- **AND** 文字标签 SHALL 向左渐变消失（透明度渐变）
- **AND** 不出现图标突然右移再左移的现象

#### Scenario: 展开过程
- **WHEN** 侧边栏从折叠状态开始展开
- **THEN** 图标 SHALL 始终保持在左侧固定位置
- **AND** 文字标签 SHALL 在宽度足够时淡入显示

### Requirement: 侧边栏二级导航
侧边栏 SHALL 支持二级导航项，包含展开/收缩动效。

#### Scenario: 二级导航展开
- **WHEN** 用户点击有子项的一级导航项
- **THEN** 子项 SHALL 以向下滑出动画展开
- **AND** 一级项的图标右侧显示展开/收缩箭头
- **AND** 子项缩进显示，有左侧连接线

#### Scenario: 二级导航收缩
- **WHEN** 用户再次点击已展开的一级导航项
- **THEN** 子项 SHALL 以向上滑入动画收缩
- **AND** 箭头旋转为收缩状态

#### Scenario: 侧边栏折叠时二级导航
- **WHEN** 侧边栏处于折叠状态
- **THEN** 二级导航 SHALL 以悬浮弹出菜单方式显示
- **AND** 弹出菜单有阴影和圆角

### Requirement: 多选下拉修复与完善
FluentMultiSelect SHALL 正常工作，不报错，提供完整的下拉选择面板。

#### Scenario: 多选下拉交互
- **WHEN** 用户点击多选下拉框
- **THEN** SHALL 弹出选择面板，显示所有可选项
- **AND** 每个选项前有复选框
- **AND** 已选项显示勾选状态
- **AND** 点击选项可切换选中/取消

#### Scenario: 已选项显示
- **WHEN** 用户选中多个选项
- **THEN** 已选项 SHALL 以标签形式显示在输入框中
- **AND** 标签有关闭按钮可单独移除
- **AND** 标签溢出时显示 "+N" 计数

### Requirement: 锚点导航修复
FluentAnchor SHALL 不报错，正确显示和交互。

#### Scenario: 锚点导航渲染
- **WHEN** 锚点导航组件渲染时
- **THEN** SHALL 正确绘制所有锚点项和指示条
- **AND** 不产生 QBackingStore 报错
- **AND** 点击锚点项正确切换选中状态

### Requirement: 通知组件美化与进度条
所有通知组件（FluentNotification、FluentPositionalNotification、FluentToast）SHALL 有更好的视觉效果和停留时间进度条。

#### Scenario: 通知视觉美化
- **WHEN** 通知弹出时
- **THEN** 通知卡片 SHALL 有圆角、阴影、主题色左边框
- **AND** 图标和文字对齐美观
- **AND** 有滑入/滑出动画

#### Scenario: 通知进度条
- **WHEN** 通知显示时
- **THEN** 通知底部 SHALL 显示进度条
- **AND** 进度条从满宽度逐渐缩短到 0
- **AND** 进度条颜色与通知类型匹配（信息蓝、成功绿、警告橙、错误红）
- **AND** 进度条动画时长与通知停留时长一致

#### Scenario: 通知悬停暂停
- **WHEN** 用户鼠标悬停在通知上
- **THEN** 进度条 SHALL 暂停
- **AND** 通知不自动消失
- **WHEN** 鼠标移出
- **THEN** 进度条继续，通知继续倒计时

#### Scenario: 通知关闭按钮
- **WHEN** 通知显示时
- **THEN** 右上角 SHALL 有关闭按钮
- **AND** 点击关闭按钮立即关闭通知

### Requirement: 下拉框黑边修复
所有下拉框（ComboBox、MultiSelect）的下拉弹出列表 SHALL 无黑边。

#### Scenario: 下拉弹出列表显示
- **WHEN** 用户打开下拉框
- **THEN** 弹出列表 SHALL 无黑色边框
- **AND** 边框颜色使用主题 stroke 色
- **AND** outline 设置为 none

## MODIFIED Requirements

### Requirement: FluentWidgetBase 主题切换
FluentWidgetBase._on_theme_changed SHALL 确保在 apply_theme 前清除组件样式缓存，避免新旧主题样式冲突。apply_theme 完成后 SHALL 调用 update() 强制重绘。

### Requirement: NavItem 布局
NavItem 布局 SHALL 使用固定左侧图标容器 + 弹性文字区域结构。图标容器宽度固定 40px，始终左对齐。折叠时文字区域宽度渐变为 0，文字透明度渐变消失。不修改图标容器的对齐方式。

### Requirement: FluentCalendar 绘制
FluentCalendar SHALL 移除 WA_TranslucentBackground 属性和 fillRect(transparent) 调用，改用主题背景色填充。年份月份从 paintEvent 背景绘制改为独立的顶部导航 QWidget。

### Requirement: FluentTimePicker 滚动
FluentTimePicker._scroll_offset SHALL 从类变量改为实例变量。滚动动画 SHALL 使用 QPropertyAnimation 实现平滑过渡。

### Requirement: FluentMultiSelect 下拉面板
FluentMultiSelect SHALL 实现完整的 QFrame 弹出面板，包含 QScrollArea + 复选框列表。弹出面板位置在触发器下方对齐。

### Requirement: FluentNotification 生命周期
FluentNotification dismiss 后 SHALL 调用 deleteLater() 释放内存。slide_x setter SHALL 安全处理 parent() 为 None 的情况。

### Requirement: FluentToast 信号管理
FluentToast._dismiss SHALL 在连接 finished 信号前先断开旧连接，避免重复触发。

## REMOVED Requirements

### Requirement: fillRect(Qt.transparent) 背景清除模式
**Reason**: 此模式在 Windows + OpenGL 环境下导致 QBackingStore::endPaint() 报错
**Migration**: 移除所有 paintEvent 中的 `fillRect(self.rect(), Qt.transparent)` 调用，改用 `setAttribute(Qt.WA_OpaquePaintEvent, True)` + 主题背景色填充，或直接使用 `setAutoFillBackground(True)` 配合主题背景
