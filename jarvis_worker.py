print("Jarvis iniciado correctamente")

from PySide6.QtCore import QThread, Signal
from voice.whisper_engine import escuchar_push_to_talk
import traceback
import threading
import time

from jarvis_core import procesar_comando

import input.keyboard_listener

from voice.tts_engine import (
    hablar,
    detener_habla
)


class JarvisWorker(QThread):
    state_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.running = True

        self.muted = False


    def run(self):
        try:
            print("WORKER INICIADO")


            while self.running:
                    try:

                        print("ESCUCHANDO...")
                        self.state_changed.emit("listening")

                        try:
                            texto = escuchar_push_to_talk()

                            print("WHISPER:", texto)

                            if not texto:

                                continue

                            texto_lower = texto.lower().strip()

                            basura = [

                                "subtítulos realizados por la comunidad de amara.org",

                                "subtítulos por la comunidad de amara.org",

                                "thank you for watching",

                                "gracias por ver el video"
                            ]

                            if texto_lower in basura:

                                continue

                            texto_lower = texto.lower().strip()

                        except Exception as e:

                            print("ERROR WHISPER:", e)

                            continue
                            

                        print("AUDIO CAPTURADO")

                        self.state_changed.emit("thinking")


                        palabras_stop = ["para", "silencio", "cállate", "callate", "detente"]

                        if any(palabra in texto_lower for palabra in palabras_stop):
                            print("INTERRUPCIÓN DETECTADA")
                            detener_habla()
                            self.state_changed.emit("idle")
                            continue
                        


                        self.state_changed.emit("thinking")

                        comando = texto_lower

                        respuesta = procesar_comando(comando)

                        print("RESPUESTA:", respuesta)

                        self.state_changed.emit("speaking")

                        threading.Thread(
                            target=hablar,
                            args=(respuesta,),
                            daemon=True
                        ).start()
                        
                        self.state_changed.emit("idle")

                        self.state_changed.emit("idle")
                        continue

                    except Exception:
                        print("ERROR INTERNO:")
                        traceback.print_exc()
                        self.state_changed.emit("idle")

        except Exception:
            print("\n💥 ERROR GRAVE EN WORKER:\n")
            traceback.print_exc()
            input("Presiona ENTER...")


    def stop(self):
        self.running = False