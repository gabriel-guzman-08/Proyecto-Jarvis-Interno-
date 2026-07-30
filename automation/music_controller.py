import yt_dlp

from automation.chrome_remote import (
    reproducir_url_youtube_music,
    pausar_reanudar_music,
    siguiente_cancion,
    cancion_anterior
)


def buscar_video_id(cancion):

    ydl_opts = {
        "quiet": True,
        "extract_flat": True
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        resultado = ydl.extract_info(
            f"ytsearch1:{cancion}",
            download=False
        )

    entries = resultado.get(
        "entries",
        []
    )

    if not entries:
        return None

    return entries[0]["id"]


def procesar_music_command(texto):

    # =========================
    # PAUSA / PLAY
    # =========================

    if (
        "pausa" in texto
        or
        "pause" in texto
    ):

        pausar_reanudar_music()

        return (
            "Música pausada, señor."
        )

    if (
        "play" in texto
        or
        "reanuda" in texto
    ):

        pausar_reanudar_music()

        return (
            "Reproduciendo música, señor."
        )

    # =========================
    # SIGUIENTE
    # =========================

    if (
        "siguiente canción" in texto
        or
        "next song" in texto
        or
        "siguiente" in texto
    ):

        siguiente_cancion()

        return (
            "Saltando canción, señor."
        )

    # =========================
    # ANTERIOR
    # =========================

    if (
        "canción anterior" in texto
        or
        "anterior" in texto
        or
        "previous song" in texto
    ):

        cancion_anterior()

        return (
            "Retrocediendo canción, señor."
        )

    # =========================
    # ACTIVAR MÚSICA
    # =========================

    activar = (
        "pon " in texto
        or
        "pong " in texto
        or
        "ponme " in texto
        or
        "reproduce " in texto
        or
        "quiero escuchar " in texto
    )

    if not activar:
        return None

    # =========================
    # LIMPIAR TEXTO
    # =========================

    cancion = (
        texto
        .replace("pon", "")
        .replace("pong", "")
        .replace("ponme", "")
    )

    # =========================
    # BUSCAR VIDEO
    # =========================

    video_id = buscar_video_id(
        cancion
    )

    if not video_id:

        return (
            "No encontré esa canción, señor."
        )

    # =========================
    # REPRODUCIR
    # =========================

    reproducir_url_youtube_music(
        video_id
    )

    return (
        f"Reproduciendo {cancion}, señor."
    )