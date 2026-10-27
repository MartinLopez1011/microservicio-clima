# Etapa 1: Builder (Compilación e instalación de dependencias)
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Etapa 2: Producción (Imagen limpia y segura solo con lo necesario para ejecutar)
FROM python:3.12-slim
WORKDIR /app

# Crear usuario sin privilegios por seguridad
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin -d /app appuser

COPY --from=builder /install /usr/local
COPY main.py .

RUN chown -R appuser:appgroup /app
USER appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/weather')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
