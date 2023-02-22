from PIL import Image
import numpy as np
from math import floor, ceil, sqrt
import time



width, height = 4, 4
xpix, ypix = 2000, 1000
octaves = 1
octavesFactor = 4
count = 1
downpush = 0

horizontallyTileable = True
verticallyTileable = False
usebw = True

class Noise:
    class Octave:
        def __init__(self, xFrequency = 1, yFrequency = 1, amplitudeFactor = 1):
            self.xFrequency = xFrequency
            self.yFrequency = yFrequency
            self.amplitudeFactor = amplitudeFactor
            self.matrix = np.random.sample((xFrequency + 1, yFrequency + 1))
            self.p = np.zeros((4))
            self.d = np.zeros((4))
            if horizontallyTileable:
                for y in range(height + 1):
                    self.matrix[width, y] = self.matrix[0, y]
        
            if verticallyTileable:
                for x in range(width + 1):
                    self.matrix[x, height] = self.matrix[x, 0]
            
            
        def getValue(self, x, y):
            xs = floor(x)
            xm = ceil(x)
            ys = floor(y)
            ym = ceil(y)
            
            if(xs == xm):
                xm += 1
            if(ys == ym):
                ym += 1
            
            self.p[0] = self.matrix[xs,ys]
            self.p[1] = self.matrix[xs,ym]
            self.p[2] = self.matrix[xm,ys]
            self.p[3] = self.matrix[xm,ym]
            
            self.d[0] = sqrt((x-xs)**2 + (y-ys)**2) 
            self.d[1] = sqrt((x-xs)**2 + (y-ym)**2) 
            self.d[2] = sqrt((x-xm)**2 + (y-ys)**2) 
            self.d[3] = sqrt((x-xm)**2 + (y-ym)**2) 
            
            
            retval = 0
            for i in range(len(self.p)):
                retval += (max(1 - self.d[i], 0) * self.p[i])
            
            return retval * self.amplitudeFactor

    def __init__(self, seed, xFrequency = 1, yFrequency = 1, octaves = 0, amplitudeFactor = 1, ampliudeOffset = None, octavesFactor = 2):
        np.random.seed(seed)
        self.xFrequency = xFrequency
        self.yFrequency = yFrequency
        self.matrix = np.random.sample((width + 1, height + 1))
        self.octaves = octaves + 1
        self.amplitudeFactor = amplitudeFactor
        self.ampliudeOffset = ampliudeOffset if ampliudeOffset != None else amplitudeFactor * octaves * 0.1
        self.octavesFactor = octavesFactor
        
        self.octaveslist = [Noise.Octave(xFrequency = self.xFrequency * self.octavesFactor ** i, yFrequency = self.yFrequency * self.octavesFactor ** i, amplitudeFactor = self.amplitudeFactor ** i) for i in range(self.octaves)]
        
    def getValue(self,x,y):
        value = 0
        for i in range(self.octaves):
            value += self.octaveslist[i].getValue(x * self.octaveslist[i].xFrequency,y * self.octaveslist[i].yFrequency)
        return value + self.ampliudeOffset
            
            
    
def generate(seed):
    noise = Noise(seed, xFrequency = width, yFrequency = height, octaves = octaves, amplitudeFactor = 0.4,ampliudeOffset = -0.3, octavesFactor = octavesFactor)
    pixels = np.zeros((xpix,ypix))
    
    for i in range(xpix):
        print(i)
        for j in range(ypix):
            val=noise.getValue(i / xpix, j / ypix)
            pixels[i,j] = val
            
    
    map = Image.new( mode = "RGB", size = (xpix, ypix) )
    pxn = map.load()
    
    for x in range(xpix):
        print(x)
        for y in range(ypix):
            temp = pixels[x,y]
            if(temp > 0.95 + downpush):
                color = (255,255,255)
            elif temp > 0.8 + downpush:
                color = (80,80,80)
            elif temp > 0.75 + downpush:
                color = (60,60,60)
            elif temp > 0.6 + downpush:
                color = (32,160,32)
            elif temp > 0.55 + downpush:
                color = (32,200,32)
            elif temp > 0.5 + downpush:
                color = (245,245,200)
            elif temp > 0.4 + downpush:
                color = (128,128,255)
            elif temp > 0.3 + downpush:
                color = (64,128,255)
            elif temp > 0.2 + downpush:
                color = (0,128,255)
            elif temp > 0.1 + downpush:
                color = (0,0,255)
            elif temp > 0.01 + downpush:
                color = (0,0,128)
            else: 
                color = (0,0,0)
            pxn[x,y] = color
            if(usebw):
                pxn[x,y] = (int(temp * 255), int(temp * 255), int(temp * 255))
    
    map.show()
    map.save("generated_image_" + str(xpix) + "-" + str(ypix) + "-" + str(seed) + ".png")
    
for i in range(count):
    generate(i)