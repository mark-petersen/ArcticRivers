import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

headers = ['Sensor Value', 'Date', 'Time']
data_dir = '/Users/franziskaborneff/drive/Science_Fair/data/'
df = pd.read_csv(data_dir + 'atmospheric_temperature/Roanoke1948.csv')
Tmax = df['TMAX']
Tmin = df['TMIN']
snow = df['SNOW']
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

startYear = np.min(year)
endYear = np.max(year) - 1  # -1 goes until 2021
nYears = int(endYear - startYear) + 1
nMonths = 12
snowMonthlyAvg = np.zeros([nYears + 1, nMonths])
counter = np.zeros([nYears + 1, nMonths], dtype='int')
snowYearlyAvg = np.zeros([nYears + 1])
counterYear = np.zeros([nYears + 1], dtype='int')
for j in range(N):
    snowMonthlyAvg[year[j] - startYear, month[j] - 1] += snow[j]
    counter[year[j] - startYear, month[j] - 1] += 1
    snowYearlyAvg[year[j] - startYear] += snow[j]
    counterYear[year[j] - startYear] += 1
snowMonthlyAvg = snowMonthlyAvg[1:nYears, :] / 10  # / counter[1:nYears, :]
plotYear = np.arange(startYear, endYear)
snowYearlyAvg = np.nan_to_num(snowYearlyAvg[1:nYears]) / 10  # / counterYear[1:nYears]

# Yearly Avg
m, b = np.polyfit(plotYear, snowYearlyAvg, 1)
plt.plot(plotYear, snowYearlyAvg, '-', label='Yearly Avg slope= ' + str(round(m * 70, 2)) + ' F/70 yrs')
plt.plot(plotYear, m * plotYear + b, '-')
print(' Yearly avg slope =', m)

# Jan
m, b = np.polyfit(plotYear, snowMonthlyAvg[:, 0], 1)
plt.plot(plotYear, snowMonthlyAvg[:, 0], label='Jan Avg slope= ' + str(round(m * 70, 2)) + ' F/70 yrs')
plt.plot(plotYear, m * plotYear + b)
print(' Jan slope =', m)

plt.legend()
plt.grid()
plt.xlabel('date')
plt.ylabel('snow fall (in)')
plt.title('Roanoke Snow Fall')
plt.show()
