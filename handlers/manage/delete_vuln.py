import flet as ft
from utils.caching import BASE_URL, get_headers
import requests


def delete_vuln(page, uuid):
    headers = get_headers()
    url = f"{BASE_URL}/api/v3/provider/vulnerabilities/bulk-action/delete"
    body = {
        "vulnerabilities": [uuid]
    }

    body_check = {
        "uuid": [uuid]
    }

    try:
        check_response = requests.post(f"{BASE_URL}/api/v3/vulnerabilities", headers=headers, json=body_check)
        items = check_response.json().get("items", [])

        if not items:
            print("No vulnerabilities found")
            page.update()
            return False

        if not items[0].get("published_at"):
            try:
                response = requests.delete(url, json=body, headers=headers, verify=False)
                if response.status_code == 200:
                    print(response.text)
                    return True

                    # uuid_field.value = ""
                    # uuid_field.update()
                else:
                    print(response.text)
                    return False
            except Exception as exc:
                print(exc)
                return False
        else:
            page.snack_bar.content = ft.Row(
                [
                    ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text("Vulnerability is already published. Impossible to Delete.", color=ft.Colors.BLACK87)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.ORANGE_400
            page.snack_bar.open = True
            page.update()
            return False

    except Exception as ex:
        print(ex)
        return False

    page.update()


def delete_selected_vulns(page, e):
    selected_uuids = list(page.app_state.selected_vuln_uuids)
    if not page.app_state.selected_vuln_uuids:
        page.snack_bar.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.QUESTION_MARK_OUTLINED, color=ft.Colors.BLACK87),
                ft.Text("No vulnerabilities selected.", color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        page.snack_bar.open = True
        page.update()
        return

    headers = get_headers()
    url = f"{BASE_URL}/api/v3/provider/vulnerabilities/bulk-action/delete"
    body = {
        "vulnerabilities": selected_uuids
    }

    try:
        response = requests.delete(url, json=body, headers=headers, verify=False)
        if response.status_code == 200:
            print(response.text)
            page.snack_bar.content = ft.Row(
                [
                    ft.Icon(name=ft.Icons.CHECK_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text("The vulnerabilities have been deleted.", color=ft.Colors.BLACK87)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
            page.snack_bar.open = True

            from handlers.manage.vuln_data import get_vuln_list_data
            from handlers.manage.tables_handler import render_vuln_table
            vuln_data = get_vuln_list_data(page.app_state.test_uuid_all_text_field.value)
            render_vuln_table(page, vuln_data)
        else:
            print(response.text)
            page.snack_bar.content = ft.Row(
                [
                    ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text(f"Delete failed: {response.status_code}", color=ft.Colors.BLACK87)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.ORANGE_400
            page.snack_bar.open = True

    except Exception as ex:
        print(ex)
        page.snack_bar.content = ft.Row(
                [
                    ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text(f"Delete failed. Error: {ex}", color=ft.Colors.BLACK87)
                ]
            )
        page.snack_bar.bgcolor = ft.Colors.RED_400
        page.snack_bar.open = True

    page.update()
