/**
 * MazeRenderer
 * Encargado de dibujar el laberinto y sus estados (ruta, explorados) en un elemento <canvas>.
 */

export class MazeRenderer {
    /**
     * @param {HTMLCanvasElement} canvas Elemento canvas donde se dibujará
     */
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // Estado interno
        this.grid = null;
        this.start = null;
        this.goal = null;
        this.cellSize = 0;
        
        // Capas visuales (se sobreponen a la cuadrícula base)
        this.explored = []; // Celdas exploradas (animación)
        this.path = [];     // Ruta final
        
        // Cargar colores desde las variables CSS para mantener consistencia
        this.colors = this._loadColors();
        
        // Escuchar cambios de tamaño de ventana para redibujar
        window.addEventListener('resize', () => {
            if (this.grid) this._resizeAndDraw();
        });
    }

    /**
     * Carga un nuevo laberinto y lo dibuja en estado inicial.
     */
    loadMaze(mazeData) {
        this.grid = mazeData.grid;
        this.start = mazeData.start;
        this.goal = mazeData.goal;
        this.explored = [];
        this.path = [];
        this._resizeAndDraw();
    }

    /**
     * Establece los datos de búsqueda y redibuja.
     */
    setSearchResult(explored, path) {
        this.explored = explored || [];
        this.path = path || [];
        this.draw();
    }
    
    /**
     * Limpia las capas de búsqueda (explorados y ruta)
     */
    clearSearch() {
        this.explored = [];
        this.path = [];
        this.draw();
    }

    // --- Métodos Internos ---

    _loadColors() {
        const style = getComputedStyle(document.documentElement);
        return {
            wall: style.getPropertyValue('--maze-wall').trim() || '#778873',
            path: style.getPropertyValue('--maze-path').trim() || '#FDF6ED',
            start: style.getPropertyValue('--maze-start').trim() || '#A1BC98',
            goal: style.getPropertyValue('--maze-goal').trim() || '#DCCFC0',
            route: style.getPropertyValue('--maze-route').trim() || '#778873',
            explored: style.getPropertyValue('--maze-explored').trim() || '#A1BC98',
            dark: style.getPropertyValue('--color-dark').trim() || '#778873',
            cream: style.getPropertyValue('--color-cream').trim() || '#FDF6ED'
        };
    }

    _resizeAndDraw() {
        if (!this.grid || !this.grid.length) return;

        const container = this.canvas.parentElement;
        const padding = 10;
        
        const availableWidth = container.clientWidth - (padding * 2);
        const availableHeight = container.clientHeight - (padding * 2);

        const rows = this.grid.length;
        const cols = this.grid[0].length;

        // Calcular el tamaño óptimo de celda para que quepa en el contenedor
        this.cellSize = Math.floor(Math.min(
            availableWidth / cols,
            availableHeight / rows
        ));

        // Asegurar un tamaño mínimo y máximo para que se vea bien
        if (this.cellSize < 5) this.cellSize = 5;
        if (this.cellSize > 40) this.cellSize = 40;

        this.canvas.width = this.cellSize * cols;
        this.canvas.height = this.cellSize * rows;

        this.draw();
    }

    draw() {
        if (!this.grid) return;

        const rows = this.grid.length;
        const cols = this.grid[0].length;

        // 1. Fondo base (muros por defecto)
        this.ctx.fillStyle = this.colors.wall;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // 2. Dibujar caminos (0 = abierto)
        this.ctx.fillStyle = this.colors.path;
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                if (this.grid[r][c] === 0) {
                    this._drawCell(r, c, this.colors.path);
                }
            }
        }

        // 3. Dibujar nodos explorados
        if (this.explored && this.explored.length > 0) {
            this.ctx.fillStyle = this.colors.explored;
            for (const pos of this.explored) {
                // No sobreescribir start y goal visualmente con explorados
                if (this._isStart(pos) || this._isGoal(pos)) continue;
                this._drawCell(pos.row, pos.col, this.colors.explored);
            }
        }

        // 4. Dibujar ruta encontrada
        if (this.path && this.path.length > 0) {
            this.ctx.fillStyle = this.colors.route;
            for (const pos of this.path) {
                if (this._isStart(pos) || this._isGoal(pos)) continue;
                
                // Círculo para la ruta se ve mejor que cuadro completo
                this._drawCircle(pos.row, pos.col, this.colors.route, 0.6);
            }
        }

        // 5. Dibujar Inicio y Meta
        if (this.start) {
            this._drawCell(this.start.row, this.start.col, this.colors.start);
            // Glifo oscuro para inicio
            this._drawText(this.start.row, this.start.col, "S", this.colors.dark);
        }
        
        if (this.goal) {
            this._drawCell(this.goal.row, this.goal.col, this.colors.goal);
            // Glifo oscuro para meta
            this._drawText(this.goal.row, this.goal.col, "G", this.colors.dark);
        }
    }

    _drawCell(row, col, color) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(
            col * this.cellSize, 
            row * this.cellSize, 
            this.cellSize, 
            this.cellSize
        );
        
        // Si es muro, añadir un borde sutil para darle textura de bloque
        if (color === this.colors.wall) {
            this.ctx.strokeStyle = "rgba(0,0,0,0.15)";
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(
                col * this.cellSize + 1, 
                row * this.cellSize + 1, 
                this.cellSize - 2, 
                this.cellSize - 2
            );
        } else if (color === this.colors.path) {
            // Celda vacía, dibujar un borde sutil (la cuadrícula)
            this.ctx.strokeStyle = "rgba(119, 136, 115, 0.1)"; // var(--color-dark) muy transparente
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(
                col * this.cellSize, 
                row * this.cellSize, 
                this.cellSize, 
                this.cellSize
            );
        }
    }
    
    _drawCircle(row, col, color, scale = 0.5) {
        const cx = (col * this.cellSize) + (this.cellSize / 2);
        const cy = (row * this.cellSize) + (this.cellSize / 2);
        const radius = (this.cellSize * scale) / 2;

        // Dibujar el fondo de la ruta
        this.ctx.fillStyle = color;
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, radius, 0, Math.PI * 2);
        this.ctx.fill();

        // Patrón punteado sobre la ruta como indicó el plan
        this.ctx.fillStyle = this.colors.cream;
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, radius * 0.4, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    _drawText(row, col, text, color) {
        this.ctx.fillStyle = color;
        this.ctx.font = `bold ${Math.floor(this.cellSize * 0.6)}px Fredoka, sans-serif`;
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        const x = (col * this.cellSize) + (this.cellSize / 2);
        const y = (row * this.cellSize) + (this.cellSize / 2) + 2; // pequeño ajuste visual para Fredoka
        this.ctx.fillText(text, x, y);
    }

    _isStart(pos) {
        return this.start && pos.row === this.start.row && pos.col === this.start.col;
    }

    _isGoal(pos) {
        return this.goal && pos.row === this.goal.row && pos.col === this.goal.col;
    }
}
