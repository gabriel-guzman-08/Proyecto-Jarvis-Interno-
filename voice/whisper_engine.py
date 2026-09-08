from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import time
from input.keyboard_listener import state

print("CARGANDO WHISPER...")

model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)

print("WHISPER LISTO")


def escuchar(segundos=3):

    audio = sd.rec(
        int(segundos * 16000),
        samplerate=16000,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    audio = audio.flatten()

    segments, info = model.transcribe(
        audio,
        language="es"
    )

    texto = ""

    for segment in segments:
        texto += segment.text

    return texto.strip()


def escuchar_push_to_talk():

    print("\nMantén | para hablar...")

    while not state["recording"]:
        time.sleep(0.01)

    print("GRABANDO...")

    audio_chunks = []

    def callback(indata, frames, time_info, status):
        audio_chunks.append(indata.copy())

    stream = sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype="float32",
        callback=callback
    )

    stream.start()

    while state["recording"]:
        time.sleep(0.01)

    stream.stop()
    stream.close()

    print("PROCESANDO...")

    if not audio_chunks:
        return ""

    audio = np.concatenate(
        audio_chunks,
        axis=0
    )

    audio = audio.flatten()

    segments, info = model.transcribe(
        audio,
        language="es"
    )

    texto = ""

    for segment in segments:
        texto += segment.text

    return texto.strip()


def escuchar_conversacion(silencio_seg=1.2, max_seg=15):

    print("MODO CONVERSACIÓN: grabando...")

    audio_chunks = []
    silencio_actual = 0
    empezo_a_hablar = False
    umbral_silencio = 0.01  # ajustable si es muy sensible o poco sensible

    def callback(indata, frames, time_info, status):
        audio_chunks.append(indata.copy())

    stream = sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype="float32",
        callback=callback
    )

    stream.start()

    tiempo_inicio = time.time()

    while True:
        time.sleep(0.1)

        if audio_chunks:
            ultimo = audio_chunks[-1]
            volumen = np.abs(ultimo).mean()

            if volumen > umbral_silencio:
                empezo_a_hablar = True
                silencio_actual = 0
            elif empezo_a_hablar:
                silencio_actual += 0.1

        if empezo_a_hablar and silencio_actual >= silencio_seg:
            break

        if time.time() - tiempo_inicio >= max_seg:
            break

    stream.stop()
    stream.close()

    print("PROCESANDO...")

    if not audio_chunks:
        return ""

    audio = np.concatenate(audio_chunks, axis=0)
    audio = audio.flatten()

    segments, info = model.transcribe(audio, language="es")

    texto = ""
    for segment in segments:
        texto += segment.text

    return texto.strip()