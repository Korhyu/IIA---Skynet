"""Pone las tuyas aca trolo"""

import numpy as np
import matplotlib.pyplot as plt
import math

def select_ind(poblacion_actual,error_punt):
    
    prueba=np.concatenate((poblacion_actual, error_punt), axis=1)
    prueba=prueba[np.argsort(-1*prueba[:,7])]
    
    #pob_ord=sorted(poblacion_actual[].score);
    # pob_ord=sorted(poblacion_actual, key=lambda individuo : individuo.score, reverse=True)
    #reparto los numeros y genero una nueva lista con los selecionados
    pob_sel=poblacion_actual                                 #Si aca no haces el copy laburas siempre con la misma lista
    for individuo in range(int(len(poblacion_actual[:,0])/2)):
        print(individuo);
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
    
def mate_ind(poblacion_nueva):
    print('mate_ind')
    #Esta funcion deberia reccorer la poblacion actual e ir seleccionando los individuos a aparear
    #para crear uno nuevo
    #Debe considerar cuantos "puestos libres" hay en la proxima poblacion para no exceder el numero

    return