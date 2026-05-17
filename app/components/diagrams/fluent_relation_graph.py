import math
import random

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class RelationNode:
    def __init__(self, name: str, group: str = "", size: float = 24):
        self.name = name
        self.group = group
        self.size = size
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0


class RelationEdge:
    def __init__(self, src: int, dst: int, weight: float = 1.0, label: str = ""):
        self.src = src
        self.dst = dst
        self.weight = weight
        self.label = label


_GROUP_COLORS = [
    "primary", "accent_success", "accent_warning", "accent_error", "accent_info",
]


class FluentRelationGraph(QWidget, FluentWidgetBase):
    _anim_progress = 0.0
    node_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(350)
        self._nodes: list[RelationNode] = []
        self._edges: list[RelationEdge] = []
        self._anim = None
        self._layout_done = False
        self._hovered_node_idx = -1
        self.setMouseTracking(True)
        QTimer.singleShot(50, self._start_anim)

    def _start_anim(self):
        self._anim = QPropertyAnimation(self, b"anim_progress")
        self._anim.setDuration(600)
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

    def add_node(self, name: str, group: str = "", size: float = 24) -> int:
        node = RelationNode(name, group, size)
        cx = self.width() / 2
        cy = self.height() / 2
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(50, 150)
        node.x = cx + dist * math.cos(angle)
        node.y = cy + dist * math.sin(angle)
        self._nodes.append(node)
        return len(self._nodes) - 1

    def add_edge(self, src: int, dst: int, weight: float = 1.0, label: str = ""):
        self._edges.append(RelationEdge(src, dst, weight, label))

    def force_layout(self, iterations: int = 100):
        if not self._nodes:
            return
        cx = self.width() / 2
        cy = self.height() / 2
        padding = 40

        for _ in range(iterations):
            for node in self._nodes:
                node.vx = 0
                node.vy = 0

            for i, n1 in enumerate(self._nodes):
                for j, n2 in enumerate(self._nodes):
                    if i >= j:
                        continue
                    dx = n2.x - n1.x
                    dy = n2.y - n1.y
                    dist = max(math.sqrt(dx * dx + dy * dy), 1)
                    repulsion = 3000 / (dist * dist)
                    fx = repulsion * dx / dist
                    fy = repulsion * dy / dist
                    n1.vx -= fx
                    n1.vy -= fy
                    n2.vx += fx
                    n2.vy += fy

            for edge in self._edges:
                if edge.src >= len(self._nodes) or edge.dst >= len(self._nodes):
                    continue
                n1 = self._nodes[edge.src]
                n2 = self._nodes[edge.dst]
                dx = n2.x - n1.x
                dy = n2.y - n1.y
                dist = max(math.sqrt(dx * dx + dy * dy), 1)
                attraction = dist * 0.01 * edge.weight
                fx = attraction * dx / dist
                fy = attraction * dy / dist
                n1.vx += fx
                n1.vy += fy
                n2.vx -= fx
                n2.vy -= fy

            for node in self._nodes:
                dx = cx - node.x
                dy = cy - node.y
                node.vx += dx * 0.001
                node.vy += dy * 0.001

                node.x += node.vx * 0.5
                node.y += node.vy * 0.5

                node.x = max(padding, min(self.width() - padding, node.x))
                node.y = max(padding, min(self.height() - padding, node.y))

        self._layout_done = True
        self.update()

    def _node_at(self, pos):
        for i, node in enumerate(self._nodes):
            r = node.size / 2 + 4
            dx = pos.x() - node.x
            dy = pos.y() - node.y
            if dx * dx + dy * dy <= r * r:
                return i
        return -1

    def _connected_node_indices(self, node_idx):
        result = set()
        for edge in self._edges:
            if edge.src == node_idx:
                result.add(edge.dst)
            elif edge.dst == node_idx:
                result.add(edge.src)
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

    def paintEvent(self, event):
        if not self._nodes:
            return
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setOpacity(self._anim_progress)

        connected = set()
        if self._hovered_node_idx >= 0:
            connected = self._connected_node_indices(self._hovered_node_idx)

        for edge in self._edges:
            self._draw_edge(painter, edge, tm, connected)

        for i, node in enumerate(self._nodes):
            is_hovered = (i == self._hovered_node_idx)
            is_connected = (i in connected)
            self._draw_node(painter, node, tm, is_hovered, is_connected)

        if self._hovered_node_idx >= 0:
            self._draw_tooltip(painter, self._nodes[self._hovered_node_idx], tm, connected)

        painter.end()

    def _draw_edge(self, painter: QPainter, edge: RelationEdge, tm: ThemeManager, connected: set):
        if edge.src >= len(self._nodes) or edge.dst >= len(self._nodes):
            return
        n1 = self._nodes[edge.src]
        n2 = self._nodes[edge.dst]

        is_highlighted = (self._hovered_node_idx >= 0 and
                         (edge.src == self._hovered_node_idx or edge.dst == self._hovered_node_idx))

        alpha = int(40 + 60 * min(edge.weight, 3) / 3) if not is_highlighted else 200
        pen_color = QColor(tm.color("primary") if is_highlighted else "fg_tertiary")
        pen_color.setAlpha(alpha)
        width = (1 + edge.weight * 0.5) if not is_highlighted else (2 + edge.weight * 0.5)
        painter.setPen(QPen(pen_color, width))
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(int(n1.x), int(n1.y), int(n2.x), int(n2.y))

        if edge.label:
            font = QFont()
            font.setPixelSize(tm.font_size("caption") - 2)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            mx = (n1.x + n2.x) / 2
            my = (n1.y + n2.y) / 2
            painter.drawText(QRectF(mx - 30, my - 10, 60, 20), Qt.AlignCenter, edge.label)

    def _draw_node(self, painter: QPainter, node: RelationNode, tm: ThemeManager, is_hovered: bool = False, is_connected: bool = False):
        group_idx = hash(node.group) % len(_GROUP_COLORS) if node.group else 0
        color_key = _GROUP_COLORS[group_idx]
        node_color = QColor(tm.color(color_key))

        r = node.size / 2
        if is_hovered:
            r += 3

        glow = QColor(node_color)
        glow.setAlpha(50 if is_hovered or is_connected else 30)
        painter.setPen(Qt.NoPen)
        painter.setBrush(glow)
        glow_r = r + (6 if is_hovered else 4)
        painter.drawEllipse(QRectF(node.x - glow_r, node.y - glow_r, glow_r * 2, glow_r * 2))

        painter.setBrush(node_color)
        painter.setPen(QPen(QColor(tm.color("bg_solid_card")), 2))
        painter.drawEllipse(QRectF(node.x - r, node.y - r, r * 2, r * 2))

        font = QFont()
        font.setPixelSize(tm.font_size("caption") - 1)
        font.setWeight(QFont.Medium)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        text_rect = QRectF(node.x - 40, node.y + r + 4, 80, 16)
        painter.drawText(text_rect, Qt.AlignCenter, node.name)

    def _draw_tooltip(self, painter: QPainter, node: RelationNode, tm: ThemeManager, connected: set):
        conn_count = len(connected)
        text = f"{node.name} ({conn_count} connections)"
        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(text) + 16
        th = 24
        tx = node.x - tw / 2
        ty = node.y - node.size / 2 - th - 10
        if ty < 0:
            ty = node.y + node.size / 2 + 10

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(tx, ty, tw, th), Qt.AlignCenter, text)

    def apply_theme(self):
        self.update()
