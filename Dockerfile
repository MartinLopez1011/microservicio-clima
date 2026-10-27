# Etapa 1: Builder (Compilación e instalación de dependencias)
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Etapa 2: Producción (Imagen limpia solo con lo necesario para ejecutar)
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY main.py .

ENV PORT=8000
EXPOSE 8000

CMD ["python", "main.py"]