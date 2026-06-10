const API_BASE = '/api';

let sintomasSeleccionados = [];

document.addEventListener('DOMContentLoaded', cargarSintomas);
document.getElementById('btn-diagnosticar').addEventListener('click', diagnosticar);
document.getElementById('btn-limpiar').addEventListener('click', limpiar);


async function cargarSintomas() {
  try {
    const res = await fetch(`${API_BASE}/sintomas`);
    const data = await res.json();
    renderizarSintomas(data.sintomas);
  } catch (e) {
    document.getElementById('sintomas-container').innerHTML = `
      <div class="col-12 text-center text-danger py-4">
        <i class="bi bi-exclamation-triangle fs-3"></i>
        <p class="mt-2">Error al cargar los síntomas. Verifica que el servidor esté corriendo.</p>
      </div>`;
  }
}

function renderizarSintomas(sintomas) {
  const container = document.getElementById('sintomas-container');
  container.innerHTML = sintomas.map(s => `
    <div class="col-md-4 col-lg-3">
      <div class="sintoma-card" data-id="${s.id}" onclick="toggleSintoma(this)">
        <i class="bi bi-check-circle sintoma-icono me-2 text-muted"></i>
        ${s.descripcion}
      </div>
    </div>`).join('');
}

function toggleSintoma(card) {
  const id = card.dataset.id;
  card.classList.toggle('seleccionado');

  if (card.classList.contains('seleccionado')) {
    sintomasSeleccionados.push(id);
  } else {
    sintomasSeleccionados = sintomasSeleccionados.filter(s => s !== id);
  }
}

function limpiar() {
  sintomasSeleccionados = [];
  document.querySelectorAll('.sintoma-card.seleccionado')
    .forEach(c => c.classList.remove('seleccionado'));
  document.getElementById('seccion-resultado').style.display = 'none';
}

async function diagnosticar() {
  if (sintomasSeleccionados.length === 0) {
    alert('Selecciona al menos un síntoma antes de diagnosticar.');
    return;
  }

  const btn = document.getElementById('btn-diagnosticar');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analizando...';

  try {
    const res = await fetch(`${API_BASE}/diagnose`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sintomas: sintomasSeleccionados })
    });

    const data = await res.json();

    if (!res.ok) {
      mostrarError(data.error || 'No se encontró diagnóstico para los síntomas seleccionados.');
      return;
    }

    mostrarResultado(data);

  } catch (e) {
    mostrarError('Error de conexión con el servidor. Verifica que Docker esté corriendo.');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="bi bi-search me-1"></i>Diagnosticar';
  }
}

function mostrarError(mensaje) {
  const contenido = document.getElementById('resultado-contenido');
  contenido.innerHTML = `
    <div class="alert alert-danger mb-0">
      <i class="bi bi-exclamation-triangle me-2"></i>${mensaje}
    </div>`;
  mostrarSeccionResultado();
}

function mostrarSeccionResultado() {
  const seccion = document.getElementById('seccion-resultado');
  seccion.style.display = 'block';
  seccion.scrollIntoView({ behavior: 'smooth' });
}

function mostrarResultado(data) {
  const contenido = document.getElementById('resultado-contenido');

  const recomendaciones = data.recomendaciones.map(r => `
    <li class="py-2">
      <i class="bi bi-check2 text-success me-2"></i>${r}
    </li>`).join('');

  contenido.innerHTML = `
    <div class="mb-3 d-flex justify-content-between align-items-center text-muted small">
      <span><i class="bi bi-hash me-1"></i>Diagnóstico #${data.id}</span>
      <span><i class="bi bi-calendar me-1"></i>${data.fecha}</span>
    </div>

    <div class="resultado-falla mb-4">
      <div class="fw-bold fs-5 mb-1">
        <i class="bi bi-exclamation-triangle text-warning me-2"></i>Falla detectada
      </div>
      <div class="fs-6">${data.descripcion}</div>
    </div>

    <div>
      <div class="fw-bold mb-2">
        <i class="bi bi-lightbulb text-primary me-2"></i>Recomendaciones
      </div>
      <ul class="list-unstyled resultado-recomendaciones mb-0">
        ${recomendaciones}
      </ul>
    </div>`;

  mostrarSeccionResultado();
}
