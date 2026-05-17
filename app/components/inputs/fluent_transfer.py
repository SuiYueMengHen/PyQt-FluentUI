from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.icons.icon_provider import get_icon
from app.theme.theme_manager import ThemeManager


class FluentTransfer(QWidget, FluentWidgetBase):
    transfer_changed = Signal(list)
    _anim_progress = 0.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._source: list[dict] = []
        self._target: list[dict] = []
        self._source_checked: set = set()
        self._target_checked: set = set()
        self._hovered_side = ""
        self._hovered_item = ""
        self.setFixedSize(480, 240)

    def set_data(self, source: list[dict], target: list[dict] = None):
        self._source = source
        self._target = target or []
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.position()
            panel_w = 180
            btn_area_x = panel_w
            btn_area_w = self.width() - 2 * panel_w

            if btn_area_x <= pos.x() <= btn_area_x + btn_area_w:
                btn_h = 28
                btn_y1 = self.height() / 2 - btn_h - 8
                btn_y2 = self.height() / 2 + 8
                if btn_y1 <= pos.y() <= btn_y1 + btn_h:
                    self._move_to_target()
                elif btn_y2 <= pos.y() <= btn_y2 + btn_h:
                    self._move_to_source()
            else:
                item = self._item_at(pos)
                if item:
                    side, key = item
                    if side == "source":
                        if key in self._source_checked:
                            self._source_checked.discard(key)
                        else:
                            self._source_checked.add(key)
                    else:
                        if key in self._target_checked:
                            self._target_checked.discard(key)
                        else:
                            self._target_checked.add(key)
            self.update()
        super().mousePressEvent(event)

    def _move_to_target(self):
        moved = [i for i in self._source if i.get("key", i.get("text", "")) in self._source_checked]
        self._source = [i for i in self._source if i.get("key", i.get("text", "")) not in self._source_checked]
        self._target.extend(moved)
        self._source_checked.clear()
        self.transfer_changed.emit([i.get("key", i.get("text", "")) for i in self._target])

    def _move_to_source(self):
        moved = [i for i in self._target if i.get("key", i.get("text", "")) in self._target_checked]
        self._target = [i for i in self._target if i.get("key", i.get("text", "")) not in self._target_checked]
        self._source.extend(moved)
        self._target_checked.clear()
        self.transfer_changed.emit([i.get("key", i.get("text", "")) for i in self._target])

    def _item_at(self, pos):
        panel_w = 180
        header_h = 32
        row_h = 28
        if pos.x() < panel_w:
            idx = int((pos.y() - header_h) / row_h)
            if 0 <= idx < len(self._source):
                key = self._source[idx].get("key", self._source[idx].get("text", ""))
                return ("source", key)
        elif pos.x() > self.width() - panel_w:
            idx = int((pos.y() - header_h) / row_h)
            if 0 <= idx < len(self._target):
                key = self._target[idx].get("key", self._target[idx].get("text", ""))
                return ("target", key)
        return None

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        panel_w = 180
        header_h = 32
        row_h = 28

        for side, items, checked, x in [
            ("source", self._source, self._source_checked, 0),
            ("target", self._target, self._target_checked, self.width() - panel_w),
        ]:
            painter.setPen(QPen(QColor(tm.color("stroke_card")), 1))
            painter.setBrush(QColor(tm.color("bg_solid_card")))
            painter.drawRoundedRect(QRectF(x, 0, panel_w, self.height()), 6, 6)

            font = QFont()
            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.DemiBold)
            painter.setFont(font)
            painter.setPen(QColor(tm.color("fg_secondary")))
            title = "源列表" if side == "source" else "目标列表"
            painter.drawText(QRectF(x + 10, 6, panel_w - 20, header_h - 6), Qt.AlignVCenter, f"{title} ({len(items)})")

            font.setPixelSize(tm.font_size("caption"))
            font.setWeight(QFont.Normal)
            painter.setFont(font)
            for i, item in enumerate(items):
                y = header_h + i * row_h
                if y + row_h > self.height():
                    break
                key = item.get("key", item.get("text", ""))
                is_checked = key in checked

                if is_checked:
                    painter.setPen(Qt.NoPen)
                    sel_bg = QColor(tm.color("primary_light"))
                    sel_bg.setAlpha(60)
                    painter.setBrush(QBrush(sel_bg))
                    painter.drawRoundedRect(QRectF(x + 4, y + 2, panel_w - 8, row_h - 4), 3, 3)

                check_size = 14
                check_x = x + 10
                check_y = y + (row_h - check_size) / 2
                painter.setPen(QPen(QColor(tm.color("primary")) if is_checked else QColor(tm.color("stroke_card")), 1.5))
                painter.setBrush(QBrush(QColor(tm.color("primary"))) if is_checked else Qt.NoBrush)
                painter.drawRoundedRect(QRectF(check_x, check_y, check_size, check_size), 2, 2)

                if is_checked:
                    check_icon = get_icon("check", tm.color("primary_text_on"), 10)
                    painter.drawPixmap(int(check_x + 2), int(check_y + 2), check_icon.pixmap(10, 10))

                painter.setPen(QColor(tm.color("fg_primary")))
                painter.drawText(QRectF(x + 30, y, panel_w - 40, row_h), Qt.AlignVCenter, item.get("text", ""))

        btn_area_x = panel_w
        btn_area_w = self.width() - 2 * panel_w
        btn_h = 28
        btn_w = min(btn_area_w - 16, 80)
        btn_x = btn_area_x + (btn_area_w - btn_w) / 2

        for i, (label, enabled) in enumerate([("→", bool(self._source_checked)), ("←", bool(self._target_checked))]):
            y = self.height() / 2 - btn_h - 8 + i * (btn_h + 8)
            bg = QColor(tm.color("primary")) if enabled else QColor(tm.color("bg_solid_tertiary"))
            fg = QColor(tm.color("primary_text_on")) if enabled else QColor(tm.color("fg_disabled"))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(bg))
            painter.drawRoundedRect(QRectF(btn_x, y, btn_w, btn_h), 4, 4)
            font = QFont()
            font.setPixelSize(tm.font_size("body"))
            painter.setFont(font)
            painter.setPen(fg)
            painter.drawText(QRectF(btn_x, y, btn_w, btn_h), Qt.AlignCenter, label)

        painter.end()

    def apply_theme(self):
        self.update()
