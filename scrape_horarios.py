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
        time.sleep(5)  ## esperamos a que cargue
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


def save_json(dfl, carrera, indice):
    carrera_nombre_a = carrera.strip()
    carrera_nombre_a = carrera_nombre_a.replace(" ", "-")
    carrera_nombre_a = carrera_nombre_a.replace("/", "-")
    dfl.to_json(
        str(carrera_nombre_a) + str(indice) + ".json", orient="records", indent=2
    )
    # return df


def json_to_list():
    array = None
    if os.path.exists("./carreras.json"):
        with open("carreras.json", "r") as archivo:
            # array = json.load(archivo)
            dataFrame = pd.read_json(archivo)
            array = dataFrame.values.tolist()
    if array != None and array != []:
        return array
    else:
        raise TypeError("No se encontraron carreras")


# json = nurin_scrape(
#     "https://horarios.ulagos.cl/Global/carrera.php?carrera=3216&nivel=6&plan=3216II2020&sede=2028"
# )
# save_json(json, "icinf", "1")
# with sync_playwright() as p:
#     browser = p.firefox.launch(headless=True)
#     page = browser.new_page()
#     page.goto("https://horarios.ulagos.cl/ptomontt/carreras.php")
#     get_carreras(page)

# if os.path.exists("./carreras.json"):
#     with open("carreras.json", "r") as archivo:
#         # array = json.load(archivo)
#         dataFrame = pd.read_json(archivo)
#         array = dataFrame.values.tolist()

array = json_to_list()
print(array[0])
