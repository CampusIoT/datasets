import figuresGenerator as fg
import separator as sp
import FiguresGeneratorJuly as fgj


import shutil
import os


#########################################

target = "patches2.data" #Raw data to be analyze
devTargets = [1,2,3,4] #wich ID devices will be analyzed
powerTargets = [2,8,14] #wich tranmission power will be analyzed
#powerTargets = [8]
timeInterval = 60*8 # Time interval to be use in the PDR calculation
DRs = ["DR0","DR1","DR2","DR3","DR4","DR5","DR6","DR8","DR9","DR10", "DR11"] #Wich DR will be used
Frequencis = [866.1, 865.9] #wich frequencies will be used
#Frequencis = [866.1, 865.9, 866.3, 865.7]
labels = {1:"600 m", 2:"400 m", 3:"1.5 Km", 4:"765 m"} #the correlation between devices ID and labels, the key is the device ID, the value the label

labelsOrder = {2:1, 1:2, 3:4, 4:3} #order of the devices ID to be deployed in the 
deltaTimeInGraphSeconds = 60*60*30 # Resolution of time plots


#########################################

#Devices separator
#sp.cleanOldData(target)

#sp.DevSeparator(target)

#sp.DRSeparator(target, devTargets)

#sp.PowerSeparator(target, devTargets)

#sp.freqSeparator(target, devTargets, powerTargets, Frequencis)

#sp.PDRGenerator(target, devTargets, powerTargets, timeInterval, Frequencis)

#sp.PDRCalculatorApril(target, devTargets, powerTargets, timeInterval, Frequencis)

#sp.PDRGeneratorWhitFQ(target, devTargets, powerTargets, timeInterval)

#sp.PDRCalculatorAprilFq(target, devTargets, powerTargets, timeInterval)



#########################################


# IMAGES ON ALL FREQUENCY CHANNELS

#fg.boxWhiskerPDRGraphs(target, devTargets, powerTargets, DRs,labels)

#fg.groupedBoxDevicesWhiskerPDRGraphs(target, devTargets, powerTargets, DRs, labels, labelsOrder, 10, 4)

#fg.groupedBoxDevicesWhiskerPDRGraphs2(target, devTargets, powerTargets, DRs, labels, labelsOrder, 10, 4)

#fg.RSSILineGraphBetweenDRs(target, devTargets, powerTargets, DRs, labels, deltaTimeInGraphSeconds, 4, 3)

#fg.RSSILineGraphBetweenDevices(target, devTargets, powerTargets, DRs ,labels, deltaTimeInGraphSeconds,4, 5)

#fg.SNRLineGraphBetweenDevices(target, devTargets, powerTargets, DRs ,labels, deltaTimeInGraphSeconds, 7, 4)

#fg.SNRLineGraphBetweenDRs(target, devTargets, powerTargets, DRs, labels, deltaTimeInGraphSeconds, 4, 3)


# IMAGES ON EACH FREQUENCY CHANNELS

#fg.boxWhiskerPDRGraphsWhitFQ(target, devTargets, powerTargets, DRs, Frequencis, labels, 10, 4)

#fg.groupedBoxWhiskerPDRGraphsWhitFQ(target, devTargets, powerTargets, DRs, Frequencis, labels, labelsOrder, 10 , 4)

#fg.RSSILineGraphBetweenDRsWhitFQ(target, devTargets, powerTargets, DRs, Frequencis, labels, deltaTimeInGraphSeconds)

#fg.RSSILineGraphBetweenDevicesWhitFQ(target, devTargets, powerTargets, DRs, Frequencis ,labels, deltaTimeInGraphSeconds, 4, 5)

#fg.SNRLineGraphBetweenDevicesWhitFQ(target, devTargets, powerTargets, DRs, Frequencis ,labels, deltaTimeInGraphSeconds)


#fg.boxWhiskerPDRGraphsWhitFQ2(target, devTargets, powerTargets, DRs, Frequencis, labels, 10, 4)

#fg.groupedBoxWhiskerPDRGraphsWhitFQ2(target, devTargets, powerTargets, DRs, Frequencis, labels, labelsOrder, 10 , 4)
