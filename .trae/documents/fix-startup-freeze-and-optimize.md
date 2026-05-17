# FluentUI 启动卡死修复与性能优化计划

## 问题诊断

启动时出现卡死、极高CPU占用、大量报错的根本原因：

### P0 致命问题
1. **所有9个页面在启动时同步实例化** — 200-300+个QWidget在主线程同步创建，阻塞事件循环
2. **强制软件渲染** — `os.environ["QSG_RHI_BACKEND"] = "software"` 导致QPainter开销放大5-10倍
3. **AnimatedBackground 60fps永不停止** — 每16ms触发一次update+paintEvent，即使页面不可见

### P1 严重问题
4. **FluentWidgetBase组件注册无自动清理** — 200+组件注册到_registered_widgets，无__del__方法
5. **QTimer.singleShot(0)导致apply_theme集中爆发** — 200+延迟调用在事件循环启动后同一帧执行
6. **20个图表组件同时创建并启动动画** — 20个QPropertyAnimation同时运行
7. **7+个永不停止的定时器/动画** — Spinner、WaveProgress、Skeleton等即使不可见也持续运行
8. **force_layout同步阻塞主线程** — 150次O(n²)迭代

### P2 中等问题
9. **paintEvent中频繁调用ThemeManager()** — 100+处，每帧重复获取单例
10. **_registered_widgets使用线性列表** — O(n)查找，主题切换时级联式重算
11. **图标固定2倍DPR渲染** — 应使用系统实际DPR
12. **QSS通配符选择器** — `*` 匹配所有QWidget，样式匹配开销大

---

## 修复计划

### 第一阶段：核心性能修复（解决卡死）

#### 1.1 实现页面懒加载
- 修改 `main_window.py`：`add_page` 只存储页面工厂函数，不立即创建页面
- 首次切换到某页面时才创建实例
- 缓存已创建的页面，避免重复创建

#### 1.2 移除强制软件渲染
- 修改 `main.py`：删除 `os.environ["QSG_RHI_BACKEND"] = "software"`
- 仅在GPU不可用时回退

#### 1.3 AnimatedBackground 智能暂停
- 添加 `showEvent`/`hideEvent` 控制
- 页面不可见时停止定时器
- 降低帧率到30fps（33ms间隔）
- 缓存ThemeManager引用

### 第二阶段：组件生命周期优化

#### 2.1 FluentWidgetBase 添加清理机制
- 添加 `__del__` 方法调用 `_cleanup_fluent_base`
- ThemeManager 使用 `WeakSet` 替代列表存储注册组件
- 添加防抖机制限制 `apply_theme` 调用频率

#### 2.2 合并启动时 apply_theme 调用
- 使用批量主题应用，避免200+组件同一帧重算样式
- 只在组件首次显示时调用 apply_theme

#### 2.3 持续动画组件智能暂停
- FluentSpinner：添加 showEvent/hideEvent 暂停/恢复定时器
- FluentWaveProgress：同上
- FluentSkeleton：同上
- FluentCarousel：页面不可见时停止自动播放
- 所有图表组件：不可见时暂停动画

### 第三阶段：性能微优化

#### 3.1 paintEvent 中使用缓存的 ThemeManager
- 所有组件的 paintEvent 使用 `self._tm` 替代 `ThemeManager()`

#### 3.2 图标DPR优化
- 使用 `self.devicePixelRatio()` 替代固定值2

#### 3.3 QSS选择器优化
- 移除 `*` 通配符，使用具体选择器

#### 3.4 force_layout 异步化
- 减少默认迭代次数或延迟到页面可见时计算

---

## 实施步骤

1. 修改 `main.py` — 移除软件渲染
2. 修改 `main_window.py` — 实现页面懒加载
3. 修改 `fluent_widget.py` — 添加__del__、防抖
4. 修改 `theme_manager.py` — 使用WeakSet
5. 修改 `animated_background.py` — 智能暂停
6. 修改 `fluent_spinner.py` — 智能暂停
7. 修改 `fluent_wave_progress.py` — 智能暂停
8. 修改 `fluent_skeleton.py` — 智能暂停、修复初始化顺序
9. 修改 `icon_provider.py` — 动态DPR
10. 修改 `qss_builder.py` — 移除通配符
11. 批量修改所有组件 paintEvent — 使用 self._tm
12. 修改 `diagram_page.py` — 延迟force_layout
13. 修改 `chart_page.py` — 延迟动画启动
14. 测试验证
