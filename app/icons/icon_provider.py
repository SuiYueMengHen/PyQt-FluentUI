import os
from pathlib import Path

from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication

from app.theme.theme_manager import ThemeManager


_ICONS_DIR = Path(__file__).parent
_FILLED_DIR = _ICONS_DIR / "filled"
_OUTLINE_DIR = _ICONS_DIR / "outline"

_cache: dict[str, QIcon] = {}
_svg_bytes_cache: dict[str, bytes] = {}

_ICON_ALIASES = {
    "close": "x",
    "add": "plus",
    "info_circle": "info-circle",
    "error": "alert-circle",
    "warning": "alert-triangle",
    "info": "info-circle",
    "image": "photo",
    "eye_off": "eye-off",
    "arrow_up": "arrow-big-up",
    "arrow_down": "arrow-big-down",
    "arrow_left": "arrow-big-left",
    "arrow_right": "arrow-big-right",
    "chevron_left": "chevron-left",
    "chevron_right": "chevron-right",
    "chevron_down": "chevron-down",
    "chevron_up": "chevron-up",
    "notifications": "bell",
    "text": "writing",
    "chart": "chart-pie",
    "project": "sitemap",
    "grid": "apps",
    "terminal": "code",
    "check_circle": "circle-check",
    "star_outline": "star",
    "more_horizontal": "dots",
    "bar_chart": "chart-pie",
    "zoom_in": "zoom-in",
    "zoom_out": "zoom",
    "download_cloud": "cloud-download",
    "upload_cloud": "cloud-upload",
    "percent": "circle-percentage",
    "refresh": "refresh",
    "delete": "trash",
    "like": "thumb-up",
    "dislike": "thumb-down",
    "favorite": "heart",
    "bookmark": "bookmark",
    "share": "share",
    "copy": "copy",
    "download": "download",
    "upload": "upload",
    "search": "search",
    "filter": "filter",
    "settings": "settings",
    "lock": "lock",
    "unlock": "lock-open",
    "mail": "mail",
    "flag": "flag",
    "globe": "globe",
    "link": "link",
    "tag": "tag",
    "clock": "clock",
    "wifi": "wifi",
    "shopping_cart": "shopping-cart",
    "ticket": "ticket",
    "gift": "gift",
    "trophy": "trophy",
    "medal": "medal",
    "sparkle": "sparkle",
    "crown": "crown",
    "volume": "volume",
    "camera": "camera",
    "music": "music",
    "maximize": "maximize",
    "minimize": "minimize",
    "user": "user",
}


def _resolve_icon_name(name: str) -> str:
    return _ICON_ALIASES.get(name, name)


def _find_svg(name: str, variant: str) -> Path | None:
    resolved = _resolve_icon_name(name)
    if variant == "filled":
        p = _FILLED_DIR / f"{resolved}.svg"
        if p.exists():
            return p
        p = _OUTLINE_DIR / f"{resolved}.svg"
        if p.exists():
            return p
    else:
        p = _OUTLINE_DIR / f"{resolved}.svg"
        if p.exists():
            return p
        p = _FILLED_DIR / f"{resolved}.svg"
        if p.exists():
            return p
    return None


def _get_svg_bytes(svg_path: Path, color: str) -> bytes:
    cache_key = f"{svg_path}_{color}"
    if cache_key in _svg_bytes_cache:
        return _svg_bytes_cache[cache_key]
    svg_data = svg_path.read_text(encoding="utf-8")
    svg_data = svg_data.replace("currentColor", color)
    svg_bytes = svg_data.encode("utf-8")
    _svg_bytes_cache[cache_key] = svg_bytes
    return svg_bytes


def _render_svg_to_pixmap(svg_data: bytes, size: int, dpr: float) -> QPixmap:
    renderer = QSvgRenderer()
    renderer.load(svg_data)
    if not renderer.isValid():
        return QPixmap()

    pixel_size = int(size * dpr)
    pixmap = QPixmap(pixel_size, pixel_size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
    renderer.render(painter)
    painter.end()

    pixmap.setDevicePixelRatio(dpr)
    return pixmap


def get_icon(name: str, color: str | None = None, size: int = 20) -> QIcon:
    tm = ThemeManager()
    variant = "filled" if tm.is_dark else "outline"
    cache_key = f"{name}_{color}_{size}_{variant}"
    if cache_key in _cache:
        return _cache[cache_key]

    icon_color = color or tm.color("fg_primary")
    svg_path = _find_svg(name, variant)
    if svg_path is None:
        return QIcon()

    svg_bytes = _get_svg_bytes(svg_path, icon_color)

    app = QApplication.instance()
    dpr = app.devicePixelRatio() if app else 1.0

    icon = QIcon()
    sizes = [16, 20, 24, 32, 48, 64]
    if size not in sizes:
        sizes.append(size)
    for s in sizes:
        pm = _render_svg_to_pixmap(svg_bytes, s, dpr)
        if not pm.isNull():
            icon.addPixmap(pm)

    _cache[cache_key] = icon
    return icon


def get_pixmap(name: str, color: str | None = None, size: int = 20) -> QPixmap:
    tm = ThemeManager()
    variant = "filled" if tm.is_dark else "outline"
    icon_color = color or tm.color("fg_primary")
    svg_path = _find_svg(name, variant)
    if svg_path is None:
        return QPixmap()

    svg_bytes = _get_svg_bytes(svg_path, icon_color)

    app = QApplication.instance()
    dpr = app.devicePixelRatio() if app else 1.0

    return _render_svg_to_pixmap(svg_bytes, size, dpr)


def clear_cache():
    _cache.clear()
    _svg_bytes_cache.clear()
