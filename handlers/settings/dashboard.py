from utils.manage_keys import save_credentials, get_credential, delete_credential
from utils.caching import BASE_URL
import requests
from logs.logger import logger
import flet as ft


def save_dashboard_key(page, key, e, reset_callback):
    if not key or key == "":
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.QUESTION_MARK, color=ft.Colors.WHITE),
                ft.Text("Please insert an API Key.", size=14)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_300
    else:
        if save_credentials("DashboardAPIKey", key):
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.WHITE),
                    ft.Text("API Key saved!", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.GREEN_300
            reset_callback()  # clear the field
            # page.go("/6")     # reload settings view
        else:
            logger.error("API Key not saved!")
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                    ft.Text("Failed to save API key.", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.RED_300

    page.snack_bar.open = True
    page.update()


def delete_dashboard_key(page, e):
    try:
        delete_credential("DashboardAPIKey")
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.WHITE),
                ft.Text("API Key Deleted Successfully!", size=14)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.GREEN_300
    except Exception as e:
        logger.exception(f"Failed to delete Dashboard API key: {e}")
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                ft.Text(f"Impossible to delete the API key for the Dashboard. Error: {e}!", size=14)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.RED_400

    page.confirm_dialog.open = False
    page.snack_bar.open = True
    page.update()


def check_dashboard_key(page, e):
    creds = get_credential("DashboardAPIKey")
    if creds:
        headers = {"x-api-key": creds}
        response = requests.post(f"{BASE_URL}/api/v3/health", headers=headers)
        if response.status_code == 200 and response.text.strip().strip('"') == "Ok":
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.VERIFIED, color=ft.Colors.WHITE),
                    ft.Text("API Key present in Windows Credential Manager, is still valid!", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.GREEN_300
        else:
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                    ft.Text("API Key present in Windows Credential Manager, is no longer valid!", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.ORANGE_300
    else:
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                ft.Text("There are non credentials saved in Windows Credential Manager!", size=14)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_300

    page.snack_bar.open = True
    page.update()


def close_dialog_dashboard(page, e):
    if hasattr(page, "confirm_dialog"):
        page.confirm_dialog.open = False
        del page.confirm_dialog
        page.update()

