from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.schemas.rpa import RegistroSimuladoRequest

router = APIRouter(prefix="/rpa-simulado", tags=["rpa-simulado"])

FORMULARIO_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Sistema externo - Registro de facturas</title>
</head>
<body>
<h1>Registro de facturas (sistema externo simulado)</h1>
<form id="formulario-registro">
  <label>No. Factura</label>
  <input id="numero_factura" type="text">
  <label>Fecha</label>
  <input id="fecha" type="text">
  <label>Proveedor</label>
  <input id="proveedor" type="text">
  <label>NIT</label>
  <input id="nit" type="text">
  <label>Subtotal</label>
  <input id="subtotal" type="text">
  <label>Impuestos</label>
  <input id="impuestos" type="text">
  <label>Total</label>
  <input id="total" type="text">
  <button id="guardar" type="submit">Guardar</button>
</form>
<p id="resultado"></p>
<script>
document.getElementById("formulario-registro").addEventListener("submit", async function (evento) {
    evento.preventDefault();
    const datos = {
        numero_factura: document.getElementById("numero_factura").value,
        fecha: document.getElementById("fecha").value,
        proveedor: document.getElementById("proveedor").value,
        nit: document.getElementById("nit").value,
        subtotal: document.getElementById("subtotal").value,
        impuestos: document.getElementById("impuestos").value,
        total: document.getElementById("total").value,
    };
    const resultadoEl = document.getElementById("resultado");
    try {
        const respuesta = await fetch("/rpa-simulado/registrar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos),
        });
        const cuerpo = await respuesta.json();
        resultadoEl.textContent = respuesta.ok ? "Registro exitoso: " + cuerpo.detail : "Error: " + cuerpo.detail;
    } catch (err) {
        resultadoEl.textContent = "Error: " + err;
    }
});
</script>
</body>
</html>
"""


@router.get("/formulario", response_class=HTMLResponse)
def formulario():
    return FORMULARIO_HTML


@router.post("/registrar")
def registrar(datos: RegistroSimuladoRequest):
    return {"detail": f"Factura {datos.numero_factura} del proveedor {datos.proveedor} registrada correctamente"}
