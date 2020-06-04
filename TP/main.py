# -*- coding: utf-8 -*-
"""
Created on Sat May 23 12:36:53 2020

@author: 
"""


import random as rd
import numpy as np
import matplotlib.pyplot as plt
import statistics


from fun_GA import select_ind, mate_ind,mutac_ind, buscarnegativos
from fun_sys import run_test, plot_filtrados, load_data, gen_signal, add_noise, plot_error
from fun_sys import FiltroFIR, plot_comparacion, FiltroEWMA, plot_best_indN, plot_in_out, save_ind


PUNTUACION_MAXIMA = 10000

# Parametros del GA ----------------------------------------------------------------------------------------------------------------------
nGen = 201                     #Generaciones a correr
pDim = 40                     #Tamaño de la poblacion
pMuta = 3                     #Probabilidad de que un individuo mute expresade en %
dMuta = 50                    #delta de Muta, osea cuanto puede variar en la mutacion expresado en %
pCruza = 40                   #probabilidad de cruza porcentual

# ----------------------------------------------------------------------------------------------------------------------


# Parametros del dEWMA -------------------------------------------------------------------------------------------------------------------
lim_gamma = [0.5, 40]
lim_alfa = [1, 30]
lim_sigma = [0.01, 5]             #Actualmente no se utiliza y el filtro calcula su sigma propio
lim_Nmax = [200, 200]             #Hay que revisar estos limites porque el filtro dEWMA ya hace una estimacion de N usando estos valores
lim_Nmin = [5, 5]              #Quiza estos parametros hay que incluirlos en los limites de arriba, para pensar
lim_N = [lim_Nmin[0], lim_Nmax[1]]




# Variables auxiliares ----------------------------------------------------------------------------------------------------------------------
poblacion_actual = []           #Array con la poblacion actual 
poblacion_nueva = []            #Array donde se van volcando los individuos de la proxima poblacion
salida_filtro = []              #Array de las salidas del filtro con cada set de parametros
evol_error_medio = []  
error_max = np.zeros(nGen)               #Evolucion del error en funcion de las generaciones
error_min = np.zeros(nGen)
error_minomorum = np.zeros(nGen)


# Parametros de la señal de prueba -------------------------------------------------------------------------------------------------------
amp = [20, 10, 15]              #Amplitudes de cada tono
per = [400, 250, 530]           #Periodos de cada tono
fase = [0, 0.78, 1.57]          #Fases de cada tono
muestras = 2000                 #Tamaño de la señal total

amp_noise = 2                   #Amplitud del ruido


# Parametros de filtros de comparacion ---------------------------------------------------------------------------------------------------
eq_FIR = 12                 #Valor N del filtro "equivalente" FIR
eq_EWMA = 12                #Valor N del filtro "equivalente" EWMA


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
    


def score_pob(error_punt, error_maximo):
    #Esta funcion deberia tomar el error de la funcion eval_test y asignar un puntaje 

    for ind in range(len(poblacion_actual)):
        error_punt[ind,1]= PUNTUACION_MAXIMA - (error_punt[ind,0] * PUNTUACION_MAXIMA / error_maximo)
        if  error_punt[ind,1] <1:
            error_punt[ind,1]=1






# Main -----------------------------------------------------------------------------------------------------------------
print('Vamos a tomar',nGen,'generaciones')
poblacion_actual = create_pop(pDim)                 #Creo la poblacion aleatoria

#datos_orig = load_data()                           #Obtengo los datos de contagio
datos_puros = gen_signal(amp, per, fase, muestras)  #Genero la señal de prueba
datos_orig = add_noise(amp_noise, datos_puros)

error_superman = 10000                              #Error del mejor individuo de todas las generaciones


filtrada_FIR = FiltroFIR(eq_FIR, datos_orig)        #Filtradas de comparacion
filtrada_EWMA = FiltroEWMA(eq_EWMA, datos_orig)

for gen in range(nGen):
    print('Generacion ',gen)

    poblacion_nueva = []                                    #Reinicio la poblacion nueva

    error_minimo = 10000
    
    error_maximo = 0
    error_promedio_gen = 0
    ind_minimo_err = 0
    ind_maximo_err = 0
    error_punt = np.empty([len(poblacion_actual), 2])      #Vector de errores y puntaje de cada individuo
    salida_filtro = np.empty([len(poblacion_actual), len(datos_orig)]) 

    # Evaluo cada individuo y le asigno el error
    for ind in range(len(poblacion_actual)):
        #aplicar  filtro a los tipitos
        [salida_filtro[ind], Ns] =  run_test(poblacion_actual[ind], datos_orig)


        #Evaluacion de la salida del filtro
        error_actual = eval_test(datos_puros, salida_filtro[ind,:])
        error_punt[ind,0] = error_actual                                    #Cargo el error en el numpy
        error_promedio_gen = error_promedio_gen + error_actual

        if error_actual < error_minimo:
            error_minimo = error_actual
            ind_minimo_err = ind
            error_min[gen]=error_actual

        if error_actual > error_maximo:
            error_maximo = error_actual
            ind_maximo_err = ind
            
        #Descubriendo a Superman
        if error_superman > error_minimo:
            superman = poblacion_actual[ind]                    #Guardo los parametros
            agujero_techo = salida_filtro[ind]                  #Guardo surespuesta al filtro
            crec_superman = Ns                                  #Guardo su evolucion de Ns
            error_superman = error_actual                       #Guardo el error para ver si sigue siendo superman
            
    #Para ploteo de errores minimo y maximo
    error_min[gen] = error_minimo
    error_max[gen] = error_maximo
    error_minomorum[gen] = error_superman

    #Calculo el error promedio de la generacion
    error_promedio_gen = error_promedio_gen / len(poblacion_actual)
    evol_error_medio.append(error_promedio_gen)
    
    #Asignacion de puntajes
    score_pob(error_punt, error_maximo)

    #Guardo los parametros del mejor individuo de esta generacion


    #Genero ploteos de la generacion
    if gen%20 is 0:
        #pobl_punt = np.concatenate((poblacion_actual, error_punt), axis=1)
        #pobl_punt = pobl_punt[np.argsort(-1*pobl_punt[:,7])]
        #plot_filtrados(pobl_punt, datos_puros, salida_filtro, gen)

        #Genero la salida del filtro FIR con el mejor individuo de la generacion y las comparo
        salidas_dEWMA = np.concatenate((salida_filtro, error_punt), axis=1)
        salidas_dEWMA = np.array(sorted(salidas_dEWMA, key=lambda x :x[-1], reverse=True))
        filtrada_dEWMA = salidas_dEWMA[0,0:-2]
        
        plot_comparacion(gen, 1, datos_puros, filtrada_dEWMA, filtrada_FIR[0], filtrada_EWMA[0], [800, 1200])
        plot_comparacion(gen, 2, datos_puros, filtrada_dEWMA, filtrada_FIR[0], filtrada_EWMA[0], [800, 900])
        plot_comparacion(gen, 3, datos_orig, filtrada_dEWMA, filtrada_FIR[0], filtrada_EWMA[0], [800, 900])



    #Seleccion de individuos
    poblacion_nueva = select_ind(poblacion_actual, error_punt)
    

    #cruza    
    poblacion_nueva = mate_ind(poblacion_nueva, pCruza)
    

    #mutacion
    poblacion_actual = mutac_ind(poblacion_nueva, pMuta, dMuta, lim_Nmax[1], lim_Nmin[0])


    #print(poblacion_actual)

#Termino y muestro resultados
#plot_error(evol_error_medio)

#print("Los mejores parametros son " + str(poblacion_actual[0,:]))
sigma_in=statistics.stdev(np.subtract(datos_orig,datos_puros))

error_FIR = eval_test(datos_puros, filtrada_FIR[0])           
error_EWMA = eval_test(datos_puros, filtrada_EWMA[0]) 

plot_error(evol_error_medio, error_max, error_min, datos_puros, datos_orig, error_minomorum, error_FIR, error_EWMA)
plot_best_indN(datos_puros, crec_superman)
plot_in_out(datos_orig, agujero_techo,"dEWMA")
plot_in_out(datos_orig, filtrada_FIR[0],"FIR")
plot_in_out(datos_orig, filtrada_EWMA[0],"EWMA")

save_ind(superman)
print("Superman")
print(str(superman))

final = [error_FIR , error_EWMA, error_EWMA[-1]]
print("Error cuadratico - FIR - EWMA - dEWMA")
print(str(final))
