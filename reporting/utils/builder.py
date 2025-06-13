import os
import re
import flet as ft
from datetime import datetime
from reporting.utils.helpers import get_severity_as_html, html_status_resolved, calculate_due_date, slugify_file_name


class Builder:
    def __init__(self, basic_info, configuration, data_fetcher, page):
        self.page = page
        self.page.app_state = page.app_state
        self.pentest_info = ""
        self.vuln_issues = []

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        resolve_path = lambda p: os.path.abspath(os.path.join(base_dir, p))

        self.report_template_file = resolve_path(configuration.report_template_file)
        self.risk_template_file = resolve_path(configuration.risk_table_template_file)
        self.finding_table_template_file = resolve_path(configuration.finding_table_template_file)
        self.finding_due_table_template_file = resolve_path(configuration.finding_due_table_template_file)
        self.finding_template_file = resolve_path(configuration.finding_template_file)
        self.methodology_file = resolve_path(configuration.methodology_file)
        self.appendix_file = resolve_path(configuration.appendix_file)

        self.info_sla = configuration.info_sla
        self.low_sla = configuration.low_sla
        self.medium_sla = configuration.medium_sla
        self.high_sla = configuration.high_sla
        self.critical_sla = configuration.critical_sla

        self.output_folder = resolve_path(configuration.report_output_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder, exist_ok=True)

        raw_data = data_fetcher.get("vulnerabilities", {})
        if isinstance(raw_data, dict):
            if all(isinstance(key, int) and isinstance(value, dict) for key, value in raw_data.items()):
                self.vuln_issues = list(raw_data.values())
            else:
                self.vuln_issues = [raw_data]
        elif isinstance(raw_data, list):
            self.vuln_issues = raw_data

        self.report_builder = ReportBuilder(self.report_template_file, self.page)
        self.pentest_info = data_fetcher["pentestInformation"]

    def load_main_template(self):
        print("[INFO] Loading main template...")
        self.report_builder.load_template()

    def fill_report_template(self):
        print("[INFO] Filling report template with standard information...")
        report_data = self.pentest_info

        self.report_builder.replace_placeholder("{YEAR}", report_data["Year"])
        self.report_builder.replace_placeholder("{APPLICATION_NAME}", report_data["Scope"])
        self.report_builder.replace_placeholder("{STATUS}", report_data["Status"])
        self.report_builder.replace_placeholder("{LAST_MODIFIED}", report_data["LastModified"])
        self.report_builder.replace_placeholder("{REFERENCE}", report_data["Name"])
        self.report_builder.replace_placeholder("{AUTHORS}", report_data["Authors"])
        self.report_builder.replace_placeholder("{START_DATE}", report_data["Start"])
        self.report_builder.replace_placeholder("{END_DATE}", report_data["End"])
        self.report_builder.replace_placeholder("{SERVICE_TYPE}", report_data["ServiceType"])
        self.report_builder.replace_placeholder("{SERVICE_LEAD}", report_data["ServiceLead"])
        self.report_builder.replace_placeholder("{MANAGEMENT_SUMMARY}", report_data["ManagementSummary"])
        self.report_builder.replace_placeholder("{SCOPE_DESCRIPTION}", report_data["Scope"])
        self.report_builder.replace_placeholder("{DURATION}", report_data["Duration"])
        self.report_builder.replace_placeholder("{REQUEST_ID}", report_data["RequestID"])

        if "Randstad" in report_data["Opco"]:
            self.report_builder.replace_placeholder("{OPCO}", report_data["Opco"])
        else:
            self.report_builder.replace_placeholder("{OPCO}", f"Randstad {report_data['Opco']}")

    def sort_vulnerability_by_severity(self):
        print("[INFO] Sorting vuln issues by severity")
        severity_order = ["Critical", "High", "Medium", "Low", "Info"]

        sorted_vulnerability_by_severity = []
        for severity in severity_order:
            for idx, vuln in enumerate(self.vuln_issues):
                if vuln["Severity"] == severity:
                    sorted_vulnerability_by_severity.append(vuln)

        self.vuln_issues = sorted_vulnerability_by_severity

    def yield_filled_templates_finding(self):
        print("[INFO] Yielding filled template findings: TemplateFinding.html")

        for idx, vuln_data in enumerate(self.vuln_issues):
            current_finding_number = idx + 1
            chapter = 4 if self.vuln_issues else 3

            finding_template_builder = ReportBuilder(self.finding_template_file, self.page)
            finding_template_builder.load_template()
            finding_template_builder.replace_placeholder("{FINDING_TITLE}", vuln_data["Title"])
            finding_template_builder.replace_placeholder("{FINDING_NUM}", f"{chapter}.{current_finding_number}")
            finding_template_builder.replace_placeholder("{FINDING_SUBNUM1}", f"{chapter}.{current_finding_number}.1")
            finding_template_builder.replace_placeholder("{FINDING_SEVERITY}",
                                                         get_severity_as_html(vuln_data["Severity"]))
            finding_template_builder.replace_placeholder("{FINDING_STATUS}", html_status_resolved(vuln_data["Status"]))
            try:
                finding_template_builder.replace_placeholder("{FINDING_DUE}", calculate_due_date(self, vuln_data))
            except UnboundLocalError as error:
                print(f"[ERROR] Couldn't calculate date for {vuln_data['Title']} with severity "
                      f"{vuln_data['Severity']}\nUnboundLocalError: {error}. ")
            finding_template_builder.replace_placeholder("{FINDING_REF}", vuln_data["Name"])
            finding_template_builder.replace_placeholder("{FINDING_DESCRIPTION}", vuln_data["Finding"])

            if vuln_data["Attachments"]:
                for uuid, attachment in vuln_data["Attachments"].items():
                    finding_template_builder.replace_image_in_template_with_b64(uuid, attachment)

            yield finding_template_builder.get_template_content()

    def add_finding_to_report_template(self):
        print("[INFO] Adding findings to report template")
        filled_findings = ""
        for finding in self.yield_filled_templates_finding():
            filled_findings += finding

        if not filled_findings:
            filled_findings = "No new vulnerabilities were found during the engagement."

        self.report_builder.replace_placeholder("{FINDINGS}", filled_findings)

    def add_risk_table_to_report_template(self):
        def severity_counter_output(s_counter):
            if s_counter == 0:
                s_counter = "No findings"
            elif s_counter == 1:
                s_counter = "1 finding"
            else:
                s_counter = str(s_counter) + " findings"

            return s_counter

        print("[INFO] Adding risks  table to report template")

        risk_table = ""
        c_counter = h_counter = m_counter = l_counter = i_counter = 0
        for vuln in self.vuln_issues:
            if vuln["Severity"] == "Critical":
                c_counter = c_counter + 1
            if vuln["Severity"] == "High":
                h_counter = h_counter + 1
            if vuln["Severity"] == "Medium":
                m_counter = m_counter + 1
            if vuln["Severity"] == "Low":
                l_counter = l_counter + 1
            if vuln["Severity"] == "Info":
                i_counter = i_counter + 1

        c_counter = severity_counter_output(c_counter)
        h_counter = severity_counter_output(h_counter)
        m_counter = severity_counter_output(m_counter)
        l_counter = severity_counter_output(l_counter)
        i_counter = severity_counter_output(i_counter)

        risk_table_template_builder = ReportBuilder(self.risk_template_file, self.page)
        risk_table_template_builder.load_template()
        risk_table_template_builder.replace_placeholder("{RISKSUMMARY_CRITICAL}", c_counter)
        risk_table_template_builder.replace_placeholder("{RISKSUMMARY_HIGH}", h_counter)
        risk_table_template_builder.replace_placeholder("{RISKSUMMARY_MEDIUM}", m_counter)
        risk_table_template_builder.replace_placeholder("{RISKSUMMARY_LOW}", l_counter)
        risk_table_template_builder.replace_placeholder("{RISKSUMMARY_INFO}", i_counter)

        risk_table += risk_table_template_builder.get_template_content()
        self.report_builder.replace_placeholder("{RISKS_SUMMARY}", risk_table)

    def add_finding_table_to_report_template(self):
        print("[INFO] Adding findings table to report template")
        findings_table = ""
        for vuln in self.vuln_issues:
            findings_table_template_builder = ReportBuilder(self.finding_table_template_file, self.page)
            findings_table_template_builder.load_template()

            findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_TITLE}", vuln["Title"])
            findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_SEVERITY}",
                                                                get_severity_as_html(vuln["Severity"]))
            findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_STATUS}",
                                                                html_status_resolved(vuln["Status"]))
            try:
                findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_DUE}",
                                                                    calculate_due_date(self, vuln))
            except UnboundLocalError as error:
                print(f"[ERROR] Couldn't calculate date for {vuln['Title']} with severity {vuln['Severity']}."
                      f"Due date set to -\nUnboundLocalError: {error}. ")
                findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_DUE}", "-")

            findings_table += findings_table_template_builder.get_template_content()

        if not findings_table:
            findings_table_template_builder = ReportBuilder(self.finding_table_template_file, self.page)
            findings_table_template_builder.load_template()
            findings_table_template_builder.load_template()

            findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_TITLE}", "No findings")
            findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_SEVERITY}", "-")
            findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_STATUS}", "-")
            findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_DUE}", "-")
            findings_table += findings_table_template_builder.get_template_content()

        self.report_builder.replace_placeholder("{FINDINGS_SUMMARY}", findings_table)

    def add_methodology_template(self):
        print("[INFO] Adding methodology description report template")
        methodology_description = ""
        methodology_description_template_builder = ReportBuilder(self.methodology_file, self.page)
        methodology_description_template_builder.load_template()
        methodology_description += methodology_description_template_builder.get_template_content()

        self.report_builder.replace_placeholder("{METHODOLOGY}", methodology_description)

    def add_findings_due_table_report_template(self):
        print("[INFO] Adding findings due table to report template")
        due_findings_table = ""
        for vuln in self.vuln_issues:
            due_findings_table_template_builder = ReportBuilder(self.finding_due_table_template_file, self.page)
            due_findings_table_template_builder.load_template()
            due_findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_TITLE}", vuln["Title"])
            due_findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_SEVERITY}",
                                                                    get_severity_as_html(vuln["Severity"]))
            try:
                due_findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_DUE}",
                                                                        calculate_due_date(self, vuln))
            except UnboundLocalError as error:
                print(f"[ERROR] Couldn't calculate date for {vuln['Title']} with severity {vuln['Severity']}. "
                      f"Due date set to -\nUnboundLocalError: {error}. ")
                due_findings_table_template_builder.replace_placeholder("{FINDINGSUMMARY_DUE}", "-")

            due_findings_table += due_findings_table_template_builder.get_template_content()
        self.report_builder.replace_placeholder("{FINDINGS_DUE_SUMMARY}", due_findings_table)

        if not due_findings_table:
            due_findings_table_template_builder = ReportBuilder(self.finding_due_table_template_file, self.page)
            due_findings_table_template_builder.load_template()
            due_findings_table_template_builder.replace_placeholder('{FINDINGSUMMARY_TITLE}', "No findings")
            due_findings_table_template_builder.replace_placeholder('{FINDINGSUMMARY_SEVERITY}', "-")
            due_findings_table_template_builder.replace_placeholder('{FINDINGSUMMARY_DUE}', "-")

            due_findings_table += due_findings_table_template_builder.get_template_content()
            self.report_builder.replace_placeholder("{FINDINGS_DUE_SUMMARY}", due_findings_table)

    def add_appendix_template(self):
        print("[INFO] Adding appendix to the report template")

        appendix_description = ""
        appendix_description_template_builder = ReportBuilder(self.appendix_file, self.page)
        appendix_description_template_builder.load_template()
        appendix_description += appendix_description_template_builder.get_template_content()

        self.report_builder.replace_placeholder("{APPENDIX}", appendix_description)

    def write_report_output_folder(self):
        report_output_location = None
        if self.pentest_info:
            app_name = self.pentest_info.get("Scope", None)
            report_name = self.pentest_info["Name"]
            report_status = self.pentest_info["Status"]

            now = datetime.now()
            output_file_name = f"{report_name}-{report_status}-{now.strftime('%Y-%m')}"
            output_file_name = f"{slugify_file_name(output_file_name)}.html"

            report_output_location = os.path.join(self.output_folder, output_file_name)

        self.page.snack_bar.content = ft.Text(f"Writing report to: {report_output_location}")
        self.page.snack_bar.bgcolor = ft.Colors.GREEN_400
        self.page.snack_bar.open = True
        print(f"[INFO] Writing report to {report_output_location}")
        template_content = self.report_builder.get_template_content()

        with open(report_output_location, "w", encoding="utf-8") as report_output_file:
            report_output_file.write(template_content)

        self.output_path = report_output_location
        if hasattr(self.page, "html_path_text"):
            self.page.html_file_path = self.output_path
            self.page.html_path_text.value = self.output_path
            self.page.update()


class ReportBuilder:
    def __init__(self, template_path, page):
        self.page = page
        self.page.app_state = page.app_state
        self.template_path = template_path
        self.template_content = None
        self.output_folder = None
        self.output_path = None

    def load_template(self):
        # Check if the template file exists
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"[ERROR] Template file not found: {self.template_path}")

        # Load the template content
        with open(self.template_path, 'r') as f:
            self.template_content = f.read()

    def replace_placeholder(self, placeholder, new_value):
        self.template_content = self.template_content.replace(placeholder, new_value)

    def replace_image_in_template_with_b64(self, uuid, attachment):
        self.template_content = re.sub("https.*(%s)" % uuid, "data:image/png;base64,%s" % attachment,
                                       self.template_content)

    def get_template_content(self):
        return self.template_content





