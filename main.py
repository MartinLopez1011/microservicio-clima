from fastapi import FastAPI

app = FastAPI()

@app.get("/weather")
def get_weather():
    return {
        "location": "Valparaíso",
        "temperature": 18,
        "status": "Soleado",
        "wind_speed_kmh": 12
    }