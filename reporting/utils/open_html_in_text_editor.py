import os
import subprocess
import platform


def open_html_in_text_editor(page):
    if not hasattr(page, "html_file_path") or not os.path.exists(page.html_file_path):
        print("HTML path is missing or invalid")
        return

    html_file = page.html_file_path

    try:
        system = platform.system()
        if system == "Windows":
            subprocess.run(["notepad.exe", html_file])
        else:  # Linux
            subprocess.run(["xdg-open", html_file])
    except Exception as e:
        print(f"Could not open file: {e}")
