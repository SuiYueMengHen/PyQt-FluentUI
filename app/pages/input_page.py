from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QScrollArea, QButtonGroup
from PySide6.QtCore import Qt

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.inputs.fluent_line_edit import FluentLineEdit
from app.components.inputs.fluent_password_edit import FluentPasswordEdit
from app.components.inputs.fluent_search_edit import FluentSearchEdit
from app.components.inputs.fluent_checkbox import FluentCheckBox
from app.components.inputs.fluent_radio_button import FluentRadioButton
from app.components.inputs.fluent_switch import FluentSwitch
from app.components.inputs.fluent_slider import FluentSlider
from app.components.inputs.fluent_spin_box import FluentSpinBox
from app.components.inputs.fluent_combo_box import FluentComboBox
from app.components.inputs.fluent_text_area import FluentTextArea
from app.components.inputs.fluent_rating import FluentRating
from app.components.inputs.fluent_calendar import FluentCalendar
from app.components.inputs.fluent_color_picker import FluentColorPicker
from app.components.inputs.fluent_toggle_group import FluentToggleGroup
from app.components.inputs.fluent_date_range_picker import FluentDateRangePicker
from app.components.inputs.fluent_time_picker import FluentTimePicker
from app.components.inputs.fluent_numeric_input import FluentNumericInput
from app.components.inputs.fluent_multi_select import FluentMultiSelect
from app.components.inputs.fluent_range_slider import FluentRangeSlider
from app.components.inputs.fluent_auto_complete import FluentAutoComplete
from app.components.inputs.fluent_transfer import FluentTransfer
from app.components.display.fluent_separator import FluentSeparator
from app.theme.theme_manager import ThemeManager


class InputPage(QWidget, FluentWidgetBase):
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

        self._title = QLabel("输入 Inputs")
        layout.addWidget(self._title)

        self._desc = QLabel("输入组件用于接收用户数据。包括文本框、选择器、开关等，共24种输入组件。")
        self._desc.setWordWrap(True)
        layout.addWidget(self._desc)

        layout.addWidget(FluentSeparator())

        self._s1 = QLabel("文本输入")
        layout.addWidget(self._s1)

        row1 = QHBoxLayout()
        row1.setSpacing(16)
        row1.addWidget(FluentLineEdit("请输入文本..."))
        row1.addWidget(FluentPasswordEdit("请输入密码..."))
        row1.addWidget(FluentSearchEdit())
        row1.addStretch()
        layout.addLayout(row1)

        layout.addWidget(FluentSeparator())

        self._s2 = QLabel("选择控件")
        layout.addWidget(self._s2)

        check_row = QHBoxLayout()
        check_row.setSpacing(24)
        check_row.addWidget(FluentCheckBox("选项 1"))
        check_row.addWidget(FluentCheckBox("选项 2"))
        check_row.addWidget(FluentCheckBox("选项 3"))
        check_row.addStretch()
        layout.addLayout(check_row)

        radio_group = QButtonGroup(self)
        radio_row = QHBoxLayout()
        radio_row.setSpacing(24)
        rb1 = FluentRadioButton("选项 A")
        rb2 = FluentRadioButton("选项 B")
        rb3 = FluentRadioButton("选项 C")
        radio_group.addButton(rb1)
        radio_group.addButton(rb2)
        radio_group.addButton(rb3)
        rb1.setChecked(True)
        radio_row.addWidget(rb1)
        radio_row.addWidget(rb2)
        radio_row.addWidget(rb3)
        radio_row.addStretch()
        layout.addLayout(radio_row)

        switch_row = QHBoxLayout()
        switch_row.setSpacing(24)
        sw1 = FluentSwitch()
        sw1.setChecked(True)
        switch_row.addWidget(sw1)
        switch_row.addWidget(QLabel("启用通知"))
        sw2 = FluentSwitch()
        switch_row.addWidget(sw2)
        switch_row.addWidget(QLabel("自动保存"))
        switch_row.addStretch()
        layout.addLayout(switch_row)

        layout.addWidget(FluentSeparator())

        self._s3 = QLabel("数值与选择")
        layout.addWidget(self._s3)

        val_row = QHBoxLayout()
        val_row.setSpacing(16)
        slider = FluentSlider()
        slider.setValue(60)
        val_row.addWidget(QLabel("滑块:"))
        val_row.addWidget(slider, 1)

        spin = FluentSpinBox()
        spin.setValue(42)
        val_row.addWidget(QLabel("数值:"))
        val_row.addWidget(spin)

        combo = FluentComboBox()
        combo.addItems(["选项 1", "选项 2", "选项 3", "选项 4"])
        val_row.addWidget(QLabel("下拉:"))
        val_row.addWidget(combo)
        val_row.addStretch()
        layout.addLayout(val_row)

        layout.addWidget(FluentSeparator())

        self._s4 = QLabel("多行文本")
        layout.addWidget(self._s4)

        text_area_container = QWidget()
        text_area_container.setStyleSheet("background: transparent;")
        text_area_layout = QVBoxLayout(text_area_container)
        text_area_layout.setContentsMargins(0, 0, 0, 0)
        text_area_layout.addWidget(FluentTextArea("请输入多行文本..."))
        layout.addWidget(text_area_container)

        layout.addWidget(FluentSeparator())

        self._s5 = QLabel("评分 / 日历 / 颜色选择器")
        layout.addWidget(self._s5)

        misc_row = QHBoxLayout()
        misc_row.setSpacing(24)
        misc_row.addWidget(FluentRating())
        misc_row.addStretch()
        layout.addLayout(misc_row)

        cal_color_row = QHBoxLayout()
        cal_color_row.setSpacing(24)
        cal_color_row.addWidget(FluentCalendar())
        cal_color_row.addWidget(FluentColorPicker())
        cal_color_row.addStretch()
        layout.addLayout(cal_color_row)

        layout.addWidget(FluentSeparator())

        self._s6 = QLabel("切换按钮组 Toggle Group")
        layout.addWidget(self._s6)

        toggle_container = QWidget()
        toggle_container.setStyleSheet("background: transparent;")
        toggle_layout = QVBoxLayout(toggle_container)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(12)

        tg1 = FluentToggleGroup([
            {"text": "日", "icon": "sun"},
            {"text": "周", "icon": "calendar"},
            {"text": "月", "icon": "chart"},
        ])
        toggle_layout.addWidget(tg1)

        tg2 = FluentToggleGroup([
            {"text": "列表"},
            {"text": "网格"},
            {"text": "看板"},
        ])
        tg2.set_current(1)
        toggle_layout.addWidget(tg2)
        layout.addWidget(toggle_container)

        layout.addWidget(FluentSeparator())

        self._s7 = QLabel("日期范围选择器 DateRangePicker / 时间选择器 TimePicker")
        layout.addWidget(self._s7)

        dt_row = QHBoxLayout()
        dt_row.setSpacing(24)
        dt_row.addWidget(FluentDateRangePicker())
        dt_row.addWidget(FluentTimePicker())
        dt_row.addStretch()
        layout.addLayout(dt_row)

        layout.addWidget(FluentSeparator())

        self._s8 = QLabel("数字输入 NumericInput / 范围滑块 RangeSlider")
        layout.addWidget(self._s8)

        num_row = QHBoxLayout()
        num_row.setSpacing(24)
        num_row.addWidget(FluentNumericInput(value=42, step=1))
        num_row.addWidget(FluentNumericInput(value=3.14, step=0.1, decimals=2))
        num_row.addStretch()
        layout.addLayout(num_row)

        range_row = QHBoxLayout()
        range_row.setSpacing(16)
        range_slider = FluentRangeSlider(min_val=0, max_val=100)
        range_slider.set_values(20, 80)
        range_row.addWidget(QLabel("范围:"))
        range_row.addWidget(range_slider, 1)
        range_row.addStretch()
        layout.addLayout(range_row)

        layout.addWidget(FluentSeparator())

        self._s9 = QLabel("多选下拉 MultiSelect / 自动补全 AutoComplete")
        layout.addWidget(self._s9)

        ms_row = QHBoxLayout()
        ms_row.setSpacing(16)
        ms = FluentMultiSelect("请选择标签")
        ms.set_items([
            {"text": "Python", "value": "python"},
            {"text": "JavaScript", "value": "js"},
            {"text": "Rust", "value": "rust"},
            {"text": "Go", "value": "go"},
            {"text": "TypeScript", "value": "ts"},
        ])
        ms_row.addWidget(ms)

        ac = FluentAutoComplete("搜索语言...")
        ac.set_suggestions(["Python", "JavaScript", "Rust", "Go", "TypeScript", "C++", "Java", "Swift", "Kotlin"])
        ms_row.addWidget(ac)
        ms_row.addStretch()
        layout.addLayout(ms_row)

        layout.addWidget(FluentSeparator())

        self._s10 = QLabel("穿梭框 Transfer")
        layout.addWidget(self._s10)

        transfer = FluentTransfer()
        transfer.set_data(
            source=[
                {"text": "选项 1", "key": "1"},
                {"text": "选项 2", "key": "2"},
                {"text": "选项 3", "key": "3"},
                {"text": "选项 4", "key": "4"},
                {"text": "选项 5", "key": "5"},
            ],
            target=[
                {"text": "已选项 A", "key": "a"},
            ]
        )
        layout.addWidget(transfer)

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
        for w in [self._s1, self._s2, self._s3, self._s4, self._s5, self._s6, self._s7, self._s8, self._s9, self._s10]:
            w.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
