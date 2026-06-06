# Manual Técnico
## Sistema de Rutas Interdepartamentales — Guatemala

---

## Índice

1. [Descripción general](#1-descripción-general)
2. [Tecnologías utilizadas](#2-tecnologías-utilizadas)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Patrón de arquitectura](#4-patrón-de-arquitectura)
5. [Base de conocimiento Prolog](#5-base-de-conocimiento-prolog)
6. [Integración Python — Prolog](#6-integración-python--prolog)
7. [Backend — API REST](#7-backend--api-rest)
8. [Frontend](#8-frontend)
9. [Flujo completo de una consulta](#9-flujo-completo-de-una-consulta)
10. [Seguridad y concurrencia](#10-seguridad-y-concurrencia)
11. [Posibles mejoras futuras](#11-posibles-mejoras-futuras)

---

## 1. Descripción general

El sistema permite encontrar rutas entre ciudades de Guatemala utilizando **programación lógica**. Toda la inteligencia de búsqueda reside en Prolog; Python actúa únicamente como capa de integración y exposición de resultados vía API REST.

**Restricciones de diseño respetadas:**
- Ningún algoritmo de búsqueda de rutas fue implementado en Python.
- El archivo Prolog original (`rutas.pl`) es de solo lectura.
- No se utiliza ninguna base de datos.

---

## 2. Tecnologías utilizadas

| Tecnología | Versión | Rol |
|---|---|---|
| SWI-Prolog | 9.2.x | Motor de inferencia lógica |
| Python | 3.11+ | Backend y capa de integración |
| PySwip | 0.2.x | Puente Python ↔ Prolog |
| FastAPI | 0.115+ | Framework del servidor REST |
| Uvicorn | 0.32+ | Servidor ASGI para FastAPI |
| HTML / CSS / JS | — | Frontend sin frameworks |

---

## 3. Estructura del proyecto

```
PRACTICA1LABCLAUDE/
│
├── prolog/
│   ├── rutas.pl                  ← Base de conocimiento original (solo lectura)
│   └── rutas_extended.pl         ← Generado por Python al agregar ciudades
│
├── backend/
│   ├── main.py                   ← Entrada de la aplicación FastAPI
│   ├── api/
│   │   └── routes.py             ← Endpoints REST (capa de presentación)
│   ├── services/
│   │   └── route_service.py      ← Lógica de negocio (capa de servicios)
│   └── prolog_integration/
│       └── prolog_engine.py      ← Comunicación con Prolog (capa de integración)
│
├── frontend/
│   ├── index.html                ← Estructura de la interfaz
│   ├── style.css                 ← Estilos visuales
│   └── app.js                   ← Funcionalidad del cliente
│
├── docs/
│   ├── manual_usuario.md
│   └── manual_tecnico.md
│
├── requirements.txt
├── .gitignore
└── CLAUDE.md
```

---

## 4. Patrón de arquitectura

El backend implementa una **arquitectura en capas** (Layered Architecture), donde cada capa tiene una responsabilidad única y solo se comunica con la capa inmediatamente inferior.

```
┌─────────────────────────────────────────┐
│         FRONTEND (HTML/CSS/JS)          │  ← Interfaz de usuario
│         Consume la API REST             │
└──────────────────┬──────────────────────┘
                   │ HTTP / JSON
┌──────────────────▼──────────────────────┐
│     CAPA DE PRESENTACIÓN (routes.py)    │  ← Recibe peticiones HTTP
│     Define endpoints, valida entrada,   │
│     devuelve respuestas HTTP            │
└──────────────────┬──────────────────────┘
                   │ Llamadas internas
┌──────────────────▼──────────────────────┐
│      CAPA DE SERVICIOS (route_service)  │  ← Lógica de negocio
│      Coordina validaciones, maneja      │
│      sesión, formatea resultados        │
└──────────────────┬──────────────────────┘
                   │ Llamadas internas
┌──────────────────▼──────────────────────┐
│  CAPA DE INTEGRACIÓN (prolog_engine)    │  ← Comunicación con Prolog
│  Ejecuta consultas via PySwip,          │
│  serializa resultados a Python          │
└──────────────────┬──────────────────────┘
                   │ PySwip
┌──────────────────▼──────────────────────┐
│       MOTOR PROLOG (rutas.pl)           │  ← Toda la lógica de rutas
│       Búsqueda, ciclos, distancias,     │
│       ruta más corta                    │
└─────────────────────────────────────────┘
```

**Ventajas de este patrón:**
- Cada capa puede modificarse sin afectar las demás.
- El motor Prolog es intercambiable sin tocar el frontend.
- Facilita las pruebas al aislar responsabilidades.

---

## 5. Base de conocimiento Prolog

### Archivo: `prolog/rutas.pl`

#### Hechos — Ciudades

```prolog
ciudad(guatemala).
ciudad(antigua).
% ... 12 ciudades en total
```

Cada hecho `ciudad/1` registra una ciudad válida en el sistema.

#### Hechos — Conexiones

```prolog
conexion(guatemala, antigua, 45).
conexion(guatemala, coban, 215).
% ... 18 conexiones en total
```

`conexion/3` recibe: origen, destino y distancia en km. Las conexiones son unidireccionales en su declaración.

#### Regla de bidireccionalidad

```prolog
conectado(X, Y, D) :- conexion(X, Y, D).
conectado(X, Y, D) :- conexion(Y, X, D).
```

Permite viajar en ambas direcciones sin duplicar los hechos.

#### Búsqueda de rutas (recursión con control de ciclos)

```prolog
ruta_aux(Destino, Destino, _, [Destino], 0).

ruta_aux(Actual, Destino, Visitados, [Actual|Resto], Distancia) :-
    conectado(Actual, Siguiente, D),
    \+ member(Siguiente, Visitados),
    ruta_aux(Siguiente, Destino, [Siguiente|Visitados], Resto, DistResto),
    Distancia is D + DistResto.
```

- **Caso base:** cuando la ciudad actual es el destino, el camino es `[Destino]` y la distancia es `0`.
- **Caso recursivo:** avanza hacia una ciudad vecina no visitada (`\+ member`), construye el camino y acumula la distancia.
- La lista `Visitados` garantiza que ninguna ciudad se repita en el recorrido.

#### Ruta más corta

```prolog
todas_las_rutas(Origen, Destino, RutasOrdenadas) :-
    findall(Distancia-Camino, ruta(Origen, Destino, Camino, Distancia), Rutas),
    msort(Rutas, RutasOrdenadas).

ruta_mas_corta(Origen, Destino, Camino, Distancia) :-
    todas_las_rutas(Origen, Destino, [Distancia-Camino|_]).
```

`findall/3` recolecta todas las soluciones de `ruta/4`. `msort/2` las ordena por distancia (la clave del par `Distancia-Camino`). La ruta más corta es el primer elemento de la lista ordenada.

#### Predicados de utilidad para el backend

```prolog
listar_ciudades(Ciudades) :- findall(C, ciudad(C), Ciudades).
ciudad_valida(Ciudad)     :- ciudad(Ciudad).
hay_ruta(Origen, Destino) :- ruta(Origen, Destino, _, _), !.
```

Estos predicados son el punto de entrada que usa Python para validar datos y consultar información sin implementar lógica en el backend.

---

## 6. Integración Python — Prolog

### Archivo: `backend/prolog_integration/prolog_engine.py`

La clase `PrologEngine` encapsula toda la comunicación con SWI-Prolog usando la librería **PySwip**.

#### Carga de archivos

```python
def _cargar(self):
    self._prolog.consult(self._base_pl)       # rutas.pl (siempre)
    if os.path.exists(self._extended_pl):
        self._prolog.consult(self._extended_pl) # rutas_extended.pl (si existe)
```

Siempre se carga el archivo original. Si existe el archivo extendido (generado por el usuario), se carga también para agregar las nuevas ciudades a la base de conocimiento activa.

#### Ejecución de consultas

```python
resultado = list(self._prolog.query("listar_ciudades(Ciudades)"))
```

`prolog.query()` devuelve un generador. Cada elemento es un diccionario donde las claves son las variables Prolog (`Ciudades`, `Camino`, `Distancia`) y los valores son los resultados unificados.

#### Archivo extendido generado

Cuando el usuario confirma nuevas ciudades, Python genera `rutas_extended.pl` con directivas `assertz`:

```prolog
:- dynamic ciudad/1, conexion/3.

:- assertz(ciudad(jalapa)).
:- assertz(conexion(jalapa, guatemala, 98)).
```

`assertz` agrega hechos al intérprete Prolog en tiempo de ejecución sin reemplazar los hechos del archivo original. La declaración `:- dynamic` es necesaria para que Prolog permita esta operación.

---

## 7. Backend — API REST

### Archivo: `backend/api/routes.py`

Todos los endpoints están bajo el prefijo `/api`.

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/ciudades` | Lista todas las ciudades disponibles |
| `POST` | `/api/rutas` | Todas las rutas entre dos ciudades (ordenadas) |
| `POST` | `/api/ruta-corta` | Solo la ruta más corta |
| `GET` | `/api/sesion` | Ciudades pendientes en la sesión actual |
| `POST` | `/api/ciudades/nueva` | Agrega una ciudad a la sesión |
| `POST` | `/api/ciudades/confirmar` | Confirma la sesión y genera `rutas_extended.pl` |
| `DELETE` | `/api/ciudades/sesion` | Descarta la sesión sin guardar |

#### Ejemplo de petición y respuesta — `/api/rutas`

**Petición:**
```json
{
  "origen": "guatemala",
  "destino": "flores"
}
```

**Respuesta:**
```json
{
  "origen": "guatemala",
  "destino": "flores",
  "rutas": [
    { "camino": ["guatemala", "coban", "flores"], "distancia": 575 },
    { "camino": ["guatemala", "zacapa", "chiquimula", "coban", "flores"], "distancia": 739 }
  ],
  "estadisticas": {
    "total_rutas": 18,
    "distancia_minima": 575,
    "distancia_maxima": 1600,
    "distancia_promedio": 1117.94
  }
}
```

---

## 8. Frontend

El frontend es una aplicación de una sola página (SPA) implementada con HTML, CSS y JavaScript puro, sin frameworks. FastAPI la sirve como archivos estáticos bajo la ruta `/app`.

### Comunicación con la API

Todas las peticiones usan la `Fetch API` del navegador:

```javascript
const res = await fetch(`${API}/rutas`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ origen, destino })
});
```

### Formato de nombres

Los nombres de ciudades se almacenan en Prolog con guión bajo (`puerto_barrios`). El frontend los convierte a formato legible al mostrarlos:

```javascript
function formatearNombre(nombre) {
  return nombre.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}
// "puerto_barrios" → "Puerto Barrios"
```

---

## 9. Flujo completo de una consulta

El siguiente diagrama muestra el recorrido de una petición desde el usuario hasta Prolog y de vuelta:

```
Usuario selecciona ciudades y hace clic en "Buscar Rutas"
        │
        ▼
app.js llama fetch() a POST /api/rutas
        │
        ▼
routes.py recibe la petición HTTP
Valida que el body tenga origen y destino
        │
        ▼
route_service.py normaliza los nombres (minúsculas, guión bajo)
Llama ciudad_valida() para cada ciudad
Llama hay_ruta() para verificar que existe conexión
        │
        ▼
prolog_engine.py adquiere el lock de hilo
Ejecuta query: ruta(guatemala, flores, Camino, Distancia)
PySwip comunica la consulta a SWI-Prolog
        │
        ▼
SWI-Prolog ejecuta ruta_aux/5 recursivamente
Encuentra todos los caminos sin ciclos
Devuelve resultados a PySwip
        │
        ▼
prolog_engine.py libera el lock
Convierte los resultados a listas Python
        │
        ▼
route_service.py ordena las rutas y calcula estadísticas
        │
        ▼
routes.py devuelve respuesta JSON con HTTP 200
        │
        ▼
app.js renderiza ruta más corta, estadísticas y lista de rutas
Usuario ve los resultados en pantalla
```

---

## 10. Seguridad y concurrencia

### Thread safety en PySwip

PySwip accede a un intérprete Prolog global que **no es thread-safe**. FastAPI puede procesar múltiples peticiones concurrentemente, lo que causaría que dos consultas Prolog se ejecuten simultáneamente y corrompan el estado del intérprete.

**Solución implementada:** un `threading.Lock` global en `prolog_engine.py` que serializa el acceso al intérprete:

```python
_prolog_lock = threading.Lock()

def ciudad_valida(self, ciudad: str) -> bool:
    with _prolog_lock:
        return bool(list(self._prolog.query(f"ciudad_valida({ciudad})")))
```

Cada método que accede a Prolog adquiere el lock antes de ejecutar la consulta y lo libera automáticamente al terminar.

---

## 11. Posibles mejoras futuras

| Mejora | Descripción |
|---|---|
| **Visualización de grafo** | Mostrar las ciudades y conexiones como un grafo visual interactivo usando una librería como D3.js |
| **Eliminación de ciudades** | Permitir al usuario eliminar ciudades agregadas desde el panel de gestión |
| **Filtro por distancia máxima** | Que el usuario pueda limitar los resultados a rutas menores a N kilómetros |
| **Exportar resultados** | Botón para descargar las rutas encontradas en formato CSV o PDF |
| **Autenticación** | Proteger el endpoint de modificación de ciudades con usuario y contraseña |
| **Persistencia mejorada** | Manejar múltiples archivos extendidos con historial de versiones |
| **Pruebas automatizadas** | Implementar suite de pruebas con `pytest` para los servicios y la integración Prolog |
| **Mapa geográfico** | Integrar un mapa real de Guatemala donde se visualicen las rutas sobre el territorio |
