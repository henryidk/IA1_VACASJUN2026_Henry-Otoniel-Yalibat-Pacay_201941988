# Manual de Usuario — Doctor Byte

## ¿Qué es Doctor Byte?

Doctor Byte es un sistema experto que te ayuda a identificar posibles fallas en tu computadora. Solo debes seleccionar los síntomas que observas y el sistema te dará un diagnóstico con recomendaciones para resolverlo.

---

## 1. Requisitos para ejecutar el sistema

- Tener instalado **Docker** y **Docker Compose**
- Conexión a internet (para las notificaciones de Telegram, opcional)

---

## 2. Instalación y primera ejecución

### Paso 1 — Configurar variables de entorno

En la carpeta del proyecto, copia el archivo de configuración:

```bash
cp .env.example .env
```

Abre el archivo `.env` y completa tus credenciales de Telegram (opcional, el sistema funciona sin esto):

```
TELEGRAM_TOKEN=token_de_tu_bot
TELEGRAM_CHAT_ID=tu_chat_id
```

### Paso 2 — Levantar el sistema

```bash
docker-compose up
```

Espera hasta que aparezca el mensaje indicando que el backend está listo.

### Paso 3 — Abrir en el navegador

| Pantalla | URL |
|---|---|
| Diagnóstico | http://localhost:8080 |
| Historial | http://localhost:8080/historial.html |
| Administración | http://localhost:8080/admin.html |

---

## 3. Realizar un diagnóstico

### 3.1 Seleccionar síntomas

En la pantalla principal verás una lista de síntomas. Marca todos los que aplican a la situación de tu computadora.

Los síntomas disponibles incluyen:

- Pantalla negra al encender
- Pantalla azul con código de error (BSOD)
- El equipo se reinicia solo
- Lentitud extrema del sistema
- El equipo no enciende
- Sobrecalentamiento
- Ruidos extraños en el disco duro
- El sistema no detecta el disco duro
- Error al iniciar el sistema operativo
- El monitor no muestra imagen
- El sistema se congela
- No detecta dispositivos USB
- No se conecta a WiFi
- La batería no carga
- El ventilador hace ruido excesivo
- Las aplicaciones se cierran solas
- Mensajes de memoria insuficiente

### 3.2 Solicitar el diagnóstico

Una vez seleccionados los síntomas, haz clic en el botón **Diagnosticar**.

### 3.3 Ver el resultado

El sistema mostrará:

- **Falla detectada**: el problema más probable según los síntomas seleccionados
- **Recomendaciones**: pasos ordenados para intentar resolver la falla

Si tienes el bot de Telegram configurado, recibirás una notificación con el diagnóstico en tu chat.

### 3.4 Reiniciar la consulta

Para hacer un nuevo diagnóstico desde cero, haz clic en el botón **Restablecer**.

---

## 4. Ver el historial de diagnósticos

Desde el menú de navegación, haz clic en **Historial** o accede a:

```
http://localhost:8080/historial.html
```

Verás una lista de todos los diagnósticos realizados, con fecha, síntomas, falla detectada y recomendaciones.

---

## 5. Panel de administración

El panel de administración permite gestionar el conocimiento del sistema y configurar el bot de Telegram.

Accede desde el menú en **Administración** o directamente en:

```
http://localhost:8080/admin.html
```

### 5.1 Gestión de síntomas

**Agregar un síntoma:**
1. Escribe la descripción del síntoma en el campo de texto
2. El sistema genera el ID automáticamente
3. Selecciona la falla que este síntoma indica
4. Haz clic en **Agregar síntoma**

**Editar la descripción de un síntoma:**
1. Haz clic en el ícono de lápiz (✏️) junto al síntoma
2. Modifica el texto en el campo que aparece
3. Confirma con ✔ o cancela con ✖

**Editar la falla que indica un síntoma (regla):**
1. Haz clic sobre el badge verde que muestra la falla actual
2. Selecciona la nueva falla en el dropdown que aparece
3. Confirma con ✔

**Eliminar un síntoma:**
1. Haz clic en el ícono de basura (🗑) junto al síntoma
2. Confirma la acción en el mensaje de alerta

> Al eliminar un síntoma se eliminan automáticamente todas sus reglas asociadas.

### 5.2 Gestión de fallas y recomendaciones

Las fallas se muestran en un acordeón. Al expandir una falla se ven sus recomendaciones.

**Agregar una falla:**
1. Escribe la descripción en el campo **Agregar falla**
2. Haz clic en **Agregar falla**

**Editar la descripción de una falla:**
1. Haz clic en el ícono de lápiz (✏️) en el encabezado del acordeón
2. Aparece un campo debajo del título — modifica el texto
3. Confirma con ✔ o cancela con ✖

**Agregar una recomendación a una falla:**
1. Expande la falla en el acordeón
2. Escribe la recomendación en el campo inferior
3. Haz clic en **Agregar**

**Editar una recomendación:**
1. Haz clic en el ícono de lápiz (✏️) junto a la recomendación
2. Modifica el texto en el campo que aparece
3. Confirma con ✔

**Eliminar una recomendación:**
1. Haz clic en el ícono ✖ junto a la recomendación

**Eliminar una falla:**
1. Expande la falla en el acordeón
2. Haz clic en **Eliminar esta falla**
3. Confirma la acción

> Al eliminar una falla se eliminan también todas sus reglas y recomendaciones.

### 5.3 Configuración del Bot de Telegram

En la sección **Configuración del Bot de Telegram** puedes:

| Campo | Descripción |
|---|---|
| Token del bot | Credencial del bot (obtenida de @BotFather). Dejar vacío para usar el del `.env` |
| Chat ID de destino | A quién llegan las notificaciones. Dejar vacío para usar el del `.env` |
| Encabezado del mensaje | La primera línea que aparece en la notificación de Telegram |
| Estado del bot | Activo: envía notificaciones. Inactivo: envía mensaje de mantenimiento |

Para guardar los cambios, haz clic en **Guardar cambios**. Aparecerá una notificación confirmando el resultado.

---

## 6. Cómo obtener el Token del bot de Telegram

El token es la credencial que identifica a tu bot. Se obtiene desde **@BotFather**, el bot oficial de Telegram para crear y administrar bots.

### Pasos:

1. Abre Telegram y busca **@BotFather** en la barra de búsqueda
2. Presiona **Start** o escribe `/start`
3. Escribe el comando `/newbot`
4. BotFather te pedirá un **nombre** para el bot (ej: `Doctor Byte Notificaciones`) — este es el nombre visible
5. Luego te pedirá un **username** — debe terminar en `bot` (ej: `doctorbyte_notif_bot`)
6. Si el username está disponible, BotFather te responderá con el token:

```
Done! Congratulations on your new bot.
...
Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

7. Copia ese token y pégalo en el campo **Token del bot** del panel de administración, o en el archivo `.env`:

```
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

> El token es privado — no lo compartas ni lo subas a repositorios públicos.

---

## 7. Cómo obtener tu Chat ID de Telegram

1. Busca **@userinfobot** en Telegram y presiona Start
2. El bot te responderá con tu ID de usuario
3. Copia ese número y pégalo en el campo **Chat ID** del panel de administración

Si quieres que las notificaciones lleguen a un grupo:
1. Crea un grupo en Telegram y agrega tu bot al grupo
2. Envía un mensaje al grupo
3. Consulta `https://api.telegram.org/bot<TOKEN>/getUpdates` para ver el `chat.id` del grupo (será un número negativo)

---

## 7. Detener el sistema

Para detener los contenedores:

```bash
docker-compose down
```

Los datos del historial y la configuración del bot se conservan en la carpeta `data/` aunque el sistema esté detenido.
