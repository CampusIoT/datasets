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

LoRaModulations = {"DR0":12, "DR1":11, "DR2":10, "DR3":9 ,"DR4":8, "DR5":7, "DR6":7}

LRFHSSModulations = {"DR8":"MOCW137", "DR9":"MOCW137","DR10":"M0CW336", "DR11":"M0CW336"}

coding_rate_order = ['1/3', '4/8', '4/7', '4/6', '4/5', '5/6']

LoRaFrequecies = [865.9,866.1]

LRFHSSFrequencies = [868.0, 868.6]



TIEMPO_DUPLICADOS_def = datetime.timedelta(seconds=500)  
TIEMPO_CONTADORES_def = datetime.timedelta(seconds=1901)  
TIEMPO_DUPLICADOS_dev2 = datetime.timedelta(seconds=540)
TIEMPO_CONTADORES_dev2 = datetime.timedelta(seconds=1981)


custom_palette = {
    'SF12': 'blue',   # Color para el 'Mode' sf1
    'MOCW137': 'green',  # Color para el 'Mode' sf2
    'MOCW336': 'orange'  # Color para el 'Mode' sf4
}

custom_palette2 = {
    'SF12': 'blue',   # Color para el 'Mode' sf1
    'OCW137': 'green',  # Color para el 'Mode' sf2
    'OCW336': 'orange'  # Color para el 'Mode' sf4
}


def listar_archivos(directorio):
    # Obtener todos los elementos en el directorio
    elementos = os.listdir(directorio)
    
    # Filtrar para obtener solo los archivos
    archivos = [f for f in elementos if os.path.isfile(os.path.join(directorio, f))]
    
    return archivos







def findFrequentSeconds(registros):
	i = 0
	counter = {}

	while i < len(registros) - 2:
		dif = abs( registros[i][0] - registros[i + 1][0] ).total_seconds()
		i += 1

		if registros[i][1] >= registros[i+1][1]:
			continue
		if dif not in counter:
			counter[dif] = 1
		counter[dif] += 1

	#print(counter)
	#print(registros)
	frequentSeconds =  max(counter, key=lambda k: counter[k])

	return frequentSeconds,counter[frequentSeconds]

def getMissingPackagesLoRa(registros):
	frequentSeconds, frequentSeconds_val = findFrequentSeconds(registros)
	
	#Time to check for lost packages

	TIME_BETWEEN = datetime.timedelta(seconds = frequentSeconds)
	registers_lost = []

	index = 0

	while index < len(registros) - 1:
		#print(comparar_distancia(registros[index][0], registros[index + 1][0], TIME_BETWEEN, rango_error = 10))
		#print(registros[index][1] + 1 == registros[index + 1][1])
		if sp.comparar_distancia(registros[index][0], registros[index + 1][0], TIME_BETWEEN, rango_error = 10) and registros[index][1] + 1 == registros[index + 1][1]:
			index += 1
			continue

		if registros[index][1] >= registros[index + 1][1]:
			index += 1
			continue

		

		registers_lost.append([ registros[index][0] + TIME_BETWEEN, registros[index][1] + 1 , (registros[index][2] + registros[index + 1][2])/2 ])

		index += 1

		index_lost = len(registers_lost) - 1
		
		while registers_lost[index_lost][1] + 1 != registros[index][1]:
			#print("enter")
			registers_lost.append([ registers_lost[index_lost][0] + TIME_BETWEEN, registers_lost[index_lost][1] + 1, (registros[index - 1][2] + registros[index][2])/2 ])
			index_lost += 1


		if not sp.comparar_distancia(registers_lost[index_lost][0], registros[index][0], 0, rango_error = 10):
			dif = abs((registers_lost[-1][0] - registros[index][0])).total_seconds()
			#print(colored(f"inconsistency found {dif}","yellow"))

	return registers_lost



def forwarwadGetMissingPackagesLRFHSS(rowPast, rowFuture, dev):
	
	if dev == 2:
		TIEMPO_DUPLICADOS = TIEMPO_DUPLICADOS_dev2
		TIEMPO_CONTADORES = TIEMPO_CONTADORES_dev2
	else:
		TIEMPO_DUPLICADOS = TIEMPO_DUPLICADOS_def
		TIEMPO_CONTADORES = TIEMPO_CONTADORES_def

	registers_lost = []
	fecha1 = {"dt":rowPast[0],"RSSI":[2] ,"order":rowPast[-1]}
	fecha2 = {"dt":rowFuture[0],"RSSI": (rowFuture[2] + rowPast[2])/2 }

	counter = rowPast[1] + 1

	if fecha1["order"] == 0:
		#print("enter")
		nd = 1
		nc = 0
		while not (sp.comparar_distancia(fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, fecha2["dt"], 0, 30)) and not (fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES > fecha2["dt"]):
			
			if nd == nc:
				registers_lost = registers_lost + [[fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, counter, fecha2["RSSI"], 0]]
				nd += 1
			else:
				registers_lost = registers_lost + [[fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, counter, fecha2["RSSI"], 1]]
				nc += 1
			counter += 1
		

	if fecha1["order"] == 1:
		nd = 0
		nc = 1
		#print("enter")
		while not (sp.comparar_distancia(fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, fecha2["dt"], 0, 30)) and not (fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES > fecha2["dt"]):
			if nd == nc:
				registers_lost = registers_lost + [[fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, counter, fecha2["RSSI"], 1]]
				nc += 1
			else:
				registers_lost = registers_lost + [[fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, counter, fecha2["RSSI"], 0]]
				nd += 1
			counter += 1

	return registers_lost

def backwardGetMissingPackagesLRFHSS(rowPast,rowFuture, dev):

	if dev == 2:
		TIEMPO_DUPLICADOS = TIEMPO_DUPLICADOS_dev2
		TIEMPO_CONTADORES = TIEMPO_CONTADORES_dev2
	else:
		TIEMPO_DUPLICADOS = TIEMPO_DUPLICADOS_def
		TIEMPO_CONTADORES = TIEMPO_CONTADORES_def
	
	registers_lost = []

	fecha2 = {"dt":rowFuture[0], "RSII":rowFuture[2] ,"order":rowFuture[-1]}
	fecha1 = {"dt":rowPast[0], "RSSI": (rowFuture[2] + rowPast[2])/2 }

	counter = rowFuture[1] - 1
	
	if fecha2["order"] == 1:

		nd = 1
		nc = 0
		while not (sp.comparar_distancia(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, fecha1["dt"], 0, 30)) and not(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES < fecha1["dt"]):
			if nd == nc:
				registers_lost = [[fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, counter,fecha1["RSSI"], 1]] + registers_lost
				nd += 1
			else:
				registers_lost = [[fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, counter, fecha1["RSSI"], 0]] + registers_lost
				nc += 1
			counter -= 1
	if fecha2["order"] == 0:

		nd = 0
		nc = 1
		while not (sp.comparar_distancia(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, fecha1["dt"], 0, 30)) and not(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES < fecha1["dt"]):
			
			if nd == nc:
				registers_lost = [[fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, counter, fecha1["RSSI"], 0]] + registers_lost
				nc += 1
			else:
				registers_lost = [[fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, counter, fecha1["RSSI"], 1]] + registers_lost
				nd += 1
			counter -= 1

	return registers_lost

def getMissingPackagesLRFHSS(registers, dev):
	
	i = 0

	backwardRegisterLost = []
	forwardRegisterLost = []

	while i < len(registers) - 1:
		if registers[i][1] > registers[i + 1][1]:
			registros = registers[:i + 1]
			registros_left = registers[i + 1:]
			break
		i += 1

	if not(i < len(registers) - 1):
		registros = registers
		registros_left = []

	find = False
	referencePosition = 0

	while ( not find ) and ( referencePosition < len(registros) - 1 ) :
		if registros[referencePosition][1] == registros[referencePosition + 1][1]:
			find = True
		else:
			referencePosition += 1

	registros = sp.fixerLRFHSS(registros,dev, "", False)

	if find:
		
		i = referencePosition - 1
		while i >= 0:
			
			backwardRegisterLost = backwardGetMissingPackagesLRFHSS(registros[i],registros[i + 1], dev) + backwardRegisterLost
			i -= 1
			
		i = referencePosition + 2
		while i < len(registros):
			
			forwardRegisterLost = forwardRegisterLost + forwarwadGetMissingPackagesLRFHSS(registros[i - 1],registros[i], dev)
			
			i += 1

	
	resultado = backwardRegisterLost + forwardRegisterLost

	if len(registros_left) > 0:

		resultado = resultado + getMissingPackagesLRFHSS(registros_left, dev)

	return resultado








def createDirectory(directory):
	if not os.path.exists(directory):
	    os.makedirs(directory)

def meanPDRFrq(target, devTargets, labels, dimx, dimy, output):
	mode_order = ['SF12', 'MOCW137', 'MOCW336']
	length_order = ['20 bytes', '51 bytes', '100 bytes']

	directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRsFRQ"
	files = listar_archivos(directorio)
	mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/PDR_Average/FQ"
	createDirectory(mainOutputDirectory)
	#createDirectory( mainOutputDirectory )

	powerDevice = {}

	for devTarget in devTargets:

		dataSetsF = {}
		data = []

		for nameFile in files:
			nameFileSplit = nameFile.split("_")
			frq = nameFileSplit[1]
			payloadLen = nameFileSplit[2]
			mode = nameFileSplit[3]
			tranmissionPower = nameFileSplit[4]
			codingRate = nameFileSplit[5].replace("-","/")
			modulation = nameFileSplit[6]
			device = nameFileSplit[7].replace(".csv","")

			if not int(device) == devTarget:
				continue

			if not device in powerDevice:
				powerDevice[device] = []
			if not tranmissionPower in powerDevice[device]:
				powerDevice[device].append(tranmissionPower)

			configuration = f"{mode}, {payloadLen} bytes"
			
			if not frq in dataSetsF:
				dataSetsF[frq] = {}

			if not configuration in dataSetsF[frq]:
				dataSetsF[frq][configuration] = {}

			label = labels[devTarget]

			file = open(directorio + "/" + nameFile, "r")
			prom = 0
			i = 0
			for line in file:
				lineSplit = line.split(",")
				if len(lineSplit[0]) > 0:
					#dataSets[configuration].append(float(lineSplit[4]))
					prom += float(lineSplit[4])
					i += 1
			file.close()
			try:
				prom = prom/i
			except:
				continue
			
			dataSetsF[frq][configuration][codingRate] = prom

		

		for key, value in powerDevice.items():
			if len(value) > 1:
				print( colored(f"Code not prepared for multiple tranmissions powers, please execute the code multiple times, only {powerDevice[device][0]} dBm Will be analyzed", 'yellow') )


		for LRfrequency in LRFHSSFrequencies:
			temp = dataSetsF[str(LRfrequency)]

			for frequency in dataSetsF:
				if float(frequency) in LRFHSSFrequencies:
					continue
				dataSetsF[frequency] = {**dataSetsF[frequency],**temp}


		for frequency in dataSetsF:
			if float(frequency) in LRFHSSFrequencies:
				continue
			# Convertir el diccionario a un DataFrame
			data_list = []
			for config, rates in dataSetsF[frequency].items():
			    sf, length = config.split(", ")
			    for cr, pdr in rates.items():

			        data_list.append({'Mode': sf, 'length': length, 'Coding Rate': cr, 'PDR': pdr})

			df = pd.DataFrame(data_list)
			df['Coding Rate'] = pd.Categorical(df['Coding Rate'], categories=coding_rate_order, ordered=True)
			df['Mode'] = pd.Categorical(df['Mode'], categories=mode_order, ordered=True)
			df['length'] = pd.Categorical(df['length'], categories=length_order, ordered=True)

			# Crear el gráfico de líneas con seaborn
			plt.figure(figsize=(dimx, dimy))
			sns.lineplot(data=df, x='Coding Rate', y='PDR', hue='Mode', style='length', markers=True, palette = custom_palette)


			# Configurar las etiquetas y el título
			plt.xlabel('CR')
			plt.ylabel('PDR')
			plt.ylim(0.5 , 1.1)
			#plt.title(f'PDR vs Coding Rate on transmission power {powerDevice[str(devTarget)][0]} dBm')
			plt.grid(True)
			legend = plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
			plt.setp(legend.get_title(), fontsize='10', fontweight='bold')
			
			plt.tight_layout()

			createDirectory(mainOutputDirectory)
			plt.savefig(mainOutputDirectory + f"/PDR_Average_{label}_{frequency}_{powerDevice[str(devTarget)][0]}dBm.png")
			plt.close()

	print("Average PDRs on each frequency graph generated")

def meanPDR(target, devTargets, labels, dimx, dimy, output):
	mode_order = ['SF12', 'OCW137', 'OCW336']
	length_order = ['20 bytes', '51 bytes', '100 bytes']

	directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
	files = listar_archivos(directorio)
	mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/PDR_Average"
	createDirectory(mainOutputDirectory)

	powerDevice = {}
	#createDirectory( mainOutputDirectory )
	for devTarget in devTargets:
		dataSets = {}
		data = []
		for nameFile in files:
			nameFileSplit = nameFile.split("_")
			payloadLen = nameFileSplit[1]
			mode = nameFileSplit[2].replace("M","")
			tranmissionPower = nameFileSplit[3]
			codingRate = nameFileSplit[4].replace("-","/")
			modulation = nameFileSplit[5]
			device = nameFileSplit[6].replace(".csv","")
			if not device in powerDevice:
				powerDevice[device] = []
			if not tranmissionPower in powerDevice[device]:
				powerDevice[device].append(tranmissionPower)
			label = labels[devTarget]

			configuration = f"{mode}, {payloadLen} bytes"

			if not int(device) == devTarget:
				continue

			if not configuration in dataSets:
				dataSets[configuration] = {}

			file = open(directorio + "/" + nameFile, "r")
			prom = 0
			i = 0
			for line in file:
				lineSplit = line.split(",")
				if len(lineSplit[0]) > 0:
					#dataSets[configuration].append(float(lineSplit[4]))
					prom += float(lineSplit[4])
					i += 1
			file.close()
			try:
				prom = prom/i
			except:
				continue

			dataSets[configuration][codingRate] = prom


		for key, value in powerDevice.items():
			if len(value) > 1:
				print( colored(f"Code not prepared for multiple tranmissions powers, please execute the code multiple times, only {powerDevice[device][0]} dBm Will be analyzed", 'yellow') )

		# Convertir el diccionario a un DataFrame
		data_list = []
		for config, rates in dataSets.items():
		    sf, length = config.split(", ")
		    for cr, pdr in rates.items():
		        data_list.append({'Mode': sf, 'length': length, 'Coding Rate': cr, 'PDR': pdr})

		#print(data_list)

		df = pd.DataFrame(data_list)
		df['Coding Rate'] = pd.Categorical(df['Coding Rate'], categories=coding_rate_order, ordered=True)
		df['Mode'] = pd.Categorical(df['Mode'], categories=mode_order, ordered=True)
		df['length'] = pd.Categorical(df['length'], categories=length_order, ordered=True)

		# Crear el gráfico de líneas con seaborn
		plt.figure(figsize=(dimx, dimy))
		sns.lineplot(data=df, x='Coding Rate', y='PDR', hue='Mode', style='length', markers=True, palette = custom_palette2)

		# Configurar las etiquetas y el título
		plt.xlabel('CR')
		plt.ylabel('PDR')
		plt.ylim(0.5 , 1.1)
		#plt.title(f'PDR vs Coding Rate on transmission power {powerDevice[str(devTarget)][0]} dBm')
		plt.grid(True)
		legend = plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
		plt.setp(legend.get_title(), fontsize='10', fontweight='bold')
		plt.tight_layout()

		createDirectory(mainOutputDirectory)
		plt.savefig(mainOutputDirectory + f"/PDR_Average_{label}.png")
		plt.close()

	print("Average PDRs graph generated")

def PDRvsTimeLen(target, devTargets, CRTargets, labels, dimx, dimy, output,  timeGraphInterval):
	mode_order = ['SF12', 'MOCW137', 'MOCW336']
	length_order = ['20 bytes', '51 bytes', '100 bytes']

	directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
	files = listar_archivos(directorio)
	mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/PDR_vs_time/LEN"
	createDirectory(mainOutputDirectory)

	i = 1
	powerDevice = {}
	for CRTarget in CRTargets:
		for devTarget in devTargets:
			dataSets = {}
			times = {}
			pdrs = {}
			label = labels[devTarget]
			for nameFile in files:
				nameFileSplit = nameFile.split("_")
				payloadLen = nameFileSplit[1]
				mode = nameFileSplit[2]
				tranmissionPower = nameFileSplit[3]
				codingRate = nameFileSplit[4].replace("-","/")
				modulation = nameFileSplit[5]
				device = nameFileSplit[6].replace(".csv","")
				if not device in powerDevice:
					powerDevice[device] = []
				if not tranmissionPower in powerDevice[device]:
					powerDevice[device].append(tranmissionPower)
				label = labels[devTarget]

				configuration = f"{mode}, {payloadLen} bytes"

				if not int(device) == devTarget:
					continue
				
				if not CRTarget == codingRate:
					continue
				
				dataSets[configuration] = pd.read_csv(directorio+ "/" +nameFile, header=None, names=['start_time', 'end_time', 'receive', 'send', 'pdr'])

				dataSets[configuration]['start_time'] = pd.to_datetime(dataSets[configuration]['start_time'])
				dataSets[configuration]['end_time'] = pd.to_datetime(dataSets[configuration]['start_time'])

			data_list = []
			for config, data in dataSets.items():
			    #print(data)
			    #print(len(data['pdr']))

			    sf, length = config.split(", ")
			    for index in range(len(data['pdr'])):
			        #print(index)
			        data_list.append({'Mode': sf, 'length': length, 'time': data['start_time'][index], 'PDR': data['pdr'][index]})
			        data_list.append({'Mode': sf, 'length': length, 'time': data['end_time'][index], 'PDR': data['pdr'][index]})

			df = pd.DataFrame(data_list)
			#df['Coding Rate'] = pd.Categorical(df['time'], categories=coding_rate_order, ordered=True)
			df['Mode'] = pd.Categorical(df['Mode'], categories=mode_order, ordered=True)
			df['length'] = pd.Categorical(df['length'], categories=length_order, ordered=True)

			# Crear el gráfico de líneas con seaborn
			plt.figure(figsize=(dimx, dimy))
			sns.lineplot(data=df, x='time', y='PDR', hue='Mode', style='length', markers=True, palette = custom_palette)

			"""
			# Graficar los datos del primer archivo
			for key, value in dataSets.items():
				sns.lineplot(x=times[key], y=pdrs[key], marker='o', label=key)
			"""
			# Configurar el gráfico
			plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
			plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))
			plt.xlabel('Time')
			plt.ylabel('PDR')
			plt.ylim(0 , 1.1)
			plt.title('PDR vs Time')
			plt.grid(True)
			plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
			plt.tight_layout()

			codingRateToWrite = CRTarget.replace("/","-")
			plt.savefig(mainOutputDirectory + f"/PDR_vs_time_{codingRateToWrite}_{label}.png")
			plt.close()
		print(i,"/",len(CRTargets) - 1, end="\r")
		i+=1
	print("PDR vs Time on length generated")

def PDRvsTimeCR(target, devTargets, LenTargets, labels, dimx, dimy, output,  timeGraphInterval):
	mode_order = ['SF12', 'MOCW137', 'MOCW336']
	length_order = ['20 bytes', '51 bytes', '100 bytes']

	directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
	files = listar_archivos(directorio)
	mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/PDR_vs_time/CR"
	createDirectory(mainOutputDirectory)

	i = 1
	powerDevice = {}
	for LenTarget in LenTargets:
		for devTarget in devTargets:
			dataSets = {}
			times = {}
			pdrs = {}
			label = labels[devTarget]
			for nameFile in files:
				nameFileSplit = nameFile.split("_")
				payloadLen = nameFileSplit[1]
				mode = nameFileSplit[2]
				tranmissionPower = nameFileSplit[3]
				codingRate = nameFileSplit[4].replace("-","/")
				modulation = nameFileSplit[5]
				device = nameFileSplit[6].replace(".csv","")
				if not device in powerDevice:
					powerDevice[device] = []
				if not tranmissionPower in powerDevice[device]:
					powerDevice[device].append(tranmissionPower)
				label = labels[devTarget]

				configuration = f"{mode}, {codingRate}"

				if not int(device) == devTarget:
					continue
				
				if not LenTarget == payloadLen:
					continue

				dataSets[configuration] = pd.read_csv(directorio+ "/" +nameFile, header=None, names=['start_time', 'end_time', 'receive', 'send', 'pdr'])

				dataSets[configuration]['start_time'] = pd.to_datetime(dataSets[configuration]['start_time'])
				dataSets[configuration]['end_time'] = pd.to_datetime(dataSets[configuration]['start_time'])

			data_list = []
			for config, data in dataSets.items():
			    #print(data)
			    #print(len(data['pdr']))

			    sf, CR = config.split(", ")
			    for index in range(len(data['pdr'])):
			        #print(index)
			        data_list.append({'Mode': sf, 'Coding Rate': CR, 'time': data['start_time'][index], 'PDR': data['pdr'][index]})
			        data_list.append({'Mode': sf, 'Coding Rate': CR, 'time': data['end_time'][index], 'PDR': data['pdr'][index]})

			df = pd.DataFrame(data_list)
			#df['Coding Rate'] = pd.Categorical(df['time'], categories=coding_rate_order, ordered=True)
			df['Mode'] = pd.Categorical(df['Mode'], categories=mode_order, ordered=True)
			df['Coding Rate'] = pd.Categorical(df['Coding Rate'], categories=coding_rate_order, ordered=True)

			# Crear el gráfico de líneas con seaborn
			plt.figure(figsize=(dimx, dimy))
			sns.lineplot(data=df, x='time', y='PDR', hue='Mode', style='Coding Rate', markers=True, palette = custom_palette)

			"""
			# Graficar los datos del primer archivo
			for key, value in dataSets.items():
				sns.lineplot(x=times[key], y=pdrs[key], marker='o', label=key)
			"""
			# Configurar el gráfico
			plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
			plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))
			plt.xlabel('Time')
			plt.ylabel('PDR')
			plt.ylim(0, 1.1)
			plt.title('PDR vs Time')
			plt.grid(True)
			plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
			plt.tight_layout()

			
			plt.savefig(mainOutputDirectory + f"/PDR_vs_time_{LenTarget}_{label}.png")
			plt.close()
		print(i,"/",len(LenTargets) - 1, end="\r")
		i+=1
	print("PDR vs Time on Coding rate generated")



def RSSILineGraphBetweenConfigurationsLen(target, devTargets, CRTargets,labels, dimx, dimy, output,  timeGraphInterval):
	mode_order = ['SF12', 'MOCW137', 'MOCW336']
	length_order = ['20 bytes', '51 bytes', '100 bytes']

	directorio = "outputs/csv/" + target.replace(".data", "") + "/LEN"
	files = listar_archivos(directorio)
	mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/RSSI_between_configuration/LEN"
	createDirectory(mainOutputDirectory)
	i = 1
	powerDevice = {}
	for CRTarget in CRTargets:
		for devTarget in devTargets:
			dataSets = {}
			times = {}
			pdrs = {}
			label = labels[devTarget]
			for nameFile in files:
				nameFileSplit = nameFile.split("_")
				payloadLen = nameFileSplit[0]
				mode = nameFileSplit[1]
				tranmissionPower = nameFileSplit[2]
				codingRate = nameFileSplit[3].replace("-","/")
				modulation = nameFileSplit[4]
				device = nameFileSplit[5].replace(".csv","")

				if not device in powerDevice:
					powerDevice[device] = []
				if not tranmissionPower in powerDevice[device]:
					powerDevice[device].append(tranmissionPower)

				label = labels[devTarget]

				configuration = f"{mode}, {payloadLen} bytes"

				if not int(device) == devTarget:
					continue
					
				if CRTarget != codingRate:
					continue
				dataSets[configuration] = pd.read_csv(directorio+ "/" +nameFile, header=None, names=['time', 'counter', 'frequency', 'RSSI', 'offset', 'SNR', 'channel'])

				dataSets[configuration]['time'] = pd.to_datetime(dataSets[configuration]['time'])

			data_list = []
			for config, data in dataSets.items():
			    #print(data)
			    #print(len(data['pdr']))

			    sf, length = config.split(", ")
			    for index in range(len(data['offset'])):
			        #print(index)
			        data_list.append({'Mode': sf, 'length': length, 'time': data['time'][index], 'RSSI': data['RSSI'][index]})
			#print(data_list)
			df = pd.DataFrame(data_list)

			df['Mode'] = pd.Categorical(df['Mode'], categories=mode_order, ordered=True)
			df['length'] = pd.Categorical(df['length'], categories=length_order, ordered=True)

			plt.figure(figsize=(dimx, dimy))
			sns.scatterplot(data=df, x='time', y='RSSI', hue='Mode', style='length', markers=True, palette = custom_palette)

			plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
			plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))
			plt.xlabel('Time')
			plt.ylabel('RSSI dBm')
			#plt.ylim(0, 1.1)
			plt.title('RSSI vs Time')
			plt.grid(True)
			plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
			plt.tight_layout()

			# Guardar el gráfico
			CRTargetToWrite = CRTarget.replace("/","-")
			plt.savefig(mainOutputDirectory + f"/RSSI_vs_time_{CRTargetToWrite}_{label}.png")
			plt.close()
		print(i,"/",len(CRTargets) - 1, end = "\r")
		i += 1
	print("RSSI graph generated ")

def RSSILineGraphBetweenConfigurationsLenFq(target, devTargets, CRTargets, labels, dimx, dimy, output,  timeGraphInterval):
	mode_order = ['SF12', 'MOCW137', 'MOCW336']
	length_order = ['20 bytes', '51 bytes', '100 bytes']

	directorio = "outputs/csv/" + target.replace(".data", "") + "/FRQ"
	files = listar_archivos(directorio)
	mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/RSSI_between_configuration/LEN/FQ"
	createDirectory(mainOutputDirectory)

	i = 1
	powerDevice = {}
	for CRTarget in CRTargets:
		for devTarget in devTargets:
			dataSetsF = {}

			label = labels[devTarget]
			for nameFile in files:
				nameFileSplit = nameFile.split("_")

				frq = nameFileSplit[0]
				payloadLen = nameFileSplit[1]
				mode = nameFileSplit[2]
				tranmissionPower = nameFileSplit[3]
				codingRate = nameFileSplit[4].replace("-","/")
				modulation = nameFileSplit[5]
				device = nameFileSplit[6].replace(".csv","")



				if not device in powerDevice:
					powerDevice[device] = []
				if not tranmissionPower in powerDevice[device]:
					powerDevice[device].append(tranmissionPower)

				label = labels[devTarget]

				configuration = f"{mode}, {payloadLen} bytes"

				if not int(device) == devTarget:
					continue
				
				if CRTarget != codingRate:
					continue


				if not frq in dataSetsF:
					dataSetsF[frq] = {}

				
				dataSetsF[frq][configuration] = pd.read_csv(directorio+ "/" +nameFile, header=None, names=['time', 'counter', 'RSSI', 'offset', 'SNR', 'channel'])

				dataSetsF[frq][configuration]['time'] = pd.to_datetime(dataSetsF[frq][configuration]['time'])


			"""
			for LRfrequency in LRFHSSFrequencies:
				temp = dataSetsF[str(LRfrequency)]

				for frequency in dataSetsF:
					if float(frequency) in LRFHSSFrequencies:
						continue
					dataSetsF[frequency] = {**dataSetsF[frequency],**temp}
			"""

			for frequency in dataSetsF:
				"""
				if frequency in map(str,LRFHSSFrequencies):
					continue
				
				"""
				data_list = []
				for config, data in dataSetsF[frequency].items():

				    sf, length = config.split(", ")
				    for index in range(len(data['offset'])):
				        #print(index)
				        data_list.append({'Mode': sf, 'length': length, 'time': data['time'][index], 'RSSI': data['RSSI'][index]})
				#print(data_list)
				df = pd.DataFrame(data_list)

				df['Mode'] = pd.Categorical(df['Mode'], categories=mode_order, ordered=True)
				df['length'] = pd.Categorical(df['length'], categories=length_order, ordered=True)

				plt.figure(figsize=(dimx, dimy))
				sns.lineplot(data=df, x='time', y='RSSI', hue='Mode', style='length', markers=True, palette = custom_palette)

				plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
				plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))
				plt.xlabel('Time')
				plt.ylabel('RSSI dBm')
				#plt.ylim(0, 1.1)
				plt.title('RSSI vs Time')
				plt.grid(True)
				plt.legend(title='Configurations', bbox_to_anchor=(1.05, 1), loc='upper left')
				plt.tight_layout()

				codingRateToWrite = CRTarget.replace("/","-")
				plt.savefig(mainOutputDirectory + f"/RSSI_vs_time_{codingRateToWrite}_{label}_{frequency}.png")
				plt.close()
		print(i,"/",len(CRTargets) - 1, end = "\r")
		i += 1
	print("RSSI graph on each frequency generated ")




def missingPointGraph(target, dimx, dimy, output, timeGraphInterval):
    directorio = "outputs/csv/patches4/FRQ"
    fileNames = listar_archivos(directorio)
    mainOutputDirectory = "outputs/figs/" + target.replace(".data", "") + "/" + output + "/missed"
    createDirectory(mainOutputDirectory)
    i = 1

    for fileName in fileNames:
        nameFileSplit = fileName.split("_")

        frq = nameFileSplit[0]
        payloadLen = nameFileSplit[1]
        mode = nameFileSplit[2]
        tranmissionPower = nameFileSplit[3]
        codingRate = nameFileSplit[4].replace("-", "/")
        modulation = nameFileSplit[5]
        device = nameFileSplit[6].replace(".csv", "")

        with open(directorio + "/" + fileName, 'r') as csvfile:
            lector_csv = csv.reader(csvfile)
            datos = list(lector_csv)

        registros = [[datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1]), int(fila[2])] for fila in datos]

        if modulation == 'LoRa':
            try:
                registers_lost = getMissingPackagesLoRa(registros)
                #print(registers_lost)
                df1 = pd.DataFrame(registros, columns=['time', 'index', 'RSSI'])
                df2 = pd.DataFrame(registers_lost, columns=['time', 'index', 'RSSI'])
            except:
                continue
        else:
            registers_lost = getMissingPackagesLRFHSS(registros, device)

            #print(registers_lost)
            
            df1 = pd.DataFrame(registros, columns=['time', 'index', 'RSSI', 'order'])
            df2 = pd.DataFrame(registers_lost, columns=['time', 'index', 'RSSI', 'order'])
        
        df1['dataset'] = 'Received'
        df2['dataset'] = 'Missed'

        # Filtrar DataFrames vacíos o con todos los valores NA antes de concatenar
        #df_list = [df1.dropna(), df2.dropna()]
        df_list = [df1, df2]
        df_list = [df for df in df_list if not df.empty]
        
        if df_list:
            df = pd.concat(df_list)
        else:
            continue

        # Crear el gráfico
        plt.figure(figsize=(dimx, dimy))

        # Graficar Received como línea azul con zorder 1
        sns.lineplot(data=df[df['dataset'] == 'Received'], x='time', y='RSSI', hue='dataset', marker='o', zorder=1)

        # Graficar Missed como scatterplot en rojo con zorder 2 para que se dibuje encima de la línea
        sns.scatterplot(data=df[df['dataset'] == 'Missed'], x='time', y='RSSI', color='red', marker='X', zorder=2)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))
        plt.xticks(rotation=45)

        plt.title('RSSI vs Time')
        plt.xlabel('Time')
        plt.ylabel('RSSI (dBm)')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(mainOutputDirectory + '/missed_' + fileName + '.png')
        plt.close()

        print(i, "/", len(fileNames) - 1, end="\r")
        i += 1

    print("Missed point graph")




def groupedBoxWhiskerPDRGraphs(target, labels, dimx, dimy, output):

    CRs = ["4/5", "4/6", "4/7", "4/8", "5/6", "4/6", "4/8", "1/3"]
    custom_order = ['1/3', '4/8', '4/7', '4/6', '4/5', '5/6']
    
    # Definir la paleta de colores personalizada
    custom_palette = {
        'SF12': 'blue',      # Color para 'SF12'
        'MOCW137': 'green',  # Color para 'MOCW137'
        'MOCW336': 'orange'  # Color para 'MOCW336'
    }

    directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    archivos = listar_archivos(directorio)

    mainOutputDirectory = "outputs/figs/"  + target.replace(".data", "") + "/" + output + "/BoxWhisker"
    createDirectory(mainOutputDirectory)

    dataSets = {}
    fileNames = listar_archivos(directorio)

    i = 1

    for fileName in fileNames:
        nameFileSplit = fileName.split("_")

        payloadLen = nameFileSplit[1]
        mode = nameFileSplit[2]
        tranmissionPower = nameFileSplit[3]
        codingRate = nameFileSplit[4].replace("-", "/")
        modulation = nameFileSplit[5]
        device = nameFileSplit[6].replace(".csv", "")

        configuration = payloadLen + " bytes at " + labels[int(device)] + " " + tranmissionPower + " dBm"

        if configuration not in dataSets:
            dataSets[configuration] = []

        with open(directorio + "/" + fileName, "r") as file:
            for line in file:
                lineSplit = line.split(",")
                dataSets[configuration].append({"CR": codingRate, "Modulation": mode, "PDR": float(lineSplit[4])})

    for key, data in dataSets.items():
        df = pd.DataFrame(data)

        # Definir el orden personalizado para la columna CR
        df['CR'] = pd.Categorical(df['CR'], categories=custom_order, ordered=True)
        
        # Asegurar que las Modulations están en el orden correcto
        df['Modulation'] = pd.Categorical(df['Modulation'], categories=custom_palette.keys(), ordered=True)

        plt.figure(figsize=(dimx, dimy))
        sns.boxplot(x='CR', y='PDR', hue='Modulation', data=df, width=0.5, palette=custom_palette)

        plt.title(f'Packet Delivery Ratio with {key}')
        plt.xlabel('Coding Rate')
        plt.ylabel('PDR')
        plt.ylim(0, 1.1)
        plt.yticks(np.arange(0, 1.1, 0.1))

        plt.legend(title='Modulation')

        plt.savefig(mainOutputDirectory + "/BoxWhisker_" + key.replace(" ", "_") + ".png")
        plt.close()

        print(i, "/", len(fileNames) - 1, end="\r")
        i += 1

    print("Grouped box whisker graphs done")