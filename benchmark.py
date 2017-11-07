#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:15:18 2017

@author: koolok
"""

 
import numpy as np
import pickle 
from distance import distance
import time
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

n = 0

starting_point_proc = time.clock()

for i in range(len(base)) :
    for j in range(len(base)) :
        if i != j :
            n +=1
            distance_matrix[i,j] = distance(base[i],base[j])
      
total_time = time.clock() - starting_point_proc

print("Our distance : average time execution : ", total_time / n)

#------------------------------------------

n = 0

starting_point_proc = time.clock()

for i in range(len(base)) :
    for j in range(len(base)) :
        if i != j :
            n +=1
            distance_matrix[i,j] = editdistance.eval(base[i],base[j])
      
total_time = time.clock() - starting_point_proc

print("Module editdistance : average time execution : ", total_time / n)

