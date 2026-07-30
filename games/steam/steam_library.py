import os
import re
print("STEAM_LIBRARY CARGADO")

STEAM_APPS = (
    r"E:\SteamLibrary\steamapps"
)


def cargar_juegos_steam():

    juegos = {}

    for archivo in os.listdir(
        STEAM_APPS
    ):

        if not archivo.startswith(
            "appmanifest_"
        ):
            continue

        ruta = os.path.join(
            STEAM_APPS,
            archivo
        )

        try:

            with open(
                ruta,
                "r",
                encoding="utf-8"
            ) as f:

                contenido = f.read()

            appid = re.search(
                r'"appid"\s+"(\d+)"',
                contenido
            )

            nombre = re.search(
                r'"name"\s+"(.+?)"',
                contenido
            )

            if (
                appid
                and
                nombre
            ):

                juegos[
                    nombre.group(1)
                    .lower()
                ] = (
                    "steam://rungameid/"
                    + appid.group(1)
                )

        except Exception as e:

            print(
                "ERROR:",
                archivo,
                e
            )

    return juegos