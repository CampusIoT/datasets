import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from dateutil import parser
import datetime

import re

from termcolor import colored

import csv

import separator as sp

import numpy as np

import xml.etree.ElementTree as ET
from math import radians, cos, sin, sqrt, atan2



#########################################

#DRs = ["DR0","DR8","DR9"] #DRs to analyze
DRs = ["DR9"]

#   Its a list, with a touple, the first value of the touple is the raw data file, the second one is a list of 
# the devices that would be analyzed, the working touples are already set here, you only need to comment or
# uncomment the desire lines
#   It's possible to mix several raw files at the same time, for example
# targets = [("velo5.data",[4]), ("velo24.data",[5])]
# this will mix the velo5 and velo24 data files. By mix I mean that the data will be plotted one on top
# of the other one

#targets = [("velo5.data",[4])]
#targets = [("velo24.data",[5])]
targets = [("velo24nigth.data",[5])]
#targets = [("velo25.data",[5])]
#targets = [("velo25nigth.data",[5])]


#  Gpx file to be used, it need to be the one related to the previous targets, for example bike_5th_july is related with velo5.data
# otherwise an error will occur. If you are mixing several raw data, then you'll need to provide several gpx files, in that case the
# order of the gpx files in the list need to be the same one as the data files in the targerts list, for example, in the previous example
# targets = [("velo5.data",[4]), ("velo24.data",[5])]
# the gpx_file list would need to be:
# gpx_file = ["bike_5th_july", "bike_24_July"]

#gpx_file = ["bike_5th_july"]
#gpx_file = ["bike_24_July"]
gpx_file = ["bike_24_July_nigth"]
#gpx_file = ["bike_25_July"]
#gpx_file = ["bike_25_July_nigth"]



window = 7  #with how many frames should the PDR be calculated?, the higher the number the lower the resolution
windowDistance = 0.5 #Distance metters

tosaveFile = "24_July_nigth_DR9" #file will be save as 'tosaveFile + {kind of graphic}.png' on the folder 'veloFigs'


#Size of the figures
sizeX = 3 
sizeY = 2

#sizeX = 5
#sizeY = 2


YaxysOnhistogram = [0,35] #Y axis limite for the histogram figure, input an empty vector for automatic
XaxysOnhistogram = [] #X axis limite for the histogram figure, input an empty vector for automatic
bin_on_histogram = 20 # numbers of bins on the histograms

#color used on the figures
custom_palette = {
    'DR0': 'blue',    
    'DR8': 'green',  
    'DR9': 'orange'
}

# Wich plots are going to be generated
GenerateLineFigure = False
GenerateBarFillFigure = False
GenerateHistogramReceivedDistance = True
GenerateHistogramPDRDistance = False #can only bee done with one DR, otherwise an error will be prompt

#########################################


def createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def generar_diccionario_interpolado(Ref, Med):
    Res = {}
    #print(Ref)
    distancias_fix = []

    # Recorrer el diccionario de mediciones (Med)
    for register in Med:
        #print(register)
        tiempo_medicion = register[0]
        payload = register[1]

        # Encontrar los dos tiempos de referencia más cercanos
        tiempos_referencia = list(Ref.keys())
        idx = np.searchsorted(tiempos_referencia, tiempo_medicion)

        # Si el tiempo de medición está fuera de los límites de los tiempos de referencia, saltar
        if idx == 0 or idx == len(tiempos_referencia):
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

        #print(distancia_fix)
        #print()

        # Agregar la distancia interpolada a la lista de distancias para este label
        #distancias_fix.append(distancia_fix)
        distancias_fix.append([distancia_fix,payload])


    return distancias_fix


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


def listar_archivos(directorio):
    # Obtener todos los elementos en el directorio
    elementos = os.listdir(directorio)
    
    # Filtrar para obtener solo los archivos
    archivos = [f for f in elementos if os.path.isfile(os.path.join(directorio, f))]
    
    return archivos


def PDRCalculator(archivo_entrada, archivo_salida, ventana, gpx_f):
    #print(archivo_entrada)
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r') as csvfile:
        lector_csv = csv.reader(csvfile)
        datos = list(lector_csv)
    #print(archivo_entrada)
    # Extraer los contadores (segunda columna) y las horas (primera columna)
    registros = [[datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])] for fila in datos]
    #print(registros)
    registros = generar_diccionario_interpolado(mapTimeDistance(gpx_f + ".gpx", "45.78630402682589,4.879759574389831"), registros)
    #print()
    #print(registros)
    resultados = []
    
    # Calcular el PDR para cada ventana
    max_contador = max(registro[1] for registro in registros)
    inicio = registros[0][1]
    index = 0
    offset = 0

    while inicio <= max_contador:
        #print(inicio)
        fin = inicio + ventana - 1
        #paquetes_en_ventana = [registro for registro in registros if inicio <= registro[1] <= fin]
        
        paquetes_en_ventana = []

        lim = index + ventana - 1

        while index <= lim and index < len(registros) - 1:
        	paquetes_en_ventana.append(registros[index])
        	index += 1
        	if registros[index][1] <= registros[index-1][1]:
        		break


       #print(paquetes_en_ventana)

        if paquetes_en_ventana:
            hora_inicio = paquetes_en_ventana[0][0]
            hora_fin = paquetes_en_ventana[-1][0]
            max_counter = paquetes_en_ventana[-1][1]
            init_counter = paquetes_en_ventana[0][1]
            
            recibidos = len(paquetes_en_ventana)
        else:
            hora_inicio = None
            hora_fin = None
            recibidos = 0
            max_counter = 0
            init_counter = 0
        
        enviados = max_counter - init_counter + offset


        pdr = recibidos / enviados if enviados > 0 else 0
        resultados.append([hora_inicio, hora_fin, recibidos, enviados, pdr])
        
        # Actualizar el inicio para la siguiente ventana
        inicio = fin + 1
    
        offset = registros[index][1] - registros[index - 1][1]


    # Guardar los resultados en el archivo de salida
    with open(archivo_salida, 'w', newline='') as csvfile:
        escritor_csv = csv.writer(csvfile)
        #escritor_csv.writerow(['Hora Inicio', 'Hora Fin', 'Recibidos', 'Enviados', 'PDR'])
        for resultado in resultados:
            if resultado[0] and resultado[1]:
                hora_inicio_str = str(resultado[0])
                hora_fin_str = str(resultado[1])
            else:
                continue
            #hora_inicio_str = str(resultado[0]) if resultado[0] else ''
            #hora_fin_str = str(resultado[1]) if resultado[1] else ''
            if hora_inicio != '':
            	escritor_csv.writerow([hora_inicio_str, hora_fin_str, resultado[2], resultado[3], resultado[4]])

def PDRCalculator2(archivo_entrada, archivo_salida, ventana, gpx_f):
    #print(archivo_entrada)
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r') as csvfile:
        lector_csv = csv.reader(csvfile)
        datos = list(lector_csv)
    #print(archivo_entrada)
    # Extraer los contadores (segunda columna) y las horas (primera columna)
    registros = []
    for fila in datos:
        try:
            registros.append([datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])])
        except:
            continue
    #registros = [[datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])] for fila in datos]
    #print(registros)
    registros = generar_diccionario_interpolado(mapTimeDistance(gpx_f + ".gpx", "45.78630402682589,4.879759574389831"), registros)
    #print()
    #print(registros)
    resultados = []
    
    # Calcular el PDR para cada ventana
    max_contador = max(registro[1] for registro in registros)
    inicio = registros[0][1]
    index = 0
    offset = 0

    while inicio <= max_contador:
        #print(inicio)
        fin = inicio + ventana - 1

        paquetes_en_ventana = []

        lim = index + ventana - 1

        paquetes_en_ventana.append(registros[index])
        index += 1

        if index >= len(registros):
            inicio = max_contador + 1
            continue


        while registros[index][1] <= fin and index < len(registros) - 1:
            paquetes_en_ventana.append(registros[index])
            index += 1
            if registros[index][1] <= registros[index-1][1]:
                break


       #print(paquetes_en_ventana)

        if paquetes_en_ventana:
            hora_inicio = paquetes_en_ventana[0][0]
            hora_fin = paquetes_en_ventana[-1][0]

            if hora_inicio == hora_fin:
                if hora_fin > registros[index][0]:
                    hora_fin = hora_inicio - 0.001
                else:
                    hora_fin = hora_inicio + 0.001

            max_counter = paquetes_en_ventana[-1][1]
            init_counter = paquetes_en_ventana[0][1]
            
            recibidos = len(paquetes_en_ventana)
        else:
            hora_inicio = None
            hora_fin = None
            recibidos = 0
            max_counter = 0
            init_counter = 0
        
        enviados = window #max_counter - init_counter #+ offset

        inicio = fin + 1

        pdr = recibidos / enviados if enviados > 0 else 0
        resultados.append([hora_inicio, hora_fin, recibidos, enviados, pdr])
        
        if len(paquetes_en_ventana) == 0:
            continue

        if registros[index][1] - paquetes_en_ventana[-1][1] >= window:
            if hora_fin > registros[index][0]:
                resultados.append([hora_fin - 0.005, registros[index][0] + 0.005, 0, window, 0])
            else:
                resultados.append([hora_fin + 0.005, registros[index][0] - 0.005, 0, window, 0])
            #resultados.append([hora_fin - 0.005, registros[index][0] + 0.005, 0, window, 0])
            inicio = registros[index][1]

        # Actualizar el inicio para la siguiente ventana


    # Guardar los resultados en el archivo de salida
    with open(archivo_salida, 'w', newline='') as csvfile:
        escritor_csv = csv.writer(csvfile)
        #escritor_csv.writerow(['Hora Inicio', 'Hora Fin', 'Recibidos', 'Enviados', 'PDR'])
        for resultado in resultados:
            if resultado[0] and resultado[1]:
                hora_inicio_str = str(resultado[0])
                hora_fin_str = str(resultado[1])
            else:
                continue
            #hora_inicio_str = str(resultado[0]) if resultado[0] else ''
            #hora_fin_str = str(resultado[1]) if resultado[1] else ''
            if hora_inicio != '':
                escritor_csv.writerow([hora_inicio_str, hora_fin_str, resultado[2], resultado[3], resultado[4]])


def PDRCalculatorDistanceIncreasing(archivo_entrada, archivo_salida, ventana, gpx_f):
    #print(archivo_entrada)
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r') as csvfile:
        lector_csv = csv.reader(csvfile)
        datos = list(lector_csv)

    # Extraer los contadores (segunda columna) y las horas (primera columna)
    registros = []
    for fila in datos:
        try:
            registros.append([datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])])
        except:
            continue

    registros = generar_diccionario_interpolado(mapTimeDistance(gpx_f + ".gpx", "45.78630402682589,4.879759574389831"), registros)
    
    resultados = []
    
    # Calcular el PDR para cada ventana
    max_distance = max(registro[0] for registro in registros)

    #inicio = registros[0][0]
    inicio = 0
    index = 0
    offset = 0

    while index < len(registros):

        fin = inicio + ventana
        if fin > max_distance:
            fin = max_distance

        paquetes_en_ventana = []

        if index < len(registros):
            #print(index)
            paquetes_en_ventana.append(registros[index])
            index += 1

            while index < len(registros) - 1:

                paquetes_en_ventana.append(registros[index])
                index += 1
                if registros[index][0] >= fin:
                    break
        


        if paquetes_en_ventana:
            distancia_init = inicio
            if len(paquetes_en_ventana) > 1:
                distancia_fin = distancia_init + ventana if distancia_init + ventana <= max_distance else max_distance
                
            else:
                distancia_fin = distancia_init 

            if distancia_init == distancia_fin:
                distancia_fin = distancia_init + 0.001


            max_counter = paquetes_en_ventana[-1][1]
            init_counter = paquetes_en_ventana[0][1]
            
            recibidos = len(paquetes_en_ventana)

            #offset = registros[index][1] - paquetes_en_ventana[-1][1] - 1
        else:
            if inicio != max_distance:
                distancia_init = inicio
                distancia_fin = fin
            else:
                distancia_init = ''
                distancia_fin = ''
            recibidos = 0
            max_counter = 0
            init_counter = 0

            offset = 0

        enviados = max_counter -  init_counter + 1 + offset
        try:
            offset = registros[index][1] - paquetes_en_ventana[-1][1] - 1
        except:
            offset = 0

        inicio = distancia_fin + 0.001
        pdr = recibidos / enviados if enviados > 0 else 0

        resultados.append([distancia_init, distancia_fin, recibidos, enviados, pdr])

    # Guardar los resultados en el archivo de salida
    
    with open(archivo_salida, 'w', newline='') as csvfile:
        escritor_csv = csv.writer(csvfile)
        #escritor_csv.writerow(['Hora Inicio', 'Hora Fin', 'Recibidos', 'Enviados', 'PDR'])
        for resultado in resultados:
            if resultado[0] and resultado[1]:
                distancia_inicio_str = str(resultado[0])
                distancia_fin_str = str(resultado[1])
            else:
                continue
            if distancia_inicio_str != '':
                escritor_csv.writerow([distancia_inicio_str, distancia_fin_str, resultado[2], resultado[3], resultado[4]])

def PDRCalculatorDistanceDecreasing(archivo_entrada, archivo_salida, ventana, gpx_f):
    #print(archivo_entrada)
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r') as csvfile:
        lector_csv = csv.reader(csvfile)
        datos = list(lector_csv)
    #print(archivo_entrada)
    # Extraer los contadores (segunda columna) y las horas (primera columna)
    registros = []
    for fila in datos:
        try:
            registros.append([datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])])
        except:
            continue
    #registros = [[datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])] for fila in datos]
    #print(registros)
    registros = generar_diccionario_interpolado(mapTimeDistance(gpx_f + ".gpx", "45.78630402682589,4.879759574389831"), registros)
    
    #print(registros)
    
    resultados = []
    
    # Calcular el PDR para cada ventana

    inicio = registros[0][0]
    index = 0
    offset = 0

    while index < len(registros):
        #print(inicio)
        fin = inicio - ventana
        if fin < 0:
            fin = 0

        paquetes_en_ventana = []

        if registros[index][0] > fin:
            paquetes_en_ventana.append(registros[index])
            index += 1

            if index >= len(registros):
                inicio = fin - 100
                continue

            while index < len(registros) - 1:
                paquetes_en_ventana.append(registros[index])
                index += 1
                if registros[index][0] <= fin:
                    break
        
        if paquetes_en_ventana:
            distancia_init = inicio
            if len(paquetes_en_ventana) > 1:
                distancia_fin = distancia_init - ventana if distancia_init - ventana >= 0 else 0
                
            else:
                distancia_fin = distancia_init 

            if distancia_init == distancia_fin:
                distancia_fin = distancia_init - 0.001


            max_counter = paquetes_en_ventana[-1][1]
            init_counter = paquetes_en_ventana[0][1]
            
            recibidos = len(paquetes_en_ventana)

            offset = registros[index][1] - paquetes_en_ventana[-1][1] - 1
        else:
            if inicio != 0:
                distancia_init = inicio
                distancia_fin = fin
            else:
                distancia_init = ''
                distancia_fin = ''
            recibidos = 0
            max_counter = 0
            init_counter = 0

            offset = 0
        
        enviados = max_counter -  init_counter + 1 + offset

        
        inicio = distancia_fin - 0.001
        pdr = recibidos / enviados if enviados > 0 else 0

        resultados.append([distancia_init, distancia_fin, recibidos, enviados, pdr])




    # Guardar los resultados en el archivo de salida
    
    with open(archivo_salida, 'w', newline='') as csvfile:
        escritor_csv = csv.writer(csvfile)
        #escritor_csv.writerow(['Hora Inicio', 'Hora Fin', 'Recibidos', 'Enviados', 'PDR'])
        for resultado in resultados:
            if resultado[0] and resultado[1]:
                distancia_inicio_str = str(resultado[0])
                distancia_fin_str = str(resultado[1])
            else:
                continue
            if distancia_inicio_str != '':
                escritor_csv.writerow([distancia_inicio_str, distancia_fin_str, resultado[2], resultado[3], resultado[4]])

def PDRCalculatorDistance(archivo_entrada, archivo_salida, ventana, gpx_f):
    #print(archivo_entrada)
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r') as csvfile:
        lector_csv = csv.reader(csvfile)
        datos = list(lector_csv)
    #print(archivo_entrada)
    # Extraer los contadores (segunda columna) y las horas (primera columna)
    registros = []
    for fila in datos:
        try:
            registros.append([datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])])
        except:
            continue

    registros = generar_diccionario_interpolado(mapTimeDistance(gpx_f + ".gpx", "45.78630402682589,4.879759574389831"), registros)
    
    resultados = []
    #print(registros[0][0])
    #print(registros[20][0])
    if registros[0][0] < registros[20][0]:
        #print("from lab to home")
        PDRCalculatorDistanceIncreasing(archivo_entrada, archivo_salida, ventana, gpx_f)
    elif registros[0][0] > registros[20][0]:
        #print("from home to lab")
        PDRCalculatorDistanceDecreasing(archivo_entrada, archivo_salida, ventana, gpx_f)
    else:
        print("ERROR two points on the same distance")
    #print()


def calculatePDRJulyFrq(target, window, gpx_f):
    folder = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    if not os.path.exists(folder):
            os.makedirs(folder)
    	
    files = listar_archivos("outputs/csv/" + target.replace(".data", "") + "/DRs")

    for nameFile in files:

        nameFileSplit = nameFile.split("_")
        DR = nameFileSplit[0]

        if DR not in DRs:
            continue

        dev = nameFileSplit[1].replace(".csv","")

        fileToRead = "outputs/csv/" + target.replace(".data", "") + "/DRs/" + nameFile
        fileToSave1 = "outputs/csv/" + target.replace(".data", "") + "/PDRsTime/PDR_" + nameFile
        fileToSave2 = "outputs/csv/" + target.replace(".data", "") + "/PDRsDistance/PDR_" + nameFile

        createDirectory("outputs/csv/" + target.replace(".data", "") + "/PDRsTime")
        createDirectory("outputs/csv/" + target.replace(".data", "") + "/PDRsDistance")

        PDRCalculator2(fileToRead, fileToSave1, window, gpx_f)
        PDRCalculatorDistance(fileToRead, fileToSave2, windowDistance, gpx_f)

    print("PDR calculated  . . .")	


def PDRvsLen_Line(targets, dimx, dimy, output):
    DR_order = ['DR0', 'DR8', 'DR9']
    #directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    #files = listar_archivos(directorio)
    #mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/PDR_vs_LEN"
    #createDirectory(mainOutputDirectory)

    i = 1

    dataSets = {}
    times = {}
    pdrs = {}
    
    for target in targets:
        nameTarget = target[0]
        directorio = "outputs/csv/" + nameTarget.replace(".data", "") + "/PDRs"
        files = listar_archivos(directorio)
        for nameFile in files:
            nameFileSplit = nameFile.split("_")
            DR = nameFileSplit[1] + "_" + nameTarget
            device = nameFileSplit[2].replace(".csv","")
            
            dataSets[DR] = pd.read_csv(directorio+ "/" +nameFile, header=None, names=['start_time', 'end_time', 'receive', 'send', 'pdr'])
            #print(DR)


            #dataSets[DR]['start_time'] = pd.to_datetime(dataSets[DR]['start_time'])
            #dataSets[DR]['end_time'] = pd.to_datetime(dataSets[DR]['start_time'])

    data_list = []
    #print(dataSets)
    for DRid, data in dataSets.items():
        DR = DRid.split("_")[0]
        for index in range(len(data['pdr'])):
            #print(index)
            data_list.append({'DR':DR, 'time': data['start_time'][index], 'PDR': data['pdr'][index]})
            data_list.append({'DR':DR, 'time': data['end_time'][index], 'PDR': data['pdr'][index]})

    df = pd.DataFrame(data_list)
    #df['Coding Rate'] = pd.Categorical(df['time'], categories=coding_rate_order, ordered=True)
    df['DR'] = pd.Categorical(df['DR'], categories=DR_order, ordered=True)

    # Crear el gráfico de líneas con seaborn
    plt.figure(figsize=(dimx, dimy))
    sns.lineplot(data=df, x='time', y='PDR', hue='DR', markers=True, palette = custom_palette)
    sns.scatterplot(data=df, x='time', y='PDR', hue='DR', markers=True, palette = custom_palette)
    """
    # Graficar los datos del primer archivo
    for key, value in dataSets.items():
        sns.lineplot(x=times[key], y=pdrs[key], marker='o', label=key)
    """
    # Configurar el gráfico
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    #plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))
    plt.xlabel('Distance')
    plt.ylabel('PDR')
    plt.ylim(0 , 1.1)
    #plt.title('PDR vs Time')
    plt.grid(True)
    plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    #codingRateToWrite = CRTarget.replace("/","-")
    plt.savefig(f"{output}Line.png")
    plt.close()

    print("PDR vs Time on length generated")

def PDRvsLen_Line2(targets, dimx, dimy, output, xlim = []):
    DR_order = ['DR0', 'DR8', 'DR9']
    #directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    #files = listar_archivos(directorio)
    #mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/PDR_vs_LEN"
    #createDirectory(mainOutputDirectory)

    i = 1

    dataSets = {}
    times = {}
    pdrs = {}
    
    for target in targets:
        nameTarget = target[0]
        directorio = "outputs/csv/" + nameTarget.replace(".data", "") + "/PDRsDistance"
        files = listar_archivos(directorio)
        for nameFile in files:
            nameFileSplit = nameFile.split("_")
            DR = nameFileSplit[1] + "_" + nameTarget
            device = nameFileSplit[2].replace(".csv","")
            
            dataSets[DR] = pd.read_csv(directorio+ "/" +nameFile, header=None, names=['start_time', 'end_time', 'receive', 'send', 'pdr'])
            #print(DR)


            #dataSets[DR]['start_time'] = pd.to_datetime(dataSets[DR]['start_time'])
            #dataSets[DR]['end_time'] = pd.to_datetime(dataSets[DR]['start_time'])

    data_list = []
    #print(dataSets)
    for DRid, data in dataSets.items():
        DR = DRid.split("_")[0]
        for index in range(len(data['pdr'])):
            #print(index)
            data_list.append({'DR':DR, 'time': data['start_time'][index], 'PDR': data['pdr'][index]})
            data_list.append({'DR':DR, 'time': data['end_time'][index], 'PDR': data['pdr'][index]})

    df = pd.DataFrame(data_list)
    #df['Coding Rate'] = pd.Categorical(df['time'], categories=coding_rate_order, ordered=True)
    df['DR'] = pd.Categorical(df['DR'], categories=DR_order, ordered=True)

    # Crear el gráfico de líneas con seaborn
    plt.figure(figsize=(dimx, dimy))
    sns.lineplot(data=df, x='time', y='PDR', hue='DR', markers=True, palette = custom_palette)
    sns.scatterplot(data=df, x='time', y='PDR', hue='DR', markers=True, palette = custom_palette)
    """
    # Graficar los datos del primer archivo
    for key, value in dataSets.items():
        sns.lineplot(x=times[key], y=pdrs[key], marker='o', label=key)
    """
    # Configurar el gráfico
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    #plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))
    plt.xlabel('Distance')
    plt.ylabel('PDR')
    plt.ylim(0 , 1.1)
    if len(xlim)> 0:
         plt.xlim(xlim)
    #plt.title('PDR vs Time')
    plt.grid(True)
    plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    #codingRateToWrite = CRTarget.replace("/","-")
    plt.savefig(f"{output}Line.png")
    plt.close()

    print("PDR vs Time on length generated")

def PDR_vs_len_Filled_curve(targets, dimx, dimy, output):
    DR_order = ['DR0', 'DR8', 'DR9']
    #directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    #files = listar_archivos(directorio)
    #mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/PDR_vs_LEN"
    #createDirectory(mainOutputDirectory)

    i = 1

    dataSets = {}
    times = {}
    pdrs = {}
    
    for target in targets:
        nameTarget = target[0]
        directorio = "outputs/csv/" + nameTarget.replace(".data", "") + "/PDRs"
        files = listar_archivos(directorio)
        for nameFile in files:
            nameFileSplit = nameFile.split("_")
            DR = nameFileSplit[1] + "_" + nameTarget
            device = nameFileSplit[2].replace(".csv","")
            
            dataSets[DR] = pd.read_csv(directorio+ "/" +nameFile, header=None, names=['start_time', 'end_time', 'receive', 'send', 'pdr'])
            #print(DR)


            #dataSets[DR]['start_time'] = pd.to_datetime(dataSets[DR]['start_time'])
            #dataSets[DR]['end_time'] = pd.to_datetime(dataSets[DR]['start_time'])

    data_list = []
    #print(dataSets)
    for DRid, data in dataSets.items():
        DR = DRid.split("_")[0]
        for index in range(len(data['pdr'])):
            #print(index)
            data_list.append({'DR':DR, 'time': data['start_time'][index], 'PDR': data['pdr'][index]})
            data_list.append({'DR':DR, 'time': data['end_time'][index], 'PDR': data['pdr'][index]})
            data_list.append({'DR':DR, 'time': data['start_time'][index] + 0.0001, 'PDR': 0})
            data_list.append({'DR':DR, 'time': data['end_time'][index] - 0.0001, 'PDR': 0})

    df = pd.DataFrame(data_list)
    #df['Coding Rate'] = pd.Categorical(df['time'], categories=coding_rate_order, ordered=True)
    df['DR'] = pd.Categorical(df['DR'], categories=DR_order, ordered=True)

    # Crear el gráfico de líneas con seaborn
    plt.figure(figsize=(dimx, dimy))
    lineplot = sns.lineplot(data=df, x='time', y='PDR', hue='DR', markers=True, palette=custom_palette)

    # Para cada línea dibujada, agregar un área con opacidad
    for line in lineplot.get_lines():
        x_values = line.get_xdata()
        y_values = line.get_ydata()
        color = line.get_color()
        plt.fill_between(x_values, y_values, color=color, alpha=0.3)#plt.fill_between(x_values, y_values, color='blue', alpha=0.3)

    #sns.scatterplot(data=df, x='time', y='PDR', hue='DR', style='DR',markers=True, palette = custom_palette)
    """
    # Graficar los datos del primer archivo
    for key, value in dataSets.items():
        sns.lineplot(x=times[key], y=pdrs[key], marker='o', label=key)
    """
    # Configurar el gráfico
    #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    #plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))
    plt.xlabel('Distance')
    plt.ylabel('PDR')
    #plt.ylim(0 , 1.1)
    #plt.title('PDR vs Time')
    plt.grid(True)
    plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    #codingRateToWrite = CRTarget.replace("/","-")
    plt.savefig(f"{output}_FillBars.png")
    plt.close()

    print("PDR vs Time on length generated")

def PDR_vs_len_histogram(targets, dimx, dimy, output, ylim=[], xlim=[]):
    DR_order = ['DR0', 'DR8', 'DR9']
    
    dataSets = {}
    
    for target in targets:
        nameTarget = target[0]
        directorio = "outputs/csv/" + nameTarget.replace(".data", "") + "/DRs"
        files = listar_archivos(directorio)
        for nameFile in files:
            nameFileSplit = nameFile.split("_")
            DR = nameFileSplit[0] + "_" + nameTarget
            if DR.split("_")[0] not in DRs:
                continue
            device = nameFileSplit[1].replace(".csv","")

            with open(directorio + "/" + nameFile, 'r') as csvfile:
                lector_csv = csv.reader(csvfile)
                datos = list(lector_csv)

            dataSets[DR] = []
            for fila in datos:
                try:
                    dataSets[DR].append([datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])])
                except:
                    continue

            dataSets[DR] = generar_diccionario_interpolado(mapTimeDistance(gpx_f + ".gpx", "45.78630402682589,4.879759574389831"), dataSets[DR])
            
    data_list = []
    for DRid, data in dataSets.items():
        DR = DRid.split("_")[0]
        for index in range(len(data)):
            # Usamos la media entre distancia inicial y final para el histograma
            data_list.append({'DR': DR, 'distance': data[index][0], 'weigth': 1})

    df = pd.DataFrame(data_list)
    df['DR'] = pd.Categorical(df['DR'])

    # Crear el histograma con seaborn con normalización
    plt.figure(figsize=(dimx, dimy))
    histplot = sns.histplot(data=df, x='distance', weights='weigth', hue='DR', multiple="stack", 
                            palette=custom_palette, bins=20)

    # Configurar el gráfico
    plt.xlabel('Distance')
    plt.ylabel('Received frames')

    if len(ylim) > 0:
        plt.ylim(ylim)
    if len(xlim) > 0:
        plt.xlim(xlim)

    plt.grid(True)

    # Solo mostrar la leyenda si hay etiquetas
    #handles, labels = histplot.get_legend_handles_labels()
    #if labels:
        # Mover la leyenda completamente fuera del gráfico, en el lado derecho
    #    plt.legend(title='Configurations', bbox_to_anchor=(1.05, 0.5), loc='center left', borderaxespad=0)

    plt.tight_layout()

    # Guardar la figura
    plt.savefig(f"{output}_histogram.png")
    plt.close()

def PDR_vs_len_histogram2(targets, dimx, dimy, output, ylim=[], xlim=[], bin_in = 20):
    DR_order = ['DR0', 'DR8', 'DR9']
    
    dataSets = {}
    
    for target in targets:
        nameTarget = target[0]
        directorio = "outputs/csv/" + nameTarget.replace(".data", "") + "/PDRsDistance"
        files = listar_archivos(directorio)
        #mainOutputDirectory = "outputs/figs/" + nameTarget.replace(".data", "") + "/" + output + "/PDR_hist"
        #createDirectory(mainOutputDirectory)
        for nameFile in files:
            nameFileSplit = nameFile.split("_")
            DR = nameFileSplit[1] + "_" + nameTarget
            device = nameFileSplit[2].replace(".csv","")
            
            dataSets[DR] = pd.read_csv(directorio + "/" + nameFile, header=None, names=['start_distance', 'end_distance', 'receive', 'send', 'pdr'])
    
    data_list = []
    for DRid, data in dataSets.items():
        DR = DRid.split("_")[0]
        for index in range(len(data['pdr'])):
            # Usamos la media entre distancia inicial y final para el histograma
            mean_distance = (data['start_distance'][index] + data['end_distance'][index]) / 2
            data_list.append({'DR': DR, 'distance': mean_distance, 'PDR': data['pdr'][index]})

    df = pd.DataFrame(data_list)
    df['DR'] = pd.Categorical(df['DR'], categories=DR_order, ordered=True)



    # Crear el histograma con seaborn con normalización
    plt.figure(figsize=(dimx, dimy))
    histplot = sns.histplot(data=df, x='distance', weights='PDR', hue='DR', multiple="stack", 
                            palette=custom_palette, bins=bin_in)

   
    # Configurar el gráfico
    plt.xlabel('Distance')
    plt.ylabel('PDR')
    plt.title('PDR vs Distance Histogram (Normalized)')
    plt.grid(True)
    plt.xlim([0,1.1])

    plt.legend(title='DRs', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()

    # Guardar la figura
    plt.savefig(f"{output}_histogram.png")
    plt.close()

#########################################

createDirectory("veloFigs")

i = 0
for target in targets:
    nameTarget = target[0]
    device = target[1]

    sp.cleanOldData(nameTarget)

    sp.DevSeparator(nameTarget)

    sp.DRSeparator(nameTarget, device)
    gpx_f = gpx_file[i]
    calculatePDRJulyFrq(nameTarget,window, gpx_f)
    i += 1

if GenerateLineFigure:
    PDRvsLen_Line2(targets, sizeX, sizeY, "veloFigs/" + tosaveFile, XaxysOnhistogram)
if GenerateBarFillFigure:
    PDR_vs_len_Filled_curve(targets, sizeX, sizeY, "veloFigs/" + tosaveFile)
if GenerateHistogramReceivedDistance:
    PDR_vs_len_histogram(targets, sizeX, sizeY, "veloFigs/" + tosaveFile, YaxysOnhistogram, XaxysOnhistogram)
if GenerateHistogramPDRDistance:
    PDR_vs_len_histogram2(targets, sizeX, sizeY, "veloFigs/" + tosaveFile, YaxysOnhistogram, XaxysOnhistogram, bin_on_histogram)