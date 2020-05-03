import math
import random
import matplotlib.pyplot as plt

from Clases import Annealing
from Clases import Ruta
from Clases import Ciudad


cant_iteraciones = 5
evol_precios = []


list_ciud = [Ciudad(0,0),
            Ciudad(5,0),
            Ciudad(0,8),
            Ciudad(8,5),
            Ciudad(4,2),
            Ciudad(7,5),
            Ciudad(3,1),
            Ciudad(2,7),
            Ciudad(4,9),
            Ciudad(2,8),
            Ciudad(3,4)]

#Lazo general para todas las iteraciones
for lista in range(cant_iteraciones):

    evol_precio = []

    #ciudades = Ciudades(list_ciud)                 #Guardo las ciudades en un objeto
    recocido = Annealing(100,1)                     #Creo el objeto de recocido
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
                #print("Acepto ruta - Condicional")
                ruta_actual.set_ruta(ruta_futura)
        


        #Histograma y ploteo
        evol_precio.append(ruta_actual.get_costo_tot())


        ruta_futura.ruta_swap(list_ciud)           #Introduzco un pequeño ruido
    
    evol_precios.append(evol_precio)
     
    ruta_actual.imprimir_ruta()
    ruta_actual.imprimir_costo()


#plt.plot(evol_precio)
for i in range(len(evol_precios)):
    plt.plot(evol_precios[i],label = 'id %s'%i)

plt.xlabel("Tiempo")
plt.ylabel("Valor")
plt.title("Evolucion del precio de la ruta")
plt.legend()
plt.show()




# for i in range(len(evol_precios[0])):
#     plt.plot([pt[i] for pt in evol_precios],label = 'id %s'%i)