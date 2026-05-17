# 头像居中修复 & 用户设置界面完善 & 实用组件扩展 Spec

## Why
FluentUserProfile 折叠状态下头像仍未在侧边栏中正确居中（QHBoxLayout 的 alignment 对 fixedSize 子控件居中效果不佳）；用户信息覆盖界面功能过于简陋，缺少可交互的设置项；需要更多实用组件丰富 Gallery 展示。

## What Changes
- 重写 FluentUserProfile 折叠模式布局逻辑，使用 paintEvent 绘制头像确保绝对居中
- 完善 FluentUserInfoOverlay，添加可交互设置项（通知开关、音量滑块、语言选择等）
- 新增 FluentSettingRow 通用设置行组件（图标+标签+控件）
- 在 Gallery 中添加设置页面展示新组件

## Impact
- Affected code: `fluent_user_profile.py`, `fluent_user_info_overlay.py`, 新增 `fluent_setting_row.py`
- Affected pages: 新增 settings_page 或在 subscription_page 同级添加

## ADDED Requirements

### Requirement: FluentUserProfile 头像绝对居中
FluentUserProfile 在折叠状态下，头像 SHALL 通过 paintEvent 直接绘制在组件中心，不依赖 QHBoxLayout 的 alignment。

#### Scenario: 折叠状态头像居中
- **WHEN** 侧边栏折叠，FluentUserProfile 宽度为 60px
- **THEN** 头像 SHALL 绘制在 (30, 32) 中心点，即组件水平中心+垂直中心
- **AND** 头像直径 32px
- **AND** 不使用 QLabel + QPixmap 方式，改用 paintEvent 中 QPainter 直接绘制圆形裁剪头像

#### Scenario: 展开状态
- **WHEN** 侧边栏展开
- **THEN** 使用 QLabel 方式显示头像（40px），左侧对齐+文字右侧排列
- **AND** 布局与当前一致

### Requirement: FluentSettingRow 通用设置行组件
系统 SHALL 提供 FluentSettingRow 组件，用于在设置界面中展示单行设置项。

#### Scenario: 开关类型设置行
- **WHEN** 创建 FluentSettingRow(icon="notifications", label="通知", control="switch")
- **THEN** 显示通知图标 + "通知"文字 + 右侧 FluentSwitch 开关

#### Scenario: 滑块类型设置行
- **WHEN** 创建 FluentSettingRow(icon="volume", label="音量", control="slider", min=0, max=100)
- **THEN** 显示音量图标 + "音量"文字 + 右侧 FluentSlider 滑块

#### Scenario: 选择类型设置行
- **WHEN** 创建 FluentSettingRow(icon="globe", label="语言", control="combo", options=["中文","English"])
- **THEN** 显示全球图标 + "语言"文字 + 右侧 FluentComboBox 下拉框

### Requirement: 完善用户信息覆盖界面
FluentUserInfoOverlay SHALL 包含可交互的设置项区域，使用 FluentSettingRow 组件构建。

#### Scenario: 覆盖界面内容
- **WHEN** 用户点击侧边栏用户资料
- **THEN** 覆盖界面 SHALL 显示：头像+用户名+角色+邮箱+分隔线+设置行列表
- **AND** 设置行包含：通知开关、音量滑块、语言选择、深色模式开关
- **AND** 底部有退出登录按钮

#### Scenario: 设置项交互
- **WHEN** 用户切换"深色模式"开关
- **THEN** SHALL 触发主题切换

### Requirement: Gallery 设置页面
Gallery SHALL 包含设置页面，展示 FluentSettingRow 等实用组件。

#### Scenario: 导航到设置页面
- **WHEN** 用户点击侧边栏"设置"导航项
- **THEN** 显示设置页面，包含多组设置行（通知、外观、语言、音量等）

## MODIFIED Requirements

### Requirement: FluentUserProfile 布局
FluentUserProfile 折叠时 SHALL 隐藏所有子控件（QLabel），在 paintEvent 中直接绘制圆形头像和背景。展开时使用 QHBoxLayout 正常布局。
