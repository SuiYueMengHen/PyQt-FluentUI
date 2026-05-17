# 用户资料居中修复 & 用户信息界面 & 按钮合并 & 组件自检 & 通知触发修复 Spec

## Why
FluentUserProfile 头像在折叠状态下未居中；点击用户资料无导航响应；最大化/还原按钮应合并为一个；部分组件使用时存在报错且无自检机制；Gallery 中通知类组件无法正常触发展示。

## What Changes
- 修复 FluentUserProfile 折叠时头像未在组件中居中的问题
- 点击用户资料组件 SHALL 导航到用户信息覆盖界面（附在原界面上方）
- 合并最大化/还原为一个按钮（当前已实现图标切换，但需移除独立的最小化按钮，将最小化功能合并到最大化按钮的右键菜单或长按行为中）
- 为每个组件添加 `self_check()` 静态方法，返回 (bool, str) 元组表示自检结果
- 修复 Gallery 中通知类组件（FluentNotification、FluentToast、FluentPositionalNotification）无法触发的问题
- 在 Gallery 中添加可交互的触发按钮使所有通知组件可展示

## Impact
- Affected code: `fluent_user_profile.py`, `fluent_navigation.py`, `main_window.py`, `fluent_notification.py`, `fluent_toast.py`, `fluent_positional_notification.py`, `feedback_page.py`, 所有 Fluent 组件
- Affected pages: `feedback_page.py`, 新增 `user_info_overlay.py`

## ADDED Requirements

### Requirement: FluentUserProfile 头像居中
FluentUserProfile 在折叠状态下，头像 SHALL 在组件区域内水平和垂直居中显示。

#### Scenario: 折叠状态头像居中
- **WHEN** 侧边栏折叠，FluentUserProfile 进入折叠状态
- **THEN** 头像 SHALL 在组件的整个区域内水平+垂直居中
- **AND** 头像尺寸为 32×32px

#### Scenario: 展开状态头像对齐
- **WHEN** 侧边栏展开
- **THEN** 头像 SHALL 左对齐，尺寸 40×40px
- **AND** 用户名和角色标签在头像右侧垂直排列

### Requirement: 用户信息覆盖界面
点击 FluentUserProfile SHALL 在当前页面内容区域上方显示用户信息覆盖界面，包含头像、用户名、角色、设置入口等。

#### Scenario: 点击用户资料
- **WHEN** 用户点击 FluentUserProfile 组件
- **THEN** 在主内容区域上方显示用户信息覆盖界面
- **AND** 覆盖界面 SHALL 有半透明背景遮罩
- **AND** 覆盖界面 SHALL 有关闭按钮

#### Scenario: 关闭用户信息
- **WHEN** 用户点击关闭按钮或遮罩区域
- **THEN** 用户信息覆盖界面 SHALL 滑出消失
- **AND** 底层页面内容恢复可见

### Requirement: 最大化/还原按钮合并
标题栏 SHALL 只保留一个窗口控制按钮用于最大化/还原切换，移除独立的最小化按钮。最小化功能通过该按钮在窗口已最大化时点击实现（showNormal 即还原），窗口正常状态点击则最大化。

#### Scenario: 窗口正常状态点击
- **WHEN** 窗口处于正常状态，用户点击最大化按钮
- **THEN** 窗口 SHALL 最大化，按钮图标切换为还原图标

#### Scenario: 窗口最大化状态点击
- **WHEN** 窗口已最大化，用户点击还原按钮
- **THEN** 窗口 SHALL 还原为正常大小，按钮图标切换为最大化图标

### Requirement: 组件自检程序
每个 Fluent 组件 SHALL 提供 `self_check()` 静态/类方法，返回 `(bool, str)` 元组，bool 表示自检是否通过，str 为详细信息。自检内容包含：关键属性初始化、主题颜色获取、图标加载、尺寸合理性。

#### Scenario: 组件自检通过
- **WHEN** 调用某组件的 `self_check()` 方法
- **THEN** 返回 `(True, "组件名: 所有检查项通过")`

#### Scenario: 组件自检失败
- **WHEN** 某组件的关键依赖缺失（如图标找不到）
- **THEN** 返回 `(False, "组件名: 图标 xxx 加载失败")`

### Requirement: Gallery 通知组件可触发
Gallery 的反馈页面中，所有通知类组件（FluentNotification、FluentToast、FluentPositionalNotification）SHALL 可通过按钮点击正常触发并展示。

#### Scenario: 触发 FluentNotification
- **WHEN** 用户在反馈页面点击"信息通知"/"成功通知"等按钮
- **THEN** SHALL 在窗口右上角弹出对应类型的通知卡片
- **AND** 通知 SHALL 有滑入动画
- **AND** 5秒后自动消失

#### Scenario: 触发 FluentToast
- **WHEN** 用户在反馈页面点击 Toast 触发按钮
- **THEN** SHALL 在窗口顶部弹出 Toast 通知
- **AND** 3秒后自动消失

#### Scenario: 触发 FluentPositionalNotification
- **WHEN** 用户在反馈页面点击"右上角"/"右下角"等位置按钮
- **THEN** SHALL 在对应位置弹出通知
- **AND** 通知 SHALL 有方向性滑入动画

## MODIFIED Requirements

### Requirement: FluentUserProfile 布局
FluentUserProfile 的布局 SHALL 使用居中对齐策略：折叠时整个内容（仅头像）在组件区域内居中，展开时头像左对齐+文字右侧排列。折叠/展开切换 SHALL 通过修改 layout alignment 实现。

### Requirement: 标题栏按钮布局
标题栏 SHALL 包含：主题切换按钮、最大化/还原按钮（合并功能）、关闭按钮。移除独立的最小化按钮。
