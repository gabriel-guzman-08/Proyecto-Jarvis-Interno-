import keyboard
import time
from voice.tts_engine import hablar
from core.behavior_profile import set_perfil

last_press = 0

state = {
    "recording": False,
    "conversation_mode": False,
}


def start_keyboard_listener():

    global last_press

    while True:

        keyboard.wait("|")

        press_start = time.time()

        state["recording"] = True

        print("PUSH TO TALK ON")

        while keyboard.is_pressed("|"):
            time.sleep(0.01)

        state["recording"] = False

        print("PUSH TO TALK OFF")

        press_duration = time.time() - press_start
        now = time.time()
        delta = now - last_press
        last_press = now

        if press_duration < 0.5 and delta < 0.4:

            state["conversation_mode"] = not state["conversation_mode"]

            if state["conversation_mode"]:

                print(
                    "CONVERSATION MODE: TRUE"
                )

                set_perfil("conversacion")

                hablar(
                    "Modo conversación activado, señor."
                )

            else:

                print(
                    "CONVERSATION MODE: FALSE"
                )

                set_perfil("balanceado")

                hablar(
                    "Modo conversación desactivado, señor."
                )