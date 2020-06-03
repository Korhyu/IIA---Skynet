"""Pone las tuyas aca trolo"""

import numpy as np
import matplotlib.pyplot as plt
import math
import random

def buscarnegativos(matriz): #Funcion para buscar errores de datos invalidos dentro del algoritmo
    for i in range(len(matriz[0,:])):
        for j in range(len(matriz[:,0])):
            if matriz[j,i] < 0:
                print("DANGER")

def select_ind(poblacion_actual,error_punt): #Recibo la los parametros del filtro (poblacion_actual) y su puntuacion (seguda columna de error_punt)
    #Funcion que toma la poblacion y los errores y puntajes y realiza la seleccion, mientras mas puntos mayor la seleccion de ese individuo
    prueba=np.concatenate((poblacion_actual, error_punt), axis=1) #concateno las dos matrices para trbajar mas comodo.
    pob_sel=np.copy(poblacion_actual) #creo una matriz auxiliar para ir cargando la poblacion seleccionada
    suma=0 #auxiliar para la suma de las puntuaciones, para luego generar la "pSel" (segun PPT de la cursada)
    aux_s=0 
    for individuo in range(int(len(poblacion_actual[:,0]))):
        suma=suma+prueba[individuo,7] #suma de la puntuacion "popF" (segun PPT de la cursada)
    for individuo in range(int(len(poblacion_actual[:,0]))):
        prueba[individuo,6]=round((prueba[individuo,7]/suma)*100) # calculo de pSel, lo guardo en la posicion 6 de la matriz ya que en esta funcion no 
    aux = np.zeros(8*100).reshape(100,8)                          # necesito el parametro que estaba en esta posicion
    for individuo in range(int(len(prueba[:,0]))):
        for i in range(int(prueba[individuo,6])):           
            if aux_s > 99:  #Esto es por las dudas de que el roredondeo de las variables aumente la cantidad
                #print('prueba')
                pass
            else:
                aux[aux_s,:]=np.copy(prueba[individuo,:]) #Voy llenando la Matriz de 100 posiciones "que es como repartir los  numeros"
            aux_s=aux_s+1
    for i in range(int(len(prueba[:,0]))):       
        rd=random.randrange(0,100,1)   #elijo uno de la matriz de 100 posiciones de manera random
        pob_sel[i,:]=np.copy(aux[rd,:6]) #lo copio a la matriz final
        while aux[rd,6]==0:            
            rd=random.randrange(0,100,1) #si por el redondeo obtendo menos de 100 posiciones relleno eligiendo mas random
            pob_sel[i,:]=np.copy(aux[rd,:6]) #lo copio a la matriz final   
    return pob_sel

    
def mate_ind(poblacion_nueva,pCruza):
    #Funcion de cruza de la poblacion
    aux = np.arange(6) # auxiliar para las cruzas
    aux_pasa = np.arange(6) #auxiliar para los que no se cruzan
    cant_cruza=0
    for cruza in range(int(len(poblacion_nueva[:,0]))): #en este for se elige quienes se cruzan 
        if pCruza > (random.randrange(0, 1000, 1))/10: #comparacion de la probabilidad de cruce
            cant_cruza=cant_cruza+1
            aux=np.vstack((aux, poblacion_nueva[cruza,:])) #agrego al "padre a cruzar"
        else:
            aux_pasa=np.vstack((aux_pasa, poblacion_nueva[cruza,:])) # agrego a los individuos que no se van a cruzar
    print('Cantidad de cruzas: ', cant_cruza)
    if np.ndim(aux) > 1: #pregrunto si hay alguno para cruzar
        i=len(aux[:,0])-1 
        if i%2 != 0 : #si hay una cantidad impar hago pasar directoa un padre. 
            aux_pasa=np.vstack((aux_pasa, aux[i,:])) #copio el ultimo padre directo
            i=i-1
        aux_cruz=np.arange(float(6)) #auxiliar pa la cruza
        while i>=2:
            pQuiebre=random.randrange(1, (int(len(poblacion_nueva[0,:]))*5),1) #calculo el punto de quiebre para la cruza
            for pQ in range(math.floor(pQuiebre/5)):
                aux_cruz[pQ]=aux[i,pQ] #lleno los paramatro hasta el punto de quiebre (padre i)
            if pQuiebre%5 != 0:
                frac_pQuiebre=pQuiebre%5 
                aux_cruz[math.floor(pQuiebre/5)]=aux[i,math.floor(pQuiebre/5)] #por ahora lleno el parametro entero en el punto de quiebre
            for pQ in range(math.ceil(pQuiebre/5),6):
                 aux_cruz[pQ]=aux[i-1,pQ] #lleno los parametro despues del punto de quiebre (padre i-1)
            aux_pasa=np.vstack((aux_pasa, aux_cruz)) # Guardo al primer hijo
            for pQ in range(math.floor(pQuiebre/5)):
                aux_cruz[pQ]=aux[i-1,pQ] #lleno los paramatro hasta el punto de quiebre (padre i-1)
            if pQuiebre%5 != 0:
                frac_pQuiebre=pQuiebre-math.floor(pQuiebre/5)
                aux_cruz[math.floor(pQuiebre/5)]=aux[i-1,math.floor(pQuiebre/5)] #por ahora lleno el parametro entero en el punto de quiebre
            for pQ in range(math.ceil(pQuiebre/5),6):
                 aux_cruz[pQ]=aux[i,pQ] #lleno los parametro despues del punto de quiebre (padre i)
            aux_pasa=np.vstack((aux_pasa, aux_cruz)) # Guardo al segundo hijo           
            i=i-2
    return aux_pasa[1:,:]



def mutac_ind(oPob,pMuta,dMuta, Nmax, Nmin):
    #Funcion que recorre la poblacion futura y genera la mutacion en los individuos   
    aux = np.copy(oPob) #auxiliar para la poblacion
    cuenta=0
    max_muta=(dMuta/100)+1 #culculo de maxima mutacion hacia arriba dMuta=taza de mutacion
    min_muta=1-(dMuta/100) #culculo de maxima mutacion hacia abajo dMuta=taza de mutacion
    print('Max muta',max_muta, 'y Min Muta', min_muta)
    for total in range(len(oPob[:,0])):
        for param in range(len(oPob[0,:])):
            if pMuta > (random.randrange(0, 1000, 1))/10: #avanzo por todos los parametros y segun la probabilidad de muta se eligen
                cuenta=cuenta+1                
                if param == 0 :
                    aux[total,param]= round(random.uniform(aux[total,param]*min_muta,aux[total,param]*max_muta)) #muto el parametro entero
                elif param==4 or param==5:
                    aux[total, 4] = Nmax
                    aux[total, 5] = Nmin
                else:
                    aux[total,param]= random.uniform(aux[total,param]*min_muta,aux[total,param]*max_muta) #muto el parametro no entero
                aux[total, 4] = Nmax #hardcodeo los limites que no los dejamos variables
                aux[total, 5] = Nmin #hardcodeo los limites que no los dejamos variables                   
    print('Cantidad de parametros mutados', cuenta)
    return aux





























