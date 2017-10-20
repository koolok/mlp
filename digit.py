# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 09:20:13 2016

@author: remi
"""

from PIL import Image, ImageDraw
import os
import pygame
import numpy as np
import random
from pygame.locals import *
import numpy as np
from collections import deque
import pickle 
#import editdistance
from array import array

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
    
    for i in range(len(distance_matrix)-1) :
        distance_matrix[-1][i] = distance_matrix[i][-1] = distance(word,base[i])
        
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

def analyse(word,base,label) :
    label_mini = -1
    mini = -1

    for i in range(len(base)) :
        w = base[i]
            
        dist = distance(word,w)
#        dist = editdistance.eval(word,w)
        print(dist)
        if dist < mini or mini < 0 :
            mini = dist
            label_mini = label[i]
    return label_mini

def analyse_triangle(word,base,label,distance_matrix) :
    if len(base) == 0 :
        return -1
    if len(base) == 1 :
        return label[0]
    
    pool = list(range(len(base)))
    
    w1 = random.choice(pool)
    pool.remove(w1)
    
    w2 = random.choice(pool)
    pool.remove(w2)

#    dist_w1 = editdistance.eval(base[w1],word)
#    dist_w2 = editdistance.eval(base[w2],word)
    dist_w1 = distance(base[w1],word)
    dist_w2 = distance(base[w2],word)
    
    while (pool != []) :
        if dist_w1 > dist_w2 :
            for i in pool :
                if distance_matrix[i][w1] < dist_w1 - dist_w2 or distance_matrix[i][w1] > dist_w1 + dist_w2 :
                    pool.remove(i)
                    
            if pool == [] :
                break
            w1 = random.choice(pool)
            pool.remove(w1)
            dist_w1 = distance(base[w1],word)
#            dist_w1 = editdistance.eval(base[w1],word)
                    
        else :
            for i in pool :
                if distance_matrix[i][w1] < dist_w2 - dist_w1 or distance_matrix[i][w1] > dist_w2 + dist_w1 :
                    pool.remove(i)
            
            if pool == [] :
                break
            w2 = random.choice(pool)
            pool.remove(w2)
            dist_w2 = distance(base[w2],word)
#            dist_w2 = editdistance.eval(base[w2],word)
            
    if (dist_w1 < dist_w2) :
        return label[w1]
    else :
        return label[w2]
        
    
def interface() : 
    #Initialisation
    pygame.init()
    base, label, distance_matrix = init()

    #Création de la fenêtre
    window = pygame.display.set_mode((560, 340),RESIZABLE)
    
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
    bRM = pygame.image.load("RM.png").convert()
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
                
                digit = analyse_triangle(word,base,label,distance_matrix)
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
                distance_matrix = distance_matrix = update_matrix(base, distance_matrix, word)
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
    
    

def pen_mat(a,b,c,d,e):
    tmp = deque([a,b,c,d,e,d,c,b])
    mat = np.zeros(shape=(8,8))
    for i_row in range(0,8):
        mat[i_row] = tmp
        tmp.rotate(1)
    return mat
    
    
pen_mat = pen_mat(0,1,2,3,4)
pen_add_suppr = 2

def distance_(seq1, seq2, max_dist=-1):
    if seq1 == seq2:
        return 0
	
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
	
    column = array('L', range(0,2*(len2 + 1),2))
	
    for x in range(1, len1 + 1):
        column[0] = x
        last = x - 1
        for y in range(1, len2 + 1):
            old = column[y]
            cost = pen_mat[ord(seq1[x - 1])-48][ord(seq2[y - 1])-48]
            column[y] = min(column[y] + 2, column[y - 1] + 2, last + cost)
            last = old
        if max_dist >= 0 and min(column) > max_dist:
            return -1
	
    if max_dist >= 0 and column[len2] > max_dist:
        return -1
    return column[len2]

def distance(word1,word2) : 
    dico = { (-1,-1):0 }
    
    for i,c_i in enumerate(word1) :
        dico[i,-1] = dico[i-1,-1]+pen_add_suppr
        dico[-1,i] = dico[-1,i-1]+pen_add_suppr
        for j,c_j in enumerate(word2) :
            c_i_int = ord(c_i) - ord('0')
            c_j_int = ord(c_j) - ord('0')
            """print(i,c_i,j,c_j)"""
            option = []
            if (i-1,j) in dico :
                x = dico[i-1,j]+pen_add_suppr
                option.append(x)
            if (i,j-1) in dico :
                x = dico[i,j-1]+pen_add_suppr
                option.append(x)
            if (i-1,j-1) in dico :
                x = dico[i-1,j-1] + pen_mat[c_i_int,c_j_int]
                option.append(x)
            dico[i,j] = min(option)
            """print(option)
            print(dist)
            print()"""
    return dico[len(word1)-1, len(word2)-1]



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
    

#word2picture(picture2word("0b.png"))
#word2picture(picture2word("0d.png"))
#print(distance(picture2word("0b.png"),picture2word("0d.png")))
#print(distance(picture2word("3.png"),picture2word("8.png")))
interface()
