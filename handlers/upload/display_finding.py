from handlers.upload.placeholder_b64 import placeholder_b64


def display_finding(page):
    # Basic finding info
    idx = page.app_state.current_finding_index
    finding = page.app_state.findings[idx]
    # print(f"[DEBUG]: {finding}")

    page.app_state.document_content.value = (
        f"Title\n"
        f"{finding['title']}\n\n"
        f"Severity\n"
        f"{finding['severity']}\n\n"
        f"Note\n"
        f"{finding['note']}"
    )
    cvss_info = page.app_state.cvss_data[idx]
    #  AI suggestions
    # Grab the list (or None) and the current slot
    ai_suggestions = getattr(page.app_state, "ai_suggestions", None)
    if ai_suggestions and idx < len(ai_suggestions):
        ai_data = ai_suggestions[idx]
        # decide which text to show
        if ai_data is None:
            text = "No AI suggestion available yet."
        elif "error" in ai_data:
            text = f"Error from AI: {ai_data['error']}"
        elif "raw" in ai_data:
            text = ai_data["raw"]
        else:
            # build a nice formatted block
            parts = []
            for key in ("description", "impact", "recommendation", "references"):
                if key in ai_data:
                    header = key.capitalize()
                    val = ai_data[key]
                    if key == "references" and isinstance(val, list):
                        # bullet‐list references
                        refs = "\n".join(f"- {r['source']}: {r['url']}" for r in val)
                        parts.append(f"{header}:\n{refs}")
                    else:
                        parts.append(f"{header}:\n{val}")
            text = "\n\n".join(parts).strip() or "[no fields returned]"
    else:
        text = "AI suggestions not generated yet."

    # Push into both fields
    # page.app_state.ai_content.value = text
    page.app_state.ai_content_editable.value = text

    # update cvss vector and severity
    page.app_state.cvss_text.value = cvss_info.get("vector", "")
    page.app_state.severity_text.value = cvss_info.get("severity", "")
    page.app_state.cvss_text.update()
    page.app_state.severity_text.update()

    # Screenshots carousel
    screenshots = finding.get("screenshots", [])
    if screenshots:
        page.app_state.current_image_index = min(page.app_state.current_image_index, len(screenshots) - 1)
        page.app_state.image_preview.src_base64 = screenshots[page.app_state.current_image_index]
        page.app_state.image_preview.update()
        page.app_state.next_image_button.disabled = len(screenshots) <= 1
        page.app_state.prev_image_button.disabled = page.app_state.current_image_index == 0
    else:
        page.app_state.image_preview.src_base64 = placeholder_b64()
        page.app_state.next_image_button.disabled = True
        page.app_state.prev_image_button.disabled = True

    # Prev/Next vuln nav buttons
    page.app_state.previous_vulns_button.disabled = idx == 0
    page.app_state.next_vulns_button.disabled = idx >= len(page.app_state.findings) - 1

    # Show matched vuln type in dropdown & text ---
    matches = page.app_state.matched_vuln_types
    if idx < len(matches) and matches[idx]:
        match = matches[idx]
        page.app_state.vuln_types_text.value = match["name"]
        page.app_state.vuln_type_uuid = match["vuln_type_uuid"]
        page.app_state.vuln_type_context_uuid = match["context_uuid"]
        page.app_state.vuln_types_dropdown.value = match["vuln_type_uuid"]
        page.app_state.vuln_types_dropdown.update()
    else:
        page.app_state.vuln_types_text.value = "No match found"
        page.app_state.vuln_type_uuid = ""
        page.app_state.vuln_type_context_uuid = ""

    # Activate ai_assistance_button
    page.app_state.ai_assistance_button.disabled = False
    # Finally update the page ---
    page.update()


def previous_vuln(page, e):
    if page.app_state.current_finding_index > 0:
        page.app_state.current_finding_index -= 1
        display_finding(page)


def next_vuln(page, e):
    if page.app_state.current_finding_index < len(page.app_state.findings) - 1:
        page.app_state.current_finding_index += 1
        display_finding(page)
