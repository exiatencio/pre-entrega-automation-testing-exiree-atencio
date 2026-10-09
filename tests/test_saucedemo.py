"""Tres casos independientes que cubren las consignas de la preentrega."""

import logging
import re
from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.saucedemo import TIMEOUT, click, login, productos_visibles, visible

logger = logging.getLogger(__name__)


def test_login_exitoso(driver):
    """Valida la redirección, el título del documento y el encabezado del inventario."""
    login(driver)
    assert urlparse(driver.current_url).path == "/inventory.html", "No se abrió el inventario"
    assert driver.title == "Swag Labs", "Título del documento incorrecto"
    assert visible(driver, (By.CSS_SELECTOR, ".title")).text == "Products"


def test_catalogo_y_elementos_de_interfaz(driver):
    """Verifica productos, menú y filtro; registra nombre y precio del primero."""
    login(driver)
    assert driver.title == "Swag Labs"
    assert visible(driver, (By.CSS_SELECTOR, ".title")).text == "Products"
    productos = productos_visibles(driver)
    assert len(productos) >= 1, "El catálogo no contiene productos visibles"
    nombre = productos[0].find_element(By.CSS_SELECTOR, ".inventory_item_name").text
    precio = productos[0].find_element(By.CSS_SELECTOR, ".inventory_item_price").text
    assert nombre.strip(), "El primer producto no tiene nombre"
    assert re.fullmatch(r"\$\d+\.\d{2}", precio), f"Precio inválido: {precio}"
    logger.info("Primer producto: %s | Precio: %s", nombre, precio)
    assert visible(driver, (By.ID, "react-burger-menu-btn")).is_enabled()
    assert visible(driver, (By.CSS_SELECTOR, ".product_sort_container")).is_enabled()
    assert visible(driver, (By.CSS_SELECTOR, ".shopping_cart_link")).is_displayed()


def test_agregar_primer_producto_al_carrito(driver):
    """Comprueba contador, nombre, precio y cantidad del producto agregado."""
    login(driver)
    assert not driver.find_elements(By.CSS_SELECTOR, ".shopping_cart_badge"), "El carrito debe iniciar vacío"
    primero = productos_visibles(driver)[0]
    nombre = primero.find_element(By.CSS_SELECTOR, ".inventory_item_name").text
    precio = primero.find_element(By.CSS_SELECTOR, ".inventory_item_price").text
    primero.find_element(By.CSS_SELECTOR, "button").click()
    WebDriverWait(driver, TIMEOUT).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".shopping_cart_badge"), "1")
    )
    assert visible(driver, (By.CSS_SELECTOR, ".shopping_cart_badge")).text == "1"
    click(driver, (By.CSS_SELECTOR, ".shopping_cart_link"))
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/cart.html"))
    assert urlparse(driver.current_url).path == "/cart.html"
    item = visible(driver, (By.CSS_SELECTOR, ".cart_item"))
    assert len(driver.find_elements(By.CSS_SELECTOR, ".cart_item")) == 1
    assert item.find_element(By.CSS_SELECTOR, ".inventory_item_name").text == nombre
    assert item.find_element(By.CSS_SELECTOR, ".inventory_item_price").text == precio
    assert item.find_element(By.CSS_SELECTOR, ".cart_quantity").text == "1"
    logger.info("Producto verificado en carrito: %s | %s | Cantidad: 1", nombre, precio)
