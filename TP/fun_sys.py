
import numpy as np
import random
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

    # Le monto una continua para ver si eso es lo que rompe el sigma
    #if st.min() < 0:
    #    st = st - st.min()


    return st

def add_noise(amp, s):
    #Agrega ruido aleatorio de amplitud especificada y desplaza la señal completa para no tener valroes negativos
    
    n = np.random.default_rng().uniform(low=-amp, high=amp, size=len(s))

    st = s + n

    #if st.min() < 0:
    #    st = st - st.min()
    
    archivo = "Señales/Señal_Pura.png"
    fig = plt.figure(figsize=(12,10))
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    plt.title('Señal Pura')
    plt.plot(s, 'k', label='Señal Pura')
    plt.grid(True)
    #plt.legend()
    plt.savefig(archivo)
    plt.close()

    archivo = "Señales/Ruido_Puro.png"
    fig = plt.figure(figsize=(12,10))
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    plt.title('Ruido Puro')
    plt.plot(n, 'k', label='Ruido Puro')
    plt.grid(True)
    #plt.legend()
    plt.savefig(archivo)
    plt.close()

    archivo = "Señales/Señal.png"
    fig = plt.figure(figsize=(12,10))
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    plt.title('Señal')
    plt.plot(st, 'k', label='Señal')
    plt.grid(True)
    #plt.legend()
    plt.savefig(archivo)
    plt.close()

    return st


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
        #sigma = 2 * (DEWMA[j-1])**(1/2)
        #sigma = 2 * (abs(DEWMA[j-1]))**(1/2)
        #sigma = sigma / (2 * (DEWMA[j-1])**(1/2))
        error = abs(variable[j]-DEWMA[j-1])
        if error > sigma:
            N = round(N/gama)
            if N < Nmin:
                N = Nmin
        if error < sigma/alfa: 
            N = round(N * gama)
            if N > Nmax:
                N = Nmax
        if N < Nmin:
            N = Nmin
        elif N > Nmax:
            N = Nmax
        Ns.append(N)
        a = DEWMA[j-1] +(variable[j]-DEWMA[j-1])/N
        DEWMA = np.append( DEWMA , np.array(a))


    param[0] = N
    param[1] = gama
    param[2] = alfa
    param[3] = sigma

    #plt.ylabel('Valor')
    #plt.xlabel('Tiempo')
    #plt.title('Evol de Ns')
    #plt.plot(Ns)
    #plt.show()

    return [DEWMA, Ns]


def FiltroFIR(N, variable):
    #Filtro FIR con N variable
    N = int(N)
    inicio = variable[0:N]
    FIR = np.zeros(N)
    FIR[N-1] = np.average(inicio)
    for j in range(0,len(variable)-N):
        a =FIR[N+j-1] +(variable[j+N]-variable[j])/N
        FIR = np.append( FIR , np.array(a ))
    return [FIR, N]


def FiltroEWMA(N, variable): 
    #Filtro EWMA con N variable
    N = int(N)
    EWMA = np.array([variable[0]])
    for j in range(1,len(variable)):
        a = EWMA[j-1] +(variable[j]-EWMA[j-1])/N
        EWMA = np.append( EWMA , np.array(a))
    return [EWMA, N]



def run_test(param, data):
    #Funcion que corre los 5 parametros recividos como lista en el filtro DEWMA
    #deve devolver la curva resultado del filtro
    #este filtro debe recivir el vector de valores de contagio del COVID

    return FiltroDEWMA(param, data)
    #return FiltroEWMA(param[0], data)
    #return FiltroFIR(param[0], data)





def plot_filtrados(pobl, orig, filtr, gen=None):
    #Funcion auxiliar para ploteo de las salidas de toda la poblacion del filtro DEWMA

    #Impresion de todos los individuos de la generacion
    archivo = "Evolucion/Gen" + str(gen) + ".png"
    fig = plt.figure(figsize=(12,10))
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    plt.title('Resultados de Generacion')

    plt.plot(orig, 'k--', label='Datos sin Ruido')
    for ind in range(len(pobl)):

        #Elimino los decimales de los parametros
        param = pobl[ind].round(decimals=2) 
        legend = ' '.join(map(str, param[0,3])) 
        plt.plot(filtr[ind], label = legend)
        
    plt.legend(loc=4)


    if archivo is None:
        plt.show()
    else:
        plt.savefig(archivo)
        plt.close()


    #Impresion del mejor y peor individuo de la generacion

    archivo = "Evolucion/GenWB" + str(gen) + ".png"
    fig = plt.figure(figsize=(12,10))
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    plt.title('Resultados Peor y Mejor de la Generacion')
    plt.plot(orig, 'k--', label='Datos sin Ruido')

    #Mejor individuo
    param = pobl[0].round(decimals=2) 
    legend = ' '.join(map(str, param)) 
    plt.plot(filtr[0], label = legend)
    #Peor individuo
    param = pobl[-1].round(decimals=2) 
    legend = ' '.join(map(str, param)) 
    plt.plot(filtr[-1], label = legend)

    plt.legend(loc=4)

    if archivo is None:
        plt.show()
    else:
        plt.savefig(archivo)
        plt.close()

    #Ploteo del mejor individuo de la generacion comparando con el FIR y el EWMA
    pass

def plot_FIR(entrada, salida_FIR, salida_DEWMA, gen, N, rango = None):
    #Funcion que plotea la salida del filtro FIR comparandola con la salida DEWMA

    if rango is not None:
        FIR = salida_FIR[rango[0]:rango[1]]
        DEWMA = salida_DEWMA[0, rango[0]: rango[1]]
        entrada = entrada[rango[0]:rango[1]]
    else:
        FIR = salida_FIR
        DEWMA = DEWMA[0,:]

    titulo = 'Comparacion entre FIR y DEWMA a igual N='
    archivo = "Evolucion/Comparacion" + str(gen) + ".png"
    fig = plt.figure(figsize=(12,10))
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    plt.title(titulo)
    plt.plot(entrada, 'k--', label='Datos sin Ruido')
    plt.plot(FIR, label = "FIR")
    plt.plot(DEWMA, label = "DEWMA")
    plt.legend(loc=4)
    plt.savefig(archivo)
    plt.close()

    
def plot_comparacion(gen, pura, DEWMA, FIR = None, EWMA = None, ran = None):
    #Ploteo las salidas de los filtros recibidos
    titulo = 'Comparacion entre filtros - Gen' + str(gen)
    archivo = "Evolucion/Comparacion" + str(gen) + ".png"
    fig = plt.figure(figsize=(12,10))
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    
    if ran is not None:
        pura = pura[ran[0] : ran[1]]
        DEWMA = DEWMA[ran[0] : ran[1]]
        FIR = FIR[ran[0] : ran[1]]
        EWMA = EWMA[ran[0] : ran[1]]

    plt.plot(pura, 'k--', label='Datos sin Ruido')
    if FIR is not None:
        plt.plot(FIR, label = "FIR")
    if EWMA is not None:
        plt.plot(EWMA, label = "EWMA")
    plt.plot(DEWMA, label = "DEWMA")

    plt.title(titulo)
    plt.legend(loc=4)
    plt.savefig(archivo)
    plt.close()

    



def plot_Ns():
    #Funcion de ploteo de la evolucion del Ns de un DEWMA y la señal de entrada al mismo

    pass

def plot_error(evol_error, error_max, error_min, datos_puros, datos_orig):
    #Funcion que genera el ploteo de la evolucion del error
    plt.figure(figsize=(14, 10))

    plt.subplot(311)
    plt.plot(datos_orig, label='Señal con ruido')
    plt.plot(datos_puros, label='Señal sin ruido')
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    plt.grid(True)
    plt.legend(loc=4)

    plt.subplot(312)
    plt.plot(evol_error, label='Medio generacional')
    plt.plot(error_max, label='Maximo generacional')
    plt.plot(error_min, label='Minimo generacional')
    plt.ylabel('Error')
    plt.xlabel('Generacion')
    plt.grid(True)
    plt.legend(loc=1)


    plt.subplot(313)
    #plt.plot(evol_error, label='Error Medio por generacion')
    plt.plot(error_min, label='Error minimo por generacion')
    plt.suptitle('Evolucion del error generacional')
    plt.ylabel('Error')
    plt.xlabel('Generacion')
    plt.grid(True)
    plt.legend(loc=1)
    plt.savefig("Evolucion/Error.png")
    plt.close()


def plot_best_indN(signal, Ns):
    '''
    archivo = "Señales/Ruido_Puro.png"
    fig = plt.figure(figsize=(12,10))
    plt.ylabel('N [muestras]')
    plt.xlabel('Tiempo')
    plt.title('Evolucion')
    plt.plot(n, 'k', label='Ruido Puro')
    
    #plt.legend()
    plt.savefig(archivo)
    plt.close()
    '''

    archivo = "Evolucion/SupermanNs.png"
    fig, ax1 = plt.subplots()
    fig = plt.figure(figsize=(12,10))
    color = 'tab:red'
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('N [muestras]', color=color)
    ax1.plot(Ns, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Señal Entrada', color=color)  # we already handled the x-label with ax1
    ax2.plot(signal, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    
    plt.grid(True)
    plt.show()
    #plt.savefig(archivo)
    plt.close()


def plot_in_out(signal, out, filtro):

    titulo = "Señal de entrada y salida del filtro " + str(filtro)
    archivo = "Señales/In_Out_" + str(filtro) + ".png"
    fig = plt.figure(figsize=(12,6))
    plt.ylabel('Valor')
    plt.xlabel('Tiempo')
    plt.plot(signal, label = "Entrada")
    plt.plot(out, label = "Salida")
    plt.title(titulo)
    plt.legend(loc=4)
    plt.savefig(archivo)
    plt.grid(True)
    plt.close()

def save_ind(ind):

    with open("ind.txt", "a") as file:
        file.write(str(ind))
        file.write('\n')
        