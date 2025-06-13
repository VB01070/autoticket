from handlers.manage.tables_handler import render_vuln_table
from handlers.manage.vuln_data import get_vuln_list_data
import flet as ft


def fetch_vulns_by_test(page, test_uuid):
    if not test_uuid:
        page.snack_bar = ft.SnackBar(ft.Text("Test UUID is missing!"), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()
        return

    try:
        vuln_data = get_vuln_list_data(test_uuid)
        render_vuln_table(page, vuln_data)
        page.app_state.fetched_vulns = vuln_data

    except Exception as e:
        print(f"Error fetching vulns: {e}")
        page.snack_bar = ft.SnackBar(ft.Text(f"Error fetching vulnerabilities"), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()