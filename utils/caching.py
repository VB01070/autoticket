import os
import pickle
import requests
import time
from utils.manage_keys import get_credential
from utils.template_parser import extract_sections_from_template
from logs.logger import logger

CACHE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cache", "data_cache.pkl"))
BASE_URL = "https://randstad.eu.vulnmanager.com"


def get_headers():
    api_key = get_credential("DashboardAPIKey")
    return {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }


def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)
    return {
        "contexts": [],
        "vuln_types": {}
    }


def save_cache(data):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(data, f)


def merge_items(existing, new_items, key="uuid"):
    existing_uuids = {item[key] for item in existing}
    return existing + [item for item in new_items if item[key] not in existing_uuids]


def fetch_context():
    url = f"{BASE_URL}/api/v3/provider/contexts"
    payload = {}
    all_items = []
    page = 1

    while True:
        api_url = f"{url}?page={page}"
        response = requests.post(api_url, headers=get_headers(), json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            all_items.extend([{"uuid": ctx["uuid"], "name": ctx["name"]} for ctx in data.get("items", [])])
        else:
            if response.status_code in (400, 401) and page == 1:
                logger.error("API key expired or invalid")
                raise ValueError("API key expired or invalid")
            break
        page += 1

    return all_items


def fetch_vuln_types_for_context(context_uuid):
    url = f"{BASE_URL}/api/v3/provider/vulnerability-types"
    payload = {"contexts": [context_uuid], "enabled": True}
    all_items = []
    page = 1

    while True:
        api_url = f"{url}?page={page}"
        response = requests.post(api_url, headers=get_headers(), json=payload)

        if response.status_code == 200:
            data = response.json()
            all_items.extend([
                {
                    "uuid": vt["uuid"],
                    "name": vt["name"],
                    "context_uuid": context_uuid
                } for vt in data.get("items", [])
            ])
        elif response.status_code == 400 and page == 1:
            logger.error("Check the API key.")
            exit(1)
        else:
            break

        page += 1

    return all_items


def fetch_template_for_vuln_type(vuln_type_uuid):
    url = f"{BASE_URL}/api/v3/provider/templates"
    payload = {"vulnerability_types": [vuln_type_uuid]}
    try:
        response = requests.post(url, headers=get_headers(), json=payload)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            if items:
                html = items[0].get("templates", {}).get("en", {}).get("template")
                if html:
                    return extract_sections_from_template(html)  # return a dict now
    except Exception as e:
        logger.exception(f"Failed fetching template for {vuln_type_uuid}: {e}")
    return None


def fetch_contexts_and_vuln_types():
    logger.debug("Fetching contexts and their vulnerability types...")
    cache = load_cache()
    contexts = fetch_context()
    cache["contexts"] = contexts
    cache["vuln_types"] = {}

    for ctx in contexts:
        vuln_types = fetch_vuln_types_for_context(ctx["uuid"])

        for vt in vuln_types:
            vt["template_text"] = fetch_template_for_vuln_type(vt["uuid"]) or ""

        cache["vuln_types"][ctx["uuid"]] = vuln_types

    save_cache(cache)
    logger.debug("Context + Vuln Type + Templates fetching complete.")


def initial_fetch_all():
    start = time.time()
    fetch_contexts_and_vuln_types()
    end = time.time()
    execution_time = end - start
    logger.info(f"Execution time: {execution_time:.2f}s")