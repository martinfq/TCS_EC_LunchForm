import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
_JSON_PATH = PROJECT_ROOT / "values.json"




def _load_values(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)



def _transform_values(data: dict, repeat: int = 5) -> list:
    return (
        [data["ULTIMATIX"], data["NOMBRE"]]
        + [data["EDIFICIO"]] * repeat
        + [data["TIPO"]] * repeat
        + [data["MENU"]] * repeat
    )



# 🔥 ÚNICO OBJETO EXPORTADO
values = _transform_values(_load_values(_JSON_PATH))
