import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image
from codec import encoder, decoder

reorder_flag = True
encoder("desktop.png", "encoded.bmp", "lsj.jpg", reorder_flag)
# encoder("f5.bmp", "encoded.bmp", "lsj.jpg", reorder_flag)
# encoder("lena_gray.png", "encoded.bmp", "lsj.jpg", reorder_flag)
decoder("encoded.bmp", reorder_flag)
