import requests
import urllib3
from utils.caching import BASE_URL, get_headers
import flet as ft
from handlers.migration.render_migration_table import render_migration_table
from utils.payload_builder import migration_payload_builder
from logs.logger import logger

# Disable InsecureRequestWarning when verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_vulns_per_migration(page, test_uuid):
    if not test_uuid:
        logger.info('No test uuid specified')
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
    try:
        vuln_data = migration_fetcher(test_uuid)
        render_migration_table(page, vuln_data)
        page.app_state.fetched_migration_vulns = vuln_data

    except Exception as e:
        logger.exception(f"Error fetching vulns: {e}")
        page.snack_bar.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                ft.Text(f"Error fetching vulns: {e}", color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        page.snack_bar.open = True
        page.update()
        return


def migration_fetcher(test_uuid):
    body = {"tests": [test_uuid]}
    headers = get_headers()

    try:
        response = requests.post(f"{BASE_URL}/api/v3/vulnerabilities", headers=headers, json=body, verify=False)
        response.raise_for_status()
        items = response.json().get("items", [])

        filtered_items = [item for item in items if not item.get("published_at")]

        return [
            {
                "uuid": item.get("uuid"),
                "id": item.get("id"),
                "description": item.get("description"),
                "details": item.get("details"),
                "severity": item.get("severity"),
                "cvss_vector": item.get("cvss_vector"),
                "authenticated": item.get("authenticated"),
                "vuln_type_uuid": item.get("vulnerability_type", {}).get("uuid"),
                "organisation_uuid": item.get("organisation", {}).get("uuid"),
                "organisation_name": item.get("organisation", {}).get("name"),
            }
            for item in filtered_items
        ]
    except Exception as ex:
        logger.exception(f"Error fetching vulns: {ex}")

def build_migration_entries(page):
    combined_entries = []
    seen_uuids = set()
    page.app_state.info_progress.visible=True
    for vuln in page.app_state.fetched_migration_vulns:
        uuid = vuln["uuid"]
        if uuid not in page.app_state.migration_selected_uuids or uuid in seen_uuids:
            continue

        selected_asset_uuid = page.app_state.migration_dropdowns.get(uuid).value
        if not selected_asset_uuid:
            logger.debug(f"[!] No asset selected for vuln {uuid}, skipping.")
            continue

        vuln_type_uuid = vuln["vuln_type_uuid"]
        context_uuid = None
        for name, data_list in page.app_state.cache["vuln_types"].items():
            for data in data_list:
                if data["uuid"] == vuln_type_uuid:
                    context_uuid = data.get("context_uuid")
                    break
            if context_uuid:
                break

        entry = {
            "original_uuid": uuid,
            "id": vuln["id"],
            "description": vuln["description"],
            "details": vuln["details"],
            "severity": vuln["severity"],
            "cvss_vector": vuln["cvss_vector"],
            "authenticated": vuln["authenticated"],
            "vuln_type_uuid": vuln_type_uuid,
            "context_uuid": context_uuid,
            "organisation_uuid": vuln["organisation_uuid"],
            "organisation_name": vuln["organisation_name"],
            "target_asset_uuid": selected_asset_uuid
        }

        combined_entries.append(entry)
        seen_uuids.add(uuid)

    migration_payload_builder(page, combined_entries)