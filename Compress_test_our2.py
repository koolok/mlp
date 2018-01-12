#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:38:10 2017

@author: koolok
"""

from picture2word import picture2word_multi_, reduce_multi
from multiprocessing import Pool
import Mnist
import random
import time
import analyse
import pickle as pk
from sklearn.model_selection import KFold
import numpy as np



def test_vs (images_base,images_labels,word_test,word_test_label) :
    test_set_size = len(word_test)
    # Test uncompress
    pool = Pool()
    
#    results = pool.starmap_async(picture2word_multi_, zip(images_base,images_labels)).get()
#        
#    results = list(zip(*results))

    base = images_base
    base_labels = images_labels
        
#    results = pool.starmap_async(reduce_multi, zip(word_test,word_test_label)).get()
#    
#    pool.close()
#    
#    results = list(zip(*results))

    test_set = word_test
    test_set_labels = word_test_label
    
    
    miss_classified = 0
    start = time.time()
    for i in range(len(test_set)) :
        word = test_set[i]
        
        digit = analyse.edit_analyse_multi(word,base,base_labels,k=3)
                
        if (digit != test_set_labels[i]) :
            miss_classified += 1
            
    processing_time = (time.time() - start) / test_set_size
    accuracy = ((test_set_size - miss_classified) / test_set_size) * 100
    
    print("Uncompress : processing time=", processing_time," accuracy=",accuracy)


    # Test compress 
    
#    pool = Pool()
#    
#    results = pool.starmap_async(picture2word_multi_, zip(images_base,images_labels)).get()
#        
#    results = list(zip(*results))

    base = images_base
    base_labels = images_labels
        
    results = pool.starmap_async(reduce_multi, zip(word_test,word_test_label)).get()
    
    pool.close()
    
    results = list(zip(*results))

    test_set = results[0]
    test_set_labels = results[1]
    
    
    miss_classified = 0
    start = time.time()
    for i in range(len(test_set)) :
        word = test_set[i]
        
        digit = analyse.edit_analyse_multi(word,base,base_labels,k=3)
                
        if (digit != test_set_labels[i]) :
            miss_classified += 1
            
    processing_time = (time.time() - start) / test_set_size
    accuracy_cp = ((test_set_size - miss_classified) / test_set_size) * 100
    
    print("Compress : processing time=", processing_time," accuracy=",accuracy_cp)

    return accuracy,accuracy_cp

def generate_sets (training_set_size=1000, test_set_size=100):
    train_images, train_labels, test_images, test_labels = Mnist.load_mnist()
    
    # Generate training set
    indices = list(range(len(train_images)))  # Or just range(len(a)) in Python 2
    random.shuffle(indices)
    
    Images_base = []
    Images_labels = []
    
    
    i = 0
    while (i<len(indices)) :
        images_base = []
        images_labels = []
        
        max_ref = [training_set_size//10] * 10
            
        i = 0
        while len(images_base) < training_set_size and i < len(indices) :
            if max_ref[train_labels[i]] > 0 :
                images_base.append(train_images[indices[i]])
                images_labels.append(train_labels[indices[i]])
                max_ref[train_labels[i]] -= 1
                indices.pop(i)
            else :
                i += 1
                
        if (len(images_base)>= training_set_size):
            Images_base.append(images_base)
            Images_labels.append(images_labels)
        
        
    # Generate test set
    indices = list(range(len(test_images)))
    random.shuffle(indices)
    
    Images_test = []
    Images_test_labels= []
    
    while ( len(indices) >= test_set_size) :
        images_test = []
        images_test_labels= []
        
        while len(images_test) < test_set_size :
            images_test.append(test_images[indices[0]])
            images_test_labels.append(test_labels[indices[0]])
            indices.pop(0)
            
        Images_test.append(images_test)
        Images_test_labels.append(images_test_labels)
        
        
    return Images_base, Images_labels, Images_test, Images_test_labels
        
    
        
        

def multi_test (nb_run=100) :    
    Images_base = []
    Images_labels = []
    Images_test = []
    Images_test_labels = []
    
    accuracy = 0
    accuracy_cp = 0
    
    file_base = open('ourbase.pk', 'rb')
    base = np.array(pk.load(file_base))
    file_base.close()
   
    file_labels = open('ourlabel.pk', 'rb')
    base_label = np.array(pk.load(file_labels))
    file_labels.close()
    
    
    kf = KFold(n_splits=10, shuffle=True)
    
    
    for train_index, test_index in kf.split(base):
        Images_base, Images_test = base[train_index], base[test_index]
        Images_labels, Images_test_labels = base_label[train_index], base_label[test_index]        
        
        accuracy_tmp, accuracy_cp_tmp = test_vs(Images_base, Images_labels, Images_test, Images_test_labels)
        
        nb_run += 1
        accuracy += accuracy_tmp
        accuracy_cp += accuracy_cp_tmp
        
    accuracy /= 10
    accuracy_cp /= 10
        
    print("Uncompress : ",accuracy," Compress : ",accuracy_cp)    
        
        




multi_test()













