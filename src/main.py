from AQICalculation import AQI_Aggregate,AQI
from ReadCSV import ReadDataAverageByDay,ReadDataAverageByHour

def main():
    filePath = '../DataAverageByHour/dataFairnet_averageByHour_KitID1037.csv'
    a = ReadDataAverageByHour(filePath)
    a.importPath()
    PM1_0       = a.PM1_0()
    PM2_5       = a.PM2_5()
    PM10        = a.PM10()
    Temperature = a.Temperature()
    Humidity    = a.Humidity()
    CO          = a.CO()
    b = AQI(PM2_5,PM10,CO)
    print(b.AQI_1h('CO'))

if __name__ == "__main__":
    main()