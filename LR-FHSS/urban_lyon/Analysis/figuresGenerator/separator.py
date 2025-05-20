import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from dateutil import parser
import datetime

import re

import csv

from termcolor import colored


LoRaModulations = {"DR0":12, "DR1":11, "DR2":10, "DR3":9 ,"DR4":8, "DR5":7, "DR6":7}

LRFHSSModulations = {"DR8":"MOCW137", "DR9":"MOCW137","DR10":"M0CW336", "DR11":"M0CW336"}

LoRaFrequecies = [865.9,866.1]

LRFHSSFrequencies = [868.0, 868.6]



def test():
	print("This is a test function to check the library")

def listar_archivos(directorio):
    # Obtener todos los elementos en el directorio
    elementos = os.listdir(directorio)
    
    # Filtrar para obtener solo los archivos
    archivos = [f for f in elementos if os.path.isfile(os.path.join(directorio, f))]
    
    return archivos

def listar_archivos_y_carpetas(directorio):
    """
    Listar todos los archivos y carpetas en un directorio dado.
    
    :param directorio: Ruta del directorio a listar.
    :return: Tupla con dos listas: 
             - La primera lista contiene los nombres de las carpetas.
             - La segunda lista contiene los nombres de los archivos.
    """
    # Obtener todos los elementos en el directorio
    elementos = os.listdir(directorio)
    
    # Filtrar para obtener solo carpetas y archivos
    carpetas = [f for f in elementos if os.path.isdir(os.path.join(directorio, f))]
    archivos = [f for f in elementos if os.path.isfile(os.path.join(directorio, f))]
    
    return carpetas, archivos

def custom_sort_key(dr):
    return int(dr[2:])

def read_first_and_last_line(file_path):
    with open(file_path, 'r') as file:
        # Leer la primera línea
        first_line = file.readline().strip()
        
        # Inicializar la última línea
        last_line = first_line
        
        # Iterar sobre las líneas restantes para encontrar la última línea
        for line in file:
            last_line = line.strip()
        
    return first_line, last_line





def isNextLine(file):
    # Obtener la posición actual en el archivo
    current_position = file.tell()
    # Intentar leer la siguiente línea
    next_line = file.readline()
    # Volver a la posición actual
    file.seek(current_position)
    # Si next_line no está vacío, significa que hay una siguiente línea




    return next_line != ''

def cleanOldData(target):
	directorio = "outputs/csv/" + target.replace(".data", "")

	directories,files = listar_archivos_y_carpetas(directorio)

	directoryAllData = {}


	for file in files:
		directoryAllData[file] = "f"

	for directory in directories:
		directoryAllData[directory] = "d"

	for key, value in directoryAllData.items():
		if value == "f" and ( (".data" in key) or (".csv" in key) ):
			os.remove(directorio + "/" + key) 
		if value == "d":
			cleanOldData(target + "/" + key)
	print(f"old data deleted on {directorio}. . .")





def DevSeparator(target):
	file = open("../files/" + target)

	folder = "outputs/csv/" + target.replace(".data", "")
	if not os.path.exists(folder):
	        os.makedirs(folder)

	for line in file:
		lineSplit = line.split(",")
		DevID = lineSplit[0][0]
		lineSplit[3] = lineSplit[3].replace("#", "")

		lineToWrite = ",".join(lineSplit[1:])
		Subfile = open(folder + "/" + DevID + ".csv","a")

		Subfile.write(lineToWrite)

		Subfile.close()

	file.close()
	print("Separated by DR and devices . . .")

def DevSeparator2(target):
	file = open("../files/" + target)

	folder = "outputs/csv/" + target.replace(".data", "")
	if not os.path.exists(folder):
	        os.makedirs(folder)

	for line in file:
		lineSplit = line.split(",")
		DevID = lineSplit[0][0]
		lenData = len(lineSplit[3])
		lineSplit[3] = lineSplit[3].replace("#", "")
		
		try:
			lineSplitSplit = lineSplit[3].split("/")
			lineSplitSplit.append(lenData)
			lineSplit[3] = "/".join(map(str,lineSplitSplit))
		except:
			pass

		lineToWrite = ",".join(lineSplit[1:])
		Subfile = open(folder + "/" + DevID + ".csv","a")

		Subfile.write(lineToWrite)

		Subfile.close()

	file.close()
	print("Separated by DR and devices . . .")

def DRSeparator(target, devTargets):
	folder = "outputs/csv/" + target.replace(".data", "") + "/DRs"
	if not os.path.exists(folder):
	        os.makedirs(folder)

	for dev in devTargets:
		dev = str(dev)
		
		file = open("outputs/csv/" + target.replace(".data", "") + "/" + dev + ".csv")

		for line in file:
			lineSplit = line.split(",")
			
			Data = ",".join(lineSplit[1:])

			DR = lineSplit[0]

			subfile = open(folder + "/" + DR + "_" + dev + ".csv","a")


			subfile.write(Data)
			subfile.close()

		file.close()

def PowerSeparator(target, devTargets):
	i = 0
	for devTarget in devTargets:
		devTargets[i] = str(devTarget)
		i += 1

	folder = "outputs/csv/" + target.replace(".data", "") + "/PWS"
	if not os.path.exists(folder):
	        os.makedirs(folder)

	DRs = []
	for i in range(0,10):
		DRs.append("DR" + str(i))


	# Ejemplo de uso
	directorio = "outputs/csv/" + target.replace(".data", "") + "/DRs"  # Cambia esto al directorio que quieras listar
	archivos = listar_archivos(directorio)

	patron = re.compile(r"^DR[0-9A-Fa-f]+_[0-9A-Fa-f]+\.csv$")

	for fileName in archivos:
		if not patron.match(fileName):
		    print("Archivo no analizable:", fileName)
		    continue


		DevID = fileName.split("_")[1].split(".")[0]
		if not (DevID in devTargets):
			continue

		file = open(directorio + "/" + fileName)

		for line in file:
			lineSplit = line.split(",")
			try:
				counter, power = lineSplit[1].split("/")
				subfile = open(folder + "/" + str(power) + "_" + fileName, "a")
				lineSplit[1] = counter
				lineToWrite = ",".join(lineSplit)
				subfile.write(lineToWrite)
				subfile.close()
			except:
				print("Line not analyzable:", line)

	    	

		file.close()
	print("Data separated by Tx power . . .")

def freqSeparator(target, devTargets, powerTargets, frequencyTargets):

	excepctionDRs = ["DR6", "DR7", "DR8", "DR9", "DR10", "DR11"]

	i = 0
	for devTarget in devTargets:
		devTargets[i] = str(devTarget)
		i += 1

	i = 0
	for powerTarget in powerTargets:
		powerTargets[i] = str(powerTarget)
		i += 1

	i = 0
	for fqs in frequencyTargets:
		frequencyTargets[i] = str(fqs)
		i += 1

	folder = "outputs/csv/" + target.replace(".data", "") + "/FQS"
	if not os.path.exists(folder):
	        os.makedirs(folder)

	DRs = []
	for i in range(0,10):
		DRs.append("DR" + str(i))


	directorio = "outputs/csv/" + target.replace(".data", "") + "/PWS"  
	archivos = listar_archivos(directorio)

	for fileName in archivos:

		power, DR, DevID =  fileName.split("_")

		DevID = DevID.replace(".csv", "")

		if not (DevID in devTargets):
			print("Device " + str(DevID) + " not analyzed")
			continue

		if not (power in powerTargets):
			print("Power " + str(power) + " not analyzed")
			continue

		file = open(directorio + "/" + fileName)

		for line in file:
			lineSplit = line.split(",")

			try:

				if not(DR in excepctionDRs):
					frq = lineSplit[2]
					#
					if not(frq in frequencyTargets):
						continue
					lineToWrite = [lineSplit[0], lineSplit[1], lineSplit[3],lineSplit[4],lineSplit[5],lineSplit[6]]
					subfile = open(folder + "/" + str(frq) + "_" + fileName, "a")
					lineToWrite = ",".join(lineToWrite)
					subfile.write(lineToWrite)
					subfile.close()
				else:
					for frq in frequencyTargets:
						lineToWrite = [lineSplit[0], lineSplit[1], lineSplit[3],lineSplit[4],lineSplit[5],lineSplit[6]]
						subfile = open(folder + "/" + str(frq) + "_" + fileName, "a")
						lineToWrite = ",".join(lineToWrite)
						subfile.write(lineToWrite)
						subfile.close()
			except:
				print("Line not analyzable:", line)

	    	

		file.close()
	print("Data separated by frq power . . .")








def modulationSeparator(target, devTargets, frequencyTargets):
	folder = "outputs/csv/" + target.replace(".data", "") + "/modulations"
	if not os.path.exists(folder):
	        os.makedirs(folder)



	for dev in devTargets:
		dev = str(dev)
		
		file = open("outputs/csv/" + target.replace(".data", "") + "/" + dev + ".csv")

		for line in file:
			lineSplit = line.split(",")

			if not str(lineSplit[3]) in map(str,frequencyTargets):
				continue

			DR = lineSplit[0]

			if DR in LoRaModulations:
				lineSplit.append(str(LoRaModulations[DR]) + "\n")
				modulation = "LoRa"
			else:
				lineSplit.append(DR.replace("UNKNOWN CODING RATE ON ","").replace("UNKNOWN CODING RATE ","") + "\n")

				if lineSplit[-1].replace("\n","") in LRFHSSModulations.keys():
					lineSplit[-1] = LRFHSSModulations[lineSplit[-1].replace("\n","")] + "\n"

				modulation = "LR-FHSS"

			lineSplit[8] = lineSplit[8].replace("\n","")
			Data = ",".join(lineSplit[1:])
			
			subfile = open(folder + "/" + modulation + "_" + dev + ".csv","a")


			subfile.write(Data)
			subfile.close()
	print("Separated by modulation . . .")

def codingRateSeparator(target, codingRateTargets):
	folder = "outputs/csv/" + target.replace(".data", "") + "/CRs"
	if not os.path.exists(folder):
	        os.makedirs(folder)
		
	files = listar_archivos("outputs/csv/" + target.replace(".data", "") + "/modulations")

	for nameFile in files:

		nameFileSplit = nameFile.split("_")
		modulation = nameFileSplit[0]
		dev = nameFileSplit[1].replace(".csv","")

		file = open("outputs/csv/" + target.replace(".data", "") + "/modulations/" + nameFile )

		for line in file:
			lineSplit = line.split(",")

			CR = lineSplit[7]

			if not str(CR) in map(str,codingRateTargets):
				continue

			lineSplit.remove(CR)
			
			Data = ",".join(lineSplit)
			
			subfile = open(folder + "/" + CR.replace("/","-") + "_" + nameFile,"a")


			subfile.write(Data)
			subfile.close()
	print("Separated by coding rate  . . .")

def PowerSeparatorJuly(target, powerTargets):
	folder = "outputs/csv/" + target.replace(".data", "") + "/PWs"
	if not os.path.exists(folder):
	        os.makedirs(folder)
		
	files = listar_archivos("outputs/csv/" + target.replace(".data", "") + "/CRs")

	for nameFile in files:

		nameFileSplit = nameFile.split("_")
		CR = nameFileSplit[0].replace("-","/")
		modulation = nameFileSplit[1]
		dev = nameFileSplit[2].replace(".csv","")

		file = open("outputs/csv/" + target.replace(".data", "") + "/CRs/" + nameFile )

		for line in file:
			lineSplit = line.split(",")
			payload = lineSplit[1].split("/")
			
			power = payload[1]
			payload.remove(power)

			lineSplit[1] = "/".join(payload)

			if not str(power) in map(str,powerTargets):
				continue

			
			Data = ",".join(lineSplit)
			
			subfile = open(folder + "/" + str(power) + "_" + nameFile,"a")


			subfile.write(Data)
			subfile.close()
	print("Separated by power  . . .")

def BWSFSeparator(target):
	folder = "outputs/csv/" + target.replace(".data", "") + "/BWsSFs"
	if not os.path.exists(folder):
	        os.makedirs(folder)
		
	files = listar_archivos("outputs/csv/" + target.replace(".data", "") + "/PWs")

	for nameFile in files:

		nameFileSplit = nameFile.split("_")
		power = nameFileSplit[0]
		CR = nameFileSplit[1].replace("-","/")
		modulation = nameFileSplit[2]
		dev = nameFileSplit[3].replace(".csv","")

		file = open("outputs/csv/" + target.replace(".data", "") + "/PWs/" + nameFile )

		for line in file:
			lineSplit = line.split(",")
			BWsOrSF = lineSplit[-1]
			
			lineSplit.remove(BWsOrSF)

			lineSplit[-1] = lineSplit[-1] + "\n"

			BWsOrSF = BWsOrSF.replace("\n","")

			Data = ",".join(lineSplit)
			
			if "CW" in BWsOrSF:
				add = ""
				if "0CW" in BWsOrSF:
					BWsOrSF = BWsOrSF.replace("0CW","OCW")
			else:
				add = "SF"
			subfile = open(folder + "/" + add + BWsOrSF + "_" + nameFile,"a")


			subfile.write(Data)
			subfile.close()
	print("Separated by OCW and spread factor  . . .")

def lengthSeparator(target, lengthTargets):
	folder = "outputs/csv/" + target.replace(".data", "") + "/LEN"
	if not os.path.exists(folder):
	        os.makedirs(folder)
		
	files = listar_archivos("outputs/csv/" + target.replace(".data", "") + "/BWsSFs")

	for nameFile in files:

		nameFileSplit = nameFile.split("_")
		BWsOrSF = nameFileSplit[0]
		power = nameFileSplit[1]
		CR = nameFileSplit[2].replace("-","/")
		modulation = nameFileSplit[3]
		dev = nameFileSplit[4].replace(".csv","")

		file = open("outputs/csv/" + target.replace(".data", "") + "/BWsSFs/" + nameFile )

		for line in file:
			lineSplit = line.split(",")
			counter,length = lineSplit[1].split("/")

			if not str(length) in map(str,lengthTargets):
				continue

			lineSplit[1] = counter

			Data = ",".join(lineSplit)
			
			subfile = open(folder + "/" + length + "_" + nameFile,"a")


			subfile.write(Data)
			subfile.close()
	print("Separated by length  . . .")

def frequencySeparatorJuly(target):

	folder = "outputs/csv/" + target.replace(".data", "") + "/FRQ"
	if not os.path.exists(folder):
	        os.makedirs(folder)
		
	files = listar_archivos("outputs/csv/" + target.replace(".data", "") + "/LEN")

	for nameFile in files:

		nameFileSplit = nameFile.split("_")
		Len = nameFileSplit[0]
		BWsOrSF = nameFileSplit[1]
		power = nameFileSplit[2]
		CR = nameFileSplit[3].replace("-","/")
		modulation = nameFileSplit[4]
		dev = nameFileSplit[5].replace(".csv","")

		file = open("outputs/csv/" + target.replace(".data", "") + "/LEN/" + nameFile )

		for line in file:
			lineSplit = line.split(",")
			
			frq = lineSplit[2]

			lineSplit.remove(frq)

			Data = ",".join(lineSplit)
			
			subfile = open(folder + "/" + frq + "_" + nameFile,"a")


			subfile.write(Data)
			subfile.close()
	print("Separated by frequency  . . .")	









def PDRGenerator(target, devTargets, powerTargets, timeInterval, frequencyTargets):

	excepctionDRs = ["DR6", "DR7", "DR8", "DR9", "DR10", "DR11"]
	frequencyTargetsCopy = []

	for frq in frequencyTargets:
		frequencyTargetsCopy.append(str(frq))
	


	minutes = timeInterval

	folder = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
	if not os.path.exists(folder):
		os.makedirs(folder)
	DRs = []
	DRs_time_marker = {}
	DRs_packet_counter = {}
	DRs_packet_counter_Rx = {}
	DRs_overtime = {}



	directorio = "outputs/csv/" + target.replace(".data", "") + "/PWS"  # Cambia esto al directorio que quieras listar
	archivos = listar_archivos(directorio)

	for DR in range(0,12):
		DRs.append("DR" + str(DR))


	for fileName in archivos:
		file = open(folder + "/PDR_" + fileName ,"w")
		file.close()

	for DR in DRs:
		DRs_time_marker[DR] = 0
		DRs_packet_counter[DR] = 0
		DRs_packet_counter_Rx[DR] = 0
		DRs_overtime[DR] = False

	#Calculando..

	for fileName in archivos:

		file = open(directorio + "/" +fileName,"r")

		power, DR, dev = fileName.split("_")

		dev = dev.replace(".csv", "")

		i = 0
		for dev in devTargets:
			devTargets[i] = int(dev)
			i += 1

		i = 0
		for power in powerTargets:
			powerTargets[i] = int(power)
			i += 1


		if not ( (DR in DRs) and ( int(power) in powerTargets ) and ( int(dev) in devTargets ) ):
			print(fileName + " will not be analyzed . . . ")
			file.close()
			continue

		DRs_packet_counter = {}
		for frq in frequencyTargetsCopy:
			DRs_packet_counter[frq] = {"counter" : 0, "receivedCounter" : 0, "offsetCounter":0, "packetSended": 0}

		excepctionFrq = ["868.0","868.6"]
		for frq in excepctionFrq:
			DRs_packet_counter[frq] = {"counter" : 0, "receivedCounter" : 0, "offsetCounter":0, "packetSended": 0}
		
		DRs_time_marker = 0
		totalPacketCounter = 0


		formato = "%Y-%m-%d %H:%M:%S"
		fechaCorte_str = "2024-06-28 10:40:36"
		fechaCorte = datetime.datetime.strptime(fechaCorte_str, formato)
		pendant = {}
		for frq in frequencyTargetsCopy:
			pendant[frq] = True
		
		for frq in excepctionFrq:
			pendant[frq] = True

		for line in file:

			lineSplit = line.split(",")


			fechaLinea = datetime.datetime.strptime(lineSplit[0], formato)
			fecha_datetime = parser.isoparse(lineSplit[0])
			
			frq = lineSplit[2] 

			if not(frq in frequencyTargetsCopy) and not( DR in excepctionDRs ):
				print(f"frequency {frq} will be ignored for the PDR calculation. . .")
				continue

			#EXCEPTION 1
			if (fechaLinea >= fechaCorte) and pendant[frq]:
				#print( f"REINICIO DEL SERVIDOR A LAS {lineSplit[0]}" )
				totalPacketCounter = 0
				DRs_time_marker = fecha_datetime
				pendant[frq] = False

				DRs_packet_counter[frq] = {"counter" : 0, "receivedCounter" : int(lineSplit[1]), "offsetCounter":int(lineSplit[1]), "packetSended": 0}

				for frq_ in frequencyTargetsCopy:
					totalPacketCounter += DRs_packet_counter[frq_]["counter"]

				for frq_ in excepctionFrq:
					totalPacketCounter += DRs_packet_counter[frq_]["counter"]

				#for frq_ in frequencyTargetsCopy:
				#	DRs_packet_counter[frq_] = {"counter" : 0, "receivedCounter" : int(lineSplit[1]), "offsetCounter":int(lineSplit[1]), "packetSended": 0}
				
				#for frq_ in excepctionFrq:
				#	DRs_packet_counter[frq_] = {"counter" : 0, "receivedCounter" : int(lineSplit[1]), "offsetCounter":int(lineSplit[1]), "packetSended": 0}

				#if("PDR_2_DR2_1.csv" == "PDR_" + fileName):
				#	print(DRs_packet_counter)


			#EXCEPTION 2
			if int(lineSplit[1]) <= DRs_packet_counter[frq]["receivedCounter"]:
				#print( f"REINICIO DEL DISPOSITIVO A LAS {lineSplit[0]}" )
				totalPacketCounter = 0
				DRs_time_marker = 0
				for frq_ in frequencyTargetsCopy:
					DRs_packet_counter[frq_] = {"counter" : 0, "receivedCounter" : 0, "offsetCounter":0, "packetSended": 0}
				for frq_ in excepctionFrq:
					DRs_packet_counter[frq_] = {"counter" : 0, "receivedCounter" : 0, "offsetCounter":0, "packetSended": 0}

			
			if DRs_time_marker == 0:
				DRs_time_marker = fecha_datetime

			deltaTime = fecha_datetime - DRs_time_marker

			if DRs_packet_counter[frq]["offsetCounter"] == 0:
					DRs_packet_counter[frq]["offsetCounter"] = 1 #int(lineSplit[1])

			totalPacketCounter += 1
			if deltaTime >= datetime.timedelta(minutes = minutes):
				DRs_packet_counter[frq]["receivedCounter"] =int(lineSplit[1])
				DRs_packet_counter[frq]["counter"] += 1
				#if("PDR_2_DR2_1.csv" == "PDR_" + fileName):
				#	print(DRs_packet_counter)

				

				for frq_ in frequencyTargetsCopy:
					if DRs_packet_counter[frq_]["counter"] != 0:
						DRs_packet_counter[frq_]["packetSended"] = DRs_packet_counter[frq_]["receivedCounter"] - DRs_packet_counter[frq_]["offsetCounter"] + 1
					else:
						if not(DR in excepctionDRs):
							print(f"no data was received on the receive window on frequency {frq_} on {dev} on power {power} on DR {DR}")

				for frq_ in excepctionFrq:
					if DRs_packet_counter[frq_]["counter"] != 0:
						DRs_packet_counter[frq_]["packetSended"] = DRs_packet_counter[frq_]["receivedCounter"] - DRs_packet_counter[frq_]["offsetCounter"] + 1

				#totalPacketCounter = 0
				totalPacketSended = 0
				for frq_ in frequencyTargetsCopy:
					if DRs_packet_counter[frq_]["counter"] != 0:
						#if("PDR_2_DR2_1.csv" == "PDR_" + fileName):
						#	print(frq_)
						#	print(DRs_packet_counter[frq_]["packetSended"])
						totalPacketSended += DRs_packet_counter[frq_]["packetSended"]

				for frq_ in excepctionFrq:

					if DRs_packet_counter[frq_]["counter"] != 0:
						#if("PDR_2_DR2_1.csv" == "PDR_" + fileName):
						#	print(frq_)
						#	print(DRs_packet_counter[frq_]["packetSended"])
						totalPacketSended += DRs_packet_counter[frq_]["packetSended"]

				#print("//")
				#print(totalPacketCounter)
				#print(totalPacketSended)

				PDR = totalPacketCounter/totalPacketSended
				
				

				file_sep = open(folder + "/PDR_" + fileName,"a")

				
				
				file_sep.write(str(fecha_datetime) + "," + str(PDR) + "," + str(totalPacketCounter) + "," + str(totalPacketSended) + "," + str(DRs_time_marker) + "\n")


				file_sep.close()

				for frq_ in frequencyTargetsCopy:
					DRs_packet_counter[frq_]["offsetCounter"] = DRs_packet_counter[frq_]["receivedCounter"] + 1
					DRs_packet_counter[frq_]["counter"] = 0

				for frq_ in excepctionFrq:
					DRs_packet_counter[frq_]["offsetCounter"] = DRs_packet_counter[frq_]["receivedCounter"] + 1
					DRs_packet_counter[frq_]["counter"] = 0
				
				DRs_packet_counter[frq]["counter"] = 0
				
				totalPacketCounter = 0
				DRs_time_marker = fecha_datetime
				#print("PDR: " + str(PDR))
			else:

				DRs_packet_counter[frq]["counter"] += 1
				DRs_packet_counter[frq]["receivedCounter"] = int(lineSplit[1])


		file.close()
	print("PDRs files generated . . .")

def PDRGeneratorWhitFQ(target, devTargets, powerTargets, timeInterval):
	minutes = timeInterval

	folder = "outputs/csv/" + target.replace(".data", "") + "/PDRsFq"
	if not os.path.exists(folder):
		os.makedirs(folder)
	DRs = []
	DRs_time_marker = {}
	DRs_packet_counter = {}
	DRs_packet_counter_Rx = {}
	DRs_overtime = {}



	directorio = "outputs/csv/" + target.replace(".data", "") + "/FQS"  # Cambia esto al directorio que quieras listar
	archivos = listar_archivos(directorio)

	for DR in range(0,12):
		DRs.append("DR" + str(DR))


	for fileName in archivos:
		file = open(folder + "/PDR_" + fileName ,"w")
		file.close()

	for DR in DRs:
		DRs_time_marker[DR] = 0
		DRs_packet_counter[DR] = 0
		DRs_packet_counter_Rx[DR] = 0
		DRs_overtime[DR] = False

	#Calculando..

	for fileName in archivos:

		file = open(directorio + "/" +fileName,"r")

		fqs, power, DR, dev = fileName.split("_")
		dev = dev.replace(".csv", "")

		i = 0

		for dev in devTargets:
			devTargets[i] = int(dev)
			i += 1




		i = 0

		for power in powerTargets:
			powerTargets[i] = int(power)
			i += 1

		if not(( DR in DRs ) and ( int(power) in powerTargets ) and ( int(dev) in devTargets ) ):
			file.close()
			print(fileName + " will not be analyzed . . . ")
			continue
		
		
		DRs_packet_counter[DR] = 0
		DRs_time_marker[DR] = 0
		
		formato = "%Y-%m-%d %H:%M:%S"
		fechaCorte_str = "2024-06-28 10:40:36"
		fechaCorte = datetime.datetime.strptime(fechaCorte_str, formato)
		pendant = True
		dataCache = 0

		for line in file:

			lineSplit = line.split(",")


			fechaLinea = datetime.datetime.strptime(lineSplit[0], formato)

			fecha_datetime = parser.isoparse(lineSplit[0])

			#EXCEPTION 1
			if (fechaLinea >= fechaCorte) and pendant:
				pendant = False
				#print( f"REINICIO DEL SERVIDOR A LAS {lineSplit[0]}" )
				DRs_time_marker[DR] = fecha_datetime
				DRs_packet_counter[DR] = 0
				DRs_packet_counter_Rx[DR] = int(lineSplit[1])
			
			#EXCEPTION 2
			if int(lineSplit[1]) <= dataCache:
				#print( f"REINICIO DEL DISPOSITIVO A LAS {lineSplit[0]}" )
				DRs_time_marker[DR] = 0
				DRs_packet_counter[DR] = 0


			dataCache = int(lineSplit[1])

			

			if DRs_time_marker[DR] == 0:
				DRs_packet_counter_Rx[DR] = 1 #int(lineSplit[1])
				DRs_time_marker[DR] = fecha_datetime

			deltaTime = fecha_datetime - DRs_time_marker[DR]

			#print(DRs_packet_counter[DR])
			#print(DRs_packet_counter_Rx[DR])
			#print(line)

			if ( deltaTime >= datetime.timedelta(minutes = minutes) ) :
				#print("Window closed")
				DRs_packet_counter[DR] += 1

				Packets_sended = int(lineSplit[1]) - DRs_packet_counter_Rx[DR] + 1

				#print(Packets_sended)
				#print(DRs_packet_counter[DR])

				PDR = DRs_packet_counter[DR]/Packets_sended

				
				DRs_time_marker[DR] = fecha_datetime

				file_sep = open(folder + "/PDR_" + fileName,"a")

				file_sep.write(str(fecha_datetime) + "," + str(PDR) + "," + str(DRs_packet_counter[DR]) + "," + str(Packets_sended) + "\n")

				file_sep.close()

				DRs_packet_counter[DR] = 0
				DRs_packet_counter_Rx[DR] = int(lineSplit[1]) + 1

				#print("PDR: " + str(PDR))
			else:
				DRs_packet_counter[DR] = DRs_packet_counter[DR] + 1

		file.close()
	print("PDRs separated by frequency files generated . . .")

def PDRGeneratorWhitFQ2(target, devTargets, powerTargets, counterInterval):
	#minutes = timeInterval

	folder = "outputs/csv/" + target.replace(".data", "") + "/PDRsFq"
	if not os.path.exists(folder):
		os.makedirs(folder)
	DRs = []
	DRs_time_marker = {}
	DRs_packet_counter = {}
	DRs_packet_counter_Rx = {}
	DRs_overtime = {}



	directorio = "outputs/csv/" + target.replace(".data", "") + "/FQS"  # Cambia esto al directorio que quieras listar
	archivos = listar_archivos(directorio)

	for DR in range(0,12):
		DRs.append("DR" + str(DR))


	for fileName in archivos:
		file = open(folder + "/PDR_" + fileName ,"w")
		file.close()

	for DR in DRs:
		DRs_time_marker[DR] = 0
		DRs_packet_counter[DR] = 0
		DRs_packet_counter_Rx[DR] = 0
		DRs_overtime[DR] = False

	#Calculando..

	for fileName in archivos:

		file = open(directorio + "/" +fileName,"r")

		fqs, power, DR, dev = fileName.split("_")
		dev = dev.replace(".csv", "")

		i = 0

		for dev in devTargets:
			devTargets[i] = int(dev)
			i += 1




		i = 0

		for power in powerTargets:
			powerTargets[i] = int(power)
			i += 1

		if not(( DR in DRs ) and ( int(power) in powerTargets ) and ( int(dev) in devTargets ) ):
			file.close()
			print(fileName + " will not be analyzed . . . ")
			continue
		
		
		DRs_packet_counter[DR] = 0
		DRs_time_marker[DR] = 0
		
		formato = "%Y-%m-%d %H:%M:%S"
		fechaCorte_str = "2024-06-28 10:40:36"
		fechaCorte = datetime.datetime.strptime(fechaCorte_str, formato)
		pendant = True
		dataCache = 0

		for line in file:

			lineSplit = line.split(",")


			fechaLinea = datetime.datetime.strptime(lineSplit[0], formato)

			fecha_datetime = parser.isoparse(lineSplit[0])

			#EXCEPTION 1
			if (fechaLinea >= fechaCorte) and pendant:
				pendant = False
				#print( f"REINICIO DEL SERVIDOR A LAS {lineSplit[0]}" )
				DRs_time_marker[DR] = int(lineSplit[1])
				DRs_packet_counter[DR] = 0
				DRs_packet_counter_Rx[DR] = int(lineSplit[1])
			
			#EXCEPTION 2
			if int(lineSplit[1]) <= dataCache:
				#print( f"REINICIO DEL DISPOSITIVO A LAS {lineSplit[0]}" )
				DRs_time_marker[DR] = 0
				DRs_packet_counter[DR] = 0


			dataCache = int(lineSplit[1])

			

			if DRs_time_marker[DR] == 0:
				DRs_packet_counter_Rx[DR] = 1 #int(lineSplit[1])
				DRs_time_marker[DR] = 1

			deltaTime = int(lineSplit[1]) - DRs_time_marker[DR]

			#print(DRs_packet_counter[DR])
			#print(DRs_packet_counter_Rx[DR])
			#print(line)

			if ( deltaTime >= counterInterval ) :
				#print("Window closed")
				DRs_packet_counter[DR] += 1

				Packets_sended = int(lineSplit[1]) - DRs_packet_counter_Rx[DR] + 1

				#print(Packets_sended)
				#print(DRs_packet_counter[DR])

				PDR = DRs_packet_counter[DR]/Packets_sended

				
				DRs_time_marker[DR] = int(lineSplit[1])

				file_sep = open(folder + "/PDR_" + fileName,"a")

				file_sep.write(str(fecha_datetime) + "," + str(PDR) + "," + str(DRs_packet_counter[DR]) + "," + str(Packets_sended) + "\n")

				file_sep.close()

				DRs_packet_counter[DR] = 0
				DRs_packet_counter_Rx[DR] = int(lineSplit[1]) + 1

				#print("PDR: " + str(PDR))
			else:
				DRs_packet_counter[DR] = DRs_packet_counter[DR] + 1

		file.close()
	print("PDRs separated by frequency files generated . . .")




def PDRCalculatorApril(target, devTargets, powerTargets, timeInterval, frequencyTargets):

	excepctionDRs = ["DR6", "DR7", "DR8", "DR9", "DR10", "DR11"]
	frequencyTargetsCopy = []

	for frq in frequencyTargets:
		frequencyTargetsCopy.append(str(frq))
	
	minutes = timeInterval

	folder = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
	if not os.path.exists(folder):
		os.makedirs(folder)

	directorio = "outputs/csv/" + target.replace(".data", "") + "/PWS"
	archivos = listar_archivos(directorio)

	formato = "%Y-%m-%d %H:%M:%S"
	fechaCorte_str = "2024-06-28 10:40:36"
	fechaCorte = datetime.datetime.strptime(fechaCorte_str, formato)

	for fileName in archivos:

		resultados = []
		power, DR, dev = fileName.split("_")

		dev = dev.replace(".csv", "")

		if not ( ( int(power) in map(int,powerTargets) ) and ( int(dev) in map(int,devTargets) ) ):
			print(fileName + " will not be analyzed . . . ")
			continue

		archivo_entrada = directorio + "/" + fileName

		with open(archivo_entrada, 'r') as csvfile:
			lector_csv = csv.reader(csvfile)
			datos = list(lector_csv)

		registros = [ [datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1]),float(fila[2])]  for fila in datos]

		inicio = registros[0][0]
		index = 0
		offsetCalc = {}

		ventana = datetime.timedelta(minutes = timeInterval)

		corteEncontrado = False

		max_time = registros[-1][0]

		while inicio + ventana <= max_time:
			fin = inicio + ventana

			paquetes_en_ventana = {}

			while registros[index][0] < fin and index < len(registros) - 1:
				#print("enter")
				#print(registros[index][0])
				frq = registros[index][2]

				if not float(frq) in map(float,frequencyTargets) and not (DR in excepctionDRs):
					index += 1
					continue

				if registros[index + 1][2] in paquetes_en_ventana:
					freq = registros[index + 1][2]
					if registros[index + 1][1] <= paquetes_en_ventana[freq][-1][1]:
						index += 1
						break
				if not frq in paquetes_en_ventana:
					paquetes_en_ventana[frq] = []

				paquetes_en_ventana[frq].append( registros[index][:2] )

				index += 1

				if index >= len(registros):
					#print("??")
					break

				if registros[index][0] > fechaCorte and corteEncontrado == False:
					#print("??")
					corteEncontrado = True
					break

			#print(paquetes_en_ventana)
			#print()

			max_counter = {}
			init_counter = {}
			recibidos = []
			enviados = []
			offset = 0
			if paquetes_en_ventana:

				for frq, val in offsetCalc.items():
					if (frq in paquetes_en_ventana) and (frq in offsetCalc):
						offsetAdd = paquetes_en_ventana[frq][0][1] - offsetCalc[frq][1] - 1
						if offsetAdd > 0:
							offset += offsetAdd
							

				hora_inicio = None
				hora_fin = None

				for lista in paquetes_en_ventana.values():
					for reg in lista:
						hora = reg[0]
						if hora_inicio is None or hora < hora_inicio:
							hora_inicio = hora
						if hora_fin is None or hora > hora_fin:
							hora_fin = hora

				for frq, value in paquetes_en_ventana.items():
					max_counter[frq] = max( registro[1] for registro in value )
					init_counter[frq] = min( registro[1] for registro in value )
					recibidos.append( len( paquetes_en_ventana[frq] ) )
					enviados.append( max_counter[frq] - init_counter[frq] + 1 )

			else:
				hora_inicio = None
				hora_fin = None
				recibidos = 0
				max_counter = 0
				init_counter = 0
				enviados = 0

			if type(recibidos) == list:
				recibidosT = sum(recibidos)
			else:
				recibidosT = recibidos
			if type(recibidos) == list:
				enviadosT = sum(enviados) + offset
			else:
				enviadosT = enviados + offset 

			if type(enviadosT) == list and type(recibidosT) == list:
				pdr = recibidosT / enviadosT if len(enviados) > 0 else 0

			else:
				pdr = recibidosT / enviadosT if  enviadosT != 0 or recibidosT != 0 else 0

			resultados.append([hora_inicio, hora_fin, recibidosT, enviadosT, pdr])
			
			fin = registros[index][0]
				
			inicio = fin
			#offsetCalc = {}
			for freq, val in paquetes_en_ventana.items():
				offsetCalc[freq] = val[-1]

		#print(resultados)
		archivo_salida = folder + "/PDR_" + fileName
		
		with open(archivo_salida, 'w', newline='') as csvfile:
			escritor_csv = csv.writer(csvfile)
			
			for resultado in resultados:
				hora_inicio_str = resultado[0].strftime('%Y-%m-%d %H:%M:%S') if resultado[0] else ''
				hora_fin_str = resultado[1].strftime('%Y-%m-%d %H:%M:%S') if resultado[1] else ''
				if hora_inicio != '':
					escritor_csv.writerow([hora_inicio_str, hora_fin_str, resultado[2], resultado[3], resultado[4]])

def PDRCalculatorAprilFq(target, devTargets, powerTargets, timeInterval):

	excepctionDRs = ["DR6", "DR7", "DR8", "DR9", "DR10", "DR11"]

	minutes = timeInterval

	folder = "outputs/csv/" + target.replace(".data", "") + "/PDRsFq"
	if not os.path.exists(folder):
		os.makedirs(folder)

	directorio = "outputs/csv/" + target.replace(".data", "") + "/FQS"
	archivos = listar_archivos(directorio)

	formato = "%Y-%m-%d %H:%M:%S"
	fechaCorte_str = "2024-06-28 10:40:36"
	fechaCorte = datetime.datetime.strptime(fechaCorte_str, formato)

	for fileName in archivos:

		resultados = []
		frq, power, DR, dev = fileName.split("_")

		dev = dev.replace(".csv", "")

		if not ( ( int(power) in map(int,powerTargets) ) and ( int(dev) in map(int,devTargets) ) ):
			print(fileName + " will not be analyzed . . . ")
			continue

		archivo_entrada = directorio + "/" + fileName

		with open(archivo_entrada, 'r') as csvfile:
			lector_csv = csv.reader(csvfile)
			datos = list(lector_csv)

		registros = [ [datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1]),float(fila[2])]  for fila in datos]

		inicio = registros[0][0]
		index = 0

		ventana = datetime.timedelta(minutes = timeInterval)

		corteEncontrado = False

		max_time = registros[-1][0]
		offset = 0
		while inicio + ventana <= max_time:
			fin = inicio + ventana

			paquetes_en_ventana = []

			while registros[index][0] < fin:

				
				paquetes_en_ventana.append( registros[index][:2] )

				if registros[index + 1][1] <= paquetes_en_ventana[-1][1]:
					index += 1
					break

				index += 1

				if index >= len(registros):
					#print("??")
					break

				if registros[index][0] > fechaCorte and corteEncontrado == False:
					#print("??")
					corteEncontrado = True
					break

			#print(paquetes_en_ventana)
			#print()


			if paquetes_en_ventana:
		

				hora_inicio = None
				hora_fin = None

				
				for reg in paquetes_en_ventana:
					hora = reg[0]
					if hora_inicio is None or hora < hora_inicio:
						hora_inicio = hora
					if hora_fin is None or hora > hora_fin:
						hora_fin = hora

				max_counter = max( registro[1] for registro in paquetes_en_ventana )
				init_counter = min( registro[1] for registro in paquetes_en_ventana )
				recibidos = len( paquetes_en_ventana ) 
				enviados = max_counter - init_counter + 1 + offset

			else:
				hora_inicio = None
				hora_fin = None
				recibidos = 0
				max_counter = 0
				init_counter = 0
				enviados = 0

			
			pdr = recibidos / enviados if enviados != 0 else 0


			resultados.append([hora_inicio, hora_fin, recibidos, enviados, pdr])
			
			fin = registros[index][0]
				
			inicio = fin
			
			offset = registros[index][1] - paquetes_en_ventana[-1][1] - 1
			if offset < 0:
				offset = 0
		#print(resultados)
		archivo_salida = folder + "/PDR_" + fileName
		
		with open(archivo_salida, 'w', newline='') as csvfile:
			escritor_csv = csv.writer(csvfile)
			
			for resultado in resultados:
				hora_inicio_str = resultado[0].strftime('%Y-%m-%d %H:%M:%S') if resultado[0] else ''
				hora_fin_str = resultado[1].strftime('%Y-%m-%d %H:%M:%S') if resultado[1] else ''
				if hora_inicio != '':
					escritor_csv.writerow([hora_inicio_str, hora_fin_str, resultado[2], resultado[3], resultado[4]])
















def PDRCalculatorJulyLoRaFQ(archivo_entrada, archivo_salida, ventana):
    # Leer el archivo de entrada
    with open(archivo_entrada, 'r') as csvfile:
        lector_csv = csv.reader(csvfile)
        datos = list(lector_csv)
    
    # Extraer los contadores (segunda columna) y las horas (primera columna)
    registros = [(datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])) for fila in datos]
    
    #for registro in registros:
    #	print(registro[1])
    # Inicializar la lista para almacenar los resultados
    resultados = []
    
    # Calcular el PDR para cada ventana
    max_contador = max(registro[1] for registro in registros)
    inicio = 1
    index = 0
    offset = 0

    while inicio <= max_contador:
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
        
        enviados = max_counter - init_counter + 1 + offset


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
            hora_inicio_str = resultado[0].strftime('%Y-%m-%d %H:%M:%S') if resultado[0] else ''
            hora_fin_str = resultado[1].strftime('%Y-%m-%d %H:%M:%S') if resultado[1] else ''
            if hora_inicio != '':
            	escritor_csv.writerow([hora_inicio_str, hora_fin_str, resultado[2], resultado[3], resultado[4]])


def isLowerEqualThanValues(val, dict_):

	for key, value in dict_.items():
		if val < value[0][1]:
			return True
	return False

def PDRCalculatorJulyLoRa(archivo_entrada, archivo_salida, ventana):
	# Leer el archivo de entrada
	with open(archivo_entrada, 'r') as csvfile:
	    lector_csv = csv.reader(csvfile)
	    datos = list(lector_csv)

	# Extraer los contadores (segunda columna) y las horas (primera columna)
	registros = [ [datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1]),float(fila[2])]  for fila in datos]

	resultados = []

	# Calcular el PDR para cada ventana
	max_contador = max(registro[1] for registro in registros)
	inicio = 1
	index = 0
	offsetCalc = {}
	while inicio + ventana - 1 <= max_contador - 1:
		fin = inicio + ventana - 1
	    #paquetes_en_ventana = [registro for registro in registros if inicio <= registro[1] <= fin]
	    
		paquetes_en_ventana = {}

	    #lim = index + ventana - 1
	    
		while registros[index][1] < fin:
			frq = registros[index][2]
			if registros[index + 1][2] in paquetes_en_ventana:
				freq = registros[index + 1][2]
				if registros[index + 1][1] <= paquetes_en_ventana[freq][-1][1]:
					index += 1
					break
			if not frq in paquetes_en_ventana:
				paquetes_en_ventana[frq] = []

			paquetes_en_ventana[frq].append( registros[index][:2] )

			index += 1

			if index >= len(registros):
				break

	   	

		max_counter = {}
		init_counter = {}
		recibidos = []
		enviados = []
		offset = 0
		if paquetes_en_ventana:

			for frq, val in offsetCalc.items():
				if (frq in paquetes_en_ventana) and (frq in offsetCalc):
					offsetAdd = paquetes_en_ventana[freq][0][1] - offsetCalc[frq][1] - 1
					if offsetAdd > 0:
						offset += offsetAdd

			hora_inicio = None
			hora_fin = None
			for lista in paquetes_en_ventana.values():
			    for reg in lista:
			        hora = reg[0]
			        if hora_inicio is None or hora < hora_inicio:
			            hora_inicio = hora
			        if hora_fin is None or hora > hora_fin:
			            hora_fin = hora
			for frq, value in paquetes_en_ventana.items():
				max_counter[frq] = max( registro[1] for registro in value )
				init_counter[frq] = min( registro[1] for registro in value )
				recibidos.append( len( paquetes_en_ventana[frq] ) )
				enviados.append( max_counter[frq] - init_counter[frq] + 1 )



	        
		else:
		    hora_inicio = None
		    hora_fin = None
		    recibidos = 0
		    max_counter = 0
		    init_counter = 0
		    enviados = 0
		if type(recibidos) == list:
			recibidosT = sum(recibidos)
		else:
			recibidosT = recibidos
		if type(recibidos) == list:
			enviadosT = sum(enviados) + offset
		else:
			enviadosT = enviados + offset 

		if type(enviadosT) == list and type(recibidosT) == list:
			pdr = recibidosT / enviadosT if len(enviados) > 0 else 0

		else:
			pdr = recibidosT / enviadosT if  enviadosT != 0 or recibidosT != 0 else 0

		resultados.append([hora_inicio, hora_fin, recibidosT, enviadosT, pdr])
	    
	    # Actualizar el inicio para la siguiente ventana

		
		fin = registros[index][1]

			
		inicio = fin + 1
		offsetCalc = {}
		for freq, val in paquetes_en_ventana.items():
			offsetCalc[freq] = val[-1]

	# Guardar los resultados en el archivo de salida
	with open(archivo_salida, 'w', newline='') as csvfile:
	    escritor_csv = csv.writer(csvfile)
	    #escritor_csv.writerow(['Hora Inicio', 'Hora Fin', 'Recibidos', 'Enviados', 'PDR'])
	    for resultado in resultados:
	        hora_inicio_str = resultado[0].strftime('%Y-%m-%d %H:%M:%S') if resultado[0] else ''
	        hora_fin_str = resultado[1].strftime('%Y-%m-%d %H:%M:%S') if resultado[1] else ''
	        if hora_inicio != '':
	        	escritor_csv.writerow([hora_inicio_str, hora_fin_str, resultado[2], resultado[3], resultado[4]])

TIEMPO_DUPLICADOS_def = datetime.timedelta(seconds=500)  # 8 minutos y 20 segundos
TIEMPO_CONTADORES_def = datetime.timedelta(seconds=1901)  # 31 minutos y 40 segundos

TIEMPO_DUPLICADOS_dev2 = datetime.timedelta(seconds=540)
TIEMPO_CONTADORES_dev2 = datetime.timedelta(seconds=1981)

def comparar_distancia(fecha1, fecha2, distancia_objetivo_int, rango_error=2):

    # Asegurarse de que distancia_objetivo_int es un número, no un timedelta
    if isinstance(distancia_objetivo_int, datetime.timedelta):
        distancia_objetivo_int = distancia_objetivo_int.total_seconds()
        
    # Convertir distancia_objetivo_int a timedelta
    distancia_objetivo = datetime.timedelta(seconds=distancia_objetivo_int)

    # Calcular la diferencia en segundos entre las dos fechas
    diferencia = abs((fecha2 - fecha1).total_seconds())
    
    # Definir el rango permitido
    rango_minimo = distancia_objetivo.total_seconds() - rango_error
    rango_maximo = distancia_objetivo.total_seconds() + rango_error
    
    # Verificar si la diferencia está dentro del rango permitido
    return rango_minimo <= diferencia <= rango_maximo

def forwarwadFixer(rowPast, rowFuture, dev, p):

	if dev == 2:
		#print("2")
		TIEMPO_DUPLICADOS = TIEMPO_DUPLICADOS_dev2
		TIEMPO_CONTADORES = TIEMPO_CONTADORES_dev2
	else:
		TIEMPO_DUPLICADOS = TIEMPO_DUPLICADOS_def
		TIEMPO_CONTADORES = TIEMPO_CONTADORES_def

	fecha1 = {"order":rowPast[-1],"dt":rowPast[0]}
	fecha2 = {"dt":rowFuture[0]}

	if fecha1["order"] == 0:
		
		#primer duplicado, es decir, partimos sumando 8 min
		nd = 1
		nc = 0
		while not (comparar_distancia(fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, fecha2["dt"], 0, 30)) and not (fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES > fecha2["dt"]):
			if nd == nc:
				nd += 1
			else:
				nc += 1
		DifferencePD = fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES - fecha2["dt"]

		if nd == nc:
			#fecha2["order"] = 0
			rowFuture.append(0)
		else:
			#fecha2["order"] = 1
			rowFuture.append(1)

	if fecha1["order"] == 1:
		
		#ahora con anterior en segundo duplicado, es decir, partimos sumando 31 min
		nd = 0
		nc = 1
		while not (comparar_distancia(fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, fecha2["dt"], 0, 30)) and not (fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES > fecha2["dt"]):
			if nd == nc:
				nc += 1
			else:
				nd += 1
		DifferenceSD = fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES - fecha2["dt"]

		if nd == nc:
			rowFuture.append(1)
			#fecha2["order"] = 1
		else:
			rowFuture.append(0)
			#fecha2["order"] = 0
		if (not (comparar_distancia(fecha1["dt"] + nd*TIEMPO_DUPLICADOS + nc*TIEMPO_CONTADORES, fecha2["dt"], 0, 30))) and p :
			print("WARNING: interpolation has a deviation higher than 30 seconds" )
			print(fecha1)
			print(fecha2)

def backwardFixer(rowPast,rowFuture, dev, p):

	if dev == 2:
		TIEMPO_DUPLICADOS = TIEMPO_DUPLICADOS_dev2
		TIEMPO_CONTADORES = TIEMPO_CONTADORES_dev2
	else:
		TIEMPO_DUPLICADOS = TIEMPO_DUPLICADOS_def
		TIEMPO_CONTADORES = TIEMPO_CONTADORES_def

	fecha2 = {"dt":rowFuture[0],"order":rowFuture[-1]}
	fecha1 = {"dt":rowPast[0]}
	if fecha2["order"] == 1:
		#primer duplicado, es decir, partimos sumando 31 min
		nd = 1
		nc = 0
		while not (comparar_distancia(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, fecha1["dt"], 0, 30)) and not(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES < fecha1["dt"]):
			
			if nd == nc:
				nd += 1
			else:
				nc += 1
		

		if nd == nc:
			rowPast.append(1)
			#fecha1["order"] = 1
		else:
			rowPast.append(0)
			#fecha1["order"] = 0
	if fecha2["order"] == 0:
		#ahora con anterior en segundo duplicado, es decir, partimos sumando 8 min
		nd = 0
		nc = 1
		while (not comparar_distancia(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, fecha1["dt"], 0, 30)) and not(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES < fecha1["dt"]):
			#print(comparar_distancia(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, fecha1["dt"], 0, 30))
			if nd == nc:
				nc += 1
			else:
				nd += 1
		

		if nd == nc:
			rowPast.append(0)
			#fecha1["order"] = 0
		else:
			rowPast.append(1)
			#fecha1["order"] = 1


		if (not comparar_distancia(fecha2["dt"] - nd*TIEMPO_DUPLICADOS - nc*TIEMPO_CONTADORES, fecha1["dt"], 0, 30)) and p:
			print("WARNING: interpolation has a deviation higher than 30 seconds" )
			print(fecha1)
			print(fecha2)

def fixCounter( row ):
	#print(row[1])
	if len(row) < 3:
		print("CRITICAL ERROR, ROW WITHOUT POSITION ID")
	elif row[-1] == 0:
		row[1] = row[1]*2 - 1
	elif row[-1] == 1:
		row[1] = row[1]*2
	#print(row[1])
	#print()

def fixerLRFHSS(registers, dev, inputFile, p=True):

	i = 0
	while i < len(registers) - 1:
		if registers[i][1] > registers[i + 1][1]:
			registros = registers[:i + 1]
			registros_left = registers[i + 1:]
			break
		i += 1
	if not(i < len(registers) - 1):
		registros = registers
		registros_left = []

	#primer paso es encontrar dos contadores juntos
	find = False

	referencePosition = 0

	while ( not find ) and ( referencePosition < len(registros) - 1 ) :
		if registros[referencePosition][1] == registros[referencePosition + 1][1]:

			registros[referencePosition].append(0)
			registros[referencePosition + 1].append(1)

			fixCounter(registros[referencePosition])
			fixCounter(registros[referencePosition + 1])
			'''
			print(referencePosition)
			print(registros[referencePosition])
			print(registros[referencePosition + 1])
			'''
			find = True
		else:
			referencePosition += 1

	if find:
		#print(f"Starting fixing counters on file {inputFile}")
		i = referencePosition - 1
		while i >= 0:
			#print("backwardFixer")
			backwardFixer(registros[i],registros[i + 1], dev, p)
			fixCounter(registros[i])
			i -= 1
		#print("all past register fixed")

		i = referencePosition + 2
		while i < len(registros):
			#print("forwarwadFixer")
			forwarwadFixer(registros[i - 1],registros[i], dev, p)
			fixCounter(registros[i])
			i+=1
		#print("all future registers fixed")


	else:
		print(colored(f"ERROR ON FILE {inputFile}, BEETWEN {registros[0][0]} TO {registros[-1][0]}, EQUIVALENT TO {len(registros)} LINES NONE DUPLICATED EXIST, CANNOT INFER REAL COUNTERS IN A DETERMINISTIC WAY",'red'))
		referencePosition = 0
		registros[referencePosition].append(0)
		fixCounter(registros[referencePosition])
		i = referencePosition + 1
		while i < len(registros):
			forwarwadFixer(registros[i - 1],registros[i], dev, p)
			fixCounter(registros[i])
			i+=1
	resultado = []
	resultado = resultado + registros
	#Reparamos el resto de manera recursiva
	if len(registros_left) > 0:
		resultado = resultado + fixerLRFHSS(registros_left,dev, inputFile)

	return resultado

def PDRCalculatorJulyLRFHSS(inputFile, outputFile, window):
	
	
	with open(inputFile, 'r') as csvfile:
	        lector_csv = csv.reader(csvfile)
	        datos = list(lector_csv)

	registros = [[datetime.datetime.strptime(fila[0], '%Y-%m-%d %H:%M:%S'), int(fila[1])] for fila in datos]


	dev = int(inputFile.split("_")[-1].replace(".csv",""))

	registros = fixerLRFHSS(registros, dev, inputFile)

	ventana = window
	# Inicializar la lista para almacenar los resultados
	resultados = []

	# Calcular el PDR para cada ventana
	max_contador = max(registro[1] for registro in registros)
	inicio = 1
	index = 0
	offset = 0
	while inicio <= max_contador:
		fin = inicio + ventana - 1
		#paquetes_en_ventana = [registro for registro in registros if inicio <= registro[1] <= fin]

		paquetes_en_ventana = []

		lim = registros[index][1] + ventana - 1

		while registros[index][1] <= lim and index < len(registros) - 1:
			paquetes_en_ventana.append(registros[index])
			index += 1

			if registros[index][1] <= registros[index-1][1]:
				break


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


		enviados = max_counter - init_counter + 1  + offset
		pdr = recibidos / enviados if enviados > 0 else 0

		resultados.append([hora_inicio, hora_fin, recibidos, enviados, pdr])

		# Actualizar el inicio para la siguiente ventana
		inicio = fin + 1

		#inicio = registros[index][1]

		if index < len(registros) - 2:
			offset = registros[index + 1][1] - registros[index][1] - 1
			if offset < 0:
				offset = registros[index + 1][1] - 1  

	# Guardar los resultados en el archivo de salida
	with open(outputFile, 'w', newline='') as csvfile:
	    escritor_csv = csv.writer(csvfile)
	    #escritor_csv.writerow(['Hora Inicio', 'Hora Fin', 'Recibidos', 'Enviados', 'PDR'])
	    for resultado in resultados:
	        hora_inicio_str = resultado[0].strftime('%Y-%m-%d %H:%M:%S') if resultado[0] else ''
	        hora_fin_str = resultado[1].strftime('%Y-%m-%d %H:%M:%S') if resultado[1] else ''
	        if hora_fin_str != '':
	        	escritor_csv.writerow([hora_inicio_str, hora_fin_str, resultado[2], resultado[3], resultado[4]])





def calculatePDRJulyFrq(target, window):
	folder = "outputs/csv/" + target.replace(".data", "") + "/PDRsFRQ"
	if not os.path.exists(folder):
	        os.makedirs(folder)
		
	files = listar_archivos("outputs/csv/" + target.replace(".data", "") + "/FRQ")

	for nameFile in files:

		nameFileSplit = nameFile.split("_")
		frq = nameFileSplit[0]
		Len = nameFileSplit[1]
		BWsOrSF = nameFileSplit[2]
		power = nameFileSplit[3]
		CR = nameFileSplit[4].replace("-","/")
		modulation = nameFileSplit[5]
		dev = nameFileSplit[6].replace(".csv","")

		fileToRead = "outputs/csv/" + target.replace(".data", "") + "/FRQ/" + nameFile
		fileToSave = "outputs/csv/" + target.replace(".data", "") + "/PDRsFRQ/PDR_" + nameFile
		if modulation == "LR-FHSS":
			PDRCalculatorJulyLRFHSS(fileToRead, fileToSave, window)
		elif modulation == "LoRa":
			PDRCalculatorJulyLoRaFQ(fileToRead, fileToSave, window)
		else:
			print(colored(f"MODULATION NOT RECOGNIZED: {modulation} ON FILE {nameFile}", 'yellow'))



	print("PDR on each frequency calculated  . . .")	
       
def calculatePDRJuly(target, window):
	folder = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
	if not os.path.exists(folder):
	        os.makedirs(folder)
		
	files = listar_archivos("outputs/csv/" + target.replace(".data", "") + "/LEN")

	for nameFile in files:

		nameFileSplit = nameFile.split("_")
		Len = nameFileSplit[0]
		BWsOrSF = nameFileSplit[1]
		power = nameFileSplit[2]
		CR = nameFileSplit[3].replace("-","/")
		modulation = nameFileSplit[4]
		dev = nameFileSplit[5].replace(".csv","")

		fileToRead = "outputs/csv/" + target.replace(".data", "") + "/LEN/" + nameFile
		fileToSave = "outputs/csv/" + target.replace(".data", "") + "/PDRs/PDR_" + nameFile
		if modulation == "LR-FHSS":
			PDRCalculatorJulyLRFHSS(fileToRead, fileToSave, window)
		elif modulation == "LoRa":
			PDRCalculatorJulyLoRa(fileToRead, fileToSave, int(window/4))
		else:
			print(f"MODULATION NOT RECOGNIZED: {modulation} ON FILE {nameFile}")



	print("PDR calculated  . . .")	