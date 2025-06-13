from yaml import load, CLoader
import os
from src import app_state

base_dir = os.path.dirname(os.path.abspath(__file__))

SERVICE_TYPE_MAP = {
    1: "adversarySimulation",
    2: "blackBox",
    3: "whiteBox"
}


class ReportConfiguration:
    def __init__(self, basic_info_arguments, page):
        self.service_name = basic_info_arguments.service
        self.configuration = None
        self.configuration_file = os.path.join(base_dir, "config.json")
        self.report_config = None
        self.page = page
        self.page.app_state = app_state

    def load_configuration_file(self):
        configuration_file_path = {
            "Adversary Simulation": os.path.join(base_dir, "config_files", "advsimreport.yaml"),
            "Black Box": os.path.join(base_dir, "config_files", "blackboxreport.yaml"),
            "White Box": os.path.join(base_dir, "config_files", "whiteboxreport.yaml"),
        }

        self.configuration_file = configuration_file_path.get(self.service_name)

        if not self.configuration_file or not os.path.exists(self.configuration_file):
            print(f"[ERROR] --> Configuration file {self.configuration_file} not found.")

        with open(self.configuration_file, "r") as f:
            self.configuration = load(f, Loader=CLoader)

    def load_report_template(self):
        print("[INFO] Loading report template...")
        report_template_configuration = self.configuration["ReportTemplates"]
        self.report_template_file = report_template_configuration["reportTemplateFile"]
        self.risk_table_template_file = report_template_configuration["riskTableTemplateFile"]
        self.finding_table_template_file = report_template_configuration["findingTableTemplateFile"]
        self.finding_due_table_template_file = report_template_configuration["findingDueTableTemplateFile"]
        self.finding_template_file = report_template_configuration["findingTemplateFile"]
        self.methodology_file = report_template_configuration["methodologyFile"]
        self.appendix_file = report_template_configuration["appendixFile"]
        self.report_output_folder = self.configuration["ReportOutputFolder"]

    def load_due_date(self):
        print("[INFO] Loading time to solve days")
        self.info_sla = self.configuration["infoDueDate"]
        self.low_sla = self.configuration["lowDueDate"]
        self.medium_sla = self.configuration["mediumDueDate"]
        self.high_sla = self.configuration["highDueDate"]
        self.critical_sla = self.configuration["criticalDueDate"]

    def load_configuration(self):
        self.load_configuration_file()
        self.load_report_template()
        self.load_due_date()
