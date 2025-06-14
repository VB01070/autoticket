import flet as ft
import requests
from utils.caching import get_headers, BASE_URL


def edit_details(page, e):
    servicenow_id = page.app_state.servicenow_id_text_field.value
    if not servicenow_id:
        servicenow_id = ""
    connection_type = page.app_state.connection_type_dropdown.value
    if not connection_type:
        connection_type = "Public"
    account_roles = page.app_state.account_role_text_field.value
    if not account_roles:
        account_roles = ""
    management_summary = page.app_state.management_summary_text_field.value
    if not management_summary:
        management_summary = ""

    test_details_body = f"[DETAILS]<br><br>ServiceNow Request ID: {servicenow_id}.<br>"
    test_details_body += f"Connection Type: {connection_type}<br>"
    if page.app_state.testing_account_switch.value:
        test_details_body += f"Test Accounts: Yes<br>"
    else:
        test_details_body += f"Test Accounts: No<br>"
    test_details_body += f"Account Roles: {account_roles}<br><br>"
    test_details_body += f"[MANAGEMENT SUMMARY]<br><br>{management_summary}"

    service_tag = page.app_state.service_tag_dropdown.value
    if not service_tag:
        service_tag = ""

    test_uuid = page.app_state.test_uuid_text_field.value
    if not test_uuid:
        page.snack_bar.content = ft.Text(f"You need to enter a test UUID")
        page.snack_bar.bgcolor = ft.Colors.RED_400
        page.app_state.test_uuid_text_field.autofocus = True
        page.app_state.test_uuid_text_field.update()

    payload = {
        "details": test_details_body,
        "tags": [service_tag]
    }

    url = f"{BASE_URL}/api/v3/tests/{test_uuid}/edit"
    response = requests.patch(url, headers=get_headers(), json=payload)
    if response.status_code == 200:
        try:
            if "success" in response.json():
                page.snack_bar.content = ft.Text(f"Test Details Updated")
                page.snack_bar.bgcolor = ft.Colors.GREEN_400
        except requests.exceptions.JSONDecodeError:
            page.snack_bar.content = ft.Text(f"Check the Test UUID")
            page.snack_bar.bgcolor = ft.Colors.RED_400
    else:
        print(response.status_code)
        print(response.text)
        page.snack_bar.content = ft.Text(f"Error: {response.status_code}: {response.text}")
        page.snack_bar.bgcolor = ft.Colors.RED_400

    page.snack_bar.open = True
    page.update()
