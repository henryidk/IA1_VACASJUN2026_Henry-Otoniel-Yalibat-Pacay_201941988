# RoboMaze

Sistema de navegación en laberintos utilizando algoritmos de búsqueda en inteligencia artificial (BFS y DFS).

## Descripción

RoboMaze es una aplicación web que permite generar laberintos virtuales y resolverlos mediante algoritmos de búsqueda clásicos. El sistema visualiza el recorrido encontrado, la cantidad de nodos explorados y el tiempo de ejecución de cada algoritmo, permitiendo comparar BFS y DFS sobre el mismo laberinto.

## Tecnologías

| Capa | Tecnología |
|------|------------|
| Backend / API REST | Python 3.13 + FastAPI + Uvicorn |
| Algoritmos | Python puro (BFS y DFS implementados desde cero) |
| Frontend | HTML + CSS + JavaScript vanilla |

## Estructura del proyecto

```
practica4/
├── README.md
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── core/config.py
│       ├── domain/
│       │   ├── maze.py
│       │   ├── maze_generator.py
│       │   └── search_strategy.py
│       ├── algorithms/
│       │   ├── bfs.py
│       │   └── dfs.py
│       ├── services/maze_service.py
│       ├── schemas/maze_schemas.py
│       └── api/routes/
│           ├── mazes.py
│           └── search.py
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

## Instalación y ejecución

> Las instrucciones completas se encuentran en [`docs/MANUAL_USUARIO.md`](docs/MANUAL_USUARIO.md).

### Requisitos previos

- Python 3.11 o superior
- Git

### Pasos rápidos

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd practica4

# 2. Crear y activar el entorno virtual
cd backend
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Levantar el servidor
uvicorn app.main:app --reload

# 5. Abrir en el navegador
# http://localhost:8000
```

## Documentación

- [Manual Técnico](docs/MANUAL_TECNICO.md) — Arquitectura, algoritmos, API REST y decisiones de diseño.
- [Manual de Usuario](docs/MANUAL_USUARIO.md) — Instalación, ejecución y guía de uso con capturas de pantalla.

## Algoritmos implementados

- **BFS (Breadth-First Search):** garantiza encontrar el camino más corto en grafos no ponderados.
- **DFS (Depth-First Search):** explora en profundidad, generalmente más rápido pero sin garantía de camino mínimo.

## Autor

Henry Otoniel Yalibat Pacay — 201941988  
Curso: Inteligencia Artificial 1 — Vacaciones Junio 2026
