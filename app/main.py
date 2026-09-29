import os
import base64
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from deepface import DeepFace
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACES_DB = os.path.join(BASE_DIR, "faces_db")
CSV_PATH = os.path.join(BASE_DIR, "asistencia.csv")

app = FastAPI(title="Sistema de Asistencia Facial")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "templates")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

if not os.path.exists(CSV_PATH):
    df_init = pd.DataFrame(columns=["Nombre", "Fecha", "Hora"])
    df_init.to_csv(CSV_PATH, index=False)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/reconocer")
async def reconocer_rostro(image_data: str = Form(...)):
    try:
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return JSONResponse({"exito": False, "mensaje": "Imagen no válida"})

        dfs = DeepFace.find(
            img_path=img,
            db_path=FACES_DB,
            enforce_detection=False,
            silent=True
        )

        if len(dfs) > 0 and not dfs[0].empty:
            match_path = dfs[0].iloc[0]['identity']
            
            file_name = os.path.basename(match_path)
            nombre = os.path.splitext(file_name)[0].replace("_", " ")

            now = datetime.now()
            fecha = now.strftime("%Y-%m-%d")
            hora = now.strftime("%H:%M:%S")

            df = pd.read_csv(CSV_PATH) if os.path.exists(CSV_PATH) else pd.DataFrame(columns=["Nombre", "Fecha", "Hora"])
            
            ya_registrado = not df[(df["Nombre"] == nombre) & (df["Fecha"] == fecha)].empty

            if not ya_registrado:
                nuevo_registro = pd.DataFrame([{"Nombre": nombre, "Fecha": fecha, "Hora": hora}])
                df = pd.concat([df, nuevo_registro], ignore_index=True)
                df.to_csv(CSV_PATH, index=False)
                status_msg = f"Asistencia registrada para {nombre}"
            else:
                status_msg = f"{nombre} ya tiene asistencia registrada hoy"

            return JSONResponse({
                "exito": True,
                "nombre": nombre,
                "hora": hora,
                "mensaje": status_msg
            })

        return JSONResponse({"exito": False, "mensaje": "Rostro no reconocido"})

    except Exception as e:
        return JSONResponse({"exito": False, "mensaje": f"Error en procesamiento: {str(e)}"})


@app.get("/asistencias")
async def obtener_asistencias():
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            return df.to_dict(orient="records")
        except Exception:
            return []
    return []