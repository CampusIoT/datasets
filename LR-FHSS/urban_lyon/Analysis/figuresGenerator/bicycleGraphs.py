import xml.etree.ElementTree as ET
from math import radians, cos, sin, sqrt, atan2

import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from dateutil import parser
import datetime

import re


import shutil
import os

import argparse

import numpy as np
from scipy.optimize import curve_fit

import separator as fg


#########################################


#target = "velo5.data"  #.data file to analyze
target = "velo25.data"
devTargets = [5]        # wich device has the bycicle information? (4 for the 5th of July, 5 for the rest)
#devTargets = [4]

DRs = ["DR0","DR8","DR9"] #Wich DRs do you want to plot?

tosaveFile = "bike_25_July" #The name of the file (png) to be saved
#gpx_file = "bike_5th_july"
gpx_file = "bike_25_July" #The Gpx file to use with the data file

#Sizes of the plot
sizeX = 6.5 
sizeY = 3

#size of the y axis, if you set it as [], it will be automatic
ylim = [-145,-55]
#ylim = []

#size of the x axis, if you set it as [], it will be automatic
xlim = [-0.4,9]
#xlim = []


#########################################

#generate_interpolated_dictionary
def generar_diccionario_interpolado(Ref, Med):
    Res = {}

    # Recorrer el diccionario de mediciones (Med)

    for label, tiempos_medicion in Med.items():
        distancias_fix = []

        # Iterar sobre cada tiempo de medición
        for tiempo_medicion in tiempos_medicion:
            # Encontrar los dos tiempos de referencia más cercanos
            tiempos_referencia = list(Ref.keys())
            idx = np.searchsorted(tiempos_referencia, tiempo_medicion)

            # Si el tiempo de medición está fuera de los límites de los tiempos de referencia, saltar
            if idx == 0 or idx == len(tiempos_referencia):
                print(label)
                print(tiempo_medicion)
                print()
                continue
            
            # Obtener los dos tiempos de referencia más cercanos
            tr1 = tiempos_referencia[idx - 1]
            tr2 = tiempos_referencia[idx]

            # Obtener las distancias correspondientes
            d1 = Ref[tr1]
            d2 = Ref[tr2]

            # Calcular la distancia interpolada (usando una interpolación lineal simple)
            delta_t1 = (tiempo_medicion - tr1).total_seconds()
            delta_t2 = (tr2 - tiempo_medicion).total_seconds()
            distancia_fix = (d1 * delta_t2 + d2 * delta_t1) / (delta_t1 + delta_t2)

            # Agregar la distancia interpolada a la lista de distancias para este label
            distancias_fix.append(distancia_fix)

        # Agregar la lista de distancias fix al diccionario Res para este label
        Res[label] = distancias_fix

    return Res

#Calculate distance with coordinates
def haversine(lat1, lon1, lat2, lon2):
    # Convertir las coordenadas de grados a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Diferencias de coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula de haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Radio de la Tierra en kilómetros. Usa 6371 para kilómetros. Usa 3956 para millas.
    r = 6371
    
    # Distancia en kilómetros
    distance = r * c
    
    return distance

def mapTimeDistance(gpx_file, reference_point):
    # Parsear el archivo GPX
    tree = ET.parse(gpx_file)
    root = tree.getroot()
    
    # Espacio de nombres utilizado en el archivo GPX
    namespaces = {
        'default': 'http://www.topografix.com/GPX/1/1',
        'ns3': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'
    }
    
    # Separar las coordenadas de referencia
    ref_lat, ref_lon = map(float, reference_point.split(','))
    
    # Diccionario para almacenar los resultados
    distance_dict = {}
    
    # Recorrer todos los puntos de la ruta
    for trkpt in root.findall('.//default:trkpt', namespaces):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        time = trkpt.find('default:time', namespaces).text
        time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        time += datetime.timedelta(hours=2)
        # Calcular la distancia desde el punto de referencia
        distance = haversine(ref_lat, ref_lon, lat, lon)
        
        # Agregar al diccionario
        distance_dict[time] = distance
    
    return distance_dict

#return a list of the files in 'directorio' directory
def listar_archivos(directorio):
    # Obtener todos los elementos en el directorio
    elementos = os.listdir(directorio)
    
    # Filtrar para obtener solo los archivos
    archivos = [f for f in elementos if os.path.isfile(os.path.join(directorio, f))]
    
    return archivos

#Generate the RSSI vs distance plot
def RSSILineGraphBetweenDRs(target, devTargets, DRs, xlim = [], ylim = []):
    dataSets = {1:[] , 2:[] , 3:[] , 4:[] }
    timeSets = {1:[] , 2:[] , 3:[] , 4:[] }

    directorio = "outputs/csv/" + target.replace(".data", "") + "/DRs"  # Cambia esto al directorio que quieras listar
    
    archivos = listar_archivos(directorio)
        

    #for powerTarget in powerTargets:

    #aqui necesito encontrar la maxima y minima ganancia entre todos ellos ...
    minData = 10000000;
    maxData = -10000000;
    for devTarget in devTargets:
        for DR in DRs:
            try:
                file = open(directorio + "/" + DR + "_" + str(devTarget) + ".csv","r")
                for line in file:
                    lineSplit = line.split(",")
                    if float(lineSplit[3]) > maxData:
                        maxData = float(lineSplit[3])

                    if float(lineSplit[3]) < minData:
                        minData = float(lineSplit[3])
                file.close()
            except:
                continue
    
    for devTarget in devTargets:
        dataSets = {}
        timeSets = {}
        for DR in DRs:
            try:
                file = open(directorio + "/" + DR + "_" + str(devTarget) + ".csv","r")

                for line in file:
                    lineSplit = line.split(",")

                    dataSets.setdefault(DR, [])
                    dataSets[DR].append(float(lineSplit[3]))

                    timeSets.setdefault(DR, [])                 
                    timeSets[DR].append(lineSplit[0])

                file.close()
            except:
                print("Error en el directorio: " + directorio + "_" + DR + "_" + str(devTarget) + ".csv")
                continue
        timeDic = {}

        #print(timeSets)
        for key in timeSets:
            timeDic[key] = [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in timeSets[key]]

        distanceDic = generar_diccionario_interpolado(mapTimeDistance(gpx_file + ".gpx", "45.78630402682589,4.879759574389831"), timeDic)

        plt.figure(figsize=(sizeX, sizeY))
        DRColor = {"DR0":"blue", "DR8":"green", "DR9":"orange"}
        for key in timeSets:
            distances = distanceDic[key]
            rssi_values = dataSets[key]
            plt.plot(distanceDic[key], dataSets[key], 'o', color = DRColor[key], label=key)
            # Ajuste de la curva de tendencia (por ejemplo, polinomio de grado 1 para lineal)
            #def power_law(x, a, b):
            #    return a * np.power(x, b)
            #popt, _ = curve_fit(power_law, distances, rssi_values)

            def logx2_law(x, A, B):
                return A * np.log10(B / x**2)
            popt, _ = curve_fit(logx2_law, distances, rssi_values, p0=(1, 1))
            A_opt, B_opt = popt
            y_fit = logx2_law(np.array(distances), A_opt, B_opt)
            print(str(key) + ": RSSI = " + str(A_opt) + "*log10(" + str(B_opt) + "/x^   2)")
            #plt.plot(distances, y_fit, "--", color = DRColor[key] , label=f'Trend {key}')
            
        # Configurar el formato del eje x para mostrar fechas y horas
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        #plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))  # Ajusta el intervalo según sea necesario
        #plt.scatter(distanceDic, rssi_values)
        plt.xlabel('Distance Km')
        plt.ylabel('RSSI dBm')
        #plt.title(f'RSSI vs Distance on {label[devTarget]} and power {powerTarget} dBm')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.legend()
        plt.grid(True)
        if len(ylim)==0:
            plt.ylim(minData*1.1,maxData*0.9)
        else:
            print("ENTER")
            plt.ylim(ylim)
        if len(xlim) > 0:
            plt.xlim(xlim)
        #plt.xlim(-0.45, 8.5)
        plt.tight_layout()
        # Rotar las etiquetas del eje x para que se vean mejor
        #plt.gcf().autofmt_xdate()

        # Guardar el gráfico como una imagen
        plt.savefig(tosaveFile + ".png")
        plt.clf()
        plt.close()

        print("RSSI figures for the device " + str(devTarget) + " created.")

    print("Graphs RSSI between DRs done . . . ")

#########################################

#if four whatever reason you need to re-process the raw files you should uncomment these lines
#fg.cleanOldData(target)

#Devices separator
#fg.DevSeparator(target)

#DR separator
#fg.DRSeparator(target, devTargets)

#########################################

RSSILineGraphBetweenDRs(target, devTargets, DRs, xlim, ylim)