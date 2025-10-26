from textwrap import indent
import requests
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
import re
import time
import json
import os  # posiblemente sacable


def nurin_scrape(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "lxml")

    header = soup.find(id="d_h")
    body = soup.find("tbody")

    columns = [
        tag.get_text(strip=True)
        for tag in header.find_all(lambda t: t.name.startswith("t"))
    ]
    rows = []
    for tr in body.find_all("tr"):
        row = [
            tag.get_text(strip=True)
            for tag in tr.find_all(lambda t: t.name.startswith("t"))
        ]
        if row:
            rows.append(row)

    df = pd.DataFrame(rows, columns=columns)
    return df


## La pagina cambio como se renderizan las carreras


def get_carreras(page):
    ## scrapeamos las carreras
    # page.goto("https://admision.ulagos.cl/carreras/campus-y-sedes/")
    page.locator("#select2-carrera-container").click()
    input = page.locator(".select2-search__field")
    i = 0
    carreras = []
    while i < 10:
        print(i)
        j = str(i) + " "
        input.fill(str(j))
        ## aprovechamos que podemos usar un caracter y un espacio para renderizar las carreras
        time.sleep(6)  ## esperamos a que cargue
        carreras_res = page.locator(".select2-results__option").all()
        carreras_aux = [li.inner_text().strip() for li in carreras_res]
        print(carreras_aux)
        carreras.extend(carreras_aux)
        i += 1
    # while i < 100:
    #     print(i)
    #     if i < 10:
    #         j = "0" + str(i)
    #     else:
    #         j = str(i)
    #     input.fill(str(j))
    #     time.sleep(4)  ## esperar a que carguen las carreras
    #     carreras_res = page.locator(".select2-results__option").all()
    #     carreras_aux = [li.inner_text().strip() for li in carreras_res]
    #     print(carreras_aux)
    #     carreras.extend(carreras_aux)
    #     i += 1
    #     ## Fuerza bruta

    carreras = list(set(carreras))

    if "No hay resultados" in carreras:
        carreras.remove("No hay resultados")
    if "Buscando..." in carreras:
        carreras.remove("Buscando...")

    df = pd.DataFrame(carreras, columns=["nombre"])

    df.to_json("carreras.json", orient="records", force_ascii=False, indent=4)

    print(df)
    return carreras


def get_options(page, carrera):

    carrera_aux = carrera
    carrera = carrera.replace("/", "")  # waaaa あ

    # print(carrera)
    c = page.locator(".select2-selection__rendered")
    c.click()
    input = input = page.locator(".select2-search__field")
    print(carrera)
    input.fill(str(carrera))
    print("cargando")
    time.sleep(4)
    page.keyboard.press("Enter")
    print("cargando")
    time.sleep(6)  # esperar a q los planes carguen pq vamos muy rapido

    # select_plan_estudios = page.locator("#plan_estudio")
    planes = page.locator("option").all()
    options = [option.inner_text().strip() for option in planes]
    print(options)
    if carrera in options:
        options.remove(carrera)
    if "Seleccione Opción" in options:
        options.remove("Seleccione Opción")
    print(options)

    return options


def scrape_carrera(page, carrera, context):
    print(carrera)
    time.sleep(4)
    options = get_options(page, carrera)
    i = 0
    for option in options:
        i += 1
        print("Locating")
        select = page.locator("#plan_estudio")
        select.click()
        time.sleep(2)
        print("Found")
        # seleccion = page.get_by_text(option)
        ## html
        print(option)
        select.select_option(label=option)

        # Waiting for buttons to load
        time.sleep(6)

        buttons = page.locator(".btn").all()

        j = 0
        for button in buttons:
            # n^2
            j += 1
            with context.expect_page() as new_page_info:
                button.click()
            new_page = new_page_info.value
            time.sleep(
                3
            )  # no se que deberia ponerle a los time sleep para que funquen mejor
            url = new_page.url
            print(url)

            df = nurin_scrape(url)
            save_json(df, carrera, i, j)
            new_page.close()
            time.sleep(2)
        # while True:
        #    print("sleeping")  # es para inspeccionar poque despues se cierra todo


def save_json(dfl, carrera, indice, jndice):
    carrera_nombre_a = carrera.strip()
    carrera_nombre_a = carrera_nombre_a.replace(" ", "-")
    carrera_nombre_a = carrera_nombre_a.replace("/", "-")
    dfl.to_json(
        str(carrera_nombre_a) + str(indice) + "-" + str(jndice) + ".json",
        orient="records",
        indent=2,
    )
    # return df


def json_to_list():
    array = None
    array_fix = []
    if os.path.exists("./carreras.json"):
        with open("carreras.json", "r") as archivo:
            # array = json.load(archivo)
            dataFrame = pd.read_json(archivo)
            array = dataFrame.values.tolist()
            for list in array:
                stringy = list[0]
                array_fix.append(str(stringy))

    if array_fix != None and array_fix != []:
        return array_fix
    else:
        raise TypeError("No se encontraron carreras")


# json = nurin_scrape(
#     "https://horarios.ulagos.cl/Global/carrera.php?carrera=3216&nivel=6&plan=3216II2020&sede=2028"
# )
# save_json(json, "icinf", "1")
# with sync_playwright() as p:
#     browser = p.firefox.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://horarios.ulagos.cl/ptomontt/carreras.php")
#     time.sleep(2)
#     print("waited")
#
#     # if os.path.exists("./carreras.json"):
#     #     with open("carreras.json", "r") as archivo:
#     #         # array = json.load(archivo)
#     #         dataFrame = pd.read_json(archivo)
#     #         array = dataFrame.values.tolist()
#
#     array = json_to_list()
#     print(array[5])
#
#     scrape_carrera(page, array[5], context)
