from datetime import datetime
from html import escape

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.schemas.rpa import RegistroSimuladoRequest

router = APIRouter(prefix="/rpa-simulado", tags=["rpa-simulado"])

# Estado en memoria del último registro hecho por el robot RPA. Es solo para que
# esta página de demostración muestre evidencia visual; no es información de negocio.
_ultimo_registro: dict | None = None

CAMPOS = [
    ("numero_factura", "N° de factura"),
    ("nit", "NIT"),
    ("proveedor", "Proveedor"),
    ("fecha", "Fecha de factura"),
    ("subtotal", "Subtotal (Q)"),
    ("impuestos", "Impuestos / IVA (Q)"),
    ("total", "Total (Q)"),
    ("estado_ocr", "Estado OCR"),
]


def _valor(campo: str) -> str:
    if _ultimo_registro is None:
        return ""
    return escape(str(_ultimo_registro.get(campo, "")))


def _renderizar_formulario() -> str:
    campos_html = "".join(
        f"""
        <div class="campo">
          <label>{etiqueta}</label>
          <input id="{campo}" type="text" value="{_valor(campo)}">
        </div>
        """
        for campo, etiqueta in CAMPOS
    )

    info_ultima_actualizacion = (
        f'<p class="muted">Último registro: {escape(_ultimo_registro["actualizado_en"])}</p>'
        if _ultimo_registro
        else '<p class="muted">Todavía no se ha ejecutado ninguna automatización.</p>'
    )

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Sistema externo - Registro de facturas (simulado)</title>
<style>
  body {{ background: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; padding: 32px; }}
  .tarjeta {{ max-width: 760px; margin: 0 auto; background: #1e293b; border-radius: 12px; padding: 28px; }}
  h1 {{ font-size: 1rem; letter-spacing: 1px; text-transform: uppercase; color: #94a3b8; margin-bottom: 4px; }}
  .descripcion {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px; }}
  .muted {{ color: #64748b; font-size: 0.8rem; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
  .campo label {{ display: block; font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; margin-bottom: 6px; }}
  .campo input {{ width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 6px; padding: 10px; color: #e2e8f0; }}
  button {{ margin-top: 24px; background: #6366f1; color: white; border: none; border-radius: 6px; padding: 12px 24px; font-weight: 600; cursor: pointer; }}
  #resultado {{ margin-top: 16px; font-size: 0.9rem; }}
</style>
</head>
<body>
<div class="tarjeta">
  <h1>Formulario de registro simulado</h1>
  <p class="descripcion">
    Este formulario representa el sistema externo donde el robot RPA registra cada factura.
    Cuando se ejecuta una automatización, Selenium abre esta página en Chromium headless y
    completa los campos automáticamente con los datos ya extraídos/validados de la factura.
  </p>
  {info_ultima_actualizacion}
  <form id="formulario-registro">
    <div class="grid">
      {campos_html}
    </div>
    <button id="guardar" type="submit">Registrar en sistema</button>
  </form>
  <p id="resultado"></p>
</div>
<script>
document.getElementById("formulario-registro").addEventListener("submit", async function (evento) {{
    evento.preventDefault();
    const datos = {{
        numero_factura: document.getElementById("numero_factura").value,
        fecha: document.getElementById("fecha").value,
        proveedor: document.getElementById("proveedor").value,
        nit: document.getElementById("nit").value,
        subtotal: document.getElementById("subtotal").value,
        impuestos: document.getElementById("impuestos").value,
        total: document.getElementById("total").value,
        estado_ocr: document.getElementById("estado_ocr").value,
    }};
    const resultadoEl = document.getElementById("resultado");
    try {{
        const respuesta = await fetch("/rpa-simulado/registrar", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify(datos),
        }});
        const cuerpo = await respuesta.json();
        resultadoEl.textContent = respuesta.ok ? "Registro exitoso: " + cuerpo.detail : "Error: " + cuerpo.detail;
    }} catch (err) {{
        resultadoEl.textContent = "Error: " + err;
    }}
}});
</script>
</body>
</html>
"""


@router.get("/formulario", response_class=HTMLResponse)
def formulario():
    return _renderizar_formulario()


@router.post("/registrar")
def registrar(datos: RegistroSimuladoRequest):
    global _ultimo_registro
    _ultimo_registro = {**datos.model_dump(), "actualizado_en": datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")}
    return {"detail": f"Factura {datos.numero_factura} del proveedor {datos.proveedor} registrada correctamente"}
