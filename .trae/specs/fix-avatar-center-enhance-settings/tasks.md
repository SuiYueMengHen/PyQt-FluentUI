# Tasks

- [x] Task 1: 重写 FluentUserProfile 折叠模式 — 使用 paintEvent 绘制头像确保绝对居中
  - [x] 1.1: 修改 `fluent_user_profile.py`，折叠时隐藏所有子控件（_avatar_label, _text_container）
  - [x] 1.2: 在 paintEvent 中检测折叠状态，折叠时直接用 QPainter 绘制圆形裁剪头像在组件中心
  - [x] 1.3: 缓存圆形裁剪后的 QPixmap，避免每次 paintEvent 重新生成
  - [x] 1.4: 验证折叠/展开切换正常，头像在折叠时绝对居中

- [x] Task 2: 创建 FluentSettingRow 通用设置行组件
  - [x] 2.1: 创建 `app/components/inputs/fluent_setting_row.py`
  - [x] 2.2: 支持 switch/slider/combo 三种控件类型
  - [x] 2.3: 每行包含：图标 + 标签文字 + 右侧控件
  - [x] 2.4: 支持白天黑夜模式
  - [x] 2.5: 添加 self_check() 方法

- [x] Task 3: 完善 FluentUserInfoOverlay 设置项
  - [x] 3.1: 替换当前的3个静态按钮为 FluentSettingRow 列表
  - [x] 3.2: 添加设置行：通知开关（switch）、音量滑块（slider）、语言选择（combo）、深色模式开关（switch）
  - [x] 3.3: 连接深色模式开关到 theme_btn_clicked 信号
  - [x] 3.4: 保留退出登录按钮在底部
  - [x] 3.5: 验证覆盖界面交互正常

- [x] Task 4: 创建 Gallery 设置页面
  - [x] 4.1: 创建 `app/pages/settings_page.py`，展示多组 FluentSettingRow
  - [x] 4.2: 在 main.py 中添加"设置"导航项（settings 图标）
  - [x] 4.3: 验证导航和主题切换正常

# Task Dependencies
- [Task 2] depends on [Task 1]（无实际依赖，可并行）
- [Task 3] depends on [Task 2]（需要 FluentSettingRow 组件）
- [Task 4] depends on [Task 2]（需要 FluentSettingRow 组件）
