FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# tesseract-ocr + tesseract-ocr-spa: motor OCR con datos de entrenamiento en español
# chromium + chromium-driver: navegador headless para el RPA con Selenium
RUN apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        tesseract-ocr-spa \
        chromium \
        chromium-driver \
        libglib2.0-0 \
        libnss3 \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# alembic upgrade head corre en cada arranque: es idempotente (no hace nada si ya
# está al día) y es necesario porque el plan free de Render no tiene Shell/SSH
# para correr migraciones manualmente.
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
