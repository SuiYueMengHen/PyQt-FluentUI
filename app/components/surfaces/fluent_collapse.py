from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QParallelAnimationGroup
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentCollapse(QWidget, FluentWidgetBase):
    _content_height = 0.0

    def __init__(self, title: str = "折叠面板", expanded: bool = False, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._title = title
        self._expanded = expanded
        self._header_height = 40
        self._content_widget = None
        self._content_max_h = 200
        self.setMinimumWidth(200)
        self.setFixedHeight(self._header_height)
        self.setCursor(Qt.PointingHandCursor)

        self._expand_anim = QPropertyAnimation(self, b"content_height")
        self._expand_anim.setDuration(300)
        self._expand_anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_content(self, widget: QWidget, max_height: int = 200):
        if self._content_widget:
            self._content_widget.setParent(None)
            self._content_widget.deleteLater()
        self._content_widget = widget
        self._content_widget.setParent(self)
        self._content_max_h = max_height
        if self._expanded:
            self._content_height = float(max_height)
            self.setFixedHeight(self._header_height + max_height)
            self._content_widget.setGeometry(0, self._header_height, self.width(), max_height)
            self._content_widget.show()
        else:
            self._content_widget.hide()

    def toggle(self):
        self._expanded = not self._expanded
        self._expand_anim.stop()
        self._expand_anim.setStartValue(self._content_height)
        self._expand_anim.setEndValue(float(self._content_max_h) if self._expanded else 0.0)
        self._expand_anim.start()
        if self._expanded:
            self._content_widget.show()

    @Property(float)
    def content_height(self):
        return self._content_height

    @content_height.setter
    def content_height(self, v):
        self._content_height = v
        self.setFixedHeight(int(self._header_height + v))
        if self._content_widget:
            self._content_widget.setGeometry(0, self._header_height, self.width(), int(v))
            self._content_widget.setVisible(v > 0)
        self.update()

    def mousePressEvent(self, event):
        if event.position().y() < self._header_height:
            self.toggle()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 6, 6)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(16, 0, self.width() - 40, self._header_height), Qt.AlignVCenter | Qt.AlignLeft, self._title)

        arrow = "▼" if self._expanded else "▶"
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_tertiary")))
        painter.drawText(QRectF(self.width() - 30, 0, 24, self._header_height), Qt.AlignCenter, arrow)

        painter.end()

    def apply_theme(self):
        self.update()
