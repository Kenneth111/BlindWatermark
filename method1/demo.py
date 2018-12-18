import os
import numpy as np
from codec import encoder, decoder

reorder_flag = True
encoder("lena_gray.png", "encoded.bmp", "lsj.jpg", reorder_flag)
decoder("encoded.bmp", 200, 100, reorder_flag)
