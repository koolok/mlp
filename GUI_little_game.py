#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:54:16 2017

@author: remi
"""

from tkinter import Radiobutton, Toplevel, IntVar, Button, Frame, Tk, Label, Canvas, StringVar
from tkinter import RIGHT, LEFT, TOP, GROOVE, BOTTOM
#from tkinter import *
from picture2word import picture2word, picture2word_
from analyse_GUI import analyse_multi
from word2picture import word2picture
from PIL import Image, ImageTk
import numpy as np
import pickle as pk
import os

training_set_size = 6000
rand_num = 42

def mouseDown1a(event) :
    global xc,yc
    xc,yc = event.x, event.y

def mouseMove1a(event) :
    global xc,yc
    xn,yn = event.x, event.y
    if xn > 97:
        xn = 97;
    elif xn < 3 :
        xn = 3;
    if yn > 97:
        yn = 97;
    elif yn < 3 :
        yn = 3;
    canvas1a.create_line(xc,yc,xn,yn,width = 3,smooth = 1)
    canvas1a.create_rectangle(xn-1,yn-1,xn+1,yn+1,fill='black')
    xc,yc = xn,yn

def mouseDown1b(event) :
    global xc,yc
    xc,yc = event.x, event.y

def mouseMove1b(event) :
    global xc,yc
    xn,yn = event.x, event.y
    if xn > 97:
        xn = 97;
    elif xn < 3 :
        xn = 3;
    if yn > 97:
        yn = 97;
    elif yn < 3 :
        yn = 3;
    canvas1b.create_line(xc,yc,xn,yn,width = 3,smooth = 1)
    canvas1b.create_rectangle(xn-1,yn-1,xn+1,yn+1,fill='black')
    xc,yc = xn,yn



def predict() :
    global canvas1a,canvas1b,text
    if len(base) >= 3 :
        canvas1a.postscript(file = 'save1a.ps', colormode='color')
        canvas1b.postscript(file = 'save1b.ps', colormode='color')
        picture1a = Image.open('save1a.ps')
        picture1b = Image.open('save1b.ps')
        word1a,prediction1a,liste1a = analyse_multi(picture2word_(picture1a),base,label,3)
        word1b,prediction1b,liste1b = analyse_multi(picture2word_(picture1b),base,label,3)
        
        os.remove('save1a.ps')
        os.remove('save1b.ps')
#        word2picture(word1a)
#        file1a = word1a+".png"
#        img1a = ImageTk.PhotoImage(file = file1a)
        
#        word2picture(word1b)
        
#        file1b = word1b+".png"
#        img1b = ImageTk.PhotoImage(file = file1b)
#        canvas5.create_image(50, 50, image=img1b)
#        canvas5.image = img
#        os.remove(file)
#        text.set(str(prediction1a)+str(prediction1b))
        
        # first digit
#        word2picture(liste1a[0])
        file1a = str(prediction1a)+".png"
        img1a = ImageTk.PhotoImage(file = file1a)
        canvas2.create_image(50,50,image=img1a)
#        os.remove(file1a)
        
        # second digit
#        word2picture(liste1b[0])
        file1b = str(prediction1b)+".png"
        img1b = ImageTk.PhotoImage(file = file1b)
        canvas3.create_image(50,50,image=img1b)
#        os.remove(file1b)
        
        number = 10 * prediction1a + prediction1b
        if number == rand_num:
            text.set('you found it!')
        elif number < rand_num:
            text.set('it\'s bigger!')
        elif number > rand_num:
            text.set('it\'s smaller!')
        
        canvas1a.delete("all")
        canvas1b.delete("all")

def erase() :
    for can in [canvas1a,canvas1b,canvas2,canvas3] :
        can.delete("all")
    text.set("")

def save() : 
    if database.get() == 1 :
        file = open('ourbase.pk', 'wb')
        pk.dump(base, file) 
        file.close()

        file = open('ourlabel.pk', 'wb') 
        pk.dump(label, file) 
        file.close()
        print("our base saved")
    elif database.get() == 2 :
        file = open('base_mnist_'+str(training_set_size)+'_custom.pk', 'wb') 
        pk.dump(base, file) 
        file.close()

        file = open('base_mnist_labels_'+str(training_set_size)+'_custom.pk', 'wb') 
        pk.dump(label, file) 
        file.close()
        print("mnist base custom saved")
    elif database.get() == 3 :
        file = open('ourbase.pk', 'wb') 
        pk.dump(base, file) 
        file.close()

        file = open('ourlabel.pk', 'wb') 
        pk.dump(label, file) 
        file.close()
        print("our base saved")
    else :  
        file = open('base_mnist_'+str(training_set_size)+'_custom.pk', 'wb') 
        pk.dump(base, file) 
        file.close()

        file = open('base_mnist_labels_'+str(training_set_size)+'_custom.pk', 'wb') 
        pk.dump(label, file) 
        file.close()
        print("mnist base custom saved")

#def correct() :
#    global toplevel
#    toplevel = Toplevel()
#    toplevel.title("Selection")
#    v = IntVar() 
##    b0 = Radiobutton(toplevel, text="0", variable=v, value=0)
##    b1 = Radiobutton(toplevel, text="1", variable=v, value=1)
##    b2 = Radiobutton(toplevel, text="2", variable=v, value=2)
##    b3 = Radiobutton(toplevel, text="3", variable=v, value=3)
##    b4 = Radiobutton(toplevel, text="4", variable=v, value=4)
##    b5 = Radiobutton(toplevel, text="5", variable=v, value=5)
##    b6 = Radiobutton(toplevel, text="6", variable=v, value=6)
##    b7 = Radiobutton(toplevel, text="7", variable=v, value=7)
##    b8 = Radiobutton(toplevel, text="8", variable=v, value=8)
##    b9 = Radiobutton(toplevel, text="9", variable=v, value=9)
##    b0.pack()
##    b1.pack()
##    b2.pack()
##    b3.pack()
##    b4.pack()
##    b5.pack()
##    b6.pack()
##    b7.pack()
##    b8.pack()
##    b9.pack()
#    button4 = Button(toplevel, text="Validate", command=lambda x=v : validate_correct(x))
#    button4.pack(side=RIGHT, padx=30, pady=30)

#def add() :
#    global toplevel2
#    toplevel2 = Toplevel()
#    toplevel2.title("Selection")
#    v2 = IntVar() 
##    b0 = Radiobutton(toplevel2, text="0", variable=v2, value=0)
##    b1 = Radiobutton(toplevel2, text="1", variable=v2, value=1)
##    b2 = Radiobutton(toplevel2, text="2", variable=v2, value=2)
##    b3 = Radiobutton(toplevel2, text="3", variable=v2, value=3)
##    b4 = Radiobutton(toplevel2, text="4", variable=v2, value=4)
##    b5 = Radiobutton(toplevel2, text="5", variable=v2, value=5)
##    b6 = Radiobutton(toplevel2, text="6", variable=v2, value=6)
##    b7 = Radiobutton(toplevel2, text="7", variable=v2, value=7)
##    b8 = Radiobutton(toplevel2, text="8", variable=v2, value=8)
##    b9 = Radiobutton(toplevel2, text="9", variable=v2, value=9)
##    b0.pack()
##    b1.pack()
##    b2.pack()
##    b3.pack()
##    b4.pack()
##    b5.pack()
##    b6.pack()
##    b7.pack()
##    b8.pack()
##    b9.pack()
#    button6 = Button(toplevel2, text="Validate", command=lambda x=v2 : validate_add(x))
#    button6.pack(side=RIGHT, padx=30, pady=30)

#def validate_add(x) :
#    global toplevel2
#    canvas1.postscript(file = 'save.ps', colormode='color')
#    picture = Image.open('save.ps')
#    word = picture2word_(picture)
#    os.remove('save.ps')
#    base.append(word)
#    label.append(x.get())
#    erase()
#    toplevel2.destroy()
#
#def validate_correct(x) :
#    global toplevel
#    canvas1.postscript(file = 'save.ps', colormode='color')
#    picture = Image.open('save.ps')
#    word = picture2word_(picture)
#    os.remove('save.ps')
#    base.append(word)
#    label.append(x.get())
#    erase()
#    toplevel.destroy()

def validate_database(x) :
    global base, label, distance_matrix
    base, label, distance_matrix = init(x.get(), training_set_size)

def init(database, training_set_size) :
    text.set('try a number!')
    if database == 0 :
        try :
            file_base = open('base_mnist_'+str(training_set_size)+'.pk', 'rb')
            base = pk.load(file_base)
            file_base.close()
   
            file_labels = open('base_mnist_labels_'+str(training_set_size)+'.pk', 'rb')
            label = pk.load(file_labels)
            file_labels.close()
            print('base mnist loaded',len(base),len(label))
        except :
            print("Error in base loading : mnist")
            base = []
            label = []
    
        try :
            file = open("distance_matrix.pk", 'rb') 
            distance_matrix = pk.load(file) 
            file.close()
        except :
            distance_matrix = np.zeros((len(base),len(base)))
        
        return base, label, distance_matrix
    elif database == 1 :
        try :
            file_base = open('ourbase.pk', 'rb')
            base = pk.load(file_base)
            file_base.close()
   
            file_labels = open('ourlabel.pk', 'rb')
            label = pk.load(file_labels)
            file_labels.close()
            print('our base loaded',len(base),len(label))
        except :
            print("Error in base loading : our")
            base = []
            label = []
    
        try :
            file = open("distance_matrix_custom.pk", 'rb') 
            distance_matrix = pk.load(file) 
            file.close()
        except :
            distance_matrix = np.zeros((len(base),len(base)))
        
        return base, label, distance_matrix
    elif database == 2 :
        try :
            file_base = open('base_mnist_'+str(training_set_size)+'_custom.pk', 'rb')
            base = pk.load(file_base)
            file_base.close()
   
            file_labels = open('base_mnist_labels_'+str(training_set_size)+'_custom.pk', 'rb')
            label = pk.load(file_labels)
            file_labels.close()
            print('base mnist custom loaded',len(base),len(label))
        except :
            print("Error in base loading : mnist custom")
            base = []
            label = []
    
        try :
            file = open("distance_matrix_custom.pk", 'rb') 
            distance_matrix = pk.load(file) 
            file.close()
        except :
            distance_matrix = np.zeros((len(base),len(base)))
        
        return base, label, distance_matrix
    elif database == 3 :
        base = []
        label = []
        distance_matrix = np.zeros((len(base),len(base)))
        print('new base loaded',len(base),len(label))

        return base, label, distance_matrix
    else :
        print("Error in the choice of the database")
        return [],[],np.zeros((0,0))

window = Tk()

window['bg']='dark gray'
window.title("Hand Written Digit Recognition")

# frame 0
frame0 = Frame(window, borderwidth=2, relief=GROOVE)
frame0.pack(side=TOP, padx=5, pady=5)

# frame 1
frame1 = Frame(window, borderwidth=2, relief=GROOVE)
frame1.pack(side=TOP, padx=30, pady=30)
Label(frame1, text="input").pack(padx=10, pady=10)

# frame 2
frame2 = Frame(window, borderwidth=2, relief=GROOVE)
frame2.pack(side=BOTTOM, padx=10, pady=10)
Label(frame2, text="output").pack(padx=10, pady=10)

# radiobutton in frame 0
database = IntVar(0)
database.set(0)
b_0 = Radiobutton(frame0, text="Mnist Database", variable=database, value=0, anchor='w')
b_1 = Radiobutton(frame0, text="Our Database", variable=database, value=1, anchor='w')
b_2 = Radiobutton(frame0, text="Mnist Custumized", variable=database, value=2, anchor='w')
b_3 = Radiobutton(frame0, text="New Database", variable=database, value=3, anchor='w')
b_0.pack()
b_1.pack()
b_2.pack()
b_3.pack()
button5 = Button(frame0, text="Validate", command=lambda x=database : validate_database(x))
button5.pack(side=RIGHT, padx=30, pady=30)

# canvas 1 in frame 1
canvas1a = Canvas(frame1, width=100, height=100, background='white')
canvas1a.bind("<Button-1>", mouseDown1a)
canvas1a.bind("<B1-Motion>", mouseMove1a)
canvas1a.pack(side=LEFT, padx=30, pady=30)

canvas1b = Canvas(frame1, width=100, height=100, background='white')
canvas1b.bind("<Button-1>", mouseDown1b)
canvas1b.bind("<B1-Motion>", mouseMove1b)
canvas1b.pack(side=LEFT, padx=30, pady=30)



# buttons in frame 1
button7 = Button(frame1, text="Save", command=save)
button7.pack(side=RIGHT, padx=30, pady=30)

#button3 = Button(frame1, text="Add", command=add)
#button3.pack(side=RIGHT, padx=30, pady=30)
#
#button2 = Button(frame1, text="Correct", command=correct)
#button2.pack(side=RIGHT, padx=30, pady=30)

button1 = Button(frame1, text="Try", command=predict)
button1.pack(side=RIGHT, padx=30, pady=30)

button0 = Button(frame1, text="Erase", command=erase)
button0.pack(side=RIGHT, padx=30, pady=30)

# canvas 5 in frame 2
#canvas5 = Canvas(frame2, width=100, height=100, background='black')
#canvas5.pack(side=LEFT, padx=30, pady=30)

# first digit
canvas2 = Canvas(frame2, width=100, height=100, background='black')
canvas2.pack(side=LEFT, padx=30, pady=30)

# second digit
canvas3 = Canvas(frame2, width=100, height=100, background='black')
canvas3.pack(side=LEFT, padx=30, pady=30)

# canvas 4 in frame 2
#canvas4 = Canvas(frame2, width=100, height=100, background='black')
#canvas4.pack(side=LEFT, padx=30, pady=30)

# frame 3 in frame 2
frame3 = Frame(frame2, bg="white", borderwidth=2, relief=GROOVE, width=100, height=100)
frame3.pack(side=RIGHT, padx=5, pady=5)
text = StringVar()
text.set("")
Label(frame3, textvariable = text,bg="white").pack(padx=10, pady=10)

base, label, distance_matrix = init(database.get(), training_set_size)

window.mainloop()

