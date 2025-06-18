import flet as ft
from handlers.manage.publish_vuln import publish_selected_vulns
import webbrowser
from logs.logger import logger

base_link_url = "https://randstad.eu.vulnmanager.com/vulnerabilities"


def render_vuln_table(page, vuln_data):
    if not hasattr(page, 'app_state'):
        logger.error("page.app_state is not initialized.")
        return

    page.app_state.selected_vuln_uuids = set()
    page.app_state.vuln_checkboxes = {}

    def on_checkbox_change(e, uuid):
        if e.control.value:
            page.app_state.selected_vuln_uuids.add(uuid)
        else:
            page.app_state.selected_vuln_uuids.discard(uuid)

        all_checked = len(page.app_state.vuln_checkboxes) > 0 and all(cb.value for cb in page.app_state.vuln_checkboxes.values())
        page.app_state.select_all_checkbox.value = all_checked
        page.update()

    def on_select_all_change(e):
        checked = e.control.value
        for uuid, cb in page.app_state.vuln_checkboxes.items():
            cb.value = checked
            if checked:
                page.app_state.selected_vuln_uuids.add(uuid)
            else:
                page.app_state.selected_vuln_uuids.discard(uuid)
        page.update()

    if not hasattr(page.app_state, 'vuln_table_container') or not isinstance(page.app_state.vuln_table_container,
                                                                             ft.Container):
        logger.error("page.app_state.vuln_table_container is not initialized as an ft.Container.")
        return

    if not vuln_data:
        page.app_state.vuln_table_container.content = ft.Text("No vulnerabilities found.")
        page.update()
        return

    page.app_state.select_all_checkbox = ft.Checkbox(label=" ", value=False, on_change=on_select_all_change)
    page.app_state.publish_selected_button = ft.IconButton(
        tooltip="Publish Selected Vulnerabilities",
        icon=ft.Icons.PUBLISH,
        on_click=lambda e: publish_selected_vulns(page),
        hover_color=ft.Colors.ORANGE_ACCENT_100,
    )

    rows = []
    for vuln in vuln_data:
        uuid = vuln["uuid"]
        checkbox = ft.Checkbox(
            value=False,
            on_change=lambda e, uuid=uuid: on_checkbox_change(e, uuid)
        )
        page.app_state.vuln_checkboxes[uuid] = checkbox
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(checkbox),
                    ft.DataCell(
                        ft.TextButton(
                            text=str(vuln.get("id", "-")),
                            on_click=lambda e, uuid=uuid: webbrowser.open(f"{base_link_url}/{uuid}/show"),
                            style=ft.ButtonStyle(padding=0)
                        )
                    ),
                    ft.DataCell(ft.Text(vuln.get("severity", "-"))),
                    ft.DataCell(ft.Text(vuln.get("state", "-"))),
                    ft.DataCell(ft.Text(vuln.get("description", "-")[:80])),
                ]
            )
        )

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Row([page.app_state.select_all_checkbox])),
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Severity")),
            ft.DataColumn(ft.Text("State")),
            ft.DataColumn(ft.Text("Title")),
        ],
        rows=rows,
        heading_row_color=ft.Colors.BLUE_GREY_50,
        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
        column_spacing=15,
        horizontal_lines=ft.BorderSide(1, ft.Colors.BLUE_GREY_100),
    )

    page.app_state.vuln_table_container.content = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[
                ft.Container(
                    content=data_table,
                    padding=0,
                    expand=True,
                )
            ],
            expand=True,
            spacing=10,
            padding=0,
            auto_scroll=False,
        ),
        padding=10,
        border=ft.border.all(1, ft.Colors.BLUE_GREY_200),
        bgcolor=ft.Colors.WHITE,
    )

    page.update()

