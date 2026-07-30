print("Jarvis iniciado correctamente")

import sys

print(sys.executable)

import os
import traceback
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


def main():
    
    app = QApplication(sys.argv)


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