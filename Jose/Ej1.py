import math
import random

from Clases import Annealing
from Clases import Ruta
from Clases import Ciudad
#from Clases import Ciudades


list_ciud = [Ciudad(0,0),
            Ciudad(10,0),
            Ciudad(0,10),
            Ciudad(8.660254,5),
            Ciudad(5,5)]

#ciudades = Ciudades(list_ciud)                 #Guardo las ciudades en un objeto
recocido = Annealing(20000,1)                    #Creo el objeto de recocido
ruta_actual = Ruta()                            #Objeto de la ruta actual
ruta_futura = Ruta()                            #Objeto de ruta nueva a comparar
ruta_actual.nueva_ruta(list_ciud)               #Determino la ruta
ruta_futura.nueva_ruta(list_ciud)               #Cambio la ruta completa


while recocido.get_ta() > 0.1:
    
    prob = recocido.calc_prob()


    if ruta_actual.get_costo_tot() < ruta_futura.get_costo_tot():
        #Si es verdad debo adoptar la ruta nueva (salir del minimo local) si la probabilidad quiere
        numero = random.randint(0, 100) / 100
        if numero <= prob:
            print("Cambio rutas - Condicional")
            ruta_actual.set_ruta(ruta_futura)
            ruta_futura.ruta_swap(list_ciud)           #Introduzco un pequeño ruido
    else:
        print("Cambio rutas - Menor Precio")
        ruta_actual.set_ruta(ruta_futura)
        ruta_futura.nueva_ruta(list_ciud)               #Cambio la ruta completa




ruta_actual.imprimir_ruta()
ruta_actual.imprimir_costo()


