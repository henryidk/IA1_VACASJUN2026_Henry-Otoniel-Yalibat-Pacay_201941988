document.addEventListener("DOMContentLoaded", cargarFacturas);
document.getElementById("archivo-factura").addEventListener("change", mostrarVistaPrevia);
document.getElementById("form-carga").addEventListener("submit", subirFactura);
document.getElementById("filtro-estado").addEventListener("change", cargarFacturas);

function mostrarAlerta(mensaje, tipo = "success") {
  const el = document.getElementById("alerta-global");
  el.className = `alert alert-${tipo}`;
  el.textContent = mensaje;
  el.classList.remove("d-none");
  setTimeout(() => el.classList.add("d-none"), 3500);
}

function mostrarVistaPrevia() {
  const archivo = document.getElementById("archivo-factura").files[0];
  const contenedor = document.getElementById("vista-previa");
  const imagenEl = document.getElementById("vista-previa-imagen");
  const pdfEl = document.getElementById("vista-previa-pdf");

  imagenEl.classList.add("d-none");
  pdfEl.classList.add("d-none");

  if (!archivo) {
    contenedor.classList.add("d-none");
    return;
  }

  const url = URL.createObjectURL(archivo);
  if (archivo.type === "application/pdf") {
    pdfEl.src = url;
    pdfEl.classList.remove("d-none");
  } else {
    imagenEl.src = url;
    imagenEl.classList.remove("d-none");
  }
  contenedor.classList.remove("d-none");
}

async function subirFactura(evento) {
  evento.preventDefault();
  const archivo = document.getElementById("archivo-factura").files[0];
  if (!archivo) return;

  const boton = document.getElementById("btn-cargar");
  boton.disabled = true;
  boton.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>Procesando...`;

  const formData = new FormData();
  formData.append("archivo", archivo);

  const { ok, data } = await apiFetch("/api/facturas", { method: "POST", body: formData });

  boton.disabled = false;
  boton.innerHTML = `<i class="bi bi-upload me-1"></i>Subir y procesar`;

  if (!ok) {
    mostrarAlerta(data?.detail || "No se pudo cargar la factura", "danger");
    return;
  }

  window.location.href = `factura.html?id=${data.id}`;
}

function badgeEstado(estado) {
  const etiquetas = { pendiente: "Pendiente", procesado: "Procesado", rechazado: "Rechazado", error: "Error" };
  return `<span class="badge badge-${estado}">${etiquetas[estado] || estado}</span>`;
}

async function cargarFacturas() {
  const estado = document.getElementById("filtro-estado").value;
  const ruta = estado ? `/api/facturas?estado=${estado}` : "/api/facturas";
  const { ok, data } = await apiFetch(ruta);
  const cuerpo = document.getElementById("tabla-facturas");

  if (!ok || !data.length) {
    cuerpo.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">No hay facturas cargadas.</td></tr>`;
    return;
  }

  cuerpo.innerHTML = data.map((f) => `
    <tr>
      <td>${f.nombre_archivo}</td>
      <td>${f.numero_factura ?? "-"}</td>
      <td>${f.fecha ?? "-"}</td>
      <td>${f.total ?? "-"}</td>
      <td>${badgeEstado(f.estado)}</td>
      <td>${new Date(f.creado_en).toLocaleString("es-GT")}</td>
      <td class="text-end">
        <a href="factura.html?id=${f.id}" class="btn btn-sm btn-outline-primary">
          <i class="bi bi-eye"></i> Ver
        </a>
      </td>
    </tr>
  `).join("");
}
