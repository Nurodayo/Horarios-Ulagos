from scrape_horarios import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Usuario_idelfos:
    # to do: hash the password
    def __init__(self, name, rut, dg, password, horario, carrera) -> None:
        self.name = name
        self.rut = rut
        self.dg = dg
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
        self.df = str(rut[i - 1])
        self.rut = rut[:-1]

    def get_rut(self):
        return str(self.rut) + "-" + str(self.df)

    def set_password(self, password):
        self.password = password
        # en set_horario le metemos un csv con el join de todos los horarios de su carrera y sus cursos abiertos

    def set_horario(self, horario):
        self.horario = horario


def login_idelfos(rut, dg, password):
    pass
