const _idFactura = new URLSearchParams(window.location.search).get("id");

document.addEventListener("DOMContentLoaded", async () => {
  if (!_idFactura) {
    window.location.href = "facturas.html";
    return;
  }
  await cargarProveedoresSelect();
  await cargarFactura();
});

document.getElementById("form-factura").addEventListener("submit", guardarCambios);
document.getElementById("btn-registrar").addEventListener("click", dispararRpa);

function mostrarAlerta(mensaje, tipo = "success") {
  const el = document.getElementById("alerta-global");
  el.className = `alert alert-${tipo}`;
  el.textContent = mensaje;
  el.classList.remove("d-none");
}

function badgeEstado(estado) {
  const etiquetas = { pendiente: "Pendiente", procesado: "Procesado", rechazado: "Rechazado", error: "Error" };
  return `<span class="badge badge-${estado}">${etiquetas[estado] || estado}</span>`;
}

async function cargarProveedoresSelect() {
  const { ok, data } = await apiFetch("/api/proveedores");
  if (!ok) return;
  const select = document.getElementById("f-proveedor_id");
  data.forEach((p) => {
    const opcion = document.createElement("option");
    opcion.value = p.id;
    opcion.textContent = `${p.nombre} (${p.nit})`;
    select.appendChild(opcion);
  });
}

async function cargarFactura() {
  const { ok, data } = await apiFetch(`/api/facturas/${_idFactura}`);
  if (!ok) {
    mostrarAlerta(data?.detail || "No se pudo cargar la factura", "danger");
    return;
  }

  const procesando = data.estado === "pendiente";
  document.getElementById("alerta-procesando").classList.toggle("d-none", !procesando);

  document.getElementById("factura-nombre-archivo").textContent = data.nombre_archivo;
  document.getElementById("factura-estado").innerHTML = badgeEstado(data.estado);
  document.getElementById("f-numero_factura").value = data.numero_factura ?? "";
  document.getElementById("f-fecha").value = data.fecha ?? "";
  document.getElementById("f-proveedor_id").value = data.proveedor_id ?? "";
  document.getElementById("f-subtotal").value = data.subtotal ?? "";
  document.getElementById("f-impuestos").value = data.impuestos ?? "";
  document.getElementById("f-total").value = data.total ?? "";
  document.getElementById("factura-texto-ocr").textContent = data.texto_ocr || "(sin texto extraído todavía)";

  document.getElementById("btn-registrar").disabled = data.estado !== "procesado";

  if (procesando) {
    setTimeout(cargarFactura, 2000);
  }
}

async function guardarCambios(evento) {
  evento.preventDefault();

  const datos = {
    numero_factura: document.getElementById("f-numero_factura").value || null,
    fecha: document.getElementById("f-fecha").value || null,
    proveedor_id: document.getElementById("f-proveedor_id").value || null,
    subtotal: document.getElementById("f-subtotal").value || null,
    impuestos: document.getElementById("f-impuestos").value || null,
    total: document.getElementById("f-total").value || null,
  };

  const { ok, data } = await apiFetch(`/api/facturas/${_idFactura}`, {
    method: "PUT",
    body: JSON.stringify(datos),
  });

  if (!ok) {
    mostrarAlerta(Array.isArray(data?.detail) ? data.detail.map((d) => d.msg).join(", ") : (data?.detail || "No se pudo guardar"), "danger");
    return;
  }

  mostrarAlerta("Factura actualizada correctamente");
  document.getElementById("factura-estado").innerHTML = badgeEstado(data.estado);
  document.getElementById("btn-registrar").disabled = data.estado !== "procesado";
}

async function dispararRpa() {
  const boton = document.getElementById("btn-registrar");
  boton.disabled = true;
  boton.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>Registrando...`;

  const { ok, data } = await apiFetch(`/api/facturas/${_idFactura}/rpa`, { method: "POST" });

  boton.innerHTML = `<i class="bi bi-robot me-1"></i>Registrar`;
  boton.disabled = false;

  if (!ok) {
    mostrarAlerta(data?.detail || "No se pudo completar el registro automático", "danger");
    return;
  }
  mostrarAlerta(data.detail || "Registrado correctamente con RPA");
}
