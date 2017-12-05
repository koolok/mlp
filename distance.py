#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 12:51:03 2017

@author: koolok
"""

from array import array
from collections import deque
import numpy as np

def pen_mat(a,b,c,d,e):
    tmp = deque([a,b,c,d,e,d,c,b])
    mat = np.zeros(shape=(8,8))
    for i_row in range(0,8):
        mat[i_row] = tmp
        tmp.rotate(1)
    return mat


#pen_mat = [[0,1,2,3,4,3,2,1],[1,0,1,2,3,4,3,2],[2,1,0,1,2,3,4,3],[3,2,1,0,1,2,3,4],[4,3,2,1,0,1,2,3],[3,4,3,2,1,0,1,2],[2,3,4,3,2,1,0,1],[1,2,3,4,3,2,1,0]]

pen_mat = pen_mat(0,1,2,3,4)
pen_add_suppr = 2

def distance(seq1, seq2, max_dist=-1):
    if seq1 == seq2:
        return 0

    seq1 = seq1.replace('#','')
    seq2 = seq2.replace('#','')

    len1, len2 = len(seq1), len(seq2)
    if max_dist >= 0 and abs(len1 - len2) > max_dist:
        return -1
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    if len1 < len2:
        len1, len2 = len2, len1
        seq1, seq2 = seq2, seq1

#    column = array('L', range(0,2*(len2 + 1),2))
    column = list(range(0,2*(len2 + 1),2))

    for x in range(1, len1 + 1):
        column[0] = x
        last = x - 1
        for y in range(1, len2 + 1):
            old = column[y]
            cost = pen_mat[ord(seq1[x - 1])-48][ord(seq2[y - 1])-48]
            column[y] = min(column[y] + 2, column[y - 1] + 2, last + int(cost))
            last = old
        if max_dist >= 0 and min(column) > max_dist:
            return -1

    if max_dist >= 0 and column[len2] > max_dist:
        return -1
    return column[len2]

def distance_(word1,word2) :
    word1 = word1.replace('#','')
    word2 = word2.replace('#','')

    dico = { (-1,-1):0 }

    for i,c_i in enumerate(word1) :
        dico[i,-1] = dico[i-1,-1]+pen_add_suppr
        dico[-1,i] = dico[-1,i-1]+pen_add_suppr
        for j,c_j in enumerate(word2) :
            c_i_int = ord(c_i) - ord('0')
            c_j_int = ord(c_j) - ord('0')
            """print(i,c_i,j,c_j)"""
            option = []
            if (i-1,j) in dico :
                x = dico[i-1,j]+pen_add_suppr
                option.append(x)
            if (i,j-1) in dico :
                x = dico[i,j-1]+pen_add_suppr
                option.append(x)
            if (i-1,j-1) in dico :
                x = dico[i-1,j-1] + pen_mat[c_i_int,c_j_int]
                option.append(x)
            dico[i,j] = min(option)
            """print(option)
            print(dist)
            print()"""
    return dico[len(word1)-1, len(word2)-1]
