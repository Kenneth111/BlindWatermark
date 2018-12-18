from scipy.fftpack import dct, idct
import numpy as np
from PIL import Image
from utils import zigzag, reorderWatermark

def encoder(input_file, output_file, watermark_file, reorder_flag):
    img = Image.open(input_file)
    img = img.convert("L")
    img_w, img_h = img.size
    N = img_h
    if img_w < img_h:
        N = img_w
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
    for i in range(100000, 120000):
        j = 0
        if water_arr[i - 100000] > 230:
            j = 1
        X1_[0, i] = (X1[0, i] + X2[0, i]) / 2 + j
        X2_[0, i] = (X1[0, i] + X2[0, i]) / 2 - j
    x1_ = idct(X1_, norm="ortho")
    x2_ = idct(X2_, norm="ortho")
    img_res = np.zeros(img_arr.shape)
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