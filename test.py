from logging import raiseExceptions
from selenium.webdriver.ie.webdriver import WebDriver
from scrape_horarios import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from bs4.element import Tag
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Firefox()  # odio chrome y todos los navegadores chromium


# benja weno pal nyacson
class Usuario_idelfos:
    # to do: hash the password
    def __init__(self, name, rut, dv, password, horario, carrera) -> None:
        self.name = name
        self.rut = rut
        self.dv = dv
        self.password = password
        self.horario = None
        self.carrera = "informatica"  # to do implementarlo para todas las carreras

    def set_name(self, name):
        self.name = str(name)

    def get_name(self):
        return self.name

    def set_rut(self, rut):
        rut = str(rut)
        i = len(rut)
        self.dv = str(rut[i - 1])
        self.rut = rut[:-1]

    def get_rut(self):
        return str(self.rut) + "-" + str(self.dv)

    def set_password(self, password):
        self.password = password
        # en set_horario le metemos un csv con el join de todos los horarios de su carrera y sus cursos abiertos

    def set_horario(self, horario):
        self.horario = horario


def login_idelfos(rut, dv, password, driver):
    driver.get("https://idelfos.ulagos.cl:8443/idelfos/faces/seg/login.jspx")
    # pagina de login siempre sera la misma a menos que por un milagro dejen de usar idelfos
    rut_input = driver.find_element(By.ID, "rutUsuarioIT")
    dv_input = driver.find_element(By.ID, "dvUsuarioIT")
    password_input = driver.find_element(By.ID, "usuarioPasswordIT")

    rut_input.send_keys(str(rut))
    dv_input.send_keys(str(dv))
    password_input.send_keys(str(password))
    password_input.send_keys(Keys.RETURN)
    time.sleep(2)  # no se si funcara
    # explicacion. Voy a cargar directamenente la pagina de los cursos y rezar que siga logueado
    driver.get(
        "https://idelfos.ulagos.cl:8443/idelfos/faces/cal/calf691500.jspx?menu=54&prog=6915"
    )


def nurin_scrape_from_selenium(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    filas = soup.find_all("tr")
    if not filas:
        raise ValueError("no funca o idelfos esta caido")

    datos = []
    for fila in filas:
        celdas = [celda.get_text(strip=True) for celda in fila.find_all("td")]
        if celdas:
            datos.append(celdas)

    df = pd.DataFrame(datos)
    return df


def guardar_cursos(driver, nombre_archivo):
    df = nurin_scrape_from_selenium(driver)
    df.to_csv(nombre_archivo, index=False, encoding="utf-8")


login_idelfos("rut", "digito verificador", "pon tu contra aca bro", driver)
guardar_cursos(driver, "test.csv")
