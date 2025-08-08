from scrape_horarios import *
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(
        headless=False
    )  # para no tener interfaz grafica :emoticon dinero:
    page = browser.new_page()
    page.goto("https://horarios.ulagos.cl/ptomontt/carreras.php")
    carreras = get_carreras(page)
    carreras_list = carreras.all_text_contents()
    carreras_list.pop(0)
    print(carreras_list)
    print("Mandandole DDos a la ULakes")

    for carrera in carreras_list:
        print("carrera: " + str(carrera))
        i = int(set_carrera(page, carrera))
        j = 1
        while j < (i + 1):
            print("Plan #:" + str(j))
            df = nurin_scrape_horario(j, page, str(carrera))
            save_json(df, str(carrera), j)
            j += 1

    # fin del codigo
    page.close()

# reminiscences of selenium version
