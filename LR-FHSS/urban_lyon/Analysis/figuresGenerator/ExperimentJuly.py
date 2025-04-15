import FiguresGeneratorJuly as fg
import separator as sp

#########################################

target = "patches5.data" #raw data to analyze
devTargets = [2,4] #ID of devices to be used
powerTargets = [2,8,14] #wich transmission power will be used
#powerTargets = [2]

Frequencis = [868.5, 867.9,866.1, 865.9,       868.0, 868.6] #wich frequency targets will be used
#Frequencis = [868.5, 867.9,       868.0, 868.6] #Bad channels  :(
#Frequencis = [866.1, 865.9,       868.0, 868.6] #Good channels :)
#Frequencis = [868.0, 868.6]

CRTargets = ["4/5","4/6", "4/7", "4/8",  "5/6", "4/6", "4/8", "1/3"] #wich coding rates will be used
LenTargets = ["20","51","100"] #wich length target could be used
#LenTargets = ["20"]

labels = {1:"600 m", 2:"400 m", 3:"1.5 Km", 4:"770 m"} # labels to be used in the plots, the key is the ID of device, the value is the label
#labels = {1:"600 m", 2:"400 m", 3:"first floor", 4:" third floor"}
labelsOrder = {2:1, 1:2, 3:4, 4:3} # in which order the labels will be plotted, the key is the ID of device, the value is the order

minute = 60 
hour = 60*minute
day = 24*hour

deltaTimeInGraphSeconds = 2*day # resolution of time plots

WindowPDR = 20 # with how many frames the PDR is calculated with

Output = "PresentationBC" #folder to save the figures

#########################################

#Data analysis

sp.cleanOldData(target)

sp.DevSeparator2(target)

sp.modulationSeparator(target, devTargets, Frequencis)

sp.codingRateSeparator(target, CRTargets)

sp.PowerSeparatorJuly(target,powerTargets)

sp.BWSFSeparator(target)

sp.lengthSeparator(target,LenTargets)

sp.frequencySeparatorJuly(target)

sp.calculatePDRJulyFrq(target, WindowPDR)

sp.calculatePDRJuly(target, WindowPDR)


######################################### 	


#Figures generator

fg.meanPDR(target, devTargets, labels ,4,2.5,Output)

fg.meanPDRFrq(target, devTargets, labels ,4,2.5,Output)

fg.PDRvsTimeLen(target, devTargets,CRTargets ,labels ,14,10,Output, deltaTimeInGraphSeconds)

fg.PDRvsTimeCR(target, devTargets,LenTargets ,labels ,14,10,Output, deltaTimeInGraphSeconds)

fg.RSSILineGraphBetweenConfigurationsLen(target, devTargets, CRTargets, labels, 14, 10, Output,  deltaTimeInGraphSeconds)

fg.RSSILineGraphBetweenConfigurationsLenFq(target, devTargets, CRTargets, labels, 14, 10, Output,  deltaTimeInGraphSeconds)

fg.missingPointGraph(target,14,10,Output,deltaTimeInGraphSeconds)

fg.groupedBoxWhiskerPDRGraphs(target, labels, 14, 10, Output)



