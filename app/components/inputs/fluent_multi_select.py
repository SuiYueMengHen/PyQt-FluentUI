from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QFrame, QScrollArea
)
from PySide6.QtCore import (
    Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QPoint, QSize
)
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentMultiSelect(QWidget, FluentWidgetBase):
    selection_changed = Signal(list)

    def __init__(self, placeholder: str = "请选择", parent=None):
        super().__init__(parent)
        self._init_fluent_base()

        self._placeholder = placeholder
        self._items: list[dict] = []
        self._selected: list[str] = []
        self._is_open = False
        self._drop_progress = 0.0  # 实例变量，不再作为类变量共享
        self._dropdown_panel = None  # 延迟创建
        self._tag_close_rects: list[tuple[str, QRectF]] = []  # 记录每个标签关闭按钮的区域

        self.setFixedHeight(32)
        self.setMinimumWidth(200)
        self.setCursor(Qt.PointingHandCursor)

        self._drop_anim = QPropertyAnimation(self, b"drop_progress")
        self._drop_anim.setDuration(200)
        self._drop_anim.setEasingCurve(QEasingCurve.OutCubic)

    # ── 公共接口 ──────────────────────────────────────────────

    def add_item(self, text: str, value: str = ""):
        self._items.append({"text": text, "value": value or text})

    def set_items(self, items: list[dict]):
        self._items = items
        # 如果面板已存在，需要重建以反映新数据
        self._destroy_dropdown_panel()

    def selected_values(self) -> list[str]:
        return list(self._selected)

    def clear_selection(self):
        self._selected.clear()
        self._sync_panel_checks()
        self.selection_changed.emit(self._selected)
        self.update()

    # ── 动画属性 ──────────────────────────────────────────────

    @Property(float)
    def drop_progress(self):
        return self._drop_progress

    @drop_progress.setter
    def drop_progress(self, v):
        self._drop_progress = v
        self.update()

    # ── 下拉面板管理 ──────────────────────────────────────────

    def _ensure_dropdown_panel(self):
        """延迟创建下拉面板"""
        if self._dropdown_panel is not None:
            return
        tm = self._tm

        panel = QFrame(self, Qt.Popup | Qt.FramelessWindowHint)
        panel.setObjectName("FluentMultiSelectDropdown")
        panel.setAttribute(Qt.WA_TranslucentBackground, False)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)

        scroll = QScrollArea(panel)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setMaximumHeight(240)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(2)

        for item in self._items:
            cb = QCheckBox(item["text"])
            cb.setProperty("item_value", item["value"])
            cb.setChecked(item["value"] in self._selected)
            cb.setCursor(Qt.PointingHandCursor)
            cb.stateChanged.connect(self._on_checkbox_state_changed)
            container_layout.addWidget(cb)

        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self._apply_panel_style(panel, scroll, container)
        panel.adjustSize()

        self._dropdown_panel = panel

    def _apply_panel_style(self, panel, scroll, container):
        """为下拉面板及其子控件应用主题样式"""
        tm = self._tm
        panel.setStyleSheet(f"""
            QFrame#FluentMultiSelectDropdown {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: 4px;
            }}
        """)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {tm.color('bg_solid_card')};
                border: none;
            }}
            QScrollBar:vertical {{
                background: {tm.color('scrollbar_bg')};
                width: 6px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {tm.color('scrollbar_handle')};
                border-radius: 3px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {tm.color('scrollbar_handle_hover')};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {tm.color('bg_solid_card')};
            }}
        """)
        # 为每个 QCheckBox 应用样式
        for cb in container.findChildren(QCheckBox):
            cb.setStyleSheet(f"""
                QCheckBox {{
                    background-color: transparent;
                    color: {tm.color('fg_primary')};
                    font-size: {tm.font_size('body')}px;
                    spacing: 6px;
                    padding: 6px 8px;
                    border-radius: 3px;
                }}
                QCheckBox:hover {{
                    background-color: {tm.color('bg_solid_tertiary')};
                }}
                QCheckBox::indicator {{
                    width: 16px;
                    height: 16px;
                    border-radius: 3px;
                    border: 1.5px solid {tm.color('stroke_card')};
                    background-color: {tm.color('bg_solid_card')};
                }}
                QCheckBox::indicator:checked {{
                    background-color: {tm.color('primary')};
                    border-color: {tm.color('primary')};
                    image: none;
                }}
            """)

    def _destroy_dropdown_panel(self):
        """销毁下拉面板"""
        if self._dropdown_panel is not None:
            self._dropdown_panel.close()
            self._dropdown_panel.deleteLater()
            self._dropdown_panel = None

    def _show_dropdown(self):
        """显示下拉面板"""
        self._ensure_dropdown_panel()
        panel = self._dropdown_panel
        if panel is None:
            return

        # 定位到触发控件下方
        pos = self.mapToGlobal(QPoint(0, self.height()))
        panel.move(pos)

        # 设置面板宽度与触发控件一致
        panel.setMinimumWidth(self.width())
        panel.setMaximumWidth(max(self.width(), 250))

        panel.show()

    def _hide_dropdown(self):
        """隐藏下拉面板"""
        if self._dropdown_panel is not None:
            self._dropdown_panel.hide()

    def _sync_panel_checks(self):
        """同步面板中复选框的选中状态"""
        if self._dropdown_panel is None:
            return
        scroll = self._dropdown_panel.findChild(QScrollArea)
        if scroll is None:
            return
        for cb in scroll.findChildren(QCheckBox):
            val = cb.property("item_value")
            if val is not None:
                cb.setChecked(val in self._selected)

    # ── 事件处理 ──────────────────────────────────────────────

    def _on_checkbox_state_changed(self, state):
        """复选框状态变更回调"""
        cb = self.sender()
        if cb is None:
            return
        val = cb.property("item_value")
        if val is None:
            return
        if state == Qt.Checked:
            if val not in self._selected:
                self._selected.append(val)
        else:
            if val in self._selected:
                self._selected.remove(val)
        self.selection_changed.emit(self._selected)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 先检查是否点击了标签的关闭按钮
            for val, rect in self._tag_close_rects:
                if rect.contains(event.position()):
                    if val in self._selected:
                        self._selected.remove(val)
                        self._sync_panel_checks()
                        self.selection_changed.emit(self._selected)
                        self.update()
                    return  # 关闭按钮点击不切换下拉
            self._toggle_dropdown()
        super().mousePressEvent(event)

    def _toggle_dropdown(self):
        self._is_open = not self._is_open
        self._drop_anim.stop()
        self._drop_anim.setStartValue(self._drop_progress)
        self._drop_anim.setEndValue(1.0 if self._is_open else 0.0)
        self._drop_anim.start()

        if self._is_open:
            self._show_dropdown()
        else:
            self._hide_dropdown()

    def hideEvent(self, event):
        """当控件自身被隐藏时，同时关闭下拉面板"""
        self._is_open = False
        self._hide_dropdown()
        super().hideEvent(event)

    def resizeEvent(self, event):
        """控件大小变化时更新面板宽度"""
        if self._dropdown_panel is not None and self._dropdown_panel.isVisible():
            self._dropdown_panel.setMinimumWidth(self.width())
        super().resizeEvent(event)

    # ── 绘制 ──────────────────────────────────────────────────

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 背景
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))

        # 边框 - 使用 drop_progress 做颜色渐变
        border_color_open = QColor(tm.color("primary"))
        border_color_closed = QColor(tm.color("stroke_card"))
        p = self._drop_progress
        border_color = QColor(
            int(border_color_closed.red() + (border_color_open.red() - border_color_closed.red()) * p),
            int(border_color_closed.green() + (border_color_open.green() - border_color_closed.green()) * p),
            int(border_color_closed.blue() + (border_color_open.blue() - border_color_closed.blue()) * p),
        )
        painter.setPen(QPen(border_color, 1 + p))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 4, 4)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        self._tag_close_rects.clear()

        if self._selected:
            x = 8
            max_tags = 3
            for val in self._selected[:max_tags]:
                item = next((i for i in self._items if i["value"] == val), None)
                if item:
                    text = item["text"]
                    tw = painter.fontMetrics().horizontalAdvance(text) + 28  # 加宽以容纳关闭按钮
                    tag_color = QColor(tm.color("primary_light"))
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QBrush(tag_color))
                    painter.drawRoundedRect(QRectF(x, 4, tw, self.height() - 8), 3, 3)

                    # 标签文字
                    painter.setPen(QColor(tm.color("primary")))
                    painter.drawText(
                        QRectF(x + 6, 0, tw - 22, self.height()),
                        Qt.AlignVCenter, text
                    )

                    # 关闭 X 按钮
                    close_x = x + tw - 16
                    close_y = (self.height() - 12) / 2
                    close_rect = QRectF(close_x, close_y, 12, 12)
                    self._tag_close_rects.append((val, QRectF(close_rect)))

                    # 绘制 X 标记
                    close_color = QColor(tm.color("primary"))
                    pen = QPen(close_color, 1.2)
                    pen.setCapStyle(Qt.RoundCap)
                    painter.setPen(pen)
                    painter.setBrush(Qt.NoBrush)
                    margin = 3
                    painter.drawLine(
                        close_x + margin, close_y + margin,
                        close_x + 12 - margin, close_y + 12 - margin
                    )
                    painter.drawLine(
                        close_x + 12 - margin, close_y + margin,
                        close_x + margin, close_y + 12 - margin
                    )

                    x += tw + 4

            if len(self._selected) > max_tags:
                painter.setPen(QColor(tm.color("fg_secondary")))
                painter.drawText(
                    QRectF(x, 0, 60, self.height()),
                    Qt.AlignVCenter, f"+{len(self._selected) - max_tags}"
                )
        else:
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(
                QRectF(10, 0, self.width() - 30, self.height()),
                Qt.AlignVCenter, self._placeholder
            )

        # 下拉箭头 - 根据 drop_progress 旋转
        arrow = get_icon("chevron_down", tm.color("fg_secondary"), 12)
        painter.save()
        arrow_x = self.width() - 20
        arrow_y = (self.height() - 12) / 2
        # 箭头旋转中心
        cx = arrow_x + 6
        cy = arrow_y + 6
        painter.translate(cx, cy)
        painter.rotate(180 * p)  # 打开时旋转 180 度
        painter.translate(-cx, -cy)
        painter.drawPixmap(int(arrow_x), int(arrow_y), arrow.pixmap(12, 12))
        painter.restore()

        painter.end()

    # ── 主题 ──────────────────────────────────────────────────

    def apply_theme(self):
        # 主题变化时销毁旧面板，下次打开时以新主题重建
        self._destroy_dropdown_panel()
        self.update()
