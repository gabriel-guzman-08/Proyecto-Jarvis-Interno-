import requests


def interpretar_juego(texto):

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8b",

            "messages": [

                {
                    "role": "system",
                    "content": """
Tu tarea es únicamente corregir nombres de videojuegos.

Reglas:
- Responde SOLO el nombre del juego.
- NO expliques nada.
- NO hagas conversación.
- NO hagas preguntas.
- NO hables como asistente.
- SOLO devuelve texto corto.

Ejemplos:

hell drivers 2
helldivers 2

marvel rival
marvel rivals

call of dute
call of duty
"""
                },

                {
                    "role": "user",
                    "content": texto
                }
            ],

            "stream": False,

            "options": {
                "temperature": 0.1
            }
        }
    )

    data = response.json()

    respuesta = (
        data["message"]["content"]
        .strip()
        .lower()
    )

    print("JUEGO INTERPRETADO:",
          respuesta)

    return respuesta