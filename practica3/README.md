# SmartInvoice

Plataforma para automatizar el procesamiento de facturas (PDF/JPG/PNG) mediante Computer Vision, OCR y RPA: extrae los datos relevantes de cada factura, los valida, los almacena y dispara reportes administrativos y notificaciones por correo.

Práctica 3 del curso de Inteligencia Artificial 1. El detalle de requerimientos está en [`practica3.md`](./practica3.md) y el plan de trabajo en [`plan_trabajo.md`](./plan_trabajo.md).

## Tecnologías

- **Backend / API REST:** Python 3.11, FastAPI, SQLAlchemy, Alembic
- **Base de datos:** PostgreSQL
- **Computer Vision:** OpenCV
- **OCR:** Tesseract (pytesseract)
- **RPA:** Selenium + Chromium headless
- **Reportes:** ReportLab (PDF), openpyxl (Excel)
- **Correo:** SMTP
- **Frontend:** HTML, CSS, JavaScript servido por nginx
- **Contenedores:** Docker y Docker Compose
- **Despliegue:** Render (Web Service + Static Site + PostgreSQL gestionado)

## Estructura del proyecto

```
practica3/
├── backend/        # API REST, modelos, OCR, CV, RPA, reportes y correo
├── frontend/        # Interfaz web administrativa (estática, servida por nginx)
├── docs/           # Manual técnico, diagrama de arquitectura
├── docker-compose.yml
└── plan_trabajo.md
```

## Cómo ejecutar

> Instrucciones completas de instalación, ejecución y despliegue se documentarán a medida que avance el proyecto (ver `plan_trabajo.md`, grupo 19).

## Estado del proyecto

En desarrollo siguiendo `plan_trabajo.md`.
