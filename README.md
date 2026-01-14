# 📄 TCS Formulario Comida (Python)

Este proyecto automatiza el **proceso de obtención, preparación y envío de un formulario web** utilizando Python.

El flujo principal es:

1. Obtener el HTML del formulario
2. Extraer los campos (`entries`)
3. Preparar los datos con valores predefinidos
4. (Opcional) Filtrar los campos por grupo
5. Enviar el formulario vía HTTP POST

El comportamiento puede ejecutarse **con o sin filtrado**, según la configuración del `main`.

---
# ⚙️ Configuración del entorno

## Requisitos
- Python 3.9+
- Acceso a internet



##  Instalar dependencias

pip install -r requirements.txt


## 🧾 Archivo de valores

Los valores del formulario se cargan desde un archivo JSON -> values.json
{
  "ULTIMATIX": "2952297",
  "NOMBRE": "Martin Fierro",
  "EDIFICIO": "Torres Castillo",
  "TIPO": "Almuerzo",
  "MENU": "Completo"
}
### Instrucciones:
1. Reemplaza los valores de las claves con tu información personal.
2. Guarda el archivo después de hacer los cambios.
3. Reemplaza EDIFICIO, TIPO y MENU con su informacion correspondiente

VALORES PERMITIDOS:

EDIFICIO : Torres Castillo, Amazonas, Cafeteria AP, BGR

TIPO: Desayuno, Almuerzo, Cena

MENU: Completo, Vegano, Snack

## SEMANA COMPLETA o DÍA ESPECÍFICO

### Para ejecutar la semana completa (sin filtro)

python main.py


Envía todos los campos del formulario sin modificaciones.

### Para ejecutar un dia especifico
Cambiar en el codigo ->
main(use_filter=True, group=4)

Reglas del filtro:
    - group debe ser del 1 al 5
    - 1 es Lunes y Viernes 5
