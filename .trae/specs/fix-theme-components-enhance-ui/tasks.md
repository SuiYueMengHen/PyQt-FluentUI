# Tasks

- [x] Task 1: 修复 QBackingStore::endPaint() 报错 — 移除所有 paintEvent 中的 fillRect(Qt.transparent)
  - [x] 1.1: 搜索所有包含 `fillRect.*Qt.transparent` 的文件，逐一修复
  - [x] 1.2: 对每个组件：移除 `fillRect(self.rect(), Qt.transparent)` 调用，改用主题背景色填充或 setAutoFillBackground
  - [x] 1.3: 移除不必要的 `setAttribute(Qt.WA_TranslucentBackground)` 设置
  - [x] 1.4: 确保所有 paintEvent 中 QPainter 正确 end()（使用 with 语句或显式调用）
  - [x] 1.5: 验证所有组件无 QBackingStore 报错

- [x] Task 2: 修复主题切换逻辑冲突
  - [x] 2.1: 修改 FluentWidgetBase._on_theme_changed — 在 apply_theme 前调用 ungrab() 和 reset hover/pressed 状态
  - [x] 2.2: 修改 FluentWidgetBase.apply_theme — 完成后调用 update() 强制重绘
  - [x] 2.3: 修复 qss_builder.py L78 font-weight bug（使用了 font_size 值）
  - [x] 2.4: 验证主题切换时所有组件正确更新

- [x] Task 3: 修复按钮文字显示不完整
  - [x] 3.1: 修改 FluentButton — 使用 setMinimumWidth 而非固定宽度，确保文字完整显示
  - [x] 3.2: 修改 FluentAccentButton — 同上
  - [x] 3.3: 修改 FluentToggleButton — 同上
  - [x] 3.4: 修改所有 QWidget 基按钮 — 在 sizeHint 中计算文字宽度
  - [x] 3.5: 验证所有按钮文字完整显示

- [x] Task 4: 修复选择控件和数值组件报错
  - [x] 4.1: 修复 FluentComboBox — focus 状态 border 从 1px 变 2px 导致布局抖动，改为统一 2px + 颜色变化
  - [x] 4.2: 修复 FluentSpinBox — 同上 focus border 问题
  - [x] 4.3: 修复 FluentComboBox — 下拉框黑边，确保 QAbstractItemView 的 margin:0 和 outline:none
  - [x] 4.4: 验证选择控件和数值组件无报错

- [x] Task 5: 重做 SpinBox 上下按钮样式
  - [x] 5.1: 重写 FluentSpinBox.apply_theme — 上下按钮使用主题色系
  - [x] 5.2: 添加悬停/按下状态样式
  - [x] 5.3: 增大箭头三角形尺寸（5px->6px），悬停变主题色
  - [x] 5.4: 添加禁用状态样式
  - [x] 5.5: 验证白天黑夜模式下样式正确

- [x] Task 6: 修复日历选择器年份月份位置
  - [x] 6.1: 重构 FluentCalendar — 将年份月份从 paintEvent 背景绘制改为独立顶部导航 QWidget
  - [x] 6.2: 顶部导航包含：左箭头按钮、年月文字标签、右箭头按钮
  - [x] 6.3: 连接箭头按钮到月份切换逻辑
  - [x] 6.4: 移除 WA_TranslucentBackground 属性，改用主题背景色
  - [x] 6.5: 验证日历显示正确

- [x] Task 7: 修复日期范围选择器交互错误
  - [x] 7.1: 修复 FluentDateRangePicker._day_at 日期计算 bug — 考虑月份第一天是星期几的偏移
  - [x] 7.2: 验证点击日期与选中日期一致
  - [x] 7.3: 验证日期范围选择逻辑正确

- [x] Task 8: 为时间选择器添加动画效果
  - [x] 8.1: 修复 _scroll_offset 类变量 bug — 改为实例变量
  - [x] 8.2: 使用 QPropertyAnimation 实现数字滚动动画
  - [x] 8.3: 添加 OutCubic 缓动，动画时长 200ms
  - [x] 8.4: 修复 paintEvent 中 QBackingStore 问题
  - [x] 8.5: 验证时间选择器动画流畅

- [x] Task 9: 侧边栏选中蓝色条动画
  - [x] 9.1: 在 FluentNavigation 中添加蓝色指示条 QWidget（独立于 NavItem）
  - [x] 9.2: 使用 QPropertyAnimation 实现指示条位置过渡
  - [x] 9.3: 切换选中项时指示条从旧位置滑动到新位置
  - [x] 9.4: 动画 OutCubic 缓动，时长 250ms
  - [x] 9.5: 验证指示条动画效果

- [x] Task 10: 修复侧边栏折叠图标跳动
  - [x] 10.1: 重构 NavItem 布局 — 图标容器固定宽度，始终左对齐
  - [x] 10.2: 折叠时通过调整 margins 视觉居中，不修改对齐方式
  - [x] 10.3: 不修改图标容器的对齐方式
  - [x] 10.4: 验证折叠/展开过程图标不跳动

- [x] Task 11: 实现侧边栏二级导航
  - [x] 11.1: 修改 NavItem 支持子项列表（children 参数）
  - [x] 11.2: 添加展开/收缩箭头图标（chevron_right/chevron_down 切换）
  - [x] 11.3: 子项 NavSubItem 使用缩进布局，6x6 圆点图标
  - [x] 11.4: 子项缩进显示（42px 左边距）
  - [x] 11.5: 折叠状态下二级导航以悬浮弹出菜单显示（QFrame + Qt.Popup）
  - [x] 11.6: 修改 FluentNavigation.add_item 支持 children 参数
  - [x] 11.7: 验证二级导航展开/收缩动效

- [x] Task 12: 修复多选下拉报错并完善功能
  - [x] 12.1: 实现 FluentMultiSelect 弹出选择面板（QFrame + QScrollArea + 复选框列表）
  - [x] 12.2: 修复 paintEvent 中 QBackingStore 报错
  - [x] 12.3: 实现选项勾选/取消交互
  - [x] 12.4: 标签有关闭按钮可单独移除（X 标记绘制 + 点击检测）
  - [x] 12.5: 修复 drop_progress 动画无效问题（边框渐变 + 箭头旋转）
  - [x] 12.6: 验证多选下拉无报错，交互正常

- [x] Task 13: 修复锚点导航报错
  - [x] 13.1: 修复 FluentAnchor paintEvent 中 QBackingStore 报错
  - [x] 13.2: 移除 fillRect(Qt.transparent)，改用主题背景色
  - [x] 13.3: 验证锚点导航无报错

- [x] Task 14: 美化通知组件并添加进度条
  - [x] 14.1: 重做 FluentNotification 视觉 — 圆角、阴影、主题色左边框、关闭按钮
  - [x] 14.2: FluentNotification 添加底部进度条（QPropertyAnimation on progress_width）
  - [x] 14.3: FluentNotification 添加悬停暂停功能（暂停进度条和倒计时）
  - [x] 14.4: FluentNotification dismiss 后调用 deleteLater()
  - [x] 14.5: 修复 slide_x setter 中 parent() 为 None 的崩溃
  - [x] 14.6: 重做 FluentPositionalNotification 视觉 — 同上美化 + 进度条
  - [x] 14.7: 修复 PositionalNotification enterEvent 暂停逻辑（用 stop+start 替代 setInterval）
  - [x] 14.8: 重做 FluentToast 视觉 — 同上美化 + 进度条
  - [x] 14.9: 修复 FluentToast._dismiss 信号重复连接问题
  - [x] 14.10: 验证所有通知组件视觉效果和进度条功能

# Task Dependencies
- [Task 1] 优先级最高，应最先完成（QBackingStore 报错影响所有组件）
- [Task 2] 优先级高，与 Task 1 可并行
- [Task 6, 7, 8] 可并行（日历/日期范围/时间选择器互相独立）
- [Task 9, 10, 11] 有依赖关系：Task 10 先修复图标跳动，Task 9 添加蓝色条动画，Task 11 添加二级导航
- [Task 12, 13] 可并行（多选下拉和锚点导航独立）
- [Task 14] 独立于其他任务
- [Task 3, 4, 5] 可并行（按钮/选择控件/SpinBox 独立）
