"""
Automatización de ingesta mensual de BCRA (Cheques Deudores MFT)
Diseñado utilizando Selenium WebDriver.
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class BCRADownloader:
    def __init__(self, download_dir: str):
        self.download_dir = os.path.abspath(download_dir)
        self.url = "https://www3.bcra.gob.ar/ChequesDeudoresMFT/Deudores"
        
        chrome_options = Options()
        # Preferencias para descarga silenciosa/automática
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0
        }
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def authenticate(self, user, password):
        # Placeholder for authentication if eventually required by BCRA in the future
        pass

    def download_monthly_data(self):
        print(f"[INFO] Navegando a {self.url}...")
        self.driver.get(self.url)
        
        try:
            # Esperar a que la tabla de archivos cargue
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-hover tbody tr td a"))
            )
            
            # Obtener todos los enlaces de archivos
            file_links = self.driver.find_elements(By.CSS_SELECTOR, "table.table-hover tbody tr td a")
            print(f"[OK] Se encontraron {len(file_links)} archivos listados.")
            
            # Iterar sobre los links encontrados. 
            # Note: The elements get stale if page reloads, so we might need to fetch them repeatedly if the page refreshes,
            # but since the download is an AJAX post -> hidden form submit, the page likely does not hard-refresh.
            # We will process the first 2 files for demonstration to prevent endless loop.
            
            for i in range(len(file_links)):
                # Fetch elements again to avoid stale DOM exceptions
                links = self.driver.find_elements(By.CSS_SELECTOR, "table.table-hover tbody tr td a")
                link = links[i]
                
                filename = link.text.strip()
                print(f"[{i+1}] Iniciando descarga de: {filename}")
                
                # Clickeamos el link para abrir el modal ("Acepto los términos y condiciones")
                self.driver.execute_script("arguments[0].scrollIntoView();", link)
                time.sleep(1)
                link.click()
                
                # Esperamos que aparezca el botón "Aceptar" del SweetAlert modal
                btn_aceptar = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar') or contains(@class, 'swal2-confirm')]"))
                )
                
                print(f"  -> Aceptando declaración jurada para {filename}...")
                btn_aceptar.click()
                
                # Esperamos a que la petición AJAX termine y empiece la descarga.
                # Se introduce una pausa conservadora.
                time.sleep(15) 
                
            print("[OK] Ciclo de descarga iterativa finalizado.")
            
        except Exception as e:
            print(f"[ERROR] Falló la descarga de archivos: {e}")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    import sys
    # Se obtienen credenciales de un archivo o ambiente gestionado
    downloader = BCRADownloader(download_dir="../../data/raw/")
    downloader.download_monthly_data()
    downloader.close()
