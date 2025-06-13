from utils.manage_keys import get_credential
from utils.caching import BASE_URL
import flet as ft
import requests
from datetime import datetime, timezone, timedelta
from html2text import HTML2Text
import re
import base64


class Fetcher:
    def __init__(self, basic_info, configuration, page):
        self.page = page
        self.page.app_state = page.app_state
        self.x_api_key = get_credential("DashboardAPIKey")
        self.basic_info = basic_info
        self.configuration = configuration

    def get_headers(self, resource):
        if resource == "attachment":
            header = {"x-api-key": self.x_api_key}
        else:
            header = {
                "Content-Type": "application/json",
                "x-api-key": self.x_api_key
            }

        return header

    def get_test_information(self, uuid):
        endpoint = "/api/v3/tests"
        url = f"{BASE_URL}{endpoint}"
        payload = {"uuid": [uuid]}

        response = requests.post(url, headers=self.get_headers("tests"), json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[EXCEPTION FETCHING TESTS ERROR] Status code: {response.status_code} - {response.text}")
            return False

    def get_vulnerabilities_for_test_information(self, uuid):
        endpoint = "/api/v3/vulnerabilities"
        url = f"{BASE_URL}{endpoint}"
        payload = {"tests": [uuid]}

        try:
            response = requests.post(url, headers=self.get_headers("vulnerabilities"), json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[EXCEPTION FETCHING VULNERABILITIES FOR TESTS]: {e}")
            return False

    def get_assets_for_test(self, uuid):
        endpoint = "/api/v3/assets"
        url = f"{BASE_URL}{endpoint}"
        payload = {"tests": [uuid]}

        try:
            response = requests.post(url, headers=self.get_headers("assets"), json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get("items", [])
            else:
                print(f"[ERROR] Couldn't fetch assets: {response.status_code}")
                return []
        except Exception as e:
            print(f"[EXCEPTION FETCHING ASSETS]: {e}")
            return []

    def get_vulnerability_information(self, uuid):
        endpoint = "/api/v3/vulnerabilities"
        url = f"{BASE_URL}{endpoint}"
        payload = {"uuid": [uuid]}

        try:
            response = requests.post(url, headers=self.get_headers("vulnerabilities"), json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[EXCEPTION FETCHING VULNERABILITY]: {e}")
            return False

    def get_b64_from_attachment(self, attachment_metadata):
        """
        Uses the provided attachments metadata (from vuln_information["attachments"])
        to fetch the actual list of attachments, then downloads each one and encodes it.
        """
        b64_encoded_content = {}

        list_url = f"{BASE_URL}{attachment_metadata['url']}"
        try:
            response = requests.post(
                list_url,
                headers=self.get_headers("attachment"),
                json=attachment_metadata["body"],
                timeout=30
            )
            if response.status_code != 200:
                print(f"[ERROR] Failed to fetch attachment list: {response.status_code}")
                return {}

            attachment_items = response.json().get("items", [])
            for attachment in attachment_items:
                attachment_url = attachment.get("url", "")
                match = re.search(r"/attachments/([0-9a-f\-]{36})", attachment_url)
                if not match:
                    print(f"[WARNING] Could not extract UUID from: {attachment_url}")
                    continue

                attachment_uuid = match.group(1)
                binary_data = self.get_attachments(attachment_uuid)
                if binary_data:
                    b64_encoded_content[attachment_uuid] = base64.b64encode(binary_data).decode("utf-8")

        except Exception as e:
            print(f"[EXCEPTION FETCHING ATTACHMENTS LIST]: {e}")

        return b64_encoded_content

    def get_attachments(self, uuid):
        """
        Fetches the binary content of a single attachment by UUID.
        """
        endpoint = f"/api/v3/attachments/{uuid}"
        url = f"{BASE_URL}{endpoint}"

        try:
            response = requests.get(url, headers=self.get_headers("attachment"), timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                print(f"[ERROR] Failed to fetch attachment {uuid}: {response.status_code}")
                return None
        except Exception as e:
            print(f"[EXCEPTION FETCHING ATTACHMENT]: {e}")
            return None

    def prepare_report_builder(self):
        now = datetime.now()
        if not self.basic_info.args.pentest:
            self.page.snack_bar.content = ft.Text("No test UUID provided")
            self.page.snack_bar.bgcolor = ft.Colors.RED_400
            self.page.snack_bar.icon = ft.Icons.ERROR
            self.page.snack_bar.open = True

        # Getting test, vuln info
        test_api_response = self.get_test_information(self.basic_info.args.pentest)
        if not test_api_response or "items" not in test_api_response or not test_api_response["items"]:
            print("[ERROR] No test data found.")
            return False

        test_data = test_api_response["items"][0]
        vuln_test_data = self.get_vulnerabilities_for_test_information(self.basic_info.args.pentest)

        # Managing starting and ending date of the test
        if self.basic_info.args.test_start:
            test_data["started_at"] = self.basic_info.args.test_start
        else:
            test_data["started_at"] = (datetime.fromisoformat(test_data["started_at"]).astimezone(timezone.utc)
                                       .strftime("%d-%m-%Y"))

        if self.basic_info.args.test_end:
            test_data["ended_at"] = self.basic_info.args.test_end
        else:
            if not test_data["ended_at"]:
                test_data["ended_at"] = datetime.today().strftime("%d-%m-%Y")
            else:
                test_data["ended_at"] = (datetime.fromisoformat(test_data["ended_at"]).astimezone(timezone.utc)
                                         .strftime("%d-%m-%Y"))

        # Calculation of the duration of the test in days

        test_start = datetime.strptime(test_data["started_at"], "%d-%m-%Y")
        test_end = datetime.strptime(test_data["ended_at"], "%d-%m-%Y")

        # initializing business days count
        test_duration = 0

        # looping through each day in the date range
        current_date = test_start
        while current_date <= test_end:
            # checking if the current day is a weekday
            if current_date.weekday() < 5:
                test_duration += 1
            # incrementing the current day by one day
            current_date += timedelta(days=1)

        # Map service to service leader
        if self.basic_info.args.service == "Adversary Simulation":
            test_data["service_type"] = "Adversary Simulation"
            test_data["service_lead"] = "Rodrigo Magalhaes"
        if self.basic_info.args.service == "Black Box":
            test_data["service_type"] = "Black/Grey Box"
            test_data["service_lead"] = "Leandro Jales"
        if self.basic_info.args.service == "White Box":
            test_data["service_type"] = "White Box"
            test_data["service_lead"] = "Timothy Tjen A Looi"

        ## Mapping KISS24 values to Randstad pentest naming
        test_data["state"] = "Final" if (test_data["state"] == "Tested") else "Concept"

        # To remove html tags
        config = HTML2Text()
        config.body_width = 0  # disable line wrapping
        _txt = config.handle(test_data["details"])

        # Getting SNow request ID
        service_now_request_id = re.search(r"ServiceNow Request ID: ([^\s\t\n\r]+)", _txt)
        if service_now_request_id:
            service_now_request_id = service_now_request_id.group(1)
        else:
            service_now_request_id = "N/A"
            print("[!] ServiceNow Request ID not found.")

        # Extract content after "[MANAGEMENT SUMMARY]" using regex
        management_summary_content = re.search(r"[\[{]MANAGEMENT SUMMARY[\]}].*?[\s\t\r\n]+(.*)", _txt,
                                               re.DOTALL | re.I)

        # Check if the regex match was successful
        if management_summary_content:
            management_summary_content = management_summary_content.group(1)
        else:
            management_summary_content = "To Do"
            print("[!] Management summary content not found.")

        # Getting asset name
        assets = self.get_assets_for_test(self.basic_info.args.pentest)
        if assets:
            asset_name = assets[0].get("name", "Unknown")
        else:
            asset_name = "Unknown"

        return_array = {
            "pentestInformation": {
                "Name": test_data['id'],
                "Status": test_data['state'],
                "Year": str(now.year),
                "Start": test_data['started_at'],
                "End": test_data['ended_at'],
                "Authors": "Global Offensive Security Team",
                "ServiceType": test_data['service_type'],
                "ServiceLead": test_data['service_lead'],
                "ManagementSummary": management_summary_content,
                "Scope": asset_name,
                "LastModified": now.strftime("%Y-%m-%d"),
                "Opco": test_data['organisation']['name'],
                "Duration": "{} {}".format(test_duration, 'days' if test_duration > 1 else 'day'),
                "RequestID": service_now_request_id
            },
            "vulnerabilities": {}
        }

        vuln_items = vuln_test_data.get("items", []) if isinstance(vuln_test_data, dict) else []
        for index, vuln in enumerate(vuln_items):
            vuln_information = self.get_vulnerability_information(vuln["uuid"])
            vuln_information = vuln_information.get("items", [])[0]

            if vuln_information["attachments"]:
                attachments_information = self.get_b64_from_attachment(vuln_information["attachments"])
            else:
                attachments_information = []

            ## Mapping KISS24 values to Randstad vuln naming
            vuln_information["state"] = "Open" if (vuln["state"] == "New") else vuln["state"]

            ## Cleaning up styles from KITS24 details
            vuln_information["details"] = re.sub('<span style=".*?">', '', vuln_information["details"])
            vuln_information["details"] = re.sub('</span>', '', vuln_information["details"])

            return_array["vulnerabilities"][index] = {
                "Name": vuln['id'],
                "Year": str(now.year),
                "Status": vuln_information['state'],
                "Severity": vuln_information['severity'],
                "Asset": vuln_information['asset']['name'],
                "Title": vuln_information['description'],
                "Type": vuln_information['vulnerability_type'],
                "Finding": vuln_information['details'],
                "PublishedAt": vuln_information['published_at'],
                "Impact": "",
                "Recommendation": "",
                "Attachments": attachments_information,
                "LastModified": now.strftime("%Y-%m-%d")
            }

        return return_array
