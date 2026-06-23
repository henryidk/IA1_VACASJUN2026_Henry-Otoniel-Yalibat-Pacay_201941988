/**
 * MazeRenderer
 * Encargado de dibujar el laberinto y sus estados (ruta, explorados) en un elemento <canvas>.
 */

export class MazeRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');

        this.grid = null;
        this.start = null;
        this.goal = null;
        this.cellSize = 0;

        this.explored = [];
        this.path = [];

        this.colors = this._loadColors();

        window.addEventListener('resize', () => {
            if (this.grid) this._resizeAndDraw();
        });
    }

    loadMaze(mazeData) {
        this.grid = mazeData.grid;
        this.start = mazeData.start;
        this.goal = mazeData.goal;
        this.explored = [];
        this.path = [];
        this._resizeAndDraw();
    }

    setSearchResult(explored, path) {
        this.explored = explored || [];
        this.path = path || [];
        this.draw();
    }

    clearSearch() {
        this.explored = [];
        this.path = [];
        this.draw();
    }

    // Mueve el inicio y redibuja de inmediato
    setStart(row, col) {
        this.start = { row, col };
        if (this.grid) this.draw();
    }

    // Mueve la meta y redibuja de inmediato
    setGoal(row, col) {
        this.goal = { row, col };
        if (this.grid) this.draw();
    }

    // --- Métodos Internos ---

    _loadColors() {
        const style = getComputedStyle(document.documentElement);
        return {
            wall:     style.getPropertyValue('--maze-wall').trim()     || '#778873',
            path:     style.getPropertyValue('--maze-path').trim()     || '#FDF6ED',
            start:    style.getPropertyValue('--maze-start').trim()    || '#A1BC98',
            goal:     style.getPropertyValue('--maze-goal').trim()     || '#DCCFC0',
            route:    style.getPropertyValue('--maze-route').trim()    || '#778873',
            explored: style.getPropertyValue('--maze-explored').trim() || '#A1BC98',
            dark:     style.getPropertyValue('--color-dark').trim()    || '#778873',
            cream:    style.getPropertyValue('--color-cream').trim()   || '#FDF6ED'
        };
    }

    _resizeAndDraw() {
        if (!this.grid || !this.grid.length) return;

        const container = this.canvas.parentElement;
        const padding = 10;

        const availableWidth  = container.clientWidth  - padding * 2;
        const availableHeight = container.clientHeight - padding * 2;

        const rows = this.grid.length;
        const cols = this.grid[0].length;

        this.cellSize = Math.floor(Math.min(availableWidth / cols, availableHeight / rows));
        if (this.cellSize < 5)  this.cellSize = 5;
        if (this.cellSize > 40) this.cellSize = 40;

        this.canvas.width  = this.cellSize * cols;
        this.canvas.height = this.cellSize * rows;

        this.draw();
    }

    draw() {
        if (!this.grid) return;

        const rows = this.grid.length;
        const cols = this.grid[0].length;

        // 1. Fondo base
        this.ctx.fillStyle = this.colors.cream;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // 2. Muros y caminos
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                if (this.grid[r][c] === 1) {
                    if (this.cellSize >= 8 && this._isRock(r, c)) {
                        this._drawRock(r, c);
                    } else {
                        this._drawWall(r, c);
                    }
                } else {
                    this._drawPath(r, c);
                }
            }
        }

        // 3. Nodos explorados
        if (this.explored && this.explored.length > 0) {
            for (const pos of this.explored) {
                if (this._isStart(pos) || this._isGoal(pos)) continue;
                this.ctx.fillStyle = this.colors.explored;
                this.ctx.fillRect(pos.col * this.cellSize, pos.row * this.cellSize, this.cellSize, this.cellSize);
            }
        }

        // 4. Ruta final
        if (this.path && this.path.length > 0) {
            for (const pos of this.path) {
                if (this._isStart(pos) || this._isGoal(pos)) continue;
                this._drawCircle(pos.row, pos.col, this.colors.route, 0.6);
            }
        }

        // 5. Inicio y Meta (siempre encima de todo)
        if (this.start) this._drawStart(this.start.row, this.start.col);
        if (this.goal)  this._drawGoal(this.goal.row, this.goal.col);
    }

    // ---- Celdas base ----

    _drawWall(row, col) {
        const x = col * this.cellSize;
        const y = row * this.cellSize;
        const s = this.cellSize;
        this.ctx.fillStyle = this.colors.wall;
        this.ctx.fillRect(x, y, s, s);
        if (s >= 6) {
            this.ctx.strokeStyle = 'rgba(0,0,0,0.15)';
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(x + 0.5, y + 0.5, s - 1, s - 1);
        }
    }

    _drawPath(row, col) {
        const x = col * this.cellSize;
        const y = row * this.cellSize;
        const s = this.cellSize;
        this.ctx.fillStyle = this.colors.path;
        this.ctx.fillRect(x, y, s, s);
        if (s >= 6) {
            this.ctx.strokeStyle = 'rgba(119, 136, 115, 0.1)';
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(x + 0.5, y + 0.5, s - 1, s - 1);
        }
    }

    // ---- Sprites retro ----

    // Determina si un muro se dibuja como roca (determinístico por posición)
    _isRock(row, col) {
        return ((row * 73 + col * 37) * 17 + row * col) % 100 < 40;
    }

    _drawRock(row, col) {
        const x = col * this.cellSize;
        const y = row * this.cellSize;
        const s = this.cellSize;
        const ctx = this.ctx;
        const u = Math.max(1, Math.floor(s / 8));

        // Cuerpo de la roca
        ctx.fillStyle = '#5c6a58';
        ctx.fillRect(x, y, s, s);

        // Borde exterior (oscuro)
        ctx.fillStyle = '#47544a';
        ctx.fillRect(x,         y,         s, u); // top
        ctx.fillRect(x,         y + s - u, s, u); // bottom
        ctx.fillRect(x,         y,         u, s); // left
        ctx.fillRect(x + s - u, y,         u, s); // right

        // Highlight esquina superior-izquierda (hace el efecto 3D retro)
        ctx.fillStyle = '#8ea089';
        ctx.fillRect(x + u, y + u, s - u * 3, u);
        ctx.fillRect(x + u, y + u, u,         s - u * 3);

        // Grieta diagonal pixel-art
        const crackX = x + Math.floor(s * 0.45);
        const crackY = y + Math.floor(s * 0.28);
        ctx.fillStyle = '#47544a';
        ctx.fillRect(crackX,     crackY,          u, u * 3);
        ctx.fillRect(crackX + u, crackY + u * 2,  u, u * 2);
    }

    // Corazón retro — marca el punto de inicio
    _drawStart(row, col) {
        const x = col * this.cellSize;
        const y = row * this.cellSize;
        const s = this.cellSize;
        const ctx = this.ctx;

        // Fondo verde claro
        ctx.fillStyle = this.colors.start;
        ctx.fillRect(x, y, s, s);

        // Símbolo corazón con borde para efecto retro
        const fontSize = Math.max(8, Math.floor(s * 0.68));
        const cx = x + s / 2;
        const cy = y + s / 2 + Math.floor(fontSize * 0.06);

        // Sombra/borde oscuro (dibujado primero, desplazado 1px)
        ctx.font = `bold ${fontSize}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = 'rgba(0,0,0,0.25)';
        ctx.fillText('♥', cx + 1, cy + 1);

        // Corazón oscuro
        ctx.fillStyle = this.colors.dark;
        ctx.fillText('♥', cx, cy);

        // Brillo pequeño (punto crema en la esquina superior del corazón)
        if (s >= 14) {
            ctx.fillStyle = this.colors.cream;
            ctx.globalAlpha = 0.5;
            const dotR = Math.max(1, Math.floor(s * 0.07));
            ctx.beginPath();
            ctx.arc(cx - Math.floor(s * 0.1), cy - Math.floor(s * 0.12), dotR, 0, Math.PI * 2);
            ctx.fill();
            ctx.globalAlpha = 1.0;
        }
    }

    // Meta con símbolo de corazón (según solicitud)
    _drawGoal(row, col) {
        const x = col * this.cellSize;
        const y = row * this.cellSize;
        const s = this.cellSize;
        const ctx = this.ctx;

        // Fondo beige
        ctx.fillStyle = this.colors.goal;
        ctx.fillRect(x, y, s, s);

        const fontSize = Math.max(8, Math.floor(s * 0.68));
        const cx = x + s / 2;
        const cy = y + s / 2 + Math.floor(fontSize * 0.06);

        ctx.font = `bold ${fontSize}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        // Sombra/borde
        ctx.fillStyle = 'rgba(0,0,0,0.25)';
        ctx.fillText('♥', cx + 1, cy + 1);

        // Corazón oscuro
        ctx.fillStyle = this.colors.dark;
        ctx.fillText('♥', cx, cy);
    }

    _drawCircle(row, col, color, scale = 0.5) {
        const cx = col * this.cellSize + this.cellSize / 2;
        const cy = row * this.cellSize + this.cellSize / 2;
        const radius = (this.cellSize * scale) / 2;

        this.ctx.fillStyle = color;
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, radius, 0, Math.PI * 2);
        this.ctx.fill();

        this.ctx.fillStyle = this.colors.cream;
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, radius * 0.4, 0, Math.PI * 2);
        this.ctx.fill();
    }

    _isStart(pos) {
        return this.start && pos.row === this.start.row && pos.col === this.start.col;
    }

    _isGoal(pos) {
        return this.goal && pos.row === this.goal.row && pos.col === this.goal.col;
    }
}
