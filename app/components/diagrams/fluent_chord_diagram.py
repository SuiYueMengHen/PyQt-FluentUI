import math

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class ChordNode:
    def __init__(self, name: str, value: float = 1.0, color_key: str = "primary"):
        self.name = name
        self.value = value
        self.color_key = color_key
        self.start_angle = 0.0
        self.span_angle = 0.0


class ChordLink:
    def __init__(self, src: int, dst: int, value: float = 1.0):
        self.src = src
        self.dst = dst
        self.value = value


_NODE_COLORS = [
    "primary", "accent_success", "accent_warning", "accent_error", "accent_info",
]


class FluentChordDiagram(QWidget, FluentWidgetBase):
    _anim_progress = 0.0
    node_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(300)
        self._nodes: list[ChordNode] = []
        self._links: list[ChordLink] = []
        self._anim = None
        self._hovered_node_idx = -1
        self.setMouseTracking(True)
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(200)
        self._resize_timer.timeout.connect(self.update)
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

    def add_node(self, name: str, value: float = 1.0, color_key: str = "") -> int:
        idx = len(self._nodes)
        if not color_key:
            color_key = _NODE_COLORS[idx % len(_NODE_COLORS)]
        self._nodes.append(ChordNode(name, value, color_key))
        return idx

    def add_link(self, src: int, dst: int, value: float = 1.0):
        self._links.append(ChordLink(src, dst, value))

    def _compute_layout(self):
        if not self._nodes:
            return
        total = sum(n.value for n in self._nodes)
        if total == 0:
            return
        gap = 0.03
        total_gap = gap * len(self._nodes)
        available = 2 * math.pi - total_gap

        current_angle = 0
        for node in self._nodes:
            node.span_angle = (node.value / total) * available
            node.start_angle = current_angle
            current_angle += node.span_angle + gap

    def _node_at_angle(self, angle):
        for i, node in enumerate(self._nodes):
            end = node.start_angle + node.span_angle
            if node.start_angle <= angle <= end:
                return i
        return -1

    def _pos_to_angle(self, pos):
        cx = self.width() / 2
        cy = self.height() / 2
        dx = pos.x() - cx
        dy = pos.y() - cy
        return math.atan2(dy, dx)

    def _pos_to_radius(self, pos):
        cx = self.width() / 2
        cy = self.height() / 2
        dx = pos.x() - cx
        dy = pos.y() - cy
        return math.sqrt(dx * dx + dy * dy)

    def mouseMoveEvent(self, event):
        pos = event.position()
        angle = self._pos_to_angle(pos)
        radius = self._pos_to_radius(pos)
        size = min(self.width(), self.height())
        outer_r = size / 2 - 30
        inner_r = outer_r - 20

        if inner_r <= radius <= outer_r + 10:
            self._hovered_node_idx = self._node_at_angle(angle)
        else:
            self._hovered_node_idx = -1
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_node_idx = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._hovered_node_idx >= 0:
            self.node_clicked.emit(self._nodes[self._hovered_node_idx].name)
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_timer.start()

    def paintEvent(self, event):
        if not self._nodes:
            return
        self._compute_layout()
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setOpacity(self._anim_progress)

        cx = self.width() / 2
        cy = self.height() / 2
        size = min(self.width(), self.height())
        outer_r = size / 2 - 30
        inner_r = outer_r - 20
        chord_r = inner_r - 5

        connected_nodes = set()
        if self._hovered_node_idx >= 0:
            for link in self._links:
                if link.src == self._hovered_node_idx:
                    connected_nodes.add(link.dst)
                elif link.dst == self._hovered_node_idx:
                    connected_nodes.add(link.src)

        for link in self._links:
            if link.src >= len(self._nodes) or link.dst >= len(self._nodes):
                continue
            src = self._nodes[link.src]
            dst = self._nodes[link.dst]

            is_highlighted = (self._hovered_node_idx >= 0 and
                            (link.src == self._hovered_node_idx or link.dst == self._hovered_node_idx))

            src_mid = src.start_angle + src.span_angle / 2
            dst_mid = dst.start_angle + dst.span_angle / 2

            sx = cx + chord_r * math.cos(src_mid)
            sy = cy + chord_r * math.sin(src_mid)
            ex = cx + chord_r * math.cos(dst_mid)
            ey = cy + chord_r * math.sin(dst_mid)

            src_color = QColor(tm.color(src.color_key))
            dst_color = QColor(tm.color(dst.color_key))

            if is_highlighted:
                src_color.setAlpha(140)
                dst_color.setAlpha(140)
            else:
                src_color.setAlpha(40 if self._hovered_node_idx >= 0 else 60)
                dst_color.setAlpha(40 if self._hovered_node_idx >= 0 else 60)

            path = QPainterPath()
            path.moveTo(sx, sy)
            ctrl_x = cx
            ctrl_y = cy
            path.cubicTo(ctrl_x, ctrl_y, ctrl_x, ctrl_y, ex, ey)

            pen_width = max(1, link.value * 2) if is_highlighted else max(0.5, link.value)
            painter.setPen(QPen(src_color, pen_width))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)

        for i, node in enumerate(self._nodes):
            is_hovered = (i == self._hovered_node_idx)
            is_connected = (i in connected_nodes)
            color = QColor(tm.color(node.color_key))

            if is_hovered:
                color = color.lighter(120)
            elif self._hovered_node_idx >= 0 and not is_connected:
                color.setAlpha(80)

            rect = QRectF(cx - outer_r, cy - outer_r, outer_r * 2, outer_r * 2)
            start_deg = -math.degrees(node.start_angle) * 16
            span_deg = -math.degrees(node.span_angle) * 16

            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawArc(rect, int(start_deg), int(span_deg))

            inner_rect = QRectF(cx - inner_r, cy - inner_r, inner_r * 2, inner_r * 2)
            bg_color = QColor(tm.color("bg_solid_base"))
            painter.setBrush(bg_color)
            painter.drawArc(inner_rect, int(start_deg), int(span_deg))

            mid_angle = node.start_angle + node.span_angle / 2
            label_r = outer_r + 16
            lx = cx + label_r * math.cos(mid_angle)
            ly = cy + label_r * math.sin(mid_angle)

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Medium if is_hovered or is_connected else QFont.Normal)
            painter.setFont(font)
            text_color = QColor(tm.color("fg_primary"))
            if self._hovered_node_idx >= 0 and not is_hovered and not is_connected:
                text_color.setAlpha(80)
            painter.setPen(text_color)

            text_rect = QRectF(lx - 50, ly - 10, 100, 20)
            alignment = Qt.AlignLeft | Qt.AlignVCenter
            if math.cos(mid_angle) < -0.3:
                alignment = Qt.AlignRight | Qt.AlignVCenter
            elif abs(math.cos(mid_angle)) <= 0.3:
                alignment = Qt.AlignCenter
            painter.drawText(text_rect, alignment, node.name)

        if self._hovered_node_idx >= 0:
            node = self._nodes[self._hovered_node_idx]
            conn_count = len(connected_nodes)
            text = f"{node.name} ({conn_count} links)"
            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(text) + 16
            th = 24
            tx = cx - tw / 2
            ty = cy - th / 2

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
