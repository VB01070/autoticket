from flet import FilePickerResultEvent, FilePicker


def open_project_folder(page, e):
    folder_picker = FilePicker()
    page.overlay.append(folder_picker)

    page.app_state.folder_picker = folder_picker

    def on_folder_selected(e: FilePickerResultEvent):
        if e.path:
            page.project_folder = e.path
            page.app_state.project_folder = e.path  # keep app_state in sync

            # update the label
            label = page.app_state.project_folder_temp_text
            label.value = e.path
            label.update()

    folder_picker.on_result = on_folder_selected
    page.update()  # ensure picker is attached before triggering
    folder_picker.get_directory_path()
