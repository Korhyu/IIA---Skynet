import math

class olla:
    def __init__(self, diametro, alto, puntos = None):
        self.diametro = diametro
        self.alto = alto

        self.calc_param()


    def calc_param(self):
        self.base = math.pi * (self.diametro / 2) * (self.diametro / 2)
        self.pollera = math.pi * self.diametro * self.alto

        self.superficie = (2 * self.base) + self.pollera
        self.volumen = self.base * self.alto
        self.relVS = self.volumen / self.superficie


class ollaGA(olla):
    def __init__(self, diametro, alto, puntos = None, prob_cruza = None):
        self.diametro = diametro
        self.alto = alto

        self.calc_param()

        self.puntos = puntos
        self.prob_cruza = prob_cruza