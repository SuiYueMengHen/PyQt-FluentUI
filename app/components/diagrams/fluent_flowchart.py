import math
from collections import deque

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, QPointF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath, QPolygonF

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FlowNode:
    def __init__(self, text: str, shape: str = "rect", x: float = 0, y: float = 0):
        self.text = text
        self.shape = shape
        self.x = x
        self.y = y
        self.width = 120.0
        self.height = 44.0


class FlowEdge:
    def __init__(self, src: int, dst: int, label: str = ""):
        self.src = src
        self.dst = dst
        self.label = label


_SHAPE_COLORS = {
    "rect": ("bg_solid_card", "stroke_card"),
    "diamond": ("accent_warning_light", "accent_warning"),
    "rounded": ("primary_light", "primary"),
    "stadium": ("accent_success_light", "accent_success"),
    "parallelogram": ("accent_info_light", "accent_info"),
}


class FluentFlowchart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0
    node_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._nodes: list[FlowNode] = []
        self._edges: list[FlowEdge] = []
        self._layout_done = False
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(350)
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

    def add_node(self, text: str, shape: str = "rect") -> int:
        node = FlowNode(text, shape)
        self._nodes.append(node)
        return len(self._nodes) - 1

    def add_edge(self, src: int, dst: int, label: str = ""):
        self._edges.append(FlowEdge(src, dst, label))

    def auto_layout(self):
        self._layout_done = False
        self._resize_timer.start()

    def _do_layout(self):
        if not self._nodes:
            return
        w = self.width()
        if w < 50:
            self._layout_done = False
            return

        levels = self._compute_levels()
        level_nodes: dict[int, list[int]] = {}
        for idx, lvl in levels.items():
            level_nodes.setdefault(lvl, []).append(idx)

        max_lvl = max(levels.values()) if levels else 0
        v_gap = 80
        h_gap = 160
        top_margin = 30

        for lvl in range(max_lvl + 1):
            nodes_in_lvl = level_nodes.get(lvl, [])
            total_width = len(nodes_in_lvl) * h_gap
            start_x = (w - total_width) / 2 + h_gap / 2 - 60
            for i, idx in enumerate(nodes_in_lvl):
                self._nodes[idx].x = start_x + i * h_gap
                self._nodes[idx].y = top_margin + lvl * v_gap
        self._layout_done = True
        self.update()

    def _compute_levels(self) -> dict[int, int]:
        levels = {}
        in_degree = {i: 0 for i in range(len(self._nodes))}
        adj: dict[int, list[int]] = {i: [] for i in range(len(self._nodes))}
        for edge in self._edges:
            adj[edge.src].append(edge.dst)
            in_degree[edge.dst] += 1

        queue = deque(i for i in range(len(self._nodes)) if in_degree[i] == 0)
        for node_idx in queue:
            levels[node_idx] = 0

        while queue:
            current = queue.popleft()
            for neighbor in adj[current]:
                in_degree[neighbor] -= 1
                new_level = levels[current] + 1
                if neighbor not in levels or levels[neighbor] < new_level:
                    levels[neighbor] = new_level
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        for i in range(len(self._nodes)):
            if i not in levels:
                levels[i] = 0
        return levels

    def _node_at(self, pos):
        for i, node in enumerate(self._nodes):
            rect = QRectF(node.x, node.y, node.width, node.height)
            if node.shape == "diamond":
                cx = node.x + node.width / 2
                cy = node.y + node.height / 2
                dx = abs(pos.x() - cx) / (node.width / 2)
                dy = abs(pos.y() - cy) / (node.height / 2)
                if dx + dy <= 1.0:
                    return i
            elif rect.contains(pos):
                return i
        return -1

    def _connected_edges(self, node_idx):
        result = []
        for edge in self._edges:
            if edge.src == node_idx or edge.dst == node_idx:
                result.append(edge)
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
                self.node_clicked.emit(self._nodes[idx].text)
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._nodes:
            self._resize_timer.start()

    def paintEvent(self, event):
        if not self._nodes:
            return
        if not self._layout_done:
            self._do_layout()
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setOpacity(self._anim_progress)

        hovered_edges = set()
        if self._hovered_node_idx >= 0:
            for i, edge in enumerate(self._edges):
                if edge.src == self._hovered_node_idx or edge.dst == self._hovered_node_idx:
                    hovered_edges.add(i)

        for i, edge in enumerate(self._edges):
            self._draw_edge(painter, edge, tm, i in hovered_edges)

        for i, node in enumerate(self._nodes):
            self._draw_node(painter, node, tm, i == self._hovered_node_idx)

        if self._hovered_node_idx >= 0:
            self._draw_tooltip(painter, self._nodes[self._hovered_node_idx], tm)

        painter.end()

    def _draw_node(self, painter: QPainter, node: FlowNode, tm: ThemeManager, is_hovered: bool = False):
        bg_key, stroke_key = _SHAPE_COLORS.get(node.shape, _SHAPE_COLORS["rect"])
        bg_color = QColor(tm.color(bg_key))
        stroke_color = QColor(tm.color(stroke_key))

        pen_width = 2.0 if is_hovered else 1.5
        painter.setPen(QPen(stroke_color, pen_width))
        painter.setBrush(bg_color)

        if is_hovered:
            shadow = QColor(stroke_color)
            shadow.setAlpha(30)
            painter.setBrush(shadow)
            rect = QRectF(node.x - 3, node.y - 3, node.width + 6, node.height + 6)
            painter.drawRoundedRect(rect, 8, 8)
            painter.setBrush(bg_color)

        rect = QRectF(node.x, node.y, node.width, node.height)

        if node.shape == "diamond":
            cx = node.x + node.width / 2
            cy = node.y + node.height / 2
            hw = node.width / 2
            hh = node.height / 2
            polygon = QPolygonF([
                QPointF(cx, cy - hh),
                QPointF(cx + hw, cy),
                QPointF(cx, cy + hh),
                QPointF(cx - hw, cy),
            ])
            painter.drawPolygon(polygon)
        elif node.shape == "rounded":
            painter.drawRoundedRect(rect, 12, 12)
        elif node.shape == "stadium":
            painter.drawRoundedRect(rect, node.height / 2, node.height / 2)
        elif node.shape == "parallelogram":
            skew = 15
            polygon = QPolygonF([
                QPointF(node.x + skew, node.y),
                QPointF(node.x + node.width, node.y),
                QPointF(node.x + node.width - skew, node.y + node.height),
                QPointF(node.x, node.y + node.height),
            ])
            painter.drawPolygon(polygon)
        else:
            painter.drawRoundedRect(rect, 4, 4)

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.Medium)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))

        if node.shape == "diamond":
            cx = node.x + node.width / 2
            cy = node.y + node.height / 2
            painter.drawText(QRectF(cx - node.width / 3, cy - 10, node.width * 2 / 3, 20), Qt.AlignCenter, node.text)
        elif node.shape == "parallelogram":
            painter.drawText(QRectF(node.x + 15, node.y, node.width - 30, node.height), Qt.AlignCenter, node.text)
        else:
            painter.drawText(rect, Qt.AlignCenter, node.text)

    def _draw_edge(self, painter: QPainter, edge: FlowEdge, tm: ThemeManager, is_hovered: bool = False):
        if edge.src >= len(self._nodes) or edge.dst >= len(self._nodes):
            return
        src = self._nodes[edge.src]
        dst = self._nodes[edge.dst]

        start_x = src.x + src.width / 2
        start_y = src.y + src.height
        end_x = dst.x + dst.width / 2
        end_y = dst.y

        pen_color = QColor(tm.color("fg_tertiary"))
        if is_hovered:
            pen_color = QColor(tm.color("primary"))
        width = 2.0 if is_hovered else 1.5
        painter.setPen(QPen(pen_color, width, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)

        path = QPainterPath()
        path.moveTo(start_x, start_y)
        mid_y = (start_y + end_y) / 2
        path.cubicTo(start_x, mid_y, end_x, mid_y, end_x, end_y)
        painter.drawPath(path)

        arrow_size = 6
        dx = end_x - start_x
        dy = end_y - mid_y
        angle = math.atan2(dy, dx) if dx != 0 else math.pi / 2
        p1 = QPointF(end_x - arrow_size * math.cos(angle - math.pi / 6),
                      end_y - arrow_size * math.sin(angle - math.pi / 6))
        p2 = QPointF(end_x - arrow_size * math.cos(angle + math.pi / 6),
                      end_y - arrow_size * math.sin(angle + math.pi / 6))
        arrow = QPolygonF([QPointF(end_x, end_y), p1, p2])
        painter.setBrush(pen_color)
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(arrow)

        if edge.label:
            font = QFont()
            font.setPixelSize(tm.font_size("caption") - 2)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            label_x = (start_x + end_x) / 2 + 4
            label_y = mid_y - 4
            painter.drawText(QRectF(label_x - 30, label_y - 10, 60, 20), Qt.AlignCenter, edge.label)

    def _draw_tooltip(self, painter: QPainter, node: FlowNode, tm: ThemeManager):
        text = f"{node.text} ({node.shape})"
        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        painter.setFont(font)
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(text) + 16
        th = 24
        tx = node.x + node.width / 2 - tw / 2
        ty = node.y - th - 8
        if ty < 0:
            ty = node.y + node.height + 8

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
