import flet as ft
from utils.caching import load_cache

records = []
filtered_records = []


def load_and_flatten_cache():
    cache = load_cache()
    new_records = []
    for ctx in cache["contexts"]:
        ctx_uuid = ctx["uuid"]
        ctx_name = ctx["name"]
        for vt in cache["vuln_types"].get(ctx_uuid, []):
            new_records.append({
                "Vulnerability Type": vt.get("display_name") or vt["name"],
                "Context": ctx_name,
                "Has Template": "Yes" if vt.get("template_text") else "No",
                "Template Text": vt.get("template_text", ""),
                "UUID": vt["uuid"]
            })
    return new_records


def update_table(page):
    global records, filtered_records

    cache = load_cache()
    records = []
    for ctx in cache["contexts"]:
        ctx_uuid = ctx["uuid"]
        ctx_name = ctx["name"]
        for vt in cache["vuln_types"].get(ctx_uuid, []):
            records.append({
                "Vulnerability Type": vt.get("display_name") or vt["name"],
                "Context": ctx_name,
                "Has Template": "Yes" if vt.get("template_text") else "No",
                "Template Text": vt.get("template_text", ""),
                "UUID": vt["uuid"]
            })

    filtered_records = records.copy()
    total_pages = (len(filtered_records) + page.rows_per_page - 1) // page.rows_per_page
    page.result_count.value = f"Total Vuln Types: {len(filtered_records)}"
    page.result_count.update()

    page.table_types_templates.rows.clear()
    start = page.current_page * page.rows_per_page
    end = start + page.rows_per_page
    for record in filtered_records[start:end]:
        def make_button(template):
            if isinstance(template, dict):
                valid = any(template.get(k) for k in ["description", "impact", "recommendation"])
            elif isinstance(template, str):
                valid = bool(template.strip())
            else:
                valid = False

            return ft.ElevatedButton(
                "View Template",
                on_click=lambda e: show_template(page.app_state, template),  # Access app_state to show dialog
                disabled=not valid
            )

        page.table_types_templates.rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(record["Vulnerability Type"])),
                ft.DataCell(ft.Text(record["Context"])),
                ft.DataCell(ft.Text(record["Has Template"])),
                ft.DataCell(make_button(record["Template Text"])),
            ])
        )

    page.update()
    print("[DEBUG] Table update complete.")


def show_template(app_state, template):  # Expect app_state
    print("[DEBUG] show_template called")

    if isinstance(template, dict):
        content = []
        if template.get("description"):
            content.append(f"## Description\n\n{template['description']}")
        if template.get("impact"):
            content.append(f"## Impact\n\n{template['impact']}")
        if template.get("recommendation"):
            content.append(f"## Recommendation\n\n{template['recommendation']}")
        full_text = "\n\n".join(content).strip()
    else:
        full_text = template.strip() or "No template available."

    dialog = app_state.template_dialog
    # swap out the old content with a fresh Markdown control
    dialog.content = ft.Column(
        [ft.Markdown(full_text)],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    dialog.open = True

    # update the page
    app_state.page.update()


def close_dialog(app_state, dialog):  # Expect app_state
    print("[DEBUG] Dialog closed")
    dialog.open = False
    app_state.page.update()


def filter_table(view: 'CacheView', query):  # Expect CacheView instance
    query = query.strip().lower()
    filtered = []
    if query:
        filtered = [r for r in view.vuln_type_template_records if query in r["Vulnerability Type"].lower()]
        view.result_count.value = f"Results: {len(filtered)}"
    else:
        filtered = view.vuln_type_template_records

    view.filtered_records = filtered

    total_pages = (len(filtered) + view.rows_per_page - 1) // view.rows_per_page
    view.table_types_templates.rows.clear()
    start_index = view.current_page * view.rows_per_page
    end_index = start_index + view.rows_per_page
    for record in view.filtered_records[start_index:end_index]:
        btn = ft.FilledTonalButton(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.VISIBILITY),
                        ft.Text("View", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2
                )
            ),
            on_click=lambda e, tmpl=record["Template Text"]: show_template(view.app_state, tmpl),
            disabled=not bool(record["Template Text"]),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.HOVERED: ft.Colors.BLUE_300,
                    ft.ControlState.DEFAULT: ft.Colors.WHITE10
                }
            )
        )

        view.table_types_templates.rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(record["Vulnerability Type"], size=12)),
            ft.DataCell(ft.Text(record["Context"], size=12)),
            ft.DataCell(ft.Text(record["Has Template"], size=12)),
            ft.DataCell(ft.Container(btn, alignment=ft.alignment.center_left))
        ]))

    view.result_count.update()
    view.table_types_templates.update()
    view.update_navigation()