# Content

This directory contains the Python codes and some dependencies for the codes (gpx files, a specific description for these files can be found [here](https://gitlab.inria.fr/jfraire/lr-fhss-experiments/-/tree/master/Data/RawData#naming-format-and-content-of-the-gpx-files)).

In this readme file the codes will be explained in order to change the pictures generated:

A quick introduction to each code is presented here:

bicycleGraphs: Generate the RSSI plots vs distance on the bicycles rides
DRCounter: Generate the DRs and frequency heatmaps
ExperimentsJuly: Generate the plots for the experiments done in July (second iteration)
ExperimentsMayJune: Generate the plots for the experiments done in may and June (first iteration)
figuresGenerator: Package used to generate the figures on the experiments of May and June
figuresGeneratorJuly: Package used to generate the figures on the experiments of July
PDR_velo: Generate the PDR related plots on the bicycle experiments
separator: Package used to analyze the raw data (separation of data, PDR calculation, etc)
TimeOnAir: Generate the TimeOnAir plots

## Important information

On the second iteration of the experiments I encountered some bugs on the firmware, for this reason, there are data on 20dBm, this could be analyzed, but it is not very interesting, other than that 2dBm and 8 dBm are used in two devices.

Another bug was found on the LR-FHSS counter, normally devices would send a counter like: 1,2,3,4,5,6... with that counter the PDR is calculated, during the second iteration in LR-FHSS (and only on LR-FHSS) the counter is duplicated, i.e. something like 1,1,2,2,3,3,4,4...
The time between duplication is regular (between 1,1 or 2,2), as the time between different counters (between 1,2 or 3,4), but they are different. using the time pattern and knowing that the counters are duplicated the counters can be fixed to calculate the PDR, this counter fixing is done in the separation files, to fix raw data a single condition must be met. A duplication of counters must be found somewhere in the raw data, once a duplication is found, all the counters can be fixed, this condition is met in all the raw data files in produce during the experiments.

## bicycleGraphs

This code generates the RSSI plot vs distance on the bicycle rides, the code is separated into three sections, and the division is marked as

```
#########################################
```
The code is divided into 5 sections:
1. Contains the dependencies used in the code (there may be some redundancy or unused packages)
2. It contains the parameters used in the process of gathering the raw data (if needed) and generates the plots. 
3. Definitions of the functions used in the code. 
4. Processing of the raw data: Uncomment if you don't need to process the data; it's recommended to comment if you don't.
5. Generate the RSSI vs distance plots.
If you want to change the specific features of the plot you may need to modify the code directly, in that case, you search for the definition of the 
``` RSSILineGraphBetweenDRs(target, devTargets, DRs, xlim = [], ylim = []) ``` function, there at the end you'll see the specific configurations of the plot, it's something like this:
```
plt.xlabel('Distance Km')
        plt.ylabel('RSSI dBm')
        #plt.title(f'RSSI vs Distance on {label[devTarget]} and power {powerTarget} dBm')process the data; it's recommended to comment if you don't.
Generate the RSSI vs distance plots.
```
If you want to change the plot's specific features you may need to modify the code directly, in that case, you search for the definition of the function
``` RSSILineGraphBetweenDRs(target, devTargets, DRs, xlim = [], ylim = []) ``` function, there at the end you'll see the specific configurations of the plot, it's something like this:
```
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
    	(...)
```
There you can change the specifics of the graph
 *Before changing this you should see if you can achieve the desired modification by changing the parameters, the descriptions of the parameters are found in the code itself*

## DRCounter

This code generates the density heatmap of DR and frequency, the code is divided into differents sections, each section is separated by:

```
#########################################
```
The code is divided into 3 sections:
1. Contains the dependencies used in the code (there may be some redundancy or unused packages)
2. Parameters to generate the graph.
3. Code to compute and generate the graph

If you want to change the plot's specific features you may need to modify the code directly, in that case, you search at the end of the code for the following snippet of code.
```
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
```
You should modify this section of the code, it's using the seaborn package

 *Before changing this you should see if you can achieve the desired modification by changing the parameters, the descriptions of the parameters are found in the code itself*

# ExperimentJuly
 This code generates all the plots from the experiments done in July (the second iteration of the experiment, changing CR, packet length, alternating between good and bad channels, etc.)

 The code is divided into different sections, each section is separated by:

```
#########################################
```
The code is divided into 4 sections:
Contains the dependencies used in the code (there may be some redundancy or unused packages)
Parameters to generate the figures
Data analysis, in this section the raw data is analyzed to recalculate the PDR and others indicators, if you should use this section every time you change one of the parameters in the parameters section.
Figures generation, in this section, the analyzed data is used to generate the plots, you could comment the pictures that you don't want to produce, and figures will be generated in a children directory: outputs/figures/(name of target)/(output), to change the size of the figures you should edit the dimensions in the functions calls directly, they are the only no-variables inputs on the function, the first is the x dimension, the second one is the y dimension

If you want to change the plot's specific features you may need to modify the code directly, in that case, you will need to alter the packages FiguresGeneratorJuly.py, this package contains all the functions use to generate the plots, look for the specific function in the said packages and look at the end of the function, usually something like this:
```
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
```
You should modify this section of the code, it's using the seaborn package.

 *Before changing this you should see if you can achieve the desired modification by changing the parameters, the descriptions of the parameters are found in the code itself*

# ExperimentsMayJune

This code generates all the plots from the experiments done in July (the first iteration of the experiment, changing DR, transmission power, weird behaving channels i.e. channels with low sensitivity)

The code is divided into different sections, each section is separated by:

```
#########################################
```
The code is divided into 4 sections:
1. Contains the dependencies used in the code (there may be some redundancy or unused packages)
2. Parameters to generate the figures
3. Data analysis, in this section the raw data is analyzed to recalculate the PDR and others indicators, if you should use this section every time you change one of the parameters in the parameters section.
4. Figures generation, in this section, the analyzed data is used to generate the plots, you could comment the pictures that you don't want to produce, and figures will be generated in a children directory: outputs/figures/(name of target)/(output), to change the size of the figures you should edit the dimensions in the functions calls directly, they are the only no-variables inputs on the function, the first is the x dimension, the second one is the y dimension
If you want to change the plot's specific features you may need to modify the code directly, in that case, you will need to alter the packages FiguresGeneratorJuly.py, this package contains all the functions use to generate the plots, look for the specific function in the said packages and look at the end of the function, usually something like this:
```
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
```
You should modify this section of the code, it's using the seaborn package.

 *Before changing this you should see if you can achieve the desired modification by changing the parameters, the descriptions of the parameters are found in the code itself* 

# PDR_velo

This code generates all the plots from the experiments bike experiments, only the PDRs related ones.

The code is divided into different sections, each section is separated by:

```
#########################################
```
The code is divided into 4 sections:
1. Contains the dependencies used in the code (there may be some redundancy or unused packages)
2. Parameters to generate the figures
3. Function definitions
4. Figures generation, in this section, the analyzed data is used to generate the plots, if you don't desire to generate certains plots check the parameters section, *note: in order to generate histogram plots you'll need to use only one DR at a time, otherwise an error will occur*
If you want to change the plot's specific features you may need to modify the code directly, in that case, you will need to alter the functions, look for the desire function and look at the end of it, until you find something like (not exactly as):
```
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
```
You should modify this section of the code, it's using the seaborn package.

 *Before changing this you should see if you can achieve the desired modification by changing the parameters, the descriptions of the parameters are found in the code itself*


# TimeOnAir
 
This code generates the plot TimeOnAir plots

The code is divided into different sections, each section is separated by:

```
#########################################
```
The code is divided into 3 sections:
1. Contains the dependencies used in the code (there may be some redundancy or unused packages)
2. Time on Air calculation procedure
3. Figures generation
If you want to change the plot's specific features you may need to modify the code directly, in that case, you will need to alter the script, look for the end of the script, until you find:
```
df = pd.DataFrame(data_list)

# Crear el gráfico de dispersión
plt.figure(figsize=(7, 5))
sns.scatterplot(data=df, x='x', y='y', hue='DR', palette=custom_palette)

# Configurar las etiquetas y título
plt.gca().invert_yaxis()
plt.grid(True)
plt.xlabel('Number of bytes sent')
plt.ylabel('Time on air ms')
plt.legend(title='DRs', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("ToA.png")
```
You should modify this section of the code, it's using the seaborn package.

# FiguresGenerator and FiguresGeneratorJuly

These packages generate the plots for the first and second iterations of the experiments, here you may modify the plots.

# separator
This package does all the data analysis, for whatever reason you which to change the way the PDR is calculated, this is the package to modify