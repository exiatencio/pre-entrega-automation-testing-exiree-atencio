# Preentrega: automatización QA de SauceDemo

Autora: Exiree Atencio.

Proyecto de práctica para automatizar login, catálogo y carrito de https://www.saucedemo.com/ con Python, Selenium WebDriver y Pytest.

## Requisitos e instalación

- Python 3.10 o superior.
- Google Chrome instalado.
- Acceso a Internet: Selenium Manager administra y descarga el controlador compatible cuando hace falta.
- Git para el control de versiones y una cuenta de GitHub para entregar.

Desde esta carpeta, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No es necesario activar el entorno virtual.

## Ejecutar las pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Las pruebas corren en Chrome sin ventana por defecto. Para ver el navegador:

```powershell
.\.venv\Scripts\python.exe -m pytest --headed
```

Para ejecutar solamente un caso:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py::test_login_exitoso
```

La configuración genera `reports/reporte.html`, con los resultados y los registros de cada caso, y `reports/ejecucion.log`. También se puede especificar el reporte:

```powershell
.\.venv\Scripts\python.exe -m pytest -v --html=reports/reporte.html --self-contained-html
```

## Casos de prueba

| Caso | Validaciones |
| --- | --- |
| Login exitoso | Credenciales públicas `standard_user` / `secret_sauce`, ruta `/inventory.html`, título `Swag Labs` y encabezado `Products`. |
| Catálogo | Al menos un producto visible, nombre y precio del primero en el log, menú, filtro y acceso al carrito. |
| Carrito | Carrito inicialmente vacío, agregado del primer producto, contador igual a 1, ruta `/cart.html`, nombre, precio y cantidad del producto. |

Cada prueba inicia y cierra su propio navegador. Ninguna depende de que se ejecute otra antes. Las funciones auxiliares usan esperas explícitas de hasta 15 segundos; no se usan pausas fijas ni esperas implícitas.

## Organización

```text
tests/
  conftest.py          # Navegador independiente y evidencias de fallos
  test_saucedemo.py    # Casos y validaciones
utils/
  saucedemo.py         # Login y acciones con esperas explícitas
reports/
  capturas/           # PNG automáticos cuando falla un caso
  reporte.html        # Resultado generado por pytest-html
  ejecucion.log       # Registro generado por Pytest
pytest.ini
requirements.txt
```

Las capturas se incorporan al reporte HTML y se guardan como PNG. Solo se generan al fallar una prueba con un navegador disponible; si Chrome no puede iniciarse, el error queda en el reporte y los logs. Los PNG están ignorados por Git para evitar subir evidencias de ejecuciones anteriores; se pueden adjuntar manualmente a la entrega si son necesarios. No se necesita `datos/` porque este proyecto no utiliza archivos de datos externos.

## Validación local

Las tres pruebas se ejecutaron contra el sitio real en Chrome y finalizaron correctamente: **3 passed**. El reporte y el log incluidos corresponden a esa ejecución. Las versiones de las dependencias principales están fijadas a las utilizadas en esta validación.

