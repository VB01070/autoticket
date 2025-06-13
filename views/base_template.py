import flet as ft
import os
from utils.open_project_folder import open_project_folder
from utils.do_caching import initial_fetch
from utils.caching import CACHE_PATH
from utils.check_update import check_for_update
import asyncio


class TemplatePage:
    def __init__(self, page: ft.Page, app_state, content_view: ft.Control, selected_index: int):
        self.page = page
        self.app_state = app_state
        self.content_view = content_view
        self.selected_index = selected_index

        self.check_update_icon = ft.Icon(name=ft.Icons.VERIFIED_OUTLINED, tooltip="Up to date", color=ft.Colors.GREEN, size=20)
        app_state.check_update_icon = self.check_update_icon

        self.info_progress = ft.ProgressRing(
            color=ft.Colors.ORANGE_ACCENT,
            width=12,
            height=12,
            stroke_width=2,
            visible=False  # Hidden by default
        )
        app_state.info_progress = self.info_progress

        page.run_task(self._async_check_for_update)

    async def _async_check_for_update(self):
        # run your blocking check in a threadpool
        ahead = await asyncio.to_thread(check_for_update)
        if ahead > 0:
            # mutate the icon and pop the dialog
            self.check_update_icon.name = ft.Icons.NOTIFICATIONS_OUTLINED
            self.check_update_icon.tooltip = "Update Available"
            self.check_update_icon.color = ft.Colors.ORANGE
            self.check_update_icon.update()

            # finally push the update back to the UI
            self.page.update()

    def render(self):
        def on_nav_change(e):
            self.page.go(f"/{e.control.selected_index}")

        # Navigation Rail
        nav_rail = ft.NavigationRail(
            selected_index=self.selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationRailDestination(icon=ft.Icons.UPLOAD, label="Upload"),
                ft.NavigationRailDestination(icon=ft.Icons.SCIENCE, label="Test"),
                ft.NavigationRailDestination(icon=ft.Icons.BUG_REPORT, label="Vulns"),
                ft.NavigationRailDestination(icon=ft.Icons.SYNC_ALT, label="Migration"),
                ft.NavigationRailDestination(icon=ft.Icons.DATASET, label="Cache"),
                ft.NavigationRailDestination(icon=ft.Icons.ASSIGNMENT, label="Reporting"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Setting"),
                ft.NavigationRailDestination(icon=ft.Icons.REFRESH, label="Restart"),
            ],
            on_change=on_nav_change,
        )
        # == Preparing top info bar  ==
        project_folder_temp_text = ft.Text(
            f"{self.app_state.project_folder if self.app_state.project_folder else 'No project folder'} ", size=12
        )
        self.app_state.project_folder_temp_text = project_folder_temp_text

        if os.path.exists(CACHE_PATH):
            cache_check_icon = ft.Icon(name=ft.Icons.CHECK, color=ft.Colors.GREEN_ACCENT)
        else:
            cache_check_icon = ft.Icon(name=ft.Icons.CLOSE, color=ft.Colors.RED_ACCENT)
        self.app_state.cache_check_icon = cache_check_icon
        self.app_state.page.cache_check_icon = cache_check_icon

        cache_state_temp_text = ft.Text("| Cache Loaded: ", size=12)

        layout = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(width=90, content=nav_rail),
                ft.VerticalDivider(width=1),
                ft.Container(
                    expand=True,
                    padding=20,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(self.app_state.current_view_title, style="headlineMedium", expand=True),
                            self.info_progress,
                            ft.FilledTonalButton(
                                content=ft.Container(
                                    padding=ft.Padding(0, 0, 0, 0),
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.Icons.AUTORENEW),
                                            ft.Text("Fetch Cache", size=12),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=2
                                    )
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.AMBER_ACCENT_100,
                                        ft.ControlState.DEFAULT: ft.Colors.WHITE10
                                    }
                                ),
                                on_click=lambda e: initial_fetch(page=e.page, e=e)
                            ),

                            ft.FilledTonalButton(
                                content=ft.Container(
                                    padding=ft.Padding(0, 0, 0, 0),
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.Icons.CREATE_NEW_FOLDER),
                                            ft.Text("Select Project Folder", size=12),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=2
                                    )
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: ft.Colors.LIGHT_BLUE_100,
                                        ft.ControlState.DEFAULT: ft.Colors.WHITE10
                                    }
                                ),
                                on_click=lambda e: open_project_folder(page=e.page, e=e)
                            ),
                            project_folder_temp_text,
                            cache_state_temp_text,
                            cache_check_icon,
                            self.check_update_icon
                        ]),
                        ft.Divider(),
                        self.content_view
                    ])
                )
            ]
        )

        return ft.Column(
            expand=True,
            controls=[
                layout,
                self.page.snack_bar  # Ensure the snackbar is always rendered
            ]
        )
