from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Hotfix: Habilitar CORS para evitar bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrumentación Prometheus en /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/weather")
def get_weather():
    return {
        "location": "Valparaíso",
        "temperature": 18,
        "status": "Soleado",
        "wind_speed_kmh": 12
    }


@app.get("/error-test")
def error_test():
    raise HTTPException(
        status_code=500,
        detail="Error simulado para validación de métricas 5xx"
    )