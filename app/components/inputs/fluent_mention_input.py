from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from app.components.base.fluent_widget import FluentWidgetBase
from app.theme.theme_manager import ThemeManager


class FluentMentionInput(QWidget, FluentWidgetBase):
    mention_selected = Signal(str)
    _drop_progress = 0.0

    def __init__(self, placeholder: str = "输入 @ 提及...", parent=None):
        super().__init__(parent)
        self._init_fluent_base()
        self._placeholder = placeholder
        self._text = ""
        self._mentions: list[str] = []
        self._users: list[dict] = []
        self._show_list = False
        self._hovered_user = -1
        self.setFixedSize(280, 80)
        self.setCursor(Qt.IBeamCursor)

        self._drop_anim = QPropertyAnimation(self, b"drop_progress")
        self._drop_anim.setDuration(150)
        self._drop_anim.setEasingCurve(QEasingCurve.OutCubic)

    def set_users(self, users: list[dict]):
        self._users = users

    @Property(float)
    def drop_progress(self):
        return self._drop_progress

    @drop_progress.setter
    def drop_progress(self, v):
        self._drop_progress = v
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace and self._text:
            self._text = self._text[:-1]
            self._check_mention()
        elif event.key() == Qt.Key_Down and self._show_list:
            self._hovered_user = min(self._hovered_user + 1, len(self._users) - 1)
            self.update()
        elif event.key() == Qt.Key_Up and self._show_list:
            self._hovered_user = max(self._hovered_user - 1, 0)
            self.update()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter) and self._show_list and 0 <= self._hovered_user < len(self._users):
            user = self._users[self._hovered_user]
            at_pos = self._text.rfind("@")
            if at_pos >= 0:
                self._text = self._text[:at_pos] + f"@{user.get('name', '')} "
                self.mention_selected.emit(user.get("name", ""))
            self._show_list = False
            self.update()
        elif event.text() and event.text().isprintable():
            self._text += event.text()
            self._check_mention()
        else:
            super().keyPressEvent(event)

    def _check_mention(self):
        if "@" in self._text:
            at_pos = self._text.rfind("@")
            query = self._text[at_pos + 1:]
            self._show_list = bool(query)
            self._hovered_user = 0
        else:
            self._show_list = False
        self.update()

    def paintEvent(self, event):
        tm = self._tm
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(tm.color('bg_solid_card')))
        border_color = QColor(tm.color("primary")) if self.hasFocus() else QColor(tm.color("stroke_card"))
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QColor(tm.color("bg_solid_card")))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 6, 6)

        font = QFont()
        font.setPixelSize(tm.font_size("body"))
        painter.setFont(font)

        if self._text:
            x = 10
            words = self._text.split(" ")
            for word in words:
                if word.startswith("@"):
                    painter.setPen(QColor(tm.color("primary")))
                    painter.drawText(int(x), int(self.height() / 2 + 4), word)
                    x += painter.fontMetrics().horizontalAdvance(word) + painter.fontMetrics().horizontalAdvance(" ")
                else:
                    painter.setPen(QColor(tm.color("fg_primary")))
                    painter.drawText(int(x), int(self.height() / 2 + 4), word)
                    x += painter.fontMetrics().horizontalAdvance(word) + painter.fontMetrics().horizontalAdvance(" ")

            if self.hasFocus():
                cursor_x = 10 + painter.fontMetrics().horizontalAdvance(self._text)
                painter.setPen(QColor(tm.color("primary")))
                painter.drawLine(int(cursor_x), 10, int(cursor_x), int(self.height() - 10))
        else:
            painter.setPen(QColor(tm.color("fg_tertiary")))
            painter.drawText(QRectF(10, 0, self.width() - 20, self.height()), Qt.AlignVCenter, self._placeholder)

        painter.end()

    def apply_theme(self):
        self.update()
