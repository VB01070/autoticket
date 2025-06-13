import flet as ft
import webbrowser

base_link_url = "https://randstad.eu.vulnmanager.com/vulnerabilities"


def render_migration_table(page, vuln_data):
    page.app_state.migration_selected_uuids = set()
    page.app_state.migration_checkboxes = {}
    page.app_state.migration_dropdowns = {}

    def on_checkbox_change(e, uuid):
        if e.control.value:
            page.app_state.migration_selected_uuids.add(uuid)
        else:
            page.app_state.migration_selected_uuids.discard(uuid)
        all_checked = len(page.app_state.migration_checkboxes) > 0 and all(cb.value for cb in page.app_state.migration_checkboxes.values())
        page.app_state.migration_select_all_checkbox.value = all_checked
        page.update()

    def on_select_all_change(e):
        checked = e.control.value
        for uuid, cb in page.app_state.migration_checkboxes.items():
            cb.value = checked
            if checked:
                page.app_state.migration_selected_uuids.add(uuid)
            else:
                page.app_state.migration_selected_uuids.discard(uuid)
        page.update()

    if not vuln_data:
        page.app_state.migration_table_container.content = ft.Text("No vulnerabilities found.")
        page.update()
        return

    page.app_state.migration_select_all_checkbox = ft.Checkbox(label=" ", value=False, on_change=on_select_all_change)

    rows = []
    for vuln in vuln_data:
        uuid = vuln["uuid"]
        checkbox = ft.Checkbox(value=False, on_change=lambda e, uuid=uuid: on_checkbox_change(e, uuid))
        page.app_state.migration_checkboxes[uuid] = checkbox

        dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option(text="Network", key="95cbe2a6-6b77-4919-92a0-52ce5fa30518"),
                ft.dropdown.Option(text="Windows", key="a5fc6cc6-3d9a-4e76-b525-1b854c7e2f49"),
                ft.dropdown.Option(text="Zscaler", key="385df8a9-6185-47d8-b422-17e77f3d7a65"),
            ],
            width=150
        )
        page.app_state.migration_dropdowns[uuid] = dropdown

        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(checkbox),
                    ft.DataCell(
                        ft.TextButton(
                            text=str(vuln.get("id", "-")),
                            on_click=lambda e, uuid=uuid: webbrowser.open(f"{base_link_url}/{uuid}/show"),
                            style=ft.ButtonStyle(padding=0),
                        )
                    ),
                    ft.DataCell(ft.Text(vuln.get("severity", "-"))),
                    ft.DataCell(ft.Text(vuln.get("state", "-"))),
                    ft.DataCell(ft.Text(vuln.get("description", "-")[:80])),
                    ft.DataCell(dropdown),
                ]
            )
        )

    page.app_state.migration_table_container.content = ft.Container(
        expand=True,
        content=ft.ListView(
            controls=[
                ft.Container(content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Row([page.app_state.migration_select_all_checkbox])),
                        ft.DataColumn(ft.Text("ID")),
                        ft.DataColumn(ft.Text("Severity")),
                        ft.DataColumn(ft.Text("State")),
                        ft.DataColumn(ft.Text("Title")),
                        ft.DataColumn(ft.Text("GIS Asset")),
                    ],
                    rows=rows,
                    heading_row_color=ft.colors.BLUE_GREY_50,
                    border=ft.border.all(1, ft.colors.BLUE_GREY_100),
                    column_spacing=15,
                    horizontal_lines=ft.BorderSide(1, ft.colors.BLUE_GREY_100),
                ))
            ],
            expand=True,
            spacing=10,
            padding=0,
            auto_scroll=False,
        ),
        padding=10,
        border=ft.border.all(1, ft.colors.BLUE_GREY_200),
        bgcolor=ft.colors.WHITE,
    )
    page.update()
