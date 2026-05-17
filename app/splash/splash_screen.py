from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QFont

from app.theme.theme_manager import ThemeManager
from app.components.feedback.fluent_progress_bar import FluentProgressBar


class SplashScreen(QWidget):
    _opacity = 1.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(480, 320)

        screen = self.screen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

        self._container = QWidget(self)
        self._container.setGeometry(0, 0, 480, 320)

        layout = QVBoxLayout(self._container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)

        self._logo_label = QLabel()
        self._logo_label.setFixedSize(64, 64)
        self._logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._logo_label, alignment=Qt.AlignCenter)

        self._title_label = QLabel("FluentUI Gallery")
        self._title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._title_label)

        self._version_label = QLabel("v1.0.0")
        self._version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._version_label)

        layout.addSpacing(24)

        self._progress = FluentProgressBar()
        self._progress.setFixedWidth(300)
        layout.addWidget(self._progress, alignment=Qt.AlignCenter)

        self._status_label = QLabel("正在初始化...")
        self._status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._status_label)

        self._fade_anim = QPropertyAnimation(self, b"window_opacity")
        self._fade_anim.setDuration(500)
        self._fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        self._load_steps = [
            (0, 20, "正在初始化主题..."),
            (20, 50, "正在加载图标..."),
            (50, 80, "正在构建组件..."),
            (80, 100, "准备就绪"),
        ]
        self._current_step = 0
        self._step_timer = QTimer(self)
        self._step_timer.timeout.connect(self._next_step)

        self._apply_splash_theme()

    def _apply_splash_theme(self):
        tm = ThemeManager()
        self._container.setStyleSheet(f"""
            QWidget {{
                background-color: {tm.color('bg_solid_card')};
                border-radius: 16px;
            }}
        """)
        self._title_label.setStyleSheet(f"""
            color: {tm.color('fg_primary')};
            font-size: 28px;
            font-weight: 700;
            background: transparent;
        """)
        self._version_label.setStyleSheet(f"""
            color: {tm.color('fg_tertiary')};
            font-size: 12px;
            background: transparent;
        """)
        self._status_label.setStyleSheet(f"""
            color: {tm.color('fg_secondary')};
            font-size: 12px;
            background: transparent;
        """)

        from app.icons.icon_provider import get_icon
        icon = get_icon("palette", tm.color("primary"), 64)
        self._logo_label.setPixmap(icon.pixmap(64, 64))

    @Property(float)
    def window_opacity(self):
        return self._opacity

    @window_opacity.setter
    def window_opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    def start_loading(self, on_finished=None):
        self._on_finished = on_finished
        self.show()
        self._step_timer.start(500)

    def _next_step(self):
        if self._current_step >= len(self._load_steps):
            self._step_timer.stop()
            self._progress.value = 100
            QTimer.singleShot(300, self._fade_out)
            return

        start_val, end_val, status = self._load_steps[self._current_step]
        self._status_label.setText(status)
        self._progress.value = end_val
        self._current_step += 1

    def _fade_out(self):
        self._fade_anim.stop()
        self._fade_anim.setStartValue(1.0)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.finished.connect(self._on_fade_finished)
        self._fade_anim.start()

    def _on_fade_finished(self):
        self.close()
        if hasattr(self, '_on_finished') and self._on_finished:
            self._on_finished()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 0))
        painter.drawRect(self.rect())
        painter.end()
