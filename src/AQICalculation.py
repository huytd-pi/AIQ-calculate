import numpy as np
from ReadCSV import ReadDataAverageByHour,ReadDataAverageByDay
from CalculateNowcast import NowCast
from Table import BPiTable

# ReadDataAverageByHour.importPath('../DataAverageByHour/dataFairnet_averageByHour_KitID1037.csv')
PM1_0       = ReadDataAverageByHour().PM1_0()
PM2_5       = ReadDataAverageByHour().PM2_5()
PM10        = ReadDataAverageByHour().PM10()
Temperature = ReadDataAverageByHour().Temperature()
Humidity    = ReadDataAverageByHour().Humidity()
CO          = ReadDataAverageByHour().CO()


class AQI:  
    def AQIhOxygenElement(I,I_1,BP,BP_1,oxygen):
        AQI = ((I_1-I)/(BP_1-BP))*(oxygen-BP)+I
        return AQI
    def AQI_PM_Element(I,I_1,BP,BP_1,nowcast):
        AQI = ((I_1-I)/(BP_1-BP))*(nowcast-BP)+I
        return AQI

    def AQI_1h(nameParameter):
        resultArray = np.array([])
        nowcastArray = np.array([])
        I = None
        I_1 = None
        BP = None
        BP_1 = None
        result = None
        if nameParameter == 'PM2_5':
            nowcastArray = NowCast.Nowcast(PM2_5)
            for i in range(11,len(PM2_5)):
                if np.isnan(PM2_5[i]) or np.isnan(nowcastArray[i-11]):
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=PM2_5[i])
                    # print(I,I_1,BP,BP_1)
                    result = AQI.AQI_PM_Element(I,I_1,BP,BP_1,nowcast=nowcastArray[i-11])
                    resultArray = np.append(resultArray,result)
        elif nameParameter == 'PM10':
            nowcastArray = NowCast.Nowcast(PM10)
            for i in range(11,len(PM10)):
                if np.isnan(PM10[i]) or np.isnan(nowcastArray[i-11]):
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=PM10[i])
                    # print(I,I_1,BP,BP_1)
                    result = AQI.AQI_PM_Element(I,I_1,BP,BP_1,nowcast=nowcastArray[i-11])
                    resultArray = np.append(resultArray,result)
        elif nameParameter == 'CO':
            for i in range(11,len(CO)):
                if np.isnan(CO[i]):
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=CO[i])
                    # print(I,I_1,BP,BP_1)
                    result = AQI.AQIhOxygenElement(I,I_1,BP,BP_1,CO[i])
                    resultArray = np.append(resultArray,result)
        return resultArray
    
    def PM_24h_Average(PM):
        averageArray    = np.array([])
        tempArray       = np.array([])
        tempArray       = PM
        for i in range(0,len(tempArray)-24,24):
            meanValue = np.mean(tempArray[i:i+24])
            averageArray = np.append(averageArray,meanValue)
        return averageArray

    def Oxygen_24h_Max(oxygen):
        maxArray       = np.array([])
        tempArray       = np.array([])
        tempArray       = oxygen
        for i in range(0,len(tempArray)-24,24):
            maxValue = np.max(tempArray[i:i+24])
            maxArray = np.append(maxArray,maxValue)
        return maxArray

    def AQI_24h(nameParameter):
        resultArray = np.array([])
        tempArray       = np.array([])
        if nameParameter == 'PM2_5':
            tempArray = AQI.PM_24h_Average(PM2_5)
            for i in range(0,len(tempArray)):
                if np.isnan(tempArray[i]):
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=tempArray[i])
                    # print(I,I_1,BP,BP_1)
                    result = AQI.AQIhOxygenElement(I,I_1,BP,BP_1,tempArray[i])
                    resultArray = np.append(resultArray,result)

        elif nameParameter == 'PM10':
            tempArray = AQI.PM_24h_Average(PM10)
            for i in range(0,len(tempArray)):
                if np.isnan(tempArray[i]):
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=tempArray[i])
                    # print(I,I_1,BP,BP_1)
                    result = AQI.AQIhOxygenElement(I,I_1,BP,BP_1,tempArray[i])
                    resultArray = np.append(resultArray,result)

        elif nameParameter == 'CO':
            tempArray = AQI.Oxygen_24h_Max(CO)
            for i in range(0,len(tempArray)):
                if np.isnan(tempArray[i]):
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=tempArray[i])
                    result = AQI.AQIhOxygenElement(I,I_1,BP,BP_1,tempArray[i])
                    resultArray = np.append(resultArray,result)
        return resultArray

class AQI_Aggregate:
    def AQI_Aggregate_1h():
        resultArray = np.array([])
        tempCO = AQI.AQI_1h('CO')
        tempPM2_5 = AQI.AQI_1h('PM2_5')
        tempPM10 = AQI.AQI_1h('PM10')
        for i in range(0,len(tempCO)):
            if np.isnan(tempCO[i]) and np.isnan(tempPM10[i]) and np.isnan(tempPM2_5[i]):
                result = np.nan
            else:
                result = np.nanmax([tempCO[i],tempPM2_5[i],tempPM10[i]])
            resultArray = np.append(resultArray,result)
        return resultArray

    def AQI_Aggregate_24h():
        resultArray = np.array([])
        tempCO = AQI.AQI_24h('CO')
        tempPM2_5 = AQI.AQI_24h('PM2_5')
        tempPM10 = AQI.AQI_24h('PM10')
        for i in range(0,len(tempCO)):
            if np.isnan(tempCO[i]) and np.isnan(tempPM10[i]) and np.isnan(tempPM2_5[i]):
                result = np.nan
            else:
                result = np.nanmax([tempCO[i],tempPM2_5[i],tempPM10[i]])
            resultArray = np.append(resultArray,result)
        return resultArray






# print(AQI_Aggregate.AQI_Aggregate_24h())


# test = AQI.AQI_24h('CO')
# with np.printoptions(threshold=np.inf):
#     print(test)
#     print(len(test))


# test = NowCast.Nowcast(PM1_0)
# with np.printoptions(threshold=np.inf):
#     print(test)
# print('nowcast: ',len(test),'   ',len(PM1_0))
# def AverageByHour():
    