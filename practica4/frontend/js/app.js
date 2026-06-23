/**
 * Aplicación Principal (app.js)
 * Conecta la UI, el cliente API y el renderizador del laberinto.
 */

import { ApiClient } from './api.js';
import { MazeRenderer } from './MazeRenderer.js';

// --- Estado Global ---
const state = {
    maze: null,       // { grid, start, goal, rows, cols }
    isGenerating: false,
    activeTool: 'wall', // 'wall', 'start', 'goal'
    isDragging: false,
    dragValue: null     // 1 para poner muro, 0 para quitar muro al arrastrar
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
    resultsContainer: document.getElementById('results-container'),
    toolBtns: document.querySelectorAll('.tool-btn')
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

// Herramientas de edición manual
refs.toolBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Actualizar UI de botones
        refs.toolBtns.forEach(b => b.classList.remove('active'));
        const targetBtn = e.currentTarget;
        targetBtn.classList.add('active');
        
        // Actualizar estado
        state.activeTool = targetBtn.dataset.tool;
    });
});

// Eventos del Canvas para edición manual
function getCanvasCoords(e) {
    const rect = refs.canvas.getBoundingClientRect();
    // Ajustar por si el canvas está escalado con CSS
    const scaleX = refs.canvas.width / rect.width;
    const scaleY = refs.canvas.height / rect.height;
    
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;
    
    const col = Math.floor(x / renderer.cellSize);
    const row = Math.floor(y / renderer.cellSize);
    return { row, col };
}

function isValidCoord(row, col) {
    if (!state.maze) return false;
    return row >= 0 && row < state.maze.rows && col >= 0 && col < state.maze.cols;
}

function applyEdit(row, col, isDrag = false) {
    if (!isValidCoord(row, col)) return;
    
    const { maze, activeTool } = state;
    let changed = false;

    // Si la celda es el inicio o meta actuales y estamos usando la herramienta de muro,
    // o al revés, hay que tener cuidado. Por simplicidad, el backend validará si pisamos algo inválido,
    // pero aquí permitimos sobreescribir.

    if (activeTool === 'wall') {
        // Evitar pisar inicio o meta
        if ((maze.start.row === row && maze.start.col === col) || 
            (maze.goal.row === row && maze.goal.col === col)) {
            return;
        }

        if (!isDrag) {
            // En clic individual, invertimos el estado
            state.dragValue = maze.grid[row][col] === 1 ? 0 : 1;
        }
        
        if (maze.grid[row][col] !== state.dragValue) {
            maze.grid[row][col] = state.dragValue;
            changed = true;
        }
    } else if (activeTool === 'start' && !isDrag) {
        maze.grid[row][col] = 0;
        maze.start = { row, col };
        renderer.setStart(row, col); // El renderer actualiza su estado y redibuja
        showStatusMessage('<div class="empty-state">Inicio movido. Ejecuta una búsqueda.</div>');
        return; // setStart ya llama a draw(), no necesitamos continuar
    } else if (activeTool === 'goal' && !isDrag) {
        maze.grid[row][col] = 0;
        maze.goal = { row, col };
        renderer.setGoal(row, col); // El renderer actualiza su estado y redibuja
        showStatusMessage('<div class="empty-state">Meta movida. Ejecuta una búsqueda.</div>');
        return; // setGoal ya llama a draw(), no necesitamos continuar
    }

    if (changed) {
        renderer.clearSearch(); // Borrar ruta anterior al editar
        renderer.draw();
        // Borrar mensaje de resultados anterior si editamos
        showStatusMessage('<div class="empty-state">Laberinto editado. Ejecuta una búsqueda.</div>');
    }
}

refs.canvas.addEventListener('mousedown', (e) => {
    if (!state.maze) return;
    state.isDragging = true;
    const { row, col } = getCanvasCoords(e);
    applyEdit(row, col, false);
});

refs.canvas.addEventListener('mousemove', (e) => {
    if (!state.isDragging || !state.maze) return;
    const { row, col } = getCanvasCoords(e);
    applyEdit(row, col, true);
});

window.addEventListener('mouseup', () => {
    state.isDragging = false;
});

// --- Ejecución y Animación de Búsqueda ---

/**
 * Anima la exploración y la ruta resultante
 */
function animateSearch(result, onComplete) {
    const { explorados, ruta } = result;
    
    // Si no hay nodos explorados o ruta (ej. sin camino y 1 nodo), dibujamos directo
    if (!explorados || explorados.length === 0) {
        renderer.setSearchResult(explorados, ruta);
        if (onComplete) onComplete();
        return;
    }

    // Calcular cuántos nodos dibujar por frame para que la animación dure ~1 segundo
    const framesTarget = 60; 
    const nodesPerFrame = Math.max(1, Math.floor(explorados.length / framesTarget));
    
    let currentIndex = 0;

    function frame() {
        currentIndex += nodesPerFrame;
        
        if (currentIndex < explorados.length) {
            // Dibujar progreso parcial
            renderer.setSearchResult(explorados.slice(0, currentIndex), []);
            requestAnimationFrame(frame);
        } else {
            // Finalizar animación dibujando la ruta definitiva
            renderer.setSearchResult(explorados, ruta);
            if (onComplete) onComplete();
        }
    }

    requestAnimationFrame(frame);
}

/**
 * Renderiza el HTML de un resultado individual
 */
function buildResultHTML(result) {
    const badgeClass = result.encontrado ? '' : ' error';
    const statusText = result.encontrado ? 'Éxito' : 'Sin Ruta';
    
    return `
        <div class="result-card">
            <div class="result-title">
                ${result.algoritmo}
                <span class="result-badge${badgeClass}">${statusText}</span>
            </div>
            <div class="result-metric">
                <span>Ruta:</span>
                <span class="result-value">${result.ruta ? result.ruta.length + ' celdas' : 'N/A'}</span>
            </div>
            <div class="result-metric">
                <span>Nodos explorados:</span>
                <span class="result-value">${result.nodos_explorados}</span>
            </div>
            <div class="result-metric">
                <span>Tiempo:</span>
                <span class="result-value">${result.tiempo_ms} ms</span>
            </div>
            <div class="result-message">${result.mensaje}</div>
        </div>
    `;
}

/**
 * Handler general para ejecutar una búsqueda
 */
async function handleSearch(algoritmo) {
    if (!state.maze) return;

    state.isGenerating = true; // Reusamos flag para bloquear botones
    const btn = algoritmo === 'BFS' ? refs.btnSearchBfs : refs.btnSearchDfs;
    btn.classList.add('loading');
    renderer.clearSearch();
    showStatusMessage(`<div class="empty-state">Ejecutando ${algoritmo}...</div>`);
    updateUIState();

    try {
        const { grid, start, goal } = state.maze;
        const result = await ApiClient.search(grid, start, goal, algoritmo);
        
        showStatusMessage('<div class="empty-state">Animando exploración...</div>');
        
        // Esperar a que termine la animación para mostrar los resultados finales
        animateSearch(result, () => {
            showStatusMessage(buildResultHTML(result), !result.encontrado);
        });
        
    } catch (error) {
        showStatusMessage(`<div class="empty-state" style="color: #f87171;">Error: ${error.message}</div>`, true);
    } finally {
        state.isGenerating = false;
        btn.classList.remove('loading');
        updateUIState();
    }
}

/**
 * Handler para la comparación
 */
async function handleCompare() {
    if (!state.maze) return;

    state.isGenerating = true;
    refs.btnCompare.classList.add('loading');
    renderer.clearSearch();
    showStatusMessage('<div class="empty-state">Ejecutando comparación...</div>');
    updateUIState();

    try {
        const { grid, start, goal } = state.maze;
        const result = await ApiClient.compare(grid, start, goal);
        
        // En comparación no animamos para que sea instantáneo y ver los números lado a lado
        // Pintamos el resultado de BFS por defecto (suele ser la mejor ruta)
        renderer.setSearchResult(result.bfs.explorados, result.bfs.ruta);
        
        const html = `
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                ${buildResultHTML(result.bfs)}
                ${buildResultHTML(result.dfs)}
            </div>
        `;
        // Si ninguno encontró ruta, marcamos error
        const isError = !result.bfs.encontrado && !result.dfs.encontrado;
        showStatusMessage(html, isError);
        
    } catch (error) {
        showStatusMessage(`<div class="empty-state" style="color: #f87171;">Error: ${error.message}</div>`, true);
    } finally {
        state.isGenerating = false;
        refs.btnCompare.classList.remove('loading');
        updateUIState();
    }
}

// Asignar listeners de búsqueda
refs.btnSearchBfs.addEventListener('click', () => handleSearch('BFS'));
refs.btnSearchDfs.addEventListener('click', () => handleSearch('DFS'));
refs.btnCompare.addEventListener('click', handleCompare);

// Inicializar UI
updateUIState();
