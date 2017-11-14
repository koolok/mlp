#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 12:55:54 2017

@author: koolok
"""

import numpy as np
import pickle 
from distance import distance
from multiprocessing import Pool


def init() :
    try :
        data = open("data.txt", "r", encoding="utf-8")
        base = []
        for line in data :
            digit,word = line.split("/")
            base.append(word[0:-1])
        data.close()
    except :
        base = []
    return base 

base = init()

distance_matrix = np.zeros((len(base),len(base)))
         
length = len(base)
pool = Pool()
for i in range(length) :
    word = base[0]
    
    base.pop(0)
    
    all_distance = pool.starmap_async(distance, zip(base,[word]*len(base))).get()
    
    k = 0
    for j in range(i+1,length) :
        distance_matrix[i][j] = distance_matrix[j][i] = all_distance[k]
        k += 1    
    
file = open('distance_matrix.pk', 'wb') 

pickle.dump(distance_matrix, file) 
file.close()