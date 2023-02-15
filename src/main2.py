from PIL import Image
import numpy as np
from math import floor, ceil, sqrt
import random

seed = 10

np.random.seed(seed)
width, height = 10, 10
xpix, ypix = 800, 800
matrix = np.random.sample((width + 1, height + 1)) 

horizontallyTileable = True
verticallyTileable = False


if horizontallyTileable:
    for y in range(height + 1):
        matrix[width, y] = matrix[0, y]
        
if verticallyTileable:
    for x in range(width + 1):
        matrix[x, height] = matrix[x, 0]

def func2d(x,y):
    xs = floor(x)
    xm = ceil(x)
    ys = floor(y)
    ym = ceil(y)
    
    if(xs == xm):
        xm += 1
    if(ys == ym):
        ym += 1
    
    p = np.zeros((4))
    p[0] = matrix[xs,ys]
    p[1] = matrix[xs,ym]
    p[2] = matrix[xm,ys]
    p[3] = matrix[xm,ym]
    
    d = np.zeros((4))
    d[0] = sqrt((x-xs)**2 + (y-ys)**2) 
    d[1] = sqrt((x-xs)**2 + (y-ym)**2) 
    d[2] = sqrt((x-xm)**2 + (y-ys)**2) 
    d[3] = sqrt((x-xm)**2 + (y-ym)**2) 
    
    
    retval = 0
    for i in range(len(p)):
        retval += (max(1 - d[i], 0) * p[i])
        

    return retval
    
pixels = np.zeros((xpix,ypix))
for i in range(ypix):
    for j in range(xpix):
        val=func2d(j / xpix * width, i / ypix * height)
        pixels[j,i] = val
        

map = Image.new( mode = "RGB", size = (xpix, ypix) )
pxn = map.load()

for y in range(ypix):
    for x in range(xpix):
        temp = pixels[x,y]
        if(temp > 0.9):
            color = (255,255,255)
        elif temp > 0.8:
            color = (80,80,80)
        elif temp > 0.75:
            color = (60,60,60)
        elif temp > 0.6:
            color = (32,160,32)
        elif temp > 0.55:
            color = (32,200,32)
        elif temp > 0.5:
            color = (245,245,200)
        elif temp > 0.4:
            color = (128,128,255)
        elif temp > 0.3:
            color = (64,128,255)
        elif temp > 0.2:
            color = (0,128,255)
        elif temp > 0.1:
            color = (0,0,255)
        else:
            color = (0,0,128)
        pxn[x,y] = color
map.show()
map.save("generated_image_" + str(xpix) + "-" + str(ypix) + "-" + str(seed) + ".png")