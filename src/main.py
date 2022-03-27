from AQICalculation import AQI_Aggregate,AQI
from ReadCSV import ReadDataAverageByDay,ReadDataAverageByHour
import matplotlib.pyplot as plt
import numpy as np
import re
import json
import pandas as pd

def plot(self):
    plt.figure()
    plt.subplot(221)
    plt.plot(self.PM2_5_AQI,'r',marker = 'o')
    plt.title('PM2.5')

    plt.subplot(222)
    plt.plot(self.PM10_AQI, 'g',marker = '*' )
    plt.title('PM10')

    plt.subplot(223)
    plt.plot(self.CO_AQI, 'b',marker = '.' )
    plt.title('CO')

    plt.subplot(224)
    plt.plot(self.AQI_1h,'y',marker = '+')
    plt.title('AQI')
    plt.show()
    pass

def main():
    jsonFile = open('../FAirKit.json')

    dataJsonFile = json.load(jsonFile)

    kitID = []
    for d in dataJsonFile:
        kitID.append(d['KitID'])
    
    for i in kitID:
        # DataAverageByDay
        # textFileName = 'DataAverageByDay/dataFairnet_averageByDay_KitID' + str(i) +'.txt'
        # csvFileName = 'DataAverageByDay/dataFairnet_averageByDay_KitID' + str(i) +'.csv'

        # DataAverageByHour
        filePath = '../DataAverageByHour/dataFairnet_averageByHour_KitID' + str(i) +'.csv'
        saveFileName = '../out/dataFairnet_averageByHour_KitID' + str(i) +'.csv'

        AverageByHour = ReadDataAverageByHour(filePath)
        AverageByHour.importPath()

        PM1_0       = AverageByHour.PM1_0()
        PM2_5       = AverageByHour.PM2_5()
        PM10        = AverageByHour.PM10()
        Temperature = AverageByHour.Temperature()
        Humidity    = AverageByHour.Humidity()
        CO          = AverageByHour.CO()

        AQI_class   = AQI(PM2_5,PM10,CO)
        CO_AQI      = AQI_class.AQI_1h('CO')
        PM2_5_AQI   = AQI_class.AQI_1h('PM2_5')
        PM10_AQI    = AQI_class.AQI_1h('PM10')

        AQI_Aggregate_class = AQI_Aggregate(PM2_5_AQI,PM10_AQI,CO_AQI)
        AQI_1h = AQI_Aggregate_class.AQI_Aggregate_1h()
        
        yymmdd,time,timeZone = AverageByHour.Time()
        
        
    
    

if __name__ == "__main__":
    main()
    pass