import cv2
import fitz
import numpy as np


def pdf_a_imagenes(contenido_pdf: bytes, dpi: int = 200) -> list[np.ndarray]:
    documento = fitz.open(stream=contenido_pdf, filetype="pdf")
    zoom = dpi / 72
    matriz = fitz.Matrix(zoom, zoom)
    imagenes = []
    for pagina in documento:
        pix = pagina.get_pixmap(matrix=matriz, colorspace=fitz.csRGB)
        arreglo = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        imagenes.append(cv2.cvtColor(arreglo, cv2.COLOR_RGB2BGR))
    documento.close()
    return imagenes


def imagen_desde_bytes(contenido: bytes) -> np.ndarray:
    arreglo = np.frombuffer(contenido, dtype=np.uint8)
    imagen = cv2.imdecode(arreglo, cv2.IMREAD_COLOR)
    if imagen is None:
        raise ValueError("No se pudo decodificar la imagen")
    return imagen


def obtener_imagenes(contenido: bytes, nombre_archivo: str) -> list[np.ndarray]:
    if nombre_archivo.lower().endswith(".pdf"):
        return pdf_a_imagenes(contenido)
    return [imagen_desde_bytes(contenido)]


def preprocesar_imagen(imagen: np.ndarray) -> np.ndarray:
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    sin_ruido = cv2.fastNlMeansDenoising(gris, h=10)
    _, binarizada = cv2.threshold(sin_ruido, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binarizada


def corregir_inclinacion(imagen_binarizada: np.ndarray) -> np.ndarray:
    invertida = cv2.bitwise_not(imagen_binarizada)
    coordenadas = np.column_stack(np.where(invertida > 0))
    if coordenadas.size == 0:
        return imagen_binarizada

    angulo = cv2.minAreaRect(coordenadas)[-1]
    if angulo < -45:
        angulo = -(90 + angulo)
    else:
        angulo = -angulo

    # En texto disperso (pocas líneas, mucho espacio en blanco) minAreaRect puede
    # devolver ángulos poco confiables; solo se corrige una inclinación plausible
    # de una foto/escaneo real (unos pocos grados), nunca una rotación drástica.
    if abs(angulo) < 0.5 or abs(angulo) > 15:
        return imagen_binarizada

    alto, ancho = imagen_binarizada.shape[:2]
    centro = (ancho // 2, alto // 2)
    matriz_rotacion = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    return cv2.warpAffine(
        imagen_binarizada,
        matriz_rotacion,
        (ancho, alto),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )


def detectar_contorno_documento(imagen_binarizada: np.ndarray, margen: int = 15) -> tuple[int, int, int, int]:
    invertida = cv2.bitwise_not(imagen_binarizada)
    alto, ancho = imagen_binarizada.shape[:2]
    puntos = cv2.findNonZero(invertida)
    if puntos is None:
        return (0, 0, ancho, alto)

    x, y, w, h = cv2.boundingRect(puntos)
    x = max(x - margen, 0)
    y = max(y - margen, 0)
    w = min(w + 2 * margen, ancho - x)
    h = min(h + 2 * margen, alto - y)
    return (x, y, w, h)


def recortar_documento(imagen_binarizada: np.ndarray) -> np.ndarray:
    x, y, ancho, alto = detectar_contorno_documento(imagen_binarizada)
    if ancho == 0 or alto == 0:
        return imagen_binarizada
    return imagen_binarizada[y : y + alto, x : x + ancho]


def preparar_para_ocr(contenido: bytes, nombre_archivo: str) -> list[np.ndarray]:
    paginas_listas = []
    for imagen in obtener_imagenes(contenido, nombre_archivo):
        binarizada = preprocesar_imagen(imagen)
        enderezada = corregir_inclinacion(binarizada)
        recortada = recortar_documento(enderezada)
        paginas_listas.append(recortada)
    return paginas_listas
