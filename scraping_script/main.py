from scrape_horarios import *
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright

## Scrapear todos los horarios
array = json_to_list()
for carrera in array:
    print(carrera)
print("carreras sede puerto montt ^^^")

scrape_all = False
nohead = False
scrape_carrs_again = False
plans = True

if nohead:
    print("Running headless = True")
else:
    print("Running headless = False")
with sync_playwright() as p:

    browser = p.firefox.launch(headless=nohead)
    context = browser.new_context()
    page = context.new_page()
    ## vamos a la pagina de horarios de ptomontt
    page.goto("https://horarios.ulagos.cl/ptomontt/carreras.php")
    time.sleep(2)  ## esperamos 2 segundos a que cargue, por l

    if plans:
        planes_to_json(page, array)

    if scrape_carrs_again:
        print("Getting carreras.json again")
        get_carreras(page)

    if scrape_all:
        for carrera in array:
            scrape_carrera(page, carrera, context)
            page.goto(
                "https://horarios.ulagos.cl/ptomontt/carreras.php"
            )  # hack para ver si funca
            time.sleep(2)

    print(" Listo :D")
