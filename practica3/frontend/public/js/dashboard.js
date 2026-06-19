document.addEventListener("DOMContentLoaded", cargarUsuario);

document.getElementById("btn-logout").addEventListener("click", cerrarSesion);

async function cargarUsuario() {
  const { ok, data } = await apiFetch("/api/auth/me");
  if (ok) {
    document.getElementById("usuario-nombre").textContent = data.nombre;
  }
}
