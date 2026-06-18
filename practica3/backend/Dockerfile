FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

# tesseract-ocr: motor OCR
# chromium + chromium-driver: navegador headless para el RPA con Selenium
RUN apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr \
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

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
