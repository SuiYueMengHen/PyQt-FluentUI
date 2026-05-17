from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon, get_pixmap
from app.theme.theme_manager import ThemeManager
from app.components.inputs.fluent_switch import FluentSwitch
from app.components.inputs.fluent_slider import FluentSlider
from app.components.inputs.fluent_combo_box import FluentComboBox


class FluentSettingRow(QWidget, FluentWidgetBase):
    value_changed = Signal(object)

    def __init__(self, icon_name: str = "", label: str = "", control: str = "switch",
                 options: list = None, min_val: int = 0, max_val: int = 100,
                 default_value=None, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._icon_name = icon_name
        self._label_text = label
        self._control_type = control
        self._options = options or []
        self._min_val = min_val
        self._max_val = max_val
        self._default_value = default_value
        self._hover = False

        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(12, 0, 12, 0)
        self._layout.setSpacing(12)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(20, 20)
        self._layout.addWidget(self._icon_label)

        self._text_label = QLabel(self._label_text)
        self._layout.addWidget(self._text_label, 1)

        self._control_widget = None

        if self._control_type == "switch":
            self._control_widget = FluentSwitch()
            if self._default_value is not None:
                self._control_widget.setChecked(bool(self._default_value))
            self._control_widget.checkedChanged.connect(self._on_switch_changed)
        elif self._control_type == "slider":
            self._control_widget = FluentSlider()
            self._control_widget.setRange(self._min_val, self._max_val)
            if self._default_value is not None:
                self._control_widget.setValue(int(self._default_value))
            else:
                self._control_widget.setValue(self._min_val)
            self._control_widget.valueChanged.connect(self._on_slider_changed)
        elif self._control_type == "combo":
            self._control_widget = FluentComboBox()
            self._control_widget.addItems(self._options)
            if self._default_value is not None and str(self._default_value) in self._options:
                self._control_widget.setCurrentText(str(self._default_value))
            self._control_widget.currentTextChanged.connect(self._on_combo_changed)

        if self._control_widget:
            self._layout.addWidget(self._control_widget)

    def _on_switch_changed(self, checked):
        self.value_changed.emit(checked)

    def _on_slider_changed(self, value):
        self.value_changed.emit(value)

    def _on_combo_changed(self, text):
        self.value_changed.emit(text)

    def value(self):
        if self._control_type == "switch" and self._control_widget:
            return self._control_widget.isChecked()
        elif self._control_type == "slider" and self._control_widget:
            return self._control_widget.value()
        elif self._control_type == "combo" and self._control_widget:
            return self._control_widget.currentText()
        return None

    def set_value(self, val):
        if self._control_type == "switch" and self._control_widget:
            self._control_widget.setChecked(bool(val))
        elif self._control_type == "slider" and self._control_widget:
            self._control_widget.setValue(int(val))
        elif self._control_type == "combo" and self._control_widget:
            self._control_widget.setCurrentText(str(val))

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self._hover:
            painter.fillRect(self.rect(), QColor(self._tm.color("nav_item_hover")))
        else:
            painter.fillRect(self.rect(), QColor(0, 0, 0, 0))
        painter.end()

    def apply_theme(self):
        tm = self._tm
        if self._icon_name:
            pixmap = get_pixmap(self._icon_name, tm.color("fg_secondary"), 20)
            self._icon_label.setPixmap(pixmap)
        self._text_label.setStyleSheet(
            f"color: {tm.color('fg_primary')}; "
            f"font-size: {tm.font_size('body')}px; "
            f"background: transparent;"
        )

    @staticmethod
    def self_check():
        from app.theme.theme_manager import ThemeManager
        from app.icons.icon_provider import get_icon
        tm = ThemeManager()
        errors = []
        for token in ["fg_primary", "fg_secondary", "nav_item_hover"]:
            try:
                tm.color(token)
            except Exception as e:
                errors.append(f"颜色token {token} 获取失败: {e}")
        try:
            icon = get_icon("settings", "#000000", 20)
            if icon.isNull():
                errors.append("图标 settings 加载失败")
        except Exception as e:
            errors.append(f"图标加载异常: {e}")
        if errors:
            return (False, "FluentSettingRow: " + "; ".join(errors))
        return (True, "FluentSettingRow: 所有检查项通过")
