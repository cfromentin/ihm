# -*- coding: utf-8 -*-
import tkinter as tk
import time
from .userinputs import UserInputHandler, OneValueDialog

class Knob(UserInputHandler):
    def __init__(self,app,userinputs, datamanager,unit,title):
        self.app=app
        self.value = datamanager.value
        self.max_range = datamanager.vmax
        self.min_range = datamanager.vmin
        self.step = datamanager.step
        self.selected = False
        self.unit = unit
        self.title = title
        self.userinputs=userinputs
        self.datamanager=datamanager

      
        self.width = int(app.winfo_screenwidth()*0.1)
        self.height = int(app.winfo_screenwidth()*0.1)#120
        self.width = 1 #int(800*0.09)
        self.height = 1 #int(800*0.09)#120

        self.font_size_value = int(self.height*0.2)#22
        self.font_size_unit = int(self.height*0.1)#10
        self.font_size_title = int(self.height*0.12)#15

        self.canvas = tk.Canvas(app, height=self.height, width=self.width)
        coord = int(self.width*0.1), int(self.height*0.1), int(self.width*0.9), int(self.height*0.9)
        self.arc_green = self.canvas.create_arc(coord, start=-45, extent=270, fill="#4E69AB")

        self.arc_grey = self.canvas.create_arc(coord, start=-45, extent=270, fill="grey",tags='knob_value')

        coord = int(self.width*0.2), int(self.height*0.2), int(self.width*0.8), int(self.height*0.8)
        self.circle = self.canvas.create_oval(coord, fill="grey", width=2,tags='knob_circle')

        self.textid = self.canvas.create_text(int(self.width*0.5), int(self.height*0.4), anchor='c', \
                font=("Helvetica", self.font_size_value),fill='white', text=str(0),tags='knob_value_text')
        #self.canvas.create_text(int(self.width*0.5), int(self.height*0.68), anchor='s', \
        #        font=("Helvetica", self.font_size_unit),fill='white', text=self.unit,tags='knob_value_unit')
        self.title_textid = self.canvas.create_text(int(self.width*0.5), int(self.height*0.99), anchor='s', \
                font=("Helvetica", self.font_size_title),fill='grey', text=self.title)

        #self.canvas.create_text(int(self.width*0.2), int(self.height*0.85), anchor='e', \
        #        font=("Helvetica", 12),fill='grey', text=self.min_range)

        #self.canvas.create_text(int(self.width*0.8), int(self.height*0.85), anchor='w', \
        #        font=("Helvetica", 12),fill='grey', text=self.max_range)        
        
        self.canvas.bind('<Configure>',self.configure)
        self.canvas.bind('<ButtonPress-1>',self.onClick)

        self.update(self.value)
    
    def configure(self,event):
        self.width = int(self.canvas.winfo_width())
        self.height = int(self.canvas.winfo_height())
        coord = int(self.width*0.1), int(self.height*0.1), int(self.width*0.9), int(self.height*0.9)
        self.canvas.coords(self.arc_green,coord)
        self.canvas.coords(self.arc_grey,coord)
        coord = int(self.width*0.2), int(self.height*0.2), int(self.width*0.8), int(self.height*0.8)
        self.canvas.coords(self.circle,coord)

        font_size = int(self.width*0.2)
        self.canvas.coords(self.textid,(int(self.width*0.5),int(self.height*0.5)))
        self.canvas.itemconfig(self.textid, font=("Helvetica",font_size))
        
        font_size = int(self.width*0.12)
        self.canvas.coords(self.title_textid,(int(self.width*0.5),int(self.height)))
        self.canvas.itemconfig(self.title_textid, font=("Helvetica",font_size))
        


    def minus_handler(self, big=False):
        inc = 10 if big else 1
        self.update(self.value-self.step*inc)
    def plus_handler(self, big=False):
        inc = 10 if big else 1
        self.update(self.value+self.step*inc)
    def selected_handler(self):
        self.selected = True
        self.canvas.itemconfigure('knob_circle', fill='#c9d2e5')
    def unselected_handler(self):
        self.selected = False
        self.canvas.itemconfigure('knob_circle', fill='gray')



    def update(self,value):
        if value>self.min_range and value <=self.max_range:
            self.value = value
            self.value_norm = 270 - (((self.value/self.max_range) + self.min_range)*270)
            item_txt = self.canvas.find_withtag("knob_value")
            self.canvas.itemconfigure(item_txt,extent=self.value_norm)
            item_txt = self.canvas.find_withtag("knob_value_text")
            self.canvas.itemconfigure(item_txt,text=str(value))
            self.canvas.update_idletasks()
            #self.datamanager.update(value)

    def onClick(self,event):
        OneValueDialog(self.app,self.title+' ('+self.unit+')',self.datamanager)
        self.update(self.datamanager.value)
    #    if self.selected:
    #        self.userinputs.select(None)
    #    else:
    #        self.userinputs.select(self)


# Programme de test

# app = tk.Tk()
# app.wm_title("Graphe Matplotlib dans Tkinter")

# btn1 = Knob(app, 0, 400,0,'MLrfr','VT')
# btn2 = Knob(app, 0, 30,1,'MLrfr','VT')
# btn3 = Knob(app, 0, 50,2,'MLrfr','VT')
# btn1.canvas.pack()
# btn2.canvas.pack()
# btn3.canvas.pack()

# # for i in range(0,400):
# #     btn1.update(i)
# #     btn2.update(i)
# #     btn3.update(i)
# #     time.sleep(0.1)
# app.mainloop()
