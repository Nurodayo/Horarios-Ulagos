import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from playwright.sync_api import sync_playwright


def nurin_scrape(url):
    # esperando x segundos como aweonao para que no retorne about:blank
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "lxml")

    tables = pd.read_html(str(soup))

    df = tables[0]
    return df


def nurin_scrape_horario(indice, driver, carrera):
    # driver = webdriver.Firefox()
    # driver.get("https://horarios.ulagos.cl/ptomontt/carreras.php")
    # carrera = driver.find_element(
    #    By.CSS_SELECTOR, ".select2-selection.select2-selection--single"
    # )
    # carrera.click()
    # carrera_input = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
    # carrera_input.send_keys(
    #    "informatica"
    # )  # por motivos de testeo voy a hacerlo con informatica y luego expandirlo a todas las carreras de PM
    # carrera_input.send_keys(Keys.RETURN)
    # set_carrera(driver, carrera)
    # print("uwu")
    carrera = carrera.split(" ", 1)[0]
    time.sleep(2)
    plan = driver.find_element(By.NAME, "plan_estudio")
    # print("owo")
    # plan.click()
    # print("antes del plan")
    select = Select(plan)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plan)
    time.sleep(1)
    select.select_by_index(indice)
    time.sleep(2)
    semestres = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-primary")
    print(str(len(semestres)) + " semestres")
    i = 1
    wait = WebDriverWait(driver, 10)
    for semestre in semestres:
        a = semestre.text
        print(a)
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", semestre
        )
        time.sleep(1)
        semestre.click()
        # no devuelve la url grrrrrr
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(4)
        url = driver.current_url
        print(url)
        df = nurin_scrape(str(url))
        df.to_csv(
            str(carrera) + "-p" + str(indice) + "-n" + str(i) + ".csv",
            index=False,
            encoding="utf-8",
        )
        time.sleep(1)
        i += 1
        # Volver a la página inicial para seleccionar otro semestre
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary")))
        time.sleep(1.25)


def set_carrera(page, nombre_carrera):
    carrera = page.locator(".select2-selection.select2-selection--single")
    carrera.wait_for(state="visible")
    carrera.click()
    campo_carrera = page.locator(".select2-search__field")
    campo_carrera.wait_for(state="visible")
    campo_carrera.type(str(nombre_carrera))
    campo_carrera.press("Enter")
    print(f"Obteniendo los planes de estudio ed {nombre_carrera}...")
    i = get_planes_estudio(page)
    if i == 0:
        print(f"\nalgo salio mal")
    else:
        print(f"\n{i} planes de estudio")
        return i
    # Selenium#
    # carrera = driver.find_element(
    #     By.CSS_SELECTOR, ".select2-selection.select2-selection--single"
    # )
    # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", carrera)
    # time.sleep(0.5)
    # carrera.click()
    # carrera_input = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
    # time.sleep(0.3)
    # carrera_input.clear()
    # carrera_input.send_keys(str(nombre_carrera) + " ")
    # carrera_input.send_keys(Keys.RETURN)
    # time.sleep(1)
    # print("obteniendo planes de estudio...")
    # i = get_planes_estudio(driver)
    # print(str(i - 1) + " planes de estudio")
    # return i


def get_planes_estudio(page):
    plan = page.locator('[name="plan_estudio"]')
    plan.wait_for(state="visible")
    planes = plan.count()
    return planes
    # slenderman#
    # benja weno pal nyacson te tiro to'o el pixi
    # plan = driver.find_element(By.NAME, "plan_estudio")
    # select = Select(plan)
    # print("trabajando...")
    # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plan)
    # print("retornando planes")
    # return len(select.options)


def get_carreras(page):
    select = page.locator('[name="carrera"]')
    carreras = select.locator("option")
    # |||selenium|||
    # carrera = driver.find_element(By.NAME, "carrera")
    # select = Select(carrera)
    # carreras = [option.get_attribute("value") for option in select.options]
    return carreras


with sync_playwright() as p:
    browser = p.firefox.launch(
        headless=False
    )  # para no tener interfaz grafica :emoticon dinero:
    page = browser.new_page()
    page.goto("https://horarios.ulagos.cl/ptomontt/carreras.php")
    i = get_carreras(page)
    print(i.all_text_contents())
    set_carrera(page, i.all_text_contents()[1])
    page.close()
