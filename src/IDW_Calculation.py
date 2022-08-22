from interpolateIDW import InterpolateByZone, InterpolateByZoneHN, InterpolateByZoneNew
import pandas as pd
import numpy as np
import csv
import sys
sys.path.insert(1, '../test')
def MixData():
    infomationKit = pd.read_csv('../out/locationFairKit.csv')
    kitID = infomationKit['Kit ID']
    pathFileNameRead1 = '../out/data/DataAverageByDay/AQI_averageByDay_KitID1037.csv'
    data1 = pd.read_csv(pathFileNameRead1)
    df1 = pd.DataFrame(data1['yymmdd'])
    df1.to_csv('../out/yymmdd.csv',header='yymmdd',index=False)
    for yymmdd in data1['yymmdd']:
        pathFileNameSave = '../out/data/DataIDW/' + str(yymmdd) + '.csv'

        headerList=['Kit ID','Latitude','Longtitude','AQI 24h']
        with open(pathFileNameSave, 'w') as file:
            dw = csv.DictWriter(file, delimiter=',',fieldnames=headerList)
            dw.writeheader()
    indexID = 0
    for ID in kitID:
        pathFileNameRead = '../out/data/DataAverageByDay/AQI_averageByDay_KitID' + str(ID) + '.csv'
        data = pd.read_csv(pathFileNameRead)
        index = 0
        for yymmdd in data['yymmdd']:
            pathFileNameSave = '../out/data/DataIDW/' + str(yymmdd) + '.csv'

            AQI_24h = data['AQI 24h'][index]
            dataAppend =   {'Kit ID': [ID],
                            'Latitude:':[infomationKit['Latitude'][indexID]],
                            'Longtitude:':[infomationKit['Longitude'][indexID]],
                            'AQI 24h':[AQI_24h]}
            # preprocessing nan value when station is idle
            if np.isnan(AQI_24h):
                pass
            else:
                df = pd.DataFrame(dataAppend)
                df.to_csv(pathFileNameSave,mode='a',index=False,header=False)
            index += 1
        indexID += 1


def main():
    datayymmdd = pd.read_csv('../out/yymmdd.csv')
    infomationKit = pd.read_csv('../out/locationFairKit.csv')
    kitID = infomationKit['Kit ID']
    n = 500
    for yymmdd in datayymmdd['yymmdd']:
        if yymmdd >= '2021-01-01':
            pathFileRead = '../out/data/DataIDW/' + str(yymmdd) + '.csv'
            data = pd.read_csv(pathFileRead)
            if len(data['Kit ID']) > 1:
                print(len(data['Kit ID']))
                InterpolateByZone(pathFileRead, yymmdd)
            else:
                continue
        else:
            continue
        # print('end test ', yymmdd)
        # if len(data) < 9:
        #     print('Khong du data kit de noi suy: ',yymmdd)
        #     continue
        # else:
        #     x = data['Longtitude'].to_numpy()
        #     y = data['Latitude'].to_numpy()
        #     z = data['AQI 24h'].to_numpy()
        #     gridIDW 		= interpolate.scipy_idw(x, y, z, n)
        #     interpolate.plot(x, y, z, gridIDW, 'IDW '+str(yymmdd), save = True)
        

if __name__ == "__main__":
    main()
