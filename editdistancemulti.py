#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:29:21 2018

@author: koolok
"""

from editdistance import eval as editdistance
from picture2word import reduce

def edidistance_multi (seq1, seq2, label, max_dist=-1):
    return (label,editdistance(seq1,seq2),seq1)

def edidistance_multi_compress (seq1, seq2, label, max_dist=-1):
    if (len(seq1) < len(seq2)) :
        seq1 = reduce(seq1,len(seq2))
    else :
        seq2 = reduce(seq2,len(seq1))
    return (label,editdistance(seq1,seq2),seq1)

def edidistance_multi_compress_GUI (seq1, seq2, label, max_dist=-1) :
    sv_seq_1 = seq1
    if (len(seq1) < len(seq2)) :
        seq1 = reduce(seq1,len(seq2))
    else :
        seq2 = reduce(seq2,len(seq1))
    return (label,editdistance(seq1,seq2),sv_seq_1)    