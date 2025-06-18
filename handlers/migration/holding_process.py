from time import sleep
import flet as ft
from handlers.migration.migrate import migrate_vuln
from handlers.migration.publish_migrated_vulns import publish_migrated_vulns
from handlers.manage.delete_vuln import delete_vuln



def run_all_process(page, final_payloads):
    original_vulns = page.app_state.migration_selected_uuids

    if not original_vulns:
        page.snack_bar.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                ft.Text("Vulnerability UUID is missing!", color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        page.snack_bar.open = True
        page.update()
        return


    migrate_vuln(page, final_payloads)
    sleep(1)

    try:
        for uuid in original_vulns:
            delete_vuln(page, uuid)

        page.snack_bar.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.CHECK_OUTLINED, color=ft.Colors.BLACK87),
                ft.Text("The vulnerability has been deleted.", color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.GREEN_400
    except Exception as err:
        print(err)
        page.snack_bar.content = ft.Row(
            [
                ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                ft.Text(f"Problem deleting original vulnerability: {err}", color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400

    from handlers.migration.fetch_vulns import fetch_vulns_per_migration
    fetch_vulns_per_migration(page, page.app_state.migrate_test_uuid_text_field.value)
    page.app_state.info_progress.visible = False
    page.snack_bar.open = True
    page.update()


