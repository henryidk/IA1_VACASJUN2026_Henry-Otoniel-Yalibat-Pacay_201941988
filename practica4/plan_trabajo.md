# Plan de Trabajo — RoboMaze (Práctica 4)

**Fecha de entrega:** 24/06/2026
**Total de commits planificados:** 28
**Alcance:** Los requerimientos obligatorios del documento, más dos opcionales que el usuario pidió incluir explícitamente: **generación automática de laberintos** (botón de laberinto aleatorio) y **modificar el tamaño del laberinto**. El resto de los opcionales (A*, guardar/cargar laberintos, múltiples metas, obstáculos dinámicos, exportar a CSV/PDF, etc.) quedan fuera de alcance por el plazo disponible.

> **Sobre los "5 laberintos":** el documento lo menciona dos veces con matices distintos: el objetivo SMART pide "resolver al menos 5 laberintos diferentes" (cumplido por el generador aleatorio), y los Requisitos mínimos del sistema piden explícitamente "incluir al menos 5 laberintos predefinidos para realizar pruebas de funcionamiento". Para cubrir ambas lecturas sin ambigüedad, el sistema incluye **las dos cosas**: 5 laberintos predefinidos versionados como JSON en `backend/data/mazes/` (servidos vía `GET /api/mazes`), más el generador aleatorio bajo demanda (`POST /api/mazes/random`). No son mutuamente excluyentes — el usuario elige cuál usar desde la misma interfaz.

> **Nota sobre el cronograma de commits:** el documento exige un historial real, sin "commits masivos el mismo día". Con un plazo de 3 días (22, 23 y 24 de junio) no es posible espaciar cada commit en días distintos, pero sí podemos asegurar que cada commit sea pequeño, funcional y verificable por separado (no un volcado final del proyecto completo), distribuidos en bloques de trabajo a lo largo de esos 3 días. Eso es lo que un avance progresivo real se vería en un plazo corto.

---

## Stack tecnológico

| Capa | Tecnología | Motivo |
|---|---|---|
| Backend / API REST | Python 3.13 + FastAPI + Uvicorn | Cumple la restricción de backend 100% Python, documentación Swagger automática útil como evidencia, fácil de levantar con un entorno virtual |
| Algoritmos de búsqueda | Python puro (sin librerías de pathfinding) | Restricción explícita del documento: BFS y DFS deben ser implementados por el estudiante |
| Laberintos predefinidos | 5 archivos JSON estáticos en `backend/data/mazes/` (variando tamaño/dificultad), cargados por `MazeRepository` | Cumple literalmente el requisito mínimo "incluir al menos 5 laberintos predefinidos"; generados una sola vez con semilla fija y versionados en el repo, no en una base de datos |
| Generación de laberintos aleatorios | Algoritmo propio de carving tipo *recursive backtracker* (basado en una pila, la misma idea que DFS), expuesto bajo demanda en `MazeGenerator` | Cumple el opcional de generación automática y permite tamaño configurable, sin depender de librerías externas de pathfinding/maze-generation |
| Frontend | HTML + CSS + JavaScript (vanilla), servido como archivos estáticos por el propio FastAPI | Un solo proceso para levantar todo el sistema (sin servidor aparte), consistente con la restricción de que el frontend solo se encargue de interacción/visualización |
| Entorno de ejecución | `venv` de Python (sin Docker) | Ya tenemos Python 3.13, `pip` y `venv` instalados localmente y el proyecto no requiere herramientas de sistema externas (no hay OCR/Selenium como en la práctica 3), así que Docker solo añadiría pasos innecesarios |
| Control de versiones | Git + GitHub (mismo repo del curso) | Exigido por el documento |

---

## Arquitectura del sistema

Patrón de arquitectura: **arquitectura en capas (Layered Architecture)** combinada con el **patrón de diseño Strategy** para los algoritmos de búsqueda (BFS y DFS son estrategias intercambiables detrás de una misma interfaz, seleccionadas en tiempo de ejecución según lo que pida el frontend).

```
┌─────────────────────────────────────────────────────────────┐
│                        Navegador (frontend)                  │
│   HTML + CSS + JS vanilla — dibuja la cuadrícula, captura     │
│   clics (inicio/meta/obstáculos), pide /api/search           │
└───────────────────────────┬───────────────────────────────────┘
                            │ HTTP (fetch)
┌───────────────────────────▼───────────────────────────────────┐
│                     Capa API (FastAPI routers)                │
│   /api/mazes  /api/mazes/{id}  /api/mazes/random              │
│   /api/search  /api/search/compare                             │
│   Valida la entrada (Pydantic), traduce HTTP <-> dominio       │
└───────────────────────────┬───────────────────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────┐
│                   Capa de Servicio (MazeService)               │
│   Orquesta: carga/genera el laberinto, elige la estrategia de  │
│   búsqueda, mide tiempo y nodos explorados, reconstruye ruta,  │
│   maneja el caso "sin ruta válida"                             │
└──────────────┬───────────────────┬────────────────────┬───────┘
               │                   │                    │
┌──────────────▼───────────┐ ┌─────▼────────────┐ ┌─────▼──────────────────┐
│ Dominio: Maze (grilla,    │ │ Algoritmos        │ │ MazeGenerator /         │
│ obstáculos, inicio, meta, │ │ (Strategy pattern)│ │ MazeRepository          │
│ tamaño configurable)      │ │ SearchStrategy     │ │ (genera aleatorio o lee│
│                            │ │ ├─ BFSStrategy     │ │ los 5 predefinidos)     │
│                            │ │ └─ DFSStrategy     │ │                         │
└────────────────────────────┘ └────────────────────┘ └──────────┬──────────────┘
                                                                  │
                                                    ┌─────────────▼─────────────┐
                                                    │  data/mazes/*.json         │
                                                    │  (5 laberintos predefinidos)│
                                                    └────────────────────────────┘
```

### Decisiones de arquitectura

- **Strategy pattern para BFS/DFS**: ambos algoritmos implementan la misma interfaz (`buscar(maze) -> ResultadoBusqueda`), lo que permite que la capa de servicio los intercambie sin condicionales `if algoritmo == "bfs"` dispersos por el código, y deja la puerta abierta a A* como estrategia opcional futura sin tocar lo ya hecho.
- **Sin base de datos**: los 5 laberintos predefinidos viven como archivos JSON versionados en el propio repositorio (`backend/data/mazes/`), generados una sola vez con semilla fija mediante un script (`scripts/generate_predefined_mazes.py`) y leídos en cada petición por `MazeRepository`. Un laberinto generado por el botón "aleatorio" nunca se persiste: se devuelve directo en la respuesta HTTP y vive solo en memoria del navegador. El estado de una búsqueda (ruta, nodos explorados, tiempo) tampoco se guarda — vive únicamente en la respuesta de esa petición.
- **MazeRepository independiente de MazeGenerator**: ambos viven junto al dominio pero no se conocen entre sí — uno lee archivos estáticos, el otro genera laberintos nuevos. La capa API los expone en rutas distintas (`GET /api/mazes`/`GET /api/mazes/{id}` vs `POST /api/mazes/random`) y el frontend decide cuál usar sin que el backend necesite saberlo.
- **Un solo proceso (FastAPI sirve también el frontend)**: se monta `frontend/` como archivos estáticos dentro de la misma app de FastAPI (`StaticFiles`), así que con `uvicorn` corriendo ya se puede abrir el navegador y usar el sistema completo, sin levantar un segundo servidor.
- **Lógica de búsqueda 100% en el backend**: el frontend solo dibuja la cuadrícula y la ruta que el backend ya calculó; nunca decide por sí mismo qué celda visitar, cumpliendo la restricción de que la exploración ocurra en el servidor.
- **Manejo explícito de "sin ruta"**: si BFS o DFS agotan la exploración sin alcanzar la meta, el servicio devuelve un resultado con `ruta: null` y un mensaje claro, en vez de lanzar una excepción genérica — el frontend lo muestra como un estado distinto (no como un error de red).
- **MazeGenerator como pieza independiente del dominio**: solo recibe `ancho`/`alto` (límites 5×5 a 30×30) y devuelve un `Maze` válido con inicio, meta y muros garantizando conectividad. No sabe nada de BFS/DFS ni de la capa de servicio.

---

## Paleta de colores y dirección visual

Paleta elegida: **verdes salvia** — `#778873` (verde oscuro), `#A1BC98` (verde claro), `#DCCFC0` (beige cálido), `#FDF6ED` (crema). Da una sensación de "jardín/bosque" coherente con un laberinto, y se aleja del estilo lila/azulado genérico que se asocia con interfaces hechas por IA.

Uso propuesto (evitando introducir colores fuera de la paleta; las variaciones de estado se logran con tintes/sombras de los mismos 4 tonos):

| Elemento | Color base | Variante |
|---|---|---|
| Fondo general | `#FDF6ED` | — |
| Paneles, tarjetas, header | `#DCCFC0` | borde en `#778873` a 30% opacidad |
| Celda vacía / camino transitable | `#FDF6ED` con borde `#DCCFC0` | — |
| Muro / obstáculo | `#778873` | sombra interna más oscura (`filter: brightness(0.85)`) |
| Celda explorada (animación BFS/DFS) | `#A1BC98` | con transición de opacidad para el efecto de "barrido" |
| Ruta final encontrada | `#778873` | con un patrón de puntos/línea en `#FDF6ED` encima, no un color nuevo |
| Inicio | `#A1BC98` | ícono/glifo en `#778873` (no un color nuevo, se distingue por forma) |
| Meta | `#DCCFC0` | ícono/glifo en `#778873` (se distingue por forma, no por color ajeno a la paleta) |
| Texto principal | `#778873` sobre `#FDF6ED` | — |

Para que no se note el uso de IA: tipografía con personalidad (no la típica `Inter`/`system-ui` por defecto — usar algo tipo *rounded/playful* vía Google Fonts), sin gradientes morados ni sombras "glassmorphism" genéricas, botones con bordes gruesos y esquinas redondeadas tipo juego de mesa, y la cuadrícula con un leve borde tipo "tablero" en vez de un grid plano de CSS por defecto.

---

## Estructura de carpetas

```
practica4/
├── practica4.md                 (documento de la práctica, ya existe)
├── plan_trabajo.md              (este documento)
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py                       # app factory, monta frontend estático y routers
│   │   ├── core/config.py
│   │   ├── domain/
│   │   │   ├── maze.py                   # entidad Maze: grilla, inicio, meta, obstáculos, tamaño
│   │   │   ├── maze_generator.py         # generador aleatorio (recursive backtracker), tamaño configurable
│   │   │   ├── maze_repository.py        # carga los 5 laberintos predefinidos desde data/mazes/*.json
│   │   │   └── search_strategy.py        # interfaz SearchStrategy (Strategy pattern)
│   │   ├── algorithms/
│   │   │   ├── bfs.py
│   │   │   └── dfs.py
│   │   ├── services/maze_service.py       # orquestación, métricas, caso sin ruta
│   │   ├── schemas/maze_schemas.py        # Pydantic request/response
│   │   └── api/routes/
│   │       ├── mazes.py                  # GET /api/mazes, GET /api/mazes/{id}, POST /api/mazes/random
│   │       └── search.py                 # POST /api/search, POST /api/search/compare
│   ├── data/mazes/                       # 5 laberintos predefinidos (.json), generados con semilla fija
│   └── scripts/generate_predefined_mazes.py  # script de un solo uso que produjo esos 5 archivos
├── frontend/
│   ├── index.html
│   ├── css/styles.css
│   └── js/
│       ├── api.js
│       ├── grid.js
│       └── app.js
└── docs/
    ├── MANUAL_TECNICO.md
    ├── MANUAL_USUARIO.md
    └── diagrama_arquitectura.png
```

---

## Grupo 1 — Configuración inicial del proyecto

| # | Commit | Qué incluye |
|---|--------|-------------|
| 1.1 | `chore: inicializar estructura del proyecto RoboMaze y README` | Carpetas `backend/`, `frontend/`, `docs/`, `.gitignore`, `README.md` esqueleto |
| 1.2 | `chore: configurar entorno virtual y dependencias del backend` | `requirements.txt` (fastapi, uvicorn, pydantic), instrucciones de `venv` en el README |

## Grupo 2 — Dominio: representación del laberinto

| # | Commit | Qué incluye |
|---|--------|-------------|
| 2.1 | `feat(domain): modelar el laberinto como cuadrícula con obstáculos, inicio y meta` | Clase `Maze`, validaciones (coordenadas dentro de rango, inicio/meta no son muro) |
| 2.2 | `feat(domain): implementar MazeGenerator aleatorio con tamaño configurable` | Algoritmo *recursive backtracker* basado en pila, garantiza conectividad entre inicio y meta por construcción; límites 5×5 a 30×30 |
| 2.3 | `feat(data): agregar 5 laberintos predefinidos en formato JSON` | `scripts/generate_predefined_mazes.py` (semilla fija por laberinto) + 5 archivos en `data/mazes/`, variando tamaño (13×13 a 37×37) y dificultad (fácil a experto) |

## Grupo 3 — API REST de laberintos

| # | Commit | Qué incluye |
|---|--------|-------------|
| 3.1 | `feat(api): agregar endpoints para listar y obtener laberintos predefinidos` | `MazeRepository` + `GET /api/mazes` (metadatos) y `GET /api/mazes/{id}` (laberinto completo), con 404 si el id no existe |
| 3.2 | `feat(api): agregar endpoint para generar un laberinto aleatorio` | `POST /api/mazes/random` recibe `ancho`/`alto`, devuelve el laberinto generado sin persistirlo |

## Grupo 4 — Algoritmos de búsqueda

| # | Commit | Qué incluye |
|---|--------|-------------|
| 4.1 | `feat(algorithms): definir interfaz SearchStrategy para los algoritmos de búsqueda` | Patrón Strategy: contrato común de entrada/salida para BFS y DFS |
| 4.2 | `feat(algorithms): implementar BFS con conteo de nodos explorados` | Cola FIFO, reconstrucción de ruta vía padres, conteo de nodos visitados |
| 4.3 | `feat(algorithms): implementar DFS con conteo de nodos explorados` | Pila/recursión controlada, mismo contrato de salida que BFS |

## Grupo 5 — Capa de servicio

| # | Commit | Qué incluye |
|---|--------|-------------|
| 5.1 | `feat(services): orquestar ejecución de algoritmos y medir tiempo de ejecución` | `MazeService.buscar(maze, algoritmo)`, cronometraje con `time.perf_counter` |
| 5.2 | `feat(services): manejar el caso sin ruta válida entre origen y destino` | Resultado explícito `ruta=null` + mensaje, sin excepciones genéricas |

## Grupo 6 — API REST de búsqueda

| # | Commit | Qué incluye |
|---|--------|-------------|
| 6.1 | `feat(api): agregar endpoint de búsqueda con selección de algoritmo` | `POST /api/search` recibe la grilla completa + inicio + meta + algoritmo BFS/DFS, devuelve ruta, nodos explorados y tiempo |
| 6.2 | `feat(api): agregar endpoint de comparación BFS vs DFS en una sola llamada` | `POST /api/search/compare`, ejecuta ambos algoritmos sobre el mismo laberinto y devuelve métricas de los dos |

## Grupo 7 — Frontend: base visual

| # | Commit | Qué incluye |
|---|--------|-------------|
| 7.1 | `feat(frontend): agregar estructura HTML, paleta de colores y estilos base` | Layout general, tipografía, variables CSS con la paleta verde salvia |
| 7.2 | `feat(frontend): renderizar la cuadrícula del laberinto recibida de la API` | Dibujo de celdas/muros/inicio/meta a partir de la respuesta de la API |

## Grupo 8 — Frontend: laberinto dinámico (predefinidos, tamaño y generación aleatoria)

| # | Commit | Qué incluye |
|---|--------|-------------|
| 8.1 | `feat(frontend): agregar selector de laberinto predefinido` | `<select>` poblado vía `GET /api/mazes`, botón "Cargar Laberinto" que pide el detalle con `GET /api/mazes/{id}` y reemplaza la cuadrícula activa |
| 8.2 | `feat(frontend): agregar control de tamaño del laberinto` | Inputs de ancho/alto con límites válidos (5–30), persisten como el tamaño a usar al generar |
| 8.3 | `feat(frontend): agregar botón para generar un laberinto aleatorio` | Llama a `POST /api/mazes/random` con el tamaño elegido y reemplaza la cuadrícula activa en pantalla |

## Grupo 9 — Frontend: edición manual del laberinto

| # | Commit | Qué incluye |
|---|--------|-------------|
| 9.1 | `feat(frontend): permitir definir inicio, meta y obstáculos por clic` | Modo de edición sobre la cuadrícula generada, validación en cliente antes de enviar |

## Grupo 10 — Frontend: selección de algoritmo, ejecución y resultados

| # | Commit | Qué incluye |
|---|--------|-------------|
| 10.1 | `feat(frontend): agregar selector de algoritmo y ejecutarlo de forma independiente con animación` | Control explícito BFS/DFS + botón "Ejecutar", animación celda por celda sobre el orden de exploración devuelto por la API |
| 10.2 | `feat(frontend): mostrar ruta final, nodos explorados y tiempo de ejecución` | Panel de resultados por algoritmo |
| 10.3 | `feat(frontend): agregar vista de comparación lado a lado entre BFS y DFS` | Usa `/api/search/compare`, tabla/gráfico comparativo de métricas |

## Grupo 11 — Manejo de errores y pulido

| # | Commit | Qué incluye |
|---|--------|-------------|
| 11.1 | `fix(frontend): manejar en la interfaz el caso sin ruta válida y estados de carga` | Mensaje claro de "sin ruta", spinners/estados durante la llamada a la API |
| 11.2 | `style(frontend): pulir animaciones, tablero y responsividad` | Detalles tipo "juego de mesa", ajuste en distintos tamaños de pantalla y de laberinto |

## Grupo 12 — Documentación y evidencias

| # | Commit | Qué incluye |
|---|--------|-------------|
| 12.1 | `docs: agregar manual técnico con arquitectura, patrón Strategy y API REST` | Diagrama de arquitectura, descripción de capas, endpoints, requerimientos funcionales/no funcionales |
| 12.2 | `docs: agregar manual de usuario con instalación, ejecución y capturas de pantalla` | Pasos de `venv`, cómo correr `uvicorn`, capturas de 5 laberintos aleatorios distintos con BFS, DFS y comparación |
| 12.3 | `docs: actualizar README con instrucciones rápidas y enlaces a los manuales` | README final apuntando a `docs/MANUAL_TECNICO.md` y `docs/MANUAL_USUARIO.md` |

---

## Resumen general

| Grupo | Commits | Enfoque |
|-------|---------|---------|
| 1. Setup inicial | 2 | Estructura y entorno |
| 2. Dominio del laberinto | 3 | Modelo Maze + MazeGenerator aleatorio + 5 laberintos predefinidos (JSON) |
| 3. API de laberintos | 2 | Listar/obtener predefinidos + `POST /api/mazes/random` |
| 4. Algoritmos de búsqueda | 3 | BFS y DFS propios (Strategy) |
| 5. Capa de servicio | 2 | Orquestación, métricas, sin ruta |
| 6. API REST de búsqueda | 2 | `POST /api/search` y `POST /api/search/compare` |
| 7. Frontend base | 2 | Paleta, layout, render de la grilla |
| 8. Frontend laberinto dinámico | 3 | Selector de predefinido + control de tamaño + botón aleatorio |
| 9. Frontend edición manual | 1 | Inicio/meta/obstáculos por clic |
| 10. Frontend resultados | 3 | Selector de algoritmo, animación, métricas, comparación |
| 11. Errores y pulido | 2 | UX de error y estética final |
| 12. Documentación | 3 | Manual técnico, manual de usuario, README |
| **Total** | **28** | |
