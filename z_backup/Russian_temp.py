import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

data_dir = '/Users/franziskaborneff/drive/Science_Fair/data/'
df = pd.read_csv(data_dir + 'atmospheric_temperature/Kyusyur_21921.txt', header=None, delim_whitespace=True)
df.columns = ["station_number", "year", "month", "day", "EX1", "TMIN", "EX2", "TOBS", "EX3", "TMAX", "EX4", "PRCP", "EX5", "EX6"]

year = df['year']
month = df['month']
day = df['day']
Tmax = df['TMAX']
Tmin = df['TMIN']


N = len(Tmax)
plotdate = np.zeros(N)
for j in range(N):
    plotdate[j] = year[j] + month[j] / 12 + day[j] / 365

plt.plot(plotdate[0:N], Tmax[0:N], 'b')
plt.plot(plotdate[0:N], Tmin[0:N], 'r')
plt.xlim(1912, 1915)
plt.ylim(-65, 30)
plt.grid()
plt.xlabel('date')
plt.ylabel('temperature (F)')
plt.title('Kyusyur Air Temperature')
# plt.show()
# plt.show()
pickle.dump([plotdate, Tmax, Tmin], open("pickle/KyusyurTemp.p", "wb"))

startYear = 1950
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

# # July
# m, b = np.polyfit(plotYear, TminMonthlyAvg[:, 6], 1)
# plt.plot(plotYear, TminMonthlyAvg[:, 6], label='July Avg slope= '+str(round(m*70,2))+' F/70 yrs')
# plt.plot(plotYear, m * plotYear + b)
# print(' July slope =', m)
#
# # Yearly Avg
# m, b = np.polyfit(plotYear, TminYearlyAvg, 1)
# plt.plot(plotYear, TminYearlyAvg,'-', label='Yearly Avg slope= '+str(round(m*70,2))+' F/70 yrs')
# plt.plot(plotYear, m * plotYear + b, '-')
# print(' Yearly avg slope =', m)
#
# # Jan
# m, b = np.polyfit(plotYear, TminMonthlyAvg[:, 0], 1)
# plt.plot(plotYear, TminMonthlyAvg[:, 0], label='Jan Avg slope= '+str(round(m*70,2))+' F/70 yrs')
# plt.plot(plotYear, m * plotYear + b)
# print(' Jan slope =', m)


plt.legend()
plt.grid()
plt.xlabel('year')
plt.ylabel('temperature (F)')
plt.show()
# # define data
