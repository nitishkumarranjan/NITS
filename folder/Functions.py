from Tkinter import *
import ttk
import tkFileDialog
import math
import tkColorChooser as tkcc
import pickle
import pygame
import pyaudio,wave,sys



def updateFile():
    global delay, mainDelay
    g=open('settings.txt','r+')
    delay = float(delay)
    mainDelay = float(mainDelay)
    f=g.read()
    print(f)
    g.seek(8)
    g.write(str(delay))
    g.write("\n")
    g.seek(24)
    g.write(str(mainDelay))
    g.write("\n")
    g.seek(0)
    f=g.read()
    print(f)
    g.close()

def updateDelay(*args):
    global delay,mainDelay
    try:
        if float(delayString.get()) < 1 or float(mainDelayString.get()) < 1:
             message.set("Please enter a number greater than 1.")
        else:
             message.set("")
             delay = float(delayString.get())
             mainDelay = float(mainDelayString.get())
    except ValueError:
        pass
    updateFile()

def decDelay():
    global delay
    delay = int((delay*10) - 1)/10
    if delay < 1:
        message.set("Value can't reduce below 1.")
        delay = int((delay*10) + 1)/10
    else:
        message.set("")
    delayString.set(delay)
    updateFile()
    
def incDelay():
    global delay
    message.set("")
    delay = int((delay*10) + 1)/10
    delayString.set(delay)
    updateFile()

def mdecDelay():
    global mainDelay
    mainDelay = int((mainDelay*10) - 1)/10
    if mainDelay < 1:
        message.set("Value can't reduce below 1.")
        mainDelay = int((mainDelay*10) + 1)/10
    else:
        message.set("")
    mainDelayString.set(mainDelay)
    updateFile()

def mincDelay():
    global mainDelay
    message.set("")
    mainDelay = int((mainDelay*10) + 1)/10
    mainDelayString.set(mainDelay)
    updateFile()

def changeColour1():
    global colour1,colFrame1
    (rgb, hexColour) = tkcc.askcolor()
    colour1 = hexColour
    print(colour1)
    colFrame1.config(bg = hexColour)
    
def changeColour2():
    global colour2,colFrame2
    (rgb, hexColour) = tkcc.askcolor()
    colour2 = hexColour
    print(colour2)
    colFrame2.config(bg = hexColour)

class Item():

    

    def __init__(self, name, image, cost, category):

        self.name = name
        self.image = image

        self.cost = cost
        self.category = category



    def changeCost(self, newCost):

        self.cost = newCost

    def printAll(self):
        print("Name : ",self.name)
        print("Cost : ",self.cost)

def picNameUpdater() :
    global itemToAdd, imageName
    itemToAdd = filedialog.askopenfilename(title = "Choose picture to add")
    itemToAdd = itemToAdd[itemToAdd.rfind('/')+1:]
    imageName.set(imageName)
    
def addItem():
    global itemName, imageName, itemCost, categoryName, itemList, itemComboBox, priceComboBox
    audioString.set('sounds/' + itemName.get()+'.wav')
    print "***AUDIO*** "+audioString;
    newItem = Item(itemName.get(), imageName.get(), int(itemCost.get()), categoryName.get())
    itemName.set('')
    imageName.set('')
    itemCost.set('')
    categoryName.set('')
    itemList.append(newItem)
    print(itemList)
    dataFile = open('data.pkl', 'wb')
    pickle.dump(itemList, dataFile)
    dataFile.close()
    #modify the drop down box after adding item
    tempList = []
    for k in range(len(itemList)):
        tempList.append(itemList[k].name)
    itemComboBox['values'] = tempList
    priceComboBox['values'] = tempList

def initItemList() :
    global itemComboBox,itemList,priceComboBox
    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()
    tempList = []
    for k in range(len(itemList)):
        tempList.append(itemList[k].name)
    itemComboBox['values'] = list(tempList)
    priceComboBox['values'] = list(tempList)


def removeItem() :
    global itemComboBox, itemList
    itemToRemove = itemComboBox.get()
    print(len(itemList))
    for k in range(len(itemList)):
        if itemList[k].name == itemToRemove :
            break
    del itemList[k]
    print(itemList)
    dataFile = open('data.pkl', 'wb')
    pickle.dump(itemList, dataFile)
    dataFile.close()
    itemComboBox.set('')
    initItemList()

def modifyPrice() :
    global pItemString, priceString, currPriceString
    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()
    for k in range(len(itemList)):
        if itemList[k].name == pItemString.get():
            itemList[k].cost = int(priceString.get())    
    dataFile = open('data.pkl', 'wb')
    pickle.dump(itemList, dataFile)
    dataFile.close()
    pItemString.set('')
    priceString.set('')
    currPriceString.set('')

def printTempPrice(*args):
    global pItemString
    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()
    for k in range(len(itemList)):
        if itemList[k].name == pItemString.get():
            currPriceString.set(str(itemList[k].cost))

