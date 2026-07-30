import pygame
import asyncio
import edge_tts
import time

is_speaking = False

pygame.mixer.init()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def generar_voz(texto):

    communicate = edge_tts.Communicate(
        text=texto,
        voice="en-US-AndrewMultilingualNeural",
        pitch="-10Hz",
        rate="+10%"
    )

    output_path = (
        f"temp_voice_{int(time.time() * 1000)}.mp3"
    )

    await communicate.save(output_path)

    return output_path


def hablar(texto):

    global is_speaking

    is_speaking = True

    texto = texto.replace("**", "")
    texto = texto.replace("*", "")
    texto = texto.replace("#", "")
    texto = texto.replace("```", "")

    texto = texto.replace(
        "Jarvis",
        "Yarvis"
    )

    texto = texto.encode(
        "cp1252",
        errors="ignore"
    ).decode("cp1252")

    output_path = loop.run_until_complete(
        generar_voz(texto)
    )

    pygame.mixer.music.stop()

    pygame.mixer.music.load(output_path)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    is_speaking = False


def detener_habla():

    global is_speaking

    try:

        pygame.mixer.music.stop()

        is_speaking = False

    except:
        pass