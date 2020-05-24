#%%
import pandas as pd 
import numpy as np 
import scipy as sc 

#%%
df = pd.read_csv('Covid-19.csv')

#%%Filtro los datos para dia100>0

#dffiltrado = df[df.dia100>0]

# %%Definición de filtro EWMA
def FiltroFIR(N, variable):
    inicio = variable[0:N]
    FIR = np.zeros(N)
    FIR[N-1] = np.average(inicio)
    for j in range(0,len(variable)-N):
        a =FIR[N+j-1] +(variable[j+N]-variable[j])/N
        FIR = np.append( FIR , np.array(a ))
    return FIR


# %%
df['FIRcasos'] = FiltroFIR(7,df['casos'])
df.to_csv('Covid-19FIR.csv')
# %%
def FiltroEWMA(N, variable):
    EWMA = np.array([variable[0]])
    for j in range(1,len(variable)):
        a = EWMA[j-1] +(variable[j]-EWMA[j-1])/N
        EWMA = np.append( EWMA , np.array(a))
    return EWMA
 
# %%
df['EWMA7casos'] = FiltroEWMA(7,df['casos'])
df.to_csv('Covid-19filtros.csv')

# %%
def FiltroDEWMA(variable, N=7, gama=1.2, alfa=1.3, Nmax=28, Nmin=7):
    '''Variable: Array a calcular, N: factor de aprendizaje, gama: Velocidad de adaptacion, alfa: Coeficiente de estabilizacion, Nmax y Nmin valores limite para N'''
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

    return [DEWMA, Ns]

# %%
df['DEWMAcasos' ], df['DEWMANs'] =  FiltroDEWMA(df['casos'])
df.to_csv('Covid-19filtros.csv')

# %%
