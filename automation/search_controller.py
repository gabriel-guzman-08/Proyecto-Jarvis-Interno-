import subprocess
import urllib.parse


chrome_path = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)


search_keywords = [
    "busca",
    "búscame",
    "buscame",
    "investiga",
    "googlea",
    "averigua",
    "encuentra"
]


def procesar_search_command(texto):

    texto = texto.lower()

    if not any(
        k in texto
        for k in search_keywords
    ):
        return None

    texto_limpio = texto

    for keyword in search_keywords:
        texto_limpio = texto_limpio.replace(
            keyword,
            ""
        )

    texto_limpio = texto_limpio.strip()

    if not texto_limpio:
        return (
            "¿Qué desea buscar, señor?"
        )

    query = urllib.parse.quote(
        texto_limpio
    )

    url = (
        f"https://www.google.com/search?q={query}"
    )

    subprocess.Popen([
        chrome_path,
        url
    ])

    return (
        f"Buscando {texto_limpio}, señor."
    )