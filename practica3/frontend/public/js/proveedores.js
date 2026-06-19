let _modalProveedor;

document.addEventListener("DOMContentLoaded", () => {
  _modalProveedor = new bootstrap.Modal(document.getElementById("modal-proveedor"));
  cargarProveedores();
});

document.getElementById("form-proveedor").addEventListener("submit", guardarProveedor);

function mostrarAlerta(mensaje, tipo = "success") {
  const el = document.getElementById("alerta-global");
  el.className = `alert alert-${tipo}`;
  el.textContent = mensaje;
  el.classList.remove("d-none");
  setTimeout(() => el.classList.add("d-none"), 3500);
}

async function cargarProveedores() {
  const { ok, data } = await apiFetch("/api/proveedores");
  const cuerpo = document.getElementById("tabla-proveedores");

  if (!ok || !data.length) {
    cuerpo.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No hay proveedores registrados.</td></tr>`;
    return;
  }

  cuerpo.innerHTML = data.map((p) => `
    <tr>
      <td>${p.nombre}</td>
      <td>${p.nit}</td>
      <td>${p.direccion ?? "-"}</td>
      <td>${p.telefono ?? "-"}</td>
      <td>${p.email ?? "-"}</td>
      <td class="text-end">
        <button class="btn btn-sm btn-outline-primary me-1" onclick='abrirModalEditar(${JSON.stringify(p)})'>
          <i class="bi bi-pencil"></i>
        </button>
        <button class="btn btn-sm btn-outline-danger" onclick="eliminarProveedor(${p.id}, '${p.nombre.replace(/'/g, "\\'")}')">
          <i class="bi bi-trash"></i>
        </button>
      </td>
    </tr>
  `).join("");
}

function abrirModalCrear() {
  document.getElementById("modal-proveedor-titulo").textContent = "Agregar proveedor";
  document.getElementById("form-proveedor").reset();
  document.getElementById("proveedor-id").value = "";
  document.getElementById("proveedor-error").classList.add("d-none");
}

function abrirModalEditar(proveedor) {
  document.getElementById("modal-proveedor-titulo").textContent = "Editar proveedor";
  document.getElementById("proveedor-error").classList.add("d-none");
  document.getElementById("proveedor-id").value = proveedor.id;
  document.getElementById("proveedor-nombre").value = proveedor.nombre;
  document.getElementById("proveedor-nit").value = proveedor.nit;
  document.getElementById("proveedor-direccion").value = proveedor.direccion ?? "";
  document.getElementById("proveedor-telefono").value = proveedor.telefono ?? "";
  document.getElementById("proveedor-email").value = proveedor.email ?? "";
  _modalProveedor.show();
}

async function guardarProveedor(evento) {
  evento.preventDefault();
  const id = document.getElementById("proveedor-id").value;
  const errorEl = document.getElementById("proveedor-error");
  errorEl.classList.add("d-none");

  const datos = {
    nombre: document.getElementById("proveedor-nombre").value,
    nit: document.getElementById("proveedor-nit").value,
    direccion: document.getElementById("proveedor-direccion").value || null,
    telefono: document.getElementById("proveedor-telefono").value || null,
    email: document.getElementById("proveedor-email").value || null,
  };

  const { ok, data } = id
    ? await apiFetch(`/api/proveedores/${id}`, { method: "PUT", body: JSON.stringify(datos) })
    : await apiFetch("/api/proveedores", { method: "POST", body: JSON.stringify(datos) });

  if (!ok) {
    errorEl.textContent = Array.isArray(data?.detail)
      ? data.detail.map((d) => d.msg).join(", ")
      : (data?.detail || "No se pudo guardar el proveedor");
    errorEl.classList.remove("d-none");
    return;
  }

  _modalProveedor.hide();
  mostrarAlerta(id ? "Proveedor actualizado correctamente" : "Proveedor agregado correctamente");
  cargarProveedores();
}

async function eliminarProveedor(id, nombre) {
  if (!confirm(`¿Eliminar al proveedor "${nombre}"?`)) return;

  const { ok, data } = await apiFetch(`/api/proveedores/${id}`, { method: "DELETE" });
  if (!ok) {
    mostrarAlerta(data?.detail || "No se pudo eliminar el proveedor", "danger");
    return;
  }
  mostrarAlerta("Proveedor eliminado correctamente");
  cargarProveedores();
}
