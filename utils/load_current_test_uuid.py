import flet as ft


def load_current_test_uuid(page, e, schema):
    if page.app_state.test_uuid:
        if schema == "test":
            page.app_state.test_uuid_text_field.value = page.app_state.test_uuid
            page.snack_bar.content = ft.Text(f"UUID successfully loaded!")
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
        elif schema == "presentation":
            page.app_state.presentation_test_uuid_text_field.value = page.app_state.test_uuid
            page.snack_bar.content = ft.Text(f"UUID successfully loaded!")
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
        elif schema == "migration":
            page.app_state.migrate_test_uuid_text_field.value = page.app_state.test_uuid
            page.snack_bar.content = ft.Text(f"UUID successfully loaded!")
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
        elif schema == "report":
            page.app_state.report_test_uuid_text_field.value = page.app_state.test_uuid
            page.snack_bar.content = ft.Text(f"UUID successfully loaded!")
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
        elif schema == "publish":
            page.app_state.test_uuid_all_text_field.value = page.app_state.test_uuid
            page.snack_bar.content = ft.Text(f"UUID successfully loaded!")
            page.snack_bar.bgcolor = ft.Colors.GREEN_400
    else:
        page.snack_bar.content = ft.Text(f"UUID not Found!")
        page.snack_bar.bgcolor = ft.Colors.RED_400

    page.snack_bar.open = True
    page.update()
