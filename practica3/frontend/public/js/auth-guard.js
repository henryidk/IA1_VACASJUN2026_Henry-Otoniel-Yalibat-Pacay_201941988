// Debe cargarse después de api.js en cada página protegida.
if (!obtenerToken()) {
  window.location.href = "login.html";
}
