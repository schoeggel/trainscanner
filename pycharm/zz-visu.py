from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def reject_outliers(data, m=4):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

pt3d = np.loadtxt("tmp/3dpoints002.asc").T
# pt3d = np.load("tmp/3dpoints002.asc").T
# pt3d = pt3d[:-1]/pt3d[-1]   # https://pythonpath.wordpress.com/import-cv2/


center = np.median(pt3d, axis= 1)
maxdist = 400
goodpt = np.ndarray((3,1), dtype=float)
distances = []
#for i, x in np.transpose(pt3d):
for x,y,z in np.transpose(pt3d):
    d = (center[0]-x)**2 + (center[1]-y)**2 + (center[2]-z)**2
    d = d**0.5
    distances.append(d)
    if d < maxdist:
        goodpt = np.append(goodpt, np.array([x, y, z]))

goodpt.shape = (-1, 3)
goodpt = goodpt.T

print(goodpt.shape)
print("avg / median distances from center:")
print(np.std(distances), np.median(distances))



xs = goodpt[0:1]-center[0]
ys = goodpt[1:2]-center[1]
zs = goodpt[2:3]-center[2]

ax.scatter(xs, ys, zs, s=0.1)



ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()