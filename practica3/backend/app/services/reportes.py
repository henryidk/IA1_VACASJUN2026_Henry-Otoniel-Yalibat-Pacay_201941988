import io
import json
from datetime import datetime
from decimal import Decimal

from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy.orm import Session

from app.models.factura import Factura
from app.models.reporte import Reporte

ENCABEZADO = ["No. Factura", "Fecha", "Proveedor", "Subtotal", "Impuestos", "Total", "Estado"]


def _filas_facturas(facturas: list[Factura]) -> list[list[str]]:
    filas = [ENCABEZADO]
    total_general = Decimal("0")
    for factura in facturas:
        proveedor_nombre = factura.proveedor.nombre if factura.proveedor else "-"
        filas.append(
            [
                factura.numero_factura or "-",
                factura.fecha.strftime("%d/%m/%Y") if factura.fecha else "-",
                proveedor_nombre,
                f"{factura.subtotal:.2f}" if factura.subtotal is not None else "-",
                f"{factura.impuestos:.2f}" if factura.impuestos is not None else "-",
                f"{factura.total:.2f}" if factura.total is not None else "-",
                factura.estado,
            ]
        )
        if factura.total is not None:
            total_general += factura.total
    filas.append(["", "", "", "", "", f"{total_general:.2f}", "TOTAL"])
    return filas


def generar_reporte_pdf(facturas: list[Factura]) -> bytes:
    buffer = io.BytesIO()
    documento = SimpleDocTemplate(buffer, pagesize=letter, title="Reporte de facturas - SmartInvoice")
    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph("Reporte administrativo de facturas - SmartInvoice", estilos["Title"]),
        Paragraph(f"Generado el {datetime.utcnow().strftime('%d/%m/%Y %H:%M')} UTC", estilos["Normal"]),
        Spacer(1, 12),
    ]

    tabla = Table(_filas_facturas(facturas), repeatRows=1)
    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#ecf0f1")),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ]
        )
    )
    elementos.append(tabla)
    documento.build(elementos)
    return buffer.getvalue()


def generar_reporte_excel(facturas: list[Factura]) -> bytes:
    libro = Workbook()
    hoja = libro.active
    hoja.title = "Facturas"

    for fila in _filas_facturas(facturas):
        hoja.append(fila)

    for celda in hoja[1]:
        celda.font = Font(bold=True)

    for columna in hoja.columns:
        ancho = max((len(str(celda.value)) for celda in columna if celda.value is not None), default=10)
        hoja.column_dimensions[columna[0].column_letter].width = ancho + 2

    buffer = io.BytesIO()
    libro.save(buffer)
    return buffer.getvalue()


def registrar_reporte(db: Session, usuario_id: int, formato: str, filtros: dict) -> Reporte:
    reporte = Reporte(usuario_id=usuario_id, formato=formato, filtros=json.dumps(filtros))
    db.add(reporte)
    db.commit()
    db.refresh(reporte)
    return reporte
