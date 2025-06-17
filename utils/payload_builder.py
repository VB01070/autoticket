from time import sleep
import filetype
import base64
import flet as ft
from handlers.migration.holding_process import run_all_process


GLOBAL_REMEDIATION_OWNER_TAG = "3507ea67-dc17-49ed-aea4-30abc7376f3c"


def severity_to_cvss(sev: str) -> str:
    sev = sev.lower()
    return {
        "critical": "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "high":     "CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N",
        "medium":   "CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N",
        "low":      "CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:P/A:N",
        "info":     "CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:N/A:N"
    }.get(sev, "CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:N/A:N")


def build_payload(finding, ai_data, uuids, cvss_data, vuln_type_name):
    print(f"FINDINGS: {type(ai_data)} - {len(ai_data)}")
    print(f"FINDINGS: {ai_data}")
    details_html = ""  # clean details, every bloody time

    details_html += f"""
<h1><span style="color:#2175d9"><strong>Description</strong></span></h1>
<p><span style="color:#000000">{ai_data.get('description', '')}</span></p>
<h1><span style="color:#2175d9"><strong>Impact</strong></span></h1>
<p><span style="color:#000000">{ai_data.get('impact', '')}</span></p>
<h1><span style="color:#2175d9"><strong>Recommendation</strong></span></h1>
<p><span style="color:#000000">{ai_data.get('recommendation', '')}</span></p>
<h1><span style="color:#2175d9"><strong>References &amp; Additional Resources</strong></span></h1>
<ul>
"""

    references = ai_data.get("references", "")
    refs = []

    if isinstance(references, str):
        refs = references.splitlines()

    elif isinstance(references, list):
        for item in references:
            if isinstance(item, str):
                refs.append(item.strip())
            elif isinstance(item, dict):
                if "source" in item and "url" in item:
                    label = item["source"].strip()
                    url = item["url"].strip()
                    refs.append(f"{label}: {url}")
                else:
                    for label, value in item.items():
                        if isinstance(value, dict) and "url" in value:
                            name = value.get("name", label).strip()
                            url = value["url"].strip()
                            refs.append(f"{name}: {url}")
                        elif isinstance(value, str):
                            refs.append(f"{label.strip()}: {value.strip()}")
                        else:
                            refs.append(f"{label}: {value}")

    elif isinstance(references, dict):
        for label, url in references.items():
            refs.append(f"{label.strip()}: {url.strip()}")

    for ref in refs:
        details_html += f'\t<li>{ref}</li>\n'

    screenshots = finding.get("screenshots", [])
    if screenshots:
        details_html += f"</ul>\n<h1><span style=\"color:#2175d9\"><strong>Screenshots</strong></span></h1>"
        for i, img_b64 in enumerate(screenshots):
            img_bytes = base64.b64decode(img_b64)
            kind = filetype.guess_mime(img_bytes)
            mime_type = kind if kind else "image/png"
            # mime = imghdr.what(None, h=img_bytes) or "png"
            # mime_type = f"image/{mime}"
            details_html += '<figure class="image">'
            details_html += f'<img alt="" databorder="" src="data:{mime_type};base64,{img_b64}" />'
            details_html += '<figcaption data-placeholder="Caption"></figcaption></figure>'

    return {
        "asset": uuids["asset"],
        "vulnerability_type": uuids["vuln_type"],
        "context": uuids["context"],
        "test": uuids["test"],
        "all_tests": False,
        "severity": cvss_data.get("severity", finding["severity"]).strip().lower(),
        "description": finding["title"].strip(),
        "details": details_html.lstrip(),
        "ready_to_publish": True,
        "cvss_vector": cvss_data.get("vector", ""),
        "authenticated": False,
        "language": "",
        "template": "",
        "tags": [""]
    }


def migration_payload_builder(page, migration_vulns):
    if not migration_vulns:
        page.snack_bar.content = ft.Text(f"No vulnerabilities selected")
        page.snack_bar.bgcolor = ft.Colors.RED_400
        page.snack_bar.open = True
        page.update()
        return

    final_payloads = []

    for item in migration_vulns:
        vulns_payload = {
            "asset": item["target_asset_uuid"],
            "vulnerability_type": item["vuln_type_uuid"],
            "context": item["context_uuid"],
            "all_tests": False,
            "severity": item["severity"].strip().lower(),
            "description": f"{item['description']} - {item['organisation_name'].upper()}",
            "details": item["details"],
            "ready_to_publish": True,
            "cvss_vector": (item["cvss_vector"]),
            "authenticated": False,
            "language": "",
            "template": "",
            "tags": [GLOBAL_REMEDIATION_OWNER_TAG]
        }

        final_payloads.append(vulns_payload)


    run_all_process(page, final_payloads)


