from core.form_core import (
    get_form_html,
    extract_entries,
    prepare_form_data
)
from core.form_submitters import submit_form_basic
from config.values_loader import values

from config.env import FORM_VIEW_URL, FORM_POST_URL


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


class StepError(Exception):
    pass


def main(use_filter: bool = False, group: int = 4):
    try:
        html = get_form_html(FORM_VIEW_URL)
        entries = extract_entries(html)
        form_data = prepare_form_data(entries, values)

        if use_filter:
            form_data = filter_form_data_by_group(form_data, group)

        success = submit_form_basic(FORM_POST_URL, form_data)
        if not success:
            raise StepError("Error al enviar el formulario")

        print("✅ Formulario enviado correctamente")

    except StepError as e:
        print(f"⚠️ Proceso detenido: {e}")


if __name__ == "__main__":
    # Comentar - Descomentar el main adecuado
    # main(use_filter=True, group=4)
    main()


