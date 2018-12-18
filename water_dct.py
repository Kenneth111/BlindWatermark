import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image
from codec import encoder, decoder

reorder_flag = True
encoder("lena_gray.png", "encoded.bmp", "lsj.jpg", reorder_flag)
decoder("encoded.bmp", 200, 100, reorder_flag)
