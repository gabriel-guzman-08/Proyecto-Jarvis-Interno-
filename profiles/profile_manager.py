import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROFILE_DIR = os.path.join(BASE_DIR, "data")


def cargar_perfil(nombre):

    ruta = os.path.join(PROFILE_DIR, f"{nombre}.json")

    print("BUSCANDO PERFIL EN:", ruta)

    if not os.path.exists(ruta):
        return None

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_perfil(nombre, datos):

    os.makedirs(PROFILE_DIR, exist_ok=True)

    ruta = os.path.join(PROFILE_DIR, f"{nombre}.json")

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    guardar_perfil(
        "gabriel",
        {
            "nombre": "Gabriel",
            "pais": "Costa Rica",
            "moneda": "CRC",
            "idioma": "es",
            "gustos": [
                "Marvel Rivals",
                "Python",
            ]
        }
    )

    print(cargar_perfil("gabriel"))

    guardar_perfil(
    "gabriel",
    {
        "nombre": "Gabriel",
        "pais": "Costa Rica",
        "moneda": "CRC",
        "idioma": "es",
        "gustos": [
            "Marvel Rivals",
            "Python",
            "Fortnite"
        ]
    }
)

