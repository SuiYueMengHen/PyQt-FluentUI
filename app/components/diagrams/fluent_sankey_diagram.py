import math

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class SankeyNode:
    def __init__(self, name: str, value: float, column: int = 0):
        self.name = name
        self.value = value
        self.column = column
        self.x = 0.0
        self.y = 0.0
        self.width = 20.0
        self.height = 0.0


class SankeyLink:
    def __init__(self, src: int, dst: int, value: float):
        self.src = src
        self.dst = dst
        self.value = value


class FluentSankeyDiagram(QWidget, FluentWidgetBase):
    _anim_progress = 0.0
    node_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._nodes: list[SankeyNode] = []
        self._links: list[SankeyLink] = []
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(300)
        self._anim = None
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(200)
        self._resize_timer.timeout.connect(self._do_layout)
        self._hovered_node_idx = -1
        self.setMouseTracking(True)
        QTimer.singleShot(50, self._start_anim)

    def _start_anim(self):
        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(800)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    @Property(float)
    def anim_progress(self):
        return self._anim_progress

    @anim_progress.setter
    def anim_progress(self, v):
        self._anim_progress = v
        self.update()

    def add_node(self, name: str, value: float, column: int = 0) -> int:
        self._nodes.append(SankeyNode(name, value, column))
        return len(self._nodes) - 1

    def add_link(self, src: int, dst: int, value: float):
        self._links.append(SankeyLink(src, dst, value))

    def auto_layout(self):
        self._resize_timer.start()

    def _do_layout(self):
        if not self._nodes:
            return
        w = self.width()
        h = self.height()
        if w < 50 or h < 50:
            return

        max_col = max(n.column for n in self._nodes)
        col_width = w / (max_col + 1)

        for col in range(max_col + 1):
            col_nodes = [n for n in self._nodes if n.column == col]
            total_value = sum(n.value for n in col_nodes)
            if total_value == 0:
                continue
            available_h = h - 40
            gap = 8
            total_gap = (len(col_nodes) - 1) * gap
            scale = (available_h - total_gap) / total_value

            current_y = 20
            for node in col_nodes:
                node.height = node.value * scale
                node.x = col * col_width + col_width / 2 - node.width / 2
                node.y = current_y
                current_y += node.height + gap

        self.update()

    def _node_at(self, pos):
        for i, node in enumerate(self._nodes):
            rect = QRectF(node.x, node.y, node.width, node.height)
            if rect.contains(pos):
                return i
        return -1

    def _connected_links(self, node_idx):
        result = []
        for i, link in enumerate(self._links):
            if link.src == node_idx or link.dst == node_idx:
                result.append(i)
        return result

    def mouseMoveEvent(self, event):
        self._hovered_node_idx = self._node_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_node_idx = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            idx = self._node_at(event.position())
            if idx >= 0:
                self.node_clicked.emit(self._nodes[idx].name)
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._nodes:
            self._resize_timer.start()

    def paintEvent(self, event):
        if not self._nodes:
            return
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setOpacity(self._anim_progress)

        _LINK_COLORS = ["primary", "accent_success", "accent_warning", "accent_error", "accent_info"]

        highlighted_links = set()
        if self._hovered_node_idx >= 0:
            highlighted_links = set(self._connected_links(self._hovered_node_idx))

        for i, link in enumerate(self._links):
            if link.src >= len(self._nodes) or link.dst >= len(self._nodes):
                continue
            src = self._nodes[link.src]
            dst = self._nodes[link.dst]

            color_key = _LINK_COLORS[i % len(_LINK_COLORS)]
            is_highlighted = (i in highlighted_links)
            link_color = QColor(tm.color(color_key))
            link_color.setAlpha(160 if is_highlighted else 80)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(link_color))

            src_right = src.x + src.width
            src_y = src.y + src.height / 2
            dst_left = dst.x
            dst_y = dst.y + dst.height / 2
            link_h = max(link.value / max(src.value, 1) * src.height, 4)

            path = QPainterPath()
            path.moveTo(src_right, src_y - link_h / 2)
            ctrl_x = (src_right + dst_left) / 2
            path.cubicTo(ctrl_x, src_y - link_h / 2, ctrl_x, dst_y - link_h / 2, dst_left, dst_y - link_h / 2)
            path.lineTo(dst_left, dst_y + link_h / 2)
            path.cubicTo(ctrl_x, dst_y + link_h / 2, ctrl_x, src_y + link_h / 2, src_right, src_y + link_h / 2)
            path.closeSubpath()
            painter.drawPath(path)

        for i, node in enumerate(self._nodes):
            color_key = _LINK_COLORS[node.column % len(_LINK_COLORS)]
            is_hovered = (i == self._hovered_node_idx)
            node_color = QColor(tm.color(color_key))
            if is_hovered:
                node_color = node_color.lighter(120)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(node_color))
            painter.drawRoundedRect(QRectF(node.x, node.y, node.width, node.height), 4, 4)

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Medium)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_primary")))

            if node.column == 0:
                text_rect = QRectF(node.x - 80, node.y, 76, node.height)
                painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, node.name)
            else:
                text_rect = QRectF(node.x + node.width + 4, node.y, 80, node.height)
                painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, node.name)

        if self._hovered_node_idx >= 0:
            node = self._nodes[self._hovered_node_idx]
            text = f"{node.name}: {node.value:.0f}"
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(text) + 16
            th = 24
            tx = node.x + node.width / 2 - tw / 2
            ty = node.y - th - 6
            if ty < 0:
                ty = node.y + node.height + 6

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(tm.color("bg_solid_card")))
            painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
            painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
            painter.setPen(QColor(tm.color("fg_primary")))
            painter.drawText(QRectF(tx, ty, tw, th), Qt.AlignCenter, text)

        painter.end()

    def apply_theme(self):
        self.update()
