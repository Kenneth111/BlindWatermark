import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image
from utils import zigzag, restoreWatermark
from codec import encoder

reorder_flag = True
# encoder("f5.bmp", "encoded.bmp", "lsj.jpg", reorder_flag)
encoder("lena_gray.png", "encoded.bmp", "lsj.jpg", reorder_flag)

lena_res = Image.open("encoded.bmp")
lena_res = lena_res.convert("L")
lena_res = np.array(lena_res)
zigzag_seq = zigzag(512)
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
