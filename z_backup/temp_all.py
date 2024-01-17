import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

riverList = ['Mack', 'Ob', 'Yukon', 'Kolyma', 'Kolyma at Sred', 'Yen']
riverList = ['Kolyma']
print(riverList)
for river in riverList:
    if river == "Mack":
        file = 'Aklavik_Mack.csv'
        titleText = 'Mack at Aklavik'
        varname = "TMIN"
    elif river == "Ob":
        file = 'salekhard_Ob.csv'
        titleText = 'Ob at Salekhard'
        varname = "TAVG"
    elif river == "Yukon":
        file = 'Bethel_Yukon.csv'
        titleText = 'Yukon at Bethel'
        varname = "TMIN"
    elif river == "Kolyma_cher":
        file = 'cherskij_Kolyma.csv'
        titleText = 'Kolyma at Cherskij'
        varname = "TAVG"
    elif river == "Kolyma":
        file = 'buhta_Kolyma.csv'
        titleText = 'Kolyma at Buhta'
        varname = "TAVG"
    elif river == "Kolyma_Ostrov":
        file = 'ostrov_Kolyma.csv'
        titleText = 'Kolyma at Ostrov'
        varname = "TAVG"
    elif river == "Yen":
        file = 'dikson_Yenisey.csv'
        titleText = 'Air Temperature, Yenisei River at Dikson'
        varname = "TAVG"
    elif river == "Lena":
        file = 'dikson_Yenisey.csv'
        titleText = 'Lena at Kyus'
        varname = "TAVG"


    # print(titleText,file)

    headers = ['Sensor Value', 'Date', 'Time']
    data_dir = '/Users/franziskaborneff/drive/Science_Fair/data/'
    df = pd.read_csv(data_dir + 'atmospheric_temperature/'+file)
    TempVar = (df[varname]-32.0)*5.0/9.0
    date = df['DATE']
    N = len(date)
    year = np.zeros(N, dtype='int')
    month = np.zeros(N, dtype='int')
    day = np.zeros(N, dtype='int')
    plotdate = np.zeros(N)
    for j in range(N):
        year[j] = date[j][0:4]
        month[j] = date[j][5:7]
        day[j] = date[j][8:10]
        plotdate[j] = year[j] + month[j] / 12 + day[j] / 365
    # plt.plot(plotdate[0:N], Tmax[0:N], 'b')
    # plt.plot(plotdate[0:N], TempVar[0:N], 'r')
    plt.clf()
    plt.grid()

    startYear = np.min(year)
    endYear = np.max(year) - 1  # -1 goes until 2021
    nYears = int(endYear - startYear) + 1
    nMonths = 12
    TempVarMonthlyAvg = np.zeros([nYears + 1, nMonths])
    counter = np.zeros([nYears + 1, nMonths], dtype='int')
    TempVarYearlyAvg = np.zeros([nYears + 1])
    counterYear = np.zeros([nYears + 1], dtype='int')
    for j in range(N):
        if np.isnan(TempVar[j]):
            continue
        TempVarMonthlyAvg[year[j] - startYear, month[j] - 1] += TempVar[j]
        counter[year[j] - startYear, month[j] - 1] += 1
        TempVarYearlyAvg[year[j] - startYear] += TempVar[j]
        counterYear[year[j] - startYear] += 1
    TempVarMonthlyAvg = TempVarMonthlyAvg[1:nYears, :] / counter[1:nYears, :]
    plotYear = np.arange(startYear, endYear)
    TempVarYearlyAvg = TempVarYearlyAvg[1:nYears] / counterYear[1:nYears]

    # July
    m, b = np.polyfit(plotYear, TempVarMonthlyAvg[:, 6], 1)
    plt.plot(plotYear, TempVarMonthlyAvg[:, 6], label='July Avg slope= '+str(round(m*70,2))+' C/70 yrs',color='r')
    plt.plot(plotYear, m * plotYear + b,'r--')
    print(' July slope =', m)
    #
    # Yearly Avg
    m, b = np.polyfit(plotYear, TempVarYearlyAvg, 1)
    plt.plot(plotYear, TempVarYearlyAvg,'-', label='Yearly Avg slope= '+str(round(m*70,2))+' C/70 yrs',color='k')
    plt.plot(plotYear, m * plotYear + b, 'k--')
    print(' Yearly avg slope =', m)

    # Jan
    print('TempVarMonthlyAvg[:, 0]',TempVarMonthlyAvg[:, 0])
    m, b = np.polyfit(plotYear[2:], TempVarMonthlyAvg[2:, 0], 1)
    plt.plot(plotYear, TempVarMonthlyAvg[:, 0], label='Jan Avg slope= '+str(round(m*70,2))+' C/70 yrs',color='b')
    plt.plot(plotYear, m * plotYear + b,'b--')
    print(' Jan slope =', m)

    plt.legend()
    plt.grid()
    plt.ylim((-32,18))
    plt.xlim((1935,2022))
    plt.xlabel('year')
    plt.grid()
    plt.ylabel('temperature (C)')
    plt.title(titleText)
    plt.show()
    plt.savefig('plots/Temp_all/Temp'+river+'.pdf')
    pickle.dump([plotdate, TempVar], open("pickle/Temp"+river+".p", "wb"))
