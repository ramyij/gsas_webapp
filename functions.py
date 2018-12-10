import os, re
import numpy as np
import pandas as pd
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pylab


basepath = "Images"
# basepath = "/home/khalana/GitRepos/Capstone_local/Images"

# This function transforms cartesian coordinates to polar. X is the image (has to be array)

def threshold_image(img,threshold_val=100, alpha=80, beta=100):
    """
    only keeps pixel values over "threshold_val". This helps tremendously in finding the wrinkles, and allows us to choose smaller n_cluster
    """
#     timg = np.asarray(img)
    a = img.mean(axis=2) < alpha
    b = img.max(axis=2) > beta
    fil = a*b
    out = fil * img.max(axis=2)
    return out


def plot_wrinkle_class(image_arr,og_filename):
    image = Image.fromarray(image_arr)
    plt.figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
    plt.imshow(image)

    filename = 'static/results/%s_wrinkle.png' % og_filename.split('/')[-1].split('.')[0]
    pylab.savefig(filename,bbox_inches='tight')


def bf_size(image, threshold_val=30):
    a = image.max(axis=2)
    tmp = a > threshold_val
    tmp_im = a * tmp
    return int(np.count_nonzero(tmp_im))

def perc_wrinkled(img, biofilm_size):
    return round(np.count_nonzero(img)/biofilm_size,4)

def process_image(img_path, resize = (128,128), threshold_1 = 20, alpha=80, beta=100):
    img = Image.open(img_path, mode='r')
    if resize is not None:
        img = img.resize(resize)
    img_arr = np.array(img).astype('uint8')
    bf_s = bf_size(img_arr,threshold_1)
    processed_image = threshold_image(img_arr, alpha=alpha, beta=beta)
    perc_wrinkle = perc_wrinkled(processed_image, biofilm_size=bf_s)
    return processed_image, perc_wrinkle