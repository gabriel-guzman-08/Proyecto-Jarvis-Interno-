from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import keyboard
import time

print("CARGANDO WHISPER...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("WHISPER LISTO")


def escuchar_push_to_talk():

    print("\nMantén | para hablar...")

    keyboard.wait("|")

    print("GRABANDO...")

    audio_chunks = []

    def callback(indata, frames, time_info, status):

        audio_chunks.append(
            indata.copy()
        )

    stream = sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype="float32",
        callback=callback
    )

    stream.start()

    while keyboard.is_pressed("|"):
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


while True:

    texto = escuchar_push_to_talk()

    print(
        "\nTRANSCRIPCIÓN:"
    )

    print(texto)