# FacePass 📸 — Sistema de Asistencia Automatizada con IA

**FacePass** es un sistema inteligente de control de asistencia basado en visión por computadora, diseñado para registrar entradas e identidades en tiempo real sin contacto físico.

Impulsado por **FastAPI** en el backend y la librería de aprendizaje profundo **DeepFace**, el sistema procesa fotogramas de video, detecta rostros y calcula distancias vectoriales (*embeddings*) contra una base de datos local para validar la identidad y registrar la asistencia de forma inmediata en un dashboard con estética **Glassmorphism en Modo Oscuro**.

---

## 🧠 ¿Cómo Reconoce la IA los Rostros?

A diferencia de los humanos, que reconocemos facciones de manera intuitiva, una máquina convierte los rasgos faciales en representaciones numéricas compuestas por mapas de características.

El pipeline convolucional opera paso a paso:

```text
[ Entrada: Webcam o Fotografía ]
               │
               ▼
[ Detector de Rostro (OpenCV / RetinaFace) ]
               │
               ├──> Detecta el área facial
               ├──> Recorta el rostro
               └──> Alinea ojos y boca
               │
               ▼
[ Capas Convolucionales de la CNN ]
               │
               └──> Convierte la imagen en un vector
                    de características (Embedding)
               │
               ▼
[ Comparación Vectorial (Distancia Coseno) ]
               │
               └──> Mide la diferencia angular contra
                    la base de datos (faces_db)
               │
               ▼
[ Evaluación del Umbral (Threshold) ]
               │
               └──> Determina si el margen de error
                    es suficientemente bajo
               │
               ├───────────────────────────┐
               ▼                           ▼
[ Registro Exitoso en CSV ]       [ Rostro No Reconocido ]
```

### La Matemática Detrás: Distancia Coseno

Para determinar si el rostro capturado (`u`) coincide con algún registro (`v`) en la carpeta `faces_db/`, el modelo mide la orientación entre sus vectores normados.

La métrica utilizada es la **Distancia Coseno**:

$$
D_C(\mathbf{u}, \mathbf{v}) =
1 -
\frac{\mathbf{u} \cdot \mathbf{v}}
{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}
$$

Donde:

* El producto punto `u · v` mide la similitud entre ambos vectores.
* Las normas `L₂` normalizan la magnitud de los vectores.
* La métrica evalúa principalmente la orientación relativa de las representaciones faciales.
* Si el valor final `D_C` está por debajo del umbral de tolerancia establecido por el modelo, el sistema confirma la coincidencia biométrica de la persona.

---

## 📂 Estructura del Repositorio

La arquitectura está diseñada para ser modular, ligera y sin necesidad de servicios de bases de datos externas.

```text
vision_por_computadora/
├── app/
│   ├── faces_db/         # Base de datos local de imágenes de referencia (.jpg / .png)
│   ├── templates/
│   │   ├── index.html    # Frontend interactivo en HTML5 y JavaScript
│   │   └── style.css     # Estilos visuales (Neón, vidrio esmerilado y modo oscuro)
│   ├── asistencia.csv    # Registro persistente generado automáticamente
│   └── main.py           # Servidor FastAPI y lógica de inferencia con DeepFace
├── .gitignore
├── LICENSE
├── README.md             # Documentación del proyecto
├── requirements.txt      # Librerías y dependencias de Python
└── start.sh              # Script bash para entorno virtual y ejecución automática
```

---

## 🛠️ Instalación y Arranque Automático

Sigue estos pasos para poner en marcha **FacePass** en tu entorno local.

### 1. Navegar al Directorio del Proyecto

Abre una terminal y ejecuta:

```bash
cd vision_por_computadora
```

### 2. Arrancar la Aplicación

Ejecuta el script automatizado `start.sh`.

Este se encargará de:

1. Crear el entorno virtual (`.venv`).
2. Actualizar `pip`.
3. Instalar los paquetes especificados en `requirements.txt`.
4. Levantar el servidor FastAPI.

```bash
./start.sh
```

### 3. Abrir el Navegador

Con el servidor en ejecución, ingresa a:

**http://127.0.0.1:8000**

> 💡 **Nota de primera ejecución:** La primera vez que presiones **"Registrar Asistencia"**, DeepFace descargará automáticamente los pesos preentrenados necesarios para el modelo de reconocimiento facial (~90 MB). Este proceso ocurre únicamente durante la primera ejecución.

---

## 💻 Características del Dashboard

### 📸 Captura en Tiempo Real

Conexión con la webcam mediante la API `getUserMedia` de HTML5 para capturar y enviar imágenes directamente al servidor.

### 🛡️ Control Anti-Duplicados

El backend valida que la persona reconocida no cuente con un registro previo durante el mismo día, evitando entradas duplicadas.

### 📊 Tabla de Asistencia Dinámica

Actualización en vivo del listado de personas registradas, mostrando:

* Nombre.
* Fecha.
* Hora exacta.

La información se actualiza sin necesidad de recargar la página.

### 🌑 Interfaz Glassmorphism

Dashboard responsivo en modo oscuro con:

* Efectos de transparencia.
* Vidrio esmerilado.
* Estética de neón.
* Retroalimentación visual del estado del reconocimiento.
* Diseño adaptable a diferentes tamaños de pantalla.

---

## ⚡ Tecnologías Utilizadas

| Tecnología           | Uso                                                                                                            |
| -------------------- | -------------------------------------------------------------------------------------------------------------- |
| **FastAPI**          | API de alta velocidad en Python para el manejo de peticiones HTTP.                                             |
| **DeepFace**         | Librería de visión artificial y aprendizaje profundo para la extracción de embeddings y reconocimiento facial. |
| **OpenCV**           | Decodificación y procesamiento de imágenes.                                                                    |
| **NumPy**            | Procesamiento y operaciones matriciales.                                                                       |
| **Pandas**           | Manipulación de datos y persistencia del historial en archivos CSV.                                            |
| **HTML5**            | Estructura del frontend y acceso a la webcam mediante `getUserMedia`.                                          |
| **CSS3**             | Diseño visual, responsive design y efectos Glassmorphism.                                                      |
| **JavaScript (ES6)** | Lógica interactiva y comunicación con el backend.                                                              |

---

## 🔄 Flujo General del Sistema

```text
              ┌─────────────────┐
              │     Webcam      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Frontend      │
              │ HTML + JS       │
              └────────┬────────┘
                       │
                 HTTP Request
                       │
                       ▼
              ┌─────────────────┐
              │    FastAPI      │
              │    Backend      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ OpenCV /        │
              │ RetinaFace      │
              └────────┬────────┘
                       │
                  Rostro detectado
                       │
                       ▼
              ┌─────────────────┐
              │    DeepFace     │
              │   Embedding     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Distancia Coseno│
              │  + Threshold    │
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        ┌───────────┐     ┌──────────────┐
        │ Coincide  │     │ No reconocido│
        └─────┬─────┘     └──────────────┘
              │
              ▼
        ┌───────────────┐
        │ asistencia.csv│
        └───────┬───────┘
                │
                ▼
        ┌────────────────┐
        │    Dashboard   │
        │ Nombre + Fecha │
        │     + Hora     │
        └────────────────┘
```

---

## 🚀 Objetivo del Proyecto

**FacePass** busca demostrar cómo las tecnologías modernas de **visión por computadora, aprendizaje profundo y desarrollo web** pueden integrarse para crear un sistema de asistencia automatizado, rápido y sin contacto físico.

El proyecto combina procesamiento de imágenes, reconocimiento facial, comparación de embeddings, una API backend y una interfaz web interactiva en una única aplicación local.
