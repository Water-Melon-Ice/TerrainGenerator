from perlin_noise import PerlinNoise
from PIL import Image
import numpy as np

xpix, ypix = 200, 200

pixels = np.zeros((ypix,xpix))

seed = 6

noise1 = PerlinNoise(octaves=3,seed = seed)
noise2 = PerlinNoise(octaves=6,seed = seed)
noise3 = PerlinNoise(octaves=12,seed = seed)
noise4 = PerlinNoise(octaves=24,seed = seed)
noise5 = PerlinNoise(octaves=48,seed = seed)
noise6 = PerlinNoise(octaves=48,seed = seed)

for i in range(ypix):
    for j in range(xpix):
        pixels[i,j] = noise1([i/xpix, j/ypix])
        pixels[i,j] += 0.5 * noise2([i/xpix, j/ypix])
        pixels[i,j] += 0.25 * noise3([i/xpix, j/ypix])
        pixels[i,j] += 0.125 * noise4([i/xpix, j/ypix])
        pixels[i,j] += 0.0625 * noise5([i/xpix, j/ypix])
        pixels[i,j] += 0.03125 * noise6([i/xpix, j/ypix])
        pixels[i,j] += 0.5
pic = Image.fromarray(pixels * 255)
#pic.show()

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
        else:
            color = (0,0,128)
        pxn[y,x] = color
map.show()
map.save("generated_image_" + str(xpix) + "-" + str(ypix) + "-" + str(seed) + ".png")