from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QFrame
)
from PySide6.QtCore import (
    Qt, Signal, QPropertyAnimation, QEasingCurve, Property, QRect, QPoint, QSize
)
from PySide6.QtGui import QPainter, QColor, QPixmap, QFont, QFontMetrics

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.navigation.fluent_user_profile import FluentUserProfile
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class NavSubItem(QWidget):
    clicked = Signal(str)
    _hover_progress = 0.0

    def __init__(self, key: str, label: str, parent_key: str = "", parent=None):
        super().__init__(parent)
        self._key = key
        self._parent_key = parent_key
        self._label_text = label
        self._active = False
        self._is_collapsed = False
        self._tm = ThemeManager()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(36)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(42, 0, 12, 0)
        self._layout.setSpacing(8)

        self._dot_label = QLabel()
        self._dot_label.setFixedSize(6, 6)
        self._dot_label.setStyleSheet("background: transparent;")
        self._layout.addWidget(self._dot_label, 0, Qt.AlignVCenter)

        self._text_label = QLabel(label)
        self._layout.addWidget(self._text_label, 0, Qt.AlignVCenter)

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._update_style()

    @property
    def key(self):
        return self._key

    @property
    def parent_key(self):
        return self._parent_key

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self._update_style()
        self.update()

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, value):
        self._hover_progress = value
        self.update()

    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit(self._key)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self._active:
            painter.setBrush(QColor(tm.color('nav_item_active')))
            painter.drawRoundedRect(self.rect().adjusted(4, 2, -4, -2), 6, 6)
        elif self._hover_progress > 0:
            hover_color = QColor(tm.color('nav_item_hover'))
            hover_color.setAlpha(int(255 * self._hover_progress))
            painter.setBrush(hover_color)
            painter.drawRoundedRect(self.rect().adjusted(4, 2, -4, -2), 6, 6)

        painter.end()

    def set_collapsed(self, collapsed: bool):
        if self._is_collapsed == collapsed:
            return
        self._is_collapsed = collapsed
        if collapsed:
            self._text_label.hide()
            self._dot_label.hide()
            self._layout.setContentsMargins(20, 0, 20, 0)
        else:
            self._text_label.show()
            self._dot_label.show()
            self._layout.setContentsMargins(42, 0, 12, 0)

    def _update_style(self):
        tm = self._tm
        dot_color = tm.color('primary') if self._active else tm.color('fg_tertiary')
        self._dot_label.setStyleSheet(
            f"background-color: {dot_color}; border-radius: 3px;"
        )
        text_color = tm.color('primary') if self._active else tm.color('fg_secondary')
        weight = '600' if self._active else '400'
        self._text_label.setStyleSheet(
            f"color: {text_color}; font-size: {tm.font_size('caption')}px; "
            f"background: transparent; font-weight: {weight};"
        )

    def apply_theme(self):
        self._update_style()


class NavItem(QWidget):
    clicked = Signal(str)
    expand_requested = Signal(object)
    _hover_progress = 0.0
    _text_opacity = 1.0

    def __init__(self, key: str, label: str, icon_name: str = "",
                 children: list[dict] | None = None, parent=None):
        super().__init__(parent)
        self._key = key
        self._label_text = label
        self._icon_name = icon_name
        self._active = False
        self._is_collapsed = False
        self._tm = ThemeManager()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._children_data = children or []
        self._expanded = False
        self._children_widgets: list[NavSubItem] = []
        self._arrow_label: QLabel | None = None

        self._icon_label = QLabel(self)
        self._icon_label.setFixedSize(20, 20)
        self._icon_label.setAlignment(Qt.AlignCenter)
        self._icon_label.setStyleSheet("background: transparent;")

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(40, 0, 12, 0)
        self._layout.setSpacing(0)

        self._text_label = QLabel(label)
        self._layout.addWidget(self._text_label, 1, Qt.AlignVCenter)

        if self._children_data:
            self._layout.addStretch()
            self._arrow_label = QLabel()
            self._arrow_label.setFixedSize(16, 16)
            self._arrow_label.setAlignment(Qt.AlignCenter)
            self._arrow_label.setStyleSheet("background: transparent;")
            self._layout.addWidget(self._arrow_label, 0, Qt.AlignVCenter)
            self._update_arrow_icon()

        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._opacity_anim = QPropertyAnimation(self, b"text_opacity")
        self._opacity_anim.setDuration(200)
        self._opacity_anim.setEasingCurve(QEasingCurve.OutCubic)

        if not icon_name:
            self._icon_label.hide()

        self._update_style()

    @property
    def key(self):
        return self._key

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        self._update_style()
        self.update()

    @property
    def has_children(self):
        return len(self._children_data) > 0

    @property
    def expanded(self):
        return self._expanded

    @property
    def children_widgets(self):
        return self._children_widgets

    @Property(float)
    def hover_progress(self):
        return self._hover_progress

    @hover_progress.setter
    def hover_progress(self, value):
        self._hover_progress = value
        self.update()

    @Property(float)
    def text_opacity(self):
        return self._text_opacity

    @text_opacity.setter
    def text_opacity(self, value):
        self._text_opacity = value
        if self._text_opacity <= 0.01:
            self._text_label.hide()
            if self._arrow_label:
                self._arrow_label.hide()
        else:
            if not self._text_label.isVisible():
                self._text_label.show()
            if self._arrow_label and not self._arrow_label.isVisible():
                self._arrow_label.show()
            self._update_text_alpha(value)
        self.update()

    def _update_text_alpha(self, opacity: float):
        alpha_val = int(opacity * 255)
        text_color = self._tm.color('primary') if self._active else self._tm.color('fg_primary')
        qc = QColor(text_color)
        qc.setAlpha(alpha_val)
        weight = '600' if self._active else '400'
        self._text_label.setStyleSheet(
            f"color: {qc.name(QColor.HexArgb)}; font-size: {self._tm.font_size('body')}px; "
            f"background: transparent; font-weight: {weight};"
        )

    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.has_children:
            if self._is_collapsed:
                self.expand_requested.emit(self)
            else:
                self.toggle_expand()
        else:
            self.clicked.emit(self._key)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self._active:
            painter.setBrush(QColor(tm.color('nav_item_active')))
            painter.drawRoundedRect(self.rect().adjusted(4, 2, -4, -2), 6, 6)
        elif self._hover_progress > 0:
            hover_color = QColor(tm.color('nav_item_hover'))
            hover_color.setAlpha(int(255 * self._hover_progress))
            painter.setBrush(hover_color)
            painter.drawRoundedRect(self.rect().adjusted(4, 2, -4, -2), 6, 6)

        painter.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition_icon()

    def _reposition_icon(self):
        icon_y = (self.height() - 20) // 2
        if self._is_collapsed:
            icon_x = max(0, (self.width() - 20) // 2)
        else:
            icon_x = 12
        self._icon_label.move(icon_x, icon_y)

    def set_collapsed(self, collapsed: bool):
        if self._is_collapsed == collapsed:
            return
        self._is_collapsed = collapsed
        if collapsed:
            self._opacity_anim.stop()
            self._opacity_anim.setStartValue(self._text_opacity)
            self._opacity_anim.setEndValue(0.0)
            self._opacity_anim.start()
            self._layout.setContentsMargins(40, 0, 12, 0)
        else:
            self._text_opacity = 1.0
            self._text_label.show()
            self._update_text_alpha(1.0)
            if self._arrow_label:
                self._arrow_label.show()
            self._layout.setContentsMargins(40, 0, 12, 0)
        self._reposition_icon()

    def _build_text_style(self):
        tm = self._tm
        text_color = tm.color('primary') if self._active else tm.color('fg_primary')
        weight = '600' if self._active else '400'
        return (
            f"color: {text_color}; font-size: {tm.font_size('body')}px; "
            f"background: transparent; font-weight: {weight};"
        )

    def toggle_expand(self):
        self._expanded = not self._expanded
        self._update_arrow_icon()
        for child in self._children_widgets:
            if self._expanded:
                child.show()
                child.setMaximumHeight(0)
                anim = QPropertyAnimation(child, b"maximumHeight")
                anim.setDuration(200)
                anim.setEasingCurve(QEasingCurve.OutCubic)
                anim.setStartValue(0)
                anim.setEndValue(36)
                anim.start()
                child._expand_anim = anim
            else:
                anim = QPropertyAnimation(child, b"maximumHeight")
                anim.setDuration(150)
                anim.setEasingCurve(QEasingCurve.InCubic)
                anim.setStartValue(child.maximumHeight())
                anim.setEndValue(0)
                anim.finished.connect(lambda c=child: c.hide())
                anim.start()
                child._collapse_anim = anim

    def collapse_children(self):
        if self._expanded:
            self._expanded = False
            self._update_arrow_icon()
        for child in self._children_widgets:
            child.setMaximumHeight(0)
            child.hide()

    def _update_arrow_icon(self):
        if self._arrow_label is None:
            return
        tm = self._tm
        icon_name = "chevron_down" if self._expanded else "chevron_right"
        icon = get_icon(icon_name, tm.color('fg_secondary'), 16)
        self._arrow_label.setPixmap(icon.pixmap(16, 16))

    def _update_style(self):
        tm = self._tm
        if self._icon_name:
            color = tm.color('primary') if self._active else tm.color('fg_secondary')
            icon = get_icon(self._icon_name, color, 20)
            self._icon_label.setPixmap(icon.pixmap(20, 20))
            self._icon_label.setStyleSheet("background: transparent;")
            self._icon_label.show()

        self._text_label.setStyleSheet(self._build_text_style())

    def apply_theme(self):
        self._update_style()
        self._update_arrow_icon()


class FluentNavigation(QWidget, FluentWidgetBase):
    item_clicked = Signal(str)
    profile_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items: list[NavItem] = []
        self._sub_items: list[NavSubItem] = []
        self._separators: list[QLabel] = []
        self._sub_to_parent: dict[str, str] = {}
        self._collapsed = False
        self._expanded_width = 240
        self._collapsed_width = 60

        self.setFixedWidth(self._expanded_width)

        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        self._header = QWidget()
        self._header.setFixedHeight(48)
        self._header_layout = QHBoxLayout(self._header)
        self._header_layout.setContentsMargins(16, 0, 8, 0)
        self._header_layout.setSpacing(8)

        self._title_label = QLabel("FluentUI")
        self._header_layout.addWidget(self._title_label)
        self._header_layout.addStretch()

        self._collapse_btn = QPushButton()
        self._collapse_btn.setFixedSize(32, 32)
        self._collapse_btn.setCursor(Qt.PointingHandCursor)
        self._collapse_btn.clicked.connect(self.toggle_collapse)
        self._header_layout.addWidget(self._collapse_btn)

        self._main_layout.addWidget(self._header)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._scroll_content = QWidget()
        self._nav_layout = QVBoxLayout(self._scroll_content)
        self._nav_layout.setContentsMargins(8, 8, 8, 8)
        self._nav_layout.setSpacing(2)
        self._nav_layout.addStretch()

        self._indicator = QWidget(self._scroll_content)
        self._indicator.setFixedSize(3, 20)
        self._indicator.setStyleSheet(
            "background-color: #0078d4; border-radius: 1.5px;"
        )
        self._indicator.hide()

        self._indicator_anim = QPropertyAnimation(self._indicator, b"geometry")
        self._indicator_anim.setDuration(250)
        self._indicator_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._scroll.setWidget(self._scroll_content)
        self._main_layout.addWidget(self._scroll)

        self._profile = FluentUserProfile(parent=self)
        self._profile.clicked.connect(self.profile_clicked.emit)
        self._main_layout.addWidget(self._profile)

        self._width_anim = QPropertyAnimation(self, b"nav_width")
        self._width_anim.setDuration(300)
        self._width_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._popup: QFrame | None = None

        self._init_fluent_base()

    @Property(int)
    def nav_width(self):
        return self.width()

    @nav_width.setter
    def nav_width(self, value):
        self.setFixedWidth(value)

    def add_item(self, key: str, label: str, icon_name: str = "",
                 children: list[dict] | None = None):
        item = NavItem(key, label, icon_name, children, self._scroll_content)
        item.clicked.connect(self._on_item_clicked)
        item.expand_requested.connect(self._show_sub_popup)
        self._nav_layout.insertWidget(self._nav_layout.count() - 1, item)
        self._items.append(item)

        if children:
            for child_data in children:
                child_key = child_data.get('key', '')
                child_label = child_data.get('label', '')
                sub_item = NavSubItem(child_key, child_label, key, self._scroll_content)
                sub_item.clicked.connect(self._on_item_clicked)
                self._nav_layout.insertWidget(self._nav_layout.count() - 1, sub_item)
                self._sub_items.append(sub_item)
                self._sub_to_parent[child_key] = key
                item._children_widgets.append(sub_item)
                sub_item.setMaximumHeight(0)
                sub_item.hide()

    def get_parent_key(self, key: str) -> str:
        return self._sub_to_parent.get(key, key)

    def add_separator(self, title: str = ""):
        sep = QLabel(title)
        tm = self._tm
        sep.setStyleSheet(
            f"color: {tm.color('fg_tertiary')}; font-size: {tm.font_size('caption')}px; "
            f"background: transparent; padding: 8px 12px 4px 12px; font-weight: 600; "
            f"letter-spacing: 0.5px;"
        )
        self._nav_layout.insertWidget(self._nav_layout.count() - 1, sep)
        self._separators.append(sep)

    def set_active(self, key: str):
        for item in self._items:
            item.active = (item.key == key)
        for sub in self._sub_items:
            sub.active = (sub.key == key)
        self._animate_indicator(key)

    def _animate_indicator(self, key: str):
        target_widget = None
        for item in self._items:
            if item.key == key:
                target_widget = item
                break
        if target_widget is None:
            for sub in self._sub_items:
                if sub.key == key:
                    target_widget = sub
                    break

        if target_widget is None:
            self._indicator.hide()
            return

        self._indicator.show()
        self._indicator.raise_()

        pos = target_widget.mapTo(self._scroll_content, QPoint(0, 0))
        target_y = pos.y() + (target_widget.height() - 20) // 2

        start_geom = self._indicator.geometry()
        end_geom = QRect(0, target_y, 3, 20)

        self._indicator_anim.stop()
        self._indicator_anim.setStartValue(start_geom)
        self._indicator_anim.setEndValue(end_geom)
        self._indicator_anim.start()

    def _on_item_clicked(self, key: str):
        self.set_active(key)
        parent_key = self.get_parent_key(key)
        if parent_key != key:
            self.item_clicked.emit(parent_key)
            for item in self._items:
                if item.key == parent_key and not item.expanded:
                    item.toggle_expand()
        else:
            self.item_clicked.emit(key)

    def _show_sub_popup(self, nav_item: NavItem):
        self._close_sub_popup()
        if not nav_item.has_children:
            return

        popup = QFrame(self, Qt.Popup | Qt.FramelessWindowHint)
        tm = self._tm
        popup.setStyleSheet(
            f"QFrame {{ background-color: {tm.color('bg_solid_card')}; "
            f"border: 1px solid {tm.color('stroke_card')}; "
            f"border-radius: 8px; padding: 4px; }}"
        )

        popup_layout = QVBoxLayout(popup)
        popup_layout.setContentsMargins(4, 4, 4, 4)
        popup_layout.setSpacing(2)

        for child_data in nav_item._children_data:
            child_key = child_data.get('key', '')
            child_label = child_data.get('label', '')
            btn = QPushButton(child_label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(32)
            btn.setStyleSheet(
                f"QPushButton {{ color: {tm.color('fg_primary')}; "
                f"background: transparent; border: none; border-radius: 4px; "
                f"padding: 4px 12px; text-align: left; "
                f"font-size: {tm.font_size('body')}px; }} "
                f"QPushButton:hover {{ background-color: {tm.color('nav_item_hover')}; }}"
            )
            btn.clicked.connect(lambda checked, k=child_key: self._on_popup_item_clicked(k))
            popup_layout.addWidget(btn)

        popup.adjustSize()

        item_pos = nav_item.mapToGlobal(QPoint(0, 0))
        popup.move(item_pos.x() + self.width(), item_pos.y())

        self._popup = popup
        popup.show()

    def _on_popup_item_clicked(self, key: str):
        self._close_sub_popup()
        self.set_active(key)
        parent_key = self.get_parent_key(key)
        self.item_clicked.emit(parent_key)

    def _close_sub_popup(self):
        if self._popup is not None:
            self._popup.close()
            self._popup.deleteLater()
            self._popup = None

    def toggle_collapse(self):
        self._collapsed = not self._collapsed
        target_width = self._collapsed_width if self._collapsed else self._expanded_width

        for item in self._items:
            item.set_collapsed(self._collapsed)
            if self._collapsed:
                item.collapse_children()

        for sub in self._sub_items:
            sub.set_collapsed(self._collapsed)
            sub.setMaximumHeight(0)
            sub.hide()

        for sep in self._separators:
            sep.setVisible(not self._collapsed)

        self._title_label.setVisible(not self._collapsed)
        self._profile.set_collapsed(self._collapsed)
        self._update_collapse_icon()

        if self._collapsed:
            self._indicator.hide()
        else:
            for item in self._items:
                if item.active:
                    self._animate_indicator(item.key)
                    break
            for sub in self._sub_items:
                if sub.active:
                    self._animate_indicator(sub.key)
                    break

        self._close_sub_popup()

        self._width_anim.stop()
        self._width_anim.setStartValue(self.width())
        self._width_anim.setEndValue(target_width)
        self._width_anim.start()

    def _update_collapse_icon(self):
        tm = self._tm
        icon_name = "chevron_left" if not self._collapsed else "chevron_right"
        self._collapse_btn.setIcon(get_icon(icon_name, tm.color("fg_secondary"), 16))

    def apply_theme(self):
        tm = self._tm
        bg = tm.color('nav_bg')
        self.setStyleSheet(f"background-color: {bg};")
        self._header.setStyleSheet(f"background-color: {bg};")
        self._title_label.setStyleSheet(
            f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; "
            f"font-weight: 600; background: transparent;"
        )
        self._collapse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: {tm.radius('sm')}px;
            }}
            QPushButton:hover {{
                background-color: {tm.color('nav_item_hover')};
            }}
        """)
        self._scroll.setStyleSheet(f"background-color: {bg}; border: none;")
        self._scroll_content.setStyleSheet(f"background-color: {bg};")

        self._indicator.setStyleSheet(
            f"background-color: {tm.color('primary')}; border-radius: 1.5px;"
        )

        self._update_collapse_icon()
        self._profile.apply_theme()
        for item in self._items:
            item.apply_theme()
        for sub in self._sub_items:
            sub.apply_theme()
        for sep in self._separators:
            sep.setStyleSheet(
                f"color: {tm.color('fg_tertiary')}; font-size: {tm.font_size('caption')}px; "
                f"background: transparent; padding: 8px 12px 4px 12px; font-weight: 600; "
                f"letter-spacing: 0.5px;"
            )
