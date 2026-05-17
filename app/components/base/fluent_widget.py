from PySide6.QtCore import QTimer
from app.theme.theme_manager import ThemeManager


class FluentWidgetBase:
    def _init_fluent_base(self):
        self._tm = ThemeManager()
        self._tm.register_widget(self)
        self._tm.theme_changed.connect(self._on_theme_changed)
        self._theme_applied = False
        QTimer.singleShot(0, self._apply_theme_deferred)

    def _apply_theme_deferred(self):
        if not self._theme_applied:
            self.apply_theme()
            self._theme_applied = True

    def _on_theme_changed(self, theme):
        if hasattr(self, '_hovered'):
            self._hovered = False
        if hasattr(self, '_pressed'):
            self._pressed = False
        self.apply_theme()
        self.update()

    def apply_theme(self):
        pass

    def _fluent_show_event(self, event):
        if not self._theme_applied:
            self.apply_theme()
            self._theme_applied = True

    def _cleanup_fluent_base(self):
        try:
            if hasattr(self, '_tm') and self._tm is not None:
                self._tm.unregister_widget(self)
                self._tm.theme_changed.disconnect(self._on_theme_changed)
        except (RuntimeError, SystemError, AttributeError):
            pass

    def __del__(self):
        try:
            self._cleanup_fluent_base()
        except Exception:
            pass
