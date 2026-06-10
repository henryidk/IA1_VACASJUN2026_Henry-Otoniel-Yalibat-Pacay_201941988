# SmartBot — Plan de Trabajo (Práctica 2)

**Fecha de entrega:** 12/06/2026
**Tiempo disponible:** 2 días

---

## Orden de trabajo recomendado

```
Hoy (10 jun):   Fase 1 → Fase 2 → Fase 3 → Fase 4
Mañana (11 jun): Fase 5 → Fase 6 (opcional) → Fase 7
12 jun:         Revisión final, evidencias, entrega
```

---

## Fase 1 — Setup e Infraestructura
> Base del proyecto. Todo lo demás depende de esto.

- [ ] Inicializar repositorio y estructura de carpetas (`/bot`, `/api`, `/frontend`, `/db`)
- [ ] Crear `docker-compose.yml` con todos los servicios (API, bot, DB, frontend)
- [ ] Configurar variables de entorno (`.env.example`) — TOKEN Telegram, DB_URL, SECRET_KEY
- [ ] Crear Dockerfile para el backend (Python 3.11)

---

## Fase 2 — Base de Datos y Modelos
> Diseño de datos. Cimientos de la API y el bot.

- [ ] Diseñar y documentar diagrama ER (entidades: preguntas, respuestas, categorías, admins, logs)
- [ ] Implementar modelos ORM (SQLAlchemy o Motor según DB elegida)
- [ ] Script de seed con 20+ preguntas frecuentes y 3+ categorías
- [ ] Configurar migraciones o inicialización de la DB (Alembic o `CREATE TABLE` inicial)

---

## Fase 3 — API REST
> Backend en Python (FastAPI recomendado).

- [ ] Login simple: verificar credenciales contra la DB y guardar sesión (usuario: `IA1-User` / pass: `IA1-password@_new`)
- [ ] Rutas protegidas verifican sesión activa
- [ ] CRUD `/preguntas` — GET, POST, PUT, DELETE
- [ ] CRUD `/categorias` — GET, POST, PUT, DELETE
- [ ] Endpoint de búsqueda/consulta para el bot — `GET /consulta?q=texto`
- [ ] Endpoint para configurar el chat ID de Telegram — `PUT /config/chat_id`
- [ ] Endpoint de fallback para mensajes sin respuesta (retorna mensaje por defecto)

---

## Fase 4 — Bot de Telegram
> Lógica del bot conectado a la API.

- [ ] Crear bot con BotFather y configurar TOKEN (guardar en `.env`)
- [ ] Escuchar mensajes y consultar la API (`python-telegram-bot`)
- [ ] Responder con datos de la DB (nunca respuestas hardcodeadas)
- [ ] Manejo de mensajes sin coincidencia (mensaje amigable al usuario)

---

## Fase 5 — Panel Administrativo
> Interfaz web para el admin.

- [ ] Pantalla de login (formulario simple, validar contra API)
- [ ] Vista CRUD de preguntas y respuestas
- [ ] Vista CRUD de categorías (asignar categoría a preguntas)
- [ ] Configuración del chat ID de Telegram desde el panel
- [ ] Vista de estadísticas *(opcional pero recomendada)*

---

## Fase 6 — Features Opcionales
> Registrar uso del bot y estadísticas.

- [ ] Guardar log de cada consulta (fecha, usuario Telegram, consulta, respuesta)
- [ ] Endpoint de estadísticas en la API (top consultas, total usuarios)
- [ ] Vista de estadísticas en el panel admin (gráficas o tablas)

---

## Fase 7 — Documentación y Cierre
> Entregables finales. Hacer en paralelo con el desarrollo.

- [ ] `README.md` con instrucciones de instalación y ejecución
- [ ] Manual técnico (`MANUAL_TECNICO.md`) — arquitectura, API, Docker, modelo de datos
- [ ] Manual de usuario (`MANUAL_USUARIO.md`) — capturas de pantalla incluidas
- [ ] Diagrama de patrón de arquitectura
- [ ] Evidencias de funcionamiento (capturas: login, CRUD, bot en Telegram, stats)
- [ ] Verificar historial de commits (mínimo 5 funcionales, no masivos del mismo día)

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| **Framework API** | FastAPI |
| **Panel admin** | Jinja2 (servido desde FastAPI, sin servicio extra) |
| **Base de datos** | PostgreSQL 15 |
| **ORM** | SQLAlchemy (tablas se crean al arrancar, sin migraciones) |
| **Bot** | python-telegram-bot (async, polling) |
| **Autenticación** | SessionMiddleware de Starlette (sesión simple, sin JWT) |
| **Contenedores** | Docker Compose — 3 servicios: `api`, `bot`, `db` |
| **Nube (temporal)** | Railway (free tier $5/mes) |
| **Nube (definitiva)** | Oracle Cloud Free Tier (si Railway no alcanza) |

---

## Notas técnicas

- **Autenticación:** login simple con sesión/cookie — sin JWT. El servidor valida credenciales, guarda sesión; las rutas protegidas solo verifican si la sesión existe.
- **Bot ↔ API:** el bot consulta la API sin autenticación especial (comunicación interna dentro de Docker).
- **Restricciones del enunciado:** toda la información en DB, sin respuestas hardcodeadas, sin plataformas de chatbot de terceros.
