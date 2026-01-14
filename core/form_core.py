# form_core.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return wrapper


@handle_error
def get_form_html(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(2000)
        html = page.content()
        browser.close()
        return html


@handle_error
def extract_entries(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    entries = {
        tag.get("name"): tag.get("aria-label") or tag.get("placeholder") or ""
        for tag in soup.find_all(["input", "textarea", "select"])
        if tag.get("name") and tag.get("name").startswith("entry.")
    }

    for match in re.findall(r'entry\.\d{8,12}', html):
        if match not in entries:
            entries[match] = ""

    return entries


@handle_error
def prepare_form_data(entries: dict, values: list) -> dict:
    matches = []
    for k in entries.keys():
        matches.extend(re.findall(r'entry\.\d{8,12}', k))

    unique_entries = list(dict.fromkeys(matches))

    return {
        entry: values[i] if i < len(values) else ""
        for i, entry in enumerate(unique_entries)
    }
