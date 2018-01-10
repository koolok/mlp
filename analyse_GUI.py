#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:32:28 2017

@author: koolok
"""

from multiprocessing import Pool
from distanceC import distance_multi_GUI

def analyse_multi(word,base,label,k=1) :
    if len(base) == 0 :
        return -1
    if len(base) == 1 :
        return label[0]
        
    pool = Pool()
    
    all_distance = pool.starmap_async(distance_multi_GUI, zip(base,[word]*len(base),label)).get()
    
    pool.close()

#    all_distance = dict(zip(label, all_distance))
#    
#    all_distance = sorted(label, key=all_distance.__getitem__)

    all_distance = sorted(all_distance, key=lambda tup: tup[1])
    
    votes = [0]*10
    
    Nearest = []
    for i in range(k):
        votes[all_distance[i][0]] +=1
        Nearest.append(all_distance[i][2])
    
    if max(votes) == 1 :
        return word, all_distance[0][0], Nearest
    return word, votes.index(max(votes)), Nearest
