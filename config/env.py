import os
from dotenv import load_dotenv

load_dotenv()

FORM_VIEW_URL = os.getenv("FORM_VIEW_URL")
FORM_POST_URL = os.getenv("FORM_POST_URL")

if not FORM_VIEW_URL or not FORM_POST_URL:
    raise RuntimeError("❌ Variables de entorno no configuradas")
