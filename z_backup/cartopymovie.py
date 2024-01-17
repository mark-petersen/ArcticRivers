import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma  # mask library
from polar_convert.constants import NORTH
from polar_convert import polar_ij_to_lonlat
import cartopy.crs as ccrs
import cartopy.feature as cfeature

data_dir = '/Users/franziskaborneff/data/ice/'
years = np.arange(1980,1981)
months = [1] # np.arange(1,13)
days = [1] #np.arange(1, 32)
fig = plt.figure()


grid_size = 25  # in km
hemisphere = NORTH
data_dir = '/Users/franziskaborneff/data/ice/'

Nx = 304
Ny = 448

lon = np.zeros([Ny, Nx])
lat = np.zeros([Ny, Nx])
# LenaMask = np.zeros([Ny, Nx])
# OceanMask = np.zeros([Ny, Nx])
i: int
for i in range(Nx):
    for j in range(Ny):
        lon[j,i], lat[j,i] = polar_ij_to_lonlat(i+1, j+1, grid_size, hemisphere)

for y in years:
    for m in months:
        for d in days:
            datestring = str(y) + str(m).zfill(2) + str(d).zfill(2)
            infile = "bt_" + datestring + "_n07_v3.1_n.bin"
            print(data_dir+infile)
            # try:
            with open(data_dir + infile, 'rb') as fr:
                ice = np.fromfile(fr, dtype='uint16')
            ice = ice.reshape(448, 304)
            ice = ice / 1000.
            ice = ma.masked_greater(ice, 1.0)
            # plt.clf()
            # plt.set_cmap("Blues_r")
            # cmap = plt.get_cmap("Blues_r")
            # cmap.set_bad(color='silver', alpha=1.)
            # plt.set_cmap("Blues_r")
            # im = plt.imshow(ice)
            ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=0))
            cs = ax.coastlines(resolution='110m', linewidth=0.5)

            ax.gridlines()
            ax.set_extent([-180, 180, 40, 90], crs=ccrs.PlateCarree())
            dx = dy = 25000

            x = np.arange(-3850000, +3750000, +dx)
            y = np.arange(+5850000, -5350000, -dy)
            print(x.shape,y.shape,ice.shape)
            ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='g'))

            kw = dict(central_latitude=90, central_longitude=-45, true_scale_latitude=70)
            cs = ax.pcolormesh(x, y, ice, cmap=plt.cm.Blues_r,
                               transform=ccrs.Stereographic(**kw))

            # plt.xticks([])
            # plt.yticks([])
            #
            # plt.title('Arctic Sea Ice Concentration ' + str(m) + '/' + str(d) + '/' + str(y))
            # plt.ylim(380, 125)
            # plt.colorbar()
            # writer.grab_frame();
            print('Success')

            plt.savefig('/Users/franziskaborneff/drive/Science_Fair/plots/seaice_'+ datestring+ ".png")
        # except:
        #         print('file not found or error')


