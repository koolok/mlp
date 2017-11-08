# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 09:20:13 2016

@author: remi
"""

from PIL import Image, ImageDraw
import os
import pygame
import numpy as np
from pygame.locals import *
import pickle 
from scipy.ndimage.interpolation import zoom
from multiprocessing import Pool
import analyse


from distance import distance

last_x = 0;
last_y = 0;


def init() :
    try :
        data = open("data.txt", "r", encoding="utf-8")
        base = []
        label = []
        for line in data :
            digit,word = line.split("/")
            base.append(word[0:-1])
            label.append(int(digit))
        data.close()
    except :
        base = []
        label = []
    
    try :
        file = open("distance_matrix.pk", 'rb') 
        distance_matrix = pickle.load(file) 
        file.close()
    except :
        distance_matrix = np.zeros((len(base),len(base)))
        
    return base, label, distance_matrix

def update_matrix(base, distance_matrix, word) :
    newrow = np.zeros(len(distance_matrix))
    distance_matrix = np.vstack([distance_matrix, newrow])
    newcol = np.zeros((len(distance_matrix),1))
    distance_matrix = np.hstack([distance_matrix,newcol])
    
    pool = Pool()
    
    all_distance = pool.starmap_async(distance, zip(base,[word]*len(base))).get()
    
    for i in range(len(distance_matrix)-1) :
        distance_matrix[-1][i] = distance_matrix[i][-1] = all_distance[i]
        
    return distance_matrix

def close(base,label,distance_matrix) :
    data = open("data.txt", "w", encoding="utf-8")
    for i in range(len(base)) :
        word = base[i]
        data.write(str(label[i])+"/"+word+"\n")
    data.close()
    os.remove("temp.png")
    os.remove("new.png")
    
    file = open('distance_matrix.pk', 'wb') 
    pickle.dump(distance_matrix, file) 
    file.close()

    
def interface() : 
    #Initialisation
    pygame.init()
    base, label, distance_matrix = init()

    #Création de la fenêtre
    window = pygame.display.set_mode((560, 340),pygame.RESIZABLE)
    
    #chargement et application de la zone de dessin et des boutons
    draw = pygame.image.load("vide.png").convert()
    validate = pygame.image.load("valider.png").convert()
    cancel = pygame.image.load("annuler.png").convert()
    b0 = pygame.image.load("0.png").convert()
    b1 = pygame.image.load("1.png").convert()
    b2 = pygame.image.load("2.png").convert()
    b3 = pygame.image.load("3.png").convert()
    b4 = pygame.image.load("4.png").convert()
    b5 = pygame.image.load("5.png").convert()
    b6 = pygame.image.load("6.png").convert()
    b7 = pygame.image.load("7.png").convert()
    b8 = pygame.image.load("8.png").convert()
    b9 = pygame.image.load("9.png").convert()
    blearn = pygame.image.load("?.png").convert()
    black = pygame.image.load("noir.png").convert()
    bRM = pygame.image.load("ADD.png").convert()
    window.blit(draw, (10,10))
    window.blit(cancel, (120,10))
    window.blit(validate, (230,10))
    window.blit(bRM, (450,10))
    window.blit(b0, (10,120))
    window.blit(b1, (120,120))
    window.blit(b2, (230,120))
    window.blit(b3, (340,120))
    window.blit(b4, (450,120))
    window.blit(b5, (10,230))
    window.blit(b6, (120,230))
    window.blit(b7, (230,230))
    window.blit(b8, (340,230))
    window.blit(b9, (450,230))
    
    #création de l'image destination et mise en blanc
    picture = Image.new("RGB",(100,100))
    initPicture(picture)
    draw_img = ImageDraw.Draw(picture)
    
    #Raffraichissement de la fenêtre
    pygame.display.flip()
    
    learn = 0
    continuer = 1
    
    # saving the last px used for smoothing
    last_x = 0
    last_y = 0
    
    while continuer :
        for event in pygame.event.get() :
            #gestion de la fermeture de la fenêtre
            if event.type == QUIT :
                close(base,label,distance_matrix)
                continuer = 0
                pygame.quit()
            
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 11 and event.pos[0] < 109 and \
            event.pos[1] > 11 and event.pos[1] < 109 :
                last_x = event.pos[0]
                last_y = event.pos[1]
            
            #gestion du dessin
            if event.type == MOUSEMOTION and event.buttons[0] == 1 and \
            event.pos[0] > 11 and event.pos[0] < 109 and \
            event.pos[1] > 11 and event.pos[1] < 109 :
                learn = 1
                new_x = event.pos[0]
                new_y = event.pos[1]
                
                window.blit(black, (340,10))
                
                draw_img.line((last_x-10,last_y-10,new_x-10,new_y-10),fill='black',width=5)
                last_x = new_x
                last_y = new_y
                #drawPixel(picture,event.pos[0]-10,event.pos[1]-10)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                pygame.display.flip()
            
            #gestion du boulon annuler
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 121 and event.pos[0] < 219 and \
            event.pos[1] > 11 and event.pos[1] < 109 :
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
                
            #gestion du bouton RM
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 451 and event.pos[0] < 549 and \
            event.pos[1] > 11 and event.pos[1] < 109 :
                learn = 1
                window.blit(blearn, (340,10))
                pygame.display.flip()
                
            #gestion du bouton valider
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 231 and event.pos[0] < 329 and \
            event.pos[1] > 11 and event.pos[1] < 109 and learn == 1 :
                picture.save("new.png")
                
                #ouverture du fichier source
                new_picture = Image.open("new.png")                
                word = picture2word(new_picture)
                
                word2 = None
                digit = analyse.analyse_triangle_knn_multi(word,base,label,distance_matrix,3)

                if (zoomout("new.png","new2.png")):
                    new_picture2 = Image.open("new2.png")
                    word2 = picture2word(new_picture2)
                    digit2 = analyse.analyse_triangle_knn_multi(word2,base,label,distance_matrix,3)
                    
                if digit == 0 :
                    window.blit(b0, (340,10))
                elif digit == 1 :
                    window.blit(b1, (340,10))
                elif digit == 2 :
                    window.blit(b2, (340,10))
                elif digit == 3 :
                    window.blit(b3, (340,10))
                elif digit == 4 :
                    window.blit(b4, (340,10))
                elif digit == 5 :
                    window.blit(b5, (340,10))
                elif digit == 6 :
                    window.blit(b6, (340,10))
                elif digit == 7 :
                    window.blit(b7, (340,10))
                elif digit == 8 :
                    window.blit(b8, (340,10))
                elif digit == 9 :
                    window.blit(b9, (340,10))
                else :
                    window.blit(blearn, (340,10))
                    
#                if digit != -1 :
#                    learn = 2
#                    base[digit].append(word)
                
                
#                if learn == 1 :
#                    window.blit(blearn, (340,10))
#                else :
#                    initPicture(picture)
#                    picture.save("temp.png")
#                    draw = pygame.image.load("temp.png").convert()
#                    window.blit(draw, (10,10))
                pygame.display.flip()
            
            #gestion des boutons chiffres
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 11 and event.pos[0] < 109 and \
            event.pos[1] > 121 and event.pos[1] < 219 and learn == 1 :
                base.append(word)
                label.append(0)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(0)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 121 and event.pos[0] < 219 and \
            event.pos[1] > 121 and event.pos[1] < 219 and learn == 1 :
                base.append(word)
                label.append(1)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(1)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 231 and event.pos[0] < 329 and \
            event.pos[1] > 121 and event.pos[1] < 219 and learn == 1 :
                base.append(word)
                label.append(2)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(2)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 341 and event.pos[0] < 439 and \
            event.pos[1] > 121 and event.pos[1] < 219 and learn == 1:
                base.append(word)
                label.append(3)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(3)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 451 and event.pos[0] < 549 and \
            event.pos[1] > 121 and event.pos[1] < 219 and learn == 1 :       
                base.append(word)
                label.append(4)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(4)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 11 and event.pos[0] < 109 and \
            event.pos[1] > 231 and event.pos[1] < 329 and learn == 1 :
                base.append(word)
                label.append(5)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(5)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 121 and event.pos[0] < 219 and \
            event.pos[1] > 231 and event.pos[1] < 329 and learn == 1 :
                base.append(word)
                label.append(6)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(6)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 231 and event.pos[0] < 329 and \
            event.pos[1] > 231 and event.pos[1] < 329 and learn == 1 :
                base.append(word)
                label.append(7)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(7)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 341 and event.pos[0] < 439 and \
            event.pos[1] > 231 and event.pos[1] < 329 and learn == 1 :
                base.append(word)
                label.append(8)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(8)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            event.pos[0] > 451 and event.pos[0] < 549 and \
            event.pos[1] > 231 and event.pos[1] < 329 and learn == 1 :
                base.append(word)
                label.append(9)
                distance_matrix = update_matrix(base, distance_matrix, word)
                if (word2 != None):
                    base.append(word)
                    label.append(9)
                    distance_matrix = update_matrix(base, distance_matrix, word)
                learn = 0
                initPicture(picture)
                picture.save("temp.png")
                draw = pygame.image.load("temp.png").convert()
                window.blit(draw, (10,10))
                window.blit(black, (340,10))
                pygame.display.flip()
            
def initPicture(picture) :
    last_x = 0
    last_y = 0             
    for x in range(100) : 
        for y in range(100) :
            picture.putpixel((x,y),(255,255,255))

def drawPixel(picture,x,y) :
    p = (0,0,0)
    picture.putpixel((x-1,y-1),p)
    picture.putpixel((x-1,y),p)
    picture.putpixel((x-1,y+1),p)
    picture.putpixel((x,y-1),p)
    picture.putpixel((x,y),p)
    picture.putpixel((x,y+1),p)
    picture.putpixel((x+1,y-1),p)
    picture.putpixel((x+1,y),p)
    picture.putpixel((x+1,y+1),p)


def word2picture(word) :
    """fonction affichant le contour correpondant au mot entré en paramètre"""
    #création de l'image destination
    picture = Image.new("RGB",(200,105))
    
    #position de départ du tracer
    w = 100
    h = 5
    
    #partage du mot en caractères
    tab = word.split()
    #print(tab)
    
    #tracer pixels par pixels
    p = (255,0,0)
    picture.putpixel((w,h),p)
    for c in tab :
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
    picture.show()
    #picture.save("test.png")
    return picture
    
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
    

def zoomout(img_name_in, img_name_out):
    img = Image.open(img_name_in)
    img_ar = np.asarray(img.convert('L'))
    
    px, py = np.where(img_ar == 0)
    
    x_min = px.min()
    y_min = py.min()
    x_max = px.max()
    y_max = py.max()
    
    delta_x = x_max - x_min
    delta_y = y_max - y_min
    
    if (delta_x > 50 or delta_y > 50):
        # zooming by .5
        img_new = np.ones([100,100])*255
        img_new[25:75,25:75] = zoom(img_ar,zoom=0.5,order=0,mode='wrap')
        #TODO add img_new
        
        for x in range(len(img_new)):
            for y in range(len(img_new[0])):
                if img_new[x,y] < 255:
                    img_new[x,y] = 0
                    
        Image.fromarray(np.uint8(img_new)).save(img_name_out)
        return True
    else:
        return False


#word2picture(picture2word("0b.png"))
#word2picture(picture2word("0d.png"))
#print(distance(picture2word("0b.png"),picture2word("0d.png")))
#print(distance(picture2word("3.png"),picture2word("8.png")))
interface()
