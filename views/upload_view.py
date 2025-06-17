import flet as ft
import os
from utils.caching import CACHE_PATH
from handlers.upload.download_template import download_template
from handlers.upload.populate_vulns_dropdown import populate_vulns_dropdown
from handlers.upload.images_handler import previous_image, next_image
from handlers.upload.placeholder_b64 import placeholder_b64
from handlers.upload.ai_handler import ai_assistance, edit_ai_suggestion, save_ai_suggestion
from handlers.upload.payload_handler import view_payload
from handlers.upload.upload_handler import upload_vulnerability
from handlers.upload.display_finding import previous_vuln, next_vuln
from handlers.upload.document_handler import load_local_document, on_browse
from handlers.upload.cvss_handler import open_cvss_calculator_dialog



class UploadView:
    def __init__(self, app_state):
        self.app_state = app_state
        self.page = app_state.page

    def render(self):
        # ==  TOP ROW START ==
        def on_vuln_type_change(e):
            selected_uuid = e.control.value
            if not selected_uuid:
                return

            # look up the display name & context UUID you stored earlier
            info = self.app_state.vuln_type_map_by_uuid[selected_uuid]
            display = info["display"]
            context_uuid = info["context_uuid"]

            # update the read-only text field
            self.app_state.vuln_types_text.value = display
            self.app_state.vuln_types_text.update()

            # store into your master lists
            idx = self.app_state.current_finding_index

            # 1) override the matched_vuln_types entry
            if idx < len(self.app_state.matched_vuln_types):
                self.app_state.matched_vuln_types[idx] = {
                    "name": display,
                    "vuln_type_uuid": selected_uuid,
                    "context_uuid": context_uuid,
                    "confidence": 1.0
                }

            # override the vuln_type_uuids entry that your payload builder reads
            # make sure the list exists already at least as long as findings
            if not hasattr(self.app_state, "vuln_type_uuids"):
                # initialize with blanks if somehow missing
                self.app_state.vuln_type_uuids = [
                    {"vuln_type": None, "context": None}
                    for _ in self.app_state.findings
                ]

            self.app_state.vuln_type_uuids[idx] = {
                "vuln_type": selected_uuid,
                "context": context_uuid
            }

            # update your state tracking too
            self.app_state.vuln_type_uuid = selected_uuid
            self.app_state.vuln_type_context_uuid = context_uuid

        has_cache = os.path.exists(CACHE_PATH)

        vuln_types_dropdown = ft.Dropdown(
            label="Vulnerability Types",
            hint_text="Select type...",
            on_change=on_vuln_type_change,
            options=[],
            disabled=False,
            enable_filter=True,
            editable=True,
            # enable_search=True,
            width=400,
            dense=True,
            text_size=10,
            border_color=ft.Colors.BLUE_GREY_400,
            focused_border_color=ft.Colors.BLUE_400,
            filled=True,
            bgcolor=ft.Colors.BLUE_GREY_50,
            expand=True
        )

        self.app_state.vuln_types_dropdown = vuln_types_dropdown
        self.app_state.page.vuln_types_dropdown = vuln_types_dropdown

        download_file_picker = ft.FilePicker(on_result=lambda e, page=self.app_state.page: download_template(e, page))
        self.app_state.page.overlay.append(download_file_picker)

        download_note_template_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.DOWNLOAD_FOR_OFFLINE),
                        ft.Text("Download Note template", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda _: download_file_picker.get_directory_path(),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.TEAL_ACCENT_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        load_note_local_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.STORAGE_OUTLINED),
                        ft.Text("Load Note", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: load_local_document(page=e.page, e=e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            ),
            disabled=not has_cache
        )

        self.app_state.load_note_local_button = load_note_local_button
        self.app_state.page.load_note_local_button = load_note_local_button

        load_note_drive_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CLOUD_UPLOAD),
                        ft.Text("Load Note Drive", size=12)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e: on_browse(page=e.page, e=e),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            ),
            # disabled=not has_cache
            disabled=True
        )

        self.app_state.load_note_drive_button = load_note_drive_button
        self.app_state.page.load_note_drive_button = load_note_drive_button

        vuln_types_text = ft.CupertinoTextField(
            placeholder_text="AI Vulnerability Types",
            placeholder_style=ft.TextStyle(color=ft.Colors.GREY_400),
            read_only=True
        )

        self.app_state.vuln_types_text = vuln_types_text
        self.app_state.page.vuln_types_text = vuln_types_text

        # building TOP ROW

        top_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                    vuln_types_dropdown,
                    vuln_types_text,
                ]),
                ft.Container(expand=True),
                load_note_local_button,
                load_note_drive_button,
                download_note_template_button
            ]
        )

        # ==  TOP ROW END ==
        # == NOTE ROW START ==

        document_content = ft.TextField(
            value="Document content will appear here",
            multiline=True,
            read_only=True,
            min_lines=13,
            max_lines=13,
            border_radius=10,
            filled=True,
            expand=True,
            text_align=ft.TextAlign.LEFT,
            text_style=ft.TextStyle(size=15),
            bgcolor=ft.Colors.SURFACE,
        )
        self.app_state.document_content = document_content
        self.app_state.page.document_content = document_content

        image_preview_text = ft.Text("Image Preview", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)

        placeholder_b64_image = placeholder_b64()

        image_preview = ft.Image(
            src_base64=placeholder_b64_image,
            width=300,
            height=200,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(5)
        )
        self.app_state.image_preview = image_preview
        self.app_state.page.image_preview = image_preview

        prev_image_button = ft.IconButton(
            icon=ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED,
            on_click=lambda e: previous_image(page=e.page, e=e),
            disabled=True,
            tooltip="Previous Image",
            hover_color=ft.Colors.ORANGE_ACCENT_100,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.BROWN_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        self.app_state.prev_image_button = prev_image_button
        self.app_state.page.prev_image_button = prev_image_button

        next_image_button = ft.IconButton(
            icon=ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED,
            on_click=lambda e: next_image(page=e.page, e=e),
            disabled=True,
            tooltip="Next Image",
            hover_color=ft.Colors.ORANGE_ACCENT_100,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.BROWN_100,
                    ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                }
            )
        )

        self.app_state.next_image_button = next_image_button
        self.app_state.page.next_image_button = next_image_button

        # building NOTE ROW

        note_row = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        document_content,
                    ],
                    expand=3,
                    spacing=5,
                    scroll=ft.ScrollMode.AUTO
                ),
                ft.Column(
                    expand=1,
                    spacing=5,
                    alignment=ft.alignment.top_center,
                    controls=[
                        ft.Container(
                            padding=5,
                            expand=1,
                            border=ft.border.all(1, ft.Colors.BLACK38),
                            border_radius=10,
                            content=ft.Column(
                                spacing=5,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    image_preview_text,
                                    ft.Divider(),
                                    image_preview,
                                    ft.Row(
                                        controls=[prev_image_button, next_image_button],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ]
                            )
                        )
                    ]
                )
            ]
        )
        # == NOTE ROW END ==
        # == CONTROLS ROW START ==

        ai_assistance_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SMART_TOY),
                        ft.Text("AI Assistance", size=12),
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
            on_click=lambda e: ai_assistance(page=e.page, e=e),
            disabled=True
        )

        self.app_state.ai_assistance_button = ai_assistance_button
        self.app_state.page.ai_assistance_button = ai_assistance_button

        view_payload_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.DATA_OBJECT),
                        ft.Text("View Payload", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.YELLOW_100,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE10
                }
            ),
            on_click=lambda e: view_payload(page=e.page, e=e),
            disabled=True
        )

        self.app_state.view_payload_button = view_payload_button
        self.app_state.page.view_payload_button = view_payload_button

        upload_vuln_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.PUBLISH),
                        ft.Text("Upload", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_ACCENT_100,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE10
                }
            ),
            on_click=lambda e: upload_vulnerability(page=e.page, e=e),
            disabled=True
        )

        self.app_state.upload_vuln_button = upload_vuln_button
        self.app_state.page.upload_vuln_button = upload_vuln_button

        upload_all_vulns_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.UPLOAD),
                        ft.Text("Upload All", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_ACCENT_100,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE10
                }
            ),
            on_click=lambda e: upload_vulnerability(page=e.page, e=e),
            disabled=True
        )

        self.app_state.upload_all_vulns_button = upload_all_vulns_button
        self.app_state.page.upload_all_vulns_button = upload_all_vulns_button

        edit_ai_content_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.EDIT_NOTE),
                        ft.Text("Edit AI Content", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.ORANGE_100,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE10
                }
            ),
            on_click=lambda e: edit_ai_suggestion(page=e.page, e=e),
            disabled=True
        )

        self.app_state.edit_ai_content_button = edit_ai_content_button
        self.app_state.page.edit_ai_content_button = edit_ai_content_button

        save_ai_content_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.SAVE),
                        ft.Text("Save AI Content", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_100,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE10
                }
            ),
            on_click=lambda e: save_ai_suggestion(page=e.page, e=e),
            disabled=True
        )

        self.app_state.save_ai_content_button = save_ai_content_button
        self.app_state.page.save_ai_content_button = save_ai_content_button

        previous_vulns_button = ft.IconButton(
            icon=ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED,
            on_click=lambda e: previous_vuln(page=e.page, e=e),
            disabled=True,
            tooltip="Previous Note",
            hover_color=ft.Colors.BROWN_100,
        )

        self.app_state.previous_vulns_button = previous_vulns_button
        self.app_state.page.previous_vulns_button = previous_vulns_button

        next_vulns_button = ft.IconButton(
            icon=ft.Icons.ARROW_CIRCLE_RIGHT_OUTLINED,
            on_click=lambda e: next_vuln(page=e.page, e=e),
            disabled=True,
            tooltip="Next Note",
            hover_color=ft.Colors.BROWN_100,
        )

        self.app_state.next_vulns_button = next_vulns_button
        self.app_state.page.next_vulns_button = next_vulns_button

        controls_row = ft.Row(
            controls=[
                ai_assistance_button,
                view_payload_button,
                # upload_vuln_button,
                upload_all_vulns_button,
                edit_ai_content_button,
                save_ai_content_button,
                ft.Container(expand=True),
                previous_vulns_button,
                next_vulns_button,
                ft.Container(expand=True),

            ]
        )

        # == CONTROLS ROW END ==

        # == AI-CVSS  ROW START ==

        ai_content_editable = ft.TextField(
            value="AI Document content will appear here - EDITABLE",
            multiline=True,
            read_only=True,
            min_lines=11,
            max_lines=11,
            border_radius=10,
            filled=True,
            expand=True,
            text_align=ft.TextAlign.LEFT,
            text_style=ft.TextStyle(size=12),
            bgcolor=ft.Colors.SURFACE,
        )

        self.app_state.ai_content_editable = ai_content_editable
        self.app_state.page.ai_content_editable = ai_content_editable

        cvss_title_text = ft.Text("CVSS4/Severity", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)

        cvss_calculator_button = ft.FilledTonalButton(
            content=ft.Container(
                padding=ft.Padding(0, 0, 0, 0),
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CALCULATE_OUTLINED),
                        ft.Text("Open CVSS Calculator", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.GREEN_100,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE10
                }
            ),
            on_click=lambda e: open_cvss_calculator_dialog(page=e.page, e=e),
            disabled=False
        )

        cvss_text = ft.Text("", size=10, italic=True, selectable=True)

        self.app_state.cvss_text = cvss_text
        self.app_state.page.cvss_text = cvss_text

        severity_text = ft.Text("", size=10, italic=True)

        self.app_state.severity_text = severity_text
        self.app_state.page.severity_text = severity_text

        cvss_dialog  = ft.AlertDialog(
            modal=True,
            title=ft.Text("CVSS v4.0 Base Score Calculator"),
        )

        self.app_state.cvss_dialog  = cvss_dialog
        self.app_state.page.cvss_dialog  = cvss_dialog

        # build AI Row

        ai_row = ft.Row(
            controls=[
                ft.Column(
                    expand=3,
                    spacing=5,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[ai_content_editable]
                ),
                ft.Column(
                    expand=1,
                    spacing=5,
                    alignment=ft.alignment.top_center,
                    controls=[
                        ft.Container(
                            padding=10,
                            expand=1,
                            border_radius=10,
                            border=ft.border.all(1, ft.Colors.BLACK38),
                            content=ft.Column(
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    cvss_title_text,
                                    ft.Divider(),
                                    cvss_calculator_button,
                                    ft.Row(
                                        controls=[
                                            ft.Text("CVSS: ", size=10, weight=ft.FontWeight.BOLD),
                                            cvss_text
                                        ]
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Text("Severity: ", size=10, weight=ft.FontWeight.BOLD),
                                            severity_text
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            ]
        )

        # == AI ROW END ==



        dummy_card = ft.Container(
            bgcolor=ft.Colors.INDIGO_50,
            border_radius=10,
            padding=20,
            content=ft.Column([
                top_row,
                note_row,
                controls_row,
                ai_row
            ])
        )

        if self.app_state.cache.get("vuln_types"):
            populate_vulns_dropdown(self.app_state)

        return ft.Column([
            dummy_card,
            cvss_dialog
        ])
