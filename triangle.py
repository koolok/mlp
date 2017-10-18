#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 12:55:54 2017

@author: koolok
"""

import numpy as np
import pickle 
import editdistance


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

for i in range(len(base)) :
    for j in range(len(base)) :
        if i != j :
            distance_matrix[i,j] = editdistance.eval(base[i],base[j])
    
file = open('distance_matrix.pk', 'wb') 

pickle.dump(distance_matrix, file) 
file.close()