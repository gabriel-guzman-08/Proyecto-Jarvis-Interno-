import json
import os
from datetime import datetime

MEMORIA_PATH = "memoria/gabriel_memoria.json"


def _cargar():
    if not os.path.exists(MEMORIA_PATH):
        return {
            "hechos": [],
            "contexto_reciente": []
        }

    with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _guardar(data):
    os.makedirs(os.path.dirname(MEMORIA_PATH), exist_ok=True)
    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def agregar_hecho(hecho):
    """Guarda un hecho permanente: 'Está escribiendo un libro sobre X'."""
    data = _cargar()
    data["hechos"].append({
        "texto": hecho,
        "fecha": datetime.now().isoformat()
    })
    _guardar(data)


def obtener_hechos(limite=15):
    data = _cargar()
    return [h["texto"] for h in data["hechos"][-limite:]]


def agregar_contexto_reciente(texto):
    """Última sesión: de qué se habló. Se usa para 'seguimos con X'."""
    data = _cargar()
    data["contexto_reciente"].append({
        "texto": texto,
        "fecha": datetime.now().isoformat()
    })
    data["contexto_reciente"] = data["contexto_reciente"][-10:]
    _guardar(data)


def obtener_contexto_reciente(limite=5):
    data = _cargar()
    return [c["texto"] for c in data["contexto_reciente"][-limite:]]