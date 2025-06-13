import asyncio
import json
import re
import flet as ft
from handlers.upload.display_finding import display_finding
from utils.assistant import generate_ai_suggestion


def ai_assistance(page, e):
    page.app_state.ai_content.value = "Generating AI suggestions for all findings..."
    page.app_state.ai_content_editable.value = "Generating AI suggestions for all findings..."
    page.app_state.info_progress.visible = True
    page.update()
    page.run_task(_do_ai_assistance_all, page)


async def _do_ai_assistance_all(page):
    page.app_state.ai_suggestions = [None] * len(page.app_state.findings)

    for idx, finding in enumerate(page.app_state.findings):
        title = finding.get("title", "")
        severity = finding.get("severity", "")
        notes = finding.get("note", "")

        template = None
        if hasattr(page.app_state, "matched_vuln_types") and idx < len(page.app_state.matched_vuln_types):
            match = page.app_state.matched_vuln_types[idx]
            if match:
                context_uuid = match["context_uuid"]
                vuln_uuid = match["vuln_type_uuid"]
                template = next(
                    (
                        vt.get("template_text")
                        for vt in page.app_state.cache.get("vuln_types", {}).get(context_uuid, [])
                        if vt["uuid"] == vuln_uuid
                    ),
                    None
                )
                print(f"[DEBUG] raw template type: {type(template)}")
                print(f"[DEBUG] raw template repr: {template!r}")
        print(template)
        print(page.app_state.ai_assistant)
        try:
            raw = await asyncio.to_thread(generate_ai_suggestion, title, severity, notes,
                                          page.app_state.ai_assistant, template)
            print(f"[RAW AI RESPONSE {idx}]:\n{raw}\n")
            try:
                data = json.loads(raw)
            except Exception as err:
                print(f"[ERROR] Failed parsing JSON for finding {idx}: {err}")
                data = {"raw": raw}
            page.app_state.ai_suggestions[idx] = data
        except Exception as ex:
            page.app_state.ai_suggestions[idx] = {"error": str(ex)}

        await asyncio.sleep(1.2)

    page.app_state.ai_suggestions_editable = [None if x is None else "" for x in page.app_state.ai_suggestions]
    display_finding(page)
    page.app_state.latest_ai_data = page.app_state.ai_suggestions[page.app_state.current_finding_index]
    page.snack_bar.content = ft.Row(
        controls=[
            ft.Icon(name=ft.Icons.SMART_TOY, color=ft.Colors.WHITE),
            ft.Text("All findings analyzed by AI Assistant!", size=14)
        ]
    )
    page.snack_bar.bgcolor = ft.Colors.GREEN_300
    page.snack_bar.open = True
    page.app_state.info_progress.visible = False
    page.app_state.edit_ai_content_button.disabled = False
    page.app_state.view_payload_button.disabled = False
    page.app_state.upload_vuln_button.disabled = False
    page.app_state.upload_all_vulns_button.disabled = False
    page.update()

    for item in page.app_state.ai_suggestions_editable:
        print(item)


def parse_editable_ai(text):
    """
    Parse The editable AI suggestion block back into payload structured (dict).
    Expected sections:
    Description:
    Impact:
    Recommendation:
    References:
    """
    sections = ["description", "impact", "recommendation", "references"]
    pattern = r"(Description|Impact|Recommendation|References):\s*\n"
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    result = {}
    current = None
    for part in parts:
        label = part.strip().lower()
        if label in sections:
            current = label
            result[current] = ""
        elif current:
            result[current] = part.strip()

    return result


def edit_ai_suggestion(page, e):
    page.app_state.ai_content_editable.read_only = False
    page.app_state.ai_content_editable.bgcolor = ft.Colors.YELLOW_50
    page.app_state.ai_content_editable.update()
    page.app_state.ai_content_editable.focus()
    page.app_state.save_ai_content_button.disabled = False
    page.app_state.save_ai_content_button.update()
    page.app_state.edit_ai_content_button.disabled = True
    page.app_state.edit_ai_content_button.update()


def save_ai_suggestion(page, e):
    current_index = page.app_state.current_finding_index
    page.app_state.ai_suggestions_editable[current_index] = page.app_state.ai_content_editable.value

    page.app_state.edit_ai_content_button.disabled = False
    page.app_state.edit_ai_content_button.update()
    page.app_state.save_ai_content_button.disabled = True
    page.app_state.save_ai_content_button.update()
    page.app_state.ai_content_editable.bgcolor = ft.Colors.SURFACE
    page.app_state.ai_content_editable.read_only = True
    page.app_state.ai_content_editable.update()