import flet as ft
from app_state import AppState
from views.base_template import TemplatePage
from views.home_view import HomeView
from views.upload_view import UploadView
from views.manage_view import ManageView
from views.migration_view import MigrationView
from views.cache_view import CacheView
from views.report_view import ReportView
from views.settings_view import SettingsView
from views.test_view import TestView
from views.about_view import AboutView


def main(page: ft.Page):
    # ---- basic page setup ----
    page.title = "GOST Admin Shortcut"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True
    page.window_resizable = True
    page.snack_bar = ft.SnackBar(content=ft.Text(""), open=False)

    # ---- shared state + caches ----
    app_state = AppState()
    app_state.page = page
    page.app_state = app_state

    # one inner‐view instance per route
    app_state.view_instances = {}
    # one rendered inner‐view control per route
    app_state.view_contents = {}

    # *** ONLY ONE TemplatePage FOR ALL ROUTES ***
    # we’ll swap out its content_view + selected_index on each nav
    tpl = TemplatePage(page, app_state, content_view=None, selected_index=0)
    app_state.template_page = tpl

    # map of routes → (title, view class)
    route_map = {
        "/":  ("Home", HomeView),
        "/1": ("Upload Vulns", UploadView),
        "/2": ("Manage Test", TestView),
        "/3": ("Manage Vuln", ManageView),
        "/4": ("Migration", MigrationView),
        "/5": ("Cache", CacheView),
        "/6": ("Report", ReportView),
        "/7": ("Settings", SettingsView),
        "/8": ("About", AboutView),
        "/9": ("Restart", None),
    }

    def route_change(e):
        # figure out route key
        route = page.route or "/"

        # full app “reboot”
        if route == "/9":
            # clear view caches
            app_state.view_instances.clear()
            app_state.view_contents.clear()
            # reset any dynamic AppState fields
            app_state.project_folder = None
            app_state.vuln_type_map = {}
            app_state.vuln_type_uuid = ""
            app_state.vuln_type_context_uuid = ""
            app_state.current_finding_index = 0
            app_state.current_image_index = 0
            app_state.findings = []
            app_state.metadata = None
            app_state.ai_suggestions = []
            app_state.ai_suggestions_editable = []
            app_state.org_uuid = ""
            app_state.org_name = ""
            app_state.asset_uuid = ""
            app_state.asset_name = ""
            app_state.test_uuid = ""
            app_state.test_id = ""
            app_state.uploaded_vulns = {}
            app_state.folder_stack = []
            app_state.current_items = []

            tpl_reset = TemplatePage(page, app_state, content_view=None, selected_index=0)
            app_state.template_page = tpl_reset

            page.go("/")
            return

        title, ViewCls = route_map.get(route, ("Home", HomeView))
        app_state.current_view_title = title

        # 1) get-or-create the inner view instance
        if route not in app_state.view_instances:
            inst = ViewCls(app_state)
            app_state.view_instances[route] = inst
            # render once
            app_state.view_contents[route] = inst.render()
        content = app_state.view_contents[route]

        # 2) update our single TemplatePage
        tpl.selected_index = int(route[1:]) if len(route) > 1 else 0
        tpl.content_view = content

        # 3) display it
        page.views.clear()
        page.views.append(
            ft.View(
                route=route,
                controls=[tpl.render()]
            )
        )
        page.update()

        # 4) special hook for cache view
        if route == "/5":
            app_state.view_instances[route].load_initial_data()

    page.on_route_change = route_change
    page.go(page.route or "/")


if __name__ == "__main__":
    ft.app(target=main)
