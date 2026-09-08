# core/behavior_profile.py

perfil_actual = "balanceado"

PERFILES = {
    "conversacion": {
        "descripcion": "Prioriza fluidez y velocidad de charla. Comandos (Steam/apps/web) siguen funcionando pero no son la prioridad.",
        "revisar_comandos": False,   # salta Steam/browser/search por velocidad
        "num_predict": 120,
        "temperature": 0.8,
    },
    "comandos": {
        "descripcion": "Prioriza ejecutar acciones (abrir juegos, apps, webs) lo más rápido posible.",
        "revisar_comandos": True,
        "num_predict": 40,
        "temperature": 0.5,
    },
    "balanceado": {
        "descripcion": "Modo por defecto: revisa comandos y conversa normal.",
        "revisar_comandos": True,
        "num_predict": 90,
        "temperature": 0.8,
    },
}


def set_perfil(nombre):
    global perfil_actual
    if nombre in PERFILES:
        perfil_actual = nombre
        print(f"BEHAVIOR PROFILE: {nombre}")
    else:
        print(f"⚠️ Perfil desconocido: {nombre}")


def get_perfil():
    return perfil_actual


def get_config():
    return PERFILES[perfil_actual]