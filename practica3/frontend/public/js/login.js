if (obtenerToken()) {
  window.location.href = "index.html";
}

document.getElementById("form-login").addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const errorEl = document.getElementById("login-error");
  errorEl.classList.add("d-none");

  try {
    const respuesta = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username: email, password }),
    });

    if (!respuesta.ok) {
      throw new Error("Correo o contraseña incorrectos");
    }

    const datos = await respuesta.json();
    guardarToken(datos.access_token);
    window.location.href = "index.html";
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.remove("d-none");
  }
});
