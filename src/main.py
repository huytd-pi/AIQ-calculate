from AQICalculation import AQI_Aggregate
from ReadCSV import ReadDataAverageByDay,ReadDataAverageByHour

def main():
    filePath = '../DataAverageByHour/dataFairnet_averageByHour_KitID1037.csv'
    a = ReadDataAverageByHour(filePath)
    a.importPath()
    print(AQI_Aggregate.AQI_Aggregate_1h())

if __name__ == "__main__":
    main()