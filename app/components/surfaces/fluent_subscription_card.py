from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentSubscriptionCard(QWidget, FluentWidgetBase):
    subscribe_clicked = Signal(str)

    def __init__(self, plan_name: str = "", price: str = "", price_unit: str = "",
                 features: list = None, recommended: bool = False, parent=None):
        super().__init__(parent)
        self._plan_name = plan_name
        self._price = price
        self._price_unit = price_unit
        self._features = features or []
        self._recommended = recommended
        self._hover_progress = 0.0

        self.setFixedWidth(260)
        self.setMinimumHeight(360)
        self.setCursor(Qt.PointingHandCursor)

        self._card_layout = QVBoxLayout(self)
        self._card_layout.setContentsMargins(24, 24, 24, 24)
        self._card_layout.setSpacing(12)

        if recommended:
            self._badge_label = QLabel("推荐")
            self._card_layout.addWidget(self._badge_label, 0, Qt.AlignRight)
        else:
            self._badge_label = None

        self._plan_label = QLabel(plan_name)
        self._card_layout.addWidget(self._plan_label)

        price_row = QHBoxLayout()
        price_row.setSpacing(4)
        self._price_label = QLabel(price)
        price_row.addWidget(self._price_label, 0, Qt.AlignBottom)
        self._unit_label = QLabel(price_unit)
        price_row.addWidget(self._unit_label, 0, Qt.AlignBottom)
        price_row.addStretch()
        self._card_layout.addLayout(price_row)

        self._card_layout.addSpacing(8)

        self._feature_widgets = []
        for feat in self._features:
            row = QHBoxLayout()
            row.setSpacing(8)
            icon_label = QLabel()
            icon_label.setFixedSize(16, 16)
            icon_label.setStyleSheet("background: transparent;")
            name_label = QLabel(feat.get("name", ""))
            name_label.setWordWrap(True)
            row.addWidget(icon_label)
            row.addWidget(name_label, 1)
            self._feature_widgets.append((icon_label, name_label, feat.get("included", True)))
            self._card_layout.addLayout(row)

        self._card_layout.addStretch()

        self._subscribe_btn = QPushButton("订阅")
        self._subscribe_btn.setFixedHeight(36)
        self._subscribe_btn.setCursor(Qt.PointingHandCursor)
        self._subscribe_btn.clicked.connect(lambda: self.subscribe_clicked.emit(self._plan_name))
        self._card_layout.addWidget(self._subscribe_btn)

        self._init_fluent_base()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        border_color = QColor(tm.color("primary")) if self._recommended else QColor(tm.color("stroke_card"))
        pen = QPen(border_color, 2 if self._recommended else 1)
        painter.setPen(pen)
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0.5, 0.5, self.width() - 1, self.height() - 1), 8, 8)

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet("background: transparent;")

        if self._badge_label:
            self._badge_label.setStyleSheet(
                f"color: {tm.color('primary')}; font-size: {tm.font_size('caption')}px; "
                f"font-weight: 600; background: {tm.color('primary_light')}; "
                f"padding: 2px 10px; border-radius: 10px;"
            )

        self._plan_label.setStyleSheet(
            f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; "
            f"font-weight: 700; background: transparent;"
        )

        self._price_label.setStyleSheet(
            f"color: {tm.color('fg_primary')}; font-size: 32px; font-weight: 700; background: transparent;"
        )
        self._unit_label.setStyleSheet(
            f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent; padding-bottom: 4px;"
        )

        for icon_label, name_label, included in self._feature_widgets:
            if included:
                icon = get_icon("check", tm.color("accent_success"), 16)
                name_label.setStyleSheet(
                    f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('body')}px; background: transparent;"
                )
            else:
                icon = get_icon("close", tm.color("fg_disabled"), 16)
                name_label.setStyleSheet(
                    f"color: {tm.color('fg_disabled')}; font-size: {tm.font_size('body')}px; background: transparent;"
                )
            icon_label.setPixmap(icon.pixmap(16, 16))

        if self._recommended:
            self._subscribe_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {tm.color('primary')};
                    border: none;
                    border-radius: {tm.radius('md')}px;
                    color: {tm.color('primary_text_on')};
                    font-size: {tm.font_size('body')}px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {tm.color('primary_hover')};
                }}
                QPushButton:pressed {{
                    background-color: {tm.color('primary_pressed')};
                }}
            """)
        else:
            self._subscribe_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: 1px solid {tm.color('stroke_card')};
                    border-radius: {tm.radius('md')}px;
                    color: {tm.color('fg_primary')};
                    font-size: {tm.font_size('body')}px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {tm.color('nav_item_hover')};
                    border-color: {tm.color('stroke_hover')};
                }}
                QPushButton:pressed {{
                    background-color: {tm.color('bg_solid_tertiary')};
                }}
            """)

        self.update()

    @staticmethod
    def self_check():
        from app.theme.theme_manager import ThemeManager
        from app.icons.icon_provider import get_icon
        tm = ThemeManager()
        errors = []
        for token in ["primary", "primary_light", "primary_text_on", "primary_hover", "primary_pressed", "fg_primary", "fg_secondary", "fg_disabled", "bg_solid_card", "stroke_card", "stroke_hover", "nav_item_hover", "bg_solid_tertiary", "accent_success"]:
            try:
                tm.color(token)
            except Exception as e:
                errors.append(f"颜色token {token} 获取失败: {e}")
        for icon_name in ["check", "close"]:
            try:
                icon = get_icon(icon_name, "#000000", 20)
                if icon.isNull():
                    errors.append(f"图标 {icon_name} 加载失败")
            except Exception as e:
                errors.append(f"图标 {icon_name} 加载异常: {e}")
        if 260 < 1 or 260 > 1024:
            errors.append(f"fixedWidth 260 不在合理范围 [1, 1024]")
        if 360 < 1 or 360 > 2048:
            errors.append(f"minHeight 360 不在合理范围 [1, 2048]")
        if errors:
            return (False, "FluentSubscriptionCard: " + "; ".join(errors))
        return (True, "FluentSubscriptionCard: 所有检查项通过")
