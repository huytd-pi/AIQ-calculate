import numpy as np

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
                arrayNowcast = np.append(arrayNowcast,np.nan)
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