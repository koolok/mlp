#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:44:39 2017

@author: koolok
"""

import mnist
from PIL import Image
import pickle 


def mnist_to_pickle() :
    train_images = mnist.train_images()
    
    images = []
    
    for i in range(len(train_images)) :
        data = train_images[i,:,:] * -1 + 256
        
        dataL = []
        
        for line in data :
            dataL.extend(line)
    
        imageL = Image.new("L",(28,28))
        imageL.putdata(dataL)
        
        imageRGB = imageL.convert(mode="RGB")
        
        images.append(imageRGB)
        
        
    file = open('mnist_train.pk', 'wb') 
    
    pickle.dump(images, file) 
    file.close()
    
    
    test_images = mnist.test_images()
        
    images = []
    
    for i in range(len(test_images)) :
        data = test_images[i,:,:] * -1 + 256
        
        dataL = []
        
        for line in data :
            dataL.extend(line)
    
        imageL = Image.new("L",(28,28))
        imageL.putdata(dataL)
        
        imageRGB = imageL.convert(mode="RGB")
        
        images.append(imageRGB)
        
        
    file = open('mnist_test.pk', 'wb') 
    
    pickle.dump(images, file) 
    file.close()

def load_mnist() :
    try :
        file = open("mnist_train.pk", 'rb') 
        train_images = pickle.load(file) 
        file.close()
        
        file = open("mnist_test.pk", 'rb') 
        test_images = pickle.load(file) 
        file.close()
        
        return train_images, mnist.train_labels(), test_images, mnist.test_labels()
        
    except :
        print("mnist_train.pk or mnist_test.pk not found. Please run mnist_to_pickle")
        
        
        