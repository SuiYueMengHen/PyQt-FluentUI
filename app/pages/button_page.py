from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.buttons.fluent_button import FluentButton
from app.components.buttons.fluent_accent_button import FluentAccentButton
from app.components.buttons.fluent_hyperlink import FluentHyperlink
from app.components.buttons.fluent_toggle_button import FluentToggleButton
from app.components.buttons.fluent_icon_button import FluentIconButton
from app.components.buttons.fluent_split_button import FluentSplitButton
from app.components.buttons.fluent_command_bar_button import FluentCommandBarButton
from app.components.buttons.fluent_dropdown_button import FluentDropDownButton
from app.components.buttons.fluent_pill_button import FluentPillButton
from app.components.buttons.fluent_fab import FluentFloatingActionButton
from app.components.display.fluent_separator import FluentSeparator
from app.theme.theme_manager import ThemeManager


class ButtonPage(QWidget, FluentWidgetBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        self._title = QLabel("按钮 Buttons")
        layout.addWidget(self._title)

        self._desc = QLabel("按钮用于触发操作或事件。Fluent Design 风格按钮提供多种变体，共11种按钮类型。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._section1_title = QLabel("基础按钮")
        layout.addWidget(self._section1_title)

        row1 = QHBoxLayout()
        row1.setSpacing(12)
        row1.addWidget(FluentButton("默认按钮"))
        row1.addWidget(FluentAccentButton("强调按钮"))
        row1.addWidget(FluentHyperlink("超链接"))
        btn_disabled = FluentButton("禁用状态")
        btn_disabled.setEnabled(False)
        row1.addWidget(btn_disabled)
        row1.addStretch()
        layout.addLayout(row1)

        layout.addWidget(FluentSeparator())

        self._section2_title = QLabel("切换按钮")
        layout.addWidget(self._section2_title)

        row2 = QHBoxLayout()
        row2.setSpacing(12)
        row2.addWidget(FluentToggleButton("选项 A"))
        row2.addWidget(FluentToggleButton("选项 B"))
        row2.addWidget(FluentToggleButton("选项 C"))
        row2.addStretch()
        layout.addLayout(row2)

        layout.addWidget(FluentSeparator())

        self._section3_title = QLabel("不同尺寸")
        layout.addWidget(self._section3_title)

        row3 = QHBoxLayout()
        row3.setSpacing(12)
        small_btn = FluentButton("小号")
        small_btn.setFixedHeight(28)
        row3.addWidget(small_btn)
        row3.addWidget(FluentButton("中号"))
        large_btn = FluentAccentButton("大号")
        large_btn.setFixedHeight(44)
        row3.addWidget(large_btn)
        row3.addStretch()
        layout.addLayout(row3)

        layout.addWidget(FluentSeparator())

        self._section4_title = QLabel("图标按钮 IconButton")
        layout.addWidget(self._section4_title)

        row4 = QHBoxLayout()
        row4.setSpacing(12)
        for icon_name in ["home", "settings", "search", "bell", "heart"]:
            row4.addWidget(FluentIconButton(icon_name))
        row4.addStretch()
        layout.addLayout(row4)

        layout.addWidget(FluentSeparator())

        self._section5_title = QLabel("胶囊按钮 PillButton")
        layout.addWidget(self._section5_title)

        row5 = QHBoxLayout()
        row5.setSpacing(12)
        row5.addWidget(FluentPillButton("标签一"))
        row5.addWidget(FluentPillButton("标签二", selected=True))
        row5.addWidget(FluentPillButton("标签三"))
        row5.addStretch()
        layout.addLayout(row5)

        layout.addWidget(FluentSeparator())

        self._section6_title = QLabel("分割按钮 SplitButton / 下拉按钮 DropDownButton")
        layout.addWidget(self._section6_title)

        row6 = QHBoxLayout()
        row6.setSpacing(12)
        row6.addWidget(FluentSplitButton("保存"))
        row6.addWidget(FluentDropDownButton("更多选项"))
        row6.addStretch()
        layout.addLayout(row6)

        layout.addWidget(FluentSeparator())

        self._section7_title = QLabel("命令栏按钮 CommandBarButton")
        layout.addWidget(self._section7_title)

        row7 = QHBoxLayout()
        row7.setSpacing(8)
        for icon_name in ["home", "mail", "calendar", "share"]:
            row7.addWidget(FluentCommandBarButton(icon_name))
        row7.addStretch()
        layout.addLayout(row7)

        layout.addWidget(FluentSeparator())

        self._section8_title = QLabel("浮动操作按钮 FAB")
        layout.addWidget(self._section8_title)

        row8 = QHBoxLayout()
        row8.setSpacing(12)
        row8.addWidget(FluentFloatingActionButton("plus"))
        row8.addWidget(FluentFloatingActionButton("edit"))
        row8.addStretch()
        layout.addLayout(row8)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"background-color: {tm.color('bg_solid_base')};")
        self._title.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_large')}px; font-weight: 700; background: transparent;")
        self._desc.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent; line-height: 1.5;")
        for w in [self._section1_title, self._section2_title, self._section3_title,
                  self._section4_title, self._section5_title, self._section6_title,
                  self._section7_title, self._section8_title]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
