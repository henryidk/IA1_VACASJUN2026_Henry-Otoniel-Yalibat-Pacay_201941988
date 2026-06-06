const API = 'http://localhost:8000/api';

// =====================================================================
// INICIALIZACIÓN
// =====================================================================

document.addEventListener('DOMContentLoaded', () => {
  inicializarTabs();
  cargarCiudades();
  actualizarSesion();

  document.getElementById('btn-buscar').addEventListener('click', buscarRutas);
  document.getElementById('btn-limpiar').addEventListener('click', limpiarBusqueda);
  document.getElementById('btn-add-conexion').addEventListener('click', agregarFilaConexion);
  document.getElementById('btn-agregar-ciudad').addEventListener('click', agregarCiudad);
  document.getElementById('btn-confirmar').addEventListener('click', confirmarCambios);
  document.getElementById('btn-limpiar-sesion').addEventListener('click', limpiarSesion);
  document.getElementById('btn-restablecer').addEventListener('click', restablecerBase);

  document.getElementById('conexiones-container').addEventListener('click', e => {
    if (e.target.classList.contains('btn-remove')) eliminarFilaConexion(e.target);
  });
});

// =====================================================================
// TABS
// =====================================================================

function inicializarTabs() {
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => {
        c.classList.remove('active');
        c.classList.add('hidden');
      });
      tab.classList.add('active');
      const target = document.getElementById(`tab-${tab.dataset.tab}`);
      target.classList.remove('hidden');
      target.classList.add('active');
    });
  });
}

// =====================================================================
// CARGAR CIUDADES EN DROPDOWNS
// =====================================================================

async function cargarCiudades() {
  try {
    const res = await fetch(`${API}/ciudades`);
    const data = await res.json();
    const ciudades = data.ciudades.map(c => formatearNombre(c));

    ['origen', 'destino'].forEach(id => {
      const select = document.getElementById(id);
      select.innerHTML = `<option value="">-- Selecciona ${id} --</option>`;
      data.ciudades.forEach((ciudad, i) => {
        const opt = document.createElement('option');
        opt.value = ciudad;
        opt.textContent = ciudades[i];
        select.appendChild(opt);
      });
    });

    // También poblar el select de conexiones en gestión de ciudades
    poblarSelectConexiones(data.ciudades);
  } catch {
    mostrarAlerta('alerta', 'No se pudo conectar con el servidor.', 'error');
  }
}

function poblarSelectConexiones(ciudades) {
  document.querySelectorAll('.conexion-destino').forEach(select => {
    const valorActual = select.value;
    select.innerHTML = '<option value="">-- Ciudad destino --</option>';
    ciudades.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c;
      opt.textContent = formatearNombre(c);
      select.appendChild(opt);
    });
    if (valorActual) select.value = valorActual;
  });
}

// =====================================================================
// BUSCAR RUTAS
// =====================================================================

async function buscarRutas() {
  const origen = document.getElementById('origen').value;
  const destino = document.getElementById('destino').value;

  ocultarAlerta('alerta');
  document.getElementById('resultados').classList.add('hidden');

  if (!origen || !destino) {
    mostrarAlerta('alerta', 'Por favor selecciona una ciudad de origen y una de destino.', 'error');
    return;
  }

  try {
    const [resRutas, resCorta] = await Promise.all([
      fetch(`${API}/rutas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ origen, destino })
      }),
      fetch(`${API}/ruta-corta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ origen, destino })
      })
    ]);

    if (!resRutas.ok) {
      const err = await resRutas.json();
      mostrarAlerta('alerta', err.detail, 'error');
      return;
    }

    const dataRutas = await resRutas.json();
    const dataCorta = await resCorta.json();

    renderizarRutaCorta(dataCorta.ruta_mas_corta);
    renderizarEstadisticas(dataRutas.estadisticas);
    renderizarListaRutas(dataRutas.rutas);

    document.getElementById('resultados').classList.remove('hidden');
  } catch {
    mostrarAlerta('alerta', 'Error al conectar con el servidor.', 'error');
  }
}

// =====================================================================
// RENDERIZADO DE RESULTADOS
// =====================================================================

function renderizarRutaCorta(ruta) {
  const caminoEl = document.getElementById('ruta-corta-camino');
  const distEl = document.getElementById('ruta-corta-distancia');

  caminoEl.innerHTML = ruta.camino.map((ciudad, i) => {
    const chip = `<span class="ciudad-chip">${formatearNombre(ciudad)}</span>`;
    const flecha = i < ruta.camino.length - 1 ? '<span class="flecha">→</span>' : '';
    return chip + flecha;
  }).join('');

  distEl.textContent = `${ruta.distancia} km`;
}

function renderizarEstadisticas(stats) {
  document.getElementById('stat-total').textContent = stats.total_rutas;
  document.getElementById('stat-min').textContent = `${stats.distancia_minima} km`;
  document.getElementById('stat-max').textContent = `${stats.distancia_maxima} km`;
  document.getElementById('stat-prom').textContent = `${stats.distancia_promedio} km`;
}

function renderizarListaRutas(rutas) {
  const lista = document.getElementById('lista-rutas');
  lista.innerHTML = rutas.map((ruta, i) => `
    <div class="ruta-item">
      <div class="ruta-numero ${i === 0 ? 'primero' : ''}">${i + 1}</div>
      <div class="ruta-detalle">
        <div class="ruta-ciudades">${ruta.camino.map(formatearNombre).join(' → ')}</div>
      </div>
      <div class="ruta-distancia">${ruta.distancia} km</div>
    </div>
  `).join('');
}

// =====================================================================
// LIMPIAR BÚSQUEDA
// =====================================================================

function limpiarBusqueda() {
  document.getElementById('origen').value = '';
  document.getElementById('destino').value = '';
  document.getElementById('resultados').classList.add('hidden');
  ocultarAlerta('alerta');
}

// =====================================================================
// UTILIDADES
// =====================================================================

function formatearNombre(nombre) {
  return nombre.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function mostrarAlerta(id, mensaje, tipo) {
  const el = document.getElementById(id);
  el.textContent = mensaje;
  el.className = `alerta alerta-${tipo}`;
}

function ocultarAlerta(id) {
  const el = document.getElementById(id);
  el.className = 'alerta hidden';
}

// =====================================================================
// GESTIÓN DE CIUDADES — FILAS DE CONEXIÓN
// =====================================================================

function agregarFilaConexion() {
  const container = document.getElementById('conexiones-container');
  const fila = document.createElement('div');
  fila.className = 'conexion-row';
  fila.innerHTML = `
    <select class="conexion-destino">
      <option value="">-- Ciudad destino --</option>
    </select>
    <input type="number" class="conexion-distancia" placeholder="km" min="1" />
    <button class="btn-icon btn-remove" title="Eliminar">✕</button>
  `;
  container.appendChild(fila);

  const ciudadesActuales = Array.from(
    document.getElementById('origen').options
  ).slice(1).map(o => o.value);
  poblarSelectConexiones(ciudadesActuales);
}

function eliminarFilaConexion(btn) {
  const container = document.getElementById('conexiones-container');
  if (container.querySelectorAll('.conexion-row').length > 1) {
    btn.closest('.conexion-row').remove();
  }
}

// =====================================================================
// GESTIÓN DE CIUDADES — AGREGAR A SESIÓN
// =====================================================================

async function agregarCiudad() {
  ocultarAlerta('alerta-ciudad');

  const ciudad = document.getElementById('nueva-ciudad').value.trim();
  if (!ciudad) {
    mostrarAlerta('alerta-ciudad', 'Ingresa el nombre de la ciudad.', 'error');
    return;
  }

  const filas = document.querySelectorAll('#conexiones-container .conexion-row');
  const conexiones = [];

  for (const fila of filas) {
    const destino = fila.querySelector('.conexion-destino').value;
    const distancia = parseFloat(fila.querySelector('.conexion-distancia').value);

    if (!destino || !distancia || distancia <= 0) {
      mostrarAlerta('alerta-ciudad', 'Completa todas las conexiones con ciudad y distancia válida.', 'error');
      return;
    }
    conexiones.push({ destino, distancia });
  }

  try {
    const res = await fetch(`${API}/ciudades/nueva`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ciudad, conexiones })
    });

    const data = await res.json();

    if (!res.ok) {
      mostrarAlerta('alerta-ciudad', data.detail, 'error');
      return;
    }

    mostrarAlerta('alerta-ciudad', data.mensaje, 'exito');
    limpiarFormularioCiudad();
    await actualizarSesion();
  } catch {
    mostrarAlerta('alerta-ciudad', 'Error al conectar con el servidor.', 'error');
  }
}

function limpiarFormularioCiudad() {
  document.getElementById('nueva-ciudad').value = '';
  const container = document.getElementById('conexiones-container');
  container.innerHTML = `
    <div class="conexion-row">
      <select class="conexion-destino">
        <option value="">-- Ciudad destino --</option>
      </select>
      <input type="number" class="conexion-distancia" placeholder="km" min="1" />
      <button class="btn-icon btn-remove" title="Eliminar">✕</button>
    </div>
  `;
  const ciudadesActuales = Array.from(
    document.getElementById('origen').options
  ).slice(1).map(o => o.value);
  poblarSelectConexiones(ciudadesActuales);
}

// =====================================================================
// GESTIÓN DE CIUDADES — SESIÓN
// =====================================================================

async function actualizarSesion() {
  try {
    const res = await fetch(`${API}/sesion`);
    const data = await res.json();
    renderizarSesion(data);
  } catch {
    // silencioso, no crítico
  }
}

function renderizarSesion(data) {
  const vacia = document.getElementById('sesion-vacia');
  const contenido = document.getElementById('sesion-contenido');
  const lista = document.getElementById('sesion-lista');

  if (!data.nuevas_ciudades.length) {
    vacia.classList.remove('hidden');
    contenido.classList.add('hidden');
    return;
  }

  vacia.classList.add('hidden');
  contenido.classList.remove('hidden');

  lista.innerHTML = data.nuevas_ciudades.map(ciudad => {
    const conexiones = data.nuevas_conexiones
      .filter(c => c.origen === ciudad)
      .map(c => `${formatearNombre(c.destino)} — ${c.distancia} km`)
      .join(', ');

    return `
      <div class="sesion-ciudad">
        <div class="sesion-ciudad-nombre">📍 ${formatearNombre(ciudad)}</div>
        ${conexiones ? `<div class="sesion-conexion">Conecta con: ${conexiones}</div>` : ''}
      </div>
    `;
  }).join('');
}

async function confirmarCambios() {
  ocultarAlerta('alerta-sesion');
  try {
    const res = await fetch(`${API}/ciudades/confirmar`, { method: 'POST' });
    const data = await res.json();

    if (!res.ok) {
      mostrarAlerta('alerta-sesion', data.detail, 'error');
      return;
    }

    mostrarAlerta('alerta-sesion', data.mensaje, 'exito');
    await actualizarSesion();
    await cargarCiudades();
  } catch {
    mostrarAlerta('alerta-sesion', 'Error al conectar con el servidor.', 'error');
  }
}

async function limpiarSesion() {
  ocultarAlerta('alerta-sesion');
  try {
    const res = await fetch(`${API}/ciudades/sesion`, { method: 'DELETE' });
    const data = await res.json();
    mostrarAlerta('alerta-sesion', data.mensaje, 'exito');
    await actualizarSesion();
  } catch {
    mostrarAlerta('alerta-sesion', 'Error al conectar con el servidor.', 'error');
  }
}

async function restablecerBase() {
  if (!confirm('¿Estás seguro? Esto eliminará todas las ciudades agregadas y volverá a la base de conocimiento original.')) return;
  ocultarAlerta('alerta-sesion');
  try {
    const res = await fetch(`${API}/ciudades/restablecer`, { method: 'DELETE' });
    const data = await res.json();
    mostrarAlerta('alerta-sesion', data.mensaje, 'exito');
    await actualizarSesion();
    await cargarCiudades();
    limpiarBusqueda();
  } catch {
    mostrarAlerta('alerta-sesion', 'Error al conectar con el servidor.', 'error');
  }
}
