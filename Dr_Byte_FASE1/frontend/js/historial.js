const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', cargarHistorial);


async function cargarHistorial() {
  try {
    const res = await fetch(`${API_BASE}/history`);
    const data = await res.json();

    document.getElementById('total-registros').textContent = `${data.total} registros`;

    if (data.total === 0) {
      mostrarVacio();
      return;
    }

    renderizarTabla(data.historial);

  } catch (e) {
    document.getElementById('historial-contenido').innerHTML = `
      <div class="text-center text-danger py-5">
        <i class="bi bi-exclamation-triangle fs-3"></i>
        <p class="mt-2">Error al cargar el historial. Verifica que el servidor esté corriendo.</p>
      </div>`;
  }
}

function mostrarVacio() {
  document.getElementById('historial-contenido').innerHTML = `
    <div class="text-center text-muted py-5">
      <i class="bi bi-inbox fs-2"></i>
      <p class="mt-2">No hay diagnósticos registrados aún.</p>
      <a href="index.html" class="btn btn-primary btn-sm mt-1">
        <i class="bi bi-search me-1"></i>Hacer un diagnóstico
      </a>
    </div>`;
}

function renderizarTabla(historial) {
  const filas = historial.map(r => `
    <tr onclick="verDetalle(${r.id})" title="Ver detalle">
      <td class="text-center fw-bold">#${r.id}</td>
      <td>${r.fecha}</td>
      <td><span class="badge-falla">${r.descripcion}</span></td>
      <td class="text-center">${r.sintomas.length}</td>
      <td class="text-center">
        <i class="bi bi-eye text-primary"></i>
      </td>
    </tr>`).join('');

  document.getElementById('historial-contenido').innerHTML = `
    <div class="table-responsive">
      <table class="table tabla-historial mb-0">
        <thead class="table-light">
          <tr>
            <th class="text-center">ID</th>
            <th>Fecha</th>
            <th>Falla detectada</th>
            <th class="text-center">Síntomas</th>
            <th class="text-center">Detalle</th>
          </tr>
        </thead>
        <tbody>${filas}</tbody>
      </table>
    </div>`;
}

async function verDetalle(id) {
  try {
    const res = await fetch(`${API_BASE}/history/${id}`);
    const data = await res.json();

    const sintomas = data.sintomas.map(s => `
      <span class="badge bg-light text-dark border me-1 mb-1">${s}</span>`).join('');

    const recomendaciones = data.recomendaciones.map(r => `
      <li class="py-1">
        <i class="bi bi-check2 text-success me-2"></i>${r}
      </li>`).join('');

    document.getElementById('modal-detalle-contenido').innerHTML = `
      <div class="mb-3 d-flex justify-content-between text-muted small">
        <span><i class="bi bi-hash me-1"></i>Diagnóstico #${data.id}</span>
        <span><i class="bi bi-calendar me-1"></i>${data.fecha}</span>
      </div>

      <div class="resultado-falla mb-4">
        <div class="fw-bold mb-1">
          <i class="bi bi-exclamation-triangle text-warning me-2"></i>Falla detectada
        </div>
        <div>${data.descripcion}</div>
      </div>

      <div class="mb-4">
        <div class="fw-bold mb-2">
          <i class="bi bi-activity text-primary me-2"></i>Síntomas reportados
        </div>
        <div>${sintomas}</div>
      </div>

      <div>
        <div class="fw-bold mb-2">
          <i class="bi bi-lightbulb text-primary me-2"></i>Recomendaciones
        </div>
        <ul class="list-unstyled resultado-recomendaciones mb-0">
          ${recomendaciones}
        </ul>
      </div>`;

    new bootstrap.Modal(document.getElementById('modalDetalle')).show();

  } catch (e) {
    alert('Error al cargar el detalle del diagnóstico.');
  }
}
