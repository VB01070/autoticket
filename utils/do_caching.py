import flet as ft
from utils.manage_keys import get_credential
from utils.caching import initial_fetch_all, load_cache, CACHE_PATH
import asyncio
import os


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
                ft.Icon(name=ft.Icons.DONE_OUTLINE, color=ft.Colors.WHITE),
                ft.Text("Cache created successfully!", size=14)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.GREEN_300
    except ValueError as e:
        if "API key expired or invalid" in str(e):
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                    ft.Text(f"{e}", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.RED_300
        else:
            page.snack_bar.content = ft.Row(
                controls=[
                    ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                    ft.Text("API key not Founded..", size=14)
                ]
            )
            page.snack_bar.bgcolor = ft.Colors.RED_300
    except Exception as ex:
        page.snack_bar.content = ft.Row(
            controls=[
                ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.WHITE),
                ft.Text(f"Initial fetch failed:{ex}", size=14)
            ]
        )
        page.snack_bar.bgcolor = ft.Colors.RED_300
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
            ft.Icon(name=ft.Icons.DOWNLOADING, color=ft.Colors.WHITE),
            ft.Text("Fetching vulnerability types…", size=14)
        ]
    )
    page.snack_bar.bgcolor = ft.Colors.BLUE_400
    page.snack_bar.open = True
    page.update()

    async def fetch_wrapper():
        await _do_initial_fetch(page)

    page.run_task(fetch_wrapper)
