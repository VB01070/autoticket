from handlers.manage.tables_handler import render_vuln_table
from handlers.manage.vuln_data import get_vuln_list_data
import flet as ft
from logs.logger import logger


def fetch_vulns_by_test(page, test_uuid):
    if not test_uuid:
        page.snack_bar.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.BLACK87),
                ft.Text("Test UUID is missing!.", color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor =ft.Colors.ORANGE_400
        page.snack_bar.open = True
        page.update()
        return

    try:
        vuln_data = get_vuln_list_data(test_uuid)
        render_vuln_table(page, vuln_data)
        page.app_state.fetched_vulns = vuln_data

    except Exception as e:
        logger.exception(f"Error fetching vulns: {e}")
        page.snack_bar.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.BLACK87),
                ft.Text(f"Error fetching vulnerabilities: {e}", color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor =ft.Colors.ORANGE_400
        page.snack_bar.open = True