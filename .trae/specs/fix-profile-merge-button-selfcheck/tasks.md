# Tasks

- [ ] Task 1: 修复 FluentUserProfile 头像折叠居中问题
  - [ ] 1.1: 修改 `fluent_user_profile.py` 的 `set_collapsed()` 方法，折叠时确保 `_avatar_label` 在整个组件区域内居中（当前 `_layout.setAlignment` 设置了 HCenter 但 avatar_label 自身有 fixedSize 导致可能未居中）
  - [ ] 1.2: 验证折叠状态下头像在侧边栏中水平和垂直居中

- [ ] Task 2: 创建用户信息覆盖界面 FluentUserInfoOverlay
  - [ ] 2.1: 创建 `app/components/overlay/fluent_user_info_overlay.py`，包含头像（大尺寸）、用户名、角色、邮箱、设置按钮等
  - [ ] 2.2: 实现半透明遮罩 + 滑入动画（从左侧滑入，300ms OutCubic）
  - [ ] 2.3: 在 FluentNavigation 中连接 FluentUserProfile.clicked 信号，触发显示覆盖界面
  - [ ] 2.4: 实现关闭按钮和遮罩点击关闭

- [ ] Task 3: 合并标题栏按钮（移除独立最小化按钮）
  - [ ] 3.1: 修改 `main_window.py` TitleBar，移除 `_min_btn`，仅保留 `_max_btn`（最大化/还原切换）和 `_close_btn`
  - [ ] 3.2: 更新 `apply_theme()` 移除 `_min_btn` 相关样式代码
  - [ ] 3.3: 验证最大化/还原图标切换正常工作

- [ ] Task 4: 为核心组件添加 self_check() 方法
  - [ ] 4.1: 为 FluentNotification 添加 self_check() — 检查主题颜色获取、painter 渲染
  - [ ] 4.2: 为 FluentToast 添加 self_check() — 检查图标加载、主题颜色
  - [ ] 4.3: 为 FluentPositionalNotification 添加 self_check() — 检查图标加载、位置计算
  - [ ] 4.4: 为 FluentUserProfile 添加 self_check() — 检查头像 pixmap 生成、主题颜色
  - [ ] 4.5: 为 FluentSubscriptionCard 添加 self_check() — 检查图标加载、主题颜色
  - [ ] 4.6: 为 FluentInfoBar 添加 self_check() — 检查图标加载
  - [ ] 4.7: 为 FluentProgressBar/FluentProgressRing 添加 self_check() — 检查值范围、主题颜色

- [ ] Task 5: 修复 Gallery 通知组件触发问题
  - [ ] 5.1: 调试 FluentNotification.show_notification() 静态方法 — 确认 parent 传递正确、位置计算正确
  - [ ] 5.2: 调试 FluentToast.show_toast_message() — 确认窗口坐标计算正确
  - [ ] 5.3: 调试 FluentPositionalNotification — 确认 FluentNotificationManager 单例工作正常、位置计算正确
  - [ ] 5.4: 在 feedback_page.py 中添加 Toast 触发按钮行（当前缺少独立的 Toast 触发按钮）
  - [ ] 5.5: 验证所有通知组件在 Gallery 中可正常触发和展示

- [ ] Task 6: 集成自检到 Gallery 展示
  - [ ] 6.1: 在 feedback_page.py 底部添加"组件自检"区域，包含一个"运行自检"按钮
  - [ ] 6.2: 点击按钮后调用所有组件的 self_check()，将结果显示在页面上

# Task Dependencies
- [Task 2] depends on [Task 1]（用户信息覆盖界面依赖头像居中修复）
- [Task 5] 独立，可与 Task 1-3 并行
- [Task 6] depends on [Task 4]（自检展示依赖 self_check 方法实现）
- [Task 3] 独立
