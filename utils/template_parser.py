from bs4 import BeautifulSoup
import re
from logs.logger import logger


def clean_text(text):
    return text.replace(u'\xa0', ' ').strip().lower()


def extract_sections_from_template(html: str):
    soup = BeautifulSoup(html, "html.parser")
    sections = {"description": "", "impact": "", "recommendation": ""}
    section_map = {
        "description": "description",
        "impact": "impact",
        "recommendation": "recommendation"
    }

    current_section = None
    collected = {k: [] for k in sections}

    for tag in soup.find_all(True):
        if tag.name == "h1":
            header_text = clean_text(tag.get_text())

            # Switch section if header matches known section
            matched = False
            for key in section_map:
                if section_map[key] in header_text:
                    current_section = key
                    matched = True
                    logger.debug(f"Switching to section: {key}")
                    break

            # If unrelated header found, stop section
            if not matched and current_section:
                logger.debug(f"Ending section capture due to unrelated header: {header_text}")
                current_section = None

            continue

        # Collect content under current section
        if current_section and tag.name not in ["h1", "script", "style"]:
            tag_text = tag.get_text(separator="\n", strip=True)
            tag_text = re.sub(r'\s+', ' ', tag_text).strip()
            if tag_text:
                normalized = clean_text(tag_text)
                if (
                    normalized != current_section
                    and not (normalized.startswith("[") and normalized.endswith("]"))
                ):
                    collected[current_section].append(tag_text)

    # Clean up duplicates and set final content
    for key in collected:
        lines = collected[key]
        seen = set()
        unique_lines = []
        for line in lines:
            normalized = clean_text(line)
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique_lines.append(line.strip())

        content = "\n".join(unique_lines).strip()
        content = "\n".join(
            line for line in content.splitlines()
            if not (line.strip().startswith("[") and line.strip().endswith("]"))
        ).strip()

        sections[key] = content

    return sections



