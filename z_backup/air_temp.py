import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

headers = ['Sensor Value', 'Date', 'Time']
data_dir = '/Users/franziskaborneff/drive/Science_Fair/data/'
df = pd.read_csv(data_dir + 'atmospheric_temperature/Roanoke1948.csv')
Tmax = df['TMAX']
Tmin = df['TMIN']
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
# plt.plot(plotdate[0:N], Tmin[0:N], 'r')
# plt.grid()
# plt.xlabel('date')
# plt.ylabel('temperature (F)')
# plt.title('Roanoke Air Temperature')
# plt.show()

startYear = np.min(year)
endYear = np.max(year) - 1  # -1 goes until 2021
nYears = int(endYear - startYear) + 1
nMonths = 12
TminMonthlyAvg = np.zeros([nYears + 1, nMonths])
counter = np.zeros([nYears + 1, nMonths], dtype='int')
TminYearlyAvg = np.zeros([nYears + 1])
counterYear = np.zeros([nYears + 1], dtype='int')
for j in range(N):
    TminMonthlyAvg[year[j] - startYear, month[j] - 1] += Tmin[j]
    counter[year[j] - startYear, month[j] - 1] += 1
    TminYearlyAvg[year[j] - startYear] += Tmin[j]
    counterYear[year[j] - startYear] += 1
TminMonthlyAvg = TminMonthlyAvg[1:nYears, :] / counter[1:nYears, :]
plotYear = np.arange(startYear, endYear)
TminYearlyAvg = TminYearlyAvg[1:nYears] / counterYear[1:nYears]

# July
m, b = np.polyfit(plotYear, TminMonthlyAvg[:, 6], 1)
plt.plot(plotYear, TminMonthlyAvg[:, 6], label='July Avg slope= '+str(round(m*70,2))+' F/70 yrs')
plt.plot(plotYear, m * plotYear + b)
print(' July slope =', m)

# Yearly Avg
m, b = np.polyfit(plotYear, TminYearlyAvg, 1)
plt.plot(plotYear, TminYearlyAvg,'-', label='Yearly Avg slope= '+str(round(m*70,2))+' F/70 yrs')
plt.plot(plotYear, m * plotYear + b, '-')
print(' Yearly avg slope =', m)

# Jan
m, b = np.polyfit(plotYear, TminMonthlyAvg[:, 0], 1)
plt.plot(plotYear, TminMonthlyAvg[:, 0], label='Jan Avg slope= '+str(round(m*70,2))+' F/70 yrs')
plt.plot(plotYear, m * plotYear + b)
print(' Jan slope =', m)


plt.legend()
plt.grid()
plt.ylim((10,72))
plt.xlabel('year')
plt.ylabel('temperature (F)')
plt.title('Roanoke Air Temperature  (Daily Min)')

plt.savefig('saved_plots/plot_Tmin_roanoke.pdf')
# define data
