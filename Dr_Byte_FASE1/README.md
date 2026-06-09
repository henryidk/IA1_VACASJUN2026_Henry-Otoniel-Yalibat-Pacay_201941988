# Doctor Byte

Sistema experto para el diagnóstico de fallas comunes en computadoras, desarrollado con Prolog como motor de inferencia e integrado con una interfaz web y un bot de Telegram.

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Motor de inferencia | SWI-Prolog + PySwip |
| Backend | Python + Flask |
| Frontend | HTML + CSS + JavaScript |
| Notificaciones | Telegram Bot API |
| Contenedores | Docker + Docker Compose |
| Persistencia | JSON |

## Requisitos previos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Instalación y ejecución

1. Clonar el repositorio
2. Copiar el archivo de variables de entorno y completarlo con tus credenciales:

```bash
cp .env.example .env
```

3. Levantar el sistema:

```bash
docker-compose up
```

4. Abrir el navegador en `http://localhost:80`

## Estructura del proyecto

```
Dr_Byte_FASE1/
├── backend/      # API Flask + integración con Prolog y Telegram
├── frontend/     # Interfaz web (HTML, CSS, JS)
├── prolog/       # Base de conocimiento (.pl)
└── docs/         # Documentación técnica y manual de usuario
```
