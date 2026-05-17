from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class _OverlayWidget(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class FluentDrawer(QWidget, FluentWidgetBase):
    closed = Signal()
    opened = Signal()
    _slide_progress = 0.0

    def __init__(self, edge: str = "left", width: int = 300, parent=None):
        super().__init__(parent)
        self._edge = edge
        self._drawer_width = width
        self._is_open = False
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.hide()

        self._overlay = _OverlayWidget(self)
        self._overlay.clicked.connect(self.close_drawer)

        self._panel = QWidget(self)
        self._panel.setFixedWidth(width)

        self._slide_anim = QPropertyAnimation(self, b"slide_progress")
        self._slide_anim.setDuration(300)
        self._slide_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._init_fluent_base()

    @Property(float)
    def slide_progress(self):
        return self._slide_progress

    @slide_progress.setter
    def slide_progress(self, value):
        self._slide_progress = value
        self._update_geometry()
        self.update()

    def set_content(self, widget: QWidget):
        from PySide6.QtWidgets import QVBoxLayout
        if self._panel.layout():
            old_layout = self._panel.layout()
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            QWidget().setLayout(old_layout)
        layout = QVBoxLayout(self._panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        layout.addWidget(widget)

    def open_drawer(self):
        self._is_open = True
        self.show()
        self.raise_()
        self._slide_anim.stop()
        self._slide_anim.setStartValue(self._slide_progress)
        self._slide_anim.setEndValue(1.0)
        self._slide_anim.start()
        self.opened.emit()

    def close_drawer(self):
        self._is_open = False
        self._slide_anim.stop()
        self._slide_anim.setStartValue(self._slide_progress)
        self._slide_anim.setEndValue(0.0)
        try:
            self._slide_anim.finished.disconnect(self._on_closed)
        except RuntimeError:
            pass
        self._slide_anim.finished.connect(self._on_closed)
        self._slide_anim.start()

    def _on_closed(self):
        self._slide_anim.finished.disconnect(self._on_closed)
        self.hide()
        self.closed.emit()

    def _update_geometry(self):
        if not self.parent():
            return
        parent_rect = self.parent().rect()
        self.setGeometry(parent_rect)

        self._overlay.setGeometry(0, 0, self.width(), self.height())

        if self._edge == "left":
            x = -self._drawer_width + self._drawer_width * self._slide_progress
        else:
            x = self.width() - self._drawer_width * self._slide_progress
        self._panel.setGeometry(int(x), 0, self._drawer_width, self.height())

    def resizeEvent(self, event):
        self._update_geometry()
        super().resizeEvent(event)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        overlay_alpha = int(255 * 0.4 * self._slide_progress)
        painter.setBrush(QColor(0, 0, 0, overlay_alpha))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        panel_rect = QRectF(self._panel.geometry())
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(panel_rect, tm.radius("lg"), tm.radius("lg"))

        painter.end()

    def apply_theme(self):
        tm = self._tm
        self._panel.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
            }}
        """)
        self.update()
