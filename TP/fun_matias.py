"""Pone las tuyas aca trolo"""

import numpy as np
import matplotlib.pyplot as plt
import math
import random



def select_ind(poblacion_actual,error_punt):
    print('select_ind')
    prueba=np.concatenate((poblacion_actual, error_punt), axis=1)
    prueba=prueba[np.argsort(-1*prueba[:,7])]
    
    #pob_ord=sorted(poblacion_actual[].score);
    # pob_ord=sorted(poblacion_actual, key=lambda individuo : individuo.score, reverse=True)
    #reparto los numeros y genero una nueva lista con los selecionados
    pob_sel=poblacion_actual                                 #Si aca no haces el copy laburas siempre con la misma lista
    for individuo in range(int(len(poblacion_actual[:,0])/2)):
        # print(individuo);
        pob_sel[individuo,:]=prueba[individuo,:6];
    for individuo in range(int(len(poblacion_actual[:,0])/4)):
        pob_sel[individuo+int(len(poblacion_actual)/2)]=prueba[individuo,:6];
    for individuo in range(int(math.ceil(len(poblacion_actual[:,0])/6))):
        pob_sel[individuo+int(len(poblacion_actual)/2)+int(len(poblacion_actual)/4)]=prueba[individuo,:6];
    for individuo in range(int(math.floor(len(poblacion_actual[:,0])/8))):
        pob_sel[individuo+int(len(poblacion_actual)/2)+int(len(poblacion_actual)/4)+int(math.floor(len(poblacion_actual[:,0])/6))]=prueba[individuo,:6];
    
    
    #envio la lista pa la proxima etapa        
    return pob_sel

#-----Crear matriz
# x = np.arange(8).reshape(2, 4)    
#-----Concatenarlas
# np.concatenate((a, b.T), axis=1)
#-----estructurarlas y ordenarlas
# dtype = [('name', 'S10'), ('height', float), ('age', int)]
# values = [('Arthur', 1.8, 41), ('Lancelot', 1.9, 38),('Galahad', 1.7, 38)]
# a = np.array(values, dtype=dtype)       # create a structured array
# np.sort(a, order='height')  
#sorted_array = an_array[numpy.argsort(an_array[:, 1])]
    
def mate_ind(poblacion_nueva,pCruza,Cant_param):
    print('mate_ind')
    aux = np.arange(6)
    aux_pasa = np.arange(6)
    cant_cruza=0
    for cruza in range(int(len(poblacion_nueva[:,0]))-1):
        #elijo los padres al azar
        if pCruza > (random.randrange(0, 1000, 1))/10:
            #lo separo para cruzar 
            cant_cruza=cant_cruza+1
            # print('cruzando')
            aux=np.vstack((aux, poblacion_nueva[cruza,:]))
           # np.vstack ((ini_array, row_to_be_added) ) 
        else:
            #pasa de una
            # print('no cruzando')
            aux_pasa=np.vstack((aux_pasa, poblacion_nueva[cruza,:]))
          #  aux_pasa=np.append(aux_pasa, poblacion_nueva[cruza,:], axis=0)
         #   print('aux_pasa')
       #     print(aux_pasa)
    # print('dimenciones')
    # print(np.ndim(aux))
    print('Cantidad de cruzas: ', cant_cruza)
    if np.ndim(aux) > 1: 
        i=len(aux[:,0])-1
        # print('i')
        # print(i)
        if i%2 != 0 :
            aux_pasa=np.vstack((aux_pasa, aux[i,:]))
            i=i-1
        # print('aux_pasa')
        # print(aux_pasa)
        aux_cruz=np.arange(float(6))
        # print('aux')
        # print(aux)
        while i>=2:
            #elijo el punto de quiebre al azar y lo aplico
            pQuiebre=random.randrange(1, (Cant_param*5)-1,1)
            # print(pQuiebre)
            for pQ in range(math.floor(pQuiebre/5)):
                aux_cruz[pQ]=aux[i,pQ]
            if pQuiebre%5 != 0:
                frac_pQuiebre=pQuiebre%5
                # print('frac_pq')
                # print(frac_pQuiebre)
                aux_cruz[math.floor(pQuiebre/5)]=((aux[i,math.floor(pQuiebre/5)]*frac_pQuiebre)+(aux[i-1,math.floor(pQuiebre/5)]*(5-frac_pQuiebre)))/5
            for pQ in range(math.ceil(pQuiebre/5),6):
                 aux_cruz[pQ]=aux[i-1,pQ] 
            # print('cruza')
            # print(aux_cruz)
            aux_pasa=np.vstack((aux_pasa, aux_cruz))
            
            for pQ in range(math.floor(pQuiebre/5)):
                aux_cruz[pQ]=aux[i-1,pQ]
            if pQuiebre%5 != 0:
                frac_pQuiebre=pQuiebre-math.floor(pQuiebre/5)
                aux_cruz[math.floor(pQuiebre/5)]=((aux[i-1,math.floor(pQuiebre/5)]*frac_pQuiebre)+(aux[i,math.floor(pQuiebre/5)]*(5-frac_pQuiebre)))/5
            for pQ in range(math.ceil(pQuiebre/5),6):
                 aux_cruz[pQ]=aux[i,pQ]
            # print('cruza')
            # print(aux_cruz)
            aux_pasa=np.vstack((aux_pasa, aux_cruz))
            
            i=i-2
   
    #Debe considerar cuantos "puestos libres" hay en la proxima poblacion para no exceder el numero
    # print('aux_pasa')
    # print(aux_pasa)
    return aux_pasa



































