import requests
import subprocess

from profiles.profile_manager import cargar_perfil

from games.steam.steam_utils import (
    procesar_game_command
)

from automation.browser_controller import (
    procesar_browser_command
)

from automation.search_controller import (
    procesar_search_command
)

from automation.music_controller import (
    procesar_music_command
)


conversation_history = []



def procesar_comando(texto):

    texto = texto.lower().strip()

    perfil = cargar_perfil("gabriel")

    print("BUSCANDO PERFIL EN:",
          "profiles/data/gabriel.json")

    print("TEXTO:", texto)

    # =========================
    # PRESETS ESPECIALES
    # =========================

    if (
        "estás despierto" in texto
        or
        "estas despierto" in texto
    ):

        chrome_path = (
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )

        subprocess.Popen([
            chrome_path,
            "https://music.youtube.com/watch?v=wjZMcWaniA4"
        ])

        return "Para usted, señor, siempre."

    # =========================
    # BROWSER CONTROLLER
    # =========================

    respuesta_browser = (
        procesar_browser_command(texto)
    )

    if respuesta_browser:
        return respuesta_browser

    # =========================
    # SEARCH CONTROLLER
    # =========================

    respuesta_search = (
        procesar_search_command(texto)
    )

    if respuesta_search:
        return respuesta_search

    # =========================
    # GAME CONTROLLER
    # =========================

    respuesta_game = (
        procesar_game_command(texto)
    )

    if respuesta_game:
        return respuesta_game

    # =========================
    # MUSIC CONTROLLER
    # =========================

    respuesta_music = (
        procesar_music_command(texto)
    )

    if respuesta_music:
        return respuesta_music
    

        # =========================
    # MEMORIA CONVERSACIONAL
    # =========================

    conversation_history.append(
        {
            "role": "user",
            "content": texto
        }
    )

    historial = ""

    for mensaje in conversation_history:

        if mensaje["role"] == "user":

            historial += (
                f"\nUsuario: "
                f"{mensaje['content']}"
            )

        else:

            historial += (
                f"\nJarvis: "
                f"{mensaje['content']}"
            )

    # =========================
    # IA CONVERSACIÓN
    # =========================

    prompt_sistema = f"""
Eres Jarvis,
un asistente avanzado inspirado en Iron Man.

Personalidad:
- elegante
- inteligente
- sofisticado
- ligeramente sarcástico
- eficiente

Siempre te diriges al usuario como:
"señor"

NUNCA uses:
- Gabriel
- Señor Gabriel
- su nombre real

Solo utiliza:
"señor"

Hablas de manera natural y segura.

Tus respuestas:
- cortas
- fluidas
- humanas

No hables como chatbot corporativo.

NO termines cada respuesta con:
"¿Necesita algo más?"
o frases similares.

No repitas cierres conversacionales.

Responde de forma natural,
como una conversación real.

A veces termina seco.
A veces con sarcasmo.
A veces con observaciones cortas.

No actúes como soporte técnico.

"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1:8b",

            "prompt":
                prompt_sistema
                +
                historial
                +
                "\nUsuario: "
                +
                texto
                +
                "\nJarvis:",

            "stream": False
        }
    )

    data = response.json()

    respuesta = (
        data["response"]
        .strip()
    )


    del conversation_history[:-20]

    return respuesta