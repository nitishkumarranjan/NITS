import os
import sys
import PIL
import pickle
import tkFont
import pygame
import time

from SettingsTab import *
from BillTab import *
from Tkinter import *
from ttk import *
from PIL import ImageTk
from PIL import Image
from copy import deepcopy

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
	    self.initData()
  	    self.initUI()
	    self.ProcessPresentNode()
	
	def initData(self):
	    self.loadSettings()
	    #hack here have to look into these
	    self.settingsOn = False

  	    #globals here for now 
  	    self.bgcolor='white'
  	    self.bgcolor1='#FFCC66'
  	    self.backgroundcolor="images/BackGroundWhite.gif"
  	    self.BackgroundImage=self.ImageCreation(self.backgroundcolor)
	    self.numberImages=["images/num1.gif","images/num2.gif","images/num3.gif","images/num4.gif","images/num5.gif","images/num6.gif"]
  	    
	    self.Images = []
  	    self.Names = []
  	    self.Bill_list = []

	    #should have been in settings.txt 
	    self.imagesPerRow = 3
	    self.noOfImages = 6  
	    self.noOfRows = self.noOfImages/self.imagesPerRow
		
	    #set present state
	    self.setState()

	    #loading root data
	    self.loadRoots()
	
	def loadSettings(self):
	    #loading basic settings from settings.txt
	    g=open('settings.txt','r')
	    d=json.loads(g.readline())
	    self.delay=float(d["delay"])
	    self.mainDelay=float(d["mainDelay"])
	    self.highcolour=d["highlight-color"]
	    self.bcDelay=float(d["bcDelay"])
	    g.close()

	def setState(self):
	    #create a state for present node 
	    self.state={}
	    self.state["isPrev"]=False
	    self.state["loopListIndex"]=-1
	    self.state["billListIndex"]=0
	    self.state["slideNo"]=0
	    self.state["after_id"]=-1
	    self.state["billData"]=[]
	    self.state["billtotal"]=0
	    self.state["bill_no"]=1
	    self.state["loop_list"]=[]
	    self.state["loop_list_names"]=[]
	    self.state["loop_data"]=[]
	    self.state["loop"]=True

	def ImageCreation(self,location):
	    img = Image.open(location)
            img1 = img.resize((300,225), Image.ANTIALIAS)
            photoImg1 = PIL.ImageTk.PhotoImage(img1)
            return photoImg1   
	
	def PlayAudio(self,destination):
	    pygame.mixer.init()
            pygame.mixer.music.load(destination)
            pygame.mixer.music.play()
            while(pygame.mixer.music.get_busy()):
                    pass

	def loadRoots(self):
	    f = open('data.json','r')
	    self.root = json.loads(f.readline())
	    self.state["present_node"] = self.root
	    self.state["prev_node"] = self.root
	    f.close()

	    self.data_root = {}
	    self.data_root["children"] = {}
	    for cat_name in self.root["children"]:
		self.data_root["children"][cat_name]={}
		self.data_root["children"][cat_name]["image"]=self.ImageCreation(self.root["children"][cat_name]["image"])
		self.data_root["children"][cat_name]["image"]=self.ImageCreation(self.root["children"][cat_name]["image"])
		self.data_root["children"][cat_name]["children"]={}
		for item_name in self.root["children"][cat_name]["children"]:
		    self.data_root["children"][cat_name]["children"][item_name]={}
		    self.data_root["children"][cat_name]["children"][item_name]["image"]=self.ImageCreation(self.root["children"][cat_name]["children"][item_name]["image"])
		    self.data_root["children"][cat_name]["children"][item_name]["children"]={}
		    for i in range(0,self.root["children"][cat_name]["children"][item_name]["quantity"]):
			self.data_root["children"][cat_name]["children"][item_name]["children"][str(i+1)]={}
			self.data_root["children"][cat_name]["children"][item_name]["children"][str(i+1)]["image"]=self.ImageCreation(self.numberImages[i])

	    self.state["present_data_node"]=self.data_root
	    self.state["prev_data_node"] = self.data_root

	
	def CreateImageArray(self,Array):
	    New_Array= []
            for i in range(0,len(Array)):
                    New_Array.append(self.ImageCreation(Array[i]))
            return New_Array
	
	def ProcessPresentNode(self):
	    #clear all backgrounds 
	    self.ClearAllBackgrounds()
	    
	    #clear all images 
	    self.ClearAllImages()
	    
	    #get images to be displayed
	    adata_to_display=[]
	    cdata_to_display=[]
	    images_to_display=[]
	    nodes = []
	    if not self.state["present_node"]["children"].has_key('1'): #hack here have to look into it to differentiate leaf parent
		    for each in self.state["present_data_node"]["children"]:
			images_to_display.append(self.state["present_data_node"]["children"][each]["image"])
			adata_to_display.append(self.state["present_node"]["children"][each])
			cdata_to_display.append(self.state["present_data_node"]["children"][each])
	    else:
		    for i in range(0,self.state["present_node"]["quantity"]):
			images_to_display.append(self.state["present_data_node"]["children"][str(i+1)]["image"])
			adata_to_display.append(self.state["present_node"]["children"][str(i+1)])
			cdata_to_display.append(self.state["present_data_node"]["children"][str(i+1)])
	    
	    if self.state["isPrev"]:
		k = self.state["slideNo"]*6
	    else:
		k=0

	    self.state["loop_list"] = []
	    self.state["loop_data"] = []
	    for i in range(0,self.noOfRows):
		for j in range(0,self.imagesPerRow):
		    if k < len(images_to_display):
			self.Images[i][j].configure(image=images_to_display[k])
		    	self.state["loop_list"].append(self.Images[i][j])
			self.Names[i][j].configure(text=adata_to_display[k]["name"])
			data={}
			data["type"]="image"
			data["main"]=adata_to_display[k]
			data["data"]=cdata_to_display[k]
			self.state["loop_data"].append(data)
		    	k = k + 1
	    
	    self.state["loop_list"].append(self.Print)
	    data={}
	    data["type"]="button"
	    data["main"]="print"
	    self.state["loop_data"].append(data)
	    
	    if self.state["isPrev"]:
	        self.state["loop_list"].append(self.Prev)
	    	data={}
	    	data["type"]="button"
	    	data["main"]="prev"
	    	self.state["loop_data"].append(data)
	    
	    if ((self.state["slideNo"]+1)*self.noOfImages < len(images_to_display)):
	        self.state["loop_list"].append(self.Next)
	    	data={}
	    	data["type"]="button"
	    	data["main"]="next"
	    	self.state["loop_data"].append(data)
	    
	    self.state["after_id"]=self.after(100,lambda : self.Interrupt())
	
	def Interrupt(self):
	    #processing for each element
	    if self.state["loop"]:
		if self.state["loopListIndex"] != -1:
	    	    self.state["loop_list"][self.state["loopListIndex"]].configure(background=self.bgcolor)
	    	self.state["loopListIndex"]= (self.state["loopListIndex"]+1) % len(self.state["loop_list"])
	    	self.state["loop_list"][self.state["loopListIndex"]].configure(background=self.highcolour)
            	self.master.bind('<1>', lambda e: self.HandleClick(self.state["loop_data"][self.state["loopListIndex"]]))
	    	if self.state["loop_data"][self.state["loopListIndex"]]["type"]=="image" and self.state["loop_data"][self.state["loopListIndex"]]["main"].has_key("audio"):
	    	    self.after(1,lambda : self.PlayAudio(self.state["loop_data"][self.state["loopListIndex"]]["main"]["audio"]))
	    self.state["after_id"]=self.after(int(1000*self.mainDelay),lambda : self.Interrupt())
	
	def HandleClick(self,data):
	    if data["type"] == "button":
		print data["main"]
		if data["main"]=="prev":
		    self.state["isPrev"]=True
		    self.state["loopListIndex"]=-1
		    self.state["slideNo"]=self.state["slideNo"]-1
		    self.ProcessPresentNode()
		elif data["main"]=="next":
		    self.state["isPrev"]=True
		    self.state["loopListIndex"]=-1
		    self.state["slideNo"]=self.state["slideNo"]+1
		    self.ProcessPresentNode()
		elif data["main"]=="print":
		    self.SendBillToProcess()
	    elif data["type"] == "image":
		self.after_cancel(self.state["after_id"])
		print data["main"]["name"]
		self.ClearAllBackgrounds()
		self.state["isPrev"]=False
		self.state["loopListIndex"]=-1
		self.state["slideNo"]=0
		if not data["main"]["isleaf"]:
		    self.state["prev_node"] = self.state["present_node"]
		    self.state["present_node"] = data["main"]
		    self.state["prev_data_node"] = self.state["present_data_node"]
		    self.state["present_data_node"]=data["data"]
		else:
		    temp={}
		    print self.state["present_node"]
		    temp["itemName"]=self.state["present_node"]["name"]
		    temp["cost"]=int(self.state["present_node"]["cost"])
		    temp["quantity"]=int(data["main"]["name"])
		    self.addToBillLog(temp)
		    self.loadRoots()
		self.ProcessPresentNode()
	
	def addToBillLog(self,data):
	    self.Bill_list[self.state["billListIndex"]][0].configure(text=str(self.state["billListIndex"]+1))
	    self.Bill_list[self.state["billListIndex"]][1].configure(text=str(data["itemName"]))
	    self.Bill_list[self.state["billListIndex"]][2].configure(text=str(data["quantity"]))
	    self.Bill_list[self.state["billListIndex"]][3].configure(text=str(data["cost"]*data["quantity"]))
	    self.state["billData"].append( str(data["itemName"])+" X "+str(data["quantity"])+" = "+str(data["cost"]*data["quantity"]))
	    self.state["billtotal"] = self.state["billtotal"] + data["cost"]*data["quantity"]
	    self.billTotal.configure(text=self.state["billtotal"])
	    self.state["billListIndex"]=self.state["billListIndex"]+1
	
	def ClearAllImages(self):
	    print self.Images
	    for i in range(0,self.noOfRows):
		for j in range(0,self.imagesPerRow):
		    self.Images[i][j].configure(image=self.BackgroundImage)
		    self.Names[i][j].configure(text='')
	
	def ClearAllBackgrounds(self):
	    for each in self.state["loop_list"]:
		each.configure(background=self.bgcolor)
	   	
	def ClearBillLog(self):
	    for i in range(0,self.state["billListIndex"]+1):
                self.Bill_list[i][0].configure(text='')
                self.Bill_list[i][1].configure(text='')
                self.Bill_list[i][2].configure(text='')
                self.Bill_list[i][3].configure(text='')
	    self.billTotal.configure(text='0')
	    self.state["billData"]=[]
	    self.state["billtotal"]=0
	    self.state["billListIndex"]=0
	
	def SendBillToProcess(self):
	    if len(self.state["billData"]) > 0:
		self.newWindow = Toplevel(self.master)
		self.state["billData"].append("total:"+str(self.state["billtotal"]))
	    	BillTab(self.newWindow,self.state["billData"],self.state["bill_no"])
		self.ClearBillLog()
	    	self.newWindow.resizable(True,False)
	    	self.newWindow.update()
	    	self.newWindow.geometry(self.newWindow.geometry())
    	    	self.newWindow.mainloop()
	
	def Restart(self):
	    self.after_cancel(self.state["after_id"])
	    self.loadSettings()
	    self.setState()
	    self.loadRoots()
	    self.ProcessPresentNode()
	    self.ClearBillLog()
    	
	def CallSettingsTab(self):
	    if not self.settingsOn:
		self.settingsOn = True
		self.newWindowS = Toplevel(self.master)
	    	self.app = SettingsTab(self.newWindowS)
	    	self.newWindowS.grid_columnconfigure(0,weight=1)
	    	self.newWindowS.resizable(True,False)
	    	self.newWindowS.update()
	    	self.newWindowS.geometry(self.newWindowS.geometry())
	    	self.newWindowS.protocol("WM_DELETE_WINDOW", self.QuitSettingsTab)
    	    	self.newWindowS.mainloop()
	
	def QuitSettingsTab(self):
		self.settingsOn = False
		self.after_cancel(self.state["after_id"])
	    	self.loadSettings()
	    	self.setState()
	    	self.loadRoots()
	    	self.ProcessPresentNode()
		self.newWindowS.destroy()

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
		self.pack(fill=BOTH, expand=1)
		
		Settings=Button(self,text='Settings',command=self.CallSettingsTab)
                Settings.grid(row=0,column=0,padx=5,pady=5,sticky=N+W)
                restart=Button(self,text='Restart',command=self.Restart)
                restart.grid(row=0,column=3,padx=5,pady=5,sticky=N+W)
		

		startRow = 1
		startColumn = 0
		rowSpan = 10
		columnSpan = 2
		Padding ="5 5 5 5"
		
		row_index = startRow
		for i in range(0,self.noOfRows):
		    self.Images.append([])
		    self.Names.append([])
		    column_index = startColumn 
		    for j in range(0,self.imagesPerRow):
			print "row,col ",row_index,column_index
			self.Images[i].append(Label(self,image=self.BackgroundImage,background=self.bgcolor,padding=Padding))
			self.Images[i][j].grid(row=row_index,rowspan=rowSpan,column=column_index,columnspan=columnSpan)
			self.Names[i].append(Label(self,text='',background=self.bgcolor,font=self.customFonts))
			self.Names[i][j].grid(row=row_index+rowSpan,column=column_index,columnspan=columnSpan) 
			column_index = column_index + columnSpan
		    row_index = row_index + rowSpan + 1
                
		
		Bill=Label(self,text='BILL ',background=self.bgcolor,font=self.customFonts)
                Bill.grid(column=9,row=2,columnspan=2,padx=5,pady=5)
                content1=Label(self,text='No. ',background=self.bgcolor,font=self.customFonts)
                content1.grid(column=6,row=3,sticky=N+E,padx=5,pady=5)
                Line2=Label(self,relief=SUNKEN,width=0.2)
                Line2.grid(column=7,row=3,rowspan=15,sticky=N+S)
                content2=Label(self,text='  Item  ',background=self.bgcolor,font=self.customFonts)
                content2.grid(column=8,row=3,sticky=N+E,padx=5,pady=5)
                Line3=Label(self,relief=SUNKEN,width=0.2)
                Line3.grid(column=9,row=3,rowspan=15,sticky=N+S)
                content3=Label(self,text=' Quantity ',background=self.bgcolor,font=self.customFonts)
                content3.grid(column=10,row=3,sticky=N+E,padx=5,pady=5)
                Line4=Label(self,relief=SUNKEN,width=0.2)
                Line4.grid(column=11,row=3,rowspan=15,sticky=N+S)
                content4=Label(self,text=' Amount ',background=self.bgcolor,font=self.customFonts)
                content4.grid(column=12,row=3,sticky=N+E,padx=5,pady=5)
                
		for i in range(0,15):
                        a=[0]*4
                        a[0]=Label(self,background=self.bgcolor,font=self.customFonts)
                        a[0].grid(column=6,row=(4+i),sticky=N+E,padx=5)
                        a[1]=Label(self,background=self.bgcolor,font=self.customFonts)
                        a[1].grid(column=8,row=(4+i),sticky=N+E,padx=5)
                        a[2]=Label(self,background=self.bgcolor,font=self.customFonts)
                        a[2].grid(column=10,row=(4+i),sticky=N+E,padx=5)
                        a[3]=Label(self,background=self.bgcolor,font=self.customFonts)
                        a[3].grid(column=12,row=(4+i),sticky=N+E,padx=5)               
                        self.Bill_list.append(a)
	        
		content5=Label(self,text=' Total: ',background=self.bgcolor,font=self.customFonts)
                content5.grid(column=10,row=19,sticky=N+E,padx=5,pady=5)
		self.billTotal=Label(self,text='0',background=self.bgcolor,font=self.customFonts)
		self.billTotal.grid(column=11,row=19,sticky=N+E,padx=5,pady=5)
	
		self.Prev=Label(self,text='Prev Slide',background=self.bgcolor,font=self.customFonts)
                self.Prev.grid(column=1,row=24,padx=5,pady=10,sticky=N+W)
		self.Next=Label(self,text='Next Slide',background=self.bgcolor,font=self.customFonts)
                self.Next.grid(column=3,row=24,padx=5,pady=10,sticky=N+W)
		self.Print=Label(self,text='  Print  ',background=self.bgcolor,relief=SUNKEN,font=("Helvetica",20))
                self.Print.grid(column=9,columnspan=2,row=22,rowspan=2,padx=5,pady=10)


if __name__ == "__main__":
    root = Tk()
    app = MainFrame(root)
    root.mainloop()
