from utils.caching import BASE_URL, get_headers
import requests


def get_vuln_list_data(test_uuid):
    body = {"tests": [test_uuid]}
    headers = get_headers()

    response = requests.post(f"{BASE_URL}/api/v3/vulnerabilities", headers=headers, json=body, verify=False)
    print(response.status_code)
    response.raise_for_status()
    items = response.json().get("items", [])

    filtered_items = [item for item in items if not item.get("published_at")]

    return [
        {
            "uuid": item.get("uuid"),
            "id": item.get("id"),
            "description": item.get("description"),
            "state": item.get("state"),
            "severity": item.get("severity")
        }
        for item in filtered_items
    ]

