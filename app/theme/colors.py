from enum import Enum


class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"


LIGHT_COLORS = {
    "primary": "#0078D4",
    "primary_hover": "#106EBE",
    "primary_pressed": "#005A9E",
    "primary_light": "#DEECF9",
    "primary_text_on": "#FFFFFF",

    "bg_solid_base": "#F5F5F5",
    "bg_solid_card": "#FFFFFF",
    "bg_solid_secondary": "#FAFAFA",
    "bg_solid_tertiary": "#F0F0F0",
    "bg_subtle": "#F9F9F9",

    "fg_primary": "#1A1A1A",
    "fg_secondary": "#616161",
    "fg_tertiary": "#8A8A8A",
    "fg_disabled": "#A0A0A0",

    "stroke_card": "#E5E5E5",
    "stroke_divider": "#F0F0F0",
    "stroke_focus": "#0078D4",
    "stroke_hover": "#C8C8C8",

    "accent_success": "#107C10",
    "accent_success_light": "#DFF6DD",
    "accent_warning": "#FF8C00",
    "accent_warning_light": "#FFF4CE",
    "accent_error": "#D13438",
    "accent_error_light": "#FDE7E9",
    "accent_info": "#0078D4",
    "accent_info_light": "#DEECF9",

    "shadow_card": "rgba(0,0,0,0.04)",
    "shadow_card_hover": "rgba(0,0,0,0.08)",
    "overlay": "rgba(0,0,0,0.4)",

    "nav_bg": "#FAFAFA",
    "nav_item_hover": "#F0F0F0",
    "nav_item_active": "#DEECF9",
    "nav_item_active_border": "#0078D4",

    "titlebar_bg": "#FFFFFF",
    "titlebar_fg": "#1A1A1A",
    "titlebar_button_hover": "#E5E5E5",
    "titlebar_button_close_hover": "#C42B1C",
    "titlebar_button_close_fg": "#FFFFFF",

    "scrollbar_bg": "#F0F0F0",
    "scrollbar_handle": "#C1C1C1",
    "scrollbar_handle_hover": "#A0A0A0",
}

DARK_COLORS = {
    "primary": "#60CDFF",
    "primary_hover": "#4DB8E8",
    "primary_pressed": "#3AA5D4",
    "primary_light": "#003A5E",
    "primary_text_on": "#003A5E",

    "bg_solid_base": "#1F1F1F",
    "bg_solid_card": "#2D2D2D",
    "bg_solid_secondary": "#252525",
    "bg_solid_tertiary": "#333333",
    "bg_subtle": "#292929",

    "fg_primary": "#F5F5F5",
    "fg_secondary": "#AAAAAA",
    "fg_tertiary": "#777777",
    "fg_disabled": "#5C5C5C",

    "stroke_card": "#3D3D3D",
    "stroke_divider": "#333333",
    "stroke_focus": "#60CDFF",
    "stroke_hover": "#4D4D4D",

    "accent_success": "#6CCB5F",
    "accent_success_light": "#1A3A1A",
    "accent_warning": "#FFB900",
    "accent_warning_light": "#3A2E00",
    "accent_error": "#FF6B6B",
    "accent_error_light": "#3A1A1A",
    "accent_info": "#60CDFF",
    "accent_info_light": "#003A5E",

    "shadow_card": "rgba(0,0,0,0.2)",
    "shadow_card_hover": "rgba(0,0,0,0.3)",
    "overlay": "rgba(0,0,0,0.6)",

    "nav_bg": "#252525",
    "nav_item_hover": "#333333",
    "nav_item_active": "#003A5E",
    "nav_item_active_border": "#60CDFF",

    "titlebar_bg": "#2D2D2D",
    "titlebar_fg": "#F5F5F5",
    "titlebar_button_hover": "#3D3D3D",
    "titlebar_button_close_hover": "#C42B1C",
    "titlebar_button_close_fg": "#FFFFFF",

    "scrollbar_bg": "#1F1F1F",
    "scrollbar_handle": "#555555",
    "scrollbar_handle_hover": "#777777",
}
