import flet as ft
import json
from utils.payload_builder import build_payload
from handlers.upload.ai_editable import parse_editable_ai
from logs.logger import logger


def view_payload(page, e):
    logger.debug("View Payload clicked")

    # Build the payload dynamically
    finding = page.app_state.findings[page.app_state.current_finding_index]
    logger.debug("Finding loaded")
    ai_raw = page.app_state.ai_suggestions[page.app_state.current_finding_index]
    ai_edit = page.app_state.ai_suggestions_editable[page.app_state.current_finding_index]
    cvss_data = page.app_state.cvss_data[page.app_state.current_finding_index]

    # If edited version is a non-empty string (i.e., user edited), parse it as structured AI data
    if ai_edit and isinstance(ai_edit, str):
        try:
            ai_data = parse_editable_ai(ai_edit)
        except Exception as ex:
            logger.exception(f"Failed to parse editable AI text: {ex}")
            ai_data = ai_raw  # fallback to original AI data
    else:
        ai_data = ai_raw

    logger.debug("AI data loaded")
    uuids = {
        "asset": page.app_state.asset_uuid,
        "vuln_type": page.app_state.vuln_type_uuids[page.app_state.current_finding_index]["vuln_type"],
        "context": page.app_state.vuln_type_uuids[page.app_state.current_finding_index]["context"],
        "test": page.app_state.test_uuid,
    }
    logger.debug(f"UUIDs: {uuids}")
    payload = build_payload(finding, ai_data, uuids, cvss_data, vuln_type_name=None)
    logger.debug("Payload built")
    # Convert to pretty JSON
    payload_json = json.dumps(payload, indent=4)
    # Create a scrollable text box with copy button
    payload_text = ft.TextField(
        value=payload_json,
        multiline=True,
        read_only=True,
        min_lines=30,
        max_lines=50,
        expand=True,
        text_size=12
    )

    def copy_payload(e):
        page.set_clipboard(payload_json)
        page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.CHECK_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text("Payload copied to clipboard!", size=14)
                ]
            )
        page.snack_bar.bgcolor = ft.Colors.GREEN_400
        page.snack_bar.open = True
        page.update()

    dialog_payload = ft.AlertDialog(
        title=ft.Text("Payload Preview"),
        bgcolor=ft.Colors.INDIGO_50,
        content=ft.Container(
            width=700,
            content=ft.Column([
                payload_text,
                ft.Row([
                    ft.FilledTonalButton(
                        content=ft.Container(
                            padding=ft.Padding(0, 0, 0, 0),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.COPY_ALL),
                                    ft.Text("Copy to Clipboard", size=12)

                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=2
                            )
                        ),
                        on_click=copy_payload,
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.ControlState.HOVERED: ft.Colors.BLUE_100,
                                ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                            }
                        )
                    ),
                    ft.FilledTonalButton(
                        content=ft.Container(
                            padding=ft.Padding(0, 0, 0, 0),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.CLOSE),
                                    ft.Text("Close", size=12)

                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=2
                            )
                        ),
                        on_click=lambda e: close_dialog_payload(page),
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.ControlState.HOVERED: ft.Colors.RED_100,
                                ft.ControlState.DEFAULT: ft.Colors.INDIGO_50
                            }
                        )
                    ),
                ], alignment=ft.MainAxisAlignment.END),
            ], spacing=10)
        ),
        modal=True
    )

    page.overlay.append(dialog_payload)

    page.dialog = dialog_payload
    page.dialog.open = True
    page.update()


def close_dialog_payload(page):
    page.dialog.open = False
    page.update()