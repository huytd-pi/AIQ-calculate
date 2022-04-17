import numpy as np

class BPiTable:
    def Table(nameTable,num):
        I_Parameter     = np.array([0,50,100,150,200,300,400,500])
        O3_1h_Parameter = np.array([0,160,200,300,400,800,1000,1200])
        O3_8h_Parameter = np.array([0,100,120,170,210,400])
        CO_Parameter    = np.array([0,10000,30000,45000,60000,90000,120000,150000])
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
        elif nameTable == 'PM2_5':
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
        length = len(parameter)
        for i in range(0,length-1):
            if num >= parameter[i]:
                a   = parameter[i]
                a_1 = parameter[i+1]
                b   = I_Parameter[i]
                b_1 = I_Parameter[i+1]
        return b,b_1,a,a_1