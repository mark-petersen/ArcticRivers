import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

riverList = ['Lena', 'Mack', 'Ob', 'Yukon', 'Kolyma', 'Kolyma at Sred', 'Yen']

for river in riverList:
    if river == "Lena":
        file = 'Lena_Kyusyur_Version_20220630.xlsx'
        titleText = 'Lena at Kyusyur'
    elif river == "Mack":
        file = 'Mackenzie_ArcticRedRiver_Version_20220630.xlsx'
        titleText = 'Mackenzie at Arctic Red River'
    elif river == "Ob":
        file = 'Ob_Salekhard_Version_20220630.xlsx'
        titleText = 'Ob at Salekhard'
    elif river == "Yukon":
        file = 'Yukon_PilotStation_Version_20220630.xlsx'
        titleText = 'Yukon at Pilot Station'
    elif river == "Kolyma":
        file = 'Kolyma_Kolymskoe_Version_20220630.xlsx'
        titleText = 'Kolyma at Kolymskoe'
    elif river == "Kolyma at Sred":
        file = 'Kolyma_Srednekolymsk_Version_20220630.xlsx'
        titleText = 'Kolyma at Sred'
    elif river == "Yen":
        file = 'Yenisei_Igarka_Version_20220630.xlsx'
        titleText = 'Yenisei at Igarka'

    headers = ['Sensor Value','Date','Time']
    data_dir = '/Users/franziskaborneff/drive/Science_Fair/data/river_flow/'
    df = pd.read_excel(data_dir+file)
    Q=df['discharge']
    date=df['date']
    N=len(date)
    year=np.zeros(N)
    month=np.zeros(N)
    day=np.zeros(N)
    plotdate=np.zeros(N)
    for j in range(N):
        year[j]=date[j][0:4]
        month[j]=date[j][5:7]
        day[j]=date[j][8:10]
        plotdate[j]=year[j]+month[j]/12+day[j]/365

    print(Q)
    plt.clf()
    plt.plot(plotdate[0:N],Q[0:N])




    plt.xlim(1973,2022)
    # plt.xlim(1940, 1960)


    plt.grid()
    plt.xlabel('date')
    plt.ylabel('river discharge (m^3/sec)')
    plt.title(titleText)
    # plt.figure(figsize=(3,3))
    plt.xlim(1930, 2023)
    plt.savefig('plots/river_all/River'+river+'1930-2023.pdf')
    plt.xlim(2015, 2020)
    plt.savefig('plots/river_all/River'+river+'2015-2020.pdf')
    pickle.dump([plotdate, Q], open("pickle/River"+river+".p", "wb"))
