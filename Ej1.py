import math
import random

class Ciudad:
    def __init__ (self, xi, yi):
        self.x = xi
        self.y = yi

    def getXY (self):
        return (self.x,self.y)

    def costo_camino (self, ciudad2):
        distx = self.x - ciudad2.x
        disty = self.y - ciudad2.y

        dist = math.sqrt(distx*distx + disty*disty)

        return dist

    def costo_camino (self, ciudad1, ciudad2):
        distx = ciudad1.x - ciudad2.x
        disty = ciudad1.y - ciudad2.y

        dist = math.sqrt(distx*distx + disty*disty)

        return dist


class Ruta:
    def __init__(self,ciudad_index = None):
        self.lista_ciudades = []
        self.lista_costos = []
        if ciudad_index is not None:
            self.lista_ciudades.append(ciudad_index)

    def nuevo_nodo (self, ciudad_index):
        if ciudad_index not in self.lista_ciudades:
            self.lista_ciudades.append(ciudad_index)
            return True
        else:
            return False

    def imprimir_ruta(self):
        print("Ruta - ", *self.lista_ciudades)

    def nueva_ruta(self, cant_ciudades):
        i = 0
        while i <= cant_ciudades:
            ciudad = random.randint(0, cant_ciudades)
            if self.nuevo_nodo(ciudad):
                i += 1

    def costo_ruta(self, list_ciud):
        for r in range(len(self.lista_ciudades)-1):
            costop = list_ciud[0].costo_camino(list_ciud[self.lista_ciudades[r]], list_ciud[self.lista_ciudades[r+1]])
            #print(f"r = {r} costo parcial = {costop}")
            #print(f"Ciudad1 = {list_ciud[self.lista_ciudades[r]]} Ciudad2 = {list_ciud[self.lista_ciudades[r+1]]}")
            self.lista_costos.append(costop)

    def imprimir_costo(self):
        print("Costos parciales - ", *self.lista_costos)
        print("Costo total - ", str(sum(self.lista_costos)))
        


list_ciud = [Ciudad(0,0),
            Ciudad(10,0),
            Ciudad(0,10),
            Ciudad(8.660254,5),
            Ciudad(5,5)]

ruta = Ruta()
ruta.nueva_ruta(len(list_ciud)-1)


#for x in range(len(ciudades)):
#    print("Distancia a " + str(x) + ": " + str(ciudades[0].costo_camino(ciudades[x])))

ruta.imprimir_ruta()
ruta.costo_ruta(list_ciud)
ruta.imprimir_costo()

