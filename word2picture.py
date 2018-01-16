#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 13:57:39 2017

@author: koolok
"""
from PIL import Image

def word2picture(word) :
    """fonction affichant le contour correpondant au mot entré en paramètre"""
    #création de l'image destination
    picture = Image.new("RGB",(100,100))
    
    #position de départ du tracer
    w = 50
    h = 10
    
    #tracer pixels par pixels
    p = (255,255,0)
    picture.putpixel((w,h),p)
    for i in range(len(word)) :
        c = word[i]
        if (c == '0') :
            w = w+1
        if (c == '1') :
            w = w+1
            h = h+1
        if (c == '2') :
            h = h+1
        if (c == '3') :
            w = w-1
            h = h+1
        if (c == '4') :
            w = w-1
        if (c == '5') :
            w = w-1
            h = h-1
        if (c == '6') :
            h = h-1
        if (c == '7') :
            w = w+1
            h = h-1
        
        picture.putpixel((w,h),p)
    #picture.show()
    picture.save("temp.png")
