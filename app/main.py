import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.theme.theme_manager import ThemeManager
from app.theme.qss_builder import build_global_qss
from app.splash.splash_screen import SplashScreen
from app.layout.main_window import MainWindow
from app.pages.hero_page import HeroPage


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    tm = ThemeManager()

    def apply_global_theme(*args):
        app.setStyleSheet(build_global_qss())

    tm.theme_changed.connect(apply_global_theme)
    apply_global_theme()

    window = MainWindow()

    window.add_page("home", "首页", "home", HeroPage())
    window.add_nav_separator("组件")

    from app.pages.button_page import ButtonPage
    from app.pages.input_page import InputPage
    from app.pages.navigation_page import NavigationPage
    from app.pages.surface_page import SurfacePage
    from app.pages.feedback_page import FeedbackPage
    from app.pages.display_page import DisplayPage
    from app.pages.chart_page import ChartPage
    from app.pages.diagram_page import DiagramPage

    window.add_lazy_page("buttons", "按钮", "add", ButtonPage)
    window.add_lazy_page("inputs", "输入", "edit", InputPage, children=[
        {"key": "inputs_text", "label": "文本输入"},
        {"key": "inputs_select", "label": "选择控件"},
        {"key": "inputs_date", "label": "日期时间"},
    ])
    window.add_lazy_page("navigation", "导航", "layout", NavigationPage, children=[
        {"key": "nav_tabs", "label": "标签导航"},
        {"key": "nav_menu", "label": "菜单导航"},
        {"key": "nav_anchor", "label": "锚点导航"},
    ])
    window.add_lazy_page("surfaces", "表面", "grid", SurfacePage)
    window.add_lazy_page("feedback", "反馈", "notifications", FeedbackPage, children=[
        {"key": "feedback_notify", "label": "通知"},
        {"key": "feedback_toast", "label": "提示"},
        {"key": "feedback_progress", "label": "进度"},
    ])
    window.add_lazy_page("display", "展示", "text", DisplayPage)
    window.add_lazy_page("charts", "图表", "chart", ChartPage)
    window.add_lazy_page("diagrams", "图示", "project", DiagramPage)

    from app.pages.subscription_page import SubscriptionPage
    window.add_lazy_page("subscription", "会员", "crown", SubscriptionPage)

    from app.pages.settings_page import SettingsPage
    window.add_lazy_page("settings", "设置", "settings", SettingsPage)

    window._nav.set_active("home")

    splash = SplashScreen()
    splash.start_loading(on_finished=lambda: (window.show(), window.raise_()))

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
