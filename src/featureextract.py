from tkinter import Tk, Label

import numpy as np
import cv2
#from skimage import io
from skimage.feature import greycomatrix, greycoprops

def glcm_feat(path):
    x = cv2.imread(path)
    print(x.shape)
    if(len(x.shape)==3):
        x= x[:, : ,2]
    nir = x[:, : ]
    glcm = greycomatrix(x, [1], [np.pi/2], levels=256, normed=True, symmetric=True)

    li=[];
    # contrast’, ‘dissimilarity’, ‘homogeneity’, ‘energy’, ‘correlation’, ‘ASM’},
    li.append(greycoprops(glcm,prop='contrast')[0][0])
    li.append(greycoprops(glcm,prop='dissimilarity')[0][0])
    li.append(greycoprops(glcm,prop='homogeneity')[0][0])
    li.append(greycoprops(glcm,prop='energy')[0][0])
    li.append(greycoprops(glcm,prop='correlation')[0][0])
    li.append(greycoprops(glcm,prop='ASM')[0][0])


    return li
# print(glcm_feat('mribrainscan.jpg'))