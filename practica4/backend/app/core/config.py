"""
Configuración general de la aplicación RoboMaze.
"""

# Límites del laberinto (en número de celdas por lado)
MAZE_MIN_SIZE: int = 5
MAZE_MAX_SIZE: int = 30

# Tamaño por defecto al generar un laberinto aleatorio
MAZE_DEFAULT_WIDTH: int = 15
MAZE_DEFAULT_HEIGHT: int = 15

# Título y versión de la API
API_TITLE: str = "RoboMaze API"
API_VERSION: str = "1.0.0"
API_DESCRIPTION: str = (
    "API REST para la generación de laberintos y la ejecución de algoritmos "
    "de búsqueda BFS y DFS."
)
