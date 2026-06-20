let _ultimoReporteId = null;

document.addEventListener("DOMContentLoaded", cargarProveedoresSelect);

function mostrarAlerta(mensaje, tipo = "success") {
  const el = document.getElementById("alerta-global");
  el.className = `alert alert-${tipo}`;
  el.textContent = mensaje;
  el.classList.remove("d-none");
}

async function cargarProveedoresSelect() {
  const { ok, data } = await apiFetch("/api/proveedores");
  if (!ok) return;
  const select = document.getElementById("r-proveedor");
  data.forEach((p) => {
    const opcion = document.createElement("option");
    opcion.value = p.id;
    opcion.textContent = p.nombre;
    select.appendChild(opcion);
  });
}

function construirQueryReporte() {
  const parametros = new URLSearchParams();
  const estado = document.getElementById("r-estado").value;
  const proveedorId = document.getElementById("r-proveedor").value;
  const fechaDesde = document.getElementById("r-fecha-desde").value;
  const fechaHasta = document.getElementById("r-fecha-hasta").value;

  if (estado) parametros.set("estado", estado);
  if (proveedorId) parametros.set("proveedor_id", proveedorId);
  if (fechaDesde) parametros.set("fecha_desde", fechaDesde);
  if (fechaHasta) parametros.set("fecha_hasta", fechaHasta);
  return parametros.toString();
}

async function generarReporte(formato) {
  const boton = document.getElementById(formato === "pdf" ? "btn-generar-pdf" : "btn-generar-excel");
  const textoOriginal = boton.innerHTML;
  boton.disabled = true;
  boton.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>Generando...`;

  try {
    const query = construirQueryReporte();
    const ruta = `/api/reportes/${formato}${query ? "?" + query : ""}`;

    const respuesta = await fetch(`${API_BASE_URL}${ruta}`, {
      headers: { Authorization: `Bearer ${obtenerToken()}` },
    });

    if (!respuesta.ok) {
      mostrarAlerta("No se pudo generar el reporte", "danger");
      return;
    }

    const blob = await respuesta.blob();
    const url = URL.createObjectURL(blob);
    const enlace = document.createElement("a");
    enlace.href = url;
    enlace.download = formato === "pdf" ? "reporte_facturas.pdf" : "reporte_facturas.xlsx";
    document.body.appendChild(enlace);
    enlace.click();
    enlace.remove();
    URL.revokeObjectURL(url);

    _ultimoReporteId = respuesta.headers.get("X-Reporte-Id");
    document.getElementById("card-enviar").style.display = _ultimoReporteId ? "block" : "none";
    mostrarAlerta(`Reporte ${formato.toUpperCase()} descargado correctamente`);
  } catch (err) {
    mostrarAlerta(`No se pudo conectar con el servidor: ${err.message}`, "danger");
  } finally {
    boton.disabled = false;
    boton.innerHTML = textoOriginal;
  }
}

async function enviarReporte() {
  if (!_ultimoReporteId) {
    mostrarAlerta("Primero genera un reporte (PDF o Excel) antes de enviarlo", "danger");
    return;
  }

  const boton = document.getElementById("btn-enviar-correo");
  const textoOriginal = boton.innerHTML;
  boton.disabled = true;
  boton.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>Enviando...`;

  try {
    const destinatario = document.getElementById("r-destinatario").value || null;

    const { ok, data } = await apiFetch(`/api/reportes/${_ultimoReporteId}/enviar`, {
      method: "POST",
      body: JSON.stringify({ destinatario }),
    });

    if (!ok) {
      mostrarAlerta(data?.detail || "No se pudo enviar el correo", "danger");
      return;
    }
    mostrarAlerta(data.detail || "Reporte enviado correctamente");
  } catch (err) {
    mostrarAlerta(`No se pudo conectar con el servidor: ${err.message}`, "danger");
  } finally {
    boton.disabled = false;
    boton.innerHTML = textoOriginal;
  }
}
