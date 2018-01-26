from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


pt3d = np.load("tmp/3dpoints001.npy")
pt3d = pt3d[:-1]/pt3d[-1]   # https://pythonpath.wordpress.com/import-cv2/
xs = pt3d[0:1]
ys = pt3d[1:2]
zs = pt3d[2:3]

ax.scatter(xs, ys, zs, s=0.2)



ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()