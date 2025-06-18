import flet as ft
from utils.manage_keys import get_credential
from utils.caching import initial_fetch_all, load_cache, CACHE_PATH
import asyncio
import os
from logs.logger import logger


async def _do_initial_fetch(page):
    try:
        # fetch everything in a thread so the event loop stays free
        await asyncio.to_thread(initial_fetch_all)
        # load the cache (also blocking, so thread it)
        page.app_state.cache = await asyncio.to_thread(load_cache)
        # build map + dropdown options
        opts = []
        for ctx_uuid, types in page.app_state.cache.get("vuln_types", {}).items():
            for vt in types:
                name = vt["name"]
                page.app_state.vuln_type_map[name] = {
                    "vuln_uuid": vt["uuid"],
                    "context_uuid": ctx_uuid
                }
                opts.append(ft.dropdown.Option(key=vt["uuid"], text=name))

        page.app_state.vuln_types_dropdown.options = opts
        page.app_state.info_progress.visible = False
        if page.route == "/1":
            page.app_state.load_note_local_button.disabled = False
            page.app_state.load_note_drive_button.disabled = False
        page.app_state.cache_check_icon.name = ft.Icons.CHECK
        page.app_state.cache_check_icon.color = ft.Colors.GREEN_ACCENT
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.BLACK87),
                ft.Text("Cache created successfully!", size=14, color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.GREEN_400
    except ValueError as e:
        if "API key expired or invalid" in str(e):
            logger.exception(f"API key expired or invalid: {e}")
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text(f"API key expired or invalid: {e}", size=14, color=ft.Colors.BLACK87)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        else:
            logger.error("API key not Founded..")
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                    ft.Text("API key not Founded..", size=14, color=ft.Colors.BLACK87)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.ORANGE_400
    except Exception as ex:
        logger.exception(f"An error occurred: {ex}")
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.WARNING_OUTLINED, color=ft.Colors.BLACK87),
                ft.Text(f"Initial fetch failed:{ex}", size=14, color=ft.Colors.BLACK87)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
    finally:
        if os.path.exists(CACHE_PATH):
            page.app_state.cache_check_icon.name = ft.Icons.CHECK
            page.app_state.cache_check_icon.color = ft.Colors.GREEN_ACCENT
            page.app_state.cache_check_icon.update()

        # if page.route == "/1":
        #     page.app_state.vuln_types_dropdown.disabled = False
        page.snack_bar.open = True
        page.update()


def initial_fetch(page, e):
    if page.route == "/1":
        page.app_state.load_note_local_button.disabled = True
        page.app_state.load_note_drive_button.disabled = True
    page.app_state.cache_check_icon.name = ft.Icons.CLOSE
    page.app_state.cache_check_icon.color = ft.Colors.RED_ACCENT
    page.app_state.info_progress.visible = True
    page.snack_bar.content = ft.Row(
        controls=[
            ft.Icon(name=ft.Icons.DOWNLOADING_OUTLINED, color=ft.Colors.BLACK87),
            ft.Text("Fetching vulnerability types…", size=14, color=ft.Colors.BLACK87)
        ]
    )
    page.snack_bar.bgcolor = ft.Colors.BLUE_400
    page.snack_bar.open = True
    page.update()

    async def fetch_wrapper():
        await _do_initial_fetch(page)

    page.run_task(fetch_wrapper)
