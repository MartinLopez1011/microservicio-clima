# ==============================================================================
# Dockerfile: Microservicio de Clima (FastAPI)
# Cumplimiento: Indicador de Evaluación IE1 (Contenerización)
# ==============================================================================

# 1. Imagen base oficial ligera y segura de Python 3.11
FROM python:3.11-slim

# Metadatos del contenedor
LABEL maintainer="Equipo DevOps <soporte@duocuc.cl>"
LABEL description="Microservicio de Pronóstico Climático contenerizado con FastAPI"
LABEL version="1.1.0"

# Variables de entorno para optimización de Python en contenedores
# - PYTHONDONTWRITEBYTECODE: Evita la creación de archivos .pyc en el contenedor
# - PYTHONUNBUFFERED: Asegura que los logs de Python se emitan directamente a stdout/stderr
# - PORT: Puerto de escucha del microservicio
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# 2. Definición del directorio de trabajo en el contenedor
WORKDIR /app

# 3. Creación de usuario sin privilegios por seguridad (Non-Root User)
# Práctica recomendada en DevOps para reducir la superficie de ataque
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin -d /app appuser

# 4. Copia e instalación de dependencias
# Se aprovecha la caché de capas de Docker copiando solo requirements.txt primero
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copia del código fuente de la aplicación
COPY main.py .

# Asignación de permisos al usuario no privilegiado
RUN chown -R appuser:appgroup /app

# Cambio al usuario seguro
USER appuser

# 6. Exposición del puerto de red
EXPOSE 8000

# 7. Verificación de salud (Healthcheck nativo del contenedor)
# Verifica periódicamente que el endpoint /weather responda correctamente
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/weather')" || exit 1

# 8. Comando de inicio del servidor ASGI Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
