from polar_convert.constants import NORTH
from polar_convert import polar_ij_to_lonlat
import numpy as np
import matplotlib.pyplot as plt
import pickle
import numpy.ma as ma  # mask library
import matplotlib.animation as animation
import matplotlib as mpl
import glob

# riverList = ['Lena', 'Mack', 'Ob', 'Yukon', 'Kolyma', 'Yen']
riverList = ['Arctic']
maxice=1.0
for river in riverList:
    if river == "Arctic":
        titleText = 'Arctic'
        # maxice = 0.3802620044832228
        latstart = 63
        latend = 90
        lonstart = 0
        lonend = 360

    if river == "Lena":
        file = 'Lena_Kyusyur_Version_20220630.xlsx'
        titleText = 'Lena'
        latstart = 70.95
        latend = 75.27
        lonstart = 120.19
        lonend = 133.06
        # latstart = 67.42
        # latend = 82
        # lonstart = 104
        # lonend = 151
    elif river == "Mack":
        file = 'Mackenzie_ArcticRedRiver_Version_20220630.xlsx'
        titleText = 'Mackenzie'
        latstart = 68.15
        latend = 71.91
        lonstart = 217.67
        lonend = 231.24
    elif river == "Ob":
        file = 'Ob_Salekhard_Version_20220630.xlsx'
        titleText = 'Ob'
        latstart = 66.41
        latend = 74.42
        lonstart = 69.78
        lonend = 75.23
    elif river == "Yukon":
        file = 'Yukon_PilotStation_Version_20220630.xlsx'
        titleText = 'Yukon'
        latstart = 61.76
        latend = 65.09
        lonstart = 360-171.93
        lonend = 360-161.16
    elif river == "Kolyma":
        file = 'Kolyma_Kolymskoe_Version_20220630.xlsx'
        titleText = 'Kolyma'
        latstart = 68.57
        latend = 72.54
        lonstart = 156.29
        lonend = 168.01
    elif river == "Yen":
        file = 'Yenisei_Igarka_Version_20220630.xlsx'
        titleText = 'Yenisei'
        latstart = 71.02
        latend = 74.42
        lonstart = 75.21
        lonend = 84.47


    i = 10  # `i` is an int representing the x grid coordinate
    j = 200  # `j` is an int representing y grid coordinate
    grid_size = 25  # in km
    hemisphere = NORTH
    lon, lat = polar_ij_to_lonlat(i, j, grid_size, hemisphere)

    data_dir = '/Users/franziskaborneff/data/ice/'

    Nx = 304
    Ny = 448

    lon = np.zeros([Ny, Nx])
    lat = np.zeros([Ny, Nx])
    RiverMask = np.zeros([Ny, Nx])
    OceanMask = np.ones([Ny, Nx])
    image = np.ones([Ny, Nx])*0.75

    i: int
    for i in range(Nx):
        for j in range(Ny):
            lon[j, i], lat[j, i] = polar_ij_to_lonlat(i + 1, j + 1, grid_size, hemisphere)
            if latstart < lat[j, i] < latend and \
                    lonstart < lon[j, i] < lonend:
                RiverMask[j, i] = 1


    infile = "bt_19790705_n07_v3.1_n.bin"
    print(data_dir + infile)

    with open(data_dir + infile, 'rb') as fr:
        ice = np.fromfile(fr, dtype='uint16')
    ice = ice.reshape(448, 304)
    for i in range(Nx):
        for j in range(Ny):
            if ice[j, i] == 1200: #land
                OceanMask[j, i] = 0


    years = np.arange(1978, 2023)
    # years = np.arange(1978, 2023)
    months = np.arange(1, 13)
    days = np.arange(1, 32)
    fig = plt.figure()
    ims = []
    Ntime = 45 * 365
    IceCover = np.zeros(Ntime)
    plotdate = np.zeros(Ntime)  # , dtype = int)
    k = 0
    for y in years:
        for m in months:
            for d in days:
                datestring = str(y) + str(m).zfill(2) + str(d).zfill(2)
                infile = 'bt_' + datestring + '_*_n.bin'
                # print(data_dir+infile)
                try:
                    with open(glob.glob(data_dir + infile)[0], 'rb') as fr:
                        ice = np.fromfile(fr, dtype='uint16')
                    ice = ice.reshape(448, 304)
                    ice = ice / 1000.

                    plotdate[k] = y + m / 12. + d / 365.

                    iceSum = 0.0
                    iceCounter = 0
                    for i in range(Nx):
                        for j in range(Ny):
                            if RiverMask[j, i] == 1 and OceanMask[j, i] == 1:
                                iceSum = iceSum + ice[j, i]
                                iceCounter = iceCounter + 1
                    IceCover[k] = iceSum / iceCounter

                    ice = ma.masked_greater(ice, 1.0)
                    k = k + 1
                    print('found ' + infile)

                    # plt.clf()
                    # plt.subplot(2,1,1)
                    # plt.set_cmap("Blues_r")
                    # cmap = plt.get_cmap("Blues_r")
                    # cmap.set_bad(color='silver', alpha=1.)
                    # plt.set_cmap("Blues_r")
                    # #fig, ax = plt.subplots()
                    # plt.imshow(np.rot90(ice[145:215,125:225], 2))
                    # plt.clim(0,1)
                    # plt.colorbar()
                    # plt.subplot(2,1,2)
                    # plt.imshow(np.rot90(OceanMask[145:215, 125:225], 2))
                    # # plt.contourf(lon[100:215,125:225], lat[100:215,125:225], ice[100:215,125:225])
                    # # ims.append([im])
                    # # plt.ylim(70,85)
                    # # plt.xlim(60,160)
                    # # plt.xlim(60,160)
                    # plt.clim(0,1)
                    # plt.colorbar()
                    # plt.show()
                except:
                    # print('File not found')
                    continue

    plt.plot(plotdate[0:k], IceCover[0:k]/maxice)
    plt.xlabel('Date')
    plt.ylabel('Sea Ice Concentration')
    plt.title(titleText+'River Outlet Sea Ice Concentration')
    plt.grid()
    pickle.dump([plotdate[0:k], IceCover[0:k]], open("pickle/IceCover"+river+str(latstart)+".p", "wb"))

    print(max(IceCover))
    plt.savefig('plots/seaice_con/'+river+str(latstart)+'_1978-2022.pdf')
    #
    #                 plt.xticks([])
    #                 plt.yticks([])
    #
    #                 plt.title('Arctic Sea Ice Concentration ' + str(m) + '/' + str(d) + '/' + str(y))
    #                 plt.ylim(380, 125)
    #                 plt.colorbar()
    #                 plt.savefig('/Users/franziskaborneff/drive/Science_Fair/plots/ice/seaice_'+ datestring+ ".png")
    #             except:
    #                 print('file not found')
    #
    #
    # ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True)
    # ani.save('/Users/franziskaborneff/drive/Science_Fair/movies/ice.mp4')
