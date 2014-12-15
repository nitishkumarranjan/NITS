###
#                       My code is hell lot of confusing even to me
#                       SO do bear with it.
#                       Apologies in advance
#
#
###

import os
from Tkinter import Tk
from Tkinter import *
from ttk import *
import math
from PIL import *
import time
import thread
import threading
import Queue
import signal
import PIL
import pygame
from PIL import ImageTk
from PIL import Image
import pickle
import tkFont
import ttk
import tkFileDialog
import tkColorChooser as tkcc
#################################################Data Retrival################################################################

Bill_list=[]
Slide=0
No_of_Windows=6
Bill_Items=[]
CurrentItem=0
Counter=[]
Bill=0
Next=0
Item_Names=[]
Item_Images=[]
F_Item_Images=[]
F_Item_Names=[]
D_Item_Images=[]
D_Item_Names=[]
Audio=[]
DAudio=[]
FAudio=[]
Cost=[]

class Item():

    def __init__(self, name, image, cost, category, audio, quantities=[1,2,3,4,5,6]):

        self.name = name
        self.image = image
        self.cost = cost
        self.category = category
        self.audio = audio
        self.quantities = quantities

pklFile = open('data.pkl', 'r')
itemList=pickle.load(pklFile)
pklFile.close()

for i in range(0,len(itemList)):
        
        if itemList[i].category=='Food':
                F_Item_Names.append(itemList[i].name)
                F_Item_Images.append(itemList[i].image)
                FAudio.append(itemList[i].audio)
        if itemList[i].category=='Drink':
                D_Item_Names.append(itemList[i].name)
                D_Item_Images.append(itemList[i].image)
                DAudio.append(itemList[i].audio)
        Item_Names.append(itemList[i].name)
        Item_Images.append(itemList[i].image)
        Cost.append(int(itemList[i].cost))
        #Audio.append(itemList[i].audio)
#################################################Constant Declaration###########################################################
Images=6*[0]
Names=6*[0]
backgroundcolor="images/BackGroundWhite.gif"
bgcolor='white'
Number=len(Item_Names)
Number_Names=["One","Two","Three","Four","Five","Six"]
Bill_text='Bill'
loc="Default.gif"
Number_Image=["images/num1.gif","images/num2.gif","images/num3.gif","images/num4.gif","images/num5.gif","images/num6.gif"]
Category_Names=["Food","Drinks"]
Category_Image=["images/food.gif","images/drinks.gif"]
q=1
w=1
ind=-10
quant=-10
App_Wid=300
M_perRow=10
Total_Number=len(Item_Names)
row_number=[i for i in range(0,20)]
column_number=[i for i in range(0,15)]
customFont=0
customFont1=0
#################################################Settings Details###########################################################
#Constants in Settings#
color=0
move_delay=0
click_delay=0


# Reading Settings#
g=open('settings.txt','r')
f=g.read()
h=f.replace(' ','\n')
h=h.replace('\r','\n')
h=h.split('\n')
delay=h[h.index('delay')+2]
move_delay=float(delay)
delay=h[h.index('mainDelay')+2]
click_delay=float(delay)
color=h[h.index('highlight-color')+2]
g.close()

############################################################################################################################
## TO MAKE THE APP GO FULLSCREEN ##

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        self._geomprev=self._geom
        geom=self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom=geom

##  READING PARAMETERS FROM SETTINGS.TXT  ####
def SettingsTab():
        os.system('python Settings_Tab.py')
while(q):
    if(w*App_Wid<1000):
        w=w+1
        #print(w)
    else:
        w=w-1
        #print(w)
        q=0
if(w*App_Wid<App_Wid*M_perRow):
    Max=w
else:
    Max=M_perRow

def restart_thread():
        os.system("python Run.py")

def Restart():
        thread.start_new_thread(restart_thread,())
        quit()
        
###  IF REFRESH IS NEEDED OR NOT   ##

##  COUNTER AND DIFFERENT THREADS ##
count=0

def first_thread():
        global count
        while(True):
                time.sleep(move_delay)
                count=count+1


def Audio_player(destination):
        pygame.mixer.init()
        pygame.mixer.music.load(destination)
        pygame.mixer.music.play()
        while(pygame.mixer.music.get_busy()):
                pass
                        


def second_thread(Print,Bill):
        global Images
        global Names
        global Next
        global CurrentItem
        prevcount=-1
        while(True):
                time.sleep(1)
#               ImageArray=[x for x in Names if x!=0]
#               ImageArray=[x for x in ImageArray if x["foreground"]!=bgcolor]
                #ImageArray=[x for x in ImageArray if x["image"]!=(BackgroundImage,)]
                length=No_of_Windows
                
                if(Names[0]["text"]==F_Item_Names[0]):
                        print "Went in he123re!"
                        for i in range(0,length+2):
                                if(count==prevcount):
                                    pass
                                elif(count%(length+2)==i):
                                        prevcount=count
                                        for j in Images[0:length]:
                                                try:
                                                        j.configure(background=bgcolor)
                                                except:
                                                        pass
                                                Print.configure(background=bgcolor)
                                                Bill.configure(background=bgcolor)
                                                Next.configure(background=bgcolor)
                                        if i==length+1:
                                                Print.configure(background=color)
                                        elif i==length:
                                                Next.configure(background=color)
                                        else:
                                                Images[i].configure(background=color)
                                                CurrentItem=i
                                                Audio_player(FAudio[i])
                elif(Names[0]["text"]==D_Item_Names[0]):
                        print "Went in here!"
                        for i in range(0,length+2):
                                if(count==prevcount):
                                    pass
                                elif(count%(length+2)==i):
                                        prevcount=count
                                        for j in Images[0:length]:
                                                try:
                                                        j.configure(background=bgcolor)
                                                except:
                                                        pass
                                                Print.configure(background=bgcolor)
                                                Bill.configure(background=bgcolor)
                                                Next.configure(background=bgcolor)
                                        if i==length+1:
                                                Print.configure(background=color)
                                        elif i==length:
                                                Next.configure(background=color)
                                        else:
                                                Images[i].configure(background=color)
                                                CurrentItem=i
                                                Audio_player(DAudio[i])
                else:
                        print "Went in else!"
                        for i in range(0,length+1):
                                if (count%(length+1)==i):
                                        for j in Images[0:length]:
                                                try:
                                                        j.configure(background=bgcolor)
                                                except:
                                                        pass
                                                Print.configure(background=bgcolor)
                                                Bill.configure(background=bgcolor)
                                        if i==length:
                                                Print.configure(background=color)
                                        else:
                                                Images[i].configure(background=color)
                                                CurrentItem=i
                                                #print "IS it really here????"
                                                #Audio_player(Audio[i])
                                                #print "Then here????"


        
        


##  IMAGE CREATION OF SPECIFIC SIZE  ##


def ImageCreation(location):
        img = Image.open(location)
        img1 = img.resize((300,225), Image.ANTIALIAS)
        photoImg1 = PIL.ImageTk.PhotoImage(img1)
        return photoImg1
        

def CreateImageArray(Array):
        New_Array=len(Array)*[0]
        for i in range(0,len(Array)):
                New_Array[i]=ImageCreation(Array[i])
        return New_Array

def ShowArray(ImageArray,TextArray,Curr_slide):
        global Images
        global Names
        global Slide
        global No_of_Windows
        a=(len(ImageArray)-Slide*6)/6
        b=(len(ImageArray)-Slide*6)%6
                
        for j in Images:
                j.configure(image=BackgroundImage,background=bgcolor)
        for k in Names:
                k.configure(text='')
        if(Curr_slide==1):
                Slide=Slide+1
                if(a==0):
                        TextArray1=TextArray[-b:]
                        ImageArray1=ImageArray[-b:]
                        No_of_Windows=b
                else:
                        TextArray1=TextArray[6*Slide:6*(Slide+1)]
                        ImageArray1=ImageArray[6*Slide:6*(Slide+1)]
                        No_of_Windows=6
                if(len(ImageArray)>6):
                        TextArray1=TextArray[0:6]
                        ImageArray1=ImageArray[0:6]
                else:
                        TextArray1=TextArray
                        ImageArray1=ImageArray
                        Num=len(ImageArray)

        else:
                Slide=0
                if(len(ImageArray)>6):
                        TextArray1=TextArray[0:6]
                        ImageArray1=ImageArray[0:6]
                else:
                        TextArray1=TextArray
                        ImageArray1=ImageArray
                        No_of_Windows=len(ImageArray)
        Num=No_of_Windows
        for i in range(0,Num):
                try:
                        Images[i].configure(image=ImageArray1[i])
                        Names[i].configure(text=TextArray1[i])
                except:
                        pass

        
def ClickEvent(master,Floor):
        global count
        global Bill_Items
        global ind
        global quant
        
        if Floor==0:
                i=count%3
                if i==2:
                        PrintBill()
                if i==1:
#                       print "GOING TO LEVEL !!!!!!!!!!!!!!!!!!"
#                       CleanSlate()
                        ShowArray(D_Item_Images,D_Item_Names,0)
                if i==0:
#                       print "GOING TO LEVEL @@@@@@@@@@@@@@@@@@"
#                       CleanSlate()
                        ShowArray(F_Item_Images,F_Item_Names,0)
                count=0
        if Floor==1:
                if Names[0]["text"]==F_Item_Names[0]:
                        ind=Item_Names.index(F_Item_Names[CurrentItem])
                if Names[0]["text"]==D_Item_Names[0]:
                        ind=Item_Names.index(D_Item_Names[CurrentItem])
#               CleanSlate()
                ShowArray(Number_Image,Number_Names,0)
                count=0
        if Floor==2:
#               CleanSlate()
                ShowArray(Category_Image,Category_Names,0)
                quant=CurrentItem+1
                if((quant>=0)&(ind>=0)):
                        Bill_Items.append([ind,quant])
                        Bill_Change()
                        ind=-10
                        quant=-10
                count=0

def Bill_Change():
        global Bill_list
        for i in range(0,len(Bill_Items)):
                Bill_list[i][0].configure(text=str(i+1)+'.')
                Bill_list[i][1].configure(text=Item_Names[Bill_Items[i][0]])
                Bill_list[i][2].configure(text=str(Bill_Items[i][1]))
                Bill_list[i][3].configure(text=str(Cost[Bill_Items[i][0]]*Bill_Items[i][1]))
#               Label(master,text=Item_Names[Bill_Items[i][0]],background=bgcolor,font=customFont).grid(column=6,row=(4+i),sticky=N+E)
#               Label(master,text=Item_Names[Bill_Items[i][0]],background=bgcolor,font=customFont).grid(column=8,row=(4+i),sticky=N+E)
#               Label(master,text=str(Bill_Items[i][1]),background=bgcolor,font=customFont).grid(column=10,row=(4+i),sticky=N+E)
#               Label(master,text=str(Cost[Bill_Items[i][0]]*Bill_Items[i][1]),background=bgcolor,font=customFont).grid(column=12,row=(4+i),sticky=N+E)
#               Total_Bill=Total_Bill+(Item_Names[Bill_Items[i][0]]).ljust(10)+(str(Bill_Items[i][1])).rjust(5)+(str(Cost[Bill_Items[i][0]]*Bill_Items[i][1])).rjust(10)+'\n'
        

def PrintBill():
        global Bill_Items
        print "Is it coming here?"
        global Bill
        w=open('Bill.txt','w')
        w.write('Bill\n')
        for i in range(0,len(Bill_Items)):
                try:
                        w.write(Item_Names[Bill_Items[i][0]]+" X "+str(Bill_Items[i][1])+" = "+str(Cost[Bill_Items[i][0]]*Bill_Items[i][1])+'\n')
                except:
                        print i
        w.close()
        clean_slate()
        Bill_Items=[]
        os.system('python Bill_change.py')
        
        
def clean_slate():
        global Bill_list
        for i in range(0,len(Bill_Items)):
                Bill_list[i][0].configure(text='')
                Bill_list[i][1].configure(text='')
                Bill_list[i][2].configure(text='')
                Bill_list[i][3].configure(text='')
        
        
def third_thread(master):
        while(True):
                time.sleep(0.1)
#               ImageArray=[x for x in Images if x!=0]
                length=No_of_Windows
#               print "The value of the variable is :"+str(count%(length+1))
                if Names[0]["text"]==Category_Names[0]:
#                       print "DID this ah[[en?"
                        if count%(length+1)==length:                            
                                master.bind('<1>', lambda e: PrintBill())
                        else:
                                master.bind('<1>', lambda e: ClickEvent(master,0))
                if((Names[0]["text"]==F_Item_Names[0])):
                        if count%(length+2)==length+1:
                                master.bind('<1>', lambda e: PrintBill())
                        elif count%(length+2)==length:
                                master.bind('<1>', lambda e: ShowArray(F_Item_Images,F_Item_Names,1))
                        else:
                                master.bind('<1>', lambda e: ClickEvent(master,1))
                if((Names[0]["text"]==D_Item_Names[0])):
                        if count%(length+2)==length+1:
                                master.bind('<1>', lambda e: PrintBill())
                        elif count%(length+2)==length:
                                master.bind('<1>', lambda e: ShowArray(D_Item_Images,D_Item_Names,1))
                        else:
                                master.bind('<1>', lambda e: ClickEvent(master,1))
                if Names[0]["text"]==Number_Names[0]:
                        if count%(length+1)==length:
                                master.bind('<1>', lambda e: PrintBill())
                        else:
                                master.bind('<1>', lambda e: ClickEvent(master,2))              


class App(Frame):

        def __init__(self,parent):
                global customFont
                global customFont1
                Frame.__init__(self,parent)
                self.parent=parent
                self.initUI(parent)
                self.customFonts = tkFont.Font(family="Helvetica", size=15)
                self.customFonts1= tkFont.Font(family="Helvetica", size=30)
                customFont=self.customFonts
                customFont1=self.customFonts1   
                
        def initUI(self,parent):
                global Bill
                global Next
                global Images
                global Names
                global Bill_list
                self.parent.title("Bill Printer")
                Style().configure("TFrame",background=bgcolor)
                self.style=Style()
                self.pack(fill=BOTH,expand=1)
                self.columnconfigure(Max,weight=1,pad=10)
                Settings=Button(self,text='Settings',command=SettingsTab)
                Settings.grid(row=0,column=0,padx=10,pady=10,sticky=W)
                restart=Button(self,text='Restart',command=Restart)
                restart.grid(row=0,column=3,padx=10,pady=10,sticky=W)
                #FIRST ROW
                Images[0]=Label(self,image=BackgroundImage,background=bgcolor,padding="5 5 5 5")
                Images[0].grid(row=1,rowspan=10,column=0,columnspan=2)
                Names[0]=Label(self,text='',background=bgcolor,font=customFont)
                Names[0].grid(row=11,column=0,columnspan=2)
                
                Images[1]=Label(self,image=BackgroundImage,background=bgcolor,padding="5 5 5 5")
                Images[1].grid(row=1,rowspan=10,column=2)
                Names[1]=Label(self,text='',background=bgcolor,font=customFont)
                Names[1].grid(row=11,column=2)
                
                Images[2]=Label(self,image=BackgroundImage,background=bgcolor,padding="5 5 5 5")
                Images[2].grid(row=1,rowspan=10,column=3)
                Names[2]=Label(self,text='',background=bgcolor,font=customFont)
                Names[2].grid(row=11,column=3)
                #SECOND ROW
                Images[3]=Label(self,image=BackgroundImage,background=bgcolor,padding="5 5 5 5")
                Images[3].grid(row=12,rowspan=10,column=0,columnspan=2)
                Names[3]=Label(self,text='',background=bgcolor,font=customFont)
                Names[3].grid(row=23,column=0,columnspan=2)
                
                Images[4]=Label(self,image=BackgroundImage,background=bgcolor,padding="5 5 5 5")
                Images[4].grid(row=12,rowspan=10,column=2)
                Names[4]=Label(self,text='',background=bgcolor,font=customFont)
                Names[4].grid(row=23,column=2)
                
                Images[5]=Label(self,image=BackgroundImage,background=bgcolor,padding="5 5 5 5")
                Images[5].grid(row=12,rowspan=10,column=3)
                Names[5]=Label(self,text='',background=bgcolor,font=customFont)
                Names[5].grid(row=23,column=3)
                
                ShowArray(Category_Image,Category_Names,0)
                Print=Label(self,text='  Print  ',background=bgcolor,relief=SUNKEN,font=("Helvetica",25))
                Print.grid(column=5,columnspan=8,row=1,padx=15,pady=5)
                Bill=Label(self,text='Bill  ',background=bgcolor,font=customFont)
                Bill.grid(column=5,row=2,columnspan=8,padx=10,pady=10)
                content1=Label(self,text='No. ',background=bgcolor,font=customFont)
                content1.grid(column=6,row=3,sticky=N+E,padx=5,pady=5)
                Line2=Label(self,relief=SUNKEN,width=0.2)
                Line2.grid(column=7,row=3,rowspan=22,sticky=N+S)
                content2=Label(self,text='  Item  ',background=bgcolor,font=customFont)
                content2.grid(column=8,row=3,sticky=N+E,padx=5,pady=5)
                Line3=Label(self,relief=SUNKEN,width=0.2)
                Line3.grid(column=9,row=3,rowspan=22,sticky=N+S)
                content3=Label(self,text=' Quantity ',background=bgcolor,font=customFont)
                content3.grid(column=10,row=3,sticky=N+E,padx=5,pady=5)
                Line4=Label(self,relief=SUNKEN,width=0.2)
                Line4.grid(column=11,row=3,rowspan=22,sticky=N+S)
                content4=Label(self,text=' Amount ',background=bgcolor,font=customFont)
                content4.grid(column=12,row=3,sticky=N+E,padx=15,pady=5)
                for i in range(0,22):
                        a=[0]*4
                        a[0]=Label(self,background=bgcolor,font=customFont)
                        a[0].grid(column=6,row=(4+i),sticky=N+E,padx=5)
                        a[1]=Label(self,background=bgcolor,font=customFont)
                        a[1].grid(column=8,row=(4+i),sticky=N+E,padx=5)
                        a[2]=Label(self,background=bgcolor,font=customFont)
                        a[2].grid(column=10,row=(4+i),sticky=N+E,padx=5)
                        a[3]=Label(self,background=bgcolor,font=customFont)
                        a[3].grid(column=12,row=(4+i),sticky=N+E,padx=15)               
                        Bill_list.append(a)
                Next=Label(self,text='Next Slide',background=bgcolor,font=customFont)
                Next.grid(column=4,row=25,padx=10,pady=10,sticky=N+E)
                thread.start_new_thread(second_thread,(Print,Bill))
                thread.start_new_thread(third_thread,(parent,))

root=Tk()
thread.start_new_thread(first_thread,())
Item_Images=CreateImageArray(Item_Images)
Category_Image=CreateImageArray(Category_Image)
Number_Image=CreateImageArray(Number_Image)
F_Item_Images=CreateImageArray(F_Item_Images)
D_Item_Images=CreateImageArray(D_Item_Images)
BackgroundImage=ImageCreation(backgroundcolor)
outerapp=FullScreenApp(root)
app=App(root)
root.mainloop()
        
