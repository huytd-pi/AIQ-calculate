import pandas as pd
import numpy as np


class ReadDataAverageByDay():
    def __init__(self):
        self.dataCSV = pd.read_csv('../DataAverageByHour/dataFairnet_averageByDay_KitID1037.csv')
    
    def PM1_0(self):    
        PM1_0       = self.dataCSV['PM1.0']
        PM1_0       = PM1_0.to_numpy()
        PM1_0       = np.delete(PM1_0,      [185,184,183,182,181])
        return PM1_0

    def PM2_5(self):
        PM2_5       = self.dataCSV['PM2.5']
        PM2_5       = PM2_5.to_numpy()
        PM2_5       = np.delete(PM2_5,      [185,184,183,182,181])
        return PM2_5

    def PM10(self):
        PM10        = self.dataCSV['PM10']
        PM10        = PM10.to_numpy()
        PM10        = np.delete(PM10,       [185,184,183,182,181])
        return PM10

    def Temperature(self):
        Temperature = self.dataCSV['Temperature']
        Temperature = Temperature.to_numpy()
        Temperature = np.delete(Temperature,[185,184,183,182,181])
        return Temperature

    def Humidity(self):
        Humidity    = self.dataCSV['Humidity']
        Humidity    = Humidity.to_numpy()
        Humidity    = np.delete(Humidity,   [185,184,183,182,181])
        return Humidity

    def CO(self):
        CO          = self.dataCSV['CO']
        CO          = CO.to_numpy()
        CO          = np.delete(CO,         [185,184,183,182,181])
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

