import weakref

from PySide6.QtCore import QObject, Signal
from app.theme.colors import Theme, LIGHT_COLORS, DARK_COLORS
from app.theme.typography import FONT_SIZES, FONT_WEIGHTS, SPACING, RADII, ANIMATION_DURATIONS, ICON_SIZES


class ThemeManager(QObject):
    theme_changed = Signal(object)

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if hasattr(self, "_initialized"):
            return
        super().__init__(parent)
        self._initialized = True
        self._theme = Theme.LIGHT
        self._registered_widgets = weakref.WeakSet()

    @property
    def theme(self):
        return self._theme

    @property
    def is_dark(self):
        return self._theme == Theme.DARK

    def toggle_theme(self):
        if self._theme == Theme.LIGHT:
            self._theme = Theme.DARK
        else:
            self._theme = Theme.LIGHT
        from app.icons.icon_provider import clear_cache
        clear_cache()
        self.theme_changed.emit(self._theme)

    def set_theme(self, theme: Theme):
        if self._theme != theme:
            self._theme = theme
            from app.icons.icon_provider import clear_cache
            clear_cache()
            self.theme_changed.emit(self._theme)

    def color(self, token: str) -> str:
        colors = DARK_COLORS if self.is_dark else LIGHT_COLORS
        return colors.get(token, "#FF00FF")

    def font_size(self, token: str) -> int:
        return FONT_SIZES.get(token, 14)

    def font_weight(self, token: str) -> str:
        return FONT_WEIGHTS.get(token, "400")

    def spacing(self, token: str) -> int:
        return SPACING.get(token, 8)

    def radius(self, token: str) -> int:
        return RADII.get(token, 8)

    def duration(self, token: str) -> int:
        return ANIMATION_DURATIONS.get(token, 250)

    def icon_size(self, token: str) -> int:
        return ICON_SIZES.get(token, 20)

    def register_widget(self, widget):
        try:
            self._registered_widgets.add(widget)
        except TypeError:
            pass

    def unregister_widget(self, widget):
        try:
            self._registered_widgets.discard(widget)
        except (TypeError, KeyError):
            pass

    @classmethod
    def reset(cls):
        cls._instance = None
