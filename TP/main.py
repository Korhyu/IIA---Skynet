# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:36:53 2020

@author: 
"""


import random as rd
import numpy as np
import matplotlib.pyplot as plt

from clases import individuo
from fun_matias import select_ind, mate_ind
from fun_jose import run_test, plot_filtrados, load_data, gen_signal, add_noise



PUNTUACION_MAXIMA = 20


poblacion_actual = []           #Array con la poblacion actual 
poblacion_nueva = []            #Array donde se van volcando los individuos de la proxima poblacion
salida_filtro = []              #Array de las salidas del filtro con cada set de parametros
evol_error = []                 #Evolucion del error en funcion de las generaciones

# Parametros del DEWMA -------------------------------------------------------------------------------------------------------------------

lim_gamma = [1, 2]
lim_alfa = [1, 2]
lim_sigma = [1, 10]             #Actualmente no se utiliza y el filtro calcula su sigma propio
lim_Nmax = [30, 40]             #Hay que revisar estos limites porque el filtro DEWMA ya hace una estimacion de N usando estos valores
lim_Nmin = [5, 15]              #Quiza estos parametros hay que incluirlos en los limites de arriba, para pensar
lim_N = [lim_Nmin[0], lim_Nmax[1]]

# Parametros del GA ----------------------------------------------------------------------------------------------------------------------
nGen = 10                      #Generaciones a correr
pDim = 30                      #Tamaño de la poblacion
prob_mut = 0.05                 #Probabilidad de que un individuo mute
indx_mut = 0                    #Indice de la mutacion (cuanto puede variar el valor original) Si es 0 el valor del parametro se asigna nuevo

pCruza=10                        #probabilidad de cruza porcentual
Cant_param=6


# Parametros de la señal de prueba -------------------------------------------------------------------------------------------------------
amp = [20, 10, 15]              #Amplitudes de cada tono
per = [200, 420, 350]              #Periodos de cada tono
fase = [0, 0, 1.5]              #Fases de cada tono
muestras = 2000                  #Tamaño de la señal total

amp_noise = 1                   #Amplitud del ruido




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

    # Verifico que el maximo no sea inferior al minimo
    if param[4] < param[5]:
        param[5] = param[4] - 1

    return param


def create_pop(num_ind):
    #Funcion que crea una poblacion de individuos aleatoria

    parametros = param_rand()
    poblacion = np.array(parametros)

    for cont in range(num_ind-1):
        parametros = np.array(param_rand())
        poblacion = np.vstack((poblacion,parametros))

    return poblacion



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
poblacion_actual = create_pop(pDim)                 #Creo la poblacion aleatoria

#datos_orig = load_data()                           #Obtengo los datos de contagio
datos_puros = gen_signal(amp, per, fase, muestras)  #Genero la señal de prueba
datos_orig = add_noise(amp_noise, datos_puros)

for gen in range(nGen):
    print('Generacion ',gen)

    error_minimo = 10000
    error_maximo = 0
    error_promedio_gen = 0
    ind_minimo_err = 0
    ind_maximo_err = 0
    error_punt = np.empty([len(poblacion_actual), 2])      #Vector de errores y puntaje de cada individuo
    salida_filtro = np.empty([len(poblacion_actual), len(datos_orig)]) 

    for ind in range(len(poblacion_actual)):
        #aplicar  filtro a los tipitos
        salida_filtro[ind] =  run_test(poblacion_actual[ind], datos_orig)


        #Evaluacion de la salida del filtro
        error_actual = eval_test(datos_puros, salida_filtro[ind,:])
        error_punt[ind,0] = error_actual                                    #Cargo el error en el numpy
        error_promedio_gen = error_promedio_gen + error_actual

        if error_actual < error_minimo:
            error_minimo = error_actual
            ind_minimo_err = ind
        if error_actual > error_maximo:
            error_maximo = error_actual
            ind_maximo_err = ind

    #Calculo el error promedio de la generacion
    error_promedio_gen = error_promedio_gen / len(poblacion_actual)
    evol_error.append(error_promedio_gen)

    archivo = "Evolucion/Gen" + str(gen) + ".png"
    plot_filtrados(poblacion_actual, datos_orig, salida_filtro, archivo)



    #Asignacion de puntajes
    for ind in range(len(poblacion_actual)):
        error_punt[ind,1]= PUNTUACION_MAXIMA - (error_punt[ind,0] * PUNTUACION_MAXIMA / error_maximo)



    #Seleccion de individuos
    poblacion_nueva = select_ind(poblacion_actual, error_punt)
    
    #cruza    
    poblacion_nueva = mate_ind(poblacion_nueva, pCruza,Cant_param)
    

    #mutacion
    #mutac_ind(poblacion_nueva)

    #poblacion_actual = poblacion_nueva.copy()

#Termino y muestro resultados

fig = plt.figure(figsize=(22,18), dpi='150')
plt.plot(evol_error)
plt.set_ylabel('Error promedio')
plt.set_xlabel('Generacion')
plt.set_title('Evolucion del error por generacion')
plt.savefig("Evolucion/Error.png")
plt.close()