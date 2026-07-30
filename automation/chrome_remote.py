import pychrome
import time
import keyboard


browser = pychrome.Browser(
    url="http://127.0.0.1:9222"
)


def get_tab():

    tabs = browser.list_tab()

    if tabs:

        tab = tabs[0]

    else:

        tab = browser.new_tab()

    tab.start()

    tab.Page.enable()

    return tab


def abrir_youtube():

    tab = get_tab()

    tab.Page.navigate(
        url="https://youtube.com"
    )

    time.sleep(3)

    tab.stop()


def reproducir_url_youtube_music(video_id):

    tab = get_tab()

    url = (
        f"https://music.youtube.com/watch?v={video_id}"
    )

    tab.Page.navigate(url=url)

    time.sleep(3)

    tab.stop()


def pausar_reanudar_music():

    keyboard.send(
        "play/pause media"
    )


def siguiente_cancion():

    keyboard.send(
        "next track"
    )


def cancion_anterior():

    keyboard.send(
        "previous track"
    )