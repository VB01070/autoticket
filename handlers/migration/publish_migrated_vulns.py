import flet as ft
from utils.caching import BASE_URL, get_headers
import requests
from logs.logger import logger


def publish_migrated_vulns(page, uuids_list):
    if not uuids_list:
        logger.info('No UUIDs provided.')
        page.snack_bar.content = ft.Row([
            ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
            ft.Text("No vulnerabilities uuids to publish.", color=ft.Colors.BLACK87)
        ])
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        page.snack_bar.open = True
        page.update()
        return

    headers = get_headers()
    url = f"{BASE_URL}/api/v3/vulnerabilities/bulk-action/change-state"
    body = {
        "vulnerabilities": uuids_list,
        "state": "publish"
    }

    try:
        response = requests.post(url, json=body, headers=headers, verify=False)
        if response.status_code == 200:
            page.snack_bar.content = ft.Row([
            ft.Icon(name=ft.Icons.CHECK_OUTLINED, color=ft.Colors.BLACK87),
            ft.Text("The migrated vulnerabilities have been published.", color=ft.Colors.BLACK87)
            ])
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
            page.snack_bar.open = True
        else:
            logger.error(f"Failed to publish migrated vulnerabilities: {response.status_code}")
            page.snack_bar.content = ft.Row([
                ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                ft.Text(f"Publish failed: {response.status_code}", color=ft.Colors.BLACK87)
                ])
            page.snack_bar.content = ft.Text()
            page.snack_bar.bgcolor = ft.Colors.ORANGE_400
            page.snack_bar.open = True

    except Exception as ex:
        logger.exception(f"Failed to publish migrated vulnerabilities: {ex}")
        page.snack_bar.content = ft.Row([
            ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
            ft.Text(f"Publish failed. Error: {ex}", color=ft.Colors.BLACK87)
            ])
        page.snack_bar.content = ft.Text()
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        page.snack_bar.open = True

    page.update()