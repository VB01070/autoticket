import flet as ft
from handlers.cache.table_templates import (
    filter_table,
    close_dialog
)


class CacheView:
    def __init__(self, app_state):
        self.app_state = app_state
        self.vuln_type_template_records = []
        self.filtered_records = []
        self.current_page = 0
        self.rows_per_page = 20

        # --- DataTable with padded headers for alignment ---
        self.table_types_templates = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Vulnerability Type")),
                ft.DataColumn(ft.Text("Context")),
                ft.DataColumn(
                    label=ft.Container(
                        padding=ft.padding.only(left=-25),  # adjust left until it lines up
                        content=ft.Text("Has Template")
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        padding=ft.padding.only(left=150),
                        content=ft.Text("View Template")
                    )
                ),
            ],
            rows=[],
            expand=True,
            width=float("inf"),
        )

        # result counter + pagination controls
        self.result_count = ft.Text(value="Search to display results", size=12, italic=True)
        self.page_number  = ft.Text(value="Page 1", size=12)
        self.prev_button = ft.IconButton(
            ft.Icons.NAVIGATE_BEFORE,
            on_click=self.prev_page,
            disabled=True
        )
        self.next_button = ft.IconButton(
            ft.Icons.NAVIGATE_NEXT,
            on_click=self.next_page,
            disabled=True
        )

        # build the rest of the UI
        self.cache_view = self._build_ui()

    def prev_page(self, e):
        if self.current_page > 0:
            self.current_page -= 1
            filter_table(self, self.app_state.search_query)
            self.update_navigation()

    def next_page(self, e):
        total_pages = (len(self.vuln_type_template_records) + self.rows_per_page - 1) // self.rows_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            filter_table(self, self.app_state.search_query)
            self.update_navigation()

    def update_navigation(self):
        total_count = len(self.filtered_records)
        total_pages = (total_count + self.rows_per_page - 1) // self.rows_per_page
        # guard against zero
        pages = total_pages if total_pages > 0 else 1
        self.page_number.value = f"Page {self.current_page + 1} of {pages}"
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == total_pages - 1 if total_pages > 0 else True
        self.next_button.disabled = self.current_page >= pages - 1
        self.page_number.update()
        self.prev_button.update()
        self.next_button.update()

    def _build_ui(self):
        search_field = ft.TextField(
            label="Search vulnerability type...",
            on_change=lambda e: self.update_search(e.control.value),
            expand=True,
        )

        template_dialog = ft.AlertDialog(
            title=ft.Text("Template Viewer"),
            content=ft.Column([ft.Text("")], scroll=ft.ScrollMode.AUTO, expand=True),
            actions=[ft.TextButton("Close", on_click=lambda e: close_dialog(self.app_state, template_dialog))],
            modal=True,
            content_padding=ft.padding.all(20),
        )
        self.app_state.template_dialog = template_dialog
        self.app_state.page.dialog = template_dialog
        self.app_state.search_query = ""

        return ft.Container(
            expand=True,
            padding=10,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=15,
                controls=[
                    ft.Column(
                        controls=[
                            search_field,
                            self.result_count
                        ],
                        spacing=10
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.prev_button,
                            self.page_number,
                            self.next_button,
                        ]
                    ),
                    ft.Container(
                        content=self.table_types_templates,
                        expand=True,
                        padding=10,
                        alignment=ft.alignment.center
                    ),
                    template_dialog
                ]
            )

        )

    def render(self):
        # Load and flatten data
        self.vuln_type_template_records = []  # Reset records on each render
        cache = self.app_state.cache or {}
        for ctx in cache["contexts"]:
            ctx_uuid = ctx["uuid"]
            ctx_name = ctx["name"]
            for vt in cache["vuln_types"].get(ctx_uuid, []):
                self.vuln_type_template_records.append({
                    "Vulnerability Type": vt.get("display_name") or vt["name"],
                    "Context": ctx_name,
                    "Has Template": "Yes" if vt.get("template_text") else "No",
                    "Template Text": vt.get("template_text", ""),
                    "UUID": vt["uuid"]
                })

        self.filtered_records = self.vuln_type_template_records.copy()
        return self.cache_view

    def update_search(self, query):
        self.current_page = 0
        self.app_state.search_query = query
        filter_table(self, query)
        self.update_navigation()

    def load_initial_data(self):
        filter_table(self, "")