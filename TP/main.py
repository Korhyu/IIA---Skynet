# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:36:53 2020

@author: 
"""


import random as rd
import numpy as np
import matplotlib.pyplot as plt

from clases import individuo
from fun_jose import run_test, plot_filtrados, load_data
from fun_matias import select_ind



PUNTUACION_MAXIMA = 20


poblacion_actual = []           #Lista con la poblacion actual 
poblacion_nueva = []            #Lista donde se van volcando los individuos de la proxima poblacion



# Parametros del DEWMA -------------------------------------------------------------------------------------------------------------------
lim_N = [2, 40]
lim_gamma = [1, 2]
lim_alfa = [1, 2]
lim_sigma = [1, 10]             #Actualmente no se utiliza y el filtro calcula su sigma propio
lim_Nmax = [2, 40]             #Hay que revisar estos limites porque el filtro DEWMA ya hace una estimacion de N usando estos valores
lim_Nmin = [1, 39]               #Quiza estos parametros hay que incluirlos en los limites de arriba, para pensar


# Parametros del GA ----------------------------------------------------------------------------------------------------------------------
nGen = 10                      #Generaciones a correr
pDim = 20                      #Tamaño de la poblacion
prob_mut = 0.05                 #Probabilidad de que un individuo mute
indx_mut = 0                    #Indice de la mutacion (cuanto puede variar el valor original) Si es 0 el valor del parametro se asigna nuevo





# Funciones ------------------------------------------------------------------------------------------------------------------------------

def param_rand():
    #Genera los parametros aleatorios y los devuelve en una lista
    param = [0, 0, 0, 0, 0, 0]

    param[0] = rd.randint(lim_N[0], lim_N[1])               #Numeros enteros
    param[4] = rd.randint(lim_Nmax[0], lim_Nmax[1])
    param[5] = rd.randint(lim_Nmin[0], lim_Nmin[1])

    param[1] = rd.uniform(lim_gamma[0], lim_gamma[1])       #Numeros con coma
    param[2] = rd.uniform(lim_alfa[0], lim_alfa[1])
    param[3] = rd.uniform(lim_sigma[0], lim_sigma[1])

    if param[4] < param[5]:
        param[5] = param[4] - 1

    return param


def create_pop(num_ind):
    #Funcion que crea una poblacion de individuos aleatoria
    #Cada individuo es una lista de los 5 parametros en el orden N, gamma, alfa, Nmax y Nmin

    for cont in range(num_ind):
        parametros = param_rand()
        poblacion_actual.append(individuo(parametros))



def read_pop():
    print('read_pop')
    #Funcion que lee el archivo de la poblacion almacenada en el archivo
   
    pass




def eval_test(original, filtrada):
    #Toma la curva filtrada y la curva del contagio
    #comparando las 2 y haciendo la evaluacion (error cuadratico medio o error medio)
    #devuelve un valor como resultado de esa comparacion
    #quiza la suma de todos los errores o alguna otra metrica a considerar

    errores_parciales = []

    for i in range(len(filtrada)):
        errores_parciales.append((original[i]-filtrada[i]) ** 2)

    err = sum(errores_parciales) / len(filtrada)

    return err
    


def score_ind():
    print('score_ind')
    #Esta funcion deberia tomar el error de la funcion eval_test y asignar un puntaje 
    #quiza esta funcion este de mas.... probablemente.... casi seguro....

    pass


def mate_ind():
    print('mate_ind')
    #Esta funcion deberia reccorer la poblacion actual e ir seleccionando los individuos a aparear
    #para crear uno nuevo
    #Debe considerar cuantos "puestos libres" hay en la proxima poblacion para no exceder el numero

    pass



def mutac_ind(poblacion):
    #Funcion que recorre la poblacion futura y genera la mutacion en los individuos

    for individuo in range(len(poblacion)):
        for i in range(4):                          #Recorro los parametros de ese individuo para ver si mutan. Esta harcodeado el parametro maximo porque esta el tema del Nmax y Nmin
            num = rd.uniform(0, 1)                  #Numero aleatorio para comprar contra la probabilidad de mutacion
            if num <= prob_mut:
                if indx_mut == 0:                   #Si el indice de mutacion es 0, busco un parametro nuevo
                    param_mut = param_rand()        #Obtengo todos los parametros nuevos, mas facil que crear una funcion que me de 1 parametro especifico
                    poblacion[individuo].param[i] = param_mut[i]
                
                else:                               #"Inercia" de mutacion
                    param_mut = poblacion[individuo].param[i]
                    if i == 0:                      #significa que estoy mutando el N y tiene que ser entero, realizo un redondeo
                        param_mut = round(param_mut * (1 + indx_mut * rd.uniform(-1, 1)))
                    else:
                        param_mut = param_mut * (1 + indx_mut * rd.uniform(-1, 1))





print('Vamos a tomar',nGen,'generaciones')
create_pop(pDim)                                #Creo la poblacion aleatoria

datos_orig = load_data()                        #Obtengo los datos de contagio
evol_error = []

for fin in range(nGen):
    print('Generacion ',fin)

    error_minimo = 10000
    error_maximo = 0
    error_promedio = 0
    ind_minimo_err = 0
    ind_maximo_err = 0
    
    for ind in range(len(poblacion_actual)):
        #aplicar  filtro a los tipitos
        poblacion_actual[ind].set_filt(run_test(poblacion_actual[ind].param))
        
        #Evaluacion de la salida del filtro
        error_actual = eval_test(datos_orig, poblacion_actual[ind].filtrada)
        poblacion_actual[ind].error = error_actual
        error_promedio = error_promedio + error_actual

        if error_actual < error_minimo:
            error_minimo = error_actual
            ind_minimo_err = ind
        if error_actual > error_maximo:
            error_maximo = error_actual
            ind_maximo_err = ind

    #Calculo el error promedio de la generacion
    error_promedio = error_promedio / len(poblacion_actual)
    evol_error.append(error_promedio)


    plot_filtrados(poblacion_actual)



    #Asignacion de puntajes
    for ind in range(len(poblacion_actual)):
        poblacion_actual[ind].score = PUNTUACION_MAXIMA - (poblacion_actual[ind].error * PUNTUACION_MAXIMA / error_maximo)



    #Seleccion de individuos
    poblacion_nueva = select_ind(poblacion_actual)
    
    #cruza
    #mate_ind()
    #mutacion
    mutac_ind(poblacion_nueva)

    poblacion_actual = poblacion_nueva.copy()

#Termino y muestro resultados

plt.plot(evol_error)
plt.show()