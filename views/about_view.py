import flet as ft
from handlers.about.about_md_text import about_md_text


class AboutView:
    def __init__(self, app_state):
        self.app_state = app_state

    def render(self):
        first_row = ft.Row([
            ft.Icon(name=ft.Icons.INFO_OUTLINE, size=40, color=ft.Colors.GREEN),
            ft.Text("About", size=38, weight=ft.FontWeight.BOLD),
        ])

        dummy_card = ft.Container(
            expand=True,
            padding=20,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Column(
                [
                    first_row,
                    ft.Markdown(
                        about_md_text,
                        selectable=True,
                        expand=True,
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
        )

        return dummy_card