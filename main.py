from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Hotfix: Habilitar CORS para evitar bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather")
def get_weather():
    return {
        "location": "Valparaíso",
        "temperature": 18,
        "status": "Soleado",
        "wind_speed_kmh": 12
    }