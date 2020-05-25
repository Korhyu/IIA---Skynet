# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:36:53 2020

@author: 
"""


import random as rd
import numpy as np

from clases import individuo
from fun_jose import run_test, plot_filtrados
from fun_matias import select_ind


poblacion_actual = []           #Lista con la poblacion actual 
poblacion_nueva = []            #Lista donde se van volcando los individuos de la proxima poblacion


# Parametros del DEWMA -------------------------------------------------------------------------------------------------------------------
lim_N = [2, 40]
lim_gamma = [0.1, 10]
lim_alfa = [0.1, 10]
lim_Nmax = [40, 40]             #Hay que revisar estos limites porque el filtro DEWMA ya hace una estimacion de N usando estos valores
lim_Nmin = [2, 2]               #Quiza estos parametros hay que incluirlos en los limites de arriba, para pensar


# Parametros del GA ----------------------------------------------------------------------------------------------------------------------
nGen = 1                        #Generaciones a correr
pDim = 20                       #Tamaño de la poblacion
prob_mut = 0.05                 #Probabilidad de que un individuo mute
indx_mut = 0                    #Indice de la mutacion (cuanto puede variar el valor original) Si es 0 el valor del parametro se asigna nuevo





# Funciones ------------------------------------------------------------------------------------------------------------------------------

def param_rand():
    #Genera los parametros aleatorios y los devuelve en una lista
    param = [0, 0, 0, 0, 0]

    param[0] = rd.randint(lim_N[0], lim_N[1])               #Numeros enteros
    param[3] = rd.randint(lim_Nmax[0], lim_Nmax[1])
    param[4] = rd.randint(lim_Nmin[0], lim_Nmin[1])

    param[1] = rd.uniform(lim_gamma[0], lim_gamma[1])       #Numeros con coma
    param[2] = rd.uniform(lim_alfa[0], lim_alfa[1])

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




def eval_test(curva_filtrada):
    print('eval_test')
    #Recive la curva filtrada y toma de la curva del contagio
    #comparando las 2 y haciendo la evaluacion (error cuadratico medio o error medio)
    #devuelve un valor como resultado de esa comparacion
    #quiza la suma de todos los errores o alguna otra metrica a considerar


    pass


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
        for i in range(3):                          #Recorro los parametros de ese individuo para ver si mutan. Esta harcodeado el parametro maximo porque esta el tema del Nmax y Nmin
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
#read_pop();
for fin in range(nGen):

    #aplicar  filtro a los tipitos
    for individuo in range(len(poblacion_actual)):
        poblacion_actual[individuo].get_filt(run_test(poblacion_actual[individuo].param))

    plot_filtrados(poblacion_actual)

    #Evaluacion de la salida del filtro
    eval_test(nGen)
    #Seleccion de individuos
    
    #llenando score provisorios----------------------------
    for individuo in range(len(poblacion_actual)):
        poblacion_actual[individuo].score=rd.randint(1,20);
    #------------------------------------------------------
    poblacion_nueva=select_ind(poblacion_actual)
    
    #cruza
    mate_ind()
    #mutacion
    mutac_ind(poblacion_nueva)

    poblacion_actual = poblacion_nueva.copy()

#Termino y muestro resultados

