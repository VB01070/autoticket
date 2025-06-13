from docx import Document
from docx.oxml.ns import qn
import base64


def parse_findings(docx_path):
    doc = Document(docx_path)
    findings = []
    metadata_data = {"org": "", "asset": "", "test": ""}
    current_finding = None
    current_section = None
    on_metadata_page = True
    image_buffer = []
    collecting_images = False

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        # ——— grab images first, even on empty-text paras ———
        if collecting_images:
            # find any <*-blip> element by local-name()
            for blip in paragraph._element.xpath('.//*[local-name()="blip"]'):
                # get the r:embed attribute via qn()
                rId = blip.get(qn('r:embed'))
                if rId and rId in doc.part.related_parts:
                    blob = doc.part.related_parts[rId].blob
                    b64 = base64.b64encode(blob).decode('utf-8')
                    image_buffer.append(b64)
        # ——————————————————————————————————————————————

        # metadata page?
        if on_metadata_page:
            if text.startswith("## Organization UUID"):
                metadata_data["org"] = text.split("## Organization UUID", 1)[1].strip()
            elif text.startswith("## Asset UUID"):
                metadata_data["asset"] = text.split("## Asset UUID", 1)[1].strip()
            elif text.startswith("## Test UUID"):
                metadata_data["test"] = text.split("## Test UUID", 1)[1].strip()
            elif text.startswith("### Title"):
                on_metadata_page = False
                current_finding = {"title": "", "severity": "", "note": "", "screenshots": []}
                current_section = "title"
                current_finding["title"] = text.split("### Title", 1)[1].strip()

        else:
            # skip empties (we already pulled images)
            if not text:
                continue

            if text.startswith("### Title"):
                if current_finding:
                    current_finding["screenshots"] = image_buffer
                    findings.append(current_finding)
                    image_buffer = []
                current_finding = {"title": "", "severity": "", "note": "", "screenshots": []}
                current_section = "title"
                current_finding["title"] = text.split("### Title", 1)[1].strip()
                collecting_images = False

            elif text.startswith("### Severity"):
                current_section = "severity"
                current_finding["severity"] = text.split("### Severity", 1)[1].strip()
                collecting_images = False

            elif text.startswith("### Note"):
                current_section = "note"
                current_finding["note"] = text.split("### Note", 1)[1].strip()
                collecting_images = False

            elif text.startswith("### Images"):
                collecting_images = True

            else:
                if current_section == "title":
                    current_finding["title"] += "\n" + text
                elif current_section == "severity":
                    current_finding["severity"] += "\n" + text
                elif current_section == "note":
                    current_finding["note"] += "\n" + text

    # finalize last one
    if current_finding:
        current_finding["screenshots"] = image_buffer
        findings.append(current_finding)

    # debug
    print(f"[DEBUG] Total findings: {len(findings)}")
    for idx, f in enumerate(findings, 1):
        print(f"[DEBUG] Finding {idx} has {len(f['screenshots'])} image(s)")

    return findings, metadata_data
