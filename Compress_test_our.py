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



def test_vs (images_base,images_labels,word_test,word_test_label) :
    test_set_size = len(word_test)
    # Test uncompress
    pool = Pool()
    
    results = pool.starmap_async(picture2word_multi_, zip(images_base,images_labels)).get()
        
    results = list(zip(*results))

    base = results[0]
    base_labels = results[1]
        
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
    
    pool = Pool()
    
    results = pool.starmap_async(picture2word_multi_, zip(images_base,images_labels)).get()
        
    results = list(zip(*results))

    base = results[0]
    base_labels = results[1]
        
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
    
    Images_base, Images_labels, Images_test, Images_test_labels = generate_sets (training_set_size=1000, test_set_size=100)
    
    accuracy = 0
    accuracy_cp = 0
    
    sqrt_run = int(nb_run**(1/2))
    
    Images_base = Images_base[0:sqrt_run]
    Images_labels = Images_labels[0:sqrt_run]
    Images_test = Images_test[0:sqrt_run]
    Images_test_labels = Images_test_labels[0:sqrt_run]
    
    file_base = open('ourbase.pk', 'rb')
    word_test = pk.load(file_base)
    file_base.close()
   
    file_labels = open('ourlabel.pk', 'rb')
    word_test_label = pk.load(file_labels)
    file_labels.close()
    
    
    
    nb_run = 0
    
    for i in range(len(Images_base)) :
        
        print("Run : ",nb_run)
        
        accuracy_tmp, accuracy_cp_tmp = test_vs(Images_base[i], Images_labels[i], word_test, word_test_label)
        
        nb_run += 1
        accuracy += accuracy_tmp
        accuracy_cp += accuracy_cp_tmp
        
    accuracy /= nb_run 
    accuracy_cp /= nb_run
        
    print("Uncompress : ",accuracy," Compress : ",accuracy_cp)



multi_test()













