import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np

#########################################

# Definir los DR0 a DR6 con una paleta y los DR8/DR10 a DR9/DR11 con otra
dr_paleta_1 = sns.color_palette("Blues", 7)  # Colores para DR0 a DR6
dr_paleta_2 = sns.color_palette("Reds", 2)   # Colores para DR8/DR10 y DR9/DR11

# Definir las paletas personalizadas unidas
custom_palette = {
    'DR0': dr_paleta_1[6],
    'DR1': dr_paleta_1[5],
    'DR2': dr_paleta_1[4],
    'DR3': dr_paleta_1[3],
    'DR4': dr_paleta_1[2],
    'DR5': dr_paleta_1[1],
    'DR6': dr_paleta_1[0],
    'DR8/DR10': dr_paleta_2[1],
    'DR9/DR11': dr_paleta_2[0]
}

data_rates = {
    'DR0': {'SF': 12, 'BW': 125e3, 'marker': 'o'},  
    'DR1': {'SF': 11, 'BW': 125e3, 'marker': 's'},  
    'DR2': {'SF': 10, 'BW': 125e3, 'marker': 'D'},  
    'DR3': {'SF': 9, 'BW': 125e3, 'marker': 'v'},   
    'DR4': {'SF': 8, 'BW': 125e3, 'marker': '^'},   
    'DR5': {'SF': 7, 'BW': 125e3, 'marker': 'P'},   
    'DR6': {'SF': 7, 'BW': 250e3, 'marker': 'X'},   
}

# Parámetros fijos
CR = 1
H = 0   
DE = {7: 0, 8: 0, 9: 0, 10: 1, 11: 1, 12: 1}  




def calculate_toa(sf, bw, cr, pl, de, h):
    t_sym = (2 ** sf) / bw  # Tiempo de símbolo en ms
    payload_symb_nb = 8 + max(np.ceil((8 * pl - 4 * sf + 28 + 16 - 20 * h) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    n_preamble = 12247
    t_preamble = t_sym*(n_preamble + 4.25)
    return t_sym * payload_symb_nb * 1000 + t_preamble

dataSets = {}
DRs = ['DR0', 'DR1', 'DR2', 'DR3', 'DR4', 'DR5', 'DR6', 'DR8/DR10', 'DR9/DR11']

for DR in DRs:
    dataSets[DR] = {}
nBytes = 0
lim = 51
add = 2
#for nBytes in range(0, 51):
while nBytes < lim:
    pl = nBytes + 0
    for DR in ['DR0', 'DR1', 'DR2', 'DR3', 'DR4', 'DR5', 'DR6']:
        dataSets[DR][nBytes] = calculate_toa(data_rates[DR]['SF'], data_rates[DR]['BW'], CR, pl, DE[data_rates[DR]['SF']], H)
    dataSets['DR8/DR10'][nBytes] = str((math.ceil((nBytes + 3) / 2) * 102.4) + 3 * 233.472)
    dataSets['DR9/DR11'][nBytes] = str((math.ceil((nBytes + 3) / 4) * 102.4) + 2 * 233.472)
    nBytes += add

# Convertir el diccionario a un DataFrame
data_list = []
for dr, values in dataSets.items():
    for x, y in values.items():
        data_list.append({'DR': dr, 'x': x, 'y': y})

#########################################

df = pd.DataFrame(data_list)

# Crear el gráfico de dispersión
plt.figure(figsize=(7, 5)) # Plots figure dimension
sns.scatterplot(data=df, x='x', y='y', hue='DR', palette=custom_palette)

# Configurar las etiquetas y título
plt.gca().invert_yaxis()
plt.grid(True)
plt.xlabel('Number of bytes sent')
plt.ylabel('Time on air ms')
plt.legend(title='DRs', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("ToA.png")

