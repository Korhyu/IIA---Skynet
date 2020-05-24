#%%
import numpy 
# %%Definición de filtro EWMA
def FiltroFIR(N, variable):
    inicio = variable[0:N]
    FIR = numpy.zeros(N)
    FIR[N-1] = numpy.average(inicio)
    for j in range(0,len(variable)-N):
        a =FIR[N+j-1] +(variable[j+N]-variable[j])/N
        FIR = numpy.append( FIR , numpy.array(a ))
    return FIR

def FiltroEWMA(N, variable): 
    EWMA = numpy.array([variable[0]])
    for j in range(1,len(variable)):
        a = EWMA[j-1] +(variable[j]-EWMA[j-1])/N
        EWMA = numpy.append( EWMA , numpy.array(a))
    return EWMA

def FiltroDEWMA(variable, N=7, gama=1.2, alfa=1.3, Nmax=28, Nmin=7):
    '''Variable: Array a calcular, N: factor de aprendizaje, gama: Velocidad de adaptacion, alfa: Coeficiente de estabilizacion, Nmax y Nmin valores limite para N'''

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

    return [DEWMA, Ns]