from interpolateKriging import InterpolateByZoneHN,InterpolateByZone
import pandas as pd
import numpy as np


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
