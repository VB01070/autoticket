import flet as ft
import datetime
from utils import state
from utils.load_current_test_uuid import load_current_test_uuid
from presentation.presentation import main
from reporting.report import generate_report_html, generate_pdf, preview_pdf_in_memory
from reporting.utils.open_html_in_text_editor import open_html_in_text_editor


class ReportView:
    def __init__(self, app_state):
        self.app_state = app_state
        self.page = app_state.page

    def render(self):
        # === GENERATE PRESENTATION SECTION - START - ===

        presentation_text = ft.Text(
            "Generate Presentation",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )

        presentation_test_uuid_text_field = ft.CupertinoTextField(
            placeholder_text="Test UUID",
            filled=True,
            expand=True
        )

        self.app_state.presentation_test_uuid_text_field = presentation_test_uuid_text_field
        self.app_state.page.presentation_test_uuid_text_field = presentation_test_uuid_text_field

        presentation_load_test_uuid_button = ft.FilledTonalButton(
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
            on_click=lambda e: load_current_test_uuid(e.page, e, "presentation"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        def on_date_change(e, event_type):
            selected_date = e.control.value
            if selected_date:
                if event_type == "meeting":
                    state.selected_date_str = selected_date.strftime("%d-%m-%Y")
                    print(f"Selected date: {state.selected_date_str}")  # for debug
                    meeting_date_text.value = f"Meeting scheduled on {state.selected_date_str}"
                    meeting_date_text.update()
                elif event_type == "start_test":
                    state.selected_date_str = selected_date.strftime("%d-%m-%Y")
                    start_test = state.selected_date_str
                    self.app_state.start_test = start_test
                    self.app_state.page.start_test = start_test
                    start_test_date_text.value = f"Test started on {state.selected_date_str}"
                    start_test_date_text.color = ft.Colors.GREEN_800
                    start_test_date_text.update()
                elif event_type == "end_test":
                    state.selected_date_str = selected_date.strftime("%d-%m-%Y")
                    end_test = state.selected_date_str
                    self.app_state.end_test = end_test
                    self.app_state.page.end_test = end_test
                    end_test_date_text.value = f"Test ended on {state.selected_date_str}"
                    end_test_date_text.color = ft.Colors.GREEN_800
                    end_test_date_text.update()

        def open_date_picker(page, event_type):
            if event_type == "meeting":
                meeting_date_picker.open = True
            elif event_type == "start_test":
                start_test_date_picker.open = True
            elif event_type == "end_test":
                end_test_date_picker.open = True

            page.update()

        meeting_date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2025, month=1, day=1),
            on_change=lambda e: on_date_change(e, "meeting")
        )

        self.page.overlay.append(meeting_date_picker)

        pick_date_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CALENDAR_TODAY_OUTLINED),
                        ft.Text("Pick Meeting Date", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: open_date_picker(e.page, "meeting"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        meeting_date_text = ft.Text(
            " ",
            italic=True,
            theme_style=ft.TextThemeStyle.BODY_SMALL,
            weight=ft.FontWeight.BOLD,
        )

        generate_presentation_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.ANALYTICS_OUTLINED),
                        ft.Text("Generate pptx", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: main(e.page, e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        # === GENERATE PRESENTATION SECTION - END - ===

        # === GENERATE REPORTING SECTION - START - ===

        generate_report_text = ft.Text(
            "Generate Report",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
        )

        report_test_uuid_text_field = ft.TextField(
            label="Test UUID",
            filled=True
        )

        self.app_state.report_test_uuid_text_field = report_test_uuid_text_field
        self.app_state.page.report_test_uuid_text_field = report_test_uuid_text_field

        report_load_test_uuid_button = ft.FilledTonalButton(
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
            on_click=lambda e: load_current_test_uuid(e.page, e, "report"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        start_test_date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2025, month=1, day=1),
            on_change=lambda e: on_date_change(e, "start_test")
        )
        self.page.overlay.append(start_test_date_picker)

        start_test_pick_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CALENDAR_MONTH_OUTLINED),
                        ft.Text("Pick Test Starting Date", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: open_date_picker(e.page, "start_test"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        start_test_date_text = ft.Text(
            " ",
            italic=True,
            theme_style=ft.TextThemeStyle.BODY_SMALL,
            weight=ft.FontWeight.BOLD,
        )

        end_test_date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2025, month=1, day=1),
            on_change=lambda e: on_date_change(e, "end_test")
        )
        self.page.overlay.append(end_test_date_picker)

        end_test_pick_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CALENDAR_MONTH),
                        ft.Text("Pick Test Ending Date", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: open_date_picker(e.page, "end_test"),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        end_test_date_text = ft.Text(
            " ",
            italic=True,
            theme_style=ft.TextThemeStyle.BODY_SMALL,
            weight=ft.FontWeight.BOLD,
        )

        def on_service_change(e):
            service_selected = service_type_dropdown.value
            print(f"Selected testing type: {service_selected}")

        service_type_dropdown = ft.Dropdown(
            label="Service",
            hint_text="Select service...",
            on_change=on_service_change,
            filled=True,
            options=[
                ft.dropdown.Option("Adversary Simulation"),
                ft.dropdown.Option("Black Box"),
                ft.dropdown.Option("White Box"),
            ],
            expand=True
        )

        self.app_state.service_type_dropdown = service_type_dropdown
        self.app_state.page.service_type_dropdown = service_type_dropdown

        generate_html_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.TAG),
                        ft.Text("Generate HTML", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: generate_report_html(e.page),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        preview_html_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SETTINGS_ETHERNET_OUTLINED),
                        ft.Text("Open HTML in Text Editor", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: open_html_in_text_editor(e.page),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        def on_file_result(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                selected_path = e.files[0].path
                print(f"Selected HTML file: {selected_path}")
                html_path_text.value = selected_path
                html_file_path = selected_path
                self.page.update()

        file_picker = ft.FilePicker(on_result=on_file_result)
        self.page.overlay.append(file_picker)
        html_path_text = ft.Text(value=" ", selectable=True, italic=True, size=10,
                                     weight=ft.FontWeight.BOLD)

        self.app_state.html_path_text = html_path_text
        self.app_state.page.html_path_text = html_path_text

        select_file_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SELECT_ALL),
                        ft.Text("Select HTML File", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: file_picker.pick_files(allowed_extensions=["html"], allow_multiple=False),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        preview_pdf_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.PICTURE_AS_PDF_OUTLINED),
                        ft.Text("Preview PDF", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: preview_pdf_in_memory(e.page),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        generate_pdf_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.ADOBE),
                        ft.Text("Generate PDF", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: generate_pdf(e.page),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        # === GENERATE REPORTING SECTION - END - ===

        presentation_container = ft.Container(
            expand=True,
            bgcolor=ft.Colors.INDIGO_50,
            border_radius=10,
            padding=20,
            content=ft.Column([
                presentation_text,
                ft.Divider(),
                ft.Row(
                    [presentation_test_uuid_text_field, presentation_load_test_uuid_button, pick_date_button,
                     generate_presentation_button],
                    expand=True
                ),
                meeting_date_text
            ])
        )

        reporting_container = ft.Container(
            expand=True,
            bgcolor=ft.Colors.INDIGO_50,
            border_radius=10,
            padding=20,
            content=ft.Column([
                generate_report_text,
                ft.Divider(),
                ft.Row(
                    [report_test_uuid_text_field, service_type_dropdown, report_load_test_uuid_button,
                     start_test_pick_button, end_test_pick_button],
                    expand=True
                ),
                ft.Row(
                    [generate_html_button, preview_html_button, select_file_button, preview_pdf_button, generate_pdf_button]
                ),
                start_test_date_text, end_test_date_text
            ])
        )

        return ft.Column([
            presentation_container,
            reporting_container
        ])
