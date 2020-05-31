import requests
import csv

pais = "ch"

url_paises = "https://api.covid19api.com/countries"
url_datos_totales = "https://api.covid19api.com/total/dayone/country/"


respuesta = requests.get(url_paises)
paises = respuesta.json()


#Imprimo los paises disponibles
for p in paises:
    print(p["Country"] + " " + p["ISO2"])


respuesta = requests.get(url_datos_totales + pais)
datos = respuesta.json()
new = 0
old = 0

archivo = pais + "_COVID.csv"

with open(archivo, "w") as file:
    writer = csv.writer(file)
    names = ['Date', 'Confirmed','New', 'Recovered', 'Deaths', 'Active']
    writer = csv.DictWriter(file, fieldnames=names)
    writer.writerow({names[0]: names[0],names[1]: names[1], names[2]: names[2],names[3]: names[3],names[4]: names[4], names[5]: names[5]})


    for dato in datos:
        new = dato["Confirmed"] - old
        writer.writerow({names[0]: dato["Date"],names[1]: dato["Confirmed"],names[2]: new ,
                        names[3]: dato["Recovered"],names[4]: dato["Deaths"], names[5]: dato["Active"]})
        old = dato["Confirmed"]