import sounddevice as sd
import numpy as np
import time

from whisper_online import FasterWhisperASR, OnlineASRProcessor

print("CARGANDO MODELO...")

asr = FasterWhisperASR(lan="es", modelsize="small")
asr.model = None  # liberamos el intento de carga anterior si lo hubo

from faster_whisper import WhisperModel

asr.model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

online = OnlineASRProcessor(asr)

print("MODELO LISTO. Habla ahora (Ctrl+C para salir)...")

SAMPLE_RATE = 16000
CHUNK_SECONDS = 1.0

def callback(indata, frames, time_info, status):
    audio_chunk = indata[:, 0].astype(np.float32)
    online.insert_audio_chunk(audio_chunk)

    output = online.process_iter()

    if output[0] is not None:
        texto = output[2]
        if texto.strip():
            print("TEXTO PARCIAL:", texto)


stream = sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    callback=callback,
    blocksize=int(SAMPLE_RATE * CHUNK_SECONDS)
)

with stream:
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nFINALIZANDO...")
        output = online.finish()
        if output[0] is not None:
            print("TEXTO FINAL:", output[2])