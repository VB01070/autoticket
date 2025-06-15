import flet as ft
from handlers.home.markdown_text import markdown_text


class HomeView:
    def __init__(self, app_state):
        self.app_state = app_state

    def render(self):

        first_row = ft.Row([
            ft.Icon(name=ft.Icons.CAMPAIGN_OUTLINED, size=40, color=ft.Colors.GREEN),
            ft.Text("What's New", size=38, weight=ft.FontWeight.BOLD),
            ft.Text(f"version {str(self.app_state.app_version)}", size=12, weight=ft.FontWeight.BOLD, italic=True)
        ])

        dummy_card = ft.Container(
            expand=True,
            padding=20,
            bgcolor=ft.Colors.SURFACE,
            content=ft.Column(
                [
                    first_row,
                    ft.Markdown(
                        markdown_text,
                        selectable=True,
                        expand=True,
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
        )

        return dummy_card
