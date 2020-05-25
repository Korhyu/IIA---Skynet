"""Pone las tuyas aca trolo"""

from clases import individuo
import numpy
import csv
import matplotlib.pyplot as plt

def select_ind(poblacion_actual):
    #voy a generar una tabla con las la "cantidad de numeros que se le reparte a cada individuo segun su score
    tabla_num=[8,8,5,5,5,5,4,4,4,4,4,4,3,3,3,3,3,3,2,2,2,2,2,2,2,2,1,1,1,1,1,1];#esta tabla sirve para mas de 32 individuos
    #pob_ord=sorted(poblacion_actual[].score);
    pob_ord=sorted(poblacion_actual, key=lambda individuo : individuo.score, reverse=True)
    #reparto los numeros y genero una nueva lista con los selecionados
    pob_sel=poblacion_actual.copy()                                 #Si aca no haces el copy laburas siempre con la misma lista
    for individuo in range(int(len(poblacion_actual)/2)):
        pob_sel[individuo]=pob_ord[individuo];
    for individuo in range(int(len(poblacion_actual)/4)):
        pob_sel[individuo+int(len(poblacion_actual)/2)]=pob_ord[individuo];   
    for individuo in range(int(len(poblacion_actual)/6)):
        pob_sel[individuo+int(len(poblacion_actual)/2)+int(len(poblacion_actual)/4)]=pob_ord[individuo];
    for individuo in range(int(len(poblacion_actual)/8)):
        pob_sel[individuo+int(len(poblacion_actual)/2)+int(len(poblacion_actual)/4)+int(len(poblacion_actual)/6)]=pob_ord[individuo];
    
    #envio la lista pa la proxima etapa        
    return pob_sel