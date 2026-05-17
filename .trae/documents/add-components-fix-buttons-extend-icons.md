# 新增组件、修复按钮、扩展图标计划

## 目标概述

1. 创建简约会员订阅界面
2. 创建与侧拉栏融为一体的用户信息界面（展开：头像+用户名，收缩：仅头像）
3. 创建多位置提示框系统（右上角、右下角、顶部居中、底部居中）
4. 修复退出键白天模式下看不见的问题
5. 修复最大化按钮图标不常见的问题（将"grid"改为"maximize"）
6. 自行想出20个额外图标别名并添加到_ICON_ALIASES
7. 确保所有新组件支持白天黑夜模式

---

## 步骤 1: 修复退出键白天模式可见性问题

**文件**: `e:\FluentUI\app\layout\main_window.py`

**问题分析**: 在[main_window.py:104-116](file:///e:/FluentUI/app/layout/main_window.py#L104-L116)中，关闭按钮使用`tm.color("titlebar_button_close_fg")`（值为`#FFFFFF`白色），背景透明。在白天模式下白色文字在白色标题栏上不可见。

**修复方案**: 
- 关闭按钮在**非hover状态**也应该使用与最小化/最大化按钮相同的`fg_secondary`颜色（`#616161`灰色），而非白色
- hover状态保留红色背景 + 白色图标
- 修改TitleBar.apply_theme()中close按钮的图标颜色逻辑：
  - 非hover: 使用 `fg_secondary` 灰色
  - hover: 使用 `titlebar_button_close_fg` 白色（红色背景上白色清晰）

**实现细节**: 需要为close按钮添加hover状态切换逻辑。使用QPushButton的enterEvent/leaveEvent或通过动态样式表实现。最简单的方案：直接给close按钮在非hover时使用`fg_secondary`颜色，hover时背景变红时图标变白。可以通过设置按钮的icon，同时设置hover样式表来处理。

实际上更简单的方法是：将close按钮的非hover图标颜色改为`fg_secondary`，这样白天模式下可见，hover时背景变为红色后图标改为白色。需要实现icon动态切换。

**具体实现**: 在TitleBar中为close_btn添加enterEvent/leaveEvent处理，hover时切换图标颜色为白色，非hover时为fg_secondary。

---

## 步骤 2: 修复最大化按钮图标

**文件**: `e:\FluentUI\app\layout\main_window.py`

**问题分析**: 在[main_window.py:104](file:///e:/FluentUI/app/layout/main_window.py#L104)中，最大化按钮使用`"grid"`图标，这是"apps"网格图标，不是常见的窗口最大化图标。

**修复方案**: 
- 已确认outline目录存在 `maximize.svg` 和 `minimize.svg` 图标
- 最大化按钮：使用 `"maximize"` 图标
- 最小化按钮：使用 `"minimize"` 图标（当前用的是`"chevron_down"`，也不常见）
- 窗口已最大化时：应切换为 `"minimize"`（还原按钮）

**具体实现**: 修改TitleBar.apply_theme()中按钮图标名映射，并在_on_maximize后更新图标状态。

---

## 步骤 3: 添加20个额外图标别名

**文件**: `e:\FluentUI\app\icons\icon_provider.py`

**20个新图标别名**（均已确认SVG文件存在）:

| 别名 | 映射到SVG | 用途说明 |
|------|-----------|---------|
| `like` | `thumb-up` | 点赞 |
| `dislike` | `thumb-down` |踩/不喜欢 |
| `favorite` | `heart` | 收藏/喜爱 |
| `bookmark` | `bookmark` | 书签/收藏 |
| `share` | `share` | 分享 |
| `copy` | `copy` | 复制 |
| `download` | `download` | 下载 |
| `upload` | `upload` | 上传 |
| `search` | `search` | 搜索 |
| `filter` | `filter` | 筛选 |
| `settings` | `settings` | 设置 |
| `lock` | `lock` | 锁定 |
| `unlock` | `lock-open` | 解锁 |
| `mail` | `mail` | 邮件 |
| `flag` | `flag` | 标记/旗帜 |
| `globe` | `globe` | 全球/国际化 |
| `link` | `link` | 链接 |
| `tag` | `tag` | 标签 |
| `clock` | `clock` | 时间 |
| `wifi` | `wifi` | WiFi |
| `shopping_cart` | `shopping-cart` | 购物车 |
| `ticket` | `ticket` | 票据/工单 |
| `gift` | `gift` | 礼物 |
| `trophy` | `trophy` | 成就/奖杯 |
| `medal` | `medal` | 勋章/奖励 |
| `sparkle` | `sparkle` | 特效/闪耀 |
| `crown` | `crown` | 皇冠/会员 |
| `volume` | `volume` | 音量 |
| `camera` | `camera` | 相机 |
| `music` | `music` | 音乐 |

> 注: 多提供了10个，总共30个新别名，超出要求的20个以确保覆盖面。

---

## 步骤 4: 创建与侧拉栏融为一体的用户信息界面

**文件**: `e:\FluentUI\app\components\navigation\fluent_user_profile.py`（新建）

**设计规格**:
- 位置：FluentNavigation侧边栏底部，与导航列表在同一容器中
- 展开状态：显示圆形头像（40px）+ 用户名 + 用户角色标签
- 收缩状态：仅显示圆形头像（32px）
- 点击交互：可触发用户菜单（后续扩展）
- 动画：跟随侧边栏收缩/展开动画同步过渡

**组件结构**:

```
FluentUserProfile(QWidget, FluentWidgetBase)
├── _avatar_label: QLabel (圆形头像，使用QPainter绘制圆形裁剪)
├── _name_label: QLabel (用户名)
├── _role_label: QLabel (角色/标签)
├── _layout: QHBoxLayout
└── set_collapsed(bool) → 控制文字隐藏/头像缩放
```

**集成方式**: 
- 修改 `FluentNavigation.__init__` 在_scroll下方添加一个固定的底部区域（bottom_widget）
- 将FluentUserProfile放入bottom_widget中
- 在toggle_collapse时同步调用profile.set_collapsed()

**头像处理**: 使用QPainter绘制圆形裁剪的pixmap，创建一个helper方法 `_clip_circle_pixmap(source: QPixmap, size: int) -> QPixmap`。默认使用一个基于crown图标生成的占位头像。

**白天/黑夜模式**: 
- 展开时背景：nav_bg，文字fg_primary
- 收缩时：头像周围可能有微妙的nav_item_hover背景环
- 头像边框：stroke_card颜色

---

## 步骤 5: 创建简约会员订阅界面

**文件**: `e:\FluentUI\app\components\surfaces\fluent_subscription_card.py`（新建）

**设计规格**:
- 简约风格，遵循Fluent Design原则
- 每张订阅卡片包含：计划名称、价格、功能列表、订阅按钮
- 三种卡片层级：免费 / 专业 / 企业
- 当前选中的计划有primary色高亮边框
- 功能列表使用check图标标注已包含功能，x图标标注不包含功能
- 按钮使用accent样式，推荐计划按钮更突出

**组件结构**:

```
FluentSubscriptionCard(QWidget, FluentWidgetBase)
├── _plan_name: QLabel (计划名)
├── _price_label: QLabel (价格)
├── _price_unit: QLabel (单位，如"/月")
├── _features: list[dict] (功能列表，name + included)
├── _subscribe_btn: FluentAccentButton / FluentButton
├── _recommended: bool (是否推荐计划)
└── paintEvent → 绘制卡片背景、边框、推荐徽章
```

**页面集成**: 在 `main.py` 中添加一个新的lazy_page:

```python
window.add_lazy_page("subscription", "会员", "crown", SubscriptionPage)
```

**SubscriptionPage**: 展示3张FluentSubscriptionCard的水平布局，每张卡片的features数据由页面传入。

**白天/黑夜模式**: 
- 卡片背景：bg_solid_card
- 边框：stroke_card，推荐卡片：primary
- 文字：fg_primary / fg_secondary
- 按钮：primary / primary_text_on

---

## 步骤 6: 创建多位置提示框系统

**文件**: `e:\FluentUI\app\components\feedback\fluent_positional_notification.py`（新建）

**设计规格**:
- 支持4个位置：右上角(top_right)、右下角(bottom_right)、顶部居中(top_center)、底部居中(bottom_center)
- 继承现有FluentNotification的设计风格（左侧accent色条、标题+消息）
- 新增：右侧关闭按钮（x图标）、图标标识（左侧accent色条区域增加variant图标）
- 自动消失（默认5秒）+ 手动关闭
- 多通知堆叠：同一位置的多条通知垂直堆叠，间距8px
- 进入动画：根据位置方向滑入（top_right从右上滑入，bottom_right从右下滑入等）
- 退出动画：反向滑出 + fade

**组件结构**:

```
FluentPositionalNotification(QWidget, FluentWidgetBase)
├── 位置枚举: Position (TOP_RIGHT, BOTTOM_RIGHT, TOP_CENTER, BOTTOM_CENTER)
├── _position: Position
├── _title, _message, _variant, _icon_name
├── _close_btn: QPushButton (x图标)
├── _slide_anim: QPropertyAnimation
├── _dismiss_timer: QTimer
├── paintEvent → 绘制卡片+图标+accent条
└── show_at_position(parent) → 计算位置并显示

FluentNotificationManager (单例辅助类)
├── _notifications: dict[Position, list[FluentPositionalNotification]]
├── show(parent, title, message, variant, position, duration)
├── _calculate_position(parent, position, index) → 计算堆叠位置
├── _on_notification_closed(position, notification) → 移除并重新排列
```

**位置计算逻辑**:
- top_right: x = parent.width() - notification.width() - 16, y = 16 + index * (height + 8)
- bottom_right: x = parent.width() - notification.width() - 16, y = parent.height() - (index+1) * (height + 8) - 16
- top_center: x = (parent.width() - notification.width()) / 2, y = 16 + index * (height + 8)
- bottom_center: x = (parent.width() - notification.width()) / 2, y = parent.height() - (index+1) * (height + 8) - 16

**尺寸**: 360 x 80px（比现有320x72略大以容纳关闭按钮）

**白天/黑夜模式**: 与现有FluentNotification保持一致，bg_solid_card背景 + stroke_card边框 + accent色条

---

## 步骤 7: 集成所有新组件到展示页面

**修改文件**: `e:\FluentUI\app\pages\feedback_page.py`

在feedback_page中增加多位置通知的演示按钮区域（4个位置按钮触发不同位置的通知）。

**修改文件**: `e:\FluentUI\app\main.py`

添加新的导航项和页面:
1. `"subscription"` → 会员订阅页面（使用crown图标）
2. 将FluentUserProfile集成到侧边栏底部

**修改文件**: `e:\FluentUI\app\components\navigation\fluent_navigation.py`

在FluentNavigation中添加底部用户信息区域，将FluentUserProfile嵌入。

---

## 步骤 8: 添加主题颜色token（如需要）

**文件**: `e:\FluentUI\app\theme\colors.py`

为新组件检查是否需要新的颜色token。可能需要:
- `subscription_card_recommended_bg` → 可以用primary_light代替
- `subscription_card_recommended_border` → 可以用primary代替
- 大部分颜色可以用现有token覆盖

**结论**: 不需要新增颜色token，现有token足够覆盖所有新组件。

---

## 文件修改总览

### 新建文件
| 文件 | 说明 |
|------|------|
| `app/components/navigation/fluent_user_profile.py` | 侧边栏融合用户信息组件 |
| `app/components/surfaces/fluent_subscription_card.py` | 会员订阅卡片组件 |
| `app/components/feedback/fluent_positional_notification.py` | 多位置通知系统 |
| `app/pages/subscription_page.py` | 会员订阅展示页面 |

### 修改文件
| 文件 | 修改内容 |
|------|---------|
| `app/layout/main_window.py` | 修复关闭按钮白天模式可见性 + 最大化/最小化图标更换 |
| `app/icons/icon_provider.py` | 添加20+个新图标别名 |
| `app/components/navigation/fluent_navigation.py` | 集成FluentUserProfile到底部 |
| `app/pages/feedback_page.py` | 添加多位置通知演示区域 |
| `app/main.py` | 添加subscription导航项 + 侧边栏用户信息初始化 |

---

## 实施顺序

1. **步骤1**: 修复退出键白天模式可见性 → 最紧急的bug修复
2. **步骤2**: 修复最大化按钮图标 → 同属bug修复
3. **步骤3**: 添加图标别名 → 基础依赖，后续组件需要
4. **步骤4**: 创建FluentUserProfile → 修改fluent_navigation.py
5. **步骤5**: 创建FluentSubscriptionCard → 新组件
6. **步骤6**: 创建FluentPositionalNotification → 新组件
7. **步骤7**: 集成到展示页面 → 连接所有组件
8. **步骤8**: 验证白天黑夜模式切换 → 最终检查

---

## UI/UX设计规范（参考ui-ux-pro-max技能）

### 会员订阅卡片
- **风格**: 简约 Fluent Design（圆角8px，微妙阴影，清晰层次）
- **排版**: 价格使用title_large字号 + 700字重，功能列表body字号
- **间距**: 卡片间24px间距，内部padding 24px
- **层次**: 推荐计划使用primary色边框+徽章标注
- **对比度**: 文字颜色确保4.5:1对比度
- **交互**: 按钮hover有primary_hover色变化，150ms过渡

### 用户信息面板
- **风格**: 与侧边栏融为一体（无独立边框）
- **头像**: 圆形裁剪，40px展开 / 32px收缩
- **间距**: 底部padding 16px，头像与文字间距12px
- **层次**: 名称fg_primary + 600字重，角色fg_secondary + 400字重
- **过渡**: 收缩/展开跟随侧边栏动画同步，300ms OutCubic

### 多位置通知
- **风格**: 与现有FluentNotification保持一致（左侧accent色条）
- **尺寸**: 360x80px，比现有略大
- **关闭按钮**: 右侧16px处，x图标14px，fg_tertiary色
- **堆叠间距**: 8px
- **动画**: 300ms OutCubic滑入，反向滑出
- **自动消失**: 5秒后自动关闭，3秒前hover暂停计时器