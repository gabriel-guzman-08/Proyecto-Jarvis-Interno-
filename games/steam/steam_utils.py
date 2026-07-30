import subprocess

from ai.game_intent_ai import (
    interpretar_juego
)

from games.steam.steam_library import (
    cargar_juegos_steam
)


games = cargar_juegos_steam()

print(
    "JUEGOS CARGADOS:",
    len(games)
)


jugar_keywords = [
    "jugar",
    "juega",
    "quiero"
]


def procesar_game_command(texto):

    print("SALIENDO GAME CONTROLLER")

    texto = texto.lower()

    print("ENTRANDO A GAME CONTROLLER")
    print("TEXTO RECIBIDO:", texto)

    palabras = texto.split()

    if not any(
        k in palabras
        for k in jugar_keywords
    ):
        return None

    juego_interpretado = (
        interpretar_juego(texto)
    )

    print(
        "JUEGO INTERPRETADO:",
        juego_interpretado
    )

    encontrado = False

    for game, url in games.items():

        if game in juego_interpretado:

            encontrado = True

            subprocess.Popen(
                [
                    "cmd",
                    "/c",
                    "start",
                    url
                ],
                shell=True
            )

            return (
                f"Preparando {game}, señor."
            )

    if juego_interpretado and not encontrado:
        return (
            f"No encontré {juego_interpretado} "
            f"en tu biblioteca de Steam."
        )

    return None