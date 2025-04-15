import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from dateutil import parser
import datetime

import re





def listar_archivos(directorio):
    # Obtener todos los elementos en el directorio
    elementos = os.listdir(directorio)
    
    # Filtrar para obtener solo los archivos
    archivos = [f for f in elementos if os.path.isfile(os.path.join(directorio, f))]
    
    return archivos






def boxWhiskerPDRGraphs(target, devTargets, powerTargets, DRs, labels):
	dataSets = {}
	for DR in DRs:
		dataSets[DR] = list()



	directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"  # Cambia esto al directorio que quieras listar
	archivos = listar_archivos(directorio)

	folder = "outputs/figs/" + target.replace(".data", "")
	if not os.path.exists(folder):
	        os.makedirs(folder)

	for powerTarget in powerTargets:
		if not os.path.exists(folder + "/" + str(powerTarget)):
			os.makedirs(folder + "/" + str(powerTarget))
		if not os.path.exists(folder + "/" + str(powerTarget) + "/PDRLine"):
			os.makedirs(folder + "/" + str(powerTarget) + "/PDRLine")
		if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker"):
			os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker")
		if not os.path.exists(folder + "/" + str(powerTarget) + "/heatMap"):
			os.makedirs(folder + "/" + str(powerTarget) + "/heatMap")





	for powerTarget in powerTargets:

		fig, axs = plt.subplots(2, 2, figsize=(12, 8))

		for devTarget in devTargets:

			dataSets = {}
			for DR in DRs:
				dataSets[DR] = list()

			for DR in DRs:
				try:
					file = open(directorio + "/PDR_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv","r")

					for line in file:
						lineSplit = line.split(",")
						dataSets[DR].append(float(lineSplit[1]))

					file.close()
				except:
					print(f"There isn't enough data for the PDR on {labels[devTarget]} on data rate {DR} whit transmission power {powerTarget}")

			# Encuentra el tamaño del array más largo
			max_length = max(len(array) for array in dataSets.values())

			# Rellena de ceros los arrays más cortos
			for key in dataSets:
				while len(dataSets[key]) < max_length:
					dataSets[key].append(0)

			df = pd.DataFrame(dataSets)

			# Crear el gráfico de diagramas de caja y bigotes
			plt.figure(figsize=(10, 6))

			sns.boxplot(data=df)

			# Añadir títulos y etiquetas
			plt.title(f'Packet Delivery Ratio on {labels[devTarget]}')
			plt.xlabel('DR')
			plt.ylabel('PDR')

			plt.ylim(0, 1.1)

			# Guardar el gráfico como una imagen
			plt.savefig( folder + "/" + str(powerTarget) + "/BoxWhisker/" + str(labels[devTarget]) + "_" + str(powerTarget) + "dBm_boxWhiskerPDR.png")
			plt.close()

			if devTarget == 1:
				ax = axs[0, 0]
			elif devTarget == 2:
				ax = axs[0,1]
			elif devTarget == 3:
				ax = axs[1,0]
			elif devTarget == 4:
				ax = axs[1,1]
			else:
				print("DEVICE NOT EXPECTED")

			sns.boxplot(data=df, ax=ax)
			ax.set_title(labels[devTarget])

			plt.close()
			


			plt.figure(figsize=(10, 6))

			# Crear el gráfico de líneas superpuestas
			for column in df.columns:
			    sns.lineplot(data=df[column], label=column)

			# Añadir títulos y etiquetas
			plt.title(f'Packet Delivery Ratio in {labels[devTarget]} on transmission power ' + str(powerTarget))
			plt.xlabel('number of measurement')
			plt.ylabel('PDR')
			plt.ylim(0, 1.1)
			# Añadir leyenda
			plt.legend()

			# Guardar el gráfico como una imagen
			plt.savefig(folder + "/" + str(powerTarget) + "/PDRLine/" + str(devTarget) + "LinePDR_PWR.png")
			plt.close()


			plt.figure(figsize=(10, 6))

			# Transponer el DataFrame para intercambiar los ejes
			df_transpuesta = df.T

			# Crear el mapa de calor con seaborn
			sns.heatmap(data=df_transpuesta, cmap="YlGnBu")

			# Añadir títulos
			plt.title(f"heatmap of PDR on {labels[devTarget]} on transmission power {powerTarget} dBm")


			# Mostrar el mapa de calor
			plt.savefig(folder + "/" + str(powerTarget) + "/heatMap/" + str(devTarget) + "PDRHeatMap_PWR.png")
			plt.close()

			#print("Box whisker figures for the device " + str(devTarget) + " whit transmission power " + str(powerTarget) + " created.")
			print(f"Box whisker figures for the device {devTarget} whit transmission power {powerTarget} created.")
		fig.tight_layout()

		# Guardar la figura como una imagen
		fig.savefig(folder + "/" + str(powerTarget) + "/BoxWhisker/PDRMatrix_PWR.png")
	print("Box whisker graphs done . . .")

def groupedBoxWhiskerPDRGraphs(target, devTargets, powerTargets, DRs, labels, dimx, dimy):
    directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker"):
            os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker")

  
    for powerTarget in powerTargets:
        data = []
        for devTarget in devTargets:
            dataSets = {DR: [] for DR in DRs}

            for DR in DRs:
                try:
                    file = open(directorio + "/PDR_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r")
                    for line in file:
                        lineSplit = line.split(",")
                        dataSets[DR].append(float(lineSplit[1]))
                    file.close()
                except:
                    print(f"There isn't enough data for the device {devTarget} on {DR} with transmission power {powerTarget}")

            for DR, values in dataSets.items():
                for value in values:
                    data.append({"Device": labels[devTarget], "DR": DR, "PDR": value})

        df = pd.DataFrame(data)

        sorted_DRs = sorted(DRs, key=custom_sort_key)

        df['DR'] = pd.Categorical(df['DR'], categories=sorted_DRs, ordered=True)

        #plt.figure(figsize=(20, 8))
        plt.figure(figsize=(dimx, dimy))
        sns.boxplot(x='DR', y='PDR', hue='Device', data=df, width=0.5)

        # Añadir títulos y etiquetas
        plt.title(f'Packet Delivery Ratio on transmission power {powerTarget} dBm')
        plt.xlabel('DR')
        plt.ylabel('PDR')
        plt.ylim(0, 1.1)
        # Añadir leyenda
        plt.legend(title='location')

        # Guardar el gráfico como una imagen
        plt.savefig(folder + "/" + str(powerTarget) + "/BoxWhisker/" + str(powerTarget) + "dBm_groupedBoxWhiskerPDR.png")
        plt.close()

        print(f"Grouped box whisker graph for transmission power {powerTarget}.")
    print("Grouped box whisker graphs done . . .")

def groupedBoxDevicesWhiskerPDRGraphs(target, devTargets, powerTargets, DRs, labels, order_dict, dimx, dimy):
    directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker"):
            os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker")

    for powerTarget in powerTargets:
        data = []
        for DR in DRs:
            dataSets = {devTarget: [] for devTarget in devTargets}

            for devTarget in devTargets:
                try:
                    file = open(directorio + "/PDR_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r")
                    for line in file:
                        lineSplit = line.split(",")
                        dataSets[devTarget].append(float(lineSplit[1]))
                    file.close()
                except:
                    print(f"There isn't enough data for the device {devTarget} on {DR} with transmission power {powerTarget}")

            for devTarget, values in dataSets.items():
                for value in values:
                    data.append({"Device": labels[devTarget], "DR": DR, "PDR": value})

        df = pd.DataFrame(data)

        sorted_labels = sorted(labels.values(), key=lambda x: order_dict[list(labels.keys())[list(labels.values()).index(x)]])

        # Ordenar dispositivos en el eje x
        df['Device'] = pd.Categorical(df['Device'], categories=sorted_labels, ordered=True)

        plt.figure(figsize=(dimx, dimy))
        sns.boxplot(x="Device", y='PDR', hue='DR', data=df) # No se necesita 'hue_order' aquí

        # Añadir títulos y etiquetas
        #plt.title(f'Packet Delivery Ratio on transmission power {powerTarget} dBm')
        plt.xlabel('Device')
        plt.ylabel('PDR')
        plt.ylim(0, 1.1)
        # Añadir leyenda
        plt.legend(title='DR', bbox_to_anchor=(1, 1), loc='upper left')

        # Guardar el gráfico como una imagen
        plt.savefig(folder + "/" + str(powerTarget) + "/BoxWhisker/" + str(powerTarget) + "dBm_groupedDeviceBoxWhiskerPDR.png")
        plt.close()

        print(f"Grouped box whisker graph for transmission power {powerTarget}.")
    print("Grouped box whisker graphs done . . .")

def RSSILineGraphBetweenDRs(target, devTargets, powerTargets, DRs, labels, timeGraphInterval, dimx, dimy):
    dataSets = {1: [], 2: [], 3: [], 4: []}
    timeSets = {1: [], 2: [], 3: [], 4: []}

    directorio = "outputs/csv/" + target.replace(".data", "") + "/PWS"  # Cambia esto al directorio que quieras listar
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/RSSIBetweenDRs"):
            os.makedirs(folder + "/" + str(powerTarget) + "/RSSIBetweenDRs")

    for powerTarget in powerTargets:
        minData = 10000000
        maxData = -10000000
        for devTarget in devTargets:
            for DR in DRs:
                try:
                    with open(directorio + "/" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r") as file:
                        for line in file:
                            lineSplit = line.split(",")
                            rssi_value = float(lineSplit[3])
                            if rssi_value > maxData:
                                maxData = rssi_value
                            if rssi_value < minData:
                                minData = rssi_value
                except:
                    continue

        for devTarget in devTargets:
            dataSets = {}
            timeSets = {}
            for DR in DRs:
                try:
                    with open(directorio + "/" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r") as file:
                        for line in file:
                            lineSplit = line.split(",")
                            dataSets.setdefault(DR, []).append(float(lineSplit[3]))
                            timeSets.setdefault(DR, []).append(lineSplit[0])
                except:
                    print(f"Error en el directorio: {directorio}/{powerTarget}_{DR}_{devTarget}.csv")
                    continue

            timeDic = {key: [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in timeSets[key]] for key in timeSets}

            min_time = min(min(timeDic[times]) for times in timeDic)
            max_time = max(max(timeDic[times]) for times in timeDic)

            time_range = [min_time + datetime.timedelta(seconds=x) for x in range(int((max_time - min_time).total_seconds()) + 1)]
            time_range_numbers = mdates.date2num(time_range)

            plt.figure(figsize=(dimx, dimy))

            for key in timeSets:
                plt.plot(timeDic[key], dataSets[key], 'o', label=key)

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))

            plt.xlabel('Time')
            plt.ylabel('RSSI dBm')
            #plt.title(f'RSSI vs Time on {labels[devTarget]} and power {powerTarget} dBm')
            plt.legend()
            plt.grid(True)
            plt.ylim(minData * 1.1, maxData * 0.9)
            #plt.ylim(-140, -110)


            plt.xticks(rotation=60, ha='right')
            plt.tight_layout()

            plt.savefig(folder + "/" + str(powerTarget) + "/RSSIBetweenDRs/RSSIBetweenDR_" + str(labels[int(devTarget)]) + "_" + str(powerTarget) + "dBm.png")
            plt.clf()
            plt.close()

            print(f"RSSI figures for the device {devTarget} with transmission power {powerTarget} created.")

    print("Graphs RSSI between DRs done . . . ")

def RSSILineGraphBetweenDevices(target, devTargets, powerTargets, DRs, labels, timeGraphInterval, dimx, dimy):
    dataSets = {1:[] , 2:[] , 3:[] , 4:[] }
    timeSets = {1:[] , 2:[] , 3:[] , 4:[] }

    directorio = "outputs/csv/" + target.replace(".data", "") + "/PWS"  # Cambia esto al directorio que quieras listar
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/RSSIBetweenDevices"):
            os.makedirs(folder + "/" + str(powerTarget) + "/RSSIBetweenDevices")

    for powerTarget in powerTargets:
        minData = 10000000
        maxData = -10000000
        for DR in DRs:
            for devTarget in devTargets:
                try:
                    file_path = directorio + "/" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                    with open(file_path, "r") as file:
                        for line in file:
                            lineSplit = line.split(",")
                            rssi_value = float(lineSplit[3])
                            if rssi_value > maxData:
                                maxData = rssi_value
                            if rssi_value < minData:
                                minData = rssi_value
                except:
                    continue

        for DR in DRs:
            dataSets = {}
            timeSets = {}

            for devTarget in devTargets:
                try:
                    file_path = directorio + "/" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                    with open(file_path, "r") as file:
                        for line in file:
                            lineSplit = line.split(",")

                            dataSets.setdefault(devTarget, [])
                            dataSets[devTarget].append(float(lineSplit[3]))

                            timeSets.setdefault(devTarget, [])
                            timeSets[devTarget].append(lineSplit[0])
                except:
                    print(f"Error en el directorio: {file_path}")
                    continue

            timeDic = {}
            for key in timeSets:
                timeDic[key] = [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in timeSets[key]]

            min_vector = [min(timeDic[times]) for times in timeDic]
            max_vector = [max(timeDic[times]) for times in timeDic]

            min_time = min(min_vector)
            max_time = max(max_vector)

            time_range = [min_time + datetime.timedelta(seconds=x) for x in range(int((max_time - min_time).total_seconds()) + 1)]

            timeNumbersDics = {key: [mdates.date2num(time) for time in timeDic[key]] for key in timeSets}
            time_range_numbers = mdates.date2num(time_range)

            plt.figure(figsize=(dimx, dimy))

            for key in timeSets:
                plt.plot(timeDic[key], dataSets[key], 'o', label=labels[key])

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))

            plt.xlabel('Time')
            plt.ylabel('RSSI dBm')
            #plt.title(f'RSSI vs Time on data rate {DR} and power {powerTarget}')
            plt.legend()
            plt.grid(True)
            plt.ylim(minData * 1.1, maxData * 0.9)

            # Rotar las etiquetas del eje x para que se vean mejor
            plt.xticks(rotation=60, ha='right')

            # Ajustar el diseño para evitar que las etiquetas se corten
            plt.tight_layout()

            # Guardar el gráfico como una imagen
            plt.savefig(folder + "/" + str(powerTarget) + "/RSSIBetweenDevices/" + "RSSIBetweenDevices_" + str(DR) + "_" + str(powerTarget) + "dBm.png")
            plt.clf()
            plt.close()

            print(f"RSSI figures for the data rate {DR} with transmission power {powerTarget} created.")

    print("Graphs RSSI between devices done . . . ")

def SNRLineGraphBetweenDevices(target, devTargets, powerTargets, DRs, labels, timeGraphInterval, dimx, dimy):
    dataSets = {1:[] , 2:[] , 3:[] , 4:[] }
    timeSets = {1:[] , 2:[] , 3:[] , 4:[] }

    excepctionDRs = ["DR8", "DR9", "DR10", "DR11"]
    directorio = "outputs/csv/" + target.replace(".data", "") + "/PWS"  # Cambia esto al directorio que quieras listar
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/SNRBetweenDevices"):
            os.makedirs(folder + "/" + str(powerTarget) + "/SNRBetweenDevices")

    for powerTarget in powerTargets:
        minData = 10000000
        maxData = -10000000
        for DR in DRs:
            for devTarget in devTargets:
                try:
                    file_path = directorio + "/" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                    with open(file_path, "r") as file:
                        for line in file:
                            lineSplit = line.split(",")
                            snr_value = float(lineSplit[5])
                            if snr_value > maxData:
                                maxData = snr_value
                            if snr_value < minData:
                                minData = snr_value
                except:
                    continue

        for DR in DRs:
            if DR in excepctionDRs:
                continue
            dataSets = {}
            timeSets = {}

            for devTarget in devTargets:
                try:
                    file_path = directorio + "/" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                    with open(file_path, "r") as file:
                        for line in file:
                            lineSplit = line.split(",")
                            dataSets.setdefault(devTarget, [])
                            dataSets[devTarget].append(float(lineSplit[5]))
                            timeSets.setdefault(devTarget, [])
                            timeSets[devTarget].append(lineSplit[0])
                except:
                    print(f"Error en el directorio: {file_path}")
                    continue

            timeDic = {}
            for key in timeSets:
                timeDic[key] = [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in timeSets[key]]
            try:
                min_vector = [min(timeDic[times]) for times in timeDic]
                max_vector = [max(timeDic[times]) for times in timeDic]

                min_time = min(min_vector)
                max_time = max(max_vector)

                time_range = [min_time + datetime.timedelta(seconds=x) for x in range(int((max_time - min_time).total_seconds()) + 1)]

                timeNumbersDics = {key: [mdates.date2num(time) for time in timeDic[key]] for key in timeSets}
                time_range_numbers = mdates.date2num(time_range)

                plt.figure(figsize=(dimx, dimy))

                for key in timeSets:
                    plt.plot(timeDic[key], dataSets[key], 'o', label=labels[key])

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))

                plt.xlabel('Time')
                plt.ylabel('SNR dB')
                #plt.title(f'SNR vs Time on data rate {DR} and power {powerTarget}')
                plt.legend()
                plt.grid(True)
                plt.ylim(minData * 1.1, maxData * 0.9)
                
                # Rotar las etiquetas del eje x para que se vean mejor
                plt.xticks(rotation=60, ha='right')

                # Ajustar el diseño para evitar que las etiquetas se corten
                plt.tight_layout()

                # Guardar el gráfico como una imagen
                plt.savefig(folder + "/" + str(powerTarget) + "/SNRBetweenDevices/" + "SNRBetweenDevices_" + str(DR) + "_" + str(powerTarget) + "dBm.png")
                plt.clf()
                plt.close()

                print(f"SNR figures for the data rate {DR} with transmission power {powerTarget} created.")
            except:
                continue
    print("Graphs SNR between devices done . . . ")

def SNRLineGraphBetweenDRs(target, devTargets, powerTargets, DRs, labels, timeGraphInterval, dimx, dimy):
    dataSets = {1: [], 2: [], 3: [], 4: []}
    timeSets = {1: [], 2: [], 3: [], 4: []}

    directorio = "outputs/csv/" + target.replace(".data", "") + "/PWS"  # Cambia esto al directorio que quieras listar
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/SNRBetweenDRs"):
            os.makedirs(folder + "/" + str(powerTarget) + "/SNRBetweenDRs")

    for powerTarget in powerTargets:
        minData = 10000000
        maxData = -10000000
        for devTarget in devTargets:
            for DR in DRs:
                try:
                    with open(directorio + "/" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r") as file:
                        for line in file:
                            lineSplit = line.split(",")
                            rssi_value = float(lineSplit[5])
                            if rssi_value > maxData:
                                maxData = rssi_value
                            if rssi_value < minData:
                                minData = rssi_value
                except:
                    continue

        for devTarget in devTargets:
            dataSets = {}
            timeSets = {}
            for DR in DRs:
                try:
                    with open(directorio + "/" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r") as file:
                        for line in file:
                            lineSplit = line.split(",")
                            dataSets.setdefault(DR, []).append(float(lineSplit[5]))
                            timeSets.setdefault(DR, []).append(lineSplit[0])
                except:
                    print(f"Error en el directorio: {directorio}/{powerTarget}_{DR}_{devTarget}.csv")
                    continue

            timeDic = {key: [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in timeSets[key]] for key in timeSets}

            min_time = min(min(timeDic[times]) for times in timeDic)
            max_time = max(max(timeDic[times]) for times in timeDic)

            time_range = [min_time + datetime.timedelta(seconds=x) for x in range(int((max_time - min_time).total_seconds()) + 1)]
            time_range_numbers = mdates.date2num(time_range)

            plt.figure(figsize=(dimx, dimy))

            for key in timeSets:
                plt.plot(timeDic[key], dataSets[key], 'o', label=key)

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))

            plt.xlabel('Time')
            plt.ylabel('SNR dB')
            #plt.title(f'RSSI vs Time on {labels[devTarget]} and power {powerTarget} dBm')
            plt.legend()
            plt.grid(True)
            plt.ylim(minData * 1.1, maxData * 0.9)
            #plt.ylim(-10, 5)

            plt.xticks(rotation=60, ha='right')
            plt.tight_layout()

            plt.savefig(folder + "/" + str(powerTarget) + "/SNRBetweenDRs/SNRBetweenDR_" + str(labels[int(devTarget)]) + "_" + str(powerTarget) + "dBm.png")
            plt.clf()
            plt.close()

            print(f"SNR figures for the device {devTarget} with transmission power {powerTarget} created.")

    print("Graphs SNR between DRs done . . . ")









def boxWhiskerPDRGraphsWhitFQ(target, devTargets, powerTargets, DRs, frequencyTargets, labels,dimx, dimy):
	dataSets = {}
	for DR in DRs:
		dataSets[DR] = list()



	directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRsFq" 
	archivos = listar_archivos(directorio)

	folder = "outputs/figs/" + target.replace(".data", "")
	if not os.path.exists(folder):
	        os.makedirs(folder)

	for powerTarget in powerTargets:
		if not os.path.exists(folder + "/" + str(powerTarget)):
			os.makedirs(folder + "/" + str(powerTarget))
		if not os.path.exists(folder + "/" + str(powerTarget) + "/PDRLine/Fq"):
			os.makedirs(folder + "/" + str(powerTarget) + "/PDRLine/Fq")
		if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq"):
			os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq")


	frqs = list()
	for fileName in archivos:
		PDR, frq, power, DR, dev = fileName.split("_")
		if not(frq in frequencyTargets):
			continue
		if not (frq in frqs):
			frqs.append(frq)


	for powerTarget in powerTargets:

		for frq in frqs:

			for devTarget in devTargets:
			
				dataSets = {}
				for DR in DRs:
					dataSets[DR] = list()

				for DR in DRs:
					try:
						file = open(directorio + "/PDR_" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv","r")

						for line in file:
							lineSplit = line.split(",")
							dataSets[DR].append(float(lineSplit[1]))

						file.close()
					except:
						print("there isn't enough data for the device " + str(devTarget) + " on " +  str(DR) + " whit transmission power " + str(powerTarget) + " on frequency " + str(frq))

				data = []
				for key, values in dataSets.items():
				    for value in values:
				        data.append({"DR": key, "PDR": value})

				df = pd.DataFrame(data)
				# Crear el gráfico de diagramas de caja y bigotes
				plt.figure(figsize=(dimx, dimy))

				sns.boxplot(x='DR', y='PDR', data=df)

				# Añadir títulos y etiquetas
				plt.title(f'Packet Delivery Ratio on {labels[devTarget]} on channel on power transmission {powerTarget} frequency {frq} MHz')
				plt.xlabel('DR')
				plt.ylabel('PDR')
				plt.ylim(0, 1.1)
				# Guardar el gráfico como una imagen
				plt.savefig( folder + "/" + str(powerTarget) + "/BoxWhisker/Fq/" + str(labels[devTarget])+ "_" + str(frq).replace(".",",") + "MHz_" + str(powerTarget) + "dBm_boxWhiskerPDR_PWR.png")
				plt.close()

				plt.figure(figsize=(10, 6))

				# Crear el gráfico de líneas superpuestas
				for column in df.columns:
				    sns.lineplot(data=df[column], label=column)

				# Añadir títulos y etiquetas
				plt.title('Packet Delivery Ratio on transmission power ' + str(powerTarget))
				plt.xlabel('number of measurement')
				plt.ylabel('PDR')
				plt.ylim(0, 1.1)
				# Añadir leyenda
				plt.legend()

				# Guardar el gráfico como una imagen
				plt.savefig(folder + "/" + str(powerTarget) + "/PDRLine/Fq/" + str(devTarget)+ "_" + str(frq).replace(".",",") + "_" + "LinePDR_PWR.png")
				plt.close()

				print("Box whisker figures for the device " + str(devTarget) + " whit transmission power " + str(powerTarget) + " on frequency " + str(frq) + " created.")
	print("Box whisker graphs done . . .")

def groupedBoxWhiskerPDRGraphsWhitFQ(target, devTargets, powerTargets, DRs, frequencyTargets, labels, order_dict,dimx, dimy):
    directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRsFq"
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq"):
            os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq")

    frqs = list()
    for fileName in archivos:
        PDR, frq, power, DR, dev = fileName.split("_")
        if not (frq in frequencyTargets):
            continue
        if not (frq in frqs):
            frqs.append(frq)

    for powerTarget in powerTargets:
        for frq in frqs:
            data = []
            for DR in DRs:
                dataSets = {devTarget: [] for devTarget in devTargets}

                for devTarget in devTargets:
                    try:
                        file = open(directorio + "/PDR_" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r")
                        for line in file:
                            lineSplit = line.split(",")
                            dataSets[devTarget].append(float(lineSplit[1]))
                        file.close()
                    except:
                        print(f"There isn't enough data for the device {devTarget} on {DR} with transmission power {powerTarget} on frequency {frq}")

                for devTarget, values in dataSets.items():
                    for value in values:
                        data.append({"Device": labels[devTarget], "DR": DR, "PDR": value})

            df = pd.DataFrame(data)

            sorted_labels = sorted(labels.values(), key=lambda x: order_dict[list(labels.keys())[list(labels.values()).index(x)]])

            df['Device'] = pd.Categorical(df['Device'], categories=sorted_labels, ordered=True)

            plt.figure(figsize=(dimx, dimy))
            sns.boxplot(x="Device", y='PDR', hue='DR', data=df) # No se necesita 'hue_order' aquí

            # Añadir títulos y etiquetas
            plt.title(f'Packet Delivery Ratio on transmission power {powerTarget} and frequency {frq} MHz')
            plt.xlabel('Device')
            plt.ylabel('PDR')
            plt.ylim(0, 1.1)
            # Añadir leyenda
            plt.legend(title='DR', bbox_to_anchor=(1, 1), loc='upper left')

            # Guardar el gráfico como una imagen
            plt.savefig(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq/" + str(frq).replace(".", ",") + "_" +str(powerTarget) + "dBm_groupedBoxWhiskerPDR_PWR.png")
            plt.close()

            print(f"Grouped box whisker graph for transmission power {powerTarget} on frequency {frq} created.")
    print("Grouped box whisker graphs done . . .")

def RSSILineGraphBetweenDRsWhitFQ(target, devTargets, powerTargets, DRs, frequencyTargets, labels, timeGraphInterval, dimx, dimy):
    dataSets = {1:[], 2:[], 3:[], 4:[]}
    timeSets = {1:[], 2:[], 3:[], 4:[]}

    directorio = "outputs/csv/" + target.replace(".data", "") + "/FQS"  # Cambia esto al directorio que quieras listar
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/RSSIBetweenDRs/Fq"):
            os.makedirs(folder + "/" + str(powerTarget) + "/RSSIBetweenDRs/Fq")

    for powerTarget in powerTargets:
        minData = 10000000
        maxData = -10000000
        for devTarget in devTargets:
            for frq in frequencyTargets:
                for DR in DRs:
                    try:
                        file_path = directorio + "/" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                        with open(file_path, "r") as file:
                            for line in file:
                                lineSplit = line.split(",")
                                rssi_value = float(lineSplit[2])
                                if rssi_value > maxData:
                                    maxData = rssi_value
                                if rssi_value < minData:
                                    minData = rssi_value
                    except:
                        continue

        for devTarget in devTargets:
            for frq in frequencyTargets:
                dataSets = {}
                timeSets = {}
                for DR in DRs:
                    try:
                        file_path = directorio + "/" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                        with open(file_path, "r") as file:
                            for line in file:
                                lineSplit = line.split(",")

                                dataSets.setdefault(DR, [])
                                dataSets[DR].append(float(lineSplit[2]))

                                timeSets.setdefault(DR, [])
                                timeSets[DR].append(lineSplit[0])
                    except:
                        print(f"Error en el directorio: {file_path}")
                        continue

                timeDic = {}
                for key in timeSets:
                    timeDic[key] = [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in timeSets[key]]

                min_vector = [min(timeDic[times]) for times in timeDic]
                max_vector = [max(timeDic[times]) for times in timeDic]

                min_time = min(min_vector)
                max_time = max(max_vector)

                time_range = [min_time + datetime.timedelta(seconds=x) for x in range(int((max_time - min_time).total_seconds()) + 1)]

                timeNumbersDics = {key: [mdates.date2num(time) for time in timeDic[key]] for key in timeSets}
                time_range_numbers = mdates.date2num(time_range)

                plt.figure(figsize=(dimx, dimy))

                for key in timeSets:
                    plt.plot(timeDic[key], dataSets[key], 'o', label=key)

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))

                plt.xlabel('Time')
                plt.ylabel('RSSI')
                plt.title(f'RSSI vs Time on {labels[devTarget]} in frequency {frq} MHz')
                plt.ylim(minData * 1.1, maxData * 0.9)
                plt.legend()
                plt.grid(True)

                plt.xticks(rotation=60, ha='right')
                plt.tight_layout()

                plt.savefig(folder + "/" + str(powerTarget) + "/RSSIBetweenDRs/Fq/RSSIOnBetweenDR_" + str(labels[devTarget]) + "_" + str(frq) + "MHz_" + str(powerTarget) + "dBm.png")
                plt.clf()
                plt.close()

        print(f"RSSI figures for the device {devTarget} with transmission power {powerTarget} and frequency {frq} created.")
    print("Graphs RSSI between DRs done . . . ")

def RSSILineGraphBetweenDevicesWhitFQ(target, devTargets, powerTargets, DRs, frequencyTargets, labels, timeGraphInterval, dimx, dimy):
    directorio = "outputs/csv/" + target.replace(".data", "") + "/FQS"
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/RSSIBetweenDevices/Fq"):
            os.makedirs(folder + "/" + str(powerTarget) + "/RSSIBetweenDevices/Fq")

    for powerTarget in powerTargets:
        minData = 10000000
        maxData = -10000000
        for DR in DRs:
            for frq in frequencyTargets:
                for devTarget in devTargets:
                    try:
                        file_path = directorio + "/" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                        with open(file_path, "r") as file:
                            for line in file:
                                lineSplit = line.split(",")
                                value = float(lineSplit[2])
                                if value > maxData:
                                    maxData = value
                                if value < minData:
                                    minData = value
                    except:
                        continue

        for DR in DRs:
            for frq in frequencyTargets:
                dataSets = {}
                timeSets = {}

                for devTarget in devTargets:
                    try:
                        file_path = directorio + "/" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                        with open(file_path, "r") as file:
                            for line in file:
                                lineSplit = line.split(",")
                                dataSets.setdefault(devTarget, [])
                                dataSets[devTarget].append(float(lineSplit[2]))
                                timeSets.setdefault(devTarget, [])
                                timeSets[devTarget].append(lineSplit[0])
                    except:
                        print("Error en el directorio: " + file_path)
                        continue

                timeDic = {}
                for key in timeSets:
                    timeDic[key] = [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in timeSets[key]]

                min_vector = []
                max_vector = []
                for times in timeDic.values():
                    min_vector.append(min(times))
                    max_vector.append(max(times))

                min_time = min(min_vector)
                max_time = max(max_vector)

                time_range = [min_time + datetime.timedelta(seconds=x) for x in range(int((max_time - min_time).total_seconds()) + 1)]

                timeNumbersDics = {}
                for key in timeSets:
                    timeNumbersDics[key] = [mdates.date2num(time) for time in timeDic[key]]

                time_range_numbers = mdates.date2num(time_range)

                # Crear el gráfico
                plt.figure(figsize=(dimx, dimy))

                for key in timeSets:
                    plt.plot(timeDic[key], dataSets[key], 'o', label=labels[key])

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))  # Ajusta el intervalo según sea necesario

                plt.xlabel('Time')
                plt.ylabel('RSSI')
                #plt.title(f'RSSI vs Time on {DR} with transmission power {powerTarget} in frequency {frq} MHz')
                plt.legend()
                plt.ylim(minData * 1.1, maxData * 0.9)
                plt.grid(True)

                # Rotar las etiquetas del eje x para que se vean mejor
                plt.xticks(rotation=60, ha='right')

                # Ajustar el diseño para evitar que las etiquetas se corten
                plt.tight_layout()

                # Guardar el gráfico como una imagen
                plt.savefig(folder + "/" + str(powerTarget) + "/RSSIBetweenDevices/Fq/" + "RSSIBetweenDevices_" + str(DR) + "_" + str(frq) + "MHz_" + str(powerTarget) + "dBm.png")
                plt.clf()
                plt.close()

            print(f"Rssi figures for Data rate {DR} with transmission power {powerTarget} on frequency {frq} created.")
    print("Graphs RSSI between devices done . . .")

def SNRLineGraphBetweenDevicesWhitFQ(target, devTargets, powerTargets, DRs, frequencyTargets, labels, timeGraphInterval, dimx, dimy):
    directorio = "outputs/csv/" + target.replace(".data", "") + "/FQS"
    archivos = listar_archivos(directorio)

    excepctionDRs = ["DR8", "DR9", "DR10", "DR11"]

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/SNRBetweenDevices/Fq"):
            os.makedirs(folder + "/" + str(powerTarget) + "/SNRBetweenDevices/Fq")

    for powerTarget in powerTargets:
        minData = 10000000
        maxData = -10000000
        for DR in DRs:
            for frq in frequencyTargets:
                for devTarget in devTargets:
                    try:
                        file_path = directorio + "/" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                        with open(file_path, "r") as file:
                            for line in file:
                                lineSplit = line.split(",")
                                value = float(lineSplit[4])
                                if value > maxData:
                                    maxData = value
                                if value < minData:
                                    minData = value
                    except:
                        continue

        for DR in DRs:
            if DR in excepctionDRs:
                continue
            for frq in frequencyTargets:
                dataSets = {}
                timeSets = {}

                for devTarget in devTargets:
                    try:
                        file_path = directorio + "/" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv"
                        with open(file_path, "r") as file:
                            for line in file:
                                lineSplit = line.split(",")
                                dataSets.setdefault(devTarget, [])
                                dataSets[devTarget].append(float(lineSplit[4]))
                                timeSets.setdefault(devTarget, [])
                                timeSets[devTarget].append(lineSplit[0])
                    except:
                        print("Error en el directorio: " + file_path)
                        continue

                timeDic = {}
                for key in timeSets:
                    timeDic[key] = [datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in timeSets[key]]

                min_vector = []
                max_vector = []
                for times in timeDic.values():
                    min_vector.append(min(times))
                    max_vector.append(max(times))

                try:
                    min_time = min(min_vector)
                    max_time = max(max_vector)
                except:
                    continue
                time_range = [min_time + datetime.timedelta(seconds=x) for x in range(int((max_time - min_time).total_seconds()) + 1)]

                timeNumbersDics = {}
                for key in timeSets:
                    timeNumbersDics[key] = [mdates.date2num(time) for time in timeDic[key]]

                time_range_numbers = mdates.date2num(time_range)

                # Crear el gráfico
                plt.figure(figsize=(dimx, dimy))

                for key in timeSets:
                    plt.plot(timeDic[key], dataSets[key], 'o', label=labels[key])

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
                plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=timeGraphInterval))  # Ajusta el intervalo según sea necesario

                plt.xlabel('Time')
                plt.ylabel('SNR')
                plt.title(f'SNR vs Time on {DR} with transmission power {powerTarget} in frequency {frq} MHz')
                plt.legend()
                plt.ylim(minData * 1.1, maxData * 0.9)
                plt.grid(True)

                # Rotar las etiquetas del eje x para que se vean mejor
                plt.xticks(rotation=60, ha='right')

                # Ajustar el diseño para evitar que las etiquetas se corten
                plt.tight_layout()

                # Guardar el gráfico como una imagen
                plt.savefig(folder + "/" + str(powerTarget) + "/SNRBetweenDevices/Fq/" + "SNRBetweenDevices_" + str(DR) + "_" + str(frq) + "MHz_" + str(powerTarget) + "dBm.png")
                plt.clf()
                plt.close()

            print(f"SNR figures for Data rate {DR} with transmission power {powerTarget} on frequency {frq} created.")
    print("Graphs SNR between devices done . . .")













def groupedBoxWhiskerPDRGraphs2(target, devTargets, powerTargets, DRs, labels, dimx, dimy):
    directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker"):
            os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker")

  
    for powerTarget in powerTargets:
        data = []
        for devTarget in devTargets:
            dataSets = {DR: [] for DR in DRs}

            for DR in DRs:
                try:
                    file = open(directorio + "/PDR_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r")
                    for line in file:
                        lineSplit = line.split(",")
                        dataSets[DR].append(float(lineSplit[4]))
                    file.close()
                except:
                    print(f"There isn't enough data for the device {devTarget} on {DR} with transmission power {powerTarget}")

            for DR, values in dataSets.items():
                for value in values:
                    data.append({"Device": labels[devTarget], "DR": DR, "PDR": value})

        df = pd.DataFrame(data)

        sorted_DRs = sorted(DRs, key=custom_sort_key)

        df['DR'] = pd.Categorical(df['DR'], categories=sorted_DRs, ordered=True)

        
        plt.figure(figsize=(dimx, dimy))
        sns.boxplot(x='DR', y='PDR', hue='Device', data=df, width=0.5)

        # Añadir títulos y etiquetas
        plt.title(f'Packet Delivery Ratio on transmission power {powerTarget} dBm')
        plt.xlabel('DR')
        plt.ylabel('PDR')
        plt.ylim(0, 1.1)
        # Añadir leyenda
        plt.legend(title='location')

        # Guardar el gráfico como una imagen
        plt.savefig(folder + "/" + str(powerTarget) + "/BoxWhisker/" + str(powerTarget) + "dBm_groupedBoxWhiskerPDR.png")
        plt.close()

        print(f"Grouped box whisker graph for transmission power {powerTarget}.")
    print("Grouped box whisker graphs done . . .")

def groupedBoxDevicesWhiskerPDRGraphs2(target, devTargets, powerTargets, DRs, labels, order_dict, dimx, dimy):
    directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRs"
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker"):
            os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker")

    for powerTarget in powerTargets:
        data = []
        for DR in DRs:
            dataSets = {devTarget: [] for devTarget in devTargets}

            for devTarget in devTargets:
                try:
                    file = open(directorio + "/PDR_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r")
                    for line in file:
                        lineSplit = line.split(",")
                        dataSets[devTarget].append(float(lineSplit[4]))
                    file.close()
                except:
                    print(f"There isn't enough data for the device {devTarget} on {DR} with transmission power {powerTarget}")

            for devTarget, values in dataSets.items():
                for value in values:
                    data.append({"Device": labels[int(devTarget)], "DR": DR, "PDR": value})

        df = pd.DataFrame(data)

        sorted_labels = sorted(labels.values(), key=lambda x: order_dict[list(labels.keys())[list(labels.values()).index(x)]])

        # Ordenar dispositivos en el eje x
        df['Device'] = pd.Categorical(df['Device'], categories=sorted_labels, ordered=True)

        plt.figure(figsize=(dimx, dimy))
        sns.boxplot(x="Device", y='PDR', hue='DR', data=df) 

        # Añadir títulos y etiquetas

        #plt.title(f'Packet Delivery Ratio on transmission power {powerTarget} dBm')
        plt.xlabel('Device')
        plt.ylabel('PDR')
        plt.ylim(0, 1.1)
        # Añadir leyenda
        plt.legend(title='DR', bbox_to_anchor=(1, 1), loc='upper left')

        # Guardar el gráfico como una imagen
        plt.savefig(folder + "/" + str(powerTarget) + "/BoxWhisker/" + str(powerTarget) + "dBm_groupedDeviceBoxWhiskerPDR.png")
        plt.close()

        print(f"Grouped box whisker graph for transmission power {powerTarget}.")
    print("Grouped box whisker graphs done . . .")



def boxWhiskerPDRGraphsWhitFQ2(target, devTargets, powerTargets, DRs, frequencyTargets, labels,dimx, dimy):
    dataSets = {}
    for DR in DRs:
        dataSets[DR] = list()



    directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRsFq" 
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
            os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/PDRLine/Fq"):
            os.makedirs(folder + "/" + str(powerTarget) + "/PDRLine/Fq")
        if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq"):
            os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq")


    frqs = list()
    for fileName in archivos:
        PDR, frq, power, DR, dev = fileName.split("_")
        if not(frq in frequencyTargets):
            continue
        if not (frq in frqs):
            frqs.append(frq)


    for powerTarget in powerTargets:

        for frq in frqs:

            for devTarget in devTargets:
            
                dataSets = {}
                for DR in DRs:
                    dataSets[DR] = list()

                for DR in DRs:
                    try:
                        file = open(directorio + "/PDR_" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv","r")

                        for line in file:
                            lineSplit = line.split(",")
                            dataSets[DR].append(float(lineSplit[4]))

                        file.close()
                    except:
                        print("there isn't enough data for the device " + str(devTarget) + " on " +  str(DR) + " whit transmission power " + str(powerTarget) + " on frequency " + str(frq))

                data = []
                for key, values in dataSets.items():
                    for value in values:
                        data.append({"DR": key, "PDR": value})

                df = pd.DataFrame(data)
                # Crear el gráfico de diagramas de caja y bigotes
                plt.figure(figsize=(dimx, dimy))

                sns.boxplot(x='DR', y='PDR', data=df)

                # Añadir títulos y etiquetas
                plt.title(f'Packet Delivery Ratio on {labels[int(devTarget)]} on channel on power transmission {powerTarget} frequency {frq} MHz')
                plt.xlabel('DR')
                plt.ylabel('PDR')
                plt.ylim(0, 1.1)
                # Guardar el gráfico como una imagen
                plt.savefig( folder + "/" + str(powerTarget) + "/BoxWhisker/Fq/" + str(labels[int(devTarget)])+ "_" + str(frq).replace(".",",") + "MHz_" + str(powerTarget) + "dBm_boxWhiskerPDR_PWR.png")
                plt.close()

                plt.figure(figsize=(10, 6))

                # Crear el gráfico de líneas superpuestas
                for column in df.columns:
                    sns.lineplot(data=df[column], label=column)

                # Añadir títulos y etiquetas
                plt.title('Packet Delivery Ratio on transmission power ' + str(powerTarget))
                plt.xlabel('number of measurement')
                plt.ylabel('PDR')
                plt.ylim(0, 1.1)
                # Añadir leyenda
                plt.legend()

                # Guardar el gráfico como una imagen
                plt.savefig(folder + "/" + str(powerTarget) + "/PDRLine/Fq/" + str(devTarget)+ "_" + str(frq).replace(".",",") + "_" + "LinePDR_PWR.png")
                plt.close()

                print("Box whisker figures for the device " + str(devTarget) + " whit transmission power " + str(powerTarget) + " on frequency " + str(frq) + " created.")
    print("Box whisker graphs done . . .")

def groupedBoxWhiskerPDRGraphsWhitFQ2(target, devTargets, powerTargets, DRs, frequencyTargets, labels, order_dict,dimx, dimy):
    directorio = "outputs/csv/" + target.replace(".data", "") + "/PDRsFq"
    archivos = listar_archivos(directorio)

    folder = "outputs/figs/" + target.replace(".data", "")
    if not os.path.exists(folder):
        os.makedirs(folder)

    for powerTarget in powerTargets:
        if not os.path.exists(folder + "/" + str(powerTarget)):
            os.makedirs(folder + "/" + str(powerTarget))
        if not os.path.exists(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq"):
            os.makedirs(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq")

    frqs = list()
    for fileName in archivos:
        PDR, frq, power, DR, dev = fileName.split("_")
        if not (frq in frequencyTargets):
            continue
        if not (frq in frqs):
            frqs.append(frq)

    for powerTarget in powerTargets:
        for frq in frqs:
            data = []
            for DR in DRs:
                dataSets = {devTarget: [] for devTarget in devTargets}

                for devTarget in devTargets:
                    try:
                        file = open(directorio + "/PDR_" + str(frq) + "_" + str(powerTarget) + "_" + DR + "_" + str(devTarget) + ".csv", "r")
                        for line in file:
                            lineSplit = line.split(",")
                            dataSets[devTarget].append(float(lineSplit[4]))
                        file.close()
                    except:
                        print(f"There isn't enough data for the device {devTarget} on {DR} with transmission power {powerTarget} on frequency {frq}")

                for devTarget, values in dataSets.items():
                    for value in values:
                        data.append({"Device": labels[int(devTarget)], "DR": DR, "PDR": value})

            df = pd.DataFrame(data)

            sorted_labels = sorted(labels.values(), key=lambda x: order_dict[list(labels.keys())[list(labels.values()).index(x)]])

            df['Device'] = pd.Categorical(df['Device'], categories=sorted_labels, ordered=True)

            plt.figure(figsize=(dimx, dimy))
            sns.boxplot(x="Device", y='PDR', hue='DR', data=df) # No se necesita 'hue_order' aquí

            # Añadir títulos y etiquetas
            plt.title(f'Packet Delivery Ratio on transmission power {powerTarget} and frequency {frq} MHz')
            plt.xlabel('Device')
            plt.ylabel('PDR')
            plt.ylim(0, 1.1)
            # Añadir leyenda
            plt.legend(title='DR', bbox_to_anchor=(1, 1), loc='upper left')

            # Guardar el gráfico como una imagen
            plt.savefig(folder + "/" + str(powerTarget) + "/BoxWhisker/Fq/" + str(frq).replace(".", ",") + "_" +str(powerTarget) + "dBm_groupedBoxWhiskerPDR_PWR.png")
            plt.close()

            print(f"Grouped box whisker graph for transmission power {powerTarget} on frequency {frq} created.")
    print("Grouped box whisker graphs done . . .")
