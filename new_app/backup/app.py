import os
import sys
import PIL
import pickle
import tkFont

from SettingsTab import *
from Tkinter import *
from ttk import *
from PIL import ImageTk
from PIL import Image

class Item():

    def __init__(self, name, image, cost, category, audio, quantities=[1,2,3,4,5,6]):

        self.name = name
        self.image = image
        self.cost = cost
        self.category = category
        self.audio = audio
        self.quantities = quantities

class MainFrame(Frame):

        def __init__(self, master, *pargs):
  	    self.master = master
	    Frame.__init__(self, master, *pargs)
  	    self.customFonts = tkFont.Font(family="Helvetica", size=15)
  	    self.customFonts1= tkFont.Font(family="Helvetica", size=30)
	    
	    #hack here have to look into these
	    self.settingsOn = False

  	    #globals here for now 
  	    self.bgcolor='white'
  	    self.bgcolor1='#FFCC66'
  	    self.backgroundcolor="images/BackGroundWhite.gif"
  	    self.BackgroundImage=self.ImageCreation(self.backgroundcolor)
  	    
	    self.Images = []
  	    self.Names = []
  	    self.Bill_list = []
  	    self.initUI()
        
	def ImageCreation(self,location):
	    img = Image.open(location)
            img1 = img.resize((300,225), Image.ANTIALIAS)
            photoImg1 = PIL.ImageTk.PhotoImage(img1)
            return photoImg1
	
	def Restart(self):
	    self.master.destroy()

	def CallSettingsTab(self):
	    if not self.settingsOn:
		self.settingsOn = True
		self.newWindow = Toplevel(self.master)
	    	#self.app = SetTab.SettingsTab(self.newWindow)
	    	self.app = SettingsTab(self.newWindow)
	    	self.newWindow.grid_columnconfigure(0,weight=1)
	    	self.newWindow.resizable(True,False)
	    	self.newWindow.update()
	    	self.newWindow.geometry(self.newWindow.geometry())
	    	self.newWindow.protocol("WM_DELETE_WINDOW", self.QuitSettingsTab)
    	    	self.newWindow.mainloop()
	
	def QuitSettingsTab(self):
		self.settingsOn = False
		self.newWindow.destroy()

        def initUI(self):
		self.master.title("Bill Printer")
		self.master.columnconfigure(0, weight=1)
	    	self.master.rowconfigure(0, weight=1)
		self.master.resizable(True,True)
		
		self.grid(column=0, row=0, sticky=(N, W, E, S))
	    	self.columnconfigure(0, weight=1)
	    	self.rowconfigure(0, weight=1)
		Style().configure("TFrame",background=self.bgcolor)
                self.style=Style()
		
		Settings=Button(self,text='Settings',command=self.CallSettingsTab)
                Settings.grid(row=0,column=0,padx=5,pady=5,sticky=W)
                restart=Button(self,text='Restart',command=self.Restart)
                restart.grid(row=0,column=3,padx=5,pady=5,sticky=W)
		
		imagesPerRow = 3
		noOfImages = 6  
		noOfRows = noOfImages/imagesPerRow
		startRow = 1
		startColumn = 0
		rowSpan = 10
		columnSpan = 2
		Padding ="5 5 5 5"
		
		row_index = startRow
		for i in range(0,noOfRows):
		    self.Images.append([])
		    self.Names.append([])
		    column_index = startColumn 
		    for j in range(0,imagesPerRow):
			self.Images[i].append(Label(self,image=self.BackgroundImage,background=self.bgcolor,padding=Padding).grid(row=row_index,rowspan=rowSpan,column=column_index,columnspan=columnSpan))
			self.Names[i].append(Label(self,text='',background=self.bgcolor,font=self.customFonts).grid(row=row_index+rowSpan,column=column_index,columnspan=columnSpan)) 
			column_index = column_index + columnSpan
		    row_index = row_index + rowSpan + 1
                
		
		Bill=Label(self,text='Bill  ',background=self.bgcolor1,font=self.customFonts)
                Bill.grid(column=5,row=2,columnspan=8,padx=1,pady=1)
                content1=Label(self,text='No. ',background=self.bgcolor1,font=self.customFonts)
                content1.grid(column=6,row=3,sticky=N+E,padx=1,pady=1)
                Line2=Label(self,relief=SUNKEN,width=0.2)
                Line2.grid(column=7,row=3,rowspan=22,sticky=N+S)
                content2=Label(self,text='  Item  ',background=self.bgcolor1,font=self.customFonts)
                content2.grid(column=8,row=3,sticky=N+E,padx=1,pady=1)
                Line3=Label(self,relief=SUNKEN,width=0.2)
                Line3.grid(column=9,row=3,rowspan=22,sticky=N+S)
                content3=Label(self,text=' Quantity ',background=self.bgcolor1,font=self.customFonts)
                content3.grid(column=10,row=3,sticky=N+E,padx=1,pady=1)
                Line4=Label(self,relief=SUNKEN,width=0.2)
                Line4.grid(column=11,row=3,rowspan=22,sticky=N+S)
                content4=Label(self,text=' Amount ',background=self.bgcolor1,font=self.customFonts)
                content4.grid(column=12,row=3,sticky=N+E,padx=1,pady=1)
                
		for i in range(0,22):
                        a=[0]*4
                        a[0]=Label(self,background=self.bgcolor1,font=self.customFonts)
                        a[0].grid(column=6,row=(4+i),sticky=N+E,padx=1)
                        a[1]=Label(self,background=self.bgcolor1,font=self.customFonts)
                        a[1].grid(column=8,row=(4+i),sticky=N+E,padx=1)
                        a[2]=Label(self,background=self.bgcolor1,font=self.customFonts)
                        a[2].grid(column=10,row=(4+i),sticky=N+E,padx=1)
                        a[3]=Label(self,background=self.bgcolor1,font=self.customFonts)
                        a[3].grid(column=12,row=(4+i),sticky=N+E,padx=15)               
                        self.Bill_list.append(a)
                
		Print=Label(self,text='  Print  ',background=self.bgcolor,relief=SUNKEN,font=("Helvetica",15))
                Print.grid(column=1,columnspan=2,row=24,padx=1,pady=1,sticky=N+W)
		
		Next=Label(self,text='Next Slide',background=self.bgcolor,font=self.customFonts)
                Next.grid(column=4,row=24,padx=1,pady=1,sticky=N+E)

if __name__ == "__main__":
    root = Tk()
    app = MainFrame(root)
    root.mainloop()
