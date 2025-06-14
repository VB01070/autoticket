import flet as ft
from utils.load_current_test_uuid import load_current_test_uuid
from handlers.manage.edit_test import edit_test_details
from handlers.manage.fetch_vulns import fetch_vulns_by_test
from handlers.manage.publish_vuln import publish_selected_vulns, publish_vulnerability
from handlers.manage.delete_vuln import delete_vuln, delete_selected_vulns


class ManageView:
    def __init__(self, app_state):
        self.app_state = app_state
        self.page = app_state.page

    def render(self):

        # test/single vulns row
        # VULNERABILITY
        modify_vuln_text = ft.Text(
            "Publish/Delete Vulnerability",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )

        vuln_uuid_text_field = ft.CupertinoTextField(
            placeholder_text="Vuln UUID",
            filled=True
        )

        self.app_state.vuln_uuid_text_field = vuln_uuid_text_field
        self.app_state.page.vuln_uuid_text_field = vuln_uuid_text_field

        publish_vuln_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.PUBLISHED_WITH_CHANGES),
                        ft.Text("Publish Vulnerability", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: publish_vulnerability(e.page, e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        delete_vuln_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.DELETE),
                        ft.Text("Delete", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: delete_vuln(e.page, e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.DEEP_ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        # all vulns row

        modify_all_vulns_text = ft.Text(
            "Publish/Delete all Vulnerabilities per Test",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )

        test_uuid_all_text_field = ft.CupertinoTextField(
            placeholder_text="Test UUID",
            filled=True,
            expand=True
        )

        self.app_state.test_uuid_all_text_field = test_uuid_all_text_field
        self.app_state.page.test_uuid_all_text_field = test_uuid_all_text_field

        load_test_uuid_all_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.FINGERPRINT),
                        ft.Text("Load the Current Test UUID", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: load_current_test_uuid(e.page, e, "publish"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        fetch_all_vuln_per_test_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.DOWNLOADING),
                        ft.Text("Fetch Vulns per test", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: fetch_vulns_by_test(e.page, test_uuid_all_text_field.value),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.AMBER_ACCENT_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        vuln_table_container = ft.Container(expand=True, height=300)

        self.app_state.vuln_table_container = vuln_table_container
        self.app_state.page.vuln_table_container = vuln_table_container

        publish_all_vuln_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.PUBLISHED_WITH_CHANGES),
                        ft.Text("Publish Selected", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: publish_selected_vulns(e.page, e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        delete_all_vuln_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.DELETE),
                        ft.Text("Delete Selected", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: delete_selected_vulns(e.page, e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.DEEP_ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        first_row = ft.Column(
            expand=True,
            spacing=20,
            controls=[
                # ft.Container(
                #     bgcolor=ft.Colors.INDIGO_50,
                #     expand=True,
                #     padding=10,
                #     content=ft.Column(
                #         expand=True,
                #         horizontal_alignment=ft.CrossAxisAlignment.START,
                #         spacing=10,
                #         controls=[
                #             modify_vuln_text,
                #             ft.Divider(),
                #             vuln_uuid_text_field,
                #             ft.Row([publish_vuln_button, delete_vuln_button, ft.Container(expand=True)]),
                #         ]
                #     )
                # ),
                ft.Container(
                    bgcolor=ft.Colors.INDIGO_50,
                    expand=True,
                    padding=10,
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        spacing=10,
                        controls=[
                            modify_all_vulns_text,
                            ft.Divider(),
                            ft.Row(
                                [test_uuid_all_text_field, load_test_uuid_all_button, fetch_all_vuln_per_test_button, publish_all_vuln_button, delete_all_vuln_button],
                                expand=True),
                            vuln_table_container
                        ]
                    )
                )
            ]
        )

        dummy_card = ft.Container(
            border_radius=10,
            padding=20,
            content=first_row
        )

        return ft.Column([
            dummy_card
        ])
