import difflib
from utils.alias_map import ALIAS_MAP


def normalize(text):
    return text.strip().lower()


def match_vuln_titles_to_cache(findings, cache):
    all_vuln_types = []
    for ctx in cache.get("contexts", []):
        for vt in cache.get("vuln_types", {}).get(ctx["uuid"], []):
            all_vuln_types.append({
                "context_uuid": ctx["uuid"],
                "vuln_type_uuid": vt["uuid"],
                "name": vt.get("display_name") or vt["name"]
            })

    matches = []
    for finding in findings:
        title = normalize(finding["title"])
        best_match = None
        best_score = 0.0

        # Check alias matches first
        for alias_key, synonyms in ALIAS_MAP.items():
            if alias_key in title:
                for vt in all_vuln_types:
                    vt_name = normalize(vt["name"])
                    if any(syn in vt_name for syn in synonyms):
                        match = vt.copy()
                        match["confidence"] = 1.0
                        matches.append(match)
                        break
                else:
                    continue
                break
        else:
            # Fallback to fuzzy match
            for vt in all_vuln_types:
                name = normalize(vt["name"])
                ratio = difflib.SequenceMatcher(None, title, name).ratio()
                if ratio > best_score:
                    best_score = ratio
                    best_match = vt

            if best_score >= 0.7:
                best_match = best_match.copy()
                best_match["confidence"] = best_score
                matches.append(best_match)
            else:
                matches.append(None)

    return matches
