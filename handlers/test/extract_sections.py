from bs4 import BeautifulSoup
from typing import Dict


def extract_sections(page, html):
    soup = BeautifulSoup(html, 'html.parser')
    sections: Dict[str, str] = {}

    for name in ("Description", "Impact", "Recommendation"):
        heading = soup.find("strong", string=name)
        if not heading:
            continue

        h1 = heading.find_parent("h1")
        if not h1:
            continue

        parts = []
        for sib in h1.next_siblings:
            if getattr(sib, "name", None) == "h1":
                break
            parts.append(str(sib))

        text = BeautifulSoup("".join(parts), "html.parser") \
            .get_text(separator=" ", strip=True)
        sections[name] = text


    return sections
