# Manual de Usuario
## Sistema de Rutas Interdepartamentales — Guatemala

---

## Índice

1. [Introducción](#1-introducción)
2. [Requisitos del sistema](#2-requisitos-del-sistema)
3. [Instalación](#3-instalación)
4. [Cómo ejecutar el sistema](#4-cómo-ejecutar-el-sistema)
5. [Cómo usar el sistema](#5-cómo-usar-el-sistema)
   - 5.1 [Buscar rutas entre ciudades](#51-buscar-rutas-entre-ciudades)
   - 5.2 [Interpretar los resultados](#52-interpretar-los-resultados)
   - 5.3 [Agregar nuevas ciudades](#53-agregar-nuevas-ciudades)
   - 5.4 [Confirmar o descartar cambios](#54-confirmar-o-descartar-cambios)
6. [Mensajes de error y soluciones](#6-mensajes-de-error-y-soluciones)
7. [Preguntas frecuentes](#7-preguntas-frecuentes)

---

## 1. Introducción

El **Sistema de Rutas Interdepartamentales** es una herramienta que permite a empresas de transporte encontrar la ruta más corta entre ciudades de Guatemala, así como consultar todas las rutas posibles entre dos puntos.

El sistema utiliza **Prolog** como motor de inteligencia para calcular rutas y **Python** como puente entre la lógica y la interfaz web.

---

## 2. Requisitos del sistema

Antes de instalar, verifica que tu computadora tenga lo siguiente:

| Requisito | Versión mínima | Cómo verificar |
|---|---|---|
| Python | 3.11 o superior | `python3 --version` |
| SWI-Prolog | 9.x | `swipl --version` |
| Navegador web | Cualquier moderno | Chrome, Firefox, Edge |

### Instalar SWI-Prolog (si no lo tienes)

**Linux (Ubuntu/Debian):**
```bash
sudo apt install swi-prolog
```

**Windows / macOS:**
Descárgalo desde: https://www.swi-prolog.org/Download.html

---

## 3. Instalación

### Paso 1 — Descarga el proyecto

Clona o descarga el repositorio en tu computadora.

### Paso 2 — Instala las dependencias de Python

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará automáticamente:
- `fastapi` — servidor web
- `uvicorn` — servidor ASGI
- `pyswip` — puente entre Python y Prolog

### Paso 3 — Verifica que todo esté listo

```bash
python3 -c "import fastapi, uvicorn, pyswip; print('Dependencias OK')"
swipl --version
```

Si ambos comandos responden sin error, estás listo.

---

## 4. Cómo ejecutar el sistema

### Paso 1 — Abre una terminal en la carpeta del proyecto

```
PRACTICA1LABCLAUDE/
```

### Paso 2 — Inicia el servidor

```bash
uvicorn backend.main:app --reload --port 8000
```

Verás un mensaje como este cuando el servidor esté listo:

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Paso 3 — Abre el navegador

Ingresa la siguiente dirección en tu navegador:

```
http://localhost:8000/app
```

El sistema cargará automáticamente con todas las ciudades disponibles.

> **Nota:** No cierres la terminal mientras usas el sistema. El servidor debe permanecer activo.

---

## 5. Cómo usar el sistema

La interfaz tiene dos secciones principales, accesibles desde las pestañas superiores:

- **Buscar Rutas** — consulta rutas entre ciudades existentes
- **Gestionar Ciudades** — agrega nuevas ciudades y conexiones

---

### 5.1 Buscar rutas entre ciudades

1. Haz clic en la pestaña **Buscar Rutas** (activa por defecto al iniciar).

2. En el campo **Ciudad de Origen**, selecciona la ciudad desde donde parte el viaje.

3. En el campo **Ciudad de Destino**, selecciona la ciudad a la que deseas llegar.

4. Haz clic en el botón **Buscar Rutas**.

5. El sistema consultará el motor Prolog y mostrará los resultados en pantalla.

> **Importante:** El origen y el destino deben ser ciudades diferentes. Si seleccionas la misma ciudad en ambos campos, el sistema mostrará un mensaje de error.

---

### 5.2 Interpretar los resultados

Tras realizar una búsqueda, verás tres secciones de resultados:

#### Ruta más corta (tarjeta verde)

Muestra el camino óptimo entre las dos ciudades seleccionadas. Las ciudades aparecen conectadas con flechas `→` y al final se indica la distancia total en kilómetros.

**Ejemplo:**
```
Guatemala → Cobán → Flores        575 km
```

#### Estadísticas

Cuatro tarjetas con información sobre todas las rutas encontradas:

| Tarjeta | Qué muestra |
|---|---|
| Total de rutas | Cantidad de caminos diferentes encontrados |
| Distancia mínima | La ruta más corta (coincide con la tarjeta verde) |
| Distancia máxima | La ruta más larga encontrada |
| Distancia promedio | Promedio de todas las rutas |

#### Todas las rutas

Lista completa de rutas ordenadas de menor a mayor distancia. Cada fila muestra:
- Un número de posición (el **#1** en verde es la más corta)
- Las ciudades del recorrido separadas por `→`
- La distancia total en kilómetros

---

### 5.3 Agregar nuevas ciudades

Si necesitas agregar una ciudad que no está en el sistema:

1. Haz clic en la pestaña **Gestionar Ciudades**.

2. En el campo **Nombre de la ciudad**, escribe el nombre de la nueva ciudad.
   - Ejemplo: `Jalapa`

3. En la sección **Conexiones**, selecciona con qué ciudad existente conecta y escribe la distancia en kilómetros.
   - Ejemplo: conecta con `Guatemala` a `98` km

4. Si la ciudad conecta con más de una ciudad, haz clic en **+ Agregar conexión** para agregar más filas.

5. Haz clic en **Agregar a sesión**.

6. La ciudad aparecerá en el panel derecho **Sesión actual** como pendiente de confirmación.

> **Nota:** La ciudad se almacena temporalmente en la sesión. Aún no está disponible para búsquedas hasta que confirmes los cambios.

---

### 5.4 Confirmar o descartar cambios

Después de agregar una o más ciudades a la sesión, tienes dos opciones:

#### Confirmar cambios

Haz clic en **Confirmar cambios**. El sistema:
- Guarda las nuevas ciudades en un archivo Prolog extendido
- Actualiza automáticamente los dropdowns de búsqueda
- Las nuevas ciudades ya estarán disponibles para consultar rutas

#### Limpiar sesión

Haz clic en **Limpiar sesión** para descartar todas las ciudades pendientes sin guardarlas.

> **Nota:** La base de conocimiento original del sistema nunca se modifica. Las ciudades nuevas se guardan en un archivo separado (`rutas_extended.pl`).

---

## 6. Mensajes de error y soluciones

| Mensaje | Causa | Solución |
|---|---|---|
| `Por favor selecciona una ciudad de origen y una de destino` | No se seleccionó alguna ciudad | Selecciona ambas ciudades antes de buscar |
| `El origen y el destino no pueden ser la misma ciudad` | Se seleccionó la misma ciudad dos veces | Selecciona ciudades diferentes |
| `La ciudad 'X' no existe en la base de conocimiento` | Ciudad no registrada | Verifica el nombre o agrégala en Gestionar Ciudades |
| `No existe ninguna ruta entre 'X' y 'Y'` | Las ciudades no están conectadas por ningún camino | No hay ruta posible con las conexiones actuales |
| `No se pudo conectar con el servidor` | El servidor no está activo | Ejecuta `uvicorn backend.main:app --port 8000` en la terminal |
| `Completa todas las conexiones con ciudad y distancia válida` | Fila de conexión incompleta | Rellena todos los campos antes de agregar la ciudad |
| `La ciudad 'X' ya existe` | El nombre ingresado ya está registrado | Usa un nombre diferente |

---

## 7. Preguntas frecuentes

**¿Puedo usar el sistema sin internet?**
Sí. El sistema funciona completamente en local, no requiere conexión a internet.

**¿Las ciudades que agrego se guardan permanentemente?**
Sí, una vez que haces clic en **Confirmar cambios**, se guardan en el archivo `prolog/rutas_extended.pl`. La próxima vez que inicies el servidor, seguirán disponibles.

**¿Qué pasa si cierro el servidor sin confirmar?**
Las ciudades que estaban en sesión pero no confirmadas se pierden. Solo se pierden las pendientes, no las ya confirmadas.

**¿Puedo agregar varias ciudades antes de confirmar?**
Sí. Puedes agregar múltiples ciudades una por una a la sesión y confirmarlas todas al mismo tiempo.

**¿Las distancias están en kilómetros?**
Sí, todas las distancias del sistema están expresadas en kilómetros.
