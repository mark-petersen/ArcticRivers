
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy.ma as ma


data_dir = '/Users/franziskaborneff/drive/Science_Fair/data/'
df = pd.read_csv(data_dir + 'atmospheric_temperature/Kyusyur_21921.txt', header=None, delim_whitespace=True)
df.columns = ["station_number", "year", "month", "day", "EX1", "Tobs", "EX2", "TOBS", "EX3", "TMAX", "EX4", "PRCP", "EX5", "EX6"]

year = df['year']
month = df['month']
day = df['day']
# Tmax = df['TMAX']
# Tobs = df['Tobs']
Tobs = df['TOBS']

N = len(Tobs)
plotdate = np.zeros(N)
for j in range(N):
    plotdate[j] = year[j] + month[j] / 12 + day[j] / 365


# plt.plot(plotdate[0:N], Tmax[0:N], 'b')
# plt.plot(plotdate[0:N], Tobs[0:N], 'r')
# plt.grid()
# plt.xlabel('date')
# plt.ylabel('temperature (F)')
# plt.title('Roanoke Air Temperature')
# plt.show()

startYear = np.min(year)
endYear = np.max(year) - 1  # -1 goes until 2021
nYears = int(endYear - startYear) + 1
nMonths = 12
TobsMonthlyAvg = np.zeros([nYears + 1, nMonths])
counter = np.zeros([nYears + 1, nMonths], dtype='int')
TobsYearlyAvg = np.zeros([nYears + 1])
counterYear = np.zeros([nYears + 1], dtype='int')
for j in range(N):
    if Tobs[j] == -99.9:
        continue
    TobsMonthlyAvg[year[j] - startYear, month[j] - 1] += Tobs[j]
    counter[year[j] - startYear, month[j] - 1] += 1
    TobsYearlyAvg[year[j] - startYear] += Tobs[j]
    counterYear[year[j] - startYear] += 1
#if data entry is bad set to previous year
plotYear = np.arange(startYear, endYear + 2)
for j in range(nYears + 1):
    if counterYear[j] == 0:
        TobsYearlyAvg[j] = TobsYearlyAvg[j-1]
    else:
        TobsYearlyAvg[j] = TobsYearlyAvg[j] / counterYear[j]

    #

for j in range(nYears +1):
    for m in range(12):
        if counter[j, m] == 0:
            TobsMonthlyAvg[j, m] = TobsMonthlyAvg[j-1, m]
        else:
            TobsMonthlyAvg[j, m] = TobsMonthlyAvg[j, m] / counter[j, m]


TobsYearlyAvg[0] = 0.0
TobsYearlyAvg[1] = 0.0
# print(plotYear[1940 - startYear:2010 - startYear], ma.masked_invalid(TobsMonthlyAvg[1940 - startYear:2010 - startYear, 6]), 1)

#July
m, b = np.polyfit(plotYear[1930 - startYear:2010 - startYear], TobsMonthlyAvg[1930 - startYear:2010 - startYear, 6], 1)
plt.plot(plotYear, TobsMonthlyAvg[:, 6], label='July Avg slope= '+str(round(m*70,2))+' F/70 yrs')
plt.plot(plotYear, m * plotYear + b)
print(' July slope =', m)

# Yearly Avg
m, b = np.polyfit(plotYear[1930 - startYear:2010 - startYear], TobsYearlyAvg[1930 - startYear:2010 - startYear], 1)
plt.plot(plotYear, TobsYearlyAvg,'-', label='Yearly Avg slope= '+str(round(m*70,2))+' F/70 yrs')
plt.plot(plotYear, m * plotYear + b, '-')
print(' Yearly avg slope =', m)

# Jan
m, b = np.polyfit(plotYear[1930 - startYear:2010 - startYear], TobsMonthlyAvg[1930 - startYear:2010 - startYear, 0], 1)
plt.plot(plotYear, TobsMonthlyAvg[:, 0], label='Jan Avg slope= '+str(round(m*70,2))+' F/70 yrs')
plt.plot(plotYear, m * plotYear + b)
print(' Jan slope =', m)


plt.legend()
plt.grid()
plt.xlim((1930,2010))
plt.ylim((-50,40))
plt.xlabel('year')
plt.ylabel('temperature (F)')
plt.title('Kyusyur Air Temperature  (Daily Obs)')
# plt.show()
plt.savefig('plots/Temp_all/TempLena.pdf')
# define data
