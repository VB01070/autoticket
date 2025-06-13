import flet as ft
import os
from weasyprint import HTML
import tempfile
import webbrowser
import threading
import time
from reporting.configuration.configuration import ReportConfiguration
from reporting.utils.starting_info_parsed import StartingInfoParsed
from reporting.utils.fetcher import Fetcher
from reporting.utils.builder import Builder


def generate_report_html(page):
    basic_info = StartingInfoParsed(page)
    basic_info.get_basic_info_from_app()
    basic_info_arguments = basic_info.args

    configuration = ReportConfiguration(basic_info_arguments, page)
    configuration.load_configuration()

    data_fetcher = Fetcher(basic_info, configuration, page)
    fetched_data = data_fetcher.prepare_report_builder()
    report_builder = Builder(basic_info, configuration, fetched_data, page)
    report_builder.load_main_template()
    report_builder.fill_report_template()
    report_builder.sort_vulnerability_by_severity()
    report_builder.add_finding_to_report_template()
    report_builder.add_risk_table_to_report_template()
    report_builder.add_finding_table_to_report_template()
    report_builder.add_methodology_template()
    report_builder.add_findings_due_table_report_template()
    report_builder.add_appendix_template()
    report_builder.write_report_output_folder()
    if hasattr(page, "html_path_text") and hasattr(report_builder, "output_path"):
        page.html_file_path = report_builder.output_path
        page.html_path_text.value = page.html_file_path
        page.update()


def generate_pdf(page):
    html_file_path = page.html_file_path  # use the path saved in app

    if not os.path.exists(html_file_path):
        page.snack_bar.content = ft.Text(f"HTML file not found: {html_file_path}")
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        page.snack_bar.open = True
        page.update()
        return

    base_name = os.path.splitext(os.path.basename(html_file_path))[0]
    project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))

    reports_dir = os.path.join(project_root, "Reports")
    os.makedirs(reports_dir, exist_ok=True)
    output_path = os.path.join(reports_dir, f"{base_name}.pdf")

    base_url = os.path.abspath(os.path.join(os.path.dirname(html_file_path), ".."))
    html = HTML(filename=html_file_path, base_url=base_url)

    try:
        print("start generating")
        html.write_pdf(output_path)
        print(f"finished generating: {output_path}")
        page.snack_bar.content = ft.Text(f"PDF saved: {output_path}")
        page.snack_bar.bgcolor = ft.Colors.GREEN_400
        page.snack_bar.open = True
        page.update()
        return output_path
    except Exception as e:
        page.snack_bar.content = ft.Text(f"PDF generation failed: {e}")
        page.snack_bar.bgcolor = ft.Colors.ORANGE_400
        page.snack_bar.open = True
        page.update()
        print(f"PDF generation failed: {e}")
        return


def preview_pdf_in_memory(page):
    html_file_path = page.html_file_path
    if not html_file_path or not os.path.exists(html_file_path):
        print("HTML file missing or not valid.")
        return

    base_url = os.path.abspath(os.path.join(os.path.dirname(html_file_path), ".."))
    html = HTML(filename=html_file_path, base_url=base_url)

    # Create and write the PDF safely
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        html.write_pdf(temp_pdf.name)
        temp_pdf_path = temp_pdf.name

    print(f"Previewing: {temp_pdf_path}")

    try:
        os.startfile(temp_pdf_path)  # Windows
    except AttributeError:
        webbrowser.open(f"file://{temp_pdf_path}")  # Fallback for other OSes

    # Clean up the temp file after it's no longer in use
    def cleanup_when_closed(path):
        time.sleep(10)  # give viewer time to open it
        while True:
            try:
                os.rename(path, path)
                break
            except PermissionError:
                time.sleep(1)
        try:
            os.remove(path)
            print(f"Temp file removed: {path}")
        except Exception as e:
            print(f"Cleanup failed: {e}")

    threading.Thread(target=cleanup_when_closed, args=(temp_pdf_path,), daemon=True).start()
