from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.core.config import settings
from app.models.factura import Factura

URL_FORMULARIO_SIMULADO = f"http://localhost:{settings.port}/rpa-simulado/formulario"


def _crear_driver() -> webdriver.Chrome:
    opciones = Options()
    opciones.binary_location = "/usr/bin/chromium"
    opciones.add_argument("--headless=new")
    opciones.add_argument("--single-process")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    opciones.add_argument("--disable-extensions")
    opciones.add_argument("--blink-settings=imagesEnabled=false")
    opciones.add_argument("--window-size=800,600")
    return webdriver.Chrome(options=opciones)


def registrar_factura_en_formulario(factura: Factura) -> dict:
    proveedor_nombre = factura.proveedor.nombre if factura.proveedor else ""
    proveedor_nit = factura.proveedor.nit if factura.proveedor else ""

    campos_enviados = {
        "numero_factura": factura.numero_factura or "(vacío)",
        "fecha": factura.fecha.isoformat() if factura.fecha else "(vacío)",
        "proveedor": proveedor_nombre or "(vacío)",
        "nit": proveedor_nit or "(vacío)",
        "subtotal": str(factura.subtotal) if factura.subtotal is not None else "(vacío)",
        "impuestos": str(factura.impuestos) if factura.impuestos is not None else "(vacío)",
        "total": str(factura.total) if factura.total is not None else "(vacío)",
        "estado_ocr": factura.estado,
    }

    driver = _crear_driver()
    try:
        driver.get(URL_FORMULARIO_SIMULADO)

        driver.find_element(By.ID, "numero_factura").send_keys(factura.numero_factura or "")
        driver.find_element(By.ID, "fecha").send_keys(factura.fecha.isoformat() if factura.fecha else "")
        driver.find_element(By.ID, "proveedor").send_keys(proveedor_nombre)
        driver.find_element(By.ID, "nit").send_keys(proveedor_nit)
        driver.find_element(By.ID, "subtotal").send_keys(str(factura.subtotal) if factura.subtotal is not None else "")
        driver.find_element(By.ID, "impuestos").send_keys(str(factura.impuestos) if factura.impuestos is not None else "")
        driver.find_element(By.ID, "total").send_keys(str(factura.total) if factura.total is not None else "")
        driver.find_element(By.ID, "estado_ocr").send_keys(factura.estado)
        driver.find_element(By.ID, "guardar").click()

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "resultado"), "")
        )
        confirmacion = driver.find_element(By.ID, "resultado").text
        if confirmacion.startswith("Error"):
            raise RuntimeError(confirmacion)
        return {"confirmacion": confirmacion, "campos_enviados": campos_enviados}
    finally:
        driver.quit()
