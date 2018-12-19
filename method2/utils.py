import numpy as np
from scipy.fftpack import dct, idct

def dct2(a):
    return dct( dct( a, axis=0, norm='ortho' ), axis=1, norm='ortho' )

def idct2(a):
    return idct( idct( a, axis=0 , norm='ortho'), axis=1 , norm='ortho')

def binarizeImg(img):
    threshold = 200
    table = []
    for  i  in  range( 256 ):
        if  i < threshold:
            table.append(0)
        else:
            table.append(1)
    tmp_img = img.point(table)
    return np.array(tmp_img)