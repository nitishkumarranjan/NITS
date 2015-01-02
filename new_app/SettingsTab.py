from Tkinter import *
from ttk import *
import tkFileDialog
import math
import tkColorChooser as tkcc
import pickle
import pygame
import pyaudio,wave,sys
import json

class Item():
    def __init__(self, name, image, cost, category, audio):
        self.name = name
        self.image = image
        self.cost = cost
        self.category = category
        self.audio = audio

'''
    the root data structure is as follows 

    root->children (dictionary with key as category name)
    root->children->children (dictionary with item name)
    root->children->children->name
			    ->cost
			    ->image
			    ->quantitys
			    ->audio
			    ->isleaf (set to true to indicate leaf node)
'''

class SettingsTab(Frame):
	def __init__(self, master, *pargs):
	    self.master = master
	    Frame.__init__(self, master, *pargs)
	    self.initUI()	

	def initUI(self):
	    self.initSettings()
	    self.master.title("Settings")
	    self.master.bind('<Return>', self.updateDelay)
	    #self = Frame(root, padding="3 3 12 12")
	    self.grid(column=0, row=0, sticky=(N, W, E, S))
	    self.columnconfigure(0, weight=1)
	    self.rowconfigure(0, weight=1)
	    #rowsArray = [1,3,4,5,6,8,9,10,11,13,14,15,16,17,18,19,20,21,22,12,23,24]
	    rowsArray = [1,3,4,5,6,8,9,10,11,14,15,16,17,18,19,20,21,22,13,12,23,24,25,26,27,28,29,30,31,32]
	    self.numberImages=["images/num1.gif","images/num2.gif","images/num3.gif","images/num4.gif","images/num5.gif","images/num6.gif"]
	    self.message = StringVar()
	    self.itemList = []
	    self.root = {}
	    #second line vars
	    #self.delay = 4.0
	    self.delayString = StringVar()
	    self.delayString.set(self.delay)
	    #third line vars
	    #self.mainDelay = 2.0
	    self.mainDelayString = StringVar()
	    self.mainDelayString.set(self.mainDelay)
	    #fourth line vars
	    #self.colour1 = '#00ff00'
	    #sixth line vars -add item
	    self.itemToAdd = ''
	    self.itemName = StringVar()
	    self.itemCost = StringVar()
	    self.imageName = StringVar()
	    self.categoryName = StringVar()
	    #seventh line vars - remove item
	    self.countryvar = StringVar()
	    #eighth line - price mod
	    self. priceString = StringVar()
	    self.pItemString = StringVar()
	    self.currPriceString = StringVar()
	    #ninth line - audio file mod
	    self.audioString = StringVar()
	    self.aItemString = StringVar()
	    self.currAudioString = StringVar()
	    self.durationString = StringVar()
	    #tenth line - self.bcDelay
	    self.bcDelayString = StringVar()
	    self.bcDelayString.set(self.bcDelay)
	    #eleventh line - modify quantities
	    self.quantitiesString = StringVar()
	    self.qItemString = StringVar()
	    self.currQuantitiesString = StringVar()
	    #eleventh line - modify quantities
	    self.pictureString = StringVar()
	    self.pictureItemString = StringVar()
	    self.currPicturesString = StringVar()
	    
	    
	    #first line
	    Label(self, text = "Parameter").grid(row = rowsArray[0], column = 1)
	    Label(self, text = "Press enter after typing to set").grid(row = rowsArray[0], column = 2)
	    Label(self, text = "Press to set").grid(row = rowsArray[0], column = 4)
	    Label(self, text = "Press to set").grid(row = rowsArray[0], column = 5)
	    Label(self, text = "Current Value").grid(row = rowsArray[0], column = 6)
	    
	    #second line
	    Label(self, text = "Delay between blocks : ").grid(row = rowsArray[1], column = 1)
	    delayEntry = Entry(self, text = "Entry", textvariable = self.delayString)
	    delayEntry.grid(row = rowsArray[1], column = 2)
	    Button(self, text="+", command=lambda : self.cDelay(1), width = 4).grid(column = 4, row = rowsArray[1])
	    Button(self, text="-", command=lambda : self.cDelay(-1), width = 4).grid(column = 5, row = rowsArray[1])
	    Label(self, textvariable = self.delayString).grid(row = rowsArray[1], column = 6)
	    
	    #third line
	    Label(self, text = "Delay between main blocks : ").grid(row = rowsArray[2], column = 1)
	    delayEntry = Entry(self, text = "Entry", textvariable = self.mainDelayString)
	    delayEntry.grid(row = rowsArray[2], column = 2)
	    Button(self, text="+", command=lambda:self.cmDelay(1), width = 4).grid(column = 4, row = rowsArray[2])
	    Button(self, text="-", command=lambda:self.cmDelay(-1), width = 4).grid(column = 5, row = rowsArray[2])
	    Label(self, textvariable = self.mainDelayString).grid(row = rowsArray[2], column = 6)
	    
	    #colourchooser
	    Label(self, text = "Change highlight colour : ").grid(row = rowsArray[3], column = 1)
	    Button(self, text="Click to change", command=self.changeColour).grid(column = 2, row = rowsArray[3])
	    self.colFrame1 = Frame(self, border=1, relief=RAISED, width=20, height=20)
	    self.colFrame1.grid(row = rowsArray[3], column = 6)
	    
	    #self.addItem
	    
	    Label(self, text = "Add a new item : " ).grid(row = rowsArray[5], column = 1)
	    
	    Label(self, text = "New Item's Name " ).grid(row = rowsArray[6], column = 2)
	    itemNameEntry = Entry(self, text = "Item Name", textvariable = self.itemName)
	    itemNameEntry.grid(row = rowsArray[6], column = 4)
	    
	    Label(self, text = "New Item's Price (in Rs) " ).grid(row = rowsArray[7], column = 2)
	    itemCostEntry = Entry(self, text = "Item Cost", textvariable = self.itemCost)
	    itemCostEntry.grid(row = rowsArray[7], column = 4)
	    Button(self, text="Add", command=self.addItem).grid(column = 6, row = rowsArray[7])
	    
	    Label(self, text = "New Item's Category " ).grid(row = rowsArray[8], column = 2)
	    self.categoryComboBox = Combobox(self, textvariable=self.categoryName)
	    self.categoryComboBox.grid(row = rowsArray[8], column = 4)
	    
	    Label(self, text = "New Item's Picture " ).grid(row = rowsArray[9], column = 2)
	    Button(self, text="Select Picture", command=self.picNameUpdater).grid(column = 4, row = rowsArray[9])
	    
	    Label(self, text = "New Item's Audio duration " ).grid(row = rowsArray[19], column = 2)
	    recordLengthEntry = Entry(self, text = "Duration", textvariable = self.durationString)
	    recordLengthEntry.grid(row = rowsArray[19], column = 4)
	    Button(self, text="Start recording", command=self.recordAudioadd).grid(column = 6, row = rowsArray[19])
	    
	    Label(self, text = "(or) New Item's Audio " ).grid(row = rowsArray[18], column = 2)
	    Button(self, text="Select Audio ", command=self.audioUpdater).grid(column = 4, row = rowsArray[18])
	    
	    
	    #self.removeItem
	    
	    Label(self, text = "Remove item : " ).grid(row = rowsArray[10], column = 1)
	    
	    Label(self, text = "Select item : " ).grid(row = rowsArray[11], column = 2)
	    self.itemComboBox = Combobox(self, textvariable=self.countryvar)
	    self.itemComboBox.grid(row = rowsArray[11], column = 4)
	    Button(self, text="Remove", command=self.removeItem).grid(column = 6, row = rowsArray[11])
	    
	    #modifyitem
	    
	    Label(self, text = "Modify Price: " ).grid(row = rowsArray[12], column = 1)
	    
	    Label(self, text = "Select item : " ).grid(row = rowsArray[13], column = 2)
	    Label(self, textvariable = self.currPriceString ).grid(row = rowsArray[13], column = 6)
	    self.priceComboBox = Combobox(self, textvariable = self.pItemString)
	    self.priceComboBox.grid(row = rowsArray[13], column = 4)
	    self.priceComboBox.bind('<<ComboboxSelected>>', self.printTempPrice)
	    
	    Label(self, text = "New Price : " ).grid(row = rowsArray[14], column = 2)
	    priceEntry = Entry(self, text = "Entry", textvariable = self. priceString)
	    priceEntry.grid(row = rowsArray[14], column = 4)
	    Button(self, text="Modify", command=self.modifyBinFile).grid(column = 6, row = rowsArray[14])
	    
	    #audiostuff
	    
	    Label(self, text = "Modify Audio : " ).grid(row = rowsArray[15], column = 1)
	    
	    Label(self, text = "Select item : " ).grid(row = rowsArray[16], column = 2)
	    Button(self, text="Play current audio", command = self.playAudio).grid(column = 6, row = rowsArray[16])
	    #Label(self, textvariable = self.currAudioString ).grid(row = rowsArray[16], column = 6)
	    self.audioComboBox = Combobox(self, textvariable = self.aItemString)
	    self.audioComboBox.grid(row = rowsArray[16], column = 4)
	    
	    recordLengthEntry = Entry(self, text = "Duration", textvariable = self.durationString)
	    recordLengthEntry.grid(row = rowsArray[20], column = 4)
	    Label(self, text = "Enter duration (in sec)" ).grid(row = rowsArray[20], column = 2)
	    Button(self, text="Start recording", command=self.recordAudio).grid(column = 6, row = rowsArray[20])
	    
	    Label(self, text = "Select a file : " ).grid(row = rowsArray[21], column = 2)
	    Button(self, text="Select Audio ", command=self.audioUpdater).grid(column = 4, row = rowsArray[21])
	    Button(self, text="Modify ", command=self.modifyBinFile).grid(column = 6, row = rowsArray[21])
	    
	    #Bill finalising self.delay
	    
	    Label(self, text = "Delay in bill finalising : ").grid(row = rowsArray[22], column = 1)
	    delayEntry = Entry(self, text = "Entry", textvariable = self.bcDelayString)
	    delayEntry.grid(row = rowsArray[22], column = 2)
	    Button(self, text="+", command=lambda:self.cbcDelay(1), width = 4).grid(column = 4, row = rowsArray[22])
	    Button(self, text="-", command=lambda:self.cbcDelay(-1), width = 4).grid(column = 5, row = rowsArray[22])
	    Label(self, textvariable = self.bcDelayString).grid(row = rowsArray[22], column = 6)
	    
	    #Modify quantities
	    
	    Label(self, text = "Modify Quantities: " ).grid(row = rowsArray[23], column = 1)
	    
	    Label(self, text = "Select item : " ).grid(row = rowsArray[24], column = 2)
	    Label(self, textvariable = self.currQuantitiesString ).grid(row = rowsArray[24], column = 6)
	    self.quantityComboBox = Combobox(self, textvariable = self.qItemString)
	    self.quantityComboBox.grid(row = rowsArray[24], column = 4)
	    self.quantityComboBox.bind('<<ComboboxSelected>>', self.printTempQuantities)
	    
	    Label(self, text = "New Quantities : " ).grid(row = rowsArray[25], column = 2)
	    priceEntry = Entry(self, text = "Entry", textvariable = self.quantitiesString)
	    priceEntry.grid(row = rowsArray[25], column = 4)
	    Button(self, text="Modify", command=self.modifyBinFile).grid(column = 6, row = rowsArray[25])
	    
	    #Modify picture
	    
	    Label(self, text = "Modify Picture: " ).grid(row = rowsArray[26], column = 1)
	    
	    Label(self, text = "Select item : " ).grid(row = rowsArray[27], column = 2)
	    self.pictureComboBox = Combobox(self, textvariable = self.pictureItemString)
	    self.pictureComboBox.grid(row = rowsArray[27], column = 4)
	    self.pictureComboBox.bind('<<ComboboxSelected>>', self.printTempPicture)
	    Label(self, textvariable = self.currPicturesString).grid(row = rowsArray[27], column = 6)
	    
	    Button(self, text="Select Picture ", command=self.pictureUpdater).grid(column = 4, row = rowsArray[28])
	    Button(self, text="Modify", command=self.modifyBinFile).grid(column = 6, row = rowsArray[28])
	    
	    
	    #self.message string
	    Label(self, textvariable = self.message).grid(row = rowsArray[23], column = 1)
	    for child in self.winfo_children(): 
		child.grid_configure(padx=2, pady=2)
	    self.initItemList()

	def updateSettings(self):
	    self.delay = float(self.delay)
	    self.mainDelay = float(self.mainDelay)
	    
	    d={}
	    d["delay"]= str(self.delay)
	    d["mainDelay"]= str(self.mainDelay)
	    d["highlight-color"]= str(self.colour1)
	    d["bcDelay"]= str(self.bcDelay)

	    g=open('settings.txt','w')
	    json.dump(d,g)
	    g.close()
	    print(d, '\n')

	def updateDelay(self,*args):
	    try:
		if float(self.delayString.get()) < 1 or float(self.mainDelayString.get()) < 1:
		    self.message.set("Please enter a number greater than 1.")
		else:
		    self.message.set("")
		    self.delay = float(self.delayString.get())
		    self.mainDelay = float(self.mainDelayString.get())
	    except ValueError:
		pass
	    self.updateSettings()

	def cDelay(sel,incordec = int):
	    self.message.set("")
	    if incordec == 1:
		self.delay = int((self.delay*10) + 1)/10.0
	    else:
		self.delay = int((self.delay*10) - 1)/10.0
		if self.delay < 1:
		    self.message.set("Value can't reduce below 1.")
		    self.delay = int((self.delay*10) + 1)/10
		else:
		    self.message.set("")
	    self.delayString.set(self.delay)
	    self.updateSettings()

	def cmDelay(self,incordec = int):
	    self.message.set("")
	    if incordec == 1:
		self.mainDelay = int((self.mainDelay*10) + 1)/10.0
	    else:
		self.mainDelay = int((self.mainDelay*10) - 1)/10.0
		if self.mainDelay < 1:
		    self.message.set("Value can't reduce below 1.")
		    self.mainDelay = int((self.mainDelay*10) + 1)/10.0
		else:
		    self.message.set("")
	    self.mainDelayString.set(self.mainDelay)
	    self.updateSettings()

	def cbcDelay(self,incordec = int):
	    #print "incordec is",incordec
	    self.message.set("")
	    if incordec == 1:
		self.bcDelay = int((self.bcDelay*10) + 1)/10.0
	    else:
		self.bcDelay = int((self.bcDelay*10) - 1)/10.0
		if self.bcDelay < 0.5:
		    self.message.set("Value can't reduce below 0.5.")
		    self.bcDelay = int((self.bcDelay*10) + 1)/10.0
		else:
		    self.message.set("")
	    self.bcDelayString.set(self.bcDelay)
	    self.updateSettings()

	def changeColour(self):
	    (rgb, hexColour) = tkcc.askcolor()
	    self.colour1 = hexColour
	    print(self.colour1)
	    self.updateSettings()
	    self.colFrame1.config(bg = hexColour)

	def picNameUpdater(self) :
	    self.itemToAdd = tkFileDialog.askopenfilename(title = "Choose picture to add")
	    self.itemToAdd = self.itemToAdd[self.itemToAdd.rfind('/')+1:]
	    self.imageName.set('images/' + self.itemToAdd)
	    print self.imageName.get()
	
	#here on handling done in pickle file
	def addItem(self):
	    tempImageName = self.imageName.get()
	    if(len(self.audioString.get())==0):
		print "no audio name"
		self.audioString.set('sounds/' + self.itemName.get()+'.wav')
	    print "****AUDIO****"+self.audioString.get();
	    
	    #newItem = Item(self.itemName.get(), self.imageName.get(), int(self.itemCost.get()), self.categoryName.get(), self.audioString.get())
	    
	    item = {}
	    item["name"] = self.itemName.get()
	    item["image"] = self.imageName.get()
	    item["cost"] = int(self.itemCost.get())
	    if len(self.audioString.get())>0:
		item["audio"] = self.audioString.get()
	    item["isleaf"] = False 
	    item["quantity"] = 6
	    item["children"]={}

	    for i in range(0,item["quantity"]):
		temp={}
		temp["isleaf"]=True
		temp["name"] = str(i+1)
		temp["image"] = self.numberImages[i] 
		item["children"][i+1]=temp


	    cat_name = self.categoryName.get()
	    item_name = self.itemName.get()

	    if not self.root["children"].has_key(cat_name):
		print "category not Found adding it-",cat_name
		self.root["children"][cat_name]={}
		self.root["children"][cat_name]["isleaf"]=False
		self.root["children"][cat_name]["children"]={}
	    
	    self.root["children"][cat_name]["children"][item_name]=item
	    f = open('data.json','w')
	    json.dump(self.root,f)
	    f.close()
	    
	    self.itemName.set('')
	    self.imageName.set('')
	    self.itemCost.set('')
	    self.categoryName.set('')
	    self.audioString.set('')
	    #newItem = Item(self.itemName.get(), self.imageName.get(), int(self.itemCost.get()), self.categoryName.get(), self.audioString.get())

	    #self.itemList.append(newItem)
	    #dataFile = open('data.pkl', 'wb')
	    #pickle.dump(self.itemList, dataFile)
	    #dataFile.close()

	    #modify the drop down box after adding item
	    tempList = []
	    tempCatList = []
	    for cat_name in self.root["children"]:
		tempCatList.append(cat_name)
		for item_name in self.root["children"][cat_name]["children"]:
		    tempList.append(item_name)

	    #for k in range(len(self.itemList)):
	    #	tempList.append(self.itemList[k].name)

	    self.itemComboBox['values'] = tempList
	    self.priceComboBox['values'] = tempList
	    self.audioComboBox['values'] = tempList
	    self.quantityComboBox['values'] = tempList
	    self.pictureComboBox['values'] = tempList
	    self.categoryComboBox['values'] = list(tempCatList) 

	def initItemList(self) :
	#    pklFile = open('data.pkl', 'rb')
	#    self.itemList = pickle.load(pklFile)
	#    print 'pickle loaded'
	#    pklFile.close()
	#    tempList = []
	#    for k in range(len(self.itemList)):
	#	tempList.append(self.itemList[k].name)
	    f = open('data.json','r')
	    self.root = json.loads(f.readline())
	    print 'json loaded'
	    print self.root
	    f.close()
	    
	    tempList = []
	    tempCatList = []
	    for cat_name in self.root["children"]:
		tempCatList.append(cat_name)
		for item_name in self.root["children"][cat_name]["children"]:
		    tempList.append(item_name)
	    
	     

	    self.itemComboBox['values'] = list(tempList)
	    self.priceComboBox['values'] = list(tempList)
	    self.audioComboBox['values'] = list(tempList)
	    self.quantityComboBox['values'] = list(tempList)
	    self.pictureComboBox['values'] = list(tempList)
	    self.categoryComboBox['values'] = list(tempCatList) 


	def removeItem(self) :
	    itemToRemove = self.itemComboBox.get()
	    #for k in range(len(self.itemList)):
	    #    if self.itemList[k].name == itemToRemove :
	    #        break
	    #del self.itemList[k]
	    #dataFile = open('data.pkl', 'wb')
	    #pickle.dump(self.itemList, dataFile)
	    #dataFile.close()
	    for cat_name in self.root["children"]:
		if self.root["children"][cat_name]["children"].has_hey(itemToRemove):
		    del self.root["children"][cat_name]["children"][itemToRemove]

	    f = open('data.json','w')
	    json.dump(self.root,f)
	    f.close()
	    
	    self.itemComboBox.set('')
	    self.initItemList()

	def modifyBinFile(self) :
	    #pklFile = open('data.pkl', 'rb')
	    #self.itemList = pickle.load(pklFile)
	    #pklFile.close()
	    f = open('data.json','r')
	    self.root = json.loads(f.readline())
	    f.close()
	    
	    #for k in range(len(self.itemList)):
	    #    if self.itemList[k].name == self.pItemString.get():
	    #        self.itemList[k].cost = int(self. priceString.get())
	    #    if self.itemList[k].name == self.aItemString.get():
	    #        self.itemList[k].audio = self.audioString.get()
	    #        print(self.itemList[k].audio, self.itemList[k].name)
	    #    if self.itemList[k].name == self.qItemString.get():
	    #        self.itemList[k].quantities = self.quantitiesString.get()
	    #        print(self.itemList[k].quantities, self.itemList[k].name)
	    #    if self.itemList[k].name == self.pictureItemString.get():
	    #        self.itemList[k].picture = self.pictureString.get()
	    #        print('picture and name', self.itemList[k].picture, self.itemList[k].name)
	    #dataFile = open('data.pkl', 'wb')
	    #pickle.dump(self.itemList, dataFile)
	    #dataFile.close()
	    for cat_name in self.root["children"]:
		for item_name in self.root["children"][cat_name]["children"]:
		    item = self.root["children"][cat_name]["children"][item_name]
		    if item["name"] == self.pItemString.get():
			item["cost"] = int(self. priceString.get())
	    	    if item["name"] == self.aItemString.get():
	    	        item["audio"] = self.audioString.get()
	    	        print(item["audio"], item["name"])
	    	    if item["name"] == self.qItemString.get():
	    	        item["quantities"] = int(self.quantitiesString.get())
	    	        print(item["quantities"], item["name"])
	    	    if item["name"] == self.pictureItemString.get():
	    	        item["image"] = self.pictureString.get()
	    	        print('picture and name', item["image"], item["name"])	   
	    
	    f = open('data.json','w')
	    json.dump(self.root,f)
	    f.close()
	    
	    self.pItemString.set('')
	    self.priceString.set('')
	    self.currPriceString.set('')
	    self.aItemString.set('')
	    self.audioString.set('')
	    self.qItemString.set('')
	    self.quantitiesString.set('')
	    self.currQuantitiesString.set('')
	    self.pictureItemString.set('')
	    self.pictureString.set('')
	    self.currPicturesString.set('')
	    self.initItemList()

	def printTempPrice(self,*args):
	#    pklFile = open('data.pkl', 'rb')
	#    self.itemList = pickle.load(pklFile)
	#    pklFile.close()
	#    for k in range(len(self.itemList)):
	#	if self.itemList[k].name == self.pItemString.get():
	#	    self.currPriceString.set(str(self.itemList[k].cost))
	    f = open('data.json','r')
	    self.root = json.loads(f.readline())
	    f.close()
	    for cat_name in self.root["children"]:
		for item_name in self.root["children"][cat_name]["children"]:
		    if item_name  == self.pItemString.get():
			item = self.root["children"][cat_name]["children"][item_name]
			self.currPriceString.set(str(item["cost"]))

	def printTempQuantities(self,*args):
	#    pklFile = open('data.pkl', 'rb')
	#    self.itemList = pickle.load(pklFile)
	#    pklFile.close()
	#    for k in range(len(self.itemList)):
	#	if self.itemList[k].name == self.qItemString.get():
	#	    self.currQuantitiesString.set(str(self.itemList[k].quantities))
	    f = open('data.json','r')
	    self.root = json.loads(f.readline())
	    f.close()
	    for cat_name in self.root["children"]:
		for item_name in self.root["children"][cat_name]["children"]:
		    if item_name  == self.qItemString.get():
			item = self.root["children"][cat_name]["children"][item_name]
			self.currQuantitiesString.set(str(item["quantities"]))


	def printTempPicture(self,*args):
	#    pklFile = open('data.pkl', 'rb')
	#    self.itemList = pickle.load(pklFile)
	#    pklFile.close()
	#    for k in range(len(self.itemList)):
	#	if self.itemList[k].name == self.pictureItemString.get():
	#	    self.currPicturesString.set(str(self.itemList[k].picture))
	    f = open('data.json','r')
	    self.root = json.loads(f.readline())
	    f.close()
	    for cat_name in self.root["children"]:
		for item_name in self.root["children"][cat_name]["children"]:
		    if item_name  == self.pictureItemString.get():
			item = self.root["children"][cat_name]["children"][item_name]
			self.currPicturesString.set(str(item["image"]))


	def audioUpdater(self) :
	    audioFileName = tkFileDialog.askopenfilename(title = "Choose audio ")
	    audioFileName = audioFileName[audioFileName.rfind('/')+1:]
	    self.audioString.set('sounds/' + audioFileName)
	    print(self.audioString.get())

	def pictureUpdater(self) :
	    pictureFileName = tkFileDialog.askopenfilename(title = "Choose picture ")
	    pictureFileName = pictureFileName[pictureFileName.rfind('/')+1:]
	    self.pictureString.set('images/' + pictureFileName)
	    print('Picture updated to', self.pictureString.get())

	def recordAudioadd(self):
	    CHUNK = 1024
	    FORMAT = pyaudio.paInt16
	    CHANNELS = 2
	    RATE = 44100
	    RECORD_SECONDS = float(self.durationString.get())
	    self.durationString.set('')
	    WAVE_OUTPUT_FILENAME = ''.join(['sounds/',self.itemName.get(),'.wav'])

	    #pklFile = open('data.pkl', 'rb')
	    #self.itemList = pickle.load(pklFile)
	    #pklFile.close()

	    #for k in range(len(self.itemList)):
	    #    if self.itemList[k].name == self.aItemString.get():
	    #        self.itemList[k].audio = WAVE_OUTPUT_FILENAME

	    #dataFile = open('data.pkl', 'wb')
	    #pickle.dump(self.itemList, dataFile)
	    f = open('data.json','r')
	    self.root = json.loads(f.readline())
	    f.close()
	    for cat_name in self.root["children"]:
		for item_name in self.root["children"][cat_name]["children"]:
		    if item_name  == self.aItemString.get():
			item = self.root["children"][cat_name]["children"][item_name]
			item["audio"] = WAVE_OUTPUT_FILENAME
	    f = open('data.json','w')
	    json.dump(self.root,f)
	    f.close()

	    self.aItemString.set('')
	    print "recording to : ", WAVE_OUTPUT_FILENAME

	    p = pyaudio.PyAudio()

	    stream = p.open(format=FORMAT,
		    channels=CHANNELS,
		    rate=RATE,
		    input=True,
		    frames_per_buffer=CHUNK)

	    print("* recording")

	    frames = []
	    self.message.set("Recording : ")
	    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	    self.message.set("")
	    print("* done recording")

	    stream.stop_stream()
	    stream.close()
	    print "waveoutputfilename : "+WAVE_OUTPUT_FILENAME;
	    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	    wf.setnchannels(CHANNELS)
	    wf.setsampwidth(p.get_sample_size(FORMAT))
	    wf.setframerate(RATE)
	    wf.writeframes(b''.join(frames))
	    wf.close()

	    print "reaches here"


	    wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
	    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
		    channels=wf.getnchannels(),
		    rate=wf.getframerate(),
		    output=True)
	    data = wf.readframes(CHUNK)

	    while data != '':
		stream.write(data)
		data = wf.readframes(CHUNK)

	    stream.stop_stream()
	    stream.close()

	    p.terminate()


	def recordAudio(self):
	    CHUNK = 1024
	    FORMAT = pyaudio.paInt16
	    CHANNELS = 2
	    RATE = 44100
	    RECORD_SECONDS = float(self.durationString.get())
	    self.durationString.set('')
	    WAVE_OUTPUT_FILENAME = ''.join(['sounds/',self.aItemString.get(),'.wav'])

	    #pklFile = open('data.pkl', 'rb')
	    #self.itemList = pickle.load(pklFile)
	    #pklFile.close()

	    #for k in range(len(self.itemList)):
	    #    if self.itemList[k].name == self.aItemString.get():
	    #        self.itemList[k].audio = WAVE_OUTPUT_FILENAME

	    #dataFile = open('data.pkl', 'wb')
	    #pickle.dump(self.itemList, dataFile)
	    f = open('data.json','r')
	    self.root = json.loads(f.readline())
	    f.close()
	    for cat_name in self.root["children"]:
		for item_name in self.root["children"][cat_name]["children"]:
		    if item_name  == self.aItemString.get():
			item = self.root["children"][cat_name]["children"][item_name]
			item["audio"] = WAVE_OUTPUT_FILENAME
	    f = open('data.json','w')
	    json.dump(self.root,f)
	    f.close()
	    
	    self.aItemString.set('')
	    print "recording to : ", WAVE_OUTPUT_FILENAME

	    p = pyaudio.PyAudio()

	    stream = p.open(format=FORMAT,
		    channels=CHANNELS,
		    rate=RATE,
		    input=True,
		    frames_per_buffer=CHUNK)

	    print("* recording")

	    frames = []
	    self.message.set("Recording : ")
	    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	    self.message.set("")
	    print("* done recording")

	    stream.stop_stream()
	    stream.close()
	    print "waveoutputfilename : "+WAVE_OUTPUT_FILENAME;
	    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	    wf.setnchannels(CHANNELS)
	    wf.setsampwidth(p.get_sample_size(FORMAT))
	    wf.setframerate(RATE)
	    wf.writeframes(b''.join(frames))
	    wf.close()

	    print "reaches here"


	    wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
	    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
		    channels=wf.getnchannels(),
		    rate=wf.getframerate(),
		    output=True)
	    data = wf.readframes(CHUNK)

	    while data != '':
		stream.write(data)
		data = wf.readframes(CHUNK)

	    stream.stop_stream()
	    stream.close()

	    p.terminate()

	def playAudio(self):
	    CHUNK = 1024
	    FORMAT = pyaudio.paInt16
	    CHANNELS = 2
	    RATE = 44100
	    RECORD_SECONDS = 2

	#    pklFile = open('data.pkl', 'rb')
	#    self.itemList = pickle.load(pklFile)
	#    pklFile.close()

	#    for k in range(len(self.itemList)):
	#	if self.itemList[k].name == self.aItemString.get():
	#	    WAVE_OUTPUT_FILENAME = self.itemList[k].audio
	    f = open('data.json','w')
	    self.root = json.loads(f.readline())
	    f.close()
	    
	    for cat_name in self.root["children"]:
		for item_name in self.root["children"][cat_name]["children"]:
		    if item_name  == self.aItemString.get():
			item = self.root["children"][cat_name]["children"][item_name]
			WAVE_OUTPUT_FILENAME = item["audio"]

	    print("Received fileName is : ", WAVE_OUTPUT_FILENAME)
	    p = pyaudio.PyAudio()

	    stream = p.open(format=FORMAT,
		    channels=CHANNELS,
		    rate=RATE,
		    input=True,
		    frames_per_buffer=CHUNK)


	    wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
	    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
		    channels=wf.getnchannels(),
		    rate=wf.getframerate(),
		    output=True)
	    data = wf.readframes(CHUNK)

	    while data != '':
		stream.write(data)
		data = wf.readframes(CHUNK)

	    stream.stop_stream()
	    stream.close()

	    p.terminate()

	def initSettings(self):
	    g=open('settings.txt','r')
	    d=json.loads(g.readline())
	    self.delay=d["delay"]
	    self.mainDelay=d["mainDelay"]
	    self.colour1=d["highlight-color"]
	    self.bcDelay=float(d["bcDelay"])
	    g.close()

#if __name__ == "__main__":
#    root = Tk()
#    app = SettingsTab(root)
#    root.mainloop()
