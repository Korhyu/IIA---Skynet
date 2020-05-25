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


lim_N = [2, 40]
lim_gamma = [0.1, 10]
lim_alfa = [0.1, 10]
lim_Nmax = [40, 40]             #Hay que revisar estos limites porque el filtro DEWMA ya hace una estimacion de N usando estos valores
lim_Nmin = [2, 2]               #Quiza estos parametros hay que incluirlos en los limites de arriba, para pensar


nGen = 1                        #Generaciones a correr
pDim = 20                       #Tamaño de la poblacion

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


def mutac_ind():
    #Funcion que recorre la poblacion futura y genera la mutacion en los individuos

    pass






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
    pob_sel=select_ind(poblacion_actual)
    
    #cruza
    mate_ind()
    #mutacion
    mutac_ind()

#Termino y muestro resultados

