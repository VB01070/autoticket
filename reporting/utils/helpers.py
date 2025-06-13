from datetime import datetime, date, timedelta
import unicodedata
import re


def get_severity_as_html(severity):

    if severity == "Info":
        return "<span id='info-f'>Info</span>"
    if severity == "Low":
        return "<span id='low-f'>Low</span>"
    if severity == "Medium":
        return "<span id='medium-f'>Medium</span>"
    if severity == "High":
        return "<span id='high-f'>High</span>"
    if severity == "Critical":
        return "<span id='critical-f'>Critical</span>"

    return severity


def html_status_resolved(status):
    if status == "Resolved":
        return "<span id='status_resolved_text'>Resolved</span>"

    return status


def calculate_due_date(config, vuln):
    severity = vuln["Severity"]
    days_to_add = 0

    if severity == "Info":
        days_to_add = config.info_sla
    if severity == "Low":
        days_to_add = config.low_sla
    if severity == "Medium":
        days_to_add = config.medium_sla
    if severity == "High":
        days_to_add = config.high_sla
    if severity == "Critical":
        days_to_add = config.critical_sla

    try:
        due_date = datetime.strptime(vuln["PublishedAt"], "%Y-%m-%dT%H:%M:%S%z")
    except:
        print(f"[WARNING] Vuln {vuln['Name']} is not published yet. Using Today's date as publish date.")
        due_date = date.today()

    while days_to_add > 0:
        due_date += timedelta(days=1)
        days_to_add -= 1

    return due_date.strftime("%d-%m-%Y")


def slugify_file_name(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '_', value)
    return re.sub(r'[-\s]+', '-', value).strip('-_')