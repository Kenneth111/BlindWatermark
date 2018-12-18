from scipy.fftpack import dct, idct
import numpy as np
from PIL import Image
from utils import zigzag, reorderWatermark, restoreWatermark, centerCrop

MAX_DIM = 1040

def encoder(input_file, output_file, watermark_file, reorder_flag):
    img = Image.open(input_file)
    img = img.convert("L")
    img_w, img_h = img.size
    N = img_h
    if img_w < img_h:
        N = img_w
    if N > MAX_DIM:
        N = MAX_DIM
    # img = centerCrop(img_w, img_h, N, img)
    watermark = Image.open(watermark_file)
    watermark = watermark.convert("L")
    watermark_w, watermark_h = watermark.size
    if img_h * img_w < watermark_h * watermark_w:
        print("the size of the input file is smaller than that of the watermark file")
        return -1
    img_arr = np.array(img)
    water_arr = np.array(watermark)
    zigzag_seq = zigzag(N)
    x1 = np.zeros((1, int(N * N / 2)))
    x2 = np.zeros((1, int(N * N / 2)))
    for i in range(N):
        for j in range(N):
            idx = zigzag_seq[i, j] - 1
            if idx % 2 == 0:
                x1[0, int(idx / 2)] = img_arr[i, j]
            else:
                x2[0, int(idx / 2)] = img_arr[i, j]
    if reorder_flag:
        water_arr = reorderWatermark(water_arr)
    else:
        water_arr = water_arr.reshape(-1, )
    X1 = dct(x1, norm="ortho")
    X2 = dct(x2, norm="ortho")
    X1_ = np.copy(X1)
    X2_ = np.copy(X2)
    for i in range(0, water_arr.shape[0]):
        j = 0
        if water_arr[i] > 230:
            j = 1
        X1_[0, i] = (X1[0, i] + X2[0, i]) / 2 + j
        X2_[0, i] = (X1[0, i] + X2[0, i]) / 2 - j
    x1_ = idct(X1_, norm="ortho")
    x2_ = idct(X2_, norm="ortho")
    img_res = np.copy(img_arr)
    for i in range(N):
        for j in range(N):
            idx = zigzag_seq[i, j] - 1
            if idx % 2 == 0:
                img_res[i, j] = x1_[0, int(idx / 2)]
            else:
                img_res[i, j] = x2_[0, int(idx / 2)]
    img_res = img_res.astype("uint8")
    img_res = Image.fromarray(img_res)
    img_res.save(output_file)

def decoder(input_file, watermark_w, watermark_h, reorder_flag):
    img_res = Image.open(input_file)
    img_res = img_res.convert("L")
    img_w, img_h = img_res.size
    N = img_h
    if img_w < img_h:
        N = img_w    
    if N > MAX_DIM:
        N = MAX_DIM        
    img_res = np.array(img_res)
    zigzag_seq = zigzag(N)
    dx1 = np.zeros((1, int(N * N / 2)))
    dx2 = np.zeros((1, int(N * N / 2)))
    for i in range(N):
        for j in range(N):
            idx = zigzag_seq[i, j] - 1
            if idx % 2 == 0:
                dx1[0, int(idx / 2)] = img_res[i, j]
            else:
                dx2[0, int(idx / 2)] = img_res[i, j]
    dX1 = dct(dx1, norm="ortho")
    dX2 = dct(dx2, norm="ortho")
    watermark_res = np.zeros((1, watermark_w * watermark_h))
    for i in range(0, watermark_h * watermark_w):
        if dX1[0, i] - dX2[0, i] > 0:
            watermark_res[0, i] = 255
        else:
            watermark_res[0, i] = 0
    if reorder_flag:
        tmp_res = restoreWatermark(watermark_res)
    else:
        tmp_res = watermark_res
    watermark_res = tmp_res.reshape(watermark_h, -1).astype("uint8")
    img_water = Image.fromarray(watermark_res)
    img_water.show()