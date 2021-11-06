import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from skimage.measure import label, regionprops

def lakes_and_bays(image):
    b = ~image
    lb = label(b)
    regs = regionprops(lb)
    count_lakes = 0
    count_bays = 0
    for reg in regs:
        on_bound = False
        for y, x in reg.coords:
            if y == 0 or x == 0 or y == image.shape[0] - 1 or x == image.shape[1] - 1:
                on_bound = True
                break
        if not on_bound:
            count_lakes += 1
        else:
            count_bays += 1
    return count_lakes, count_bays

def has_vline(region):
    lines = np.sum(region.image, 0) // region.image.shape[0]
    return 1 in lines

def recognize(region):
    if np.all(region.image):
        return "-"
    lakes_image, bays_image = lakes_and_bays(region.image)
    if lakes_image == 2:
        if has_vline(region):
            return "B"
        else:
            return "8"
    if lakes_image == 1:
        #P - 1 lake, 2 bays
        #D - 1 lake, 2 bays (same)
        if bays_image == 2:
            cy = region.image.shape[0]//2
            cx = region.image.shape[1]//2 
            if region.image[cy, cx] > 0:    #check central pixel
                return "P"                  #if > 0 -> P
            else:
                return "D"                  #else -> D
        elif bays_image == 3:
            return "A"
        else:
            return "0"
    if lakes_image == 0:
        if has_vline(region):
            return "1"
        if bays_image == 2:
            return "/"
        _, cut_cb = lakes_and_bays(region.image[2:-2, 2:-2])
        if cut_cb == 4:
            return "X"
        if cut_cb == 5:
            cy = region.image.shape[0]//2
            cx = region.image.shape[1]//2
            if region.image[cy, cx] > 0:
                return "*"
            return "W"

    return None

image = plt.imread("imgs/symbols.png")
binary = np.sum(image, 2)
binary[binary > 0] = 1

labeled = label(binary)

#print(np.max(labeled))

regions = regionprops(labeled)

d = defaultdict(lambda : 0)
for region in regions:
    symbol = recognize(region)
    d[symbol] += 1

print(d)    
print(round((1 - d[None] / sum(d.values())) * 100, 2), '% определения', sep='')

#print(sum(d.values()))

#print(lakes_and_bays(regions[177].image))

# plt.imshow(labeled, cmap="gray")
# plt.show()