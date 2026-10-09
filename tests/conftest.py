"""Cada prueba usa un navegador nuevo y guarda evidencia si falla."""

import logging
import re
from datetime import datetime
from pathlib import Path

import pytest
import pytest_html
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

ROOT = Path(__file__).resolve().parents[1]
CAPTURAS = ROOT / "reports" / "capturas"
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Mostrar el navegador durante las pruebas")


@pytest.fixture
def driver(request):
    """El alcance por función evita compartir sesión o carrito entre pruebas."""
    options = webdriver.ChromeOptions()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)
    logger.info("Navegador iniciado: %s", request.node.name)
    try:
        yield browser
    finally:
        browser.quit()
        logger.info("Navegador cerrado: %s", request.node.name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura fallos de preparación o ejecución mientras el navegador está abierto."""
    outcome = yield
    report = outcome.get_result()
    if report.failed and report.when in ("setup", "call"):
        browser = item.funcargs.get("driver")
        if browser is None:
            logger.error("Fallo antes de disponer de navegador: %s", item.nodeid)
            return
        CAPTURAS.mkdir(parents=True, exist_ok=True)
        nombre = re.sub(r"[^a-zA-Z0-9_-]", "_", item.nodeid)
        destino = CAPTURAS / f"{nombre}_{datetime.now():%Y%m%d_%H%M%S_%f}.png"
        try:
            captura = browser.get_screenshot_as_base64()
            import base64
            destino.write_bytes(base64.b64decode(captura))
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.png(captura, name="Captura del fallo"))
            report.extras = extras
            logger.error("Fallo en %s; captura: %s", item.nodeid, destino)
        except WebDriverException:
            logger.exception("No se pudo capturar el navegador")
