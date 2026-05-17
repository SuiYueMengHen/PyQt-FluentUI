from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class OrgNode:
    def __init__(self, name: str, title: str = "", avatar: str = "", children: list = None):
        self.name = name
        self.title = title
        self.avatar = avatar
        self.children = children or []
        self.x = 0.0
        self.y = 0.0
        self.width = 140.0
        self.height = 60.0


_LEVEL_COLORS = [
    "primary",
    "accent_success",
    "accent_warning",
    "accent_error",
    "accent_info",
]


class FluentOrgChart(QWidget, FluentWidgetBase):
    _anim_progress = 0.0
    node_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(320)
        self._root: OrgNode = OrgNode("")
        self._h_gap = 30
        self._v_gap = 70
        self._padding = 30
        self._anim = None
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(200)
        self._resize_timer.timeout.connect(self._do_layout)
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
        self._root = self._build_node(data)
        self._do_layout()
        self.update()

    def _build_node(self, data: dict) -> OrgNode:
        node = OrgNode(
            name=data.get("name", ""),
            title=data.get("title", ""),
            avatar=data.get("avatar", ""),
        )
        for child_data in data.get("children", []):
            node.children.append(self._build_node(child_data))
        return node

    def _subtree_width(self, node: OrgNode) -> float:
        if not node.children:
            return node.width
        total = sum(self._subtree_width(c) for c in node.children)
        total += (len(node.children) - 1) * self._h_gap
        return max(total, node.width)

    def _do_layout(self):
        if not self._root.name:
            return
        w = self.width()
        if w < 50:
            return
        self._root.x = (w - self._root.width) / 2
        self._root.y = self._padding
        if self._root.children:
            self._layout_children(self._root, self._root.y + self._root.height + self._v_gap)
        self.update()

    def _layout_children(self, parent: OrgNode, y: float):
        total_w = self._subtree_width(parent)
        cx = parent.x + parent.width / 2
        start_x = cx - total_w / 2

        current_x = start_x
        for child in parent.children:
            child_w = self._subtree_width(child)
            child.x = current_x + (child_w - child.width) / 2
            child.y = y
            if child.children:
                self._layout_children(child, y + child.height + self._v_gap)
            current_x += child_w + self._h_gap

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
        self._hovered_node = self._node_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_node = None
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            node = self._node_at(event.position())
            if node:
                self.node_clicked.emit(node.name)
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_timer.start()

    def paintEvent(self, event):
        if not self._root.name:
            return
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setOpacity(self._anim_progress)

        self._draw_connections(painter, self._root, tm, 0)
        self._draw_node(painter, self._root, tm, 0)
        self._draw_subtree(painter, self._root, tm, 0)

        if self._hovered_node:
            self._draw_tooltip(painter, self._hovered_node, tm)

        painter.end()

    def _draw_subtree(self, painter: QPainter, node: OrgNode, tm: ThemeManager, depth: int):
        for child in node.children:
            self._draw_connections(painter, child, tm, depth + 1)
            self._draw_node(painter, child, tm, depth + 1)
            self._draw_subtree(painter, child, tm, depth + 1)

    def _draw_node(self, painter: QPainter, node: OrgNode, tm: ThemeManager, depth: int):
        is_hovered = (node == self._hovered_node)
        rect = QRectF(node.x, node.y, node.width, node.height)
        color_key = _LEVEL_COLORS[depth % len(_LEVEL_COLORS)]
        accent = QColor(tm.color(color_key))

        if is_hovered:
            shadow = QColor(accent)
            shadow.setAlpha(25)
            painter.setPen(Qt.NoPen)
            painter.setBrush(shadow)
            painter.drawRoundedRect(QRectF(node.x - 3, node.y - 3, node.width + 6, node.height + 6), 10, 10)

        painter.setPen(QPen(accent, 2.0 if is_hovered else 1.5))
        bg = QColor(tm.color("bg_solid_card"))
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 8, 8)

        top_bar = QRectF(node.x, node.y, node.width, 4)
        painter.setPen(Qt.NoPen)
        painter.setBrush(accent)
        painter.drawRoundedRect(top_bar, 2, 2)

        font = QFont()
        font.setPixelSize(tm.font_size("caption"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("fg_primary")))
        name_rect = QRectF(node.x + 8, node.y + 8, node.width - 16, 20)
        painter.drawText(name_rect, Qt.AlignCenter, node.name)

        if node.title:
            font.setPixelSize(tm.font_size("caption") - 2)
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            title_rect = QRectF(node.x + 8, node.y + 30, node.width - 16, 18)
            painter.drawText(title_rect, Qt.AlignCenter, node.title)

    def _draw_connections(self, painter: QPainter, node: OrgNode, tm: ThemeManager, depth: int):
        if not node.children:
            return
        is_hovered = (node == self._hovered_node)
        pen_color = QColor(tm.color("stroke_card"))
        if is_hovered:
            pen_color = QColor(tm.color("primary"))
        painter.setPen(QPen(pen_color, 2.0 if is_hovered else 1.5))
        painter.setBrush(Qt.NoBrush)

        parent_cx = node.x + node.width / 2
        parent_bottom = node.y + node.height

        mid_y = parent_bottom + self._v_gap / 2

        path = QPainterPath()
        path.moveTo(parent_cx, parent_bottom)
        path.lineTo(parent_cx, mid_y)

        if len(node.children) > 1:
            left_x = node.children[0].x + node.children[0].width / 2
            right_x = node.children[-1].x + node.children[-1].width / 2
            path.moveTo(left_x, mid_y)
            path.lineTo(right_x, mid_y)

        painter.drawPath(path)

        for child in node.children:
            child_cx = child.x + child.width / 2
            child_path = QPainterPath()
            child_path.moveTo(child_cx, mid_y)
            child_path.lineTo(child_cx, child.y)
            painter.drawPath(child_path)

    def _draw_tooltip(self, painter: QPainter, node: OrgNode, tm: ThemeManager):
        text = f"{node.name}" + (f" - {node.title}" if node.title else "")
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
