# FluentUI 风格 PySide6 组件库 Gallery — 实施计划

## 项目概述

使用 PySide6 从零构建一个 FluentUI 风格的现代化桌面组件库 Gallery 应用。所有组件均为自制，不依赖 QtFluentUI 等第三方组件库。支持白天/黑夜模式切换、启动加载界面、Hero 展示页、简约 SVG 图标系统。

---

## 技术栈

| 项目 | 选择 | 说明 |
|------|------|------|
| 语言 | Python 3.10+ | 兼容性好 |
| UI 框架 | PySide6 | Qt for Python 官方绑定 |
| 包管理 | pip + venv | 使用清华镜像源 |
| 图标 | 自绘 SVG | 简约线性风格，参考 Fluent UI Icons |
| 动画 | QPropertyAnimation / QVariantAnimation | Qt 原生动画框架 |
| 样式 | QSS (Qt StyleSheet) | 类 CSS 样式系统 |

---

## 设计系统 (基于 ui-ux-pro-max 规范)

### 配色方案

**亮色模式 (Light)**
| Token | 色值 | 用途 |
|-------|------|------|
| `--primary` | `#0078D4` | 主色调 (Fluent Blue) |
| `--primary-hover` | `#106EBE` | 主色悬停 |
| `--primary-pressed` | `#005A9E` | 主色按下 |
| `--bg-solid-base` | `#F5F5F5` | 页面背景 |
| `--bg-solid-card` | `#FFFFFF` | 卡片/面板背景 |
| `--bg-solid-secondary` | `#FAFAFA` | 次级背景 |
| `--fg-primary` | `#1A1A1A` | 主文字 |
| `--fg-secondary` | `#616161` | 次级文字 |
| `--fg-disabled` | `#A0A0A0` | 禁用文字 |
| `--stroke-card` | `#E5E5E5` | 卡片边框 |
| `--stroke-divider` | `#F0F0F0` | 分割线 |
| `--accent-success` | `#107C10` | 成功 |
| `--accent-warning` | `#FF8C00` | 警告 |
| `--accent-error` | `#D13438` | 错误 |

**暗色模式 (Dark)**
| Token | 色值 | 用途 |
|-------|------|------|
| `--primary` | `#60CDFF` | 主色调 (亮蓝) |
| `--primary-hover` | `#4DB8E8` | 主色悬停 |
| `--primary-pressed` | `#3AA5D4` | 主色按下 |
| `--bg-solid-base` | `#1F1F1F` | 页面背景 |
| `--bg-solid-card` | `#2D2D2D` | 卡片/面板背景 |
| `--bg-solid-secondary` | `#252525` | 次级背景 |
| `--fg-primary` | `#F5F5F5` | 主文字 |
| `--fg-secondary` | `#AAAAAA` | 次级文字 |
| `--fg-disabled` | `#5C5C5C` | 禁用文字 |
| `--stroke-card` | `#3D3D3D` | 卡片边框 |
| `--stroke-divider` | `#333333` | 分割线 |
| `--accent-success` | `#6CCB5F` | 成功 |
| `--accent-warning` | `#FFB900` | 警告 |
| `--accent-error` | `#FF6B6B` | 错误 |

### 字体系统

| 级别 | 字号 | 字重 | 行高 |
|------|------|------|------|
| Display | 28px | Bold (700) | 1.3 |
| Title Large | 20px | Semibold (600) | 1.4 |
| Title Medium | 16px | Semibold (600) | 1.4 |
| Body | 14px | Regular (400) | 1.5 |
| Caption | 12px | Regular (400) | 1.5 |

### 间距系统 (8px 网格)

| Token | 值 |
|-------|-----|
| `--spacing-xxs` | 4px |
| `--spacing-xs` | 8px |
| `--spacing-sm` | 12px |
| `--spacing-md` | 16px |
| `--spacing-lg` | 24px |
| `--spacing-xl` | 32px |
| `--spacing-xxl` | 48px |

### 圆角系统

| Token | 值 |
|-------|-----|
| `--radius-sm` | 4px |
| `--radius-md` | 8px |
| `--radius-lg` | 12px |
| `--radius-xl` | 16px |

### 动画规范

| 类型 | 时长 | 缓动函数 |
|------|------|----------|
| 微交互 (hover/press) | 150ms | ease-out |
| 状态切换 (展开/折叠) | 250ms | ease-in-out |
| 页面过渡 | 300ms | ease-in-out |
| 启动动画 | 800-1500ms | ease-out |

---

## 项目结构

```
e:\FluentUI\
├── .venv\                          # 虚拟环境
├── app\
│   ├── __init__.py
│   ├── main.py                     # 入口文件 (splash + app 启动)
│   ├── theme\
│   │   ├── __init__.py
│   │   ├── theme_manager.py        # 主题管理器 (亮/暗切换)
│   │   ├── colors.py               # 颜色 Token 定义
│   │   ├── typography.py           # 字体 Token 定义
│   │   └── qss_builder.py          # QSS 动态构建器
│   ├── icons\
│   │   ├── __init__.py
│   │   ├── icon_provider.py        # SVG 图标加载/着色引擎
│   │   └── svg\                    # SVG 图标文件
│   │       ├── home.svg
│   │       ├── palette.svg
│   │       ├── sun.svg
│   │       ├── moon.svg
│   │       ├── chevron_right.svg
│   │       ├── search.svg
│   │       └── ... (约 30 个图标)
│   ├── components\
│   │   ├── __init__.py
│   │   ├── base\
│   │   │   ├── __init__.py
│   │   │   ├── fluent_widget.py    # 组件基类 (主题感知)
│   │   │   └── hover_mixin.py      # 悬停动画混入
│   │   ├── buttons\
│   │   │   ├── __init__.py
│   │   │   ├── fluent_button.py        # 基础按钮
│   │   │   ├── fluent_accent_button.py # 强调按钮
│   │   │   ├── fluent_hyperlink.py     # 超链接按钮
│   │   │   └── fluent_toggle_button.py # 切换按钮
│   │   ├── inputs\
│   │   │   ├── __init__.py
│   │   │   ├── fluent_line_edit.py     # 输入框
│   │   │   ├── fluent_password_edit.py # 密码框
│   │   │   ├── fluent_search_edit.py   # 搜索框
│   │   │   ├── fluent_checkbox.py      # 复选框
│   │   │   ├── fluent_radio_button.py  # 单选按钮
│   │   │   ├── fluent_switch.py        # 开关
│   │   │   ├── fluent_slider.py        # 滑块
│   │   │   ├── fluent_spin_box.py      # 数值框
│   │   │   └── fluent_combo_box.py     # 下拉框
│   │   ├── navigation\
│   │   │   ├── __init__.py
│   │   │   ├── fluent_navigation.py    # 侧边导航栏
│   │   │   ├── fluent_breadcrumb.py    # 面包屑
│   │   │   ├── fluent_tab_bar.py       # 标签栏
│   │   │   └── fluent_pivot.py         # 枢轴切换
│   │   ├── surfaces\
│   │   │   ├── __init__.py
│   │   │   ├── fluent_card.py          # 卡片
│   │   │   ├── fluent_expander.py      # 展开面板
│   │   │   └── fluent_dialog.py        # 对话框
│   │   ├── feedback\
│   │   │   ├── __init__.py
│   │   │   ├── fluent_progress_bar.py  # 进度条
│   │   │   ├── fluent_progress_ring.py # 环形进度
│   │   │   ├── fluent_badge.py         # 徽章
│   │   │   ├── fluent_tooltip.py       # 工具提示
│   │   │   └── fluent_info_bar.py      # 信息条
│   │   └── display\
│   │       ├── __init__.py
│   │       ├── fluent_avatar.py        # 头像
│   │       ├── fluent_tag.py           # 标签
│   │       └── fluent_separator.py     # 分割线
│   ├── pages\
│   │   ├── __init__.py
│   │   ├── hero_page.py            # Hero 展示页
│   │   ├── button_page.py          # 按钮展示页
│   │   ├── input_page.py           # 输入组件展示页
│   │   ├── navigation_page.py      # 导航组件展示页
│   │   ├── surface_page.py         # 表面组件展示页
│   │   ├── feedback_page.py        # 反馈组件展示页
│   │   └── display_page.py         # 展示组件展示页
│   ├── splash\
│   │   ├── __init__.py
│   │   └── splash_screen.py        # 启动加载界面
│   └── layout\
│       ├── __init__.py
│       └── main_window.py          # 主窗口布局
├── requirements.txt
└── start.bat                      # Windows 启动脚本
```

---

## 实施步骤

### 阶段一：环境搭建 (Step 1)

1. **创建 Python 虚拟环境**
   ```powershell
   cd e:\FluentUI
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **配置 pip 镜像源并安装 PySide6**
   ```powershell
   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   pip install PySide6
   ```

3. **创建项目目录结构** — 按上述结构创建所有 `__init__.py` 和模块文件

4. **创建 `requirements.txt`**
   ```
   PySide6>=6.6.0
   ```

### 阶段二：主题系统 (Step 2)

1. **`colors.py`** — 定义亮色/暗色颜色 Token 字典，包含所有语义化颜色
2. **`typography.py`** — 定义字体 Token (字号、字重、行高)
3. **`theme_manager.py`** — 主题管理器单例：
   - 管理 `Theme.LIGHT` / `Theme.DARK` 状态
   - 提供 `toggle_theme()` 切换方法
   - 发射 `theme_changed` 信号通知所有组件
   - 提供 `get_color(token)` / `get_font(token)` 查询方法
4. **`qss_builder.py`** — 根据当前主题动态生成 QSS 样式表，将颜色 Token 注入 QSS 变量

### 阶段三：图标系统 (Step 3)

1. **创建 SVG 图标** — 约 30 个简约线性风格图标，使用统一 stroke-width=1.5、24x24 viewBox
   - 导航类: home, palette, components, settings, info
   - 操作类: search, add, edit, delete, copy, share
   - 方向类: chevron_right, chevron_left, chevron_down, arrow_back
   - 状态类: check, close, warning, error, info_circle
   - 主题类: sun, moon
   - 其他: eye, eye_off, more_horizontal, notifications, user

2. **`icon_provider.py`** — SVG 图标引擎：
   - 从文件加载 SVG
   - 根据主题颜色动态替换 SVG 中的 `currentColor` 占位符
   - 缓存已渲染的 QIcon/QPixmap
   - 支持指定尺寸和颜色覆盖

### 阶段四：组件基类 (Step 4)

1. **`fluent_widget.py`** — 所有自定义组件的基类：
   - 继承自对应 Qt 基类 (QWidget / QPushButton 等)
   - 注册到 ThemeManager，主题切换时自动调用 `on_theme_changed()`
   - 提供 `apply_theme()` 抽象方法供子类实现

2. **`hover_mixin.py`** — 悬停动画混入：
   - `enterEvent` / `leaveEvent` 触发 QPropertyAnimation
   - 平滑过渡背景色/边框色 (150ms, ease-out)
   - 按下状态 `mousePressEvent` 反馈

### 阶段五：核心组件实现 (Step 5-9)

#### Step 5: 按钮组件

| 组件 | 功能 | 关键特性 |
|------|------|----------|
| `FluentButton` | 基础按钮 | 悬停/按下动画，圆角8px，主题感知 |
| `FluentAccentButton` | 强调按钮 | 主色填充，白色文字，阴影 |
| `FluentHyperlink` | 超链接按钮 | 无边框，主色文字，下划线悬停 |
| `FluentToggleButton` | 切换按钮 | 选中/未选中状态切换，视觉反馈 |

#### Step 6: 输入组件

| 组件 | 功能 | 关键特性 |
|------|------|----------|
| `FluentLineEdit` | 输入框 | 底部边框样式，聚焦动画，placeholder |
| `FluentPasswordEdit` | 密码框 | 密码可见/隐藏切换按钮 |
| `FluentSearchEdit` | 搜索框 | 搜索图标，圆角，清空按钮 |
| `FluentCheckBox` | 复选框 | 自绘勾选动画，主题色 |
| `FluentRadioButton` | 单选按钮 | 自绘圆点动画 |
| `FluentSwitch` | 开关 | 滑动动画，主题色轨道 |
| `FluentSlider` | 滑块 | 自定义轨道/滑块样式，主题色 |
| `FluentSpinBox` | 数值框 | 上下按钮，底部边框 |
| `FluentComboBox` | 下拉框 | 圆角弹出，悬停高亮 |

#### Step 7: 导航组件

| 组件 | 功能 | 关键特性 |
|------|------|----------|
| `FluentNavigation` | 侧边导航栏 | 可折叠，图标+文字，选中指示条，分组 |
| `FluentBreadcrumb` | 面包屑 | ">" 分隔符，可点击导航 |
| `FluentTabBar` | 标签栏 | 底部指示条动画，可关闭 |
| `FluentPivot` | 枢轴切换 | 选中下划线滑动动画 |

#### Step 8: 表面组件

| 组件 | 功能 | 关键特性 |
|------|------|----------|
| `FluentCard` | 卡片 | 圆角12px，微阴影，悬停提升效果 |
| `FluentExpander` | 展开面板 | 展开/折叠动画，旋转箭头 |
| `FluentDialog` | 对话框 | 毛玻璃遮罩，缩放进入动画 |

#### Step 9: 反馈 & 展示组件

| 组件 | 功能 | 关键特性 |
|------|------|----------|
| `FluentProgressBar` | 进度条 | 圆角，主题色，不确定态动画 |
| `FluentProgressRing` | 环形进度 | 自绘圆弧，旋转动画 |
| `FluentBadge` | 徽章 | 圆角/圆点，数字/状态色 |
| `FluentTooltip` | 工具提示 | 圆角，淡入动画 |
| `FluentInfoBar` | 信息条 | 成功/警告/错误/信息 四种类型，滑入动画 |
| `FluentAvatar` | 头像 | 圆形裁剪，在线状态指示 |
| `FluentTag` | 标签 | 圆角，可关闭，颜色变体 |
| `FluentSeparator` | 分割线 | 水平/垂直，主题色边框 |

### 阶段六：启动加载界面 (Step 10)

1. **`splash_screen.py`** — 自定义启动画面：
   - 继承 `QWidget`，无边框、置顶
   - 居中显示应用 Logo (Fluent UI 风格图标)
   - 应用名称 + 版本号
   - 加载进度条 (FluentProgressBar)
   - 加载状态文字 ("正在初始化主题..." → "正在加载组件..." → "准备就绪")
   - 淡出过渡到主窗口 (QPropertyAnimation opacity 1→0)
   - 总时长约 2-3 秒

### 阶段七：主窗口 & Hero 页面 (Step 11)

1. **`main_window.py`** — 主窗口布局：
   - 左侧: FluentNavigation 侧边栏 (可折叠)
   - 顶部: 标题栏 (应用名 + 主题切换按钮)
   - 中央: QStackedWidget 切换各展示页
   - 窗口圆角，自定义标题栏 (无边框)

2. **`hero_page.py`** — Hero 展示页：
   - 大标题 "FluentUI Gallery" + 副标题描述
   - 主题色渐变背景装饰
   - 快速导航卡片 (3-4 个特色卡片)
   - 主题切换预览

### 阶段八：组件展示页面 (Step 12)

每个展示页面统一结构：
- 页面标题 + 描述
- 分组展示 (Subtitle + 组件区)
- 每个组件有标题标签和交互区域
- 支持实时主题切换预览

| 页面 | 展示内容 |
|------|----------|
| `button_page.py` | 所有按钮变体、不同尺寸、禁用状态 |
| `input_page.py` | 所有输入组件、验证状态、禁用状态 |
| `navigation_page.py` | 导航栏交互、标签切换、面包屑 |
| `surface_page.py` | 卡片、展开面板、对话框触发 |
| `feedback_page.py` | 进度条/环、徽章、工具提示、信息条 |
| `display_page.py` | 头像、标签、分割线 |

### 阶段九：入口 & 启动脚本 (Step 13)

1. **`main.py`** — 应用入口：
   - 创建 QApplication
   - 设置高 DPI 支持
   - 显示 SplashScreen
   - 初始化 ThemeManager
   - 加载主窗口
   - SplashScreen 淡出过渡

2. **`start.bat`** — Windows 启动脚本：
   ```bat
   @echo off
   call .venv\Scripts\activate.bat
   python app\main.py
   ```

---

## 关键技术实现要点

### 1. 主题切换机制
- ThemeManager 是单例，维护当前主题状态
- 所有 FluentWidget 子类在 `__init__` 中自动注册
- 主题切换时 ThemeManager 发射信号，所有组件调用 `apply_theme()` 更新 QSS
- QSS 通过 `qss_builder.py` 动态生成，替换颜色变量

### 2. 自绘组件
- 使用 `paintEvent(QPaintEvent)` + `QPainter` 自绘：
  - CheckBox: 绘制圆角方框 + 勾选路径动画
  - Switch: 绘制圆角轨道 + 圆形滑块
  - ProgressRing: 绘制圆弧
  - Slider: 绘制轨道 + 滑块
- 使用 `QPropertyAnimation` 驱动动画属性

### 3. SVG 图标着色
- SVG 模板中使用 `fill="currentColor"` 占位
- `icon_provider.py` 读取 SVG 文本，替换 `currentColor` 为实际主题色
- 使用 `QSvgRenderer` 渲染为 QPixmap/QIcon

### 4. 启动画面
- 自定义 QWidget (非 QSplashScreen)，更灵活控制动画
- 使用 QPropertyAnimation 实现淡入淡出
- QTimer 模拟加载进度

### 5. 无边框窗口
- `setWindowFlags(Qt.FramelessWindowHint)`
- 自绘标题栏 (拖拽、最小化、最大化、关闭按钮)
- 支持 `resizeEvent` 边缘拖拽调整大小

---

## 质量检查清单

- [ ] 所有组件支持亮色/暗色模式
- [ ] 文字对比度 ≥ 4.5:1 (WCAG AA)
- [ ] 交互元素有悬停/按下/禁用状态
- [ ] 动画时长在 150-300ms 范围
- [ ] SVG 图标统一 stroke-width 和风格
- [ ] 8px 间距系统一致性
- [ ] 启动画面流畅过渡
- [ ] 侧边导航可折叠
- [ ] Hero 页面视觉冲击力
- [ ] 所有组件可交互，非纯展示
