from clases import individuo
import numpy
import csv
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
        
        return datos



def FiltroDEWMA(param):
    '''Variable: Array a calcular, N: factor de aprendizaje, gama: Velocidad de adaptacion, alfa: Coeficiente de estabilizacion, Nmax y Nmin valores limite para N'''

    N = param[0]
    gama = param[1]
    alfa = param[2]
    Nmax = param[3]
    Nmin = param[4]

    variable = []
    variable = load_data()
    


    DEWMA = numpy.array([variable[0]])
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
        DEWMA = numpy.append( DEWMA , numpy.array(a))

    return DEWMA




def run_test(param):
    #Funcion que corre los 5 parametros recividos como lista en el filtro DEWMA
    #deve devolver la curva resultado del filtro
    #este filtro debe recivir el vector de valores de contagio del COVID

    return FiltroDEWMA(param)








def plot_filtrados(pobl):
    #Funcion auxiliar para ploteo de las salidas de toda la poblacion del filtro DEWMA
    plt.plot(load_data(), 'k--', label='Datos de contagio')
    for ind in range(len(pobl)):

        legend = ' '.join(map(str, pobl[ind].param)) 

        plt.plot(pobl[ind].filtrada, label = legend)
        plt.legend()

    plt.show()