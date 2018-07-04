import matplotlib.pyplot as plt
import numpy as np
from potential_fields import potencial
from numpy.linalg import norm

zoom = 1
mapsize = np.array([215, 185])
maplines = [
    [40, 40, 40, 80],
    [40, 80, 60, 80],
    [60, 80, 60, 40],
    [60, 40, 40, 40],

    [40+70, 40+30, 40+70, 80+30],
    [40+70, 80+30, 60+70, 80+30],
    [60+70, 80+30, 60+70, 40+30],
    [60+70, 40+30, 40+70, 40+30],

    [0, 0, mapsize[0], 0],
    [0, 0, 0, mapsize[1]],
    [0, mapsize[1], mapsize[0], mapsize[1]],
    [mapsize[0], 0, mapsize[0], mapsize[1]]
]

print(maplines)

objectives = [
	[200, 200]
]

dangers = [
	[200, 10]
]

sizex, sizey = (mapsize*zoom).astype(int)
x = np.linspace(0, mapsize[0], sizex)
y = np.linspace(0, mapsize[1], sizey)

X, Y = np.meshgrid(x, y, sparse=True)
M = np.zeros((sizey, sizex))

UU = np.zeros((sizey, sizex))
VV = np.zeros((sizey, sizex))
SS = np.zeros((sizey, sizex))

for i in range(sizex):
	for j in range(sizey):
		p = [x[i], y[j]]
		F, U = potencial(p, maplines, objectives, dangers)
		M[j, i] = U
		UU[j, i] = F[0]
		VV[j, i] = F[1]
		SS[j, i] = norm(F)/10




# M[M > 100] = 100

plt.gca().set_xlim([0,sizex])
plt.gca().set_ylim([0,sizey])
plt.gca().invert_yaxis()

plt.streamplot(X, Y, UU, VV, color=M, density=0.99)

#plt.imshow(M, interpolation='nearest')

# show lines
for line in maplines:
	line = np.array(line)
	x1, y1, x2, y2 = line
	x = np.array([x1, x2])*zoom
	y = np.array([y1, y2])*zoom
	plt.plot(x, y, color='white')

plt.show()

# PARA VER O U, COMENTAR LINHA 64 E DESCOMENTAR A LINHA 66 (DESCE PRO MAIS ESCURO)