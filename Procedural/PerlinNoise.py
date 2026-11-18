# Perlin Noise function implemented in Python, Made 2 years ago
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image
resolutionx = 240
resolutiony = 240
spacing = 60
''''
def lightercolor(x):
    return(255 / (1 - math.exp(-(x/127) + 2)))
def darkercolor(x):
    return(255 / (1 + math.exp(-(x/127) + 2)))
'''
def terrain_grad(x):
    color_stops = [
        "hsla(150, 6%, 37%, 1)",  
        "hsla(95, 58%, 59%, 1)",   
        "hsla(124, 64%, 53%, 1)",  
        "hsla(182, 70%, 55%, 1)",  
        "hsla(250, 100%, 47%, 1)"   
    ]
    positions = [0, 0.22, 0.47, 0.73, 1]
    if x <= positions[0]:
      start_color = color_stops[0]
      end_color = color_stops[0]
      start_pos = positions[0]
      end_pos = positions[0]
    elif x <= positions[1]:
      start_color = color_stops[0]
      end_color = color_stops[1]
      start_pos = positions[0]
      end_pos = positions[1]
    elif x <= positions[2]:
        start_color = color_stops[1]
        end_color = color_stops[2]
        start_pos = positions[1]
        end_pos = positions[2]
    elif x <= positions[3]:
        start_color = color_stops[2]
        end_color = color_stops[3]
        start_pos = positions[2]
        end_pos = positions[3]
    elif x <= positions[4]:
        start_color = color_stops[3]
        end_color = color_stops[4]
        start_pos = positions[3]
        end_pos = positions[4]
    else:
        start_color = color_stops[4]
        end_color = color_stops[4]
        start_pos = positions[4]
        end_pos = positions[4]
    gradient_string = f"linear-gradient(90deg, {start_color} {start_pos * 100}%, {end_color} {end_pos * 100}%)"

    return gradient_string


def normalize_vecs(array):  
    for i in range(len(array)):
        for j in range(len(array[i])):
            magnitude = math.sqrt((array[i][j][0]**2) + (array[i][j][1]**2))
            array[i][j] = array[i][j] / magnitude
    return array
def fade_curve(t):
    return((6*(t**5)) - (15*(t**4)) + (10 * t**3)) 
def lerp(a, b, t):
    return((a * (1-t)) + (b * t))
def init_vectors(dimx, dimy, vector1, vector2):
    for i in range(dimx):
        for j in range(dimy):
            if np.random.rand(1, 1) < 0.5:
                vector1.append([-1 * (np.random.rand(1, 1))])
            else:     
                vector1.append([(np.random.rand(1, 1))])
            if np.random.rand(1, 1) < 0.5:
                vector2.append([-1 * (np.random.rand(1, 1))])
            else:     
                vector2.append([(np.random.rand(1, 1))])
def perlin_noise(resolutionx, resolutiony, spacing, amplitude):
    dimx=int(resolutionx/spacing + 1)
    dimy=int(resolutiony/spacing + 1)   
    vecsdim1 = []
    vecsdim2 = []
    output_array = np.zeros((resolutionx, resolutiony))
    init_vectors(dimx, dimy, vecsdim1, vecsdim2)
    vecsdim1 = np.array(vecsdim1)
    vecsdim2 = np.array(vecsdim2)
    vecsdim1.shape = (dimx, dimy)
    vecsdim2.shape = (dimx, dimy)
    vectors = np.dstack((vecsdim1, vecsdim2))

    vectors = normalize_vecs(vectors)
    for x in range(resolutionx):
        for y in range(resolutiony):
            tlcell = [(x // spacing), (y // spacing)]
            trcell = [tlcell[0] + 1, tlcell[1]]
            blcell = [tlcell[0], tlcell[1]+1]
            brcell = [blcell[0] + 1, blcell[1]]
            local_x = (x % spacing) / spacing
            local_y = (y % spacing) / spacing
            tl_v = vectors[tlcell[0]][tlcell[1]]
            tr_v = vectors[trcell[0]][trcell[1]]
            bl_v = vectors[blcell[0]][blcell[1]]
            br_v = vectors[brcell[0]][brcell[1]]
            local_tl_dist = np.array((local_x, local_y))
            local_tr_dist = np.array((local_x - 1, local_y))
            local_bl_dist = np.array((local_x, local_y - 1))
            local_br_dist = np.array((local_x - 1, local_y - 1))
            dp_tl = np.dot(tl_v, local_tl_dist.T)
            dp_tr = np.dot(tr_v, local_tr_dist.T)    
            dp_bl = np.dot(bl_v, local_bl_dist.T) 
            dp_br = np.dot(br_v, local_br_dist.T) 
            fade_x = fade_curve(local_x)
            fade_y = fade_curve(local_y)
            interp_top = lerp(dp_tl, dp_tr, fade_x)
            interp_bottom = lerp(dp_bl, dp_br, fade_x)
            pixel_value = lerp(interp_top, interp_bottom, fade_y)
            output_array[x][y] = pixel_value 
    return(output_array * amplitude)



#frac_output_array = np.array((perlin_noise(400, 400, 5, 0.125) + perlin_noise(400, 400, 100, 0.25) + perlin_noise(400, 400, 20, 0.5)  + perlin_noise(400, 400, 40, 1) + perlin_noise(400, 400, 80, 2)), dtype=object)
frac_output_array = np.array(perlin_noise(400, 400, 80, 2), dtype=object)
min = np.min(frac_output_array) - 0.05
max = np.max(frac_output_array) + 0.05
norm_output_array = ((frac_output_array - min) / (max - min) * 150) 

for i in range(len(norm_output_array)):
    for j in range(len(norm_output_array[i])):
        norm_output_array[i][j] = (norm_output_array[i][j])
        if norm_output_array[i][j] >= 200:
            norm_output_array[i][j] = [255, 0, 0]
norm_output_array = norm_output_array.astype(np.uint8)
curr_noise_image = Image.fromarray(norm_output_array)
curr_noise_image.show()
save = input("Would you like to save this image? Reply Y for yes and N for no:")
filename = input("Please type the name of the file to save the image to. Do not include the file format:")
curr_noise_image.save(str(filename)+".jpg")
print("img saved")
