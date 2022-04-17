import pandas as pd
import numpy as np
import re


class ReadDataAverageByDay():
    def __init__(self,filePath):
        self.filePath = filePath

    def importPath(self):
        self.dataCSV = pd.read_csv(self.filePath)
    
    def PM1_0(self):    
        PM1_0       = self.dataCSV['PM1.0']                         #read PM1.0 from file
        PM1_0       = PM1_0.to_numpy()                              #converted into numpy array
        PM1_0       = np.delete(PM1_0,      [len(PM1_0)-1,len(PM1_0)-2,len(PM1_0)-3,len(PM1_0)-4,len(PM1_0)-5])  #delete row max min median mean stddev
        return PM1_0

    def PM2_5(self):
        PM2_5       = self.dataCSV['PM2.5']                         #read PM2.5 from file
        PM2_5       = PM2_5.to_numpy()                              #converted into numpy array
        PM2_5       = np.delete(PM2_5,      [len(PM2_5)-1,len(PM2_5)-2,len(PM2_5)-3,len(PM2_5)-4,len(PM2_5)-5]) #delete row max min median mean stddev
        return PM2_5

    def PM10(self):
        PM10        = self.dataCSV['PM10']                          #read PM10 from file
        PM10        = PM10.to_numpy()                               #converted into numpy array
        PM10        = np.delete(PM10,       [len(PM10)-1,len(PM10)-2,len(PM10)-3,len(PM10)-4,len(PM10)-5])  #delete row max min median mean stddev
        return PM10

    def Temperature(self):
        Temperature = self.dataCSV['Temperature']                   #read temperature from file
        Temperature = Temperature.to_numpy()                        #converted into numpy array
        Temperature = np.delete(Temperature,[len(Temperature)-1,len(Temperature)-2,len(Temperature)-3,len(Temperature)-4,len(Temperature)-5])  #delete row max min median mean stddev
        return Temperature

    def Humidity(self):
        Humidity    = self.dataCSV['Humidity']                      #read Humidity from file
        Humidity    = Humidity.to_numpy()                           #converted into numpy array
        Humidity    = np.delete(Humidity,   [len(Humidity)-1,len(Humidity)-2,len(Humidity)-3,len(Humidity)-4,len(Humidity)-5]) #delete row max min median mean stddev
        return Humidity

    def CO(self):
        CO          = self.dataCSV['CO']                            #read CO from file
        CO          = CO.to_numpy()                                 #converted into numpy array
        CO          = np.delete(CO,         [len(CO)-1,len(CO)-2,len(CO)-3,len(CO)-4,len(CO)-5]) #delete row max min median mean stddev
        return CO
    def Time(self):
        timeString          = self.dataCSV['Unnamed: 0']
        timeString          = timeString.to_numpy()
        timeString          = np.delete(timeString,         [len(timeString)-1,len(timeString)-2,len(timeString)-3,len(timeString)-4,len(timeString)-5])
        yymmdd = np.array([])
        time = np.array([])
        timeZone = np.array([])
        for i in range(0,len(timeString)):
            temp = re.split('[  +]',timeString[i])
            yymmdd = np.append(yymmdd,temp[0])
            time = np.append(time,temp[1])
            timeZone = np.append(timeZone,temp[2])
        return yymmdd,time,timeZone


class ReadDataAverageByHour:
    
    def __init__(self,filePath):
        self.filePath = filePath

    def importPath(self):
        self.dataCSV = pd.read_csv(self.filePath)

    def PM1_0(self):    
        PM1_0       = self.dataCSV['PM1.0']
        PM1_0       = PM1_0.to_numpy()
        PM1_0       = np.delete(PM1_0,      [len(PM1_0)-1,len(PM1_0)-2,len(PM1_0)-3,len(PM1_0)-4,len(PM1_0)-5])
        return PM1_0

    def PM2_5(self):
        PM2_5       = self.dataCSV['PM2.5']
        PM2_5       = PM2_5.to_numpy()
        PM2_5       = np.delete(PM2_5,      [len(PM2_5)-1,len(PM2_5)-2,len(PM2_5)-3,len(PM2_5)-4,len(PM2_5)-5])
        return PM2_5

    def PM10(self):
        PM10        = self.dataCSV['PM10']
        PM10        = PM10.to_numpy()
        PM10        = np.delete(PM10,       [len(PM10)-1,len(PM10)-2,len(PM10)-3,len(PM10)-4,len(PM10)-5])
        return PM10

    def Temperature(self):
        Temperature = self.dataCSV['Temperature']
        Temperature = Temperature.to_numpy()
        Temperature = np.delete(Temperature,[len(Temperature)-1,len(Temperature)-2,len(Temperature)-3,len(Temperature)-4,len(Temperature)-5])
        return Temperature

    def Humidity(self):
        Humidity    = self.dataCSV['Humidity']
        Humidity    = Humidity.to_numpy()
        Humidity    = np.delete(Humidity,   [len(Humidity)-1,len(Humidity)-2,len(Humidity)-3,len(Humidity)-4,len(Humidity)-5])
        return Humidity

    def CO(self):
        CO          = self.dataCSV['CO']
        CO          = CO.to_numpy()
        CO          = np.delete(CO,         [len(CO)-1,len(CO)-2,len(CO)-3,len(CO)-4,len(CO)-5])
        return CO
    
    def Time(self):
        timeString          = self.dataCSV['Unnamed: 0']
        timeString          = timeString.to_numpy()
        timeString          = np.delete(timeString,         [len(timeString)-1,len(timeString)-2,len(timeString)-3,len(timeString)-4,len(timeString)-5])
        timeString          = np.delete(timeString,range(0,11,1))
        yymmdd = np.array([])
        time = np.array([])
        timeZone = np.array([])
        for i in range(0,len(timeString)):
            temp = re.split('[  +]',timeString[i])
            yymmdd = np.append(yymmdd,temp[0])
            time = np.append(time,temp[1])
            timeZone = np.append(timeZone,temp[2])
        return yymmdd,time,timeZone

