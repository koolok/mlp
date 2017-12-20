#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:54:16 2017

@author: remi
"""

from tkinter import Radiobutton, Toplevel, IntVar, Button, Frame, Tk, Label, Canvas
from tkinter import RIGHT, LEFT, TOP, GROOVE, BOTTOM
from tkinter import *
from picture2word import picture2word
from analyse_GUI import analyse_multi
from word2picture import word2picture
from PIL import Image, ImageTk
import numpy as np
import pickle as pk
import os

def mouseDown(event) :
    global xc,yc
    xc,yc = event.x, event.y

def mouseMove(event) :
    global xc,yc
    xn,yn = event.x, event.y
    canvas1.create_line(xc,yc,xn,yn,width = 3,smooth = 1)
    canvas1.create_rectangle(xn-1,yn-1,xn+1,yn+1,fill='black')
    xc,yc = xn,yn

def predict() :
    global canvas1,text
    canvas1.postscript(file = 'save.ps', colormode='color')
    picture = Image.open('save.ps')
    word,prediction,liste = analyse_multi(picture2word(picture),base,label,3)
    os.remove('save.ps')
    word2picture(word)
    file = word+".png"
    img = ImageTk.PhotoImage(file = file)
    canvas5.create_image(50, 50, image=img)
    canvas5.image = img
    os.remove(file)
    text.set(str(prediction))
    for i,can in enumerate([canvas2,canvas3,canvas4]) :
        word2picture(liste[i])
        file = liste[i]+".png"
        img = ImageTk.PhotoImage(file = file)
        can.create_image(50, 50, image=img)
        can.image = img
        os.remove(file)

def erase() :
    for can in [canvas1,canvas2,canvas3,canvas4,canvas5] :
        can.delete("all")
    text.set("")
    
def correct() :
    global toplevel
    toplevel = Toplevel()
    toplevel.title("Selection")
    v = IntVar() 
    b0 = Radiobutton(toplevel, text="0", variable=v, value=0)
    b1 = Radiobutton(toplevel, text="1", variable=v, value=1)
    b2 = Radiobutton(toplevel, text="2", variable=v, value=2)
    b3 = Radiobutton(toplevel, text="3", variable=v, value=3)
    b4 = Radiobutton(toplevel, text="4", variable=v, value=4)
    b5 = Radiobutton(toplevel, text="5", variable=v, value=5)
    b6 = Radiobutton(toplevel, text="6", variable=v, value=6)
    b7 = Radiobutton(toplevel, text="7", variable=v, value=7)
    b8 = Radiobutton(toplevel, text="8", variable=v, value=8)
    b9 = Radiobutton(toplevel, text="9", variable=v, value=9)
    b0.pack()
    b1.pack()
    b2.pack()
    b3.pack()
    b4.pack()
    b5.pack()
    b6.pack()
    b7.pack()
    b8.pack()
    b9.pack()
    button4 = Button(toplevel, text="Validate", command=lambda x=v : validate_correct(x))
    button4.pack(side=RIGHT, padx=30, pady=30)

def validate_correct(x) :
    global toplevel
#à remplacer par l'ajout dans la base
    print(x.get())
    erase()
    toplevel.destroy()

def validate_database(x) :
    global base, label, distance_matrix
    base, label, distance_matrix = init(x.get(), 6000)

def init(database, training_set_size) :
    if database == 0 :
        try :
            file_base = open('base_mnist_'+str(training_set_size)+'.pk', 'rb')
            base = pk.load(file_base)
            file_base.close()
   
            file_labels = open('base_mnist_labels'+str(training_set_size)+'.pk', 'rb')
            label = pk.load(file_labels)
            file_labels.close()
        except :
            print("Error in base loading")
            base = []
            label = []
    
        try :
            file = open("distance_matrix.pk", 'rb') 
            distance_matrix = pickle.load(file) 
            file.close()
        except :
            distance_matrix = np.zeros((len(base),len(base)))
        
        return base, label, distance_matrix
    else :
        print("Error in the choice of the database")
        return 1,2,3

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
b_0 = Radiobutton(frame0, text="mnist", variable=database, value=0, anchor='w')
b_1 = Radiobutton(frame0, text="our database", variable=database, value=1, anchor='w')
b_2 = Radiobutton(frame0, text="both", variable=database, value=2, anchor='w')
b_3 = Radiobutton(frame0, text="empty", variable=database, value=3, anchor='w')
b_0.pack()
b_1.pack()
b_2.pack()
b_3.pack()
button5 = Button(frame0, text="Validate", command=lambda x=database : validate_database(x))
button5.pack(side=RIGHT, padx=30, pady=30)

# canvas 1 in frame 1
canvas1 = Canvas(frame1, width=100, height=100, background='white')
canvas1.bind("<Button-1>", mouseDown)
canvas1.bind("<B1-Motion>", mouseMove)
canvas1.pack(side=LEFT, padx=30, pady=30)

# buttons in frame 1
button3 = Button(frame1, text="Add", command=window.quit)
button3.pack(side=RIGHT, padx=30, pady=30)

button2 = Button(frame1, text="Correct", command=correct)
button2.pack(side=RIGHT, padx=30, pady=30)

button1 = Button(frame1, text="Predict", command=predict)
button1.pack(side=RIGHT, padx=30, pady=30)

button0 = Button(frame1, text="Erase", command=erase)
button0.pack(side=RIGHT, padx=30, pady=30)

# canvas 5 in frame 2
canvas5 = Canvas(frame2, width=100, height=100, background='black')
canvas5.pack(side=LEFT, padx=30, pady=30)

# canvas 2 in frame 2
canvas2 = Canvas(frame2, width=100, height=100, background='white')
canvas2.pack(side=LEFT, padx=30, pady=30)

# canvas 3 in frame 2
canvas3 = Canvas(frame2, width=100, height=100, background='white')
canvas3.pack(side=LEFT, padx=30, pady=30)

# canvas 4 in frame 2
canvas4 = Canvas(frame2, width=100, height=100, background='white')
canvas4.pack(side=LEFT, padx=30, pady=30)

# frame 3 in frame 2
frame3 = Frame(frame2, bg="white", borderwidth=2, relief=GROOVE, width=100, height=100)
frame3.pack(side=RIGHT, padx=5, pady=5)
text = StringVar()
text.set("")
Label(frame3, textvariable = text,bg="white").pack(padx=10, pady=10)

base, label, distance_matrix = init(database.get(), 6000)

window.mainloop()

