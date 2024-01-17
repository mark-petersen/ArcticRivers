import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma  # mask library
import matplotlib.animation as animation
import matplotlib as mpl

data_dir = '/Users/franziskaborneff/data/ice/'
years = np.arange(1980,1981)
months = [1] # np.arange(1,13)
days = [1] #np.arange(1, 32)
fig = plt.figure()



for y in years:
    for m in months:
        for d in days:
            datestring = str(y) + str(m).zfill(2) + str(d).zfill(2)
            infile = "bt_" + datestring + "_n07_v3.1_n.bin"
            print(data_dir+infile)
            try:
                with open(data_dir + infile, 'rb') as fr:
                    ice = np.fromfile(fr, dtype='uint16')
                ice = ice.reshape(448, 304)
                ice = ice / 1000.
                ice = ma.masked_greater(ice, 1.0)
                plt.clf()
                plt.set_cmap("Blues_r")
                cmap = plt.get_cmap("Blues_r")
                cmap.set_bad(color='silver', alpha=1.)
                plt.set_cmap("Blues_r")
                im = plt.imshow(ice)
                # ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=0))
                # cs = ax.pcolormesh(x, y, ice, cmap=plt.cm.Blues,
                #                    transform=ccrs.Stereographic(**kw))

                plt.xticks([])
                plt.yticks([])

                plt.title('Arctic Sea Ice Concentration ' + str(m) + '/' + str(d) + '/' + str(y))
                plt.ylim(380, 125)
                plt.colorbar()
                # writer.grab_frame();
                print('Success')

                plt.savefig('/Users/franziskaborneff/drive/Science_Fair/plots/seaice_'+ datestring+ ".png")
            except:
                print('file not found or error')


