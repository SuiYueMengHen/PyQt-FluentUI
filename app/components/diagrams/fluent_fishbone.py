import math

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPainterPath

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FishBoneCategory:
    def __init__(self, name: str, causes: list[str] = None):
        self.name = name
        self.causes = causes or []
        self.bone_start_x = 0.0
        self.bone_start_y = 0.0
        self.bone_end_x = 0.0
        self.bone_end_y = 0.0


class FluentFishbone(QWidget, FluentWidgetBase):
    _anim_progress = 0.0
    category_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(320)
        self._effect: str = ""
        self._categories: list[FishBoneCategory] = []
        self._anim = None
        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(200)
        self._resize_timer.timeout.connect(self.update)
        self._hovered_cat = -1
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

    def set_data(self, effect: str, categories: list[dict]):
        self._effect = effect
        self._categories = []
        for cat in categories:
            self._categories.append(FishBoneCategory(
                name=cat.get("name", ""),
                causes=cat.get("causes", []),
            ))
        self.update()

    def _compute_bone_geometry(self):
        w = self.width()
        h = self.height()
        spine_y = h / 2
        spine_start_x = 60
        spine_end_x = w - 40
        n = len(self._categories)
        if n == 0:
            return
        segment_len = (spine_end_x - spine_start_x - 80) / n
        for i, cat in enumerate(self._categories):
            cat_x = spine_start_x + 40 + i * segment_len + segment_len / 2
            is_top = (i % 2 == 0)
            bone_angle = math.radians(60)
            bone_len = min(h * 0.35, 140)
            cat.bone_start_x = cat_x
            cat.bone_start_y = spine_y
            if is_top:
                cat.bone_end_x = cat_x - bone_len * math.cos(bone_angle)
                cat.bone_end_y = spine_y - bone_len * math.sin(bone_angle)
            else:
                cat.bone_end_x = cat_x - bone_len * math.cos(bone_angle)
                cat.bone_end_y = spine_y + bone_len * math.sin(bone_angle)

    def _cat_at(self, pos):
        for i, cat in enumerate(self._categories):
            cx = (cat.bone_start_x + cat.bone_end_x) / 2
            cy = (cat.bone_start_y + cat.bone_end_y) / 2
            dx = abs(pos.x() - cx)
            dy = abs(pos.y() - cy)
            if dx < 50 and dy < 50:
                return i
        return -1

    def mouseMoveEvent(self, event):
        self._compute_bone_geometry()
        self._hovered_cat = self._cat_at(event.position())
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._hovered_cat = -1
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            idx = self._cat_at(event.position())
            if idx >= 0:
                self.category_clicked.emit(self._categories[idx].name)
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_timer.start()

    def paintEvent(self, event):
        if not self._effect or not self._categories:
            return
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        painter.setOpacity(self._anim_progress)

        w = self.width()
        h = self.height()
        spine_y = h / 2
        spine_start_x = 60
        spine_end_x = w - 40

        spine_pen = QPen(QColor(tm.color("fg_primary")), 3, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(spine_pen)
        painter.drawLine(int(spine_start_x), int(spine_y), int(spine_end_x), int(spine_y))

        arrow_size = 10
        painter.setBrush(QColor(tm.color("fg_primary")))
        painter.setPen(Qt.NoPen)
        arrow_path = QPainterPath()
        arrow_path.moveTo(spine_end_x, spine_y)
        arrow_path.lineTo(spine_end_x - arrow_size, spine_y - arrow_size / 2)
        arrow_path.lineTo(spine_end_x - arrow_size, spine_y + arrow_size / 2)
        arrow_path.closeSubpath()
        painter.drawPath(arrow_path)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)
        painter.setPen(QColor(tm.color("primary")))
        effect_rect = QRectF(spine_end_x - 120, spine_y - 30, 110, 24)
        painter.drawText(effect_rect, Qt.AlignRight | Qt.AlignVCenter, self._effect)

        n = len(self._categories)
        if n == 0:
            painter.end()
            return

        cat_colors = [
            "primary", "accent_success", "accent_warning", "accent_error", "accent_info",
            "primary", "accent_success", "accent_warning",
        ]

        segment_len = (spine_end_x - spine_start_x - 80) / n
        self._compute_bone_geometry()

        for i, cat in enumerate(self._categories):
            color_key = cat_colors[i % len(cat_colors)]
            cat_color = QColor(tm.color(color_key))
            is_hovered = (i == self._hovered_cat)

            cat_x = cat.bone_start_x
            bone_end_x = cat.bone_end_x
            bone_end_y = cat.bone_end_y
            is_top = (i % 2 == 0)

            bone_width = 3.0 if is_hovered else 2
            bone_pen = QPen(cat_color, bone_width, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(bone_pen)
            painter.drawLine(int(cat_x), int(spine_y), int(bone_end_x), int(bone_end_y))

            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.DemiBold if is_hovered else QFont.DemiBold)
            painter.setFont(font)
            painter.setPen(cat_color if not is_hovered else cat_color.lighter(120))

            if is_top:
                cat_rect = QRectF(bone_end_x - 60, bone_end_y - 22, 70, 20)
                painter.drawText(cat_rect, Qt.AlignCenter, cat.name)
            else:
                cat_rect = QRectF(bone_end_x - 60, bone_end_y + 4, 70, 20)
                painter.drawText(cat_rect, Qt.AlignCenter, cat.name)

            cause_pen = QPen(QColor(tm.color("fg_tertiary")), 1, Qt.SolidLine, Qt.RoundCap)
            painter.setPen(cause_pen)

            for j, cause in enumerate(cat.causes):
                t = (j + 1) / (len(cat.causes) + 1)
                cause_x = cat_x + (bone_end_x - cat_x) * t
                cause_y = spine_y + (bone_end_y - spine_y) * t

                if is_top:
                    cause_end_y = cause_y - 16
                else:
                    cause_end_y = cause_y + 16

                painter.drawLine(int(cause_x), int(cause_y), int(cause_x), int(cause_end_y))

                font.setPixelSize(tm.font_size("caption") - 2)
                font.setWeight(QFont.Normal)
                painter.setFont(font)
                painter.setPen(QColor(tm.color("fg_secondary")))

                if is_top:
                    cause_rect = QRectF(cause_x - 40, cause_end_y - 16, 80, 16)
                else:
                    cause_rect = QRectF(cause_x - 40, cause_end_y + 2, 80, 16)
                painter.drawText(cause_rect, Qt.AlignCenter, cause)

        if self._hovered_cat >= 0:
            cat = self._categories[self._hovered_cat]
            text = f"{cat.name}: {', '.join(cat.causes)}"
            font.setPixelSize(tm.font_size("caption"))
            painter.setFont(font)
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(text) + 16
            th = 24
            tx = (cat.bone_start_x + cat.bone_end_x) / 2 - tw / 2
            ty = min(cat.bone_start_y, cat.bone_end_y) - th - 8
            if ty < 0:
                ty = max(cat.bone_start_y, cat.bone_end_y) + 8

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
