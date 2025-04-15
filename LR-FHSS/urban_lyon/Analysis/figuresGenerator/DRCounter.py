import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec



def generate_array(start, step, stop):
    result = []
    aumento = 0
    while round(start + aumento, 2) < stop:
        value = round(start + aumento, 2)
        result.append(value)
        aumento += step
    return result

#########################################

#File to be opened
file = open("../files/2024-07-26DRSeker.data")

x = 14 # X dimension for the plot file
y = 4 # Y dimension for the plot file

#########################################


dataSets = []

DRs = []

for DR in range(0, 6):
    DRs.append("DR" + str(DR))

DR_data = {}
Freq_data = {}

for line in file:
    lineSplit = line.split(",")
    DR = lineSplit[0]
    freq = lineSplit[2].lstrip(" ").rstrip("\n")
    if DR in DRs:
        dataSets.append({"DR": DR, "Frequency": float(freq)})

    if freq in Freq_data:
        Freq_data[freq] += 1
    else:
        Freq_data[freq] = 1

    if DR in DRs:
        if DR in DR_data:
            DR_data[DR] += 1
        else:
            DR_data[DR] = 1

file.close()

DRs = ["DR0", "DR1", "DR2", "DR3", "DR4", "DR5", "DR6"]

freq_vect = generate_array(864.9, 0.1, 868.9)

for frq in freq_vect:
    frq_float = float(frq)
    if frq_float in Freq_data:
        continue
    Freq_data[str(frq_float)] = 0
    for DR in DRs:
        dataSets.append({"DR": DR, "Frequency": frq_float})

df = pd.DataFrame(dataSets)

print("DR: ")
print(DR_data)

print("")

print("Frequency:")
print(Freq_data)

# Crear una tabla de conteo para las combinaciones de DR y Frequency
conteo_combinaciones = df.groupby(['DR', 'Frequency']).size().unstack(fill_value=0)

# Crear el heatmap con GridSpec para ajustar la posición de la barra de color
fig = plt.figure(figsize=(x, y))
gs = GridSpec(1, 2, width_ratios=[50, 1], wspace=0.05)

ax = fig.add_subplot(gs[0])
cax = fig.add_subplot(gs[1])

sns.heatmap(conteo_combinaciones, annot=False, fmt="d", cmap="coolwarm", ax=ax, cbar_ax=cax, cbar_kws={'label': 'Count'})

# Configuración de etiquetas y título
ax.set_xlabel('Frequency MHz')
ax.set_ylabel('DR')

# Ajustar diseño para evitar que el texto se corte y reducir el espacio blanco a la izquierda
plt.subplots_adjust(left=0.05, bottom=0.2, right=0.95, top=0.9)

# Guardar el gráfico como una imagen
plt.savefig("outputs/figs/DR_frequency_sekeer.png")

