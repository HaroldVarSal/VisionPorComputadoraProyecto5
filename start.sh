#!/bin/bash

# 1. Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi

# 2. Activar entorno virtual
source .venv/bin/activate

# 3. Actualizar pip e instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Iniciar la aplicación con Uvicorn
echo "Iniciando servidor de asistencia facial..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload