import flet as ft
from collections import OrderedDict
from helpers.cvss4 import CVSS4
from helpers.exceptions import CVSS4Error


def open_cvss_calculator_dialog(page, e):
    print("--- Button clicked! Populating and opening dialog... ---")

    # Get the dialog shell we created in the view
    dialog = page.app_state.cvss_dialog
    app_state = page.app_state

    # Define the dropdown options
    METRIC_OPTIONS = {
        "AV": OrderedDict([("N", "Network"), ("A", "Adjacent"), ("L", "Local"), ("P", "Physical")]),
        "AC": OrderedDict([("L", "Low"), ("H", "High")]),
        "AT": OrderedDict([("N", "None"), ("P", "Present")]),
        "PR": OrderedDict([("N", "None"), ("L", "Low"), ("H", "High")]),
        "UI": OrderedDict([("N", "None"), ("P", "Passive"), ("A", "Active")]),
        "VC": OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")]),
        "VI": OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")]),
        "VA": OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")]),
        "SC": OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")]),
        "SI": OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")]),
        "SA": OrderedDict([("H", "High"), ("L", "Low"), ("N", "None")]),
    }

    # --- Action handlers for the dialog's buttons ---
    def calculate_and_close(e):
        # The vector string is built here
        vector_parts = ["CVSS:4.0"]
        for metric, control in controls_map.items():
            vector_parts.append(f"{metric}:{control.value}")
        vector_string = "/".join(vector_parts)

        try:
            c = CVSS4(vector_string)
            # We can keep the severity calculation
            severity = c.severity
            if severity.lower() == "none":
                severity = "Info"

        except CVSS4Error as ex:
            # If there's an error, we can update the UI accordingly
            vector_string = "Error: Invalid Vector"
            severity = "Error"
            print(f"CVSS Error: {ex}")

        # === THIS IS THE ONLY CHANGE ===
        # Assign the vector_string to the text field instead of the numerical score
        idx = app_state.current_finding_index
        app_state.cvss_data[idx]["vector"] = vector_string
        app_state.cvss_data[idx]["severity"] = severity

        app_state.cvss_text.value = vector_string
        app_state.severity_text.value = str(severity)
        # ==============================

        dialog.open = False
        page.update()

    def close_dialog(e):
        dialog.open = False
        page.update()

    # --- Function to build dropdowns ---
    def create_metric_dropdown(metric_key, label, default_value_key):
        options = [
            ft.dropdown.Option(key=key, text=text)
            for key, text in METRIC_OPTIONS[metric_key].items()
        ]
        return ft.Dropdown(
            label=label,
            options=options,
            value=default_value_key,
            dense=True,
            expand=True,
        )

    # --- Build the calculator controls ---
    controls_map = {
        "AV": create_metric_dropdown("AV", "Attack Vector (AV)", "N"),
        "AC": create_metric_dropdown("AC", "Attack Complexity (AC)", "L"),
        "AT": create_metric_dropdown("AT", "Attack Requirements (AT)", "N"),
        "PR": create_metric_dropdown("PR", "Privileges Required (PR)", "N"),
        "UI": create_metric_dropdown("UI", "User Interaction (UI)", "N"),
        "VC": create_metric_dropdown("VC", "Vulnerable System Confidentiality (VC)", "H"),
        "VI": create_metric_dropdown("VI", "Vulnerable System Integrity (VI)", "H"),
        "VA": create_metric_dropdown("VA", "Vulnerable System Availability (VA)", "H"),
        "SC": create_metric_dropdown("SC", "Subsequent System Confidentiality (SC)", "N"),
        "SI": create_metric_dropdown("SI", "Subsequent System Integrity (SI)", "N"),
        "SA": create_metric_dropdown("SA", "Subsequent System Availability (SA)", "N"),
    }

    # === THIS IS THE CRITICAL MISSING PIECE ===
    # 1. Assign the calculator controls to the dialog's 'content'
    dialog.content = ft.Column(
        controls=[ft.Row([v]) for v in controls_map.values()],
        spacing=8,
        scroll=ft.ScrollMode.ADAPTIVE,
        width=500,
    )

    # 2. Assign the buttons to the dialog's 'actions'
    dialog.actions = [
        ft.FilledButton("Calculate", on_click=calculate_and_close),
        ft.TextButton("Close", on_click=close_dialog),
    ]
    # ==========================================

    # 3. Open the dialog, which is now populated with the calculator
    dialog.open = True
    page.update()