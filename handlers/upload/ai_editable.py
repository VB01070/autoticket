import re
import flet as ft


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

    page.view_payload_button.disabled = True
    page.view_payload_button.update()
    page.upload_vuln_button.disabled = True
    page.upload_vuln_button.update()
    page.upload_all_vulns_button.disabled = True
    page.upload_all_vulns_button.update()


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

    page.view_payload_button.disabled = False
    page.view_payload_button.update()
    page.upload_vuln_button.disabled = False
    page.upload_vuln_button.update()
    page.upload_all_vulns_button.disabled = False
    page.upload_all_vulns_button.update()
