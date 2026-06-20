document.addEventListener("DOMContentLoaded", cargarBitacora);

function badgeEstado(estado) {
  const conocidos = ["pendiente", "procesado", "rechazado", "error"];
  const clase = conocidos.includes(estado) ? `badge-${estado}` : "bg-secondary";
  return `<span class="badge ${clase}">${estado}</span>`;
}

function construirQuery() {
  const parametros = new URLSearchParams();
  const estado = document.getElementById("f-estado").value;
  const tipoEvento = document.getElementById("f-tipo-evento").value;
  const usuarioId = document.getElementById("f-usuario-id").value;
  const fechaDesde = document.getElementById("f-fecha-desde").value;
  const fechaHasta = document.getElementById("f-fecha-hasta").value;

  if (estado) parametros.set("estado", estado);
  if (tipoEvento) parametros.set("tipo_evento", tipoEvento);
  if (usuarioId) parametros.set("usuario_id", usuarioId);
  if (fechaDesde) parametros.set("fecha_desde", fechaDesde);
  if (fechaHasta) parametros.set("fecha_hasta", fechaHasta);
  return parametros.toString();
}

async function cargarBitacora() {
  const query = construirQuery();
  const { ok, data } = await apiFetch(`/api/bitacora${query ? "?" + query : ""}`);
  const cuerpo = document.getElementById("tabla-bitacora");

  if (!ok || !data.length) {
    cuerpo.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No hay eventos registrados.</td></tr>`;
    return;
  }

  cuerpo.innerHTML = data.map((e) => `
    <tr>
      <td>${new Date(e.fecha_hora).toLocaleString("es-GT")}</td>
      <td>${e.tipo_evento}</td>
      <td>${e.factura_id ? `<a href="factura.html?id=${e.factura_id}">${e.documento ?? "-"}</a>` : (e.documento ?? "-")}</td>
      <td>${e.usuario_id ?? "-"}</td>
      <td>${badgeEstado(e.estado)}</td>
      <td class="small">${e.resultado ?? "-"}</td>
    </tr>
  `).join("");
}

async function cargarMonitoreoRpa() {
  const cuerpo = document.getElementById("tabla-rpa");
  cuerpo.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-4">Cargando...</td></tr>`;

  const [{ ok: okFacturas, data: facturas }, { ok: okEventos, data: eventos }] = await Promise.all([
    apiFetch("/api/facturas"),
    apiFetch("/api/bitacora?tipo_evento=rpa"),
  ]);

  if (!okFacturas || !okEventos) {
    cuerpo.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-4">No se pudo cargar el monitoreo.</td></tr>`;
    return;
  }

  if (!facturas.length) {
    cuerpo.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-4">No hay facturas cargadas todavía.</td></tr>`;
    return;
  }

  // El listado de bitácora ya viene ordenado por fecha descendente,
  // así que la primera coincidencia por factura es la ejecución más reciente.
  const ultimaPorFactura = {};
  eventos.forEach((e) => {
    if (e.factura_id !== null && !(e.factura_id in ultimaPorFactura)) {
      ultimaPorFactura[e.factura_id] = e;
    }
  });

  cuerpo.innerHTML = facturas.map((f) => {
    const evento = ultimaPorFactura[f.id];
    const numeroExtra = f.numero_factura ? ` (No. extraído: ${f.numero_factura})` : "";
    return `
      <tr>
        <td><a href="factura.html?id=${f.id}">${f.nombre_archivo}</a>${numeroExtra}</td>
        <td>${badgeEstado(f.estado)}</td>
        <td>${evento ? new Date(evento.fecha_hora).toLocaleString("es-GT") : "Sin ejecutar"}</td>
        <td class="small">${evento ? `${badgeEstado(evento.estado)} ${evento.resultado ?? ""}` : "-"}</td>
      </tr>
    `;
  }).join("");
}
