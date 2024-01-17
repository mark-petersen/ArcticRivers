import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import pickle
from scipy import stats
import numpy.ma as ma

#########################################################################
#  Compute Threshold Dates
#########################################################################
riverList = ['Yukon','Ob','Lena', 'Mack','Yen','Kolyma']
# riverList = ['Kolyma']
thresholdSlope = -99.0*np.ones([6,3])
iRiver = -1

for river in riverList:
    startplotyear = 1979
    endplotyear = startplotyear + 5
    convertFtoC = True
    if river == 'Lena':
        titleText = 'Lena'
        convertFtoC = False
    elif river == 'Mack':
        titleText = 'Mackenzie'
    elif river == 'Ob':
        titleText = 'Ob at Salekhard'
    elif river == 'Yukon':
        titleText = 'Yukon'
    elif river == 'Kolyma':
        titleText = 'Kolyma'
    elif river == 'Kolyma':
        titleText = 'Kolyma'
    elif river == 'Yen':
        titleText = 'Yenisei'
    elif river == 'Arctic63':
        titleText = 'Arctic'

    iRiver += 1

    Threshold = True
    if Threshold:
        # Ice Melt Threshold
        IceDate, Ice = pickle.load(open('pickle/IceCover' + river + '.p', 'rb'))
        L = len(Ice)
        IceThreshold = 0.90
        IceMeltDay = np.zeros(200)
        IceMeltYear = np.zeros(200)
        y = 0  # year counter +1
        startYear = int(IceDate[0])
        lastMeltYear = 0
        for d in range(L):
            currentYear = int(IceDate[d])
            if Ice[d] < IceThreshold and currentYear > lastMeltYear \
                    and IceDate[d] - int(IceDate[d]) > 0.25:  # melt date must be after quarter year
                IceMeltYear[y] = int(IceDate[d])
                IceMeltDay[y] = IceDate[d] - int(IceDate[d])
                y = y + 1
                lastMeltYear = int(IceDate[d])
        finalIceY = y - 1

        # # River Discharge Threshold
        RiverDate, Discharge = pickle.load(open('pickle/River' + river + '.p', 'rb'))
        L = len(RiverDate)
        riverThreshold = 0.3 * np.max(Discharge)
        dischargeDay = np.zeros(200)
        dischargeYear = np.zeros(200)
        y = 0  # year counter +1
        startYear = int(RiverDate[0])
        lastMeltYear = 0
        for d in range(L):
            currentYear = int(RiverDate[d])
            if Discharge[d] > riverThreshold and currentYear > lastMeltYear:
                dischargeYear[y] = int(RiverDate[d])
                dischargeDay[y] = RiverDate[d] - int(RiverDate[d])
                y = y + 1
                lastMeltYear = int(RiverDate[d])
        finalDischargeY = y - 1
        #
        # # Air Temp Threshold
        # if river == "Lena":
        #     plotdate, TempVar, TempDummy = pickle.load(open('pickle/Temp' + river + '.p', 'rb'))
        # else:
        #     plotdate, TempVar = pickle.load(open('pickle/Temp' + river + '.p', 'rb'))
        #     print(plotdate, TempVar)
        # if convertFtoC:
        #     TempVar = (TempVar - 32) * 5.0 / 9.0
        # # print(river, np.shape(plotdate), np.shape(TempVar))
        # L = len(plotdate)
        # tempThreshold = 5.0
        # TempVarDay = np.zeros(200)
        # TempVarYear = np.zeros(200)
        # y = 0  # year counter +1
        # startYear = int(plotdate[0])
        # lastMeltYear = 0
        # for d in range(L):
        #     currentYear = int(plotdate[d])
        #     # print('d', d, 'y', y, np.size(plotdate), np.size(TempVarYear), TempVar, tempThreshold, currentYear, lastMeltYear )
        #
        #     if TempVar[d] > tempThreshold and currentYear > lastMeltYear:
        #         print('d',d,'y',y,np.size(plotdate),np.size(TempVarYear))
        #         TempVarYear[y] = int(plotdate[d])
        #         TempVarDay[y] = plotdate[d] - int(plotdate[d])
        #         y = y + 1
        #         lastMeltYear = int(plotdate[d])
        # finalTempY = y - 1

    # Daily Plot
    dailyPlot = False
    if dailyPlot:
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 4)
        fig.subplots_adjust(right=0.75)

        twin1 = ax.twinx()
        twin2 = ax.twinx()

        # Offset the right spine of twin2.  The ticks and label have already been
        # placed on the right by twinx above.
        twin2.spines.right.set_position(('axes', 1.2))

        p1, = ax.plot(IceDate, Ice, 'b-', label='Sea Ice Concentration')
        p2, = twin1.plot(RiverDate, Discharge / 1000, 'r-', label='River Discharge')
        p3, = twin2.plot(plotdate, TempVar, 'g-', label='Atm. Temperature')

        plt.hlines(tempThreshold, 1900, 2024, 'g', linestyles='--')
        ax.hlines(IceThreshold, 1900, 2024, 'b', linestyles='--')
        twin1.hlines(riverThreshold / 1000, 1900, 2024, 'r', linestyles='--')

        ax.set_xlim(startplotyear, endplotyear)

        ax.set_ylim(-0.05, 2.5)
        twin1.set_ylim(-5, 150)
        twin2.set_ylim(-100, 40)

        ax.set_xlabel('date')
        ax.set_ylabel('sea ice concentration (fraction)')
        twin1.set_ylabel('river discharge (m^3/s, *1000)')
        twin2.set_ylabel('atmospheric temperature (C)')

        ax.yaxis.label.set_color(p1.get_color())
        twin1.yaxis.label.set_color(p2.get_color())
        twin2.yaxis.label.set_color(p3.get_color())

        tkw = dict(size=4, width=1.5)
        ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
        twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
        twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
        ax.tick_params(axis='x', **tkw)

        plt.title('' + titleText + ' River')

        # for short plot of season:
        # fig.set_size_inches(6.5, 4)
        # ax.set_xlim(2002.45, 2002.7)
        # plt.title('' + titleText + ' River, daily data')
        # ax.set_xticks(2002.0 + np.array([152, 182, 213, 244, 274, 305, 335])/365.0)
        # ax.set_xticklabels(['Jun 1', 'Jul 1', 'Aug 1', 'Sep 1', 'Oct 1', 'Nov 1', 'Dec 1'])
        # ax.set_xlabel('date in 2002')

        plt.show()
        # plt.savefig('plots/plot_all_daily/' + river + '_plot_all_daily' + str(startplotyear) + '.pdf')

    # Threshold Plot
    thresholdPlot = True
    if thresholdPlot:
        # Plot
        startYear = 1979
        lastMeltYear = 2022
        plt.clf()

        dur = lastMeltYear-startYear

        startfityear = startYear
        i1 = max(0, int(startfityear - IceMeltYear[0]))
        # m1, b1 = np.polyfit(IceMeltYear[i1:i1+dur], IceMeltDay[i1:i1+dur] * 365, 1)
        # print("m1, b1", m1, b1)
        m1, b1, r_value, p_value, std_err = scipy.stats.linregress(IceMeltYear[i1:i1+dur], IceMeltDay[i1:i1+dur] * 365)
        thresholdSlope[iRiver, 0] = m1
        # print(river, " Icemelt m1, b1", m1, b1, " r_value, p_value", r_value, p_value)


        i2 = max(0, int(startfityear - dischargeYear[0]))
        m2, b2 = np.polyfit(dischargeYear[i2:i2+dur], dischargeDay[i2:i2+dur] * 365, 1)
        m2, b2, r_value, p_value, std_err = scipy.stats.linregress(dischargeYear[i2:i2+dur], dischargeDay[i2:i2+dur] * 365)
        # print(river, "riverdischarge m2, b2", m2, b2, "r_value, p_value", r_value, p_value)
        thresholdSlope[iRiver, 1] = m2
        #
        #
        # i3 = max(0, int(startfityear - TempVarYear[0]))
        # print(TempVarYear)
        # print('(TempVarYear[i3:i3+dur])', TempVarYear[i3:i3+dur])
        # print('(TempVarDay[i3:i3+dur])', TempVarDay[i3:i3+dur])
        #
        # m3, b3 = np.polyfit(TempVarYear[i3:i3+dur], TempVarDay[i3:i3+dur] * 365, 1)
        # # m3, b3, r_value, p_value, std_err = scipy.stats.linregress(TempVarYear[i3:i3+dur], TempVarDay[i3:i3+dur] * 365)
        # print(river, "temp m2, b2", m2, b2, "r_value, p_value", r_value, p_value)
        # thresholdSlope[iRiver,2] = m3

        # plotVarList = ['S','R','T']
        plotVarList = ['S','R']
        for plotVar in plotVarList:
            plt.clf()
            if plotVar=='S':
                plt.plot(IceMeltYear[0:finalIceY], IceMeltDay[0:finalIceY] * 365, label='Sea Ice Breakup, m={:.2f}'.format(m1), color='b')
            elif plotVar == 'R':
                plt.plot(dischargeYear[0:finalDischargeY], dischargeDay[0:finalDischargeY] * 365, label='River Ice Breakup, m={:.2f}'.format(m2), color='r')
            # elif plotVar == 'T':
            #     plt.plot(TempVarYear[0:finalTempY], TempVarDay[0:finalTempY] * 365, label='Air Temp > 5C, m={:.2f}'.format(m3), color='g')

            plt.hlines(182, startYear, lastMeltYear, linestyles='--', color='grey')
            plt.hlines(213, startYear, lastMeltYear, linestyles='--', color='grey')
            plt.hlines(152, startYear, lastMeltYear, linestyles='--', color='grey')
            plt.hlines(121, startYear, lastMeltYear, linestyles='--', color='grey')
            plt.hlines(91, startYear, lastMeltYear, linestyles='--', color='grey')
            plt.text(startYear + 2, 213.5 + 1, 'August 1')
            plt.text(startYear + 2, 182.5 + 1, 'July 1')
            plt.text(startYear + 2, 152.5 + 1, 'June 1')
            plt.text(startYear + 2, 121.5 + 1, 'May 1')
            plt.text(startYear + 2, 91.5 + 1, 'April 1')

            if plotVar=='S':
                plt.plot(IceMeltYear[i1:finalIceY], m1 * IceMeltYear[i1:finalIceY] + b1, color='b', linestyle='--')
                plt.title('' + titleText + ' River, Day of Year Sea Ice Breaks Up')
                plt.ylabel('day of year sea ice breaks up')
            elif plotVar == 'R':
                plt.plot(dischargeYear[i2:finalDischargeY], m2 * dischargeYear[i2:finalDischargeY] + b2, color='r', linestyle='--')
                plt.title('' + titleText + ' River, Day of Year River Ice Breaks Up')
                plt.ylabel('day of year river ice breaks up')
            # elif plotVar == 'T':
            #     plt.plot(TempVarYear[i3 - 10:finalTempY], m3 * TempVarYear[i3 - 10:finalTempY] + b3, color='g',linestyle='--')
            #     plt.title('' + titleText + ' River, Day of Year Air Temperature > 5C')
            #     plt.ylabel('Day of Year Air Temperature > 5C')

            plt.xlim(startYear, lastMeltYear)
            plt.legend()
            plt.xlabel('Year')
            plt.ylim(140, 220)
            plt.ylim(152, 240)

            plt.xlim(startfityear, 2021)
            plt.savefig('plots/thresholddate/' + river + 'threshold+p_'+plotVar+'_'+str(startfityear)+'.pdf')
            # plt.show()

    corrPlot_discharge_ice = True
    if corrPlot_discharge_ice:
        endYear = 2020
        if river == 'Yukon':
            startYear = 1980
            nYears = endYear - startYear - 1
        elif river == 'Kolyma':
            startYear = 1985
            nYears = endYear - startYear - 3
        else:
            startYear = 1980
            nYears = endYear - startYear
        # print('dischargeYear',dischargeYear)
        # print('startyear', startYear)
        iStartDischarge = int(np.where(dischargeYear == startYear)[0])
        iStartIceVar = int(np.where(IceMeltYear == startYear)[0])
        r = np.corrcoef(dischargeDay[iStartDischarge:iStartDischarge + nYears],
                        IceMeltDay[iStartIceVar: iStartIceVar + nYears])
        plottime = 365 * dischargeDay[iStartDischarge:iStartDischarge + nYears]
        plt.clf()
        plt.plot(365 * dischargeDay[iStartDischarge:iStartDischarge + nYears],
                 365 * IceMeltDay[iStartIceVar: iStartIceVar + nYears], '.')
        # print(np.size(dischargeDay), np.shape(dischargeDay))
        # print(iStartDischarge, nYears)
        # print(365 * dischargeDay[iStartDischarge:iStartDischarge + nYears])
        plt.title(titleText + ' Correlation: Discharge vs Sea Ice r='+'{:.3f}'.format(r[0,1])+' T='+str(IceThreshold))
        plt.xlabel('Day of River Freshet > 50k m^3/s')
        plt.ylabel('Day of Sea Ice Breakup')
        print(titleText + ' Correlation: Discharge vs Sea Ice r='+'{:.3f}'.format(r[0,1])+' T='+str(IceThreshold))
        m, b = np.polyfit(plottime,
                          365 * IceMeltDay[iStartIceVar: iStartIceVar + nYears], 1)
        plt.plot(plottime, m * plottime + b)
        plt.savefig('plots/corrAirTempDischarge/' + river + '_corrSeaIceDischarge90.pdf')
        # plt.show()

    # Corr Plot
    corrPlot = False
    if corrPlot:
        startYear = 1980
        endYear = 2020
        nYears = endYear - startYear
        iStartDischarge = int(np.where(dischargeYear == startYear)[0])
        iStartTempVar = int(np.where(IceMeltYear == startYear)[0])
        r = np.corrcoef(dischargeDay[iStartDischarge:iStartDischarge + nYears],
                        TempVarDay[iStartTempVar: iStartTempVar + nYears])
        print(r)
        plottime = 365 * dischargeDay[iStartDischarge:iStartDischarge + nYears]
        plt.clf()
        plt.plot(365 * dischargeDay[iStartDischarge:iStartDischarge + nYears],
                 365 * TempVarDay[iStartTempVar: iStartTempVar + nYears], '.')
        print(np.size(dischargeDay), np.shape(dischargeDay))
        print(iStartDischarge, nYears)
        plt.title(titleText + ' Correlation between Discharge and Air Temp')
        plt.xlabel('Day of River Discharge > 50k m^3/s')
        plt.ylabel('Day of Atm Temp > 5C')
        m, b = np.polyfit(plottime,
                          365 * TempVarDay[iStartTempVar: iStartTempVar + nYears], 1)
        plt.plot(plottime, m * plottime + b)
        plt.savefig('plots/corrAirTempDischarge/' + river + '_corrAirTempDischarge.pdf')
        # plt.show()
    from matplotlib.collections import LineCollection

    def multiline(xs, ys, c, ax=None, **kwargs):
        '''Plot lines with different colorings

        Parameters
        ----------
        xs : iterable container of x coordinates
        ys : iterable container of y coordinates
        c : iterable container of numbers mapped to colormap
        ax (optional): Axes to plot on.
        kwargs (optional): passed to LineCollection

        Notes:
            len(xs) == len(ys) == len(c) is the number of line segments
            len(xs[i]) == len(ys[i]) is the number of points for each line (indexed by i)

        Returns
        -------
        lc : LineCollection instance.
        '''

        # find axes
        ax = plt.gca() if ax is None else ax

        # create LineCollection
        segments = [np.column_stack([x, y]) for x, y in zip(xs, ys)]
        lc = LineCollection(segments, **kwargs)

        # set coloring of line segments
        #    Note: I get an error if I pass c as a list here... not sure why.
        lc.set_array(np.asarray(c))

        # add lines to axes and rescale
        #    Note: adding a collection doesn't autoscalee xlim/ylim
        ax.add_collection(lc)
        ax.autoscale()
        return lc


    # Summer Plot
    riverdischargesummer = False
    if riverdischargesummer:
        RiverDate, Discharge = pickle.load(open('pickle/River' + river + '.p', 'rb'))
        L = len(RiverDate)
        dischargeArray = np.zeros([365, 200])
        xs = np.zeros([365, 200])
        yint = np.zeros([365, 200])
        y = 0  # year counter +1
        startYear = int(RiverDate[0])
        lastMeltYear = startYear
        for d in range(L - 360):
            currentYear = int(RiverDate[d])
            if currentYear > lastMeltYear:
                dischargeArray[:, y] = Discharge[d:d + 365]
                xs[:, y] = np.arange(1, 366)  # day of year
                y = y + 1
                lastMeltYear = int(RiverDate[d])
        finalDischargeY = y - 1

        print(dischargeArray)
        n_lines = 30
        x = np.arange(200)

        yint = np.arange(startYear, startYear + y)
        ys = dischargeArray[:, 0:y].T
        xs = xs[:, 0:y].T

        colors = np.arange(n_lines)

        fig, ax = plt.subplots()
        lc = multiline(xs, ys / 1000, yint, cmap='coolwarm', lw=0.5)
        plt.xlim(150, 300)
        plt.ylabel('River Discharge m^3/s, *1000')
        plt.xlabel('Day of Year')
        axcb = fig.colorbar(lc)
        axcb.set_label('Year')
        ax.set_title('' + titleText + ' River Discharge')
        ax.set_xticks([121, 152, 182, 213, 244, 274, 305])
        ax.set_xticklabels(['May 1', 'Jun 1', 'Jul 1', 'Aug 1', 'Sep 1', 'Oct 1', 'Nov 1'])
        plt.savefig('plots/riverdischargesummer/' + river + '_dischargesummer.pdf')

    atmTzoom = False
    if atmTzoom:
        plotdate, TempVar = pickle.load(open('pickle/Temp' + river + '.p', 'rb'))
        L = len(plotdate)
        ## smooth TempVar
        n = 30
        # number of smoothing neighbors on each side
        TempVarSmooth = TempVar
        for d in range(n + 1, L - 1):
            TempVarSmooth[d] = np.average(TempVar[d - n:d + n + 1])

        TempVarArray = np.zeros([365, 120])
        xs = np.zeros([365, 120])
        yint = np.zeros([365, 120])
        y = 0  # year counter +1
        startYear = int(plotdate[0])
        lastMeltYear = startYear
        for d in range(L - 360):
            currentYear = int(plotdate[d])
            if currentYear > lastMeltYear:
                print(currentYear)

                TempVarArray[:, y] = TempVarSmooth[d:d + 365]
                xs[:, y] = np.arange(1, 366)  # day of year
                y = y + 1
                lastMeltYear = int(plotdate[d])
        finalDischargeY = y - 1

        print(TempVarArray)
        n_lines = 30
        x = np.arange(120)

        yint = np.arange(startYear, startYear + y)
        ys = TempVarArray[:, 0:y].T
        xs = xs[:, 0:y].T

        colors = np.arange(n_lines)

        fig, ax = plt.subplots()
        lc = multiline(xs, ys, yint, cmap='coolwarm', lw=0.5)
        plt.xlim(150, 300)
        plt.ylabel('River Discharge m^3/s, *1000')
        plt.xlabel('Day of Year')
        axcb = fig.colorbar(lc)
        axcb.set_label('Year')
        ax.set_title('' + titleText + ' River Discharge at Kyusyur')
        ax.set_xticks([121, 152, 182, 213, 244, 274, 305])
        ax.set_xticklabels(['May 1', 'Jun 1', 'Jul 1', 'Aug 1', 'Sep 1', 'Oct 1', 'Nov 1'])
        plt.show()
        # plt.savefig('saved_plots/plot_all_summerdischarge.pdf')
