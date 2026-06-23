/**
 * Aplicación Principal (app.js)
 * Conecta la UI, el cliente API y el renderizador del laberinto.
 */

import { ApiClient } from './api.js';
import { MazeRenderer } from './MazeRenderer.js';

// --- Estado Global ---
const state = {
    maze: null,       // { grid, start, goal, rows, cols }
    isGenerating: false
};

// --- Referencias al DOM ---
const refs = {
    canvas: document.getElementById('maze-canvas'),
    btnGenerate: document.getElementById('btn-generate'),
    inputCols: document.getElementById('input-cols'),
    inputRows: document.getElementById('input-rows'),
    btnSearchBfs: document.getElementById('btn-search-bfs'),
    btnSearchDfs: document.getElementById('btn-search-dfs'),
    btnCompare: document.getElementById('btn-compare'),
    resultsContainer: document.getElementById('results-container')
};

// --- Inicialización ---
const renderer = new MazeRenderer(refs.canvas);

// --- Funciones de Utilidad ---

/**
 * Actualiza el estado visual de los botones según si hay un laberinto cargado
 * y si hay una operación en curso.
 */
function updateUIState() {
    // Si estamos generando, bloqueamos todo
    if (state.isGenerating) {
        refs.btnGenerate.disabled = true;
        refs.inputCols.disabled = true;
        refs.inputRows.disabled = true;
        refs.btnSearchBfs.disabled = true;
        refs.btnSearchDfs.disabled = true;
        refs.btnCompare.disabled = true;
        return;
    }

    // Si no estamos generando, restauramos controles de generación
    refs.btnGenerate.disabled = false;
    refs.inputCols.disabled = false;
    refs.inputRows.disabled = false;

    // Los botones de búsqueda dependen de si existe un laberinto
    const hasMaze = state.maze !== null;
    refs.btnSearchBfs.disabled = !hasMaze;
    refs.btnSearchDfs.disabled = !hasMaze;
    refs.btnCompare.disabled = !hasMaze;
}

/**
 * Muestra un mensaje en el contenedor de resultados.
 */
function showStatusMessage(html, isError = false) {
    refs.resultsContainer.innerHTML = html;
    if (isError) {
        refs.resultsContainer.style.borderColor = 'rgba(239, 68, 68, 0.4)';
    } else {
        refs.resultsContainer.style.borderColor = 'var(--glass-border)';
    }
}

// --- Event Handlers ---

/**
 * Evento: Clic en Generar Laberinto
 */
async function handleGenerate() {
    const cols = parseInt(refs.inputCols.value, 10);
    const rows = parseInt(refs.inputRows.value, 10);

    // Validación básica de UI
    if (isNaN(cols) || cols < 5 || cols > 30 || isNaN(rows) || rows < 5 || rows > 30) {
        showStatusMessage('<div class="empty-state" style="color: #f87171;">Por favor ingresa dimensiones entre 5 y 30.</div>', true);
        return;
    }

    // Actualizar estado a "cargando"
    state.isGenerating = true;
    refs.btnGenerate.classList.add('loading');
    showStatusMessage('<div class="empty-state">Generando laberinto perfecto...</div>');
    updateUIState();

    try {
        // Llamada a la API
        const mazeData = await ApiClient.generateMaze(cols, rows);
        
        // Guardar en estado y renderizar
        state.maze = mazeData;
        renderer.loadMaze(mazeData);
        
        showStatusMessage(`<div class="empty-state">Laberinto de ${cols}x${rows} celdas (Grid real: ${mazeData.cols}x${mazeData.rows}) generado. Listo para buscar.</div>`);
    } catch (error) {
        showStatusMessage(`<div class="empty-state" style="color: #f87171;">Error: ${error.message}</div>`, true);
        state.maze = null; // Resetear en caso de error
    } finally {
        state.isGenerating = false;
        refs.btnGenerate.classList.remove('loading');
        updateUIState();
    }
}

// --- Asignación de Eventos ---
refs.btnGenerate.addEventListener('click', handleGenerate);

// (Los listeners de búsqueda se implementarán en el Grupo 10)

// Inicializar UI
updateUIState();
