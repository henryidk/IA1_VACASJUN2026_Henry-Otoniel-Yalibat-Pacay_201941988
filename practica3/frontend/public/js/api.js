// En local (Docker Compose) usa el backend local; en producción, el de Render.
// Se puede forzar otra URL (debug) con: localStorage.setItem("api_base_url_override", "...")
const API_BASE_URL = localStorage.getItem("api_base_url_override")
  || (["localhost", "127.0.0.1"].includes(window.location.hostname)
    ? "http://localhost:8000"
    : "https://smartinvoice-backend-5q8h.onrender.com");

const CLAVE_TOKEN = "smartinvoice_token";

function obtenerToken() {
  return localStorage.getItem(CLAVE_TOKEN);
}

function guardarToken(token) {
  localStorage.setItem(CLAVE_TOKEN, token);
}

function eliminarToken() {
  localStorage.removeItem(CLAVE_TOKEN);
}

function cerrarSesion() {
  eliminarToken();
  window.location.href = "login.html";
}

async function apiFetch(ruta, opciones = {}) {
  const token = obtenerToken();
  const headers = { ...(opciones.headers || {}) };
  const sinContentTypeAutomatico = opciones.body instanceof URLSearchParams || opciones.body instanceof FormData;
  if (!sinContentTypeAutomatico) {
    headers["Content-Type"] = "application/json";
  }
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const respuesta = await fetch(`${API_BASE_URL}${ruta}`, { ...opciones, headers });

  if (respuesta.status === 401) {
    cerrarSesion();
    throw new Error("Sesión expirada, inicia sesión de nuevo");
  }

  const cuerpo = respuesta.status === 204 ? null : await respuesta.json().catch(() => null);
  return { ok: respuesta.ok, status: respuesta.status, data: cuerpo };
}
