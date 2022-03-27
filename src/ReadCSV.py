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
        PM1_0       = np.delete(PM1_0,      [185,184,183,182,181])  #delete row max min median mean stddev
        return PM1_0

    def PM2_5(self):
        PM2_5       = self.dataCSV['PM2.5']                         #read PM2.5 from file
        PM2_5       = PM2_5.to_numpy()                              #converted into numpy array
        PM2_5       = np.delete(PM2_5,      [185,184,183,182,181])  #delete row max min median mean stddev
        return PM2_5

    def PM10(self):
        PM10        = self.dataCSV['PM10']                          #read PM10 from file
        PM10        = PM10.to_numpy()                               #converted into numpy array
        PM10        = np.delete(PM10,       [185,184,183,182,181])  #delete row max min median mean stddev
        return PM10

    def Temperature(self):
        Temperature = self.dataCSV['Temperature']                   #read temperature from file
        Temperature = Temperature.to_numpy()                        #converted into numpy array
        Temperature = np.delete(Temperature,[185,184,183,182,181])  #delete row max min median mean stddev
        return Temperature

    def Humidity(self):
        Humidity    = self.dataCSV['Humidity']                      #read Humidity from file
        Humidity    = Humidity.to_numpy()                           #converted into numpy array
        Humidity    = np.delete(Humidity,   [185,184,183,182,181])  #delete row max min median mean stddev
        return Humidity

    def CO(self):
        CO          = self.dataCSV['CO']                            #read CO from file
        CO          = CO.to_numpy()                                 #converted into numpy array
        CO          = np.delete(CO,         [185,184,183,182,181])  #delete row max min median mean stddev
        return CO


class ReadDataAverageByHour:
    
    def __init__(self,filePath):
        self.filePath = filePath

    def importPath(self):
        self.dataCSV = pd.read_csv(self.filePath)

    def PM1_0(self):    
        PM1_0       = self.dataCSV['PM1.0']
        PM1_0       = PM1_0.to_numpy()
        PM1_0       = np.delete(PM1_0,      [4348,4347,4346,4345,4344])
        return PM1_0

    def PM2_5(self):
        PM2_5       = self.dataCSV['PM2.5']
        PM2_5       = PM2_5.to_numpy()
        PM2_5       = np.delete(PM2_5,      [4348,4347,4346,4345,4344])
        return PM2_5

    def PM10(self):
        PM10        = self.dataCSV['PM10']
        PM10        = PM10.to_numpy()
        PM10        = np.delete(PM10,       [4348,4347,4346,4345,4344])
        return PM10

    def Temperature(self):
        Temperature = self.dataCSV['Temperature']
        Temperature = Temperature.to_numpy()
        Temperature = np.delete(Temperature,[4348,4347,4346,4345,4344])
        return Temperature

    def Humidity(self):
        Humidity    = self.dataCSV['Humidity']
        Humidity    = Humidity.to_numpy()
        Humidity    = np.delete(Humidity,   [4348,4347,4346,4345,4344])
        return Humidity

    def CO(self):
        CO          = self.dataCSV['CO']
        CO          = CO.to_numpy()
        CO          = np.delete(CO,         [4348,4347,4346,4345,4344])
        return CO
    
    def Time(self):
        timeString          = self.dataCSV['Unnamed: 0']
        timeString          = timeString.to_numpy()
        timeString          = np.delete(timeString,         [4348,4347,4346,4345,4344])
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

