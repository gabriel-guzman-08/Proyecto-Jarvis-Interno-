print("Jarvis iniciado correctamente")

import sys

print(sys.executable)

import os
import traceback
import subprocess
import time
import requests
from PySide6.QtWidgets import QApplication
import ctypes
import threading

from input.keyboard_listener import (
    start_keyboard_listener
)


myappid = 'jarvis.ai.assistant.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

import sys
import os

sys.path.append(os.path.abspath("."))

from ui.main_window import JarvisMainWindow


from jarvis_worker import JarvisWorker


proceso_ollama = None


def ollama_esta_corriendo():
    try:
        requests.get("http://localhost:11434", timeout=2)
        return True
    except Exception:
        return False


def iniciar_ollama_si_hace_falta():
    global proceso_ollama

    if ollama_esta_corriendo():
        print("OLLAMA YA ESTABA CORRIENDO")
        return

    print("OLLAMA NO ESTÁ CORRIENDO, INICIANDO...")

    try:
        proceso_ollama = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception as e:
        print("⚠️ No se pudo iniciar Ollama automáticamente:", e)
        return

    # Espera hasta que Ollama responda (máximo ~15 segundos)
    for _ in range(30):
        if ollama_esta_corriendo():
            print("OLLAMA INICIADO CORRECTAMENTE")
            return
        time.sleep(0.5)

    print("⚠️ Ollama no respondió a tiempo, puede tardar más en arrancar")


def cerrar_ollama_si_lo_iniciamos():
    global proceso_ollama

    if proceso_ollama is not None:
        print("CERRANDO OLLAMA (lo habíamos iniciado nosotros)...")
        proceso_ollama.terminate()


def main():

    print("APP START")

    iniciar_ollama_si_hace_falta()

    def precargar_modelo():
        try:
            requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.1:8b", "prompt": "hola", "stream": False},
                timeout=60
            )
            print("MODELO PRECARGADO EN VRAM")
        except Exception as e:
            print("⚠️ No se pudo precargar el modelo:", e)

    threading.Thread(
        target=precargar_modelo,
        daemon=True
    ).start()

    app = QApplication(sys.argv)

    app.aboutToQuit.connect(cerrar_ollama_si_lo_iniciamos)

    keyboard_thread = threading.Thread(
        target=start_keyboard_listener,
        daemon=True
    )

    keyboard_thread.start()

    window = JarvisMainWindow()
    window.show()

    worker = JarvisWorker()
    window.worker = worker
    worker.state_changed.connect(window.set_orb_state)
    worker.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n🔥 ERROR DETECTADO:\n")
        traceback.print_exc()
        input("\nPresiona ENTER para cerrar...")