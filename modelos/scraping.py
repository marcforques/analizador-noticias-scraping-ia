from pathlib import Path
import tempfile
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_CHROMEDRIVER = RUTA_PROYECTO / "chromedriver.exe"


def obtener_titular(noticia):
    texto_noticia = noticia.get_attribute("textContent") or ""
    texto_noticia = " ".join(texto_noticia.split())

    if 35 < len(texto_noticia) < 180:
        return texto_noticia

    enlaces = noticia.find_elements(By.XPATH, ".//a")

    for enlace in enlaces:
        texto = enlace.get_attribute("textContent") or ""
        texto = " ".join(texto.split())
        if 35 < len(texto) < 180:
            return texto

    return ""


def iniciar_driver():
    perfil_temporal = tempfile.mkdtemp(prefix="chrome-selenium-", dir="C:\\tmp")

    opciones = ChromeOptions()
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    opciones.add_argument("--disable-crash-reporter")
    opciones.add_argument("--disable-extensions")
    opciones.add_argument(f"--user-data-dir={perfil_temporal}")
    opciones.add_argument("--window-size=1366,900")

    if RUTA_CHROMEDRIVER.exists():
        driver = webdriver.Chrome(
        service=ChromeService(str(RUTA_CHROMEDRIVER)),
        options=opciones
    )
    else:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=opciones
        )

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)
    return driver


def scraping_noticias():
    driver = None

    noticias = []

    try:
        driver = iniciar_driver()
        driver.get("https://www.eleconomista.es/ultimas-noticias/")
        time.sleep(5)

        # Pulsamos el boton de aceptar cookies si aparece
        boton_aceptar = driver.find_elements(
            By.XPATH, "//a[@data-mrf-role='userAgreeToAll']"
        )

        if boton_aceptar:
            driver.execute_script("arguments[0].click();", boton_aceptar[0])
            time.sleep(2)

        # Bajamos un poco hasta la zona donde aparecen las noticias
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(2)

        # Buscamos los titulares
        noticias_web = driver.find_elements(By.XPATH, "//h2[contains(@class, 'h3')]")
        print(f"Titulares encontrados: {len(noticias_web)}")

        for noticia_web in noticias_web:
            titular = obtener_titular(noticia_web)

            if titular and {"titular": titular} not in noticias:
                noticias.append({"titular": titular})

            if len(noticias) == 15:
                break

        if not noticias:
            noticias_web = driver.find_elements(By.XPATH, "//h2 | //h3")
            print(f"Segundo intento con h2/h3 encontrados: {len(noticias_web)}")

            for noticia_web in noticias_web:
                titular = obtener_titular(noticia_web)

                if titular and {"titular": titular} not in noticias:
                    noticias.append({"titular": titular})

                if len(noticias) == 15:
                    break

        print("\nTitulares extraidos:")
        if noticias:
            for idx, noticia in enumerate(noticias, start=1):
                print(f"{idx}. {noticia['titular']}")
        else:
            print("No se encontraron titulares.")

    except WebDriverException as e:
        print(f"Error al abrir Chrome o cargar la pagina: {e}")

    except Exception as e:
        print(f"Error detectado durante el scraping: {e}")

    finally:
        if driver:
            time.sleep(3)
            driver.quit()

    return noticias
