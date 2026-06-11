# Manual de Usuario — SmartBot

## Índice

1. [Requisitos previos](#1-requisitos-previos)
2. [Instalación y configuración](#2-instalación-y-configuración)
3. [Levantar el proyecto](#3-levantar-el-proyecto)
4. [Panel administrativo](#4-panel-administrativo)
5. [Uso del bot de Telegram](#5-uso-del-bot-de-telegram)
6. [Solución de problemas comunes](#6-solución-de-problemas-comunes)

---

## 1. Requisitos previos

Antes de ejecutar el proyecto asegúrate de tener instalado:

- **Docker Desktop** (Windows/Mac) o **Docker Engine + Docker Compose** (Linux)
  - Verificar: `docker --version` y `docker compose version`
- **Git**
  - Verificar: `git --version`
- Conexión a internet (para descargar imágenes de Docker y comunicarse con Telegram)

---

## 2. Instalación y configuración

### 2.1 Clonar el repositorio

```bash
git clone https://github.com/<usuario>/IA1_VACASJUN2026.git
cd IA1_VACASJUN2026/practica2
```

### 2.2 Crear el archivo de variables de entorno

Copiar el archivo de ejemplo y editarlo con los valores reales:

```bash
cp .env.example .env
```

Abrir `.env` y completar los valores:

```env
# Token del bot (obtenido desde BotFather en Telegram)
TELEGRAM_TOKEN=<tu_token_aquí>

# Credenciales del administrador (no modificar para evaluación)
ADMIN_USER=IA1-User
ADMIN_PASSWORD=IA1-password@_new

# Credenciales de la base de datos
DB_USER=postgres
DB_PASSWORD=postgres

# Clave secreta para las sesiones del panel (cualquier cadena larga)
SECRET_KEY=cambia_esta_clave_por_una_segura
```

> **Importante:** El archivo `.env` contiene información sensible. Nunca lo subas a GitHub.

---

## 3. Levantar el proyecto

### 3.1 Primera vez (construcción de imágenes)

Desde la carpeta `practica2/`:

```bash
docker compose up --build -d
```

Este comando:
1. Construye las imágenes de `api` y `bot`
2. Levanta los 3 servicios (`db`, `api`, `bot`) en segundo plano

### 3.2 Poblar la base de datos

Solo es necesario hacerlo **una vez**, después del primer `up`:

```bash
docker compose exec api python seed.py
```

Salida esperada:
```
Categorías y preguntas creadas.
Usuario admin creado.
```

### 3.3 Verificar que todo está corriendo

```bash
docker compose ps
```

Los tres servicios deben aparecer con estado `Up` o `running`.

Para ver logs en tiempo real:

```bash
docker compose logs -f
```

Para ver solo un servicio:

```bash
docker compose logs api -f
docker compose logs bot -f
```

### 3.4 Usos posteriores

Una vez que ya construiste las imágenes y poblaste la DB, para iniciar el proyecto:

```bash
docker compose up -d
```

Para detener:

```bash
docker compose down
```

---

## 4. Panel administrativo

### 4.1 Acceder al panel

Con el proyecto corriendo, abrir el navegador en:

```
http://localhost:8000/login
```

### 4.2 Iniciar sesión

Ingresar las credenciales de administrador:

- **Usuario:** `IA1-User`
- **Contraseña:** `IA1-password@_new`

> El botón "Mostrar" permite ver la contraseña antes de enviar el formulario.

Al ingresar correctamente se redirige al **Dashboard**.

---

### 4.3 Dashboard

Muestra un resumen del sistema:
- Total de preguntas registradas
- Total de categorías
- Preguntas activas e inactivas

---

### 4.4 Gestión de Preguntas

Navegar a **Preguntas** en el menú lateral.

#### Crear una pregunta nueva

1. Hacer clic en **Nueva pregunta**
2. Completar los campos:
   - **Pregunta:** texto de la consulta frecuente
   - **Respuesta:** texto que el bot responderá
   - **Categoría:** seleccionar de la lista (opcional)
   - **Activa:** marcar para que el bot pueda usarla
3. Hacer clic en **Guardar**

#### Editar una pregunta

1. En la lista de preguntas, hacer clic en **Editar** en la fila correspondiente
2. Modificar los campos deseados
3. Hacer clic en **Guardar**

#### Desactivar una pregunta

Al editar una pregunta, desmarcar el checkbox **Activa**. El bot dejará de usar esa pregunta sin eliminarla.

#### Eliminar una pregunta

1. En la lista, hacer clic en **Eliminar**
2. Confirmar la acción en el diálogo del navegador

---

### 4.5 Gestión de Categorías

Navegar a **Categorías** en el menú lateral.

#### Crear una categoría

1. Hacer clic en **Nueva categoría**
2. Ingresar nombre y descripción
3. Hacer clic en **Guardar**

#### Editar o eliminar

Mismos pasos que en preguntas.

> **Nota:** No se puede eliminar una categoría que tenga preguntas asignadas. Primero reasignar o eliminar las preguntas.

---

### 4.6 Configuración del Chat ID

Navegar a **Configuración** en el menú lateral.

1. Obtener el ID del grupo o chat de Telegram donde el bot debe enviar mensajes
   - En Telegram, agregar el bot `@RawDataBot` al grupo y enviará el chat ID
   - O usar la URL: `https://api.telegram.org/bot<TOKEN>/getUpdates` y buscar `chat.id`
2. Ingresar el ID en el campo **Chat ID de Telegram**
3. Hacer clic en **Guardar configuración**

---

### 4.7 Cerrar sesión

Hacer clic en **Cerrar sesión** en la parte inferior del menú lateral.

---

## 5. Uso del bot de Telegram

### 5.1 Encontrar el bot

Buscar el bot por su nombre de usuario en Telegram (el que se configuró en BotFather) y abrir la conversación.

### 5.2 Comandos disponibles

| Comando | Descripción |
|---|---|
| `/start` | Mensaje de bienvenida e instrucciones básicas |
| `/ayuda` | Explica cómo usar el bot |
| `/categorias` | Lista los temas disponibles en el sistema |

### 5.3 Realizar una consulta

Simplemente escribe tu pregunta en el chat, sin necesidad de usar comandos:

**Ejemplos de consultas:**
```
¿Cuál es el horario de atención?
horario
inscripción
¿Qué documentos necesito?
exámenes finales
```

El bot buscará la respuesta más cercana en la base de datos y responderá automáticamente.

### 5.4 Cuando no hay respuesta

Si el bot no encuentra información relacionada con la consulta, responderá:

> _"No encontré información sobre eso. Puedes intentar reformular tu consulta o escribir /categorias para ver los temas disponibles."_

En ese caso, intenta:
- Usar palabras clave más simples
- Revisar los temas disponibles con `/categorias`
- Reformular la pregunta

---

## 6. Solución de problemas comunes

### El panel no carga en `localhost:8000`

Verificar que el servicio `api` está corriendo:
```bash
docker compose ps
docker compose logs api --tail=20
```

### El bot no responde en Telegram

1. Verificar que el token en `.env` es correcto
2. Verificar que el servicio `bot` está corriendo:
```bash
docker compose logs bot --tail=20
```
3. Si aparece el error `Unauthorized`, el token es inválido. Obtener uno nuevo desde BotFather.

### La base de datos está vacía (no hay preguntas)

Ejecutar el seed:
```bash
docker compose exec api python seed.py
```

### Errores al levantar por primera vez

Si hay errores de build, reconstruir desde cero:
```bash
docker compose down -v
docker compose up --build -d
```

> **Advertencia:** `down -v` elimina los datos de la base de datos. Volver a ejecutar el seed después.

### No puedo hacer login con `IA1-User`

El usuario admin se crea con el seed. Verificar que el seed se ejecutó correctamente. Si el problema persiste:
```bash
docker compose down -v
docker compose up --build -d
docker compose exec api python seed.py
```
