import numpy as np
from ReadCSV import ReadDataAverageByHour,ReadDataAverageByDay
from CalculateNowcast import NowCast
from Table import BPiTable


class AQI:  
    def __init__(self,PM2_5,PM10,CO):
        self.PM2_5 = PM2_5
        self.PM10 = PM10
        self.CO = CO

    def AQIhOxygenElement(I,I_1,BP,BP_1,oxygen):        #formula for calculating AQI of oxygen
        AQI = ((I_1-I)/(BP_1-BP))*(oxygen-BP)+I
        return AQI
    def AQI_PM_Element(I,I_1,BP,BP_1,nowcast):          #formula for calculating AQI of nowcast
        AQI = ((I_1-I)/(BP_1-BP))*(nowcast-BP)+I
        return AQI

    def AQI_1h(self,nameParameter):
        resultArray = np.array([])
        nowcastArray = np.array([])
        I = None    #The AQI value at i given in the table corresponds to the BPi value.
        I_1 = None  #The AQI value at i+1 given in the table corresponds to the value BPi+1
        BP = None   #The lower limit concentration of the observed parameter value specified in Table 2 corresponds to the level i
        BP_1 = None #The upper limit concentration of the observed parameter value specified in Table 2 corresponds to the level i+1
        result = None
        if nameParameter == 'PM2_5':
            nowcastArray = NowCast.Nowcast(self.PM2_5)  #calculate nowcast
            for i in range(11,len(self.PM2_5)):         #from the 11th value
                if np.isnan(self.PM2_5[i]) or np.isnan(nowcastArray[i-11]):
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=self.PM2_5[i])
                    # print(I,I_1,BP,BP_1)
                    result = AQI.AQI_PM_Element(I,I_1,BP,BP_1,nowcast=nowcastArray[i-11])
                    resultArray = np.append(resultArray,result)
        elif nameParameter == 'PM10':                   
            nowcastArray = NowCast.Nowcast(self.PM10)   #calculate nowcast
            for i in range(11,len(self.PM10)):          #from the 11th value
                if np.isnan(self.PM10[i]) or np.isnan(nowcastArray[i-11]):
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=self.PM10[i])
                    # print(I,I_1,BP,BP_1)
                    result = AQI.AQI_PM_Element(I,I_1,BP,BP_1,nowcast=nowcastArray[i-11])
                    resultArray = np.append(resultArray,result)
        elif nameParameter == 'CO':                     #calculate nowcast
            for i in range(11,len(self.CO)):            #from the 11th value
                if np.isnan(self.CO[i]) or self.CO[i] >= 150000:
                    result = np.nan
                    resultArray = np.append(resultArray,result)
                else:
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=self.CO[i])
                    # print(I,I_1,BP,BP_1)
                    result = AQI.AQIhOxygenElement(I,I_1,BP,BP_1,self.CO[i])
                    resultArray = np.append(resultArray,result)
                # print('CO: ',self.CO[i],'--->AQI: ',result)
        return resultArray      #array of 1h average AQI results.
    
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

    def AQI_24h(self,nameParameter):
        resultArray = np.array([])
        tempArray       = np.array([])
        if nameParameter == 'PM2_5':
            tempArray = AQI.PM_24h_Average(self.PM2_5)
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
            tempArray = AQI.PM_24h_Average(self.PM10)
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
            tempArray = AQI.Oxygen_24h_Max(self.CO)
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
    def __init__(self,PM2_5_AQI,PM10_AQI,CO_AQI):
        self.PM2_5_AQI = PM2_5_AQI
        self.PM10_AQI = PM10_AQI
        self.CO_AQI = CO_AQI

    def AQI_Aggregate_1h(self):
        resultArray = np.array([])
        for i in range(0,len(self.CO_AQI)):
            if np.isnan(self.CO_AQI[i]) and np.isnan(self.PM10_AQI[i]) and np.isnan(self.PM2_5_AQI[i]):
                result = np.nan
            else:
                result = np.nanmax([self.CO_AQI[i],self.PM2_5_AQI[i],self.PM10_AQI[i]])
                resultArray = np.append(resultArray,result)
        return resultArray

    def AQI_Aggregate_24h(self):
        resultArray = np.array([])
        for i in range(0,len(self.CO_AQI)):
            if np.isnan(self.CO_AQI[i]) and np.isnan(self.PM10_AQI[i]) and np.isnan(self.PM2_5_AQI[i]):
                result = np.nan
            else:
                result = np.nanmax([self.CO_AQI[i],self.PM2_5_AQI[i],self.PM10_AQI[i]])
            resultArray = np.append(resultArray,result)
        return resultArray
