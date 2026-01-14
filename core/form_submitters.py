# form_submitters.py
import requests
from core.form_core import handle_error


@handle_error
def submit_form_basic(url: str, form_data: dict) -> bool:
    response = requests.post(url, data=form_data)
    return response.status_code == 200
