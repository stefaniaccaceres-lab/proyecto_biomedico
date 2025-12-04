#!/usr/bin/env python3

#!/usr/bin/env python3

"""
main.py

Sistema para generación, validación, almacenamiento y consulta de registros biomédicos.
Cumple con los requisitos del enunciado: generación de datos, validación con regex,
exportación a TXT/CSV/JSON, manejo de carpetas, logging y conexión a MongoDB Atlas.

Requisitos:
    pip install -r requirements.txt

Uso:
    python main.py
"""

import os
import csv
import json
import re
import random
from pathlib import Path
from datetime import datetime
import logging

try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except Exception:
    PYMONGO_AVAILABLE = False

# -------------------- Configuración y rutas --------------------

BASE_DIR = Path.cwd() / "data"
TXT_DIR = BASE_DIR / "txt"
CSV_DIR = BASE_DIR / "csv"
JSON_DIR = BASE_DIR / "json"
LOG_FILE = BASE_DIR / "log.txt"

# Crear carpetas
for d in (BASE_DIR, TXT_DIR, CSV_DIR, JSON_DIR):
    d.mkdir(parents=True, exist_ok=True)

# -------------------- Regex solicitados --------------------

PATTERN_ID = re.compile(r"^ID-\d{3}$")           # ID-001
PATTERN_FR = re.compile(r"^[1-9][0-9] Anos$")    # 18–99 Años
PATTERN_FC = re.compile(r"^\d{3}ppm$")           # 090ppm
PATTERN_SPO2 = re.compile(r"^\d{2}%$")           # 95%

# -------------------- Logging --------------------

def setup_logging():
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info("Inicio del sistema de registro de signos vitales")

setup_logging()

# -------------------- Generación de datos --------------------

def generate_record(n):
    """Genera un registro biomédico siguiendo el formato del enunciado."""

    rec_id = f"ID-{n:03d}"
    age = f"{random.randint(18, 99)} Anos"
    fc_raw = random.randint(50, 140)
    fc = f"{fc_raw:03d}ppm"
    spo2_raw = random.randint(85, 100)
    spo2 = f"{spo2_raw}%"

    return {
        "id": rec_id,
        "fr": age,
        "fc": fc,
        "spo2": spo2
    }

# -------------------- Validación --------------------

def validate_record(record):
    return (
        PATTERN_ID.match(record["id"]) and
        PATTERN_FR.match(record["fr"]) and
        PATTERN_FC.match(record["fc"]) and
        PATTERN_SPO2.match(record["spo2"])
    )

# -------------------- Exportar --------------------

def save_txt(records):
    path = TXT_DIR / "registros.txt"
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(str(r) + "\n")
    return path

def save_csv(records):
    path = CSV_DIR / "registros.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "fr", "fc", "spo2"])
        writer.writeheader()
        writer.writerows(records)
    return path

def save_json(records):
    path = JSON_DIR / "registros.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)
    return path

# -------------------- MongoDB --------------------

def save_to_mongo(records):
    if not PYMONGO_AVAILABLE:
        print("PyMongo no está instalado. No se guardará en MongoDB.")
        return

    uri = input("\nIngresa tu cadena de conexión a MongoDB Atlas:\n> ")

    try:
        client = MongoClient(uri)
        db = client["biomedico"]
        col = db["registros"]
        col.insert_many(records)
        print("Datos almacenados en MongoDB correctamente.")
    except Exception as e:
        print("Error al conectar o insertar en MongoDB:", e)

# -------------------- Main --------------------

def main():
    print("Generando registros biomédicos...")

    records = [generate_record(i) for i in range(1, 21)]
    valid = [r for r in records if validate_record(r)]

    print(f"Registros generados: {len(records)}")
    print(f"Registros válidos: {len(valid)}")

    txt_path = save_txt(valid)
    csv_path = save_csv(valid)
    json_path = save_json(valid)

    print("\nArchivos generados:")
    print("TXT  ->", txt_path)
    print("CSV  ->", csv_path)
    print("JSON ->", json_path)

    # Guardar en MongoDB si se desea
    opc = input("\n¿Deseas guardar los datos en MongoDB? (s/n): ")
    if opc.lower() == "s":
        save_to_mongo(valid)

    print("\nProceso finalizado.")

if __name__ == "__main__":
    main()
