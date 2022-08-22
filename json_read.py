import json
import array
import requests
import pandas as pd


def loadAPI():
    jsonFile = open('FAirKit.json')

    dataJsonFile = json.load(jsonFile)

    kitID = []
    for d in dataJsonFile:
        kitID.append(d['KitID'])

    for i in kitID:
        acc_url_averageByHour = "http://api2.fairnet.vn/data/averageByHour?KitID=" + \
            str(i) + "&start=1546275600000&finish=1577811600000"
        # acc_url_averageByDay = "http://api2.fairnet.vn/data/averageByDay?KitID=" + \
        #     str(i) + "&start=1546275600000&finish=1577811600000"
        print(i)
        # fileNameAverageByDay = "2019/DataAverageByDay/dataFairnet_averageByDay_KitID" + str(i) + ".txt"
        fileNameAverageByHour = "2019/DataAverageByHour/dataFairnet_averageByHour_KitID" + str(i) + ".txt"

        # fileDataAverageByDay = open(fileNameAverageByDay,'w')
        fileDataAverageByHour = open(fileNameAverageByHour,'w')
        
        # fileDataAverageByDay.write(requests.get(acc_url_averageByDay).text)
        fileDataAverageByHour.write(requests.get(acc_url_averageByHour).text)

        # fileDataAverageByDay.close()
        fileDataAverageByHour.close()

        # print(dataJsonFile)

        # format json file write 
        # dataFormat = (json.dumps(dataJsonFile,indent = 4,sort_keys=True,ensure_ascii=False).encode('utf8')).decode()
        # with open("FAirKitFormat.json", "w") as outfile:
        #     outfile.write(dataFormat)
    jsonFile.close()

def formatTextToCSV():
    jsonFile = open('FAirKit.json')

    dataJsonFile = json.load(jsonFile)

    kitID = []
    for d in dataJsonFile:
        kitID.append(d['KitID'])

    for i in kitID:
        print('KitID: ',i)
        
        # DataAverageByDay
        # textFileNameDataAverageByDay = '2019/DataAverageByDay/dataFairnet_averageByDay_KitID' + str(i) +'.txt'
        # csvFileNameDataAverageByDay = '2019/DataAverageByDay/dataFairnet_averageByDay_KitID' + str(i) +'.csv'
        # DataAverageByHour
        textFileNameDataAverageByHour = '2019/DataAverageByHour/dataFairnet_averageByHour_KitID' + str(i) +'.txt'
        csvFileNameDataAverageByHour = '2019/DataAverageByHour/dataFairnet_averageByHour_KitID' + str(i) +'.csv'

        # csvFile = pd.read_csv(textFileNameDataAverageByDay,delimiter =',',engine='python')
        csvFile = pd.read_csv(textFileNameDataAverageByHour,delimiter =',',engine='python')

        # csvFile.columns['Time','PM1','PM2.5','PM10','Temperature','Humidity','CO']
        # csvFile.to_csv(csvFileNameDataAverageByDay,index=None)
        csvFile.to_csv(csvFileNameDataAverageByHour,index=None)

loadAPI()
formatTextToCSV()