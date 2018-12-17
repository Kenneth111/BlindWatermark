import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image
from utils import zigzag, reorderWatermark, restoreWatermark

reorder_flag = True
lena = Image.open("lena_gray.png")
lena = lena.convert("L")
watermark = Image.open("lsj.jpg")
watermark = watermark.convert("L")
lena_arr = np.array(lena)
water_arr = np.array(watermark)
zigzag_seq = zigzag(512)
x1 = np.zeros((1, int(512 * 512 / 2)))
x2 = np.zeros((1, int(512 * 512 / 2)))
for i in range(512):
    for j in range(512):
        idx = zigzag_seq[i, j] - 1
        if idx % 2 == 0:
            x1[0, int(idx / 2)] = lena_arr[i, j]
        else:
            x2[0, int(idx / 2)] = lena_arr[i, j]
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
lena_res = np.zeros(lena_arr.shape)
for i in range(512):
    for j in range(512):
        idx = zigzag_seq[i, j] - 1
        if idx % 2 == 0:
            lena_res[i, j] = x1_[0, int(idx / 2)]
        else:
            lena_res[i, j] = x2_[0, int(idx / 2)]
lena_res = lena_res.astype("uint8")
img_res = Image.fromarray(lena_res)
img_res.save("encoded.bmp")

dx1 = np.zeros((1, int(512 * 512 / 2)))
dx2 = np.zeros((1, int(512 * 512 / 2)))
for i in range(512):
    for j in range(512):
        idx = zigzag_seq[i, j] - 1
        if idx % 2 == 0:
            dx1[0, int(idx / 2)] = lena_res[i, j]
        else:
            dx2[0, int(idx / 2)] = lena_res[i, j]
dX1 = dct(dx1, norm="ortho")
dX2 = dct(dx2, norm="ortho")
watermark_res = np.zeros((1, 20000))
for i in range(100000, 120000):
    if dX1[0, i] - dX2[0, i] > 0:
        watermark_res[0, i - 100000] = 255
    else:
        watermark_res[0, i - 100000] = 0
if reorder_flag:
    tmp_res = restoreWatermark(watermark_res)
else:
    tmp_res = watermark_res
watermark_res = tmp_res.reshape(100, -1).astype("uint8")
img_water = Image.fromarray(watermark_res)
img_water.show()
