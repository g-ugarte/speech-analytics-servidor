from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
import os

PATRONES_REPORTES = {
    "Detalle de Mensajes":  '//div[@class="glyph-icon flaticon-sent"]',
    "Detalle de Casos": '//div[@class="glyph-icon flaticon-news"]'
}


class Descargar_Reportes():
    def __init__(self, debug: bool = True) -> None : 
        with open(os.path.join(os.getcwd(), "res/descarga_chat.json"), 'r') as f:
            self.parametros = json.load(f)
        self.options = Options()

        self.options.add_argument(f"--user-data-dir={self.parametros['user-data-dir']}")
        self.options.add_argument(f"--profile-directory={self.parametros['profile-directory']}")
        self.options.add_argument("--enable-chrome-browser-cloud-management")
        self.options.add_argument("--no-sandbox")

        if debug:
            self.options.add_experimental_option('detach', True)

        self.service = Service(self.parametros["msedgedriver"])

        self.driver = webdriver.Edge(service=self.service, options=self.options)

    def descargar(self, patron: str):
        self.driver.get("https://interbank.s1gateway.com/app/")
        print("Página Accedida")
        sleep(3)

        login_btn = self.driver.find_element(By.ID, 'button_saml')
        login_btn.click()
        print("Loguear")

        while True:
            try:
                self.driver.switch_to.default_content()
                frame = self.driver.find_element(By.ID, 's1-gateway-mf')
                self.driver.switch_to.frame(frame)
                analytics_image = self.driver.find_element(By.XPATH, '//*[@alt="Métricas"]')
                hover = ActionChains(self.driver).move_to_element(analytics_image)
                hover.perform()
                break
            except:
                print("Intento: Acceder a frame de navegacion")
                sleep(2)


        analytics_anchor = self.driver.find_element(By.XPATH, '//*[@title="Analytics"]')
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(analytics_anchor)).click()


        self.original_tab = self.driver.current_window_handle
        WebDriverWait(self.driver, 5).until(EC.number_of_windows_to_be(2))

        for wh in self.driver.window_handles:
            if wh != self.original_tab:
                self.driver.switch_to.window(wh)
                break

        sleep(5)

        self.driver.find_element(By.XPATH, patron).click()

        while True:
            try:
                self.driver.find_element(By.ID, "fr-period").click()
                break
            except:
                print("Intento: Especificar rango")
                sleep(2)

        sleep(2)
        self.driver.find_element(By.XPATH, f'//li[@data-range-key="{self.parametros["range"]}"]').click()
        # driver.find_element(By.XPATH, '//li[@data-range-key="last2weeks"]').click()
        sleep(2)
        self.driver.find_element(By.XPATH, '//button[@onclick="executeReport()"]').click()
        while True:
            try:
                self.driver.find_element(By.XPATH, '//div[@class="dropdown action-btn report-tools"]').click()
                break
            except:
                print("Intento: Exportar Excel")
                sleep(2)
        sleep(2)
        self.driver.find_element(By.ID, "export-report").click()
    
    def validar(self):
        print("Status: Archivo descargando")
        path = f"{self.parametros['downloads']}/Detalle de Mensajes.xlsx"
        while not os.path.isfile(path):
            print("Status: Archivo descargando")
            sleep(5)
        self.driver.close()
        self.driver.quit()
        # self.driver.switch_to.window(self.original_tab)
        """ elements = self.driver.find_elements(by=By.CSS_SELECTOR, value="*")
        with open("html_content.txt", "w") as file:
            # Loop through each element and write its HTML content to the file
            for element in elements:
                html_content = element.get_attribute("outerHTML")
                file.write(html_content + "\n")  # Write HTML content to the file """


        """ frame_auth = self.driver.find_element(By.ID, 's1-gateway-mf')
        self.driver.switch_to.frame(frame_auth)
        elements = self.driver.find_elements(by=By.CSS_SELECTOR, value="*")
        with open("html_content.txt", "w", encoding='utf-8') as file:
            # Loop through each element and write its HTML content to the file
            for element in elements:
                html_content = element.get_attribute("outerHTML")
                file.write(html_content + "\n")  # Write HTML content to the file """

        return path

        # self.driver.find_element(By.XPATH, '//img[contains(@title, "@intercorp")]').click()
        # self.driver.close()

if __name__ == "__main__":
    obj = Descargar_Reportes()
    obj.descargar(PATRONES_REPORTES['Detalle de Mensajes'])
    ruta_excel = obj.validar()
    