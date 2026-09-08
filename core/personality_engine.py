import json
import os

ESTADO_PATH = "memoria/estado_personalidad.json"

ESTADO_DEFAULT = {
    "humor": "neutral",       # relajado, bromista, profesional, cansado
    "sarcasmo_nivel": 5,      # 0-10, ajustable con el tiempo
    "formalidad": "cercano",  # formal, cercano
}


def _cargar():
    if not os.path.exists(ESTADO_PATH):
        return ESTADO_DEFAULT.copy()
    with open(ESTADO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _guardar(estado):
    os.makedirs(os.path.dirname(ESTADO_PATH), exist_ok=True)
    with open(ESTADO_PATH, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)


def obtener_estado():
    return _cargar()


def ajustar_sarcasmo(delta):
    """delta positivo si el usuario se ríe/reacciona bien al sarcasmo."""
    estado = _cargar()
    estado["sarcasmo_nivel"] = max(0, min(10, estado["sarcasmo_nivel"] + delta))
    _guardar(estado)


def set_humor(nuevo_humor):
    estado = _cargar()
    estado["humor"] = nuevo_humor
    _guardar(estado)


def construir_bloque_personalidad():
    """Esto es lo único que se inyecta al prompt — pequeño y dinámico."""
    estado = _cargar()

    sarcasmo_desc = "muy sarcástico" if estado["sarcasmo_nivel"] >= 7 \
        else "algo sarcástico" if estado["sarcasmo_nivel"] >= 4 \
        else "casi nada sarcástico"

    return f"""
Tu humor actual es: {estado['humor']}.
Tu nivel de sarcasmo es: {sarcasmo_desc}.
Tu formalidad es: {estado['formalidad']}.
"""