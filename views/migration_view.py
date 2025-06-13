import flet as ft
from utils.load_current_test_uuid import load_current_test_uuid
from handlers.migration.fetch_vulns import fetch_vulns_per_migration, build_migration_entries


class MigrationView:
    def __init__(self, app_state):
        self.app_state = app_state
        self.page = app_state.page

    def render(self):

        migrate_vulns_text = ft.Text(
            "Migrate Vulnerabilities per Test",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )

        migrate_test_uuid_text_field = ft.CupertinoTextField(
            placeholder_text="Test UUID",
            filled=True,
            expand=True
        )

        self.app_state.migrate_test_uuid_text_field = migrate_test_uuid_text_field
        self.app_state.page.migrate_test_uuid_text_field = migrate_test_uuid_text_field

        migration_load_test_uuid_button = ft.FilledTonalButton(
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
            on_click=lambda e: load_current_test_uuid(e.page, e, "migration"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        migration_fetch_vuln_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.AUTORENEW),
                        ft.Text("Fetch Vulnerabilities", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: fetch_vulns_per_migration(e.page, migrate_test_uuid_text_field.value),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        migrate_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CALL_SPLIT),
                        ft.Text("Migrate selected Vulnerabilities", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: build_migration_entries(e.page),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        migration_table_container = ft.Container(expand=True)

        self.app_state.migration_table_container = migration_table_container
        self.app_state.page.migration_table_container = migration_table_container

        first_row = ft.Column(
            expand=True,
            spacing=20,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.INDIGO_50,
                    expand=True,
                    padding=10,
                    content=ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        spacing=20,
                        controls=[
                            migrate_vulns_text,
                            ft.Divider(),
                            ft.Row(
                                controls=[
                                    migrate_test_uuid_text_field, migration_load_test_uuid_button,
                                    migration_fetch_vuln_button, migrate_button
                                ],
                                expand=True
                            ),
                            migration_table_container
                        ]
                    )
                )
            ]
        )

        dummy_card = ft.Container(
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=20,
            content=first_row
        )

        return ft.Column([
            dummy_card
        ])
