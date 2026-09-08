import subprocess
from difflib import SequenceMatcher

from ai.game_intent_ai import (
    interpretar_juego
)

from games.steam.steam_library import (
    cargar_juegos_steam
)


games = cargar_juegos_steam()

print("NOMBRES EN BIBLIOTECA:", list(games.keys()))

print(
    "JUEGOS CARGADOS:",
    len(games)
)


jugar_keywords = [
    "jugar",
    "juega",
    "quiero"
]

abrir_keywords_juego = [
    "abre",
    "abreme",
    "inicia",
    "lanza",
    "ejecuta"
]


def parece_trigger(palabra, triggers, umbral=0.78):
    for t in triggers:
        # Si la diferencia de longitud es grande, no es la misma palabra
        if abs(len(palabra) - len(t)) > 2:
            continue
        ratio = SequenceMatcher(None, palabra, t).ratio()
        if ratio >= umbral:
            return True
    return False

def procesar_game_command(texto):

    print("SALIENDO GAME CONTROLLER")

    texto = texto.lower()

    print("ENTRANDO A GAME CONTROLLER")
    print("TEXTO RECIBIDO:", texto)

    palabras = texto.split()

    primera_palabra = palabras[0] if palabras else ""

    # "jugar"/"juega"/"quiero" ya son suficientemente distintivas,
    # exigimos coincidencia exacta para evitar falsos positivos
    tiene_jugar = primera_palabra in jugar_keywords

    # Solo "abre" tolera variaciones de Whisper (abra, abri, etc.)
    tiene_abrir = parece_trigger(
        primera_palabra,
        abrir_keywords_juego,
        umbral=0.78
    )

    if not tiene_jugar and not tiene_abrir:
        return None

    juego_interpretado = (
        interpretar_juego(texto, games)
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

    # Vino de "abre X" y no coincidió con ningún juego:
    # no bloqueamos, dejamos que browser_controller decida
    # (podría ser un sitio web como "abre youtube").
    if tiene_abrir and not tiene_jugar and not encontrado:
        return None

    # Vino de "jugar/quiero" y no coincidió:
    # ahí sí avisamos que no está en la biblioteca.
    if juego_interpretado and not encontrado:
        return (
            f"No encontré {juego_interpretado} "
            f"en tu biblioteca de Steam."
        )

    return None