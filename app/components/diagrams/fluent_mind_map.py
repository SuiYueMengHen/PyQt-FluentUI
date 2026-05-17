from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class MindMapNode:
    def __init__(self, text: str, children: list = None, color_key: str = ""):
        self.text = text
        self.children = children or []
        self.color_key = color_key
        self.x = 0.0
        self.y = 0.0
        self.width = 0.0
        self.height = 0.0


_BRANCH_COLORS = [
    "primary", "accent_success", "accent_warning", "accent_error", "accent_info",
]


class FluentMindMap(QWidget, FluentWidgetBase):
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._root: MindMapNode = MindMapNode("")
        self._node_height = 32
        self._h_gap = 60
        self._v_gap = 12
        self._padding = 40
        self._data_set = False
        self._layout_valid = False
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(300)
        self._anim = None
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(200)
        self._resize_timer.timeout.connect(self._do_layout_and_update)
        self._hovered_node = None
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

    def set_data(self, data: dict):
        self._root = self._build_node(data, 0)
        self._data_set = True
        self._layout_valid = False
        self._resize_timer.start()

    def _build_node(self, data: dict, depth: int) -> MindMapNode:
        color_key = _BRANCH_COLORS[depth % len(_BRANCH_COLORS)] if depth > 0 else ""
        node = MindMapNode(data.get("text", ""), color_key=color_key)
        for child_data in data.get("children", []):
            node.children.append(self._build_node(child_data, depth + 1))
        return node

    def _measure_node(self, node: MindMapNode) -> float:
        fm = self.fontMetrics()
        text_width = fm.horizontalAdvance(node.text) + 24
        node.width = max(text_width, 60)
        node.height = self._node_height
        return node.width

    def _subtree_height(self, node: MindMapNode) -> float:
        if not node.children:
            return node.height
        total = sum(self._subtree_height(c) for c in node.children)
        total += (len(node.children) - 1) * self._v_gap
        return max(total, node.height)

    def _do_layout(self):
        if not self._data_set or not self._root.text:
            return False
        w = self.width()
        h = self.height()
        if w < 50 or h < 50:
            return False
        self._measure_node(self._root)
        for child in self._root.children:
            self._measure_subtree(child)
        self._root.x = self._padding
        self._root.y = h / 2 - self._root.height / 2
        if self._root.children:
            self._layout_right(self._root, self._root.x + self._root.width + self._h_gap)
        self._layout_valid = True
        return True

    def _do_layout_and_update(self):
        if self._do_layout():
            self.update()

    def _measure_subtree(self, node: MindMapNode):
        self._measure_node(node)
        for child in node.children:
            self._measure_subtree(child)

    def _layout_right(self, parent: MindMapNode, start_x: float):
        total_h = self._subtree_height(parent)
        cy = parent.y + parent.height / 2
        current_y = cy - total_h / 2
        for child in parent.children:
            child_h = self._subtree_height(child)
            child.x = start_x
            child.y = current_y + (child_h - child.height) / 2
            if child.children:
                self._layout_right(child, start_x + child.width + self._h_gap)
            current_y += child_h + self._v_gap

    def _node_at(self, pos, node=None):
        if node is None:
            node = self._root
        rect = QRectF(node.x, node.y, node.width, node.height)
        if rect.contains(pos):
            return node
        for child in node.children:
            found = self._node_at(pos, child)
            if found:
                return found
        return None

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._hovered_node = self._node_at(pos)
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_node = None
        self.update()
        super().leaveEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._data_set:
            self._resize_timer.start()

    def paintEvent(self, event):
        if not self._data_set or not self._root.text:
            return
        if not self._layout_valid:
            if not self._do_layout():
                return
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        progress = self._anim_progress
        painter.setOpacity(progress)

        self._draw_node(painter, self._root, tm, is_root=True)
        self._draw_connections(painter, self._root, tm)
        for child in self._root.children:
            self._draw_subtree(painter, child, tm, 1)

        if self._hovered_node:
            self._draw_tooltip(painter, self._hovered_node, tm)

        painter.end()

    def _draw_subtree(self, painter: QPainter, node: MindMapNode, tm: ThemeManager, depth: int):
        self._draw_node(painter, node, tm, depth=depth)
        self._draw_connections(painter, node, tm)
        for child in node.children:
            self._draw_subtree(painter, child, tm, depth + 1)

    def _draw_node(self, painter: QPainter, node: MindMapNode, tm: ThemeManager, is_root: bool = False, depth: int = 0):
        rect = QRectF(node.x, node.y, node.width, node.height)
        is_hovered = (node == self._hovered_node)

        if is_root:
            painter.setPen(Qt.NoPen)
            bg = QColor(tm.color("primary"))
            if is_hovered:
                bg = bg.lighter(115)
            painter.setBrush(bg)
            painter.drawRoundedRect(rect, 8, 8)
            font = QFont()
            font.setPixelSize(tm.font_size("body"))
            font.setWeight(QFont.DemiBold)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("primary_text_on")))
        else:
            color_key = node.color_key or _BRANCH_COLORS[(depth - 1) % len(_BRANCH_COLORS)]
            base_color = QColor(tm.color(color_key))
            light_color = QColor(base_color)
            light_color.setAlpha(30 if not is_hovered else 60)
            pen_width = 1.5 if not is_hovered else 2.5
            painter.setPen(QPen(base_color, pen_width))
            painter.setBrush(light_color)
            painter.drawRoundedRect(rect, 6, 6)
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Medium)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_primary")))

        painter.drawText(rect, Qt.AlignCenter, node.text)

    def _draw_connections(self, painter: QPainter, node: MindMapNode, tm: ThemeManager):
        if not node.children:
            return
        for child in node.children:
            color_key = child.color_key or "primary"
            pen_color = QColor(tm.color(color_key))
            is_hovered = (child == self._hovered_node or node == self._hovered_node)
            pen_color.setAlpha(180 if is_hovered else 120)
            width = 2.5 if is_hovered else 2
            painter.setPen(QPen(pen_color, width, Qt.SolidLine, Qt.RoundCap))
            painter.setBrush(Qt.NoBrush)

            start_x = node.x + node.width
            start_y = node.y + node.height / 2
            end_x = child.x
            end_y = child.y + child.height / 2

            path = QPainterPath()
            path.moveTo(start_x, start_y)
            ctrl_x = (start_x + end_x) / 2
            path.cubicTo(ctrl_x, start_y, ctrl_x, end_y, end_x, end_y)
            painter.drawPath(path)

    def _draw_tooltip(self, painter: QPainter, node: MindMapNode, tm: ThemeManager):
        text = node.text
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
        bg = QColor(tm.color("bg_solid_card"))
        painter.setBrush(bg)
        painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)
        painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(tx, ty, tw, th), 4, 4)

        painter.setPen(QColor(tm.color("fg_primary")))
        painter.drawText(QRectF(tx, ty, tw, th), Qt.AlignCenter, text)

    def apply_theme(self):
        self.update()
