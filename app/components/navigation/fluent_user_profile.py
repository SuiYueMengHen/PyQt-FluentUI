from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QPixmap, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_pixmap
from app.theme.theme_manager import ThemeManager


def _clip_circle_pixmap(source: QPixmap, size: int) -> QPixmap:
    scaled = source.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    dpr = scaled.devicePixelRatio()
    pixel_size = int(size * dpr)
    result = QPixmap(pixel_size, pixel_size)
    result.fill(Qt.transparent)
    painter = QPainter(result)
    painter.setRenderHint(QPainter.Antialiasing, True)
    path = QPainterPath()
    path.addEllipse(0, 0, pixel_size, pixel_size)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, scaled)
    painter.end()
    result.setDevicePixelRatio(dpr)
    return result


class FluentUserProfile(QWidget, FluentWidgetBase):
    clicked = Signal()

    def __init__(self, username: str = "Fluent User", role: str = "Free", parent=None):
        super().__init__(parent)
        self._username = username
        self._role = role
        self._is_collapsed = False
        self._collapsed_avatar_pixmap = QPixmap()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(64)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(12, 8, 12, 8)
        self._layout.setSpacing(12)

        self._avatar_label = QLabel()
        self._avatar_label.setFixedSize(40, 40)
        self._avatar_label.setAlignment(Qt.AlignCenter)
        self._avatar_label.setStyleSheet("background: transparent;")
        self._layout.addWidget(self._avatar_label, 0, Qt.AlignVCenter)

        self._text_container = QWidget()
        self._text_container.setStyleSheet("background: transparent;")
        self._text_layout = QVBoxLayout(self._text_container)
        self._text_layout.setContentsMargins(0, 0, 0, 0)
        self._text_layout.setSpacing(2)

        self._name_label = QLabel(username)
        self._text_layout.addWidget(self._name_label)

        self._role_label = QLabel(role)
        self._text_layout.addWidget(self._role_label)

        self._layout.addWidget(self._text_container, 1, Qt.AlignVCenter)

        self._init_fluent_base()
        self._generate_default_avatar()

    def _generate_default_avatar(self):
        tm = self._tm
        if self._is_collapsed:
            size = 32
            pm = get_pixmap("user", tm.color("primary"), size)
            if not pm.isNull():
                self._collapsed_avatar_pixmap = _clip_circle_pixmap(pm, size)
            else:
                fallback = QPixmap(size, size)
                fallback.fill(QColor(tm.color("primary")))
                self._collapsed_avatar_pixmap = _clip_circle_pixmap(fallback, size)
        else:
            size = 40
            pm = get_pixmap("user", tm.color("primary"), size)
            if not pm.isNull():
                clipped = _clip_circle_pixmap(pm, size)
                self._avatar_label.setPixmap(clipped)
            else:
                fallback = QPixmap(size, size)
                fallback.fill(QColor(tm.color("primary")))
                clipped = _clip_circle_pixmap(fallback, size)
                self._avatar_label.setPixmap(clipped)

    def set_avatar(self, pixmap: QPixmap):
        if self._is_collapsed:
            self._collapsed_avatar_pixmap = _clip_circle_pixmap(pixmap, 32)
        else:
            clipped = _clip_circle_pixmap(pixmap, 40)
            self._avatar_label.setPixmap(clipped)

    def set_collapsed(self, collapsed: bool):
        if self._is_collapsed == collapsed:
            return
        self._is_collapsed = collapsed
        if collapsed:
            self._avatar_label.hide()
            self._text_container.hide()
            self._layout.setContentsMargins(0, 8, 0, 8)
            self._generate_default_avatar()
        else:
            self._avatar_label.show()
            self._text_container.show()
            self._avatar_label.setFixedSize(40, 40)
            self._layout.setContentsMargins(12, 8, 12, 8)
            self._layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self._collapsed_avatar_pixmap = QPixmap()
            self._generate_default_avatar()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("nav_item_hover")))
        painter.drawRoundedRect(self.rect().adjusted(4, 2, -4, -2), 6, 6)
        if self._is_collapsed and not self._collapsed_avatar_pixmap.isNull():
            cx = self.width() / 2
            cy = self.height() / 2
            painter.drawPixmap(int(cx - 16), int(cy - 16), self._collapsed_avatar_pixmap)
        painter.end()

    def apply_theme(self):
        tm = self._tm
        self._name_label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('body')}px; font-weight: 600; background: transparent;")
        self._role_label.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('caption')}px; background: transparent;")
        self._generate_default_avatar()
        self.update()

    @staticmethod
    def self_check():
        from app.theme.theme_manager import ThemeManager
        from app.icons.icon_provider import get_pixmap
        tm = ThemeManager()
        errors = []
        for token in ["primary", "fg_primary", "fg_secondary", "nav_item_hover"]:
            try:
                tm.color(token)
            except Exception as e:
                errors.append(f"颜色token {token} 获取失败: {e}")
        for icon_name in ["user"]:
            try:
                pm = get_pixmap(icon_name, "#000000", 20)
                if pm.isNull():
                    errors.append(f"图标 {icon_name} 加载失败")
            except Exception as e:
                errors.append(f"图标 {icon_name} 加载异常: {e}")
        if 64 < 1 or 64 > 512:
            errors.append(f"fixedHeight 64 不在合理范围 [1, 512]")
        if errors:
            return (False, "FluentUserProfile: " + "; ".join(errors))
        return (True, "FluentUserProfile: 所有检查项通过")
