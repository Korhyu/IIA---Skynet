from producto import ollaGA
import random
import numpy
import matplotlib.pyplot as plt


#Parametros del GA
poblacion = 200                             #Tamaño de la pobacion inicial
elitismo = 0                                #A ver donde incorporar
pob_cte = 1                                 #A ver donde incorporar
generaciones = 500                          #Cantidad de generaciones a desarollar
prob_cruza = 0.3                            #Probabilidad de cruzar 2 padres
prob_mutacion = 0.05                        #Probabilidad de mutacion


#Parametros del producto
limites_diam = (0.1, 0.5)                   #Limites del diametro minima y maxima
limites_alt = (0.1, 0.5)                    #Limites de la altura minima y maxima


ollas = []

#Creacion de poblacion original ------------------------------------------------
for i in range(poblacion):
    dia = random.uniform(limites_diam[0], limites_diam[1])
    alt = random.uniform(limites_alt[0], limites_alt[1])
    #dia = limites_diam[0] + ((limites_diam[1] - limites_diam[0])/random.randint(1,100))
    #alt = limites_alt[0] + ((limites_alt[1] - limites_alt[0])/random.randint(1,100))
    
    ollas.append(ollaGA(dia,alt))
    ollas = sorted(ollas, key=lambda x: x.relVS, reverse=True)

gen_actual = []
for i in range(poblacion):
    gen_actual.append(ollaGA(ollas[i].diametro,ollas[i].alto))


for gen in range(generaciones):
    #Seleccion ----------------------------------------------------------------------
    #Ordeno la salida de acuerdo a su relacion V/S
    gen_actual = sorted(gen_actual, key=lambda x: x.relVS, reverse=True)
    #Asigno puntos en funcion de su V/S, la primera obtiene tantos puntos como
    #poblacion, mientras que la ultima solo obtiene 1 punto
    for i in range(poblacion):
        gen_actual[i].puntos = poblacion - i


    #Funcion de ajuste
    #De momento no tengo funcion de ajuste, voy a iterar la cantidad de 
    #generaciones indicadas y ver el resultado al final de las mismas


    #Cruza ------------------------------------------------------------------------
    gen_sig = []
    padres = []
    hijos = []
    #Dado el puntaje obtenido cada individuo tiene una probabilidad dada de acuerdo
    #a lo indicado mas arriba
    #Con puntos = poblacion, la probabilidad es total, de ahi en adelante baja
    for i in range(poblacion):
        gen_actual[i].prob_cruza = prob_cruza * gen_actual[i].puntos/poblacion
        numero = random.randint(0, 10000) / 10000
        if numero <= gen_actual[i].prob_cruza:
            padres.append(gen_actual[i])
            if len(padres) == 2:
                #Creo los hijos
                hijos.append(padres[0])
                hijos.append(padres[1])
                alto1 = padres[1].alto
                alto2 = padres[0].alto
                hijos[0].alto = alto1
                hijos[1].alto = alto2
                gen_sig.append(hijos[0])
                gen_sig.append(hijos[1])
                padres = []
                hijos = []
        else:
            #No es padre
            gen_sig.append(gen_actual[i])

    if len(padres) == 1:
        gen_sig.append(padres[0])
        padres = []
        
    #Mutacion
    for i in range(poblacion):
        numero = random.randint(0, 10000) / 10000
        if numero <= prob_mutacion:
            numero = random.randint(0, 1)
            if numero == 0:
                gen_sig[i].alto = random.uniform(limites_alt[0], limites_alt[1])
            else:
                gen_sig[i].diametro = random.uniform(limites_diam[0], limites_diam[1])

    #Recalculo parametros
    for i in range(poblacion):
        gen_sig[i].calc_param()
        


    #Terminados los pasos paso a la siguiente generacion
    gen_actual = gen_sig

gen_actual = sorted(gen_actual, key=lambda x: x.relVS, reverse=True)


original = []
ultima = []
volumen = []
superficie = []
diametro = []
altura = []
d_h = []


for i in range(poblacion):
    original.append(ollas[i].relVS)
    ultima.append(gen_actual[i].relVS)
    volumen.append(gen_actual[i].volumen)
    superficie.append(gen_actual[i].superficie / 10)
    diametro.append(gen_actual[i].diametro)
    altura.append(gen_actual[i].alto)
    d_h.append(diametro[i]/altura[i])



print("Diametro " + str(gen_actual[0].diametro))
print("Altura " + str(gen_actual[0].alto))
print("Volumen " + str(gen_actual[0].volumen))
print("Superficie " + str(gen_actual[0].superficie))
print("V/S " + str(gen_actual[0].volumen / gen_actual[0].superficie))

plt.plot(original,label = 'Primera')
plt.plot(ultima,label = 'Ultima')
#plt.plot(volumen,label = 'Volumen')
#plt.plot(superficie,label = 'Superficie')
#plt.plot(diametro,label = 'Diametro')
#plt.plot(altura,label = 'Altura')
#plt.plot(d_h,label = 'D/h')
plt.xlabel("Ollas")
plt.ylabel("Relacion V/S")
plt.title("Relacion Volumen / Superficie")
plt.legend()
#plt.set_xticks(numpy.arange(0, 1, 0.1))
#plt.set_yticks(numpy.arange(0, 1., 0.1))
#plt.scatter(x, y)
plt.show()


pass
