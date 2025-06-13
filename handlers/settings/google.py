import base64
import json
import tempfile
import os
import time
import flet as ft
from utils.manage_keys import save_credentials, get_credential, delete_credential


def save_google_key(file_path):
    try:
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
        encoded = base64.b64encode(raw_bytes).decode("utf-8")
        save_credentials("GoogleKey", encoded)
        return True
    except Exception as e:
        print(e)
        return False


def handle_google_json_selection(page, e):
    status = page.app_state.google_json_status
    if e.files:
        file_path = e.files[0].path
        if save_google_key(file_path):
            status.value = f"{e.files[0].name}"
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.WHITE),
                    ft.Text("API Key saved securely in Windows Credential Manager!", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
        else:
            status.value = "Failed to save file"
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.SENTIMENT_VERY_DISSATISFIED, color=ft.Colors.WHITE),
                    ft.Text("API Key was NOT saved", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.RED_400
    else:
        status.value = "Selection cancelled"
        status.color = ft.Colors.GREY

    page.snack_bar.open = True
    status.update()
    page.update()


def check_google_key(page, e):
    if get_credential("GoogleKey"):
        page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.SENTIMENT_SATISFIED, color=ft.Colors.WHITE),
                    ft.Text("API Key present in Windows Credential Manager!", size=14)
                ]
        )
        page.snack_bar.bgcolor = ft.Colors.BLUE_400
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


def delete_google_key(page, e):
    try:
        delete_credential("GoogleKey")
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.WHITE),
                ft.Text("Google Credentials Deleted Successfully!", size=14)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.GREEN_300
    except Exception as e:
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


def close_dialog_google(page, e):
    if hasattr(page, "confirm_dialog"):
        page.confirm_dialog.open = False
        del page.confirm_dialog
        page.update()


def load_google_key():
    encoded = get_credential("GoogleKey")
    if not encoded:
        return False

    raw_bytes = base64.b64decode(encoded)
    json_bytes = raw_bytes.decode("utf-8")
    json_data = json.loads(json_bytes)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8")
    json.dump(json_data, temp)
    temp.close()

    return temp.name
