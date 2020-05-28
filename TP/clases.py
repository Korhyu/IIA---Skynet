

class individuo():
    #Parametros del filtro
    param = [0, 0, 0, 0, 0, 0]

    #Puntaje del individuo
    score = 0

    #Curva resultado del filtro
    filtrada = []
    
    #Error entre la curva real y la calculada usando el metodo que corresponda
    error = 0

    """ Alternativa
    # Para el caso del filtro por tratarse de 5 datos con nombre uso un diccionario para almacenar los valores
    # de los distintos parametros del filtro de esta forma cada individuo tiene el nombre del parametro
    parametros = dict(N=0, gamma=0, alfa=0, sigma=0, Nmax=0, Nmin=0)
    """

    
    def __init__(self, parametros=None):
        self.param = parametros


    def set_score(self, sc_ind):
        self.score = sc_ind

    def set_filt(self, filtrada):
        self.filtrada = filtrada[0].copy()          #Cargo la curva filtrada
        #self.set_param(filtrada[1])                 #Cargo los parametros despues del filtro

    def set_param(self, parametros):
        for i in range(len(parametros)):
            self.param[i] = parametros[i]

    def get_param(self):
        return self.param