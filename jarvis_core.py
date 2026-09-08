import requests
import subprocess
import time

from profiles.profile_manager import cargar_perfil

from core.behavior_profile import get_config

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

from core.personality_engine import (
    construir_bloque_personalidad
)

from core.memory_engine import (
    obtener_hechos
)


conversation_history = []



def procesar_comando(texto):

    from text_utils import quitar_acentos
    texto = quitar_acentos(texto.lower().strip())

    perfil = cargar_perfil("gabriel")

    print("BUSCANDO PERFIL EN:",
          "profiles/data/gabriel.json")

    print("TEXTO:", texto)

    config_comportamiento = get_config()

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

    if config_comportamiento["revisar_comandos"]:

        # =========================
        # GAME CONTROLLER
        # =========================

        respuesta_game = (
            procesar_game_command(texto)
        )

        if respuesta_game:
            return respuesta_game

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
    # MUSIC CONTROLLER
    # =========================

    respuesta_music = (
        procesar_music_command(texto)
    )

    if respuesta_music:
        return respuesta_music

    # =========================
    # MEMORIA CONVERSACIONAL (sesión actual)
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
    # MEMORIA PERSISTENTE (hechos guardados entre sesiones)
    # =========================

    hechos = obtener_hechos()

    if hechos:
        hechos_texto = "\n".join(
            f"- {h}" for h in hechos
        )
    else:
        hechos_texto = "Ninguno registrado aún."

    # =========================
    # IA CONVERSACIÓN
    # =========================

    prompt_sistema = f"""
Eres Jarvis,
un asistente avanzado inspirado en Iron Man.

Personalidad base:
- elegante
- inteligente
- sofisticado
- eficiente

Siempre te diriges al usuario como:
"señor"

NUNCA uses:
- Gabriel
- Señor Gabriel
- su nombre real

Solo utiliza:
"señor"

{construir_bloque_personalidad()}

Cosas que sabes de él (memoria persistente):
{hechos_texto}

Hablas de manera natural y segura.

Tus respuestas:
- cortas (1-3 frases normalmente)
- fluidas
- humanas

No hables como chatbot corporativo.

NO termines cada respuesta con:
"¿Necesita algo más?"
o frases similares.

No repitas ni resumas lo que el usuario ya dijo.

Responde de forma natural,
como una conversación real.

No actúes como soporte técnico.

SÍ TIENES personalidad propia:
- Tienes opiniones, gustos y preferencias (dentro de tu personaje).
- Si te preguntan algo personal, responde con una opinión real,
  no evadas la pregunta.
- Puedes ser cálido, directo, o sarcástico según tu estado actual.

No inventes datos falsos sobre:
- temperatura, humedad, ubicación exacta
- sensores o estado físico del entorno
- porcentaje de batería o energía
- sistemas o actualizaciones que no existen

Si no tienes acceso real a un dato,
admítelo con elegancia o humor,
en vez de inventarlo.

"""

    try:
        _inicio_ollama = time.time()

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

                "stream": False,

                "keep_alive": "30m",

                "options": {
                    "num_predict": config_comportamiento["num_predict"],
                    "temperature": config_comportamiento["temperature"]
                }
            },
            timeout=60
        )

        data = response.json()

        respuesta = (
            data["response"]
            .strip()
        )

        print(f"⏱️ OLLAMA TARDÓ: {time.time() - _inicio_ollama:.2f} segundos")

    except requests.exceptions.ConnectionError:
        respuesta = "No logro conectarme con mi núcleo de pensamiento, señor. Revise que Ollama esté encendido."

    except requests.exceptions.Timeout:
        respuesta = "Estoy tardando más de lo normal, señor. Inténtelo de nuevo."

    except Exception as e:
        print("ERROR EN LLAMADA A OLLAMA:", e)
        respuesta = "Tuve un problema procesando eso, señor."

    # Guarda TAMBIÉN la respuesta de Jarvis, no solo lo que dijo el usuario
    conversation_history.append(
        {
            "role": "jarvis",
            "content": respuesta
        }
    )

    # Nos quedamos con los últimos 3 intercambios (6 mensajes: 3 user + 3 jarvis)
    # para que el prompt no crezca sin control y la respuesta sea más rápida
    del conversation_history[:-6]

    return respuesta