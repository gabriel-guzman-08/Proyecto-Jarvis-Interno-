import subprocess


chrome_path = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)


websites = {
    "youtube": "https://youtube.com",
    "twitter": "https://twitter.com",
    "x": "https://twitter.com",
    "reddit": "https://reddit.com",
    "gmail": "https://mail.google.com",
    "spotify": "https://spotify.com",
    "twitch": "https://twitch.tv",
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "whatsapp": "https://web.whatsapp.com",
    "netflix": "https://netflix.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com"
}


abrir_keywords = [
    "abre",
    "abreme",
    "entra a",
    "ve a",
    "lanza",
    "inicia",
    "ejecuta"
]


def procesar_browser_command(texto):

    texto = texto.lower()

    if not any(
        k in texto
        for k in abrir_keywords
    ):
        return None

    for sitio, url in websites.items():

        if sitio in texto:

            subprocess.Popen([
                chrome_path,
                url
            ])

            return (
                f"Abriendo {sitio}, señor."
            )

    texto_limpio = texto

    for keyword in abrir_keywords:
        texto_limpio = texto_limpio.replace(
            keyword,
            ""
        )

    texto_limpio = texto_limpio.strip()

    if texto_limpio:

        posible_url = (
            f"https://{texto_limpio}.com"
        )

        subprocess.Popen([
            chrome_path,
            posible_url
        ])

        return (
            f"Abriendo {texto_limpio}, señor."
        )

    return None