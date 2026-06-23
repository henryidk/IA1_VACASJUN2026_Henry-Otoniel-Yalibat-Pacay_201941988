/**
 * API Client para RoboMaze
 * Maneja todas las llamadas a la API de FastAPI.
 */

const API_BASE_URL = '/api';

export const ApiClient = {
    /**
     * Lista los laberintos predefinidos disponibles (metadatos, sin grid).
     * @returns {Promise<Array<Object>>} Lista de { id, nombre, dificultad, rows, cols }.
     */
    async listMazes() {
        try {
            const response = await fetch(`${API_BASE_URL}/mazes`);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al listar laberintos predefinidos');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error - listMazes:', error);
            throw error;
        }
    },

    /**
     * Obtiene un laberinto predefinido completo por su id.
     * @param {string} id Id del laberinto predefinido.
     * @returns {Promise<Object>} Datos del laberinto (grid, start, goal).
     */
    async getMaze(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/mazes/${id}`);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al obtener el laberinto');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error - getMaze:', error);
            throw error;
        }
    },

    /**
     * Genera un laberinto aleatorio.
     * @param {number} cols Número de columnas lógicas.
     * @param {number} rows Número de filas lógicas.
     * @returns {Promise<Object>} Datos del laberinto (grid, start, goal).
     */
    async generateMaze(cols, rows) {
        try {
            const response = await fetch(`${API_BASE_URL}/mazes/random`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cols, rows }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al generar el laberinto');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error - generateMaze:', error);
            throw error;
        }
    },

    /**
     * Ejecuta una búsqueda (BFS o DFS) en un laberinto.
     * @param {Array<Array<number>>} grid Cuadrícula del laberinto.
     * @param {Object} start Posición {row, col}.
     * @param {Object} goal Posición {row, col}.
     * @param {string} algoritmo 'BFS' o 'DFS'.
     * @returns {Promise<Object>} Resultados de la búsqueda.
     */
    async search(grid, start, goal, algoritmo) {
        try {
            const response = await fetch(`${API_BASE_URL}/search/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ grid, start, goal, algoritmo }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Error en búsqueda ${algoritmo}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error - search ${algoritmo}:`, error);
            throw error;
        }
    },

    /**
     * Ejecuta una comparación entre BFS y DFS en un laberinto.
     * @param {Array<Array<number>>} grid Cuadrícula del laberinto.
     * @param {Object} start Posición {row, col}.
     * @param {Object} goal Posición {row, col}.
     * @returns {Promise<Object>} Resultados de la comparación {bfs, dfs}.
     */
    async compare(grid, start, goal) {
        try {
            const response = await fetch(`${API_BASE_URL}/search/compare`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ grid, start, goal }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error en comparación');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error - compare:', error);
            throw error;
        }
    }
};
