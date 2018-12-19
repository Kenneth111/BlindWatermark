import numpy as np
from PIL import Image
from utils import dct2, idct2, binarizeImg

BLOCK_SIZE = 8
Q = 12

def encoder(input_file, output_file, watermark_file):
    img = Image.open(input_file)
    img = img.convert("L")
    img_w, img_h = img.size
    img_arr = np.array(img)

    watermark = Image.open(watermark_file)
    watermark = watermark.convert("L")
    water_w, water_h = watermark.size
    water_arr = binarizeImg(watermark).reshape(-1)

    col_num = int(img_w / BLOCK_SIZE)
    for block_id, w in enumerate(water_arr):
        x = block_id % col_num
        y = int(block_id / col_num)
        startY = y * BLOCK_SIZE
        endY = (y + 1) * BLOCK_SIZE
        startX = x * BLOCK_SIZE
        endX = (x + 1) * BLOCK_SIZE
        tmp_dct = dct2(img_arr[startY:endY, startX:endX])
        tmp_dc = np.round(tmp_dct[0, 0] / Q)
        if (tmp_dc + water_arr[block_id]) % 2 == 1:
            new_dc = (tmp_dc - 0.5) * Q
        else:
            new_dc = (tmp_dc + 0.5) * Q
        tmp_dct[0, 0] = new_dc
        img_arr[startY:endY, startX:endX] = idct2(tmp_dct).clip(0, 255).astype("uint8")        
    new_img = Image.fromarray(img_arr)
    new_img.save(output_file)

def decoder(input_file, watermark_file, water_w, water_h):
    img = Image.open(input_file)
    img = img.convert("L")
    img_w, img_h = img.size
    img_arr = np.array(img)
    col_num = int(img_w / BLOCK_SIZE)

    length = water_w * water_h
    watermark = np.zeros((1, length))
    for block_id in range(length):
        x = block_id % col_num
        y = int(block_id / col_num)
        startY = y * BLOCK_SIZE
        endY = (y + 1) * BLOCK_SIZE
        startX = x * BLOCK_SIZE
        endX = (x + 1) * BLOCK_SIZE
        tmp_dct = dct2(img_arr[startY:endY, startX:endX])
        tmp_dc = int(tmp_dct[0, 0] / Q)
        if tmp_dc % 2 == 1:
            watermark[0, block_id] = 1
        else:
            watermark[0, block_id] = 0
    watermark *= 255
    watermark = watermark.reshape(water_h, water_w).astype("uint8")
    img_water = Image.fromarray(watermark)
    img_water.save(watermark_file)
    