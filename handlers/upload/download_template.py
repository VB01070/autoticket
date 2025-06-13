import os
import shutil
import flet as ft


def download_template(e: ft.FilePickerResultEvent, page):
    src_path = os.path.join(os.path.dirname(__file__), "..", "..", "templates", "AutoTicket_template.docx")
    if e.path:
        # e.path is now a folder
        dst_path = os.path.join(e.path, "AutoTicket_template.docx")
        try:
            shutil.copy(src_path, dst_path)
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.WHITE),
                    ft.Text(f"Template downloaded successfully to {dst_path}", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.GREEN_300
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                    ft.Text(f"Error downloading template: {ex}", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.RED_300
            page.snack_bar.open = True
            page.update()
