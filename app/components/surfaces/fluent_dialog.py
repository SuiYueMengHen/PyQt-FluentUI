from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.components.buttons.fluent_button import FluentButton
from app.components.buttons.fluent_accent_button import FluentAccentButton
from app.theme.theme_manager import ThemeManager


class FluentDialog(QDialog, FluentWidgetBase):
    def __init__(self, title: str = "Dialog", content: str = "", parent=None):
        super().__init__(parent)
        self._title = title
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(420, 240)

        self._container = QWidget(self)
        self._container.setGeometry(0, 0, 420, 240)

        self._init_fluent_base()

        layout = QVBoxLayout(self._container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self._title_label = QLabel(title)
        layout.addWidget(self._title_label)

        self._content_label = QLabel(content)
        self._content_label.setWordWrap(True)
        layout.addWidget(self._content_label)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self._cancel_btn = FluentButton("取消")
        self._cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self._cancel_btn)

        self._ok_btn = FluentAccentButton("确定")
        self._ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self._ok_btn)

        layout.addLayout(btn_layout)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QColor(0, 0, 0, 100))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        container_rect = QRectF(self._container.geometry())
        painter.setBrush(QColor(tm.color('bg_solid_card')))
        painter.setPen(QPen(QColor(tm.color('stroke_card')), 1))
        painter.drawRoundedRect(container_rect, 12, 12)

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self._title_label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('title_medium')}px; font-weight: 600; background: transparent;")
        self._content_label.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('body')}px; background: transparent;")
        self._container.setStyleSheet("background: transparent;")
