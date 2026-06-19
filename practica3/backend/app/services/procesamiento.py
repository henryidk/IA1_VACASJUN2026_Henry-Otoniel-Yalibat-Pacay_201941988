import logging

from app.core.database import SessionLocal
from app.models.bitacora import TipoEvento
from app.models.factura import EstadoFactura, Factura
from app.services.bitacora import registrar_evento
from app.services.cv import preparar_para_ocr
from app.services.ocr import extraer_campos, extraer_texto

logger = logging.getLogger("smartinvoice")


def procesar_factura(factura_id: int, contenido: bytes, nombre_archivo: str, usuario_id: int) -> None:
    db = SessionLocal()
    try:
        factura = db.query(Factura).filter(Factura.id == factura_id).first()
        if factura is None:
            return

        try:
            paginas = preparar_para_ocr(contenido, nombre_archivo)
            texto = "\n".join(extraer_texto(pagina) for pagina in paginas)
            campos = extraer_campos(texto)

            factura.texto_ocr = texto
            factura.numero_factura = campos["numero_factura"]
            factura.fecha = campos["fecha"]
            factura.subtotal = campos["subtotal"]
            factura.impuestos = campos["impuestos"]
            factura.total = campos["total"]
            db.commit()

            registrar_evento(
                db,
                factura_id=factura.id,
                usuario_id=usuario_id,
                tipo_evento=TipoEvento.OCR,
                estado=factura.estado,
                documento=factura.nombre_archivo,
                resultado="Texto extraído y campos parseados correctamente",
            )
        except Exception as exc:
            logger.exception("Error procesando OCR de la factura %s", factura_id)
            factura.estado = EstadoFactura.ERROR
            db.commit()
            registrar_evento(
                db,
                factura_id=factura.id,
                usuario_id=usuario_id,
                tipo_evento=TipoEvento.OCR,
                estado=EstadoFactura.ERROR,
                documento=factura.nombre_archivo,
                resultado=f"Error durante el procesamiento OCR: {exc}",
            )
    finally:
        db.close()
