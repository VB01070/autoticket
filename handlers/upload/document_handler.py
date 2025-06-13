import flet as ft
import os
from flet import FilePicker, FilePickerResultEvent
from utils.parser import parse_findings
from utils.drive_utils import list_folder, download_file_as_docx
from handlers.upload.display_finding import display_finding
from handlers.upload.vuln_type_matcher import match_vuln_titles_to_cache


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_PATH = 'token.pickle'


def load_local_document(page, e):
    def on_file_selected(event: FilePickerResultEvent):
        if not event.files:
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.CLOSE, color=ft.Colors.WHITE),
                    ft.Text("Document selection cancelled", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.ORANGE_300
            page.snack_bar.open = True
            page.update()

        file_path = event.files[0].path
        try:
            page.app_state.findings, page.app_state.metadata = parse_findings(file_path)
            if not page.app_state.findings:
                page.snack_bar.content = ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CONTENT_PASTE_OFF, color=ft.Colors.WHITE),
                        ft.Text("No findings found in that document.", size=14)
                    ]
                )
                page.snack_bar.bgcolor = ft.Colors.ORANGE_300
                page.snack_bar.open = True
                page.update()

            # print(f"[DEBUG] {page.app_state.findings}")
            page.app_state.matched_vuln_types = match_vuln_titles_to_cache(page.app_state.findings, page.app_state.cache)

            # map UUIDs with findings
            vuln_type_uuids = []
            for match in page.app_state.matched_vuln_types:
                if match:
                    vuln_type_uuids.append({
                        "vuln_type": match["vuln_type_uuid"],
                        "context": match["context_uuid"]
                    })
                else:
                    vuln_type_uuids.append({
                        "vuln_type": None,
                        "context": None
                    })

            page.app_state.vuln_type_uuids = vuln_type_uuids
            # reset index and metadata
            page.app_state.current_finding_index = 0
            page.app_state.org_uuid = page.app_state.metadata.get("org", "")
            page.app_state.asset_uuid = page.app_state.metadata.get("asset", "")
            page.app_state.test_uuid = page.app_state.metadata.get("test", "")

            # enable the nav buttons
            page.app_state.previous_vulns_button.disabled = True
            page.app_state.next_vulns_button.disabled = len(page.app_state.findings) == 1

            display_finding(page)

        except Exception as ex:
            print(ex)
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.WHITE),
                    ft.Text(f"Failed to load document. Error: {ex}", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.RED_400
            page.snack_bar.open = True
            page.update()

    if not hasattr(page, "local_file_picker"):
        page.app_state.local_file_picker = FilePicker()
        page.overlay.append(page.app_state.local_file_picker)
        page.update()

    page.app_state.local_file_picker.on_result = on_file_selected
    page.app_state.local_file_picker.pick_files(
        dialog_title="Select document",
        allowed_extensions=["docx"],
        allow_multiple=False
    )

    page.app_state.previous_vulns_button.disabled = False
    page.app_state.next_vulns_button.disabled = False
    page.update()


def on_browse(page, e):
    print("[DEBUG] on_browse called")

    page.app_state.current_folder = "1LvaID3TriOjpgrqBHkCKk6niC6tJfJLt"
    page.app_state.folder_stack = []

    def load_drive_folder(page):
        print("[DEBUG] load_drive_folder start")
        page.app_state.drive_table.rows.clear()
        try:
            page.app_state.current_items = list_folder(page.app_state.current_folder)
            print(f"[DEBUG] Got {len(page.app_state.current_items)} items from Drive")
        except Exception as e:
            print(f"[ERROR] Drive Error: {e}")
            page.snack_bar.content = ft.Text(f"Drive Error: {e}")
            page.snack_bar.bgcolor = ft.Colors.RED_400
            page.snack_bar.open = True
            page.update()

            return

        for idx, item in enumerate(page.app_state.current_items):
            name = item['name']
            is_folder = item['mimeType'] == 'application/vnd.google-apps.folder'

            page.app_state.drive_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.icons.FOLDER if is_folder else ft.icons.DESCRIPTION,
                                        color=ft.Colors.BLUE if is_folder else ft.Colors.GREY_600,
                                        size=20
                                    ),
                                    ft.Text(name),
                                ],
                                spacing=10,
                            ),
                            on_tap=(lambda index: (lambda e: handle_row_click(page, index)))(idx),
                        ),
                        ft.DataCell(ft.Text("Folder" if is_folder else "Google Doc")),

                    ],
                    data=idx,
                )
            )

        print("[DEBUG] Rows added to table")
        page.app_state.drive_table.expand = True  # makes the table stretch to max width
        page.update()
        print("[DEBUG] Page updated after loading")

    # === Define button handlers ===
    def handle_back_click(e):
        if page.app_state.folder_stack:
            page.app_state.current_folder = page.app_state.folder_stack.pop()
            page.app_state._last_clicked_folder = None
            load_drive_folder(page)

    def handle_close_click(e):
        page.app_state._last_clicked_folder = None
        page.dialog.open = False
        page.update()

    def handle_row_click(page, index):
        item = page.app_state.current_items[index]
        mime = item["mimeType"]

        # --- 1) Folders: debounce double‐taps ---
        if mime == "application/vnd.google-apps.folder":
            new_folder = item["id"]
            # if we just loaded this same folder, ignore
            if getattr(page.app_state, "_last_clicked_folder", None) == new_folder:
                return
            # otherwise remember it and navigate in
            page.app_state._last_clicked_folder = new_folder
            page.app_state.folder_stack.append(page.app_state.current_folder)
            page.app_state.current_folder = new_folder
            load_drive_folder(page)
            return

        # --- 2) Docs: clear the debounce guard and process file ---
        if mime == "application/vnd.google-apps.document":
            # clear the folder‐click guard so next folder click works
            page.app_state._last_clicked_folder = None

            # download to your project folder
            local_path = os.path.join(
                page.app_state.project_folder,
                f"{item['name']}.docx"
            )
            try:
                download_file_as_docx(item["id"], local_path)

                # show success
                page.snack_bar.content = ft.Text(f"Downloaded: {local_path}")
                page.snack_bar.bgcolor = ft.Colors.GREEN_400
                page.snack_bar.open = True

                # parse & match
                page.app_state.findings, page.app_state.metadata = parse_findings(local_path)
                page.app_state.matched_vuln_types = match_vuln_titles_to_cache(
                    page.app_state.findings,
                    page.app_state.cache
                )

                page.app_state.vuln_type_uuids = [
                    {"vuln_type": m["vuln_type_uuid"], "context": m["context_uuid"]}
                    if m else {"vuln_type": None, "context": None}
                    for m in page.app_state.matched_vuln_types
                ]
                # reset AI state
                page.app_state.ai_suggestions = [None] * len(page.app_state.findings)

                # reset nav buttons
                page.app_state.previous_vulns_button.disabled = True
                page.app_state.next_vulns_button.disabled = (len(page.app_state.findings) == 1)

                # show the first finding
                display_finding(page)

                # close the dialog
                page.dialog.open = False

            except Exception as ex:
                print(ex)
                page.snack_bar.content = ft.Text(f"Download Failed: {ex}")
                page.snack_bar.bgcolor = ft.Colors.RED_400
                page.snack_bar.open = True

            # finally, update the UI
            page.update()
            return

    page.app_state.drive_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Type")),
        ],
        rows=[],
        width=500,
        column_spacing=20,
        heading_row_height=50,
        divider_thickness=1,
    )

    table_container = ft.Container(
        content=page.app_state.drive_table,
        width=520,
        height=400,
        padding=10,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 2),
        ),
    )

    page.app_state.drive_dialog = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(ft.Icons.FOLDER, color=ft.Colors.AMBER),
            ft.Text("Browse Google Drive", size=22, weight="bold"),
        ], spacing=10),
        content=ft.Column([
            table_container,
            ft.Row([
                ft.ElevatedButton("⬅ Back", on_click=handle_back_click, bgcolor=ft.Colors.BLUE_100,
                                  color=ft.Colors.BLUE_900),
                ft.ElevatedButton("❌ Cancel", on_click=handle_close_click, bgcolor=ft.Colors.RED_100,
                                  color=ft.Colors.RED_900),
            ], alignment=ft.MainAxisAlignment.END, tight=True)
        ],
            spacing=20,
            expand=True),
        modal=True
    )

    page.overlay.append(page.app_state.drive_dialog)
    page.dialog = page.app_state.drive_dialog
    page.dialog.open = True
    page.update()
    print("[DEBUG] Dialog created and opened")

    # === Load folder content ===
    page.app_state._last_clicked_folder = None
    load_drive_folder(page)
