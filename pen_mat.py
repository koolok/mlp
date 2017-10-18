#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:40:51 2017

@author: jmarnat
"""


# =============================================================================
# penalty matrix
# =============================================================================

import numpy as np
from collections import deque

def pen_mat(a,b,c,d,e):
    tmp = deque([a,b,c,d,e,d,c,b])
    mat = np.zeros(shape=(8,8))
    for i_row in range(0,8):
        mat[i_row] = tmp
        tmp.rotate(1)
    return mat
    
    
print(pen_mat(1.0,1.2,1.4,1.8,2))




# =============================================================================
# traning create a smaller version
# =============================================================================


