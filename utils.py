from os.path import exists
import numpy as np

def zigzag(N):
    try:
        zz_mtx = np.zeros((N,N))
    except TypeError as err:
        print("N must be an integer, error msg: {0}".format(err))
        return -1
    except ValueError as err:
        print("N must be larger than 0, error msg: {0}".format(err))
        return -1
    for n in range(2,N+2):
        zz_mtx[n-2, 0] = 1/2*((-1)**n)*(n+((-1)**n)*((n-2)*n+2)-2)
    for i in range(1, N+1):
        for j in range(2, N+1):
            if ((i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1)):
                zz_mtx[i-1, j-1] = zz_mtx[i-1, j-2] + (2*i-1)
            else:
                zz_mtx[i-1, j-1] = zz_mtx[i-1, j-2] + (j-1)*2
    zz_mtx = np.fliplr(zz_mtx)
    for i in range(2, N+1):
        for j in range(1, N):
            if i > j:
                zz_mtx[i-1, j-1] = zz_mtx[i-1, j-1] - (i - j) ** 2
    zz_mtx = np.fliplr(zz_mtx)    
    return zz_mtx

#watermark_arr: m * n
def reorderWatermark(watermark_arr):
    watermark_arr = watermark_arr.reshape(-1,)
    N = watermark_arr.shape[0]
    if exists("permutation.npz"):
        per = np.load("permutation.npz")['arr_0']
    else:
        per = np.random.permutation(N)
        np.savez("permutation.npz", per)
    return watermark_arr[per.tolist()]

def restoreWatermark(tmp_watermark):
    per = np.load("permutation.npz")['arr_0']
    N = per.shape[0]
    tmp_res = np.zeros((1, N))
    for (i, order) in zip(per.tolist(), range(N)):
        tmp_res[0, i] = tmp_watermark[0, order]
    return tmp_res