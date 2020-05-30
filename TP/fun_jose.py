from clases import individuo
import numpy as np
import csv
import math
import matplotlib.pyplot as plt

pais = "ar"


def load_data():
    #Lee los datos del archivo "ar_COVID.csv" y devuele en el vector los datos de los contagios nuevos por dia
    archivo = pais + "_COVID.csv"
    
    with open(archivo) as file:
        datos = []
        reader = csv.reader(file)
        reader = csv.DictReader(file)   #Cargo los encabezados en el lector del archivo
        #next(reader, None)              #Salteo la fila de encabezados
        for fila in reader:
            datos.append(int(fila['New']))
        
        return np.array(datos)


def gen_signal(amp, per, fases, muestras):
    # Recibe las amplitudes, periodos y fases como vectores y el numero de muestras es un int.
    # devuelve la señal como suma de todos los senos usando los parametros antes dados.
    # Los periodos indicados son la cantidad de muestras necesarias para un ciclo de senoidal

    if len(amp) != len(per) and len(amp) != len(fases):
        #Verifico que los vectores sean del mismo tamaño
        print("Los vectores de amplitud, frecuencia y fase deben tener la misma cantidad de elementos")
        return None
    
    s = np.empty([len(amp), muestras]) 

    for i in range(len(amp)):
        for j in range(muestras):
            s[i,j] = amp[i] * math.sin(2 * math.pi * j / per[i])

    st = np.empty(muestras) 
    for j in range(muestras):
        st[j] = sum(s[:,j])


    #plt.plot(s.transpose())
    #plt.plot(st)
    #plt.show()

    return st

def add_noise(amp, signal):
    
    n = np.random.normal(0, amp, size=len(signal))

    signal = signal + n

    #plt.plot(n)
    #plt.plot(signal)
    #plt.show()

    return signal


def FiltroDEWMA(param, data):
    '''Variable: Array a calcular, N: factor de aprendizaje, gama: Velocidad de adaptacion, alfa: Coeficiente de estabilizacion, Nmax y Nmin valores limite para N'''

    N = param[0]
    gama = param[1]
    alfa = param[2]
    sigma = param[3]
    Nmax = param[4]
    Nmin = param[5]

    variable = data


    DEWMA = np.array([variable[0]])
    Ns = [N]
    for j in range(1,len(variable)):
        sigma = 2 * (DEWMA[j-1])**(1/2)
        error = abs(variable[j]-DEWMA[j-1])
        if error > sigma:
            N = N/gama
            if N < Nmin:
                N = Nmin
        if error < sigma/alfa: 
            N = N * gama
            if N > Nmax:
                N = Nmax
        Ns.append(N)
        a = DEWMA[j-1] +(variable[j]-DEWMA[j-1])/N
        DEWMA = np.append( DEWMA , np.array(a))

    param[0] = N
    param[1] = gama
    param[2] = alfa
    param[3] = sigma

    return DEWMA




def run_test(param, data):
    #Funcion que corre los 5 parametros recividos como lista en el filtro DEWMA
    #deve devolver la curva resultado del filtro
    #este filtro debe recivir el vector de valores de contagio del COVID

    return FiltroDEWMA(param, data)








def plot_filtrados(pobl, curvas):
    #Funcion auxiliar para ploteo de las salidas de toda la poblacion del filtro DEWMA
    plt.plot(load_data(), 'k--', label='Datos de contagio')
    for ind in range(len(pobl)):

        legend = ' '.join(map(str, pobl[ind])) 

        plt.plot(curvas[ind], label = legend)
        plt.legend()

    plt.show()