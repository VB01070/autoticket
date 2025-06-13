from utils.caching import BASE_URL, get_headers
import flet as ft
import requests
import json
import re


GIS_UUID = "135a57f3-2fef-4980-b182-93e263890b19"


def migrate_vuln(page, payloads):
    new_vulns_uuid = []
    if not payloads:
        page.snack_bar.content = ft.Text(f"No Vulnerabilities has been selected.")
        page.snack_bar.bgcolor = ft.Colors.RED_400
        page.snack_bar.open = True
        page.update()
        return

    headers = get_headers()
    url = f"{BASE_URL}/api/v3/provider/vulnerabilities/{GIS_UUID}/create"

    for item in payloads:
        try:
            response = requests.post(url, headers=headers, json=item)
            if response.status_code == 200:
                page.snack_bar.content = ft.Text(f"Vulnerability successfully submitted!")
                page.snack_bar.bgcolor = ft.Colors.GREEN_400
                page.snack_bar.open = True
                page.update()
                data = json.loads(response.text)
                if "success" in data and data["success"]:
                    match = re.search(r"\(UUID:\s*([a-f0-9\-]+)\)", data["success"][0])
                    if match:
                        uuid = match.group(1)
                        new_vulns_uuid.append(uuid)
                        print(f"[+] New UUID extracted: {uuid}")
                    else:
                        print(f"[-] Failed to extract UUID from payload: {payloads}")
                else:
                    print("No success in response text")
            else:
                page.snack_bar.content = ft.Text(f"Upload Failed! Status: {response.status_code}")
                page.snack_bar.bgcolor = ft.Colors.RED_400
                page.snack_bar.open = True
                page.update()
                print(f"{response.status_code}: {response.text}")
        except Exception as ex:
            page.snack_bar.content = ft.Text(f"Error! Request failed: {ex}")
            page.snack_bar.bgcolor = ft.Colors.RED_400
            page.snack_bar.open = True
            page.update()
            print(ex)

