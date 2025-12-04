# Sistema de Gestión y Análisis de Signos Vitales

Este proyecto implementa un sistema completo para la generación, validación, almacenamiento, exportación e integración con bases de datos NoSQL (MongoDB Atlas) de registros biomédicos. Incluye manejo de archivos, ordenamiento de datos, expresiones regulares, logging, estructura de carpetas y un menú interactivo.

## Funcionalidades

1. Procesamiento y Ordenamiento de Datos
- Generación de 50 registros biomédicos aleatorios.
- Cada registro contiene:
  - `id` → formato `ID-001`
  - `fr` → edad en formato `18 Anos`
  - `fc` → frecuencia cardíaca `090ppm`
  - `spo2` → saturación `95%`
- Ordenamiento automático por frecuencia cardiaca.

2. Gestión de Archivos: TXT, CSV y JSON
- Exportación automática de registros ordenados.
- Importación desde archivos `.json`.
- Verificación de rutas y manejo de excepciones.

3. Herramientas del Sistema (os, IO, pathlib)
- Creación automática de carpetas:
  - `/data/txt`
  - `/data/csv`
  - `/data/json`
- Movimiento y organización de archivos.
- Generación de `log.txt` con todas las acciones.

4. Validación con Expresiones Regulares
Validación estricta de:
- ID
- Edad (fr)
- Frecuencia Cardíaca (fc)
- SpO2

5. Integración con MongoDB Atlas
- Conexión segura mediante URI (variable de entorno `MONGO_URI`).
- Inserción de registros validados.
- Consultas:
  - Promedio de frecuencia cardiaca.
  - Registros con SpO2 < 94.
  - Búsqueda por ID.
- Exportación de consultas a `mongo_results.json`.

6. Menú Interactivo
Incluye opciones para:
- Generar datos
- Ingresar registros
- Validar
- Exportar/Importar
- Conectarse a MongoDB
- Ejecutar consultas

7. Uso de GitHub
- Repositorio privado
- Código y README incluidos
- Mínimo 5 commits documentados

---

## Cómo ejecutar

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Crear variable de entorno para MongoDB URI (opcional si vas a ingresar manualmente):
```bash
export MONGO_URI="mongodb+srv://usuario:password@cluster.mongodb.net/?retryWrites=true&w=majority"
```

3. Ejecutar el programa:
```bash
python main.py
```

---

## Estructura del proyecto
```
Proyecto/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── data/
    ├── txt/
    ├── csv/
    ├── json/
    └── log.txt
```

---
