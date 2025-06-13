from handlers.upload.display_finding import display_finding


def previous_image(page, e):
    if page.app_state.current_image_index > 0:
        page.app_state.current_image_index -= 1
        display_finding(page)


def next_image(page, e):
    screenshots = page.app_state.findings[page.app_state.current_finding_index].get("screenshots", [])
    if page.app_state.current_image_index < len(screenshots) - 1:
        page.app_state.current_image_index += 1
        display_finding(page)
