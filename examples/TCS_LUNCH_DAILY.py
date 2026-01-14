from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import re


FORM_VIEW_URL = "https://docs.google.com/forms/d/e/1FAIpQLSebAR7SAmwvpQ06lxJba62HSS7E1UrDR2mhYyG-BEuHqoehJg/viewform"
FORM_POST_URL = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSebAR7SAmwvpQ06lxJba62HSS7E1UrDR2mhYyG-BEuHqoehJg/formResponse"

VALUES = [
    "2952297", "Martin Fierro", 
    "Torres Castillo", "Torres Castillo", "Torres Castillo", "Torres Castillo", "Torres Castillo",
    "Almuerzo", "Almuerzo", "Almuerzo", "Almuerzo", "Almuerzo",
    "Completo", "Completo", "Completo", "Completo", "Completo"
]


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
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
    for match in re.findall(r'entry\.\d{10}', html):
        if match not in entries:
            entries[match] = ""
    return entries


@handle_error
def prepare_form_data(entries: dict, values: list) -> dict:
    matches = []
    for k in entries.keys():
        matches.extend(re.findall(r'entry\.\d{8,12}', k))
    unique_entries = list(dict.fromkeys(matches))
    print(unique_entries)
    return {entry: values[i] if i < len(values) else "" for i, entry in enumerate(unique_entries)}

def filter_form_data_by_group(data: dict, n: int) -> dict:
    if not 1 <= n <= 5:
        raise ValueError("El parámetro n debe estar entre 1 y 5")

    keys = list(data.keys())

    if len(keys) < 2:
        raise ValueError("Se requieren al menos 2 elementos iniciales")

    # Siempre incluir los primeros 2
    selected_keys = keys[:2]

    remaining = keys[2:]

    for i in range(0, len(remaining), 5):
        group = remaining[i:i + 5]

        if len(group) < 5:
            raise ValueError(
                f"Grupo incompleto en la posición {i // 5 + 1}: "
                f"esperados 5 elementos, encontrados {len(group)}"
            )

        selected_keys.append(group[n - 1])  # n es 1-based

    return {k: data[k] for k in selected_keys}


@handle_error
def submit_form(url: str, form_data: dict) -> bool:
    response = requests.post(url, data=form_data)
    return response.status_code == 200


class StepError(Exception):
    pass


def main():
    try:
        html = get_form_html(FORM_VIEW_URL)
        if not html:
            raise StepError("No se pudo obtener el HTML del formulario")

        entries = extract_entries(html)
        if not entries:
            raise StepError("No se encontraron entradas válidas")

        form_data = prepare_form_data(entries, VALUES)
        if not form_data:
            raise StepError("Error al preparar datos del formulario")

        filtered = filter_form_data_by_group(form_data, 3)

        print(form_data)
        print("-----------------")
        print(filtered)
        success = submit_form(FORM_POST_URL, filtered)
        if not success:
            raise StepError("Error al enviar el formulario")
        print("✅ Formulario enviado correctamente")

    except StepError as e:
        print(f"⚠️ Proceso detenido: {e}")



if __name__ == "__main__":
    main()
