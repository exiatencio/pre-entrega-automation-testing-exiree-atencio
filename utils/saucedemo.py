"""Acciones compartidas con esperas explícitas, sin pausas fijas."""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com/"
TIMEOUT = 15
logger = logging.getLogger(__name__)


def visible(driver, locator):
    """Espera hasta que el elemento esté visible."""
    return WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located(locator))


def click(driver, locator):
    """Espera hasta que se pueda hacer clic en el elemento."""
    WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(locator)).click()


def login(driver):
    """Ingresa con las credenciales públicas del sitio de práctica."""
    driver.get(BASE_URL)
    visible(driver, (By.ID, "user-name")).send_keys("standard_user")
    visible(driver, (By.ID, "password")).send_keys("secret_sauce")
    click(driver, (By.ID, "login-button"))
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/inventory.html"))
    visible(driver, (By.CSS_SELECTOR, ".inventory_list"))
    logger.info("Login completado; URL: %s", driver.current_url)


def productos_visibles(driver):
    """Devuelve los productos cuando todos los elementos encontrados son visibles."""
    return WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".inventory_item"))
    )
