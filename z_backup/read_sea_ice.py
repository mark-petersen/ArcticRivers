import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma # mask library
data_dir = '/Users/franziskaborneff/drive/Science_Fair/data/ice/'
infile = 'bt_197811_n07_v3.1_n.bin'
with open(data_dir+infile, 'rb') as fr:
	#hdr = fr.read(300)
	ice = np.fromfile(fr, dtype='uint16')
print('size ',np.shape(ice))
ice = ice.reshape(448, 304)

ice = ice / 1000.

ice = ma.masked_greater(ice, 1.0)
print(np.max(ice))

fig, ax = plt.subplots()
plt.imshow(ice)
plt.set_cmap('Blues_r')
fig.set_facecolor("red")
plt.title('Arctic Sea Ice Concentration')
plt.ylim(380, 125)
plt.colorbar()
plt.show()
