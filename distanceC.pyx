#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:39:44 2017

@author: koolok
"""
from cpython cimport array
import array


cpdef int distance(str seq1, str seq2, int max_dist=-1):
    if seq1 == seq2:
        return 0
#
#    cdef char *seq1
#    cdef char *seq2
    
    seq1 = seq1.replace('#','')
    seq2 = seq2.replace('#','')
    
    cdef int len1
    cdef int len2
    
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

#    cdef array.array a = array.array('i', list(range(0,2*(len2 + 1),2)))
#    cdef int[:] column = a

    cdef list column
    column = list(range(0,2*(len2 + 1),2))
    
#    cdef array.array b = array.array('i', [[0,1,2,3,4,3,2,1],[1,0,1,2,3,4,3,2],[2,1,0,1,2,3,4,3],[3,2,1,0,1,2,3,4],[4,3,2,1,0,1,2,3],[3,4,3,2,1,0,1,2],[2,3,4,3,2,1,0,1],[1,2,3,4,3,2,1,0]])
#    cdef int[:] pen_mat = b

    cdef list pen_mat
    pen_mat = [[0,1,2,3,4,3,2,1],[1,0,1,2,3,4,3,2],[2,1,0,1,2,3,4,3],[3,2,1,0,1,2,3,4],[4,3,2,1,0,1,2,3],[3,4,3,2,1,0,1,2],[2,3,4,3,2,1,0,1],[1,2,3,4,3,2,1,0]]


    cdef int x
    cdef int y
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