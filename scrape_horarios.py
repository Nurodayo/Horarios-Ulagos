from textwrap import indent
import requests
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
import re
import time


def nurin_scrape(url):
    # esperando x segundos como aweonao para que no retorne about:blank
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "lxml")

    tables = pd.read_html(str(soup))

    df = tables[0]
    return df


def nurin_scrape_horario(indice, page, carrera):
    carrera_nombre_a = carrera.replace(" ", "-")
    carrera_nombre_a = carrera_nombre_a.strip()
    carrera_nombre_a = re.sub(r"[^\w\-]", "", carrera_nombre_a)
    # context = browser.new_context()
    plan = page.locator('[name="plan_estudio"]')
    plan.select_option(index=indice)
    semestres = page.locator(".btn.btn-primary")
    semestres.wait_for(state="visible")

    cant = semestres.count()
    df_list = []
    print(f"\n{cant} semestres en {carrera}")
    i = 0
    while i < cant:
        with page.context.expect_page() as new_tab:
            semestres.nth(i).click()
            page.wait_for_timeout(500)
            pagina_horario = new_tab.value
            page.wait_for_timeout(500)
            pagina_horario.wait_for_load_state()
        url = str(pagina_horario.url)
        df = nurin_scrape(url)
        df_list.append(df)
        # df.to_json(carrera_nombre_a + ".json", orient="records", indent=2)
        page.wait_for_timeout(500)
        pagina_horario.close()
        semestres.nth(i).wait_for(state="visible")
        i += 1
    return df_list


def set_carrera(page, nombre_carrera):
    carrera = page.locator(".select2-selection.select2-selection--single")
    carrera.wait_for(state="visible")
    carrera.click()
    time.sleep(2)  # a veces clickea y los semestres no cargan
    campo_carrera = page.locator(".select2-search__field")
    campo_carrera.wait_for(state="visible")
    campo_carrera.type(str(nombre_carrera))
    campo_carrera.press("Enter")
    print(f"\nObteniendo los planes de estudio ed {nombre_carrera}...")
    i = get_planes_estudio(page)
    if i == 0:
        print(f"\nalgo salio mal")
        return 0
    else:
        print(f"\n{i} planes de estudio")
        return i


def get_planes_estudio(page):
    plan = page.locator('[name="plan_estudio"]')
    plan.wait_for(state="visible")
    planes = plan.count()
    return planes


def get_carreras(page):
    select = page.locator('[name="carrera"]')
    carreras = select.locator("option")
    return carreras


def save_json(dfl, carrera, indice):
    carrera_nombre_a = carrera.strip()
    carrera_nombre_a = carrera_nombre_a.replace(" ", "-")
    carrera_nombre_a = carrera_nombre_a.replace("/", "-")
    df = pd.concat(dfl, ignore_index=True)
    df.to_json(
        str(carrera_nombre_a) + str(indice) + ".json", orient="records", indent=2
    )
    # return df


# with sync_playwright() as p:
#  browser = p.firefox.launch(
#      headless=False
#  )  # para no tener interfaz grafica :emoticon dinero:
#  page = browser.new_page()
#  page.goto("https://horarios.ulagos.cl/ptomontt/carreras.php")
#  i = get_carreras(page).all_text_contents()[1]
#  print(i)
#  indice = set_carrera(page, i)
#  dfl = nurin_scrape_horario(indice, page, i)
#  save_json(dfl, str(i), 1)
#  page.close()
