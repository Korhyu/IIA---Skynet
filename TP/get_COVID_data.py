import requests
import csv


url_paises = "https://api.covid19api.com/countries"
url_datos_totales = "https://api.covid19api.com/total/dayone/country/"


respuesta = requests.get(url_paises)
paises = respuesta.json()


for pais in paises:
    print(pais["Country"] + " " + pais["ISO2"])


respuesta = requests.get(url_datos_totales+"ar")
datos = respuesta.json()

with open("ar_COVID.csv", "w") as file:
    writer = csv.writer(file)
    fieldnames = ['Date', 'Confirmed','New', 'Recovered', 'Deaths']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writerow({'Date': fieldnames[0],'Confirmed': fieldnames[1], 'New': fieldnames[2],'Recovered': fieldnames[3],'Deaths': fieldnames[4]})


    for dato in datos:
        writer.writerow({'Date': dato["Date"],'Confirmed': dato["Confirmed"],'Recovered': dato["Recovered"],'Deaths': dato["Deaths"]})