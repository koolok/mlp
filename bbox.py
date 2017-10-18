#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 14:46:00 2017

@author: jmarnat
"""

from PIL import Image
import numpy as np
from scipy.ndimage.interpolation import zoom
import matplotlib.pyplot as plt


img = Image.open('9.png')
img_ar = np.asarray(img.convert('L'))

px, py = np.where(img_ar == 0)

x_min = px.min()
y_min = py.min()
x_max = px.max()
y_max = py.max()

delta_x = x_max - x_min
delta_y = y_max - y_min

if (delta_x > 50 or delta_y > 50):
    # zooming by .5
    img_new = np.ones([100,100])*255
    img_new[25:75,25:75] = zoom(img_ar,zoom=0.5,order=0,mode='wrap')
    #TODO add img_new
    
    for x in range(len(img_new)):
        for y in range(len(img_new[0])):
            if img_new[x,y] < 255:
                img_new[x,y] = 0
                
    Image.fromarray(np.uint8(img_new)).save('new2.png')
    
    
  
elif (delta_x < 50 and delta_y < 50):
    # zooming by 2
    mid_x = x_max - delta_x/2
    mid_y = y_max - delta_y/2
    
    img_new2 = zoom(img_new,zoom=2,order=0,mode='nearest')
    img_bb = img_new2[2*x_min:2*x_max,2*y_min:2*y_max]
    
    img_new = np.ones([100,100])*255
    img_new[0:len(img_bb),0:len(img_bb[0])] = img_bb
    
    Image.fromarray(np.uint8(img_new)).save('new2.png')
    #TODO add img_new















