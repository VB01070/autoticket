import flet as ft
from utils.load_current_test_uuid import load_current_test_uuid
from utils.service_tag_references import (
    white_box_tag_uuid,
    black_box_tag_uuid,
    grey_box_tag_uuid,
    adversary_simulation_tag_uuid
)
from handlers.test.edit_details import edit_details
from handlers.test.build_ai_management_summary_payload import build_ai_management_summary_payload


class TestView:
    def __init__(self, app_state):
        self.app_state = app_state
        self.page = app_state.page

    def render(self):
        # TEST
        modify_test_details_text = ft.Text(
            "Modify test details",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )

        test_uuid_text_field = ft.CupertinoTextField(
            placeholder_text="Test UUID",
            filled=True,
            expand=True
        )

        self.app_state.test_uuid_text_field = test_uuid_text_field
        self.app_state.page.test_uuid_text_field = test_uuid_text_field

        load_test_uuid_button = ft.FilledTonalButton(
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
            on_click=lambda e: load_current_test_uuid(e.page, e, "test"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        servicenow_id_text_field = ft.CupertinoTextField(
            placeholder_text="ServiceNow Request ID",
            filled=True,
            expand=True
        )

        self.app_state.servicenow_id_text_field = servicenow_id_text_field
        self.app_state.page.servicenow_id_text_field = servicenow_id_text_field

        connection_type_dropdown = ft.Dropdown(
            label="Connection Type",
            options=[
                ft.dropdown.Option("Public"),
                ft.dropdown.Option("VPN"),
                ft.dropdown.Option("TeamViewer"),
                ft.dropdown.Option("IP WhiteList"),
                ft.dropdown.Option("RDP"),
                ft.dropdown.Option("Other..."),
            ],
            expand=True
        )

        self.app_state.connection_type_dropdown = connection_type_dropdown
        self.app_state.page.connection_type_dropdown = connection_type_dropdown

        testing_account_switch = ft.CupertinoSwitch(
            label="Test Accounts",
            value=True
        )

        self.app_state.testing_account_switch = testing_account_switch
        self.app_state.page.testing_account_switch = testing_account_switch

        account_role_text_field = ft.CupertinoTextField(
            placeholder_text="Account Roles",
            filled=True,
            expand=True
        )

        self.app_state.account_role_text_field = account_role_text_field
        self.app_state.page.account_role_text_field = account_role_text_field

        management_summary_text_field = ft.CupertinoTextField(
            placeholder_text="Management Summary",
            filled=True,
            multiline=True,
            min_lines=10,
            max_lines=10,
            read_only=False
        )

        self.app_state.management_summary_text_field = management_summary_text_field
        self.app_state.page.management_summary_text_field = management_summary_text_field

        service_tag_dropdown = ft.Dropdown(
            label="Service Tags",
            options=[
                ft.dropdown.Option(key=adversary_simulation_tag_uuid, text="Adversary Simulation"),
                ft.dropdown.Option(key=black_box_tag_uuid, text="Black Box"),
                ft.dropdown.Option(key=grey_box_tag_uuid, text="Grey Box"),
                ft.dropdown.Option(key=white_box_tag_uuid, text="White Box"),
            ],
            expand=True
        )

        self.app_state.service_tag_dropdown = service_tag_dropdown
        self.app_state.page.service_tag_dropdown = service_tag_dropdown

        generate_ai_summary_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SMART_TOY),
                        ft.Text("Ai Assistance", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: build_ai_management_summary_payload(e.page, e, test_uuid_text_field.value),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        save_test_details_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SAVE),
                        ft.Text("Save Changes", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: edit_details(e.page, e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        first_row = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=20,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.INDIGO_50,
                    expand=1,
                    padding=10,
                    content=ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            modify_test_details_text,
                            ft.Divider(),
                            ft.Row([test_uuid_text_field, load_test_uuid_button, servicenow_id_text_field], expand=True),
                            ft.Row([ connection_type_dropdown, service_tag_dropdown, testing_account_switch, account_role_text_field], expand=True),
                            management_summary_text_field,
                            ft.Row([generate_ai_summary_button, save_test_details_button, ft.Container(expand=True)])
                        ]
                    ),
                )
            ]
        )

        dummy_card = ft.Container(
            bgcolor=ft.Colors.INDIGO_50,
            border_radius=10,
            padding=20,
            content=ft.Column([
                first_row
            ])
        )

        return ft.Column([
            dummy_card
        ])
