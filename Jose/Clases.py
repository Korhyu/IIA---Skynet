import math
import random

class Annealing:
    def __init__(self, tr, tau):
        self.ti = 600           #Valor de la temperatura inicial de calentamiento
        self.ta = self.ti       #Temperatura actual del recocido
        self.tf = 0             #Temperatura final del recocido
        self.tau = tau          #Constante de "enfriamiento"
        self.tr = tr            #Time resolution del "enfriamiento"
        self.pa = 1             #Probabilidad de aceptar
        self.tim = 0            #tiempo actual del "enfriamiento"

        self.ts = self.tau/round(self.tr)
        

    def calc_temp(self):
        self.ta = self.ti * math.exp(-self.tim / self.tau)
        self.tim += self.ts



    def calc_prob(self):
        self.calc_temp()
        self.pa = self.ta / self.ti

        return self.pa


    def get_ta(self):
        return self.ta


    def get_pa(self):
        return self.pa

        

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
        #Calcula el costo del camino entre las ciudades de los indices ingresados
        distx = ciudad1.x - ciudad2.x
        disty = ciudad1.y - ciudad2.y

        dist = math.sqrt(distx*distx + disty*disty)

        return dist



class Ciudades(Ciudad):
    def __init__(self, lista):
        self.lista_ciudades = []
        for index in range(len(lista)):
            self.lista_ciudades.append(lista[index])

    def append_ciudad (self, Ciudad):                   #no esta terminado
        self.lista_ciudades.append(Ciudad)

    def costo_camino(self, index1, index2):
        return self.lista_ciudades[0].costo_camino(self.lista_ciudades[index1],self.lista_ciudades[index2])

    def costos_ruta(self, indices):
        costos = []
        for index in range(len(self.lista_ciudades)-1):
            costos.append(self.costo_camino(indices[index],indices[index+1]))
        return costos



class Ruta(Ciudad):
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

    def nueva_ruta(self, list_ciud):
        self.clear_nodos()
        i = 0
        cant_ciudades = len(list_ciud)-1
        while i <= cant_ciudades:
            ciudad = random.randint(0, cant_ciudades)
            if self.nuevo_nodo(ciudad):
                i += 1
        
        self.costo_ruta(list_ciud)

    def ruta_swap(self, list_ciud):
        indice1 = random.randint(0, len(list_ciud)-1)
        indice2 = random.randint(0, len(list_ciud)-1)
        while indice1 == indice2:
            indice2 = random.randint(0, len(self.lista_ciudades)-1)

        self.lista_ciudades[indice1], self.lista_ciudades[indice2] = self.lista_ciudades[indice2], self.lista_ciudades[indice1]

        self.costo_ruta(list_ciud)

    def clear_nodos(self):
        self.lista_ciudades.clear()
        self.lista_ciudades.clear()
        self.lista_costos.clear()

    def costo_ruta(self, list_ciud):
        self.lista_costos.clear()
        for r in range(len(self.lista_ciudades)-1):
            costop = self.costo_camino(list_ciud[self.lista_ciudades[r]], list_ciud[self.lista_ciudades[r+1]])
            self.lista_costos.append(costop)

    def get_costo_tot(self):
        return round(sum(self.lista_costos),2)

    def imprimir_costo(self):
        print("Costo total - ", str(sum(self.lista_costos)))

    def imprimir_costos(self):
        print("Costos parciales - ", *self.lista_costos)
        print("Costo total - ", str(sum(self.lista_costos)))
        
    def get_ruta(self):
        ruta = []
        ruta = self.lista_ciudades
        return ruta

    def get_costos(self):
        costos = self.lista_costos
        return costos

    def set_ruta(self, Ruta):
        self.clear_nodos()

        ruta = Ruta.get_ruta()
        for index in range(len(ruta)):
            self.lista_ciudades.append(ruta[index])

        costos = Ruta.get_costos()
        for index in range(len(costos)):
            self.lista_costos.append(costos[index])





#for x in range(len(ciudades)):
#    print("Distancia a " + str(x) + ": " + str(ciudades[0].costo_camino(ciudades[x])))