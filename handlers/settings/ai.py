import flet as ft
from utils.manage_keys import save_credentials, get_credential, delete_credential
import requests
import google.generativeai  as genai


def save_ai_key(page, key, e, reset_callback):
    if not key or key == "":
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.QUESTION_MARK, color=ft.Colors.WHITE),
                ft.Text("Please insert an API Key.", size=14)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_300
    else:
        if save_credentials("AiAPIKey", key):
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
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                    ft.Text("Failed to save API key.", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.RED_300

    page.snack_bar.open = True
    page.update()


def check_ai_key(page, e):
    assistant = page.app_state.ai_assistant
    print(assistant)
    cred = get_credential("AiAPIKey")
    if cred:
        if assistant == "GPT":
            headers = {"Authorization": f"Bearer {cred}"}
            response = requests.get("https://api.openai.com/v1/models", headers=headers)
            if response.status_code == 200:
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
        elif assistant == "Gemini":
            try:
                genai.configure(api_key=cred)
                _ = genai.list_models()
                page.snack_bar.content = ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.VERIFIED, color=ft.Colors.WHITE),
                        ft.Text("API Key present in Windows Credential Manager, is still valid!", size=14)
                    ]
                )
                page.snack_bar.bgcolor = ft.Colors.GREEN_300
            except Exception as e:
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


def delete_ai_key(page, e):
    try:
        delete_credential("AiAPIKey")
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.WHITE),
                ft.Text("API Key Deleted Successfully!", size=14)
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


def close_dialog_ai(page, e):
    if hasattr(page, "confirm_dialog"):
        page.confirm_dialog.open = False
        del page.confirm_dialog
        page.update()
