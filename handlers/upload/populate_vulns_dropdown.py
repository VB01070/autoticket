import flet as ft


def populate_vulns_dropdown(app_state):
    dropdown = app_state.vuln_types_dropdown

    dropdown.options.clear()
    # map by display (for populating) and by uuid (for selection lookups)
    app_state.vuln_type_map        = {}  # display → {context_uuid, vuln_type_uuid}
    app_state.vuln_type_map_by_uuid = {} # uuid → {display, context_uuid}

    for ctx in app_state.cache.get("contexts", []):
        for vt in app_state.cache.get("vuln_types", {}).get(ctx["uuid"], []):
            display = vt.get("display_name") or vt["name"]
            uuid    = vt["uuid"]

            # add the option
            dropdown.options.append(ft.dropdown.Option(key=uuid, text=display))

            # fill both maps
            app_state.vuln_type_map[display] = {
                "context_uuid": ctx["uuid"],
                "vuln_type_uuid": uuid,
            }
            app_state.vuln_type_map_by_uuid[uuid] = {
                "display": display,
                "context_uuid": ctx["uuid"],
            }
