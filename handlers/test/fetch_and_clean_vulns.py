from utils.caching import BASE_URL, get_headers
from handlers.test.extract_sections import extract_sections
import requests
import urllib3
import flet as ft
from logs.logger import logger

# Disable InsecureRequestWarning when verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_and_clean_vulns(page, test_uuid):
    if not test_uuid:
        page.snack_bar.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                ft.Text("Test UUID is missing!", color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        page.snack_bar.open = True
        page.update()
        return

    page.app_state.info_progress.visible = True
    page.app_state.management_summary_text_field.value = "Generating AI Management Summary..."
    page.update()

    url = f"{BASE_URL}/api/v3/vulnerabilities"
    body = {"tests": [test_uuid]}
    headers = get_headers()

    try:
        response = requests.post(url, headers=headers, json=body, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.exception(f"Failed to fetch AI API key: {e}")
        return []

    items = response.json().get("items", [])
    cleaned = []
    for item in items:
        details_html = item.get("details", "")
        sections = extract_sections(page, details_html)
        cleaned.append({
            "title": item.get("description", ""),
            "severity": item.get("severity", ""),
            **sections
        })

    return cleaned


