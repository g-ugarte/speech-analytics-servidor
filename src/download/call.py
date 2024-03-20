from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from glob import glob

import json

class Descargar_Llamada():
    def __init__(self, debug: bool = True) -> None : 
        self.options = Options()

        with open(os.path.join(os.getcwd(), "res/descarga_llamada.json")) as f:
            self.parametros = json.load(f)

        self.options.add_argument(f"--user-data-dir={self.parametros['user_data_dir']}")
        self.options.add_argument(f"--profile-directory={self.parametros['profile_directory']}")
        self.options.add_argument("--enable-chrome-browser-cloud-management")
        self.options.add_argument("--no-sandbox")

        if debug:
            self.options.add_experimental_option('detach', True)

        self.service = Service(self.parametros['edge_driver'])

        self.driver = webdriver.Edge(service=self.service, options=self.options)

    def descargar(self, llamada_id: str="e48744dd-d150-4b6e-b519-c72c055ea6a7"):
        self.driver.get(f"https://apps.mypurecloud.com/directory/#/analytics/interactions/{llamada_id}/admin?tabId={self.parametros['admin_tab_id']}")

        while True:
            try:
                frame_ui = self.driver.find_element(By.XPATH, '//iframe[@title="Analytics UI"]')
                self.driver.switch_to.frame(frame_ui)
                break
            except:
                print(f"[{llamada_id}]:Intento: Acceder a frame de UI")
                sleep(2)

        while True:
            try:
                frame_coordinar = self.driver.find_element(By.TAG_NAME, 'iframe')
                self.driver.switch_to.frame(frame_coordinar)
                break
            except:
                print(f"[{llamada_id}]:Intento: Acceder a frame de descargas")
                sleep(2)

        while True:
            try:
                btn = self.driver.find_element(By.XPATH, '//button[@data-bind="click: $data.editDownload"]')
                sleep(1)
                btn.click()
                break
            except:
                print(f"[{llamada_id}]:Intento: Acceso a boton de descarga")
                sleep(2)


        sel = Select(self.driver.find_element(By.XPATH, '//select[@class="form-control input-sm format-select-options"]'))
        sel.select_by_value("mp3")
        sleep(1)

        btn_descargar = self.driver.find_element(By.XPATH, '//button[@class="btn btn-default recording-download-button"]')
        btn_descargar.click()

    def validar(self, llamada_id: str):
        print("Status: Archivo descargando")
        path = f'{self.parametros["download_directory"]}/Llamada1-{llamada_id}.mp3'
        while not os.path.isfile(path):
            print("Status: Archivo descargando")
            sleep(5)
        self.driver.quit()
        return path

import os.path
        
if __name__ == '__main__':
    UUIDS = [
        "29af59bb-657c-4bea-b2dc-51f884f14c7a",
# '1773ac6e-ae5b-4b6f-82a0-0ea9e6af4b0a',
# '98e26d30-717d-4051-927d-0fa3689cd63f',
# 'd6bdd89f-c1a8-43cf-a1b7-21c130425f94',
# 'ec933740-9b2e-4029-9e90-09ef2005363f',
# '1d9b0b9f-59fb-4a16-8e45-7b1f7be1ae80',
# 'afc1c460-1253-4487-979e-54cab3a849ee',
# '7baf990a-647d-4b3f-a02a-813335f82b6c',
# '93b3d1d2-683d-4223-b803-73dd19277ed3',
# 'e2c20319-d8b6-486e-a9f3-9007a48065a6',
# '3af6f178-401b-42ef-bed8-3df177842cf7',
# '7c2bfc93-09d4-473a-9a69-4604a67c3f55',
# '569aa7f2-acf3-4be3-a493-1ad960d7d895',
# 'b36054c4-3d4b-43ae-aa95-11578604795c',
# 'e72aba96-55a1-4083-bc1e-4b21275d25ca',
# '8c2750d3-055a-47e1-857d-5094535bb56f',
# 'b5c9feaa-0984-469f-a4ac-895b4b2945b3',
# '7392eaf8-7294-413c-9af6-f5a0b4b8d733',
# '98d9f745-e952-4870-82fe-ca6638fc2230',
# 'b33e621f-66de-4386-9850-65950ed9ff69',
# 'fb9eee3e-7dde-406d-9f35-02f71a49b412',
]
    a = Descargar_Llamada()
    for id, uuid in enumerate(UUIDS):
        a.descargar(llamada_id=uuid)
        a.validar(llamada_id=uuid)
        # path = f"C:/Users/bp3285/Downloads/Speech-Analytics-Downloads/Llamada1-{uuid}.mp3"
        # while not os.path.isfile(path):
        #     print("Buscando archivo descargando o en descarga")
        #     sleep(2)