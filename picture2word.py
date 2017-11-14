#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 19:51:32 2017

@author: koolok
"""

def picture2word(picture) :
    """fonction retournant le mot correspondant au pictogramme noir tracé dans
    le fichier entrer en paramètre"""

    #picture.show()
    #récupération des dimensions de l'image
    width,height = picture.size
    #print(width)
    #print(height)

    #recherche du pixel de départ pris en haut puis à gauche
    w = 0
    h = 0
    while (picture.getpixel((w,h)) != (0,0,0)) :
        w = w+1
        if (w >= width) : 
            w = 0
            h = h+1
            if (h >= height) :
                # L'image est entièrement blanche
                return ""
            
            

    #print("largeur : ",w," et hauteur : ",h," pour le premier pixel.")

    #parcours de l'image à partir de ce pixel
    #E = 0 / SE = 1 / S = 2 / SO = 3 / O = 4 / NO = 5 / N = 6 / NE = 7
    w_save = w
    h_save = h
    end = 1
    word = ""
    last = 0
    while (end) :
        
        if (last == 0) :
            if (picture.getpixel((w-1,h-1)) == (0,0,0)) :
                last = 5
                w = w-1
                h = h-1
            elif (picture.getpixel((w,h-1)) == (0,0,0)) :
                last = 6
                h = h-1
            elif (picture.getpixel((w+1,h-1)) == (0,0,0)) :
                last = 7
                w = w+1
                h = h-1
            elif (picture.getpixel((w+1,h)) == (0,0,0)) :
                last = 0
                w = w+1
            elif (picture.getpixel((w+1,h+1)) == (0,0,0)) :
                last = 1
                w = w+1
                h = h+1
            elif (picture.getpixel((w,h+1)) == (0,0,0)) :
                last = 2
                h = h+1
            elif (picture.getpixel((w-1,h+1)) == (0,0,0)) :
                last = 3
                w = w-1
                h = h+1
            elif (picture.getpixel((w-1,h)) == (0,0,0)) :
                last = 4
                w = w-1
        elif (last == 1) :
            if (picture.getpixel((w,h-1)) == (0,0,0)) :
                last = 6
                h = h-1
            elif (picture.getpixel((w+1,h-1)) == (0,0,0)) :
                last = 7
                w = w+1
                h = h-1
            elif (picture.getpixel((w+1,h)) == (0,0,0)) :
                last = 0
                w = w+1
            elif (picture.getpixel((w+1,h+1)) == (0,0,0)) :
                last = 1
                w = w+1
                h = h+1
            elif (picture.getpixel((w,h+1)) == (0,0,0)) :
                last = 2
                h = h+1
            elif (picture.getpixel((w-1,h+1)) == (0,0,0)) :
                last = 3
                w = w-1
                h = h+1
            elif (picture.getpixel((w-1,h)) == (0,0,0)) :
                last = 4
                w = w-1
            elif (picture.getpixel((w-1,h-1)) == (0,0,0)) :
                last = 5
                w = w-1
                h = h-1
        elif (last == 2) :
            if (picture.getpixel((w+1,h-1)) == (0,0,0)) :
                last = 7
                w = w+1
                h = h-1
            elif (picture.getpixel((w+1,h)) == (0,0,0)) :
                last = 0
                w = w+1
            elif (picture.getpixel((w+1,h+1)) == (0,0,0)) :
                last = 1
                w = w+1
                h = h+1
            elif (picture.getpixel((w,h+1)) == (0,0,0)) :
                last = 2
                h = h+1
            elif (picture.getpixel((w-1,h+1)) == (0,0,0)) :
                last = 3
                w = w-1
                h = h+1
            elif (picture.getpixel((w-1,h)) == (0,0,0)) :
                last = 4
                w = w-1
            elif (picture.getpixel((w-1,h-1)) == (0,0,0)) :
                last = 5
                w = w-1
                h = h-1
            elif (picture.getpixel((w,h-1)) == (0,0,0)) :
                last = 6
                h = h-1
        elif (last == 3) :
            if (picture.getpixel((w+1,h)) == (0,0,0)) :
                last = 0
                w = w+1
            elif (picture.getpixel((w+1,h+1)) == (0,0,0)) :
                last = 1
                w = w+1
                h = h+1
            elif (picture.getpixel((w,h+1)) == (0,0,0)) :
                last = 2
                h = h+1
            elif (picture.getpixel((w-1,h+1)) == (0,0,0)) :
                last = 3
                w = w-1
                h = h+1
            elif (picture.getpixel((w-1,h)) == (0,0,0)) :
                last = 4
                w = w-1
            elif (picture.getpixel((w-1,h-1)) == (0,0,0)) :
                last = 5
                w = w-1
                h = h-1
            elif (picture.getpixel((w,h-1)) == (0,0,0)) :
                last = 6
                h = h-1
            elif (picture.getpixel((w+1,h-1)) == (0,0,0)) :
                last = 7
                w = w+1
                h = h-1
        elif (last == 4) :
            if (picture.getpixel((w+1,h+1)) == (0,0,0)) :
                last = 1
                w = w+1
                h = h+1
            elif (picture.getpixel((w,h+1)) == (0,0,0)) :
                last = 2
                h = h+1
            elif (picture.getpixel((w-1,h+1)) == (0,0,0)) :
                last = 3
                w = w-1
                h = h+1
            elif (picture.getpixel((w-1,h)) == (0,0,0)) :
                last = 4
                w = w-1
            elif (picture.getpixel((w-1,h-1)) == (0,0,0)) :
                last = 5
                w = w-1
                h = h-1
            elif (picture.getpixel((w,h-1)) == (0,0,0)) :
                last = 6
                h = h-1
            elif (picture.getpixel((w+1,h-1)) == (0,0,0)) :
                last = 7
                w = w+1
                h = h-1
            elif (picture.getpixel((w+1,h)) == (0,0,0)) :
                last = 0
                w = w+1
        elif (last == 5) :
            if (picture.getpixel((w,h+1)) == (0,0,0)) :
                last = 2
                h = h+1
            elif (picture.getpixel((w-1,h+1)) == (0,0,0)) :
                last = 3
                w = w-1
                h = h+1
            elif (picture.getpixel((w-1,h)) == (0,0,0)) :
                last = 4
                w = w-1
            elif (picture.getpixel((w-1,h-1)) == (0,0,0)) :
                last = 5
                w = w-1
                h = h-1
            elif (picture.getpixel((w,h-1)) == (0,0,0)) :
                last = 6
                h = h-1
            elif (picture.getpixel((w+1,h-1)) == (0,0,0)) :
                last = 7
                w = w+1
                h = h-1
            elif (picture.getpixel((w+1,h)) == (0,0,0)) :
                last = 0
                w = w+1
            elif (picture.getpixel((w+1,h+1)) == (0,0,0)) :
                last = 1
                w = w+1
                h = h+1
        elif (last == 6) :
            if (picture.getpixel((w-1,h+1)) == (0,0,0)) :
                last = 3
                w = w-1
                h = h+1
            elif (picture.getpixel((w-1,h)) == (0,0,0)) :
                last = 4
                w = w-1
            elif (picture.getpixel((w-1,h-1)) == (0,0,0)) :
                last = 5
                w = w-1
                h = h-1
            elif (picture.getpixel((w,h-1)) == (0,0,0)) :
                last = 6
                h = h-1
            elif (picture.getpixel((w+1,h-1)) == (0,0,0)) :
                last = 7
                w = w+1
                h = h-1
            elif (picture.getpixel((w+1,h)) == (0,0,0)) :
                last = 0
                w = w+1
            elif (picture.getpixel((w+1,h+1)) == (0,0,0)) :
                last = 1
                w = w+1
                h = h+1
            elif (picture.getpixel((w,h+1)) == (0,0,0)) :
                last = 2
                h = h+1
        elif (last == 7) :
            if (picture.getpixel((w-1,h)) == (0,0,0)) :
                last = 4
                w = w-1
            elif (picture.getpixel((w-1,h-1)) == (0,0,0)) :
                last = 5
                w = w-1
                h = h-1
            elif (picture.getpixel((w,h-1)) == (0,0,0)) :
                last = 6
                h = h-1
            elif (picture.getpixel((w+1,h-1)) == (0,0,0)) :
                last = 7
                w = w+1
                h = h-1
            elif (picture.getpixel((w+1,h)) == (0,0,0)) :
                last = 0
                w = w+1
            elif (picture.getpixel((w+1,h+1)) == (0,0,0)) :
                last = 1
                w = w+1
                h = h+1
            elif (picture.getpixel((w,h+1)) == (0,0,0)) :
                last = 2
                h = h+1
            elif (picture.getpixel((w-1,h+1)) == (0,0,0)) :
                last = 3
                w = w-1
                h = h+1
        word = word + str(last)
        if (w == w_save and h == h_save) :
            end = 0
        #print("pixel étudié : ",w," , ",h)
        
    cleaned_picture = clean_picture(picture,w_save,h_save)
    second_word = picture2word(cleaned_picture)
        
    if (second_word != ""):
        word = word + "#" + second_word
        
    return(word)


def clean_picture(picture,w,h) :
    picture.putpixel((w,h), (255,255,255))
        
    if picture.getpixel((w+1,h)) == (0,0,0) :
        picture = clean_picture(picture, w+1, h)
    if picture.getpixel((w+1,h+1)) == (0,0,0) :
        picture = clean_picture(picture, w+1, h+1)
    if picture.getpixel((w+1,h-1)) == (0,0,0) :
        picture = clean_picture(picture, w+1, h-1)
        
    if picture.getpixel((w-1,h)) == (0,0,0) :
        picture = clean_picture(picture, w-1, h)
    if picture.getpixel((w-1,h+1)) == (0,0,0) :
        picture = clean_picture(picture, w-1, h+1)
    if picture.getpixel((w-1,h-1)) == (0,0,0) :
        picture = clean_picture(picture, w-1, h-1)
        
    if picture.getpixel((w,h+1)) == (0,0,0) :
        picture = clean_picture(picture, w, h+1)
    if picture.getpixel((w,h-1)) == (0,0,0) :
        picture = clean_picture(picture, w, h-1)
        
    return picture