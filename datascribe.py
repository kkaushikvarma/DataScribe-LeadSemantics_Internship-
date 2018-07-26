import matplotlib.pyplot as plt
import numpy as np
import datetime
from math import *
import operator
import statistics
import random

from process_csv import Process_CSV, DataFrame_2D
from grammar import Constructor, parse

data = Process_CSV('stocks.csv')
data.labels_row = False
data.set_axis("x",1,'datetime','%b %d %Y')
data.set_axis("y",2,'float', None)
data.variable_col = 0
data = data.transform()






import sys
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import *
from PIL import Image, ImageTk


class GUI:
    def __init__(self,i):
        trend = DataFrame_2D(i[0],i[1],None)
        self.stack = []
        self.stack.append(trend)
        
        
        self.main_gui(trend)
        
        
    def main_gui(self,trend):
        self.root = Tk()
        self.trend = trend
        naframe = Frame(self.root)
        naframe.pack(side= TOP)
        frame = Frame(self.root, padx=20, pady=20)
        
        bottomframe = Frame(self.root, padx=20, pady=20)
        bottomframe.pack( side = "bottom", expand = True)
        frame.pack(side = "bottom",expand = True, fill = "both")
        obj = Constructor(trend)
        period = obj.datex
        txt =  obj.get_string
        viz = trend.visualize()
#        print("\n".join(txt))
        def sh1():
            new_trend = self.trend.trends[1][0]
            
            if len(new_trend.data) > 10:
                nt = DataFrame_2D(new_trend.label,new_trend.data,self.trend.initial_date)
                if nt.trends != None:
                    self.root.destroy()
                    self.stack.append(self.trend)
                    self.main_gui(nt)
        def sh2():
            new_trend = self.trend.trends[1][1]
            
            if len(new_trend.data) > 10:
                nt = DataFrame_2D(new_trend.label,new_trend.data,self.trend.initial_date)
                if nt.trends != None:
                    self.root.destroy()
                    self.stack.append(self.trend)
                    self.main_gui(nt)
        def back():
            if self.stack != []:
                trend = self.stack.pop()
                self.root.destroy()
                self.main_gui(trend)
        canvas = None
        def again():
            self.root.destroy()
            self.main_gui(trend)
                
        d1 = StringVar()
        d2 = StringVar()
        im1 = Image.open("ic1.png")
        ph1 = ImageTk.PhotoImage(im1)
        im2 = Image.open("ic2.png")
        ph2 = ImageTk.PhotoImage(im2)
        im3 = Image.open("ic3.png")
        ph3 = ImageTk.PhotoImage(im3)
        
        cent_lab = Label(frame, text=period, fg = "#2f3542",relief = "raised", font = ("Helvetica 14 bold"), padx=8)
        cent_lab.pack(side = LEFT)
        bx1 = Button(frame, image = ph1 , fg="red",relief = "flat",command = back, padx = 50)
        bx1.pack(side = RIGHT)
        bx2 = Button(frame, image = ph2 , fg="red",command = again, padx = 50,relief = "flat")
        bx2.pack(side = RIGHT)  
        nframe = Frame(bottomframe)
        nframe.pack(side = TOP)
        nframe2 = Frame(bottomframe)
        nframe2.pack(side = BOTTOM)
        
        
        
        lb1 = Label(nframe, textvariable = d1, fg = "#2f3542", anchor = "w", font = ("Helvetica 10 bold"),justify = LEFT, width = 56)
        lb1.pack( side = LEFT, fill = "both")
        lb2 = Label(nframe2, textvariable = d2, fg = "#2f3542", anchor = "w", font = ("Helvetica 10 bold"),justify = LEFT, width = 56)
        lb2.pack( side = LEFT, fill = "both")
        button1 = Button(nframe, image = ph3 ,relief = "flat", fg="red", command = sh1)
        button1.pack( side = RIGHT)
        button2 = Button(nframe2, image = ph3 ,relief = "flat", fg="red", command = sh2)
        button2.pack( side = RIGHT)
        try:
            d1.set(txt[0].replace('\033[1m','').replace('\033[0m',''))
        except:
            back()
        try:
            
            d2.set(txt[1].replace('\033[1m','').replace('\033[0m',''))
        except:
            d2.set('')

        canvas = FigureCanvasTkAgg(viz, naframe)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        self.root.mainloop()


i = data[0]
#GUI(i)

#
#def recurs(i,date=None):
#    if date == None:
#        trend = DataFrame_2D(i[0],i[1],None)
#    else:
#        print("yayy")
#        trend = DataFrame_2D(i.label,i.data,date)
#    if trend.trends != None:
#        print(Constructor(trend).get_string)
#        trend.visualize()
#        for new_trend in trend.trends[1]:
#            print(new_trend.raw)
#            if len(new_trend.data) > 10:
#                print(len(new_trend.data))
#                recurs(new_trend,trend.initial_date)
##    
#AAPL = data[0]
#recurs(AAPL)
#AAPL = data[1]
#recurs(AAPL)
#AAPL = data[2]
#recurs(AAPL)
#AAPL = data[3]
#recurs(AAPL)
#AAPL = data[4]
#recurs(AAPL)

#for i in AAPL:
#    
#    trends = i.get_frame()
#    local = []
#    for trend in trends[1]:
#        if len(trend.data) > 8:
#            la = DataFrame_2D(i.label,trend.data,i.initial_date)
#            print(Constructor(la).get_string)
#            la.visualize()
#            
#            
#    print(Constructor(i).get_string)
#    i.visualize()

    
