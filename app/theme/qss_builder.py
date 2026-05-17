from app.theme.theme_manager import ThemeManager


def build_global_qss() -> str:
    tm = ThemeManager()
    c = lambda token: tm.color(token)
    s = lambda token: f"{tm.spacing(token)}px"
    r = lambda token: f"{tm.radius(token)}px"

    return f"""
    QWidget {{
        font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
        font-size: {tm.font_size("body")}px;
        color: {c("fg_primary")};
        background-color: {c("bg_solid_base")};
    }}

    QScrollArea {{
        background-color: transparent;
        border: none;
    }}

    QScrollBar:vertical {{
        background-color: {c("scrollbar_bg")};
        width: 8px;
        margin: 0;
        border-radius: 4px;
    }}

    QScrollBar::handle:vertical {{
        background-color: {c("scrollbar_handle")};
        min-height: 30px;
        border-radius: 4px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {c("scrollbar_handle_hover")};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background-color: {c("scrollbar_bg")};
        height: 8px;
        margin: 0;
        border-radius: 4px;
    }}

    QScrollBar::handle:horizontal {{
        background-color: {c("scrollbar_handle")};
        min-width: 30px;
        border-radius: 4px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background-color: {c("scrollbar_handle_hover")};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    QLabel {{
        background-color: transparent;
        color: {c("fg_primary")};
    }}

    QLabel#subtitle {{
        color: {c("fg_secondary")};
        font-size: {tm.font_size("body")}px;
    }}

    QLabel#section_title {{
        color: {c("fg_primary")};
        font-size: {tm.font_size("title_medium")}px;
        font-weight: {tm.font_weight("semibold")};
    }}
    """
