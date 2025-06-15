import flet as ft


def edit_summary(page, e):
    page.app_state.management_summary_text_field.read_only = False
    page.app_state.management_summary_text_field.bgcolor = ft.Colors.YELLOW_50
    page.app_state.management_summary_text_field.update()
    page.app_state.management_summary_text_field.focus()
    page.app_state.generate_ai_summary_button.disabled = True
    page.app_state.generate_ai_summary_button.update()
    page.app_state.upload_test_details_button.disabled = True
    page.app_state.upload_test_details_button.update()
    page.app_state.edit_ai_summary_button.disabled = True
    page.app_state.edit_ai_summary_button.update()
    page.app_state.save_edit_ai_summary_button.disabled = False
    page.app_state.save_edit_ai_summary_button.update()


def save_ai_edit_summary(page, e):
    page.app_state.management_summary_text_field.read_only = True
    page.app_state.management_summary_text_field.bgcolor = ft.Colors.SURFACE
    page.app_state.management_summary_text_field.update()
    page.app_state.generate_ai_summary_button.disabled = False
    page.app_state.generate_ai_summary_button.update()
    page.app_state.upload_test_details_button.disabled = False
    page.app_state.upload_test_details_button.update()
    page.app_state.edit_ai_summary_button.disabled = False
    page.app_state.edit_ai_summary_button.update()
    page.app_state.save_edit_ai_summary_button.disabled = True
    page.app_state.save_edit_ai_summary_button.update()
