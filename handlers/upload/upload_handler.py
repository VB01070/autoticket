import flet as ft
import json
import requests
import asyncio
from utils.payload_builder import build_payload
from handlers.upload.ai_editable import parse_editable_ai
from utils.caching import BASE_URL
from utils.manage_keys import get_credential


def upload_all_vulnerabilities(page, e):
    # Build the payload dynamically
    finding = page.app_state.findings[page.app_state.current_finding_index]
    ai_raw = page.app_state.ai_suggestions[page.app_state.current_finding_index]
    ai_edit = page.app_state.ai_suggestions_editable[page.app_state.current_finding_index]

    if ai_edit and isinstance(ai_edit, str):
        try:
            ai_data = parse_editable_ai(ai_edit)
        except Exception as ex:
            ai_data = ai_raw
    else:
        ai_data = ai_raw

    uuids = {
        "asset": page.app_state.asset_uuid,
        "vuln_type": page.app_state.vuln_type_uuids[page.app_state.current_finding_index]["vuln_type"],
        "context": page.app_state.vuln_type_uuids[page.app_state.current_finding_index]["context"],
        "test": page.app_state.test_uuid,
    }

    payload = build_payload(finding, ai_data, uuids, vuln_type_name=None)
    x_api_key = get_credential("DashboardAPIKey")
    org_uuid = page.app_state.org_uuid
    url = f"{BASE_URL}/api/v3/provider/vulnerabilities/{org_uuid}/create"
    headers = {
        "x-api-key": x_api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            page.app_state.info_progress.visible = False
            page.snack_bar.content = ft.Text("Vulnerability successfully submitted!")
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
            page.snack_bar.open = True
            page.update()
        else:
            page.app_state.info_progress.visible = False
            page.snack_bar.content = ft.Text(f"Upload Failed! Status: {response.status_code}: {response.text}")
            page.snack_bar.bgcolor = ft.Colors.RED_400
            page.snack_bar.open = True
            page.update()
    except Exception as ex:
        page.app_state.info_progress.visible = False
        page.snack_bar.content = ft.Text(f"Error! Request failed: {ex}")
        page.snack_bar.bgcolor = ft.Colors.RED_400
        page.snack_bar.open = True
        page.update()


async def _upload_single_vuln(page, idx, finding, ai_data, uuids, url, headers):
    try:
        payload = build_payload(finding, ai_data, uuids, vuln_type_name=None)
        response = await asyncio.to_thread(requests.post, url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"[ERROR] Upload failed for finding {idx + 1}: {response.status_code} - {response.text}")
            return False
        return True

    except Exception as ex:
        print(f"[EXCEPTION] Failed to upload finding {idx + 1}: {ex}")
        return False


def upload_vulnerability(page, e):
    page.app_state.info_progress.visible = True
    page.snack_bar.content = ft.Text("Uploading all vulnerabilities...")
    page.snack_bar.bgcolor = ft.Colors.BLUE_200
    page.snack_bar.open = True
    page.update()

    page.run_task(_do_upload_all_vulns, page)


async def _do_upload_all_vulns(page):
    x_api_key = get_credential("DashboardAPIKey")
    org_uuid = page.app_state.org_uuid
    url = f"{BASE_URL}/api/v3/provider/vulnerabilities/{org_uuid}/create"
    headers = {
        "x-api-key": x_api_key,
        "Content-Type": "application/json"
    }

    tasks = []
    for idx, finding in enumerate(page.app_state.findings):
        ai_raw = page.app_state.ai_suggestions[idx]
        ai_edit = page.app_state.ai_suggestions_editable[idx]

        # Prefer editable if valid
        if ai_edit and isinstance(ai_edit, str):
            try:
                ai_data = parse_editable_ai(ai_edit)
            except Exception:
                ai_data = ai_raw
        else:
            ai_data = ai_raw

        uuids = {
            "asset": page.app_state.asset_uuid,
            "vuln_type": page.app_state.vuln_type_uuids[idx]["vuln_type"],
            "context": page.app_state.vuln_type_uuids[idx]["context"],
            "test": page.app_state.test_uuid,
        }

        tasks.append(_upload_single_vuln(page, idx, finding, ai_data, uuids, url, headers))

    results = await asyncio.gather(*tasks)
    all_success = all(results)

    page.app_state.info_progress.visible = False
    page.snack_bar.content = ft.Text(
        "All vulnerabilities uploaded!" if all_success else "Some vulnerabilities failed to upload."
    )
    page.snack_bar.bgcolor = ft.Colors.GREEN_400 if all_success else ft.Colors.RED_400
    page.snack_bar.open = True
    page.update()
