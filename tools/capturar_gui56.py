"""Prueba de interfaz y capturas reales; requiere Playwright y Chromium."""
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
CAPTURAS = ROOT / "entregas/semanas5y6/capturas"


def ejecutar():
    servidor = subprocess.Popen([sys.executable, "-m", "src.gui", "--web", "--port", "8551"], cwd=ROOT)
    try:
        for _ in range(60):
            try:
                urlopen("http://127.0.0.1:8551", timeout=1).close()
                break
            except OSError:
                time.sleep(1)
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chromium", headless=True)
            page = browser.new_page(viewport={"width": 1400, "height": 1100}, device_scale_factor=1.5)
            page.goto("http://127.0.0.1:8551")
            page.wait_for_timeout(8000)
            page.locator("flt-semantics-placeholder").dispatch_event("click")
            page.wait_for_timeout(2000)
            def escribir(label, value):
                campo = page.get_by_role("textbox", name=label, exact=True)
                campo.click()
                page.wait_for_timeout(500)
                page.keyboard.press("Meta+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(value, delay=70)
                page.wait_for_timeout(400)
                page.keyboard.press("Tab")
                page.wait_for_timeout(600)

            page.screenshot(path=str(CAPTURAS / "01_catalogo.png"), full_page=True)
            for label, value in [("Código", "L002"), ("Título", "Programación en Python"),
                                 ("Autor", "Edisson Carchi"), ("ISBN", "DEMO-002"),
                                 ("Precio ($)", "25.50"), ("Stock", "5")]:
                escribir(label, value)
            page.get_by_role("button", name="Agregar", exact=True).click()
            page.wait_for_timeout(700)
            print(page.locator("body").aria_snapshot())
            page.get_by_text("Producto L002 agregado correctamente.", exact=True).wait_for()
            page.screenshot(path=str(CAPTURAS / "02_agregar.png"), full_page=True)
            escribir("Buscar por código o título", "L002")
            expect(page.locator("body")).to_contain_text("1 resultados · 3 productos en el catálogo")
            page.screenshot(path=str(CAPTURAS / "03_buscar.png"), full_page=True)
            page.get_by_role("button", name="Editar L002", exact=True).click()
            escribir("Precio ($)", "30.00")
            escribir("Stock", "9")
            page.get_by_role("button", name="Actualizar", exact=True).click()
            page.get_by_text("Producto L002 actualizado correctamente.", exact=True).wait_for()
            expect(page.locator("body")).to_contain_text("$30.00")
            page.screenshot(path=str(CAPTURAS / "04_actualizar.png"), full_page=True)
            page.get_by_role("button", name="Editar L002", exact=True).click()
            page.get_by_role("button", name="Eliminar", exact=True).click()
            page.get_by_text("Producto L002 eliminado correctamente.", exact=True).wait_for()
            escribir("Buscar por código o título", "")
            expect(page.locator("body")).to_contain_text("2 resultados · 2 productos en el catálogo")
            page.screenshot(path=str(CAPTURAS / "05_eliminar.png"), full_page=True)
            for label, value in [("Código", " l001 "), ("Título", "Duplicado"),
                                 ("Autor", "Autor"), ("ISBN", "DEMO"),
                                 ("Precio ($)", "12"), ("Stock", "2")]:
                escribir(label, value)
            page.get_by_role("button", name="Agregar", exact=True).click()
            page.get_by_text("El código L001 ya existe", exact=True).wait_for()
            page.screenshot(path=str(CAPTURAS / "06_duplicado.png"), full_page=True)
            escribir("Código", "L003")
            escribir("Stock", "-1")
            page.get_by_role("button", name="Agregar", exact=True).click()
            page.get_by_text("El stock debe ser un entero no negativo", exact=True).wait_for()
            page.screenshot(path=str(CAPTURAS / "07_validacion.png"), full_page=True)
            print("CRUD gráfico, búsqueda, duplicados y validación: OK")
            browser.close()
    finally:
        servidor.terminate()
        servidor.wait(timeout=15)


if __name__ == "__main__":
    ejecutar()
