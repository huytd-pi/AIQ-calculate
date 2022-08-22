import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def plotAQI24h():
    infoKit = pd.read_csv('../out/locationFairKit.csv')
    kitID = infoKit['Kit ID']
    fig, axs = plt.subplots(figsize=(15, 7))
    plt.title('Average AQI value for the day')
    axs.set(xlabel='Data', ylabel='AQI')
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
    plt.gcf().autofmt_xdate()

    # i = 1037
    # pathDataAQI = '../out/data/DataAverageByDay/AQI_averageByDay_KitID' + str(i) + '.csv'
    # dataAQI = pd.read_csv(pathDataAQI)
    # AQI_24h = dataAQI['AQI 24h']
    # time = dataAQI['yymmdd']
    
    # axs.plot(time, AQI_24h, label=str(i))
    
    for i in kitID:
        pathDataAQI = '../out/data/DataAverageByDay/AQI_averageByDay_KitID' + str(i) + '.csv'
        dataAQI = pd.read_csv(pathDataAQI)
        AQI_24h = dataAQI['AQI 24h']
        time = dataAQI['yymmdd']

        axs.plot(time, AQI_24h, label=str(i))
    pos = axs.get_position()
    axs.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
    plt.legend(loc='center right', bbox_to_anchor=(1.1, 0.5))
    plt.show()


def plotAQI1h():
    infoKit = pd.read_csv('../out/locationFairKit.csv')
    kitID = infoKit['Kit ID']
    fig, axs = plt.subplots(figsize=(15, 7))
    plt.title('Average AQI value per hour on 2021-12-04')
    axs.set(xlabel='Data', ylabel='AQI')
    plt.gcf().autofmt_xdate()
    for i in kitID:
        pathDataAQI = '../out/data/DataAverageByHour/AQI_averageByHour_KitID' + str(i) + '.csv'
        dataAQI = pd.read_csv(pathDataAQI)
        AQI_1h = np.array([])
        time = np.array([])
        index = 0
        for yymmdd in dataAQI['yymmdd']:
            if yymmdd == '2021-12-12':
                AQI_1h = np.append(AQI_1h,dataAQI['AQI 1h'][index])
                time = np.append(time,dataAQI['time'][index])
            index += 1

        axs.plot(time, AQI_1h, label=str(i))
        # print(time)
        # print('-----------------------------------------')
    pos = axs.get_position()
    axs.set_position([pos.x0, pos.y0, pos.width * 0.9, pos.height])
    plt.legend(loc='center right', bbox_to_anchor=(1.1, 0.5))
    plt.show()

def plotRadarMap24h():
    infoKit = pd.read_csv('../out/locationFairKit.csv')
    kitID = infoKit['Kit ID']
    # i = 1037
    # pathDataAQI = '../out/data/DataAverageByDay/AQI_averageByDay_KitID' + str(i) + '.csv'
    # dataAQI = pd.read_csv(pathDataAQI)
    # AQI_24h = dataAQI['AQI 24h']
    # time = dataAQI['yymmdd']
    plt.figure(figsize=(9, 9))
    axs = plt.subplot(polar=True)
    plt.title('Average AQI value for the day')
    for i in kitID:
        pathDataAQI = '../out/data/DataAverageByDay/AQI_averageByDay_KitID' + \
            str(i) + '.csv'
        dataAQI = pd.read_csv(pathDataAQI)
        AQI_24h = dataAQI['AQI 24h']
        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(AQI_24h))
        
        axs.set_xticks( [0, np.pi/6, np.pi*2/6,np.pi*3/6, np.pi*4/6, np.pi*5/6,
                        np.pi*6/6, np.pi*7/6, np.pi*8/6, np.pi*9/6, np.pi*10/6, np.pi*11/6])
        label = ['01-2021', '02-2021', '03-2021', '04-2021', '05-2021', '06-2021',
                '07-2021', '08-2021', '09-2021', '10-2021', '11-2021', '12-2021']
        axs.set_xticklabels(label)           
        plt.plot(label_loc, AQI_24h)
    plt.show()


plotAQI24h()
