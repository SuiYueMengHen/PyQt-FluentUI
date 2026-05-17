from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QSpacerItem
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QPainter, QColor, QPen

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


_PRESET_COLORS = [
    "#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#FFFF00",
    "#7CFC00", "#00FF00", "#00FA9A", "#00CED1", "#00BFFF",
    "#1E90FF", "#0000FF", "#8A2BE2", "#9400D3", "#FF00FF",
    "#FF1493", "#FF69B4", "#DC143C", "#B22222", "#8B0000",
    "#F5F5DC", "#FAEBD7", "#D2B48C", "#BC8F8F", "#808080",
    "#FFFFFF", "#C0C0C0", "#A9A9A9", "#696969", "#000000",
]


class _ColorSwatch(QWidget):
    clicked = Signal(str)

    def __init__(self, color: str, size: int = 28, parent=None):
        super().__init__(parent)
        self._color = color
        self._size = size
        self._tm = ThemeManager()
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        self._hovered = False

    @property
    def color(self):
        return self._color

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self._color)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        rect = QRectF(0, 0, self._size, self._size)
        radius = 4

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self._color))
        painter.drawRoundedRect(rect, radius, radius)

        if self._hovered:
            painter.setPen(QPen(QColor(self._tm.color("primary")), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), radius, radius)

        painter.end()


class FluentColorPicker(QWidget, FluentWidgetBase):
    colorChanged = Signal(str)

    def __init__(self, columns: int = 6, parent=None):
        super().__init__(parent)
        self._columns = columns
        self._selected_color = None
        self._swatches = []

        layout = QGridLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        for i, color in enumerate(_PRESET_COLORS):
            row = i // columns
            col = i % columns
            swatch = _ColorSwatch(color, 28, self)
            swatch.clicked.connect(self._on_swatch_clicked)
            layout.addWidget(swatch, row, col)
            self._swatches.append(swatch)

        layout.addItem(QSpacerItem(0, 12), len(_PRESET_COLORS) // columns + 1, 0, 1, columns)

        self._preview = QLabel()
        self._preview.setFixedHeight(32)
        self._preview.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._preview, len(_PRESET_COLORS) // columns + 2, 0, 1, columns)

        self._init_fluent_base()

    def _on_swatch_clicked(self, color: str):
        self._selected_color = color
        self.colorChanged.emit(color)
        self._update_preview()

    def _update_preview(self):
        tm = self._tm
        if self._selected_color:
            self._preview.setStyleSheet(f"""
                QLabel {{
                    background-color: {self._selected_color};
                    border: 1px solid {tm.color('stroke_card')};
                    border-radius: {tm.radius('sm')}px;
                    color: {"#FFFFFF" if QColor(self._selected_color).lightness() < 128 else "#000000"};
                    font-size: {tm.font_size('caption')}px;
                }}
            """)
            self._preview.setText(self._selected_color)
        else:
            self._preview.setStyleSheet(f"""
                QLabel {{
                    background-color: {tm.color('bg_solid_tertiary')};
                    border: 1px solid {tm.color('stroke_card')};
                    border-radius: {tm.radius('sm')}px;
                    color: {tm.color('fg_tertiary')};
                    font-size: {tm.font_size('caption')}px;
                }}
            """)
            self._preview.setText("No color selected")

    @property
    def selected_color(self):
        return self._selected_color

    @selected_color.setter
    def selected_color(self, value):
        self._selected_color = value
        self._update_preview()

    def apply_theme(self):
        tm = self._tm
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {tm.color('bg_solid_card')};
                border: 1px solid {tm.color('stroke_card')};
                border-radius: {tm.radius('md')}px;
            }}
        """)
        self._update_preview()
