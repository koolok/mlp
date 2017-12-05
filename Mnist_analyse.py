#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 20:37:41 2017

@author: koolok
"""

from picture2word import picture2word
import numpy as np
import pickle 
from editdistance import eval as editdistance
from distanceC import distance
from multiprocessing import Pool
import Mnist
import os
import random
import analyse
import time


# Pickelize the Mnist database
def init_base() :
    if ( os.path.isfile("base_mnist.pk") and os.path.isfile("base_mnist_labels.pk") ) :
        file_base = open("base_mnist.pk", 'rb') 
        base = pickle.load(file_base) 
        file_base.close()
        
        file_train_images = open("base_mnist_labels.pk", 'rb') 
        train_labels = pickle.load(file_train_images) 
        file_train_images.close()
        
    else :
        
        train_images, train_labels, test_images, test_labels = Mnist.load_mnist()
        
        base = []
        
        pool = Pool()
        
        base = pool.map_async(picture2word, train_images).get()
        
        file = open('base_mnist.pk', 'wb') 
    
        pickle.dump(base, file) 
        file.close()
        
        file = open('base_mnist_labels.pk', 'wb') 
    
        pickle.dump(train_labels, file) 
        file.close()
        
    return base, train_labels

# Calculate the distances matrix :
#    The first one whit our edit-distance function
#    The second one with the editdistance function from the package editdistance
def pickle_matrix(number_of_sample=1000) :
    
    base, train_labels = init_base()    
    
    indices = list(range(len(base)))  # Or just range(len(a)) in Python 2
    random.shuffle(indices)
    indices = indices[0:number_of_sample]
    
    sub_base = []
    sub_labels = []
    
    for indice in indices :
        sub_base.append(base[indice])
        sub_labels.append(train_labels[indice])
        
    name = 'base_mnist_'+str(number_of_sample)+'.pk'
    file = open(name, 'wb') 

    pickle.dump(sub_base, file) 
    file.close()
    
    name = 'base_mnist_labels'+str(number_of_sample)+'.pk'
    file = open(name, 'wb') 

    pickle.dump(sub_labels, file) 
    file.close()
    
    sv_sub_base = sub_base
             
#==============================================================================
# Calculate distance matrix with our distance function    
#==============================================================================
    distance_matrix = np.zeros((number_of_sample,number_of_sample))
    length = len(sub_base)
    pool = Pool()
    start = time.time()
    for i in range(length) :
#        for j in range(i+1,length) :
#            print(i,j)
#            print(sub_base[i])
#            print(sub_base[j])
#            
#            distance_matrix[i,j] = distance_matrix[j,i] = distance(sub_base[i],sub_base[j])
        
        
        word = sub_base[0]
        
        sub_base.pop(0)
        
        all_distance = pool.starmap_async(distance, zip(sub_base,[word]*len(sub_base))).get()
        
        
        k = 0
        for j in range(i+1,length) :
            distance_matrix[i,j] = distance_matrix[j,i] = all_distance[k]
            k += 1    
        
    processing_time_distance = time.time() - start
    
    print("Processing time to compute the distance matrix whit our distance function: ",processing_time_distance)
    
    name = 'distance_matrix_mnist'+str(number_of_sample)+'.pk'
    file = open(name, 'wb') 
    
    pickle.dump(distance_matrix, file) 
    file.close()

#==============================================================================
# Calculate distance matrix with editdistance function
#==============================================================================
    distance_matrix = np.zeros((number_of_sample,number_of_sample))
    sub_base = sv_sub_base
    length = len(sub_base)
    pool = Pool()
    start = time.time()
    for i in range(length) :
#        for j in range(i+1,length) :
#            print(i,j)
#            print(sub_base[i])
#            print(sub_base[j])
#            
#            distance_matrix[i,j] = distance_matrix[j,i] = distance(sub_base[i],sub_base[j])
        
        
        word = sub_base[0]
        
        sub_base.pop(0)
        
        all_distance = pool.starmap_async(editdistance, zip(sub_base,[word]*len(sub_base))).get()
        
        
        k = 0
        for j in range(i+1,length) :
            distance_matrix[i,j] = distance_matrix[j,i] = all_distance[k]
            k += 1    
        
    processing_time_editdistance = time.time() - start
    
    print("Processing time to compute the distance matrix whit editdistance function: ",processing_time_editdistance)

    
    name = 'editdistance_matrix_mnist'+str(number_of_sample)+'.pk'
    file = open(name, 'wb') 
    
    pickle.dump(distance_matrix, file) 
    file.close()

    return processing_time_distance, processing_time_editdistance

def pickle_matrix_editdistance_only(number_of_sample=1000) :
    
    base, train_labels = init_base()    
    
    indices = list(range(len(base)))  # Or just range(len(a)) in Python 2
    random.shuffle(indices)
    indices = indices[0:number_of_sample]
    
    sub_base = []
    sub_labels = []
    
    for indice in indices :
        sub_base.append(base[indice])
        sub_labels.append(train_labels[indice])
        
    name = 'base_mnist_'+str(number_of_sample)+'.pk'
    file = open(name, 'wb') 

    pickle.dump(sub_base, file) 
    file.close()
    
    name = 'base_mnist_labels'+str(number_of_sample)+'.pk'
    file = open(name, 'wb') 

    pickle.dump(sub_labels, file) 
    file.close()
        
    distance_matrix = np.zeros((number_of_sample,number_of_sample))
    length = len(sub_base)
    pool = Pool()
    start = time.time()
    for i in range(length) :
        
        word = sub_base[0]
        
        sub_base.pop(0)
        
        all_distance = pool.starmap_async(editdistance, zip(sub_base,[word]*len(sub_base))).get()
        
        
        k = 0
        for j in range(i+1,length) :
            distance_matrix[i,j] = distance_matrix[j,i] = all_distance[k]
            k += 1    
        
    processing_time_editdistance = time.time() - start
    print("Processing time to compute the distance matrix whit editdistance function: ",processing_time_editdistance)

    
    name = 'editdistance_matrix_mnist'+str(number_of_sample)+'.pk'
    file = open(name, 'wb') 
    
    pickle.dump(distance_matrix, file) 
    file.close()

    return processing_time_editdistance

def generate_test_set(test_set_size=100) :
    train_images, train_labels, test_images, test_labels = Mnist.load_mnist()
    
    indices = list(range(len(test_images)))
    random.shuffle(indices)
    indices = indices[0:test_set_size]
    
    sub_test_set = []
    sub_test_labels = []
    sub_test_base = []
    
    i = 0
    while (len(sub_test_set) < test_set_size) :
        image = test_images[i]
        word = picture2word(image)
        
        if word != "" :
            sub_test_set.append(test_images[i])
            sub_test_labels.append(test_labels[i]) 
            sub_test_base.append(word)
            
        i += 1
        
    name = 'test_mnist_'+str(test_set_size)+'.pk'
    file = open(name, 'wb') 

    pickle.dump(sub_test_base, file) 
    file.close()
    
    name = 'test_mnist_labels_'+str(test_set_size)+'.pk'
    file = open(name, 'wb') 

    pickle.dump(sub_test_labels, file) 
    file.close()
    
def test_distance (training_set_size=1000, test_set_size=100):
    if not( os.path.isfile('base_mnist_'+str(training_set_size)+'.pk') and os.path.isfile('base_mnist_labels'+str(training_set_size)+'.pk') and os.path.isfile('distance_matrix_mnist'+str(training_set_size)+'.pk')) :
        pickle_matrix(number_of_sample=training_set_size)
        
    if not( os.path.isfile('test_mnist_'+str(test_set_size)+'.pk') and os.path.isfile('test_mnist_labels'+str(test_set_size)+'.pk')) :
        generate_test_set(test_set_size=test_set_size)
        
    file_base = open('base_mnist_'+str(training_set_size)+'.pk', 'rb') 
    base = pickle.load(file_base) 
    file_base.close()
    
    file_labels = open('base_mnist_labels'+str(training_set_size)+'.pk', 'rb') 
    label = pickle.load(file_labels) 
    file_labels.close()
    
    file_distance_matrix = open('distance_matrix_mnist'+str(training_set_size)+'.pk', 'rb') 
    distance_matrix = pickle.load(file_distance_matrix) 
    file_distance_matrix.close()
    
    file_base = open('test_mnist_'+str(test_set_size)+'.pk', 'rb') 
    sub_test_base = pickle.load(file_base) 
    file_base.close()
    
    file_labels = open('test_mnist_labels_'+str(test_set_size)+'.pk', 'rb') 
    sub_test_labels = pickle.load(file_labels) 
    file_labels.close()
    
            
#==============================================================================
# Test with our distance
#==============================================================================
    
    miss_classified = 0
    start = time.time()
    for i in range(len(sub_test_base)) :
        word = sub_test_base[i]
        
        digit = analyse.analyse_triangle_knn_multi(word,base,label,distance_matrix,k=3)
                
        if (digit != sub_test_labels[i]) :
            miss_classified += 1
            
    processing_time_distance = (time.time() - start) / test_set_size
    accuracy_distance = ((test_set_size - miss_classified) / test_set_size) * 100


    return processing_time_distance, accuracy_distance
    

def test_editdistance(training_set_size=1000, test_set_size=100):
    if not( os.path.isfile('base_mnist_'+str(training_set_size)+'.pk') and os.path.isfile('base_mnist_labels'+str(training_set_size)+'.pk') and os.path.isfile('editdistance_matrix_mnist'+str(training_set_size)+'.pk')) :
        pickle_matrix(number_of_sample=training_set_size)
        
    if not( os.path.isfile('test_mnist_'+str(test_set_size)+'.pk') and os.path.isfile('test_mnist_labels'+str(test_set_size)+'.pk')) :
        generate_test_set(test_set_size=test_set_size)
        
    file_base = open('base_mnist_'+str(training_set_size)+'.pk', 'rb') 
    base = pickle.load(file_base) 
    file_base.close()
    
    file_labels = open('base_mnist_labels'+str(training_set_size)+'.pk', 'rb') 
    label = pickle.load(file_labels) 
    file_labels.close()
    
    file_distance_matrix = open('editdistance_matrix_mnist'+str(training_set_size)+'.pk', 'rb') 
    editdistance_matrix = pickle.load(file_distance_matrix) 
    file_distance_matrix.close()
    
    file_base = open('test_mnist_'+str(test_set_size)+'.pk', 'rb') 
    sub_test_base = pickle.load(file_base) 
    file_base.close()
    
    file_labels = open('test_mnist_labels_'+str(test_set_size)+'.pk', 'rb') 
    sub_test_labels = pickle.load(file_labels) 
    file_labels.close()

#==============================================================================
# Test with editdistance
#==============================================================================
    
    miss_classified = 0
    start = time.time()
    for i in range(len(sub_test_base)) :
        word = sub_test_base[i]
        
        digit = analyse.edit_analyse_triangle_knn_multi(word,base,label,editdistance_matrix,k=3)
                
        if (digit != sub_test_labels[i]) :
            miss_classified += 1
            
    processing_time_editdistance = (time.time() - start) / test_set_size
    accuracy_editdistance = ((test_set_size - miss_classified) / test_set_size) * 100
    
#############

    return processing_time_editdistance, accuracy_editdistance