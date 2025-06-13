import flet as ft
from flet import FilePicker
from handlers.settings.dashboard import (
    save_dashboard_key,
    check_dashboard_key,
    delete_dashboard_key,
    close_dialog_dashboard,
)
from handlers.settings.google import (
    handle_google_json_selection,
    check_google_key,
    delete_google_key,
    close_dialog_google
)
from handlers.settings.ai import (
    save_ai_key,
    check_ai_key,
    delete_ai_key,
    close_dialog_ai
)


class SettingsView:
    def __init__(self, app_state):
        self.app_state = app_state
        self.page = app_state.page

    def render(self):
        def card(icon, title: str, body_controls: list[ft.Control]):
            return ft.Container(
                bgcolor=ft.Colors.INDIGO_50,
                border_radius=10,
                padding=20,
                expand=True,  # This makes the container expand to fill available space
                content=ft.Column(
                    expand=True,  # Column should expand to fill container
                    alignment=ft.MainAxisAlignment.START,  # Align content to top
                    spacing=10,  # Add consistent spacing between elements
                    controls=[
                        ft.Row([
                            ft.Icon(icon, size=20),
                            ft.Text(title, style="titleSmall", expand=True)
                        ]),
                        ft.Divider(),
                        *body_controls,
                        ft.Container(expand=True)  # Spacer to push content to top
                    ]
                )
            )

        # === Alert dialog ===

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Deletion"),
            content=ft.Text("Are you sure you want to delete this key?"),
        )

        def handle_key_to_delete(page, e, service):
            if service == "Dashboard":
                confirm_dialog.actions = [
                    ft.TextButton("Yes", on_click=lambda e: delete_dashboard_key(page=e.page, e=e)),
                    ft.TextButton("Cancel", on_click=lambda e: close_dialog_dashboard(page=e.page, e=e))
                ]
            elif service == "Google":
                confirm_dialog.actions = [
                    ft.TextButton("Yes", on_click=lambda e: delete_google_key(page=e.page, e=e)),
                    ft.TextButton("Cancel", on_click=lambda e: close_dialog_google(page=e.page, e=e))
                ]
            elif service == "AI":
                confirm_dialog.actions = [
                    ft.TextButton("Yes", on_click=lambda e: delete_ai_key(page=e.page, e=e)),
                    ft.TextButton("Cancel", on_click=lambda e: close_dialog_ai(page=e.page, e=e))
                ]

            page.confirm_dialog = confirm_dialog
            page.confirm_dialog.open = True
            page.update()

        # === Dashboard card content blocks ===
        api_dashboard_info_text = ft.Text("Manage your KISS24 platform API key.")

        api_dashboard_text_field = ft.TextField(label="API Key", password=True, can_reveal_password=True)

        api_dashboard_button_save = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.SAVE),
                        ft.Text("Save", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: save_dashboard_key(
                page=e.page,
                key=api_dashboard_text_field.value,
                e=e,
                reset_callback=lambda: (
                    api_dashboard_text_field.__setattr__("value", ""),
                    api_dashboard_text_field.update()
                )
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        api_dashboard_button_check = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.CHECK_CIRCLE),
                        ft.Text("Check", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: check_dashboard_key(page=e.page, e=e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        api_dashboard_button_delete = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.DELETE),
                        ft.Text("Delete", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: handle_key_to_delete(page=e.page, e=e, service="Dashboard"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.RED_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                        }
            )
        )

        dashboard_card = card(
            icon=ft.Icons.VPN_KEY,
            title="API Key (General)",
            body_controls=[
                api_dashboard_info_text,
                api_dashboard_text_field,
                ft.Row(
                    controls=[
                        api_dashboard_button_save,
                        api_dashboard_button_check,
                        api_dashboard_button_delete
                    ]
                )
            ]
        )

        # === Google card content blocks ===

        google_key_info_text = ft.Text("Manage Google Desktop key.")

        google_json_picker = FilePicker()
        self.page.overlay.append(google_json_picker)
        google_json_picker.on_result = lambda e: handle_google_json_selection(page=self.page, e=e)

        google_json_status = ft.Text("No file selected", italic=True, color=ft.Colors.GREY, size=10)
        self.app_state.google_json_status = google_json_status

        google_button_check = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.CHECK_CIRCLE),
                        ft.Text("Check", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: check_google_key(page=e.page, e=e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        upload_json_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.UPLOAD_FILE),
                        ft.Text("Upload and Save", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda _: google_json_picker.pick_files(
                allowed_extensions=["json"],
                dialog_title="Select Google Service Account JSON"
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.BLUE_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        google_button_delete = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.DELETE),
                        ft.Text("Delete", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: handle_key_to_delete(page=e.page, e=e, service="Google"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.RED_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                        }
            )
        )

        google_card = card(
            icon=ft.Icons.LANGUAGE,
            title="Google Cloud Key",
            body_controls=[
                google_key_info_text,
                ft.Row(
                    controls=[
                        upload_json_button,
                        google_button_check,
                        google_button_delete
                    ]
                ),
                google_json_status
            ]
        )

        # === AI card content blocks ===

        api_ai_info_text = ft.Text("Manage the key used for LLM-based features.")

        api_ai_text_field = ft.TextField(label="API Key", password=True, can_reveal_password=True)

        api_ai_button_save = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.SAVE),
                        ft.Text("Save", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: save_ai_key(
                page=e.page,
                key=api_ai_text_field.value,
                e=e,
                reset_callback=lambda: (
                    api_ai_text_field.__setattr__("value", ""),
                    api_ai_text_field.update()
                )
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        api_ai_button_check = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.CHECK_CIRCLE),
                        ft.Text("Check", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: check_ai_key(page=e.page, e=e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        api_ai_button_delete = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 6, 0, 6),  # top/bottom spacing
                content=ft.Column(
                    controls=[
                        ft.Icon(name=ft.Icons.DELETE),
                        ft.Text("Delete", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: handle_key_to_delete(page=e.page, e=e, service="AI"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.RED_300,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        ai_card = card(
            icon=ft.Icons.SMART_TOY,
            title="AI Integration Key",
            body_controls=[
                api_ai_info_text,
                api_ai_text_field,
                ft.Row(
                    controls=[
                        api_ai_button_save,
                        api_ai_button_check,
                        api_ai_button_delete
                    ]
                )
            ]
        )

        # === Layout row ===
        settings_body = ft.Row(
            expand=True,
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,  # Align all cards to top
            controls=[
                ft.Container(
                    expand=True,  # Each container should expand equally
                    content=dashboard_card
                ),
                ft.Container(
                    expand=True,
                    content=google_card
                ),
                ft.Container(
                    expand=True,
                    content=ai_card
                ),
            ]
        )

        return ft.Column(
            expand=True,  # Make the main column expand to fill available space
            controls=[
                ft.Container(
                    padding=ft.padding.all(10),
                    content=settings_body,
                    expand=True
                ),
                confirm_dialog
            ]
        )
