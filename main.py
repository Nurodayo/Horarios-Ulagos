from scrape_horarios import *
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

driver = webdriver.Firefox()
driver.get("https://horarios.ulagos.cl/ptomontt/carreras.php")
carreras = get_carreras(driver)
carreras.pop(0)
print(carreras)
print("Mandandole DDoS a la ULA")
for carrera in carreras:
    # driver.get("https://horarios.ulagos.cl/ptomontt/carreras.php")
    time.sleep(0.5)
    print("carrera " + str(carrera))
    i = set_carrera(driver, str(carrera))
    j = 1
    while j < i:
        print("plan " + str(j))
        nurin_scrape_horario(j, driver, carrera)
        time.sleep(1)
        j += 1
    time.sleep(0.1)

driver.quit()
