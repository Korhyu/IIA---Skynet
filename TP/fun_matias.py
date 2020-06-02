"""Pone las tuyas aca trolo"""

import numpy as np
import matplotlib.pyplot as plt
import math
import random

def buscarnegativos(matriz):
    for i in range(len(matriz[0,:])):
        for j in range(len(matriz[:,0])):
            if matriz[j,i] < 0:
                print("DANGER")

def select_ind(poblacion_actual,error_punt):
    #Funcion que toma la poblacion y los errores y puntajes y realiza la seleccion, mientras mas puntos mayor la seleccion de ese individuo
    #print('select_ind')
    prueba=np.concatenate((poblacion_actual, error_punt), axis=1)
    prueba=prueba[np.argsort(-1*prueba[:,7])]
    pob_sel=poblacion_actual

    suma=0
    aux_s=0
    for individuo in range(int(len(poblacion_actual[:,0]))):
        suma=suma+prueba[individuo,7]
    for individuo in range(int(len(poblacion_actual[:,0]))):
        prueba[individuo,6]=round((prueba[individuo,7]/suma)*100)
    # for individuo in range(int(len(poblacion_actual[:,0]))):
    aux = np.zeros(8*100).reshape(100,8)
    # print(prueba)
    for individuo in range(int(len(prueba[:,0]))):
        for i in range(int(prueba[individuo,6])):
            
            if aux_s > 99:
                #print('prueba')
                pass
            else:
                aux[aux_s,:]=np.copy(prueba[individuo,:])
            aux_s=aux_s+1

    for i in range(int(len(prueba[:,0]))):       
        rd=random.randrange(0,100,1)
        pob_sel[i,:]=np.copy(aux[rd,:6])
        while aux[rd,6]==0:            
            rd=random.randrange(0,100,1)
            pob_sel[i,:]=np.copy(aux[rd,:6])
            #print(aux[rd,6])
                            
    #print(pob_sel)
    #pob_ord=sorted(poblacion_actual[].score);
    # pob_ord=sorted(poblacion_actual, key=lambda individuo : individuo.score, reverse=True)
 #    #reparto los numeros y genero una nueva lista con los selecionados
 #    pob_sel=poblacion_actual                                 #Si aca no haces el copy laburas siempre con la misma lista
 #    # print('len/2',int(len(poblacion_actual[:,0])/2))
 #    for individuo in range(int(len(poblacion_actual[:,0])/2)):
 #        # print(individuo);
 #        pob_sel[individuo,:]=prueba[individuo,:6];
 #    # print('len/4',int(len(poblacion_actual[:,0])/4))
 #    for individuo in range(int(len(poblacion_actual[:,0])/4)):
 #        pob_sel[individuo+int(len(poblacion_actual)/2)]=prueba[individuo,:6];
 #    # print('len/6',int(len(poblacion_actual[:,0])/6))
 #    for individuo in range(int(math.ceil(len(poblacion_actual[:,0])/6))):
 #        pob_sel[individuo+int(len(poblacion_actual)/2)+int(len(poblacion_actual)/4)]=prueba[individuo,:6];
 #    # print('len/8',int(len(poblacion_actual[:,0])/8))
 #    rango_final=int(len(poblacion_actual[:,0]))-int(len(poblacion_actual[:,0])/2)-int(len(poblacion_actual[:,0])/4)-int(len(poblacion_actual[:,0])/6)
 # #   print('rango final',rango_final)
 #    for individuo in range(rango_final):
 #        pob_sel[individuo+int(len(poblacion_actual)/2)+int(len(poblacion_actual)/4)+int(math.floor(len(poblacion_actual[:,0])/6))]=prueba[individuo,:6];
    
    
    #envio la lista pa la proxima etapa        
    return pob_sel

    
def mate_ind(poblacion_nueva,pCruza):
    #Funcion de cruza de la poblacion
    # print(poblacion_nueva)
    aux = np.arange(6)
    aux_pasa = np.arange(6)
    cant_cruza=0
    for cruza in range(int(len(poblacion_nueva[:,0]))):
        #elijo los padres al azar
        if pCruza > (random.randrange(0, 1000, 1))/10:
            #lo separo para cruzar 
            cant_cruza=cant_cruza+1
            aux=np.vstack((aux, poblacion_nueva[cruza,:]))
            #np.vstack((ini_array, row_to_be_added) ) 
        else:
            #pasa de una
            aux_pasa=np.vstack((aux_pasa, poblacion_nueva[cruza,:]))
            #aux_pasa=np.append(aux_pasa, poblacion_nueva[cruza,:], axis=0)

    print('Cantidad de cruzas: ', cant_cruza)
    if np.ndim(aux) > 1: 
        i=len(aux[:,0])-1
        if i%2 != 0 :
            aux_pasa=np.vstack((aux_pasa, aux[i,:]))
            i=i-1
        aux_cruz=np.arange(float(6))

        while i>=2:
            #elijo el punto de quiebre al azar y lo aplico
            pQuiebre=random.randrange(1, (int(len(poblacion_nueva[0,:]))*5),1)

            for pQ in range(math.floor(pQuiebre/5)):
                aux_cruz[pQ]=aux[i,pQ]
            if pQuiebre%5 != 0:
                frac_pQuiebre=pQuiebre%5
                aux_cruz[math.floor(pQuiebre/5)]=aux[i,math.floor(pQuiebre/5)]#((aux[i,math.floor(pQuiebre/5)]frac_pQuiebre)+(aux[i-1,math.floor(pQuiebre/5)](5-frac_pQuiebre)))/5
            for pQ in range(math.ceil(pQuiebre/5),6):
                 aux_cruz[pQ]=aux[i-1,pQ] 

            aux_pasa=np.vstack((aux_pasa, aux_cruz))
            
            for pQ in range(math.floor(pQuiebre/5)):
                aux_cruz[pQ]=aux[i-1,pQ]
            if pQuiebre%5 != 0:
                frac_pQuiebre=pQuiebre-math.floor(pQuiebre/5)
                aux_cruz[math.floor(pQuiebre/5)]=aux[i-1,math.floor(pQuiebre/5)]
                #aux_cruz[math.floor(pQuiebre/5)]=((aux[i-1,math.floor(pQuiebre/5)]frac_pQuiebre)+(aux[i,math.floor(pQuiebre/5)](5-frac_pQuiebre)))/5
            for pQ in range(math.ceil(pQuiebre/5),6):
                 aux_cruz[pQ]=aux[i,pQ]

            aux_pasa=np.vstack((aux_pasa, aux_cruz))
            
            i=i-2
   
    #Debe considerar cuantos "puestos libres" hay en la proxima poblacion para no exceder el numero
    #print(len(aux_pasa[:,0]))
    return aux_pasa[1:,:]



def mutac_ind(oPob,pMuta,dMuta, Nmax, Nmin):
    #Funcion que recorre la poblacion futura y genera la mutacion en los individuos
    
    aux = oPob
    cuenta=0

    max_muta=(dMuta/100)+1
    min_muta=1-(dMuta/100)
    print('Max muta',max_muta, 'y Min Muta', min_muta)
    for total in range(len(oPob[:,0])):
        for param in range(len(oPob[0,:])):
            if pMuta > (random.randrange(0, 1000, 1))/10:
                cuenta=cuenta+1
                
                if param == 0 :
                    aux[total,param]= round(random.uniform(aux[total,param]*min_muta,aux[total,param]*max_muta))
                elif param==4 or param==5:
                    aux[total, 4] = Nmax
                    aux[total, 5] = Nmin
                else:
                    aux[total,param]= random.uniform(aux[total,param]*min_muta,aux[total,param]*max_muta)

                
                    
    print('Cantidad de parametros mutados', cuenta)


    

    return aux


'''Incertar subploteo aca como segunda parte de esta funcion a todo ponerles nombres 
    distinto de archivo con alguna diferencia para que no se pisen
    Son todas ideas eh... fijate cuales te parecen piolas y si se te ocurren mas
        -Ploteo con la señal original y sin ruido
        -Ploteo con la señal original, el mejor de la poblacion y el peor
        -Ploteo de los errores (diferencia entre señal y salida del filtro) ya estan en el vector
        -Error maximo (un color), minimo (otro color) y promedio (otro color) de la generacion

'''




























