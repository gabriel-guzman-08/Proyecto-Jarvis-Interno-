import re
from difflib import SequenceMatcher


NUMEROS = {
    "uno": "1", "una": "1",
    "dos": "2",
    "tres": "3",
    "cuatro": "4",
    "cinco": "5",
    "seis": "6",
    "siete": "7",
    "ocho": "8",
    "nueve": "9",
    "diez": "10",
}


def normalizar(s):
    s = s.lower()
    for palabra, numero in NUMEROS.items():
        s = re.sub(rf'\b{palabra}\b', numero, s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s


def similitud(a, b):
    return SequenceMatcher(None, a, b).ratio()


def mejor_ventana(texto_norm, nombre_norm):
    """Busca la sub-cadena dentro de texto_norm más parecida a nombre_norm."""
    n = len(nombre_norm)

    if n == 0 or len(texto_norm) < 2:
        return 0.0

    mejor_score = 0.0

    for tam in range(max(2, n - 2), n + 3):
        for i in range(0, max(1, len(texto_norm) - tam + 1)):
            ventana = texto_norm[i:i + tam]
            score = similitud(ventana, nombre_norm)
            if score > mejor_score:
                mejor_score = score

    return mejor_score


def interpretar_juego(texto, games_dict=None):

    texto = texto.lower().strip()

    if not games_dict:
        return texto

    texto_norm = normalizar(texto)

    mejor_juego = None
    mejor_score = 0.0

    for nombre in games_dict.keys():

        nombre_norm = normalizar(nombre)

        # coincidencia directa (rápida)
        if nombre_norm in texto_norm:
            return nombre

        # coincidencia difusa (tolera errores de Whisper)
        score = mejor_ventana(texto_norm, nombre_norm)

        if score > mejor_score:
            mejor_score = score
            mejor_juego = nombre

    print("MEJOR MATCH:", mejor_juego, "SCORE:", round(mejor_score, 2))

    if mejor_score >= 0.72:
        return mejor_juego

    return texto