from PIL import Image
import numpy as np
from math import floor, ceil, sqrt, atan




width, height = 10, 10
xpix, ypix = 100, 100
count = 3
bw=True
cl=True

class Noise:
    class Octave:
        def __init__(self, xFrequency = 1, yFrequency = 1, amplitudeFactor = 1):
            self.xFrequency = xFrequency
            self.yFrequency = yFrequency
            self.amplitudeFactor = amplitudeFactor
            self.matrix = np.random.sample((xFrequency + 1, yFrequency + 1))
            
            
        def getValue(self, x, y):
            xs = floor(x)
            xm = ceil(x)
            ys = floor(y)
            ym = ceil(y)
            
            if(xs == xm):
                xm += 1
            if(ys == ym):
                ym += 1
            
            p = np.zeros((4))
            p[0] = self.matrix[xs,ys]
            p[1] = self.matrix[xs,ym]
            p[2] = self.matrix[xm,ys]
            p[3] = self.matrix[xm,ym]
            
            d = np.zeros((4))
            d[0] = sqrt((x-xs)**2 + (y-ys)**2) 
            d[1] = sqrt((x-xs)**2 + (y-ym)**2) 
            d[2] = sqrt((x-xm)**2 + (y-ys)**2) 
            d[3] = sqrt((x-xm)**2 + (y-ym)**2) 
                
            radian_to_degree = 57.2958
            
            degreeFactor = np.zeros((4))
            degreeFactor[0] = (-abs(((abs(atan((y-ys)/(x-xs)) * radian_to_degree) % 90.0) - 45.0)/45.0))+1 if (x-xs) != 0 else 0
            degreeFactor[1] = (-abs(((abs(atan((y-ym)/(x-xs)) * radian_to_degree) % 90.0) - 45.0)/45.0))+1 if (x-xs) != 0 else 0
            degreeFactor[2] = (-abs(((abs(atan((y-ys)/(x-xm)) * radian_to_degree) % 90.0) - 45.0)/45.0))+1 if (x-xm) != 0 else 0
            degreeFactor[3] = (-abs(((abs(atan((y-ym)/(x-xm)) * radian_to_degree) % 90.0) - 45.0)/45.0))+1 if (x-xm) != 0 else 0
            print(degreeFactor[0]) if x - xs != 0 else x
            
            retval = 0
            for i in range(len(p)):
                retval += (max(1 + ((sqrt(2)-1) * degreeFactor[i]) - d[i], 0) * p[i])
            
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
    noise = Noise(seed, xFrequency = width, yFrequency = height, octaves = 0, amplitudeFactor = 0.33,ampliudeOffset = 0)
    pixels = np.zeros((ypix,xpix))
    
    for i in range(ypix):
        for j in range(xpix):
            val=noise.getValue(j / xpix, i / ypix)
            pixels[i,j] = val
            
    if(bw):
        map2 = Image.new( mode = "RGB", size = (xpix, ypix) )
        pxn2 = map2.load()
        for y in range(ypix):
            for x in range(xpix):
                temp = int(pixels[y,x] * 255)
                color = (temp,temp,temp)
                pxn2[y,x] = color
        map2.show()
    
    if(cl):
        map = Image.new( mode = "RGB", size = (xpix, ypix) )
        pxn = map.load()
    
        for y in range(ypix):
            for x in range(xpix):
                temp = pixels[y,x]
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
                elif temp > 0.01:
                    color = (0,0,128)
                else: 
                    color = (0,0,0)
                pxn[y,x] = color
        map.show()
        map.save("generated_image_" + str(xpix) + "-" + str(ypix) + "-" + str(seed) + ".png")
    
for i in range(count):
    generate(i)