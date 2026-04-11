
import json
import os
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "records.json")


def load_data() -> List[Dict[str, Any]]:
    """
    Load records from the JSON file.

    Returns:
        List[Dict[str, Any]]: List of records.
    """
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠ Advertencia: El archivo de los datos está corrupto. Iniciando con lista nueva.")
        return []
    except Exception as e:
        print(f"⚠ Error inesperado al cargar los datos: {e}")
        return []


def save_data(data: List[Dict[str, Any]]) -> None:
    """
    Save records to the JSON file.

    Args:
        data (List[Dict[str, Any]]): List of records to save.
    """
    try:
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠ Error guardando datos: {e}")
