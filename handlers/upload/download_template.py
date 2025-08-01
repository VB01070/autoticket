import os
import shutil
import flet as ft
from logs.logger import logger


def download_template(e: ft.FilePickerResultEvent, page):
    src_path = os.path.join(os.path.dirname(__file__), "..", "..", "templates", "AutoTicket_template.docx")
    if e.path:
        # e.path is now a folder
        dst_path = os.path.join(e.path, "AutoTicket_template.docx")
        try:
            shutil.copy(src_path, dst_path)
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.BLACK87),
                    ft.Text(f"Template downloaded successfully to {dst_path}", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            logger.exception(f"Exception while downloading AutoTicket template: {ex}")
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text(f"Error downloading template: {ex}", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.ORANGE_400
            page.snack_bar.open = True
            page.update()
