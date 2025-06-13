import flet as ft
from handlers.home.markdown_text import markdown_text


class HomeView:
    def __init__(self, app_state):
        self.app_state = app_state

    def render(self):

        dummy_card = ft.Container(
            expand=True,
            padding=20,
            bgcolor=ft.Colors.INDIGO_50,
            content=ft.Column(
                [
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
