import keyboard
import time
push_to_talk_pressed = False
from voice.tts_engine import hablar


conversation_mode = False

push_to_talk_until = 0

last_press = 0


def start_keyboard_listener():

    global conversation_mode
    global push_to_talk_until
    global last_press

    while True:

        keyboard.wait("|")

        press_start = time.time()

        push_to_talk_pressed = True

        print("PUSH TO TALK ON")

        while keyboard.is_pressed("|"):
            time.sleep(0.01)

        push_to_talk_pressed = False

        print("PUSH TO TALK OFF")

        press_duration = (
            time.time() - press_start
        )

        now = time.time()

        delta = now - last_press

        last_press = now

        # DOBLE TOQUE
        if (
            press_duration < 0.5
            and
            delta < 0.4
        ):

            conversation_mode = (
                not conversation_mode
            )

            if conversation_mode:

                print(
                    "CONVERSATION MODE: TRUE"
                )

                hablar(
                    "Modo conversación activado, señor."
                )

            else:

                print(
                    "CONVERSATION MODE: FALSE"
                )

                hablar(
                    "Modo conversación desactivado, señor."
                )