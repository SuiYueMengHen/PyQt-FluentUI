from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, QMimeData, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QDrag

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class KanbanCard(QWidget, FluentWidgetBase):
    clicked = Signal(str)
    _hover = 0.0

    def __init__(self, card_id: str, title: str, description: str = "", tag: str = "", tag_color: str = "primary", parent=None):
        super().__init__(parent)
        self._card_id = card_id
        self._title = title
        self._description = description
        self._tag = tag
        self._tag_color = tag_color
        self._init_fluent_base()
        self.setMinimumWidth(200)
        self.setMaximumWidth(280)
        self.setCursor(Qt.PointingHandCursor)
        self._hover_anim = QPropertyAnimation(self, b"hover_progress")
        self._hover_anim.setDuration(150)
        self._hover_anim.setEasingCurve(QEasingCurve.OutCubic)

    @Property(float)
    def hover_progress(self):
        return self._hover

    @hover_progress.setter
    def hover_progress(self, v):
        self._hover = v
        self.update()

    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self._card_id)

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        bg = QColor(tm.color("bg_solid_card"))
        border = QColor(tm.color("stroke_card"))
        if self._hover > 0:
            border = QColor(tm.color("primary"))
            border.setAlpha(int(80 * self._hover))

        painter.setPen(QPen(border, 1))
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 8, 8)

        y = 12
        if self._tag:
            tag_color = QColor(tm.color(self._tag_color))
            tag_color.setAlpha(40)
            painter.setPen(Qt.NoPen)
            painter.setBrush(tag_color)
            tag_rect = QRectF(12, y, 8, 8)
            painter.drawRoundedRect(tag_rect, 4, 4)
            y += 16

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(12, y, self.width() - 24, 20), Qt.AlignLeft | Qt.AlignVCenter, self._title)
        y += 22

        if self._description:
            font.setPixelSize(tm.font_size("caption") - 1)
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            painter.drawText(QRectF(12, y, self.width() - 24, 40), Qt.AlignLeft | Qt.TextWordWrap, self._description)

        painter.end()

    def sizeHint(self):
        h = 60
        if self._tag:
            h += 16
        if self._description:
            h += 40
        return QSize(self.minimumWidth(), h)

    def apply_theme(self):
        self.setStyleSheet("background: transparent;")
        self.update()


class KanbanColumn(QWidget, FluentWidgetBase):
    card_clicked = Signal(str)

    def __init__(self, title: str, color: str = "primary", parent=None):
        super().__init__(parent)
        self._column_title = title
        self._column_color = color
        self._init_fluent_base()
        self.setMinimumWidth(240)
        self.setMaximumWidth(300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._header = QWidget()
        self._header.setFixedHeight(40)
        header_layout = QHBoxLayout(self._header)
        header_layout.setContentsMargins(12, 0, 12, 0)

        self._dot = QWidget()
        self._dot.setFixedSize(8, 8)
        header_layout.addWidget(self._dot)

        self._title_label = QLabel(title)
        header_layout.addWidget(self._title_label)
        header_layout.addStretch()

        self._count_label = QLabel("0")
        header_layout.addWidget(self._count_label)
        layout.addWidget(self._header)

        self._cards_layout = QVBoxLayout()
        self._cards_layout.setSpacing(8)
        layout.addLayout(self._cards_layout)
        layout.addStretch()

        self._cards: list[KanbanCard] = []

    def add_card(self, card: KanbanCard):
        self._cards.append(card)
        self._cards_layout.addWidget(card)
        card.clicked.connect(self.card_clicked.emit)
        self._count_label.setText(str(len(self._cards)))

    def apply_theme(self):
        tm = self._tm
        self._header.setStyleSheet(f"background: transparent;")
        color = QColor(tm.color(self._column_color))
        self._dot.setStyleSheet(f"background-color: {color.name()}; border-radius: 4px;")
        self._title_label.setStyleSheet(f"color: {tm.color('fg_primary')}; font-size: {tm.font_size('body')}px; font-weight: 600; background: transparent;")
        self._count_label.setStyleSheet(f"color: {tm.color('fg_secondary')}; font-size: {tm.font_size('caption')}px; background: transparent;")
        for card in self._cards:
            card.apply_theme()


class FluentKanbanBoard(QWidget, FluentWidgetBase):
    card_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._columns: list[KanbanColumn] = []

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._container = QWidget()
        self._container_layout = QHBoxLayout(self._container)
        self._container_layout.setContentsMargins(8, 8, 8, 8)
        self._container_layout.setSpacing(12)
        self._scroll.setWidget(self._container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._scroll)

    def add_column(self, title: str, color: str = "primary") -> KanbanColumn:
        col = KanbanColumn(title, color)
        self._columns.append(col)
        self._container_layout.addWidget(col)
        col.card_clicked.connect(self.card_clicked.emit)
        return col

    def apply_theme(self):
        tm = self._tm
        self._scroll.setStyleSheet(f"background: transparent; border: none;")
        self._container.setStyleSheet(f"background-color: {tm.color('bg_solid_secondary')}; border-radius: {tm.radius('lg')}px;")
        for col in self._columns:
            col.apply_theme()
