import pandas as pd
from scipy.interpolate import interp1d

NACELLE_NUMBERS = 3

global linearInterpolators
linearInterpolators = [None for _ in range(NACELLE_NUMBERS)]
global positions
positions = [None for _ in range(NACELLE_NUMBERS)]

def loadFile(filepath:str):
    dataFrame = pd.read_csv(filepath,sep=';',decimal='.')
    # convert the datetime column to a pandas datetime object
    dataFrame['Date_Time'] = pd.to_datetime(dataFrame['date'])
    # convert the datetime column to an integer
    dataFrame['timestamp'] = dataFrame['Date_Time'].astype(int)
    # divide the resulting integer by the number of nanoseconds in milli second
    dataFrame['timestamp'] = dataFrame['timestamp'] // 10**6
    return dataFrame

def getLinearInterpolators(nacelleId):
    global linearInterpolators
    global positions
    if linearInterpolators[nacelleId] == None:
        # Load the dataFrame
        filepath = f"../dataset/raw_irma_logs/irma_ncu{nacelleId+1}.csv"
        dataFrame = loadFile(filepath)
        timestamp = dataFrame["timestamp"].to_list()
        alt = dataFrame["altitude"].to_list()
        lat = dataFrame["latitude"].to_list()
        lon = dataFrame["longitude"].to_list()

        linearInterpolators[nacelleId] = [
            interp1d(timestamp,lat,fill_value="extrapolate"),
            interp1d(timestamp,lon,fill_value="extrapolate"),
            interp1d(timestamp,alt,fill_value="extrapolate")
        ]
        # Also load the positions
        positions[nacelleId] = [timestamp,lat,lon,alt]
    return linearInterpolators[nacelleId]

def isStart(timesamp, nacelleId):
    deltaT = 60000
    linearInterpolators = getLinearInterpolators(nacelleId)
    deltaAlt = linearInterpolators[0](timesamp + deltaT) - linearInterpolators[0](timesamp)
    return True if deltaAlt >= 0 else False



def getAltitude(timestamp,nacelleId):
    lerp = getLinearInterpolators(nacelleId)
    altitude = lerp[2](timestamp)

    # Clamp the altitude at 0
    return altitude if altitude > 0 else 0

def getLatitude(timestamp,nacelleId):
    lerp = getLinearInterpolators(nacelleId)
    global positions

    altitude = getAltitude(timestamp,nacelleId)
    if altitude <= 0:
        # If we are on the ground, return the start or end latitude
        if isStart(timestamp,nacelleId):
            return positions[nacelleId][1][0]
        else:
            return positions[nacelleId][1][-1]
    return lerp[0](timestamp)

def getLongitude(timestamp,nacelleId):
    lerp = getLinearInterpolators(nacelleId)
    global positions

    altitude = getAltitude(timestamp,nacelleId)
    if altitude <= 0:
        # If we are on the ground, return the start or end latitude
        if isStart(timestamp,nacelleId):
            return positions[nacelleId][2][0]
        else:
            return positions[nacelleId][2][-1]
        
    return lerp[1](timestamp)
