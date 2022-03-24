import pandas as pd
import array
import numpy as np

dataCSV = pd.read_csv('../DataAverageByHour/dataFairnet_averageByHour_KitID1037.csv')

PM1_0       = dataCSV['PM1.0']
PM2_5       = dataCSV['PM2.5']
PM10        = dataCSV['PM10']
Temperature = dataCSV['Temperature']
Humidity    = dataCSV['Humidity']
CO          = dataCSV['CO']

PM1_0       = PM1_0.to_numpy()
PM2_5       = PM2_5.to_numpy()
PM10        = PM10.to_numpy()
Temperature = Temperature.to_numpy()
Humidity    = Humidity.to_numpy()
CO          = CO.to_numpy()

PM1_0       = np.delete(PM1_0,      [4348,4347,4346,4345,4344])
PM2_5       = np.delete(PM2_5,      [4348,4347,4346,4345,4344])
PM10        = np.delete(PM10,       [4348,4347,4346,4345,4344])
Temperature = np.delete(Temperature,[4348,4347,4346,4345,4344])
Humidity    = np.delete(Humidity,   [4348,4347,4346,4345,4344])
CO          = np.delete(CO,         [4348,4347,4346,4345,4344])

class NowCast:
    def Nowcast(argument):
        index = 11
        arrayNowcast = np.array([])
        while index < len(argument):
            
            MonitoringValues = np.array([])
            for i in range(1,13):
                MonitoringValues = np.append(MonitoringValues,argument[index-i+1])
            # print(MonitoringValues,"    ")
            if  (np.isnan(MonitoringValues[0]) and np.isnan(MonitoringValues[1])) or\
                (np.isnan(MonitoringValues[0]) and np.isnan(MonitoringValues[2])) or \
                (np.isnan(MonitoringValues[1]) and np.isnan(MonitoringValues[2])) or \
                (np.isnan(MonitoringValues[0]) and np.isnan(MonitoringValues[1]) and np.isnan(MonitoringValues[3])):
                index += 1
            else:
                W = np.nanmin(MonitoringValues)/np.nanmax(MonitoringValues)
                # print("max: ",np.nanmax(MonitoringValues)," min: ",np.nanmin(MonitoringValues)," W: ",W)
                if W <= 0.5:
                    w = 0.5
                    nowcast1 = 0
                    # print("nowcast element: ",end='')
                    for i in range (1,13):
                        if np.isnan(MonitoringValues[i-1]):
                            MonitoringValues[i-1] = 0
                            
                        nowcast1 = pow(0.5,i)*MonitoringValues[i-1] + nowcast1
                        # print(pow(0.5,i)*MonitoringValues[i-1],end=' ')
                    arrayNowcast = np.append(arrayNowcast,nowcast1)
                    # print(nowcast1,end="    ")
                else:
                    w = W
                    S1 = 0
                    S2 = 0
                    for i in range(1,13):
                        if np.isnan(MonitoringValues[i-1]):
                            MonitoringValues[i-1] = 0
                        S1 = S1 + pow(w,i)*MonitoringValues[i-1]
                        S2 = S2 + pow(w,i)
                    nowcast2 = S1/S2
                    # print(nowcast2)
                    arrayNowcast = np.append(arrayNowcast,nowcast2)
                index += 1
            
        return arrayNowcast
                    
class BPiTable:
    def Table(nameTable,num):
        I_Parameter     = np.array([0,50,100,150,200,300,400,500])
        O3_1h_Parameter = np.array([0,100,120,170,210,400])
        O3_8h_Parameter = np.array([0,100,120,170,210,400])
        CO_Parameter    = np.array([0,160,200,300,400,800,1000,1200])
        SO2_Parameter   = np.array([0,125,350,550,800,1600,2100,2630])
        NO2_Parameter   = np.array([0,100,200,700,1200,2350,3100,3850])
        PM10_Parameter  = np.array([0,50,150,250,350,420,500,600])
        PM2_5_Parameter = np.array([0,25,50,80,150,250,350,500])
        parameter       = np.array([])
        if nameTable == 'O3_1h':
            parameter = O3_1h_Parameter
        elif nameTable == 'O3_8h':
            parameter = O3_8h_Parameter
        elif nameTable == 'CO':
            parameter = CO_Parameter
        elif nameTable == 'SO2':
            parameter = SO2_Parameter
        elif nameTable == 'NO2':
            parameter = NO2_Parameter
        elif nameTable == 'PM10':
            parameter = PM10_Parameter
        elif nameTable == 'PM2.5':
            parameter = PM2_5_Parameter
        # match nameTable:
        #     case 'O3_1h':
        #         parameter = O3_1h_Parameter
        #     case 'O3_8h':
        #         parameter = O3_8h_Parameter
        #     case 'CO':
        #         parameter = CO_Parameter
        #     case 'SO2':
        #         parameter = SO2_Parameter
        #     case 'NO2':
        #         parameter = NO2_Parameter
        #     case 'PM10':
        #         parameter = PM10_Parameter
        #     case 'PM2.5':
        #         parameter = PM2_5_Parameter
        # print(parameter)
        a   = None
        a_1 = None
        b   = None
        b_1 = None
        for i in range(0,len(parameter)-1):
            if num >= parameter[i]:
                a   = parameter[i]
                a_1 = parameter[i+1]
                b   = I_Parameter[i]
                b_1 = I_Parameter[i+1]
        return b,b_1,a,a_1

class AQI:  
    def AQIhOxygenElement(I,I_1,BP,BP_1,oxygen):
        AQI = ((I_1-I)/(BP_1-BP))*(oxygen-BP)+I
        return AQI
    def AQI_PM_Element(I,I_1,BP,BP_1,nowcast):
        AQI = ((I_1-I)/(BP_1-BP))*(nowcast-BP)+I
        return AQI
    
    def AQI(nameParameter):
        resultArray = np.array([])
        nowcastArray = np.array([])
        I = 0
        I_1 = 0
        BP = 0
        BP_1 = 0
        result = 0
        if nameParameter[0] == 'P' and nameParameter[1] == 'M':
            if nameParameter[2] == '1' and nameParameter[3] == '0':
                nowcastArray = NowCast.Nowcast(PM10)
                # print(len(PM10),'   ',len(nowcastArray))
                for i in range(11,len(PM10)):
                    # print('PM10[',i,']: ',PM10[i],end=' ')
                    if np.isnan(PM10[i]):
                        result = None
                    else:
                        I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=PM10[i])
                        # result = AQI.AQI_PM_Element(I,I_1,BP,BP_1,nowcast=nowcastArray[i-11])
                        result = 0
                    # print(I,I_1,BP,BP_1)
                    resultArray = np.append(resultArray,result)
            else:
                nowcastArray = NowCast.Nowcast(PM2_5)
                for i in range(11,len(PM2_5)):
                    I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=PM2_5[i])
                    # print(I,I_1,BP,BP_1)
                    # result = AQI.AQI_PM_Element(I,I_1,BP,BP_1,nowcast=nowcastArray[i-11])
                    resultArray = np.append(resultArray,result)
        else:
            for i in range(0,len(CO)):
                I,I_1,BP,BP_1 = BPiTable.Table(nameTable=nameParameter,num=CO[i])
                # print(I,I_1,BP,BP_1)
                # result = AQI.AQIhOxygenElement(I,I_1,BP,BP_1,CO[i])
                resultArray = np.append(resultArray,result)
        
        return resultArray

# num = int(input('inout: '))
# a,b,c,d = BPiTable.Table('PM2.5',num)
# print(a)
# print(b)
# print(c)
# print(d)

# test = AQI.AQI('PM10')
# with np.printoptions(threshold=np.inf):
#     print(test)

test = NowCast.Nowcast(PM1_0)
with np.printoptions(threshold=np.inf):
    print(test)
print('nowcast: ',len(test),'   ',len(PM1_0))
# def AverageByHour():
    