from ReadCSV import ReadDataAverageByDay,ReadDataAverageByHour
import pandas as pd
from AQICalculation import AQI_Aggregate,AQI

class AQIExportCSV:
    def __init__(self,filePath):
        self.dataKitID = pd.read_csv(filePath)

    def averageByHour(self):
        kitID = self.dataKitID['Kit ID']
        for index in kitID:
            filePath = '../DataAverageByHour/dataFairnet_averageByHour_KitID' + str(index) +'.csv'
            saveFileName = '../out/data/DataAverageByHour/AQI_averageByHour_KitID' + str(index) +'.csv'
            AverageByHour = ReadDataAverageByHour(filePath)
            AverageByHour.importPath()

            PM2_5       = AverageByHour.PM2_5()
            PM10        = AverageByHour.PM10()
            CO          = AverageByHour.CO()
            yymmdd,time,timeZone = AverageByHour.Time()

            AQI_class   = AQI(PM2_5,PM10,CO)
            CO_AQI      = AQI_class.AQI_1h('CO')
            PM2_5_AQI   = AQI_class.AQI_1h('PM2_5')
            PM10_AQI    = AQI_class.AQI_1h('PM10')

            AQI_Aggregate_class = AQI_Aggregate(PM2_5_AQI,PM10_AQI,CO_AQI)
            AQI_1h = AQI_Aggregate_class.AQI_Aggregate_1h()

            dict = {'yymmdd': yymmdd,'time':time,'time zone':timeZone,'AQI 1h':AQI_1h}
            df = pd.DataFrame(dict)
            df.to_csv(saveFileName,encoding='utf-8')
        
    def averageByDay(self):
        kitID = self.dataKitID['Kit ID']
        for index in kitID:
            filePath = '../DataAverageByHour/dataFairnet_averageByHour_KitID' + str(index) +'.csv'
            filePath1 = '../DataAverageByDay/dataFairnet_averageByDay_KitID' + str(index) +'.csv'
            saveFileName = '../out/data/DataAverageByDay/AQI_averageByDay_KitID' + str(index) +'.csv'
            AverageByDay = ReadDataAverageByHour(filePath)
            AverageByDay.importPath()
            TimeDay = ReadDataAverageByDay(filePath1)
            TimeDay.importPath()

            PM2_5       = AverageByDay.PM2_5()
            PM10        = AverageByDay.PM10()
            CO          = AverageByDay.CO()
            yymmdd,time,timeZone = TimeDay.Time()

            AQI_class   = AQI(PM2_5,PM10,CO)
            CO_AQI      = AQI_class.AQI_24h('CO')
            PM2_5_AQI   = AQI_class.AQI_24h('PM2_5')
            PM10_AQI    = AQI_class.AQI_24h('PM10')

            AQI_Aggregate_class = AQI_Aggregate(PM2_5_AQI,PM10_AQI,CO_AQI)
            AQI_24h = AQI_Aggregate_class.AQI_Aggregate_24h()

            dict = {'yymmdd': yymmdd,'time':time,'time zone':timeZone,'AQI 24h':AQI_24h}
            df = pd.DataFrame(dict)
            df.to_csv(saveFileName,encoding='utf-8')
        
        