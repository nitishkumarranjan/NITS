from Tkinter import *
import ttk
import tkFileDialog
import math
import tkColorChooser as tkcc
import pickle
import pygame
import pyaudio,wave,sys


def updateFile():
    global delay, mainDelay, colour1
    g=open('settings.txt','r+')
    delay = float(delay)
    mainDelay = float(mainDelay)
    f=g.read()
    g.close()
    print(f)
    f = f.replace('\n', ' ')
    f = f.split(' ')

    f[2] = str(delay)
    f[5] = str(mainDelay)
    f[8] = str(colour1)
    f[11] = str(bcDelay)

    f1 = ' '.join(f[:3])
    f2 = ' '.join(f[3:6])
    f3 = ' '.join(f[6:9])
    f4 = ' '.join(f[9:])
    f = '\n'.join([f1,f2,f3,f4])

    g=open('settings.txt','w')
    print(f, '\n')
    g.write(f)
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

def cDelay(incordec = int):
    global delay
    message.set("")
    if incordec == 1:
        delay = int((delay*10) + 1)/10.0
    else:
        delay = int((delay*10) - 1)/10.0
        if delay < 1:
            message.set("Value can't reduce below 1.")
            delay = int((delay*10) + 1)/10
        else:
            message.set("")
    delayString.set(delay)
    updateFile()

def cmDelay(incordec = int):
    global mainDelay
    message.set("")
    if incordec == 1:
        mainDelay = int((mainDelay*10) + 1)/10.0
    else:
        mainDelay = int((mainDelay*10) - 1)/10.0
        if mainDelay < 1:
            message.set("Value can't reduce below 1.")
            mainDelay = int((mainDelay*10) + 1)/10.0
        else:
            message.set("")
    mainDelayString.set(mainDelay)
    updateFile()

def cbcDelay(incordec = int):
    global bcDelay
    #print "incordec is",incordec
    message.set("")
    if incordec == 1:
        bcDelay = int((bcDelay*10) + 1)/10.0
    else:
        bcDelay = int((bcDelay*10) - 1)/10.0
        if bcDelay < 0.5:
            message.set("Value can't reduce below 0.5.")
            bcDelay = int((bcDelay*10) + 1)/10.0
        else:
            message.set("")
    bcDelayString.set(bcDelay)
    updateFile()

def changeColour():
    global colour1,colFrame1
    (rgb, hexColour) = tkcc.askcolor()
    colour1 = hexColour
    print(colour1)
    updateFile()
    colFrame1.config(bg = hexColour)


class Item():

    def __init__(self, name, image, cost, category, audio):

        self.name = name
        self.image = image
        self.cost = cost
        self.category = category
        self.audio = audio

def picNameUpdater() :
    global itemToAdd, imageName
    itemToAdd = tkFileDialog.askopenfilename(title = "Choose picture to add")
    itemToAdd = itemToAdd[itemToAdd.rfind('/')+1:]
    imageName.set('images/' + itemToAdd)
    print imageName.get()

def addItem():
    global itemName, imageName, itemCost, categoryName, itemList, itemComboBox, priceComboBox, audioComboBox, audioString
    tempImageName = imageName.get()
    if(len(audioString.get())==0):
        print "no audio name"
        audioString.set('sounds/' + itemName.get()+'.wav')
    print "****AUDIO****"+audioString.get();
    newItem = Item(itemName.get(), imageName.get(), int(itemCost.get()), categoryName.get(), audioString.get())
    itemName.set('')
    imageName.set('')
    itemCost.set('')
    categoryName.set('')
    audioString.set('')
    #newItem = Item(itemName.get(), imageName.get(), int(itemCost.get()), categoryName.get(), audioString.get())

    itemList.append(newItem)
    dataFile = open('data.pkl', 'wb')
    pickle.dump(itemList, dataFile)
    dataFile.close()
    
    #modify the drop down box after adding item
    tempList = []
    for k in range(len(itemList)):
        tempList.append(itemList[k].name)
    itemComboBox['values'] = tempList
    priceComboBox['values'] = tempList
    audioComboBox['values'] = tempList
    quantityComboBox['values'] = tempList
    pictureComboBox['values'] = tempList

def initItemList() :
    global itemComboBox,itemList,priceComboBox, quantityComboBox,pictureComboBox
    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    print 'pickle loaded'
    pklFile.close()
    tempList = []
    for k in range(len(itemList)):
        tempList.append(itemList[k].name)
    itemComboBox['values'] = list(tempList)
    priceComboBox['values'] = list(tempList)
##    print 'here',itemComboBox['values'], priceComboBox['values']
    audioComboBox['values'] = list(tempList)
    quantityComboBox['values'] = list(tempList)
    pictureComboBox['values'] = list(tempList)


def removeItem() :
    global itemComboBox, itemList
    itemToRemove = itemComboBox.get()
    for k in range(len(itemList)):
        if itemList[k].name == itemToRemove :
            break
    del itemList[k]
    dataFile = open('data.pkl', 'wb')
    pickle.dump(itemList, dataFile)
    dataFile.close()
    itemComboBox.set('')
    initItemList()

def modifyBinFile() :
    global pItemString, priceString, currPriceString, aItemString, audioString
    global pictureItemString,pictureString, currPicturesString
    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()
    for k in range(len(itemList)):
        if itemList[k].name == pItemString.get():
            itemList[k].cost = int(priceString.get())
        if itemList[k].name == aItemString.get():
            itemList[k].audio = audioString.get()
            print(itemList[k].audio, itemList[k].name)
        if itemList[k].name == qItemString.get():
            itemList[k].quantities = quantitiesString.get()
            print(itemList[k].quantities, itemList[k].name)
        if itemList[k].name == pictureItemString.get():
            itemList[k].picture = pictureString.get()
            print('picture and name', itemList[k].picture, itemList[k].name)
    dataFile = open('data.pkl', 'wb')
    pickle.dump(itemList, dataFile)
    dataFile.close()
    pItemString.set('')
    priceString.set('')
    currPriceString.set('')
    aItemString.set('')
    audioString.set('')
    qItemString.set('')
    quantitiesString.set('')
    currQuantitiesString.set('')
    pictureItemString.set('')
    pictureString.set('')
    currPicturesString.set('')
    initItemList()

def printTempPrice(*args):
    global pItemString
    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()
    for k in range(len(itemList)):
        if itemList[k].name == pItemString.get():
            currPriceString.set(str(itemList[k].cost))

def printTempQuantities(*args):
    global qItemString
    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()
    for k in range(len(itemList)):
        if itemList[k].name == qItemString.get():
            currQuantitiesString.set(str(itemList[k].quantities))

def printTempPicture(*args):
    global pictureItemString
    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()
    for k in range(len(itemList)):
        if itemList[k].name == pictureItemString.get():
            currPicturesString.set(str(itemList[k].picture))

def audioUpdater() :
    global audioString
    audioFileName = tkFileDialog.askopenfilename(title = "Choose audio ")
    audioFileName = audioFileName[audioFileName.rfind('/')+1:]
    audioString.set('sounds/' + audioFileName)
    print(audioString.get())

def pictureUpdater() :
    global pictureString
    pictureFileName = tkFileDialog.askopenfilename(title = "Choose picture ")
    pictureFileName = pictureFileName[pictureFileName.rfind('/')+1:]
    pictureString.set('images/' + pictureFileName)
    print('Picture updated to', pictureString.get())
##    print(pictureString.get())

def recordAudioadd():
    global meessage
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = float(durationString.get())
    durationString.set('')
    WAVE_OUTPUT_FILENAME = ''.join(['sounds/',itemName.get(),'.wav'])

    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()

    for k in range(len(itemList)):
        if itemList[k].name == aItemString.get():
            itemList[k].audio = WAVE_OUTPUT_FILENAME

    dataFile = open('data.pkl', 'wb')
    pickle.dump(itemList, dataFile)

    aItemString.set('')
    print "recording to : ", WAVE_OUTPUT_FILENAME

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    message.set("Recording : ")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    message.set("")
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


def recordAudio():
    global meessage
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = float(durationString.get())
    durationString.set('')
    WAVE_OUTPUT_FILENAME = ''.join(['sounds/',aItemString.get(),'.wav'])

    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()

    for k in range(len(itemList)):
        if itemList[k].name == aItemString.get():
            itemList[k].audio = WAVE_OUTPUT_FILENAME

    dataFile = open('data.pkl', 'wb')
    pickle.dump(itemList, dataFile)

    aItemString.set('')
    print "recording to : ", WAVE_OUTPUT_FILENAME

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    message.set("Recording : ")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    message.set("")
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

def playAudio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 2

    pklFile = open('data.pkl', 'rb')
    itemList = pickle.load(pklFile)
    pklFile.close()

    for k in range(len(itemList)):
        if itemList[k].name == aItemString.get():
            WAVE_OUTPUT_FILENAME = itemList[k].audio
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

def initVals():
    global delay,mainDelay,colour1,bcDelay
    g=open('settings.txt','r')
    f=g.read()
    h=f.replace(' ','\n')
    h=h.replace('\r','\n')
    h=h.split('\n')
    tempDelay=h[h.index('delay')+2]
    delay=float(tempDelay)
    tempDelay=h[h.index('mainDelay')+2]
    mainDelay=float(tempDelay)
    colour1=h[h.index('highlight-color')+2]
    tempDelay = h[h.index('bcDelay')+2]
    bcDelay = float(tempDelay)
    g.close()

initVals()
root=Tk()
root.title("Settings")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
#rowsArray = [1,3,4,5,6,8,9,10,11,13,14,15,16,17,18,19,20,21,22,12,23,24]
rowsArray = [1,3,4,5,6,8,9,10,11,14,15,16,17,18,19,20,21,22,13,12,23,24,25,26,27,28,29,30,31,32]
message = StringVar()
itemList = []
#second line vars
#delay = 4.0
delayString = StringVar()
delayString.set(delay)
#third line vars
#mainDelay = 2.0
mainDelayString = StringVar()
mainDelayString.set(mainDelay)
#fourth line vars
#colour1 = '#00ff00'
#sixth line vars -add item
itemToAdd = ''
itemName = StringVar()
itemCost = StringVar()
imageName = StringVar()
categoryName = StringVar()
#seventh line vars - remove item
countryvar = StringVar()
#eighth line - price mod
priceString = StringVar()
pItemString = StringVar()
currPriceString = StringVar()
#ninth line - audio file mod
audioString = StringVar()
aItemString = StringVar()
currAudioString = StringVar()
durationString = StringVar()
#tenth line - bcDelay
bcDelayString = StringVar()
bcDelayString.set(bcDelay)
#eleventh line - modify quantities
quantitiesString = StringVar()
qItemString = StringVar()
currQuantitiesString = StringVar()
#eleventh line - modify quantities
pictureString = StringVar()
pictureItemString = StringVar()
currPicturesString = StringVar()


#first line
ttk.Label(mainframe, text = "Parameter").grid(row = rowsArray[0], column = 1)
ttk.Label(mainframe, text = "Press enter after typing to set").grid(row = rowsArray[0], column = 2)
ttk.Label(mainframe, text = "Press to set").grid(row = rowsArray[0], column = 4)
ttk.Label(mainframe, text = "Press to set").grid(row = rowsArray[0], column = 5)
ttk.Label(mainframe, text = "Current Value").grid(row = rowsArray[0], column = 6)

#second line
ttk.Label(mainframe, text = "Delay between blocks : ").grid(row = rowsArray[1], column = 1)
delayEntry = ttk.Entry(mainframe, text = "Entry", textvariable = delayString)
delayEntry.grid(row = rowsArray[1], column = 2)
ttk.Button(mainframe, text="+", command=lambda : cDelay(1), width = 4).grid(column = 4, row = rowsArray[1])
ttk.Button(mainframe, text="-", command=lambda : cDelay(-1), width = 4).grid(column = 5, row = rowsArray[1])
ttk.Label(mainframe, textvariable = delayString).grid(row = rowsArray[1], column = 6)

#third line
ttk.Label(mainframe, text = "Delay between main blocks : ").grid(row = rowsArray[2], column = 1)
delayEntry = ttk.Entry(mainframe, text = "Entry", textvariable = mainDelayString)
delayEntry.grid(row = rowsArray[2], column = 2)
ttk.Button(mainframe, text="+", command=lambda:cmDelay(1), width = 4).grid(column = 4, row = rowsArray[2])
ttk.Button(mainframe, text="-", command=lambda:cmDelay(-1), width = 4).grid(column = 5, row = rowsArray[2])
ttk.Label(mainframe, textvariable = mainDelayString).grid(row = rowsArray[2], column = 6)

#colourchooser
ttk.Label(mainframe, text = "Change highlight colour : ").grid(row = rowsArray[3], column = 1)
ttk.Button(mainframe, text="Click to change", command=changeColour).grid(column = 2, row = rowsArray[3])
colFrame1 = Frame(mainframe, border=1, relief=RAISED, width=20, height=20)
colFrame1.grid(row = rowsArray[3], column = 6)
colFrame1.config(bg = colour1)

#additem

ttk.Label(mainframe, text = "Add a new item : " ).grid(row = rowsArray[5], column = 1)

ttk.Label(mainframe, text = "New Item's Name " ).grid(row = rowsArray[6], column = 2)
itemNameEntry = ttk.Entry(mainframe, text = "Item Name", textvariable = itemName)
itemNameEntry.grid(row = rowsArray[6], column = 4)

ttk.Label(mainframe, text = "New Item's Price (in Rs) " ).grid(row = rowsArray[7], column = 2)
itemCostEntry = ttk.Entry(mainframe, text = "Item Cost", textvariable = itemCost)
itemCostEntry.grid(row = rowsArray[7], column = 4)
ttk.Button(mainframe, text="Add", command=addItem).grid(column = 6, row = rowsArray[7])

ttk.Label(mainframe, text = "New Item's Category " ).grid(row = rowsArray[8], column = 2)
categoryComboBox = ttk.Combobox(mainframe, textvariable=categoryName)
categoryComboBox.grid(row = rowsArray[8], column = 4)
categoryComboBox['values'] = ['Food', 'Drink']

ttk.Label(mainframe, text = "New Item's Picture " ).grid(row = rowsArray[9], column = 2)
ttk.Button(mainframe, text="Select Picture", command=picNameUpdater).grid(column = 4, row = rowsArray[9])

ttk.Label(mainframe, text = "New Item's Audio duration " ).grid(row = rowsArray[19], column = 2)
recordLengthEntry = ttk.Entry(mainframe, text = "Duration", textvariable = durationString)
recordLengthEntry.grid(row = rowsArray[19], column = 4)
ttk.Button(mainframe, text="Start recording", command=recordAudioadd).grid(column = 6, row = rowsArray[19])

ttk.Label(mainframe, text = "(or) New Item's Audio " ).grid(row = rowsArray[18], column = 2)
ttk.Button(mainframe, text="Select Audio ", command=audioUpdater).grid(column = 4, row = rowsArray[18])


#removeitem

ttk.Label(mainframe, text = "Remove item : " ).grid(row = rowsArray[10], column = 1)

ttk.Label(mainframe, text = "Select item : " ).grid(row = rowsArray[11], column = 2)
itemComboBox = ttk.Combobox(mainframe, textvariable=countryvar)
itemComboBox.grid(row = rowsArray[11], column = 4)
ttk.Button(mainframe, text="Remove", command=removeItem).grid(column = 6, row = rowsArray[11])

#modifyitem

ttk.Label(mainframe, text = "Modify Price: " ).grid(row = rowsArray[12], column = 1)

ttk.Label(mainframe, text = "Select item : " ).grid(row = rowsArray[13], column = 2)
ttk.Label(mainframe, textvariable = currPriceString ).grid(row = rowsArray[13], column = 6)
priceComboBox = ttk.Combobox(mainframe, textvariable = pItemString)
priceComboBox.grid(row = rowsArray[13], column = 4)
priceComboBox.bind('<<ComboboxSelected>>', printTempPrice)

ttk.Label(mainframe, text = "New Price : " ).grid(row = rowsArray[14], column = 2)
priceEntry = ttk.Entry(mainframe, text = "Entry", textvariable = priceString)
priceEntry.grid(row = rowsArray[14], column = 4)
ttk.Button(mainframe, text="Modify", command=modifyBinFile).grid(column = 6, row = rowsArray[14])

#audiostuff

ttk.Label(mainframe, text = "Modify Audio : " ).grid(row = rowsArray[15], column = 1)

ttk.Label(mainframe, text = "Select item : " ).grid(row = rowsArray[16], column = 2)
ttk.Button(mainframe, text="Play current audio", command = playAudio).grid(column = 6, row = rowsArray[16])
#ttk.Label(mainframe, textvariable = currAudioString ).grid(row = rowsArray[16], column = 6)
audioComboBox = ttk.Combobox(mainframe, textvariable = aItemString)
audioComboBox.grid(row = rowsArray[16], column = 4)

recordLengthEntry = ttk.Entry(mainframe, text = "Duration", textvariable = durationString)
recordLengthEntry.grid(row = rowsArray[20], column = 4)
ttk.Label(mainframe, text = "Enter duration (in sec)" ).grid(row = rowsArray[20], column = 2)
ttk.Button(mainframe, text="Start recording", command=recordAudio).grid(column = 6, row = rowsArray[20])

ttk.Label(mainframe, text = "Select a file : " ).grid(row = rowsArray[21], column = 2)
ttk.Button(mainframe, text="Select Audio ", command=audioUpdater).grid(column = 4, row = rowsArray[21])
ttk.Button(mainframe, text="Modify ", command=modifyBinFile).grid(column = 6, row = rowsArray[21])

#Bill finalising delay

ttk.Label(mainframe, text = "Delay in bill finalising : ").grid(row = rowsArray[22], column = 1)
delayEntry = ttk.Entry(mainframe, text = "Entry", textvariable = bcDelayString)
delayEntry.grid(row = rowsArray[22], column = 2)
ttk.Button(mainframe, text="+", command=lambda:cbcDelay(1), width = 4).grid(column = 4, row = rowsArray[22])
ttk.Button(mainframe, text="-", command=lambda:cbcDelay(-1), width = 4).grid(column = 5, row = rowsArray[22])
ttk.Label(mainframe, textvariable = bcDelayString).grid(row = rowsArray[22], column = 6)

#Modify quantities

ttk.Label(mainframe, text = "Modify Quantities: " ).grid(row = rowsArray[23], column = 1)

ttk.Label(mainframe, text = "Select item : " ).grid(row = rowsArray[24], column = 2)
ttk.Label(mainframe, textvariable = currQuantitiesString ).grid(row = rowsArray[24], column = 6)
quantityComboBox = ttk.Combobox(mainframe, textvariable = qItemString)
quantityComboBox.grid(row = rowsArray[24], column = 4)
quantityComboBox.bind('<<ComboboxSelected>>', printTempQuantities)

ttk.Label(mainframe, text = "New Quantities : " ).grid(row = rowsArray[25], column = 2)
priceEntry = ttk.Entry(mainframe, text = "Entry", textvariable = quantitiesString)
priceEntry.grid(row = rowsArray[25], column = 4)
ttk.Button(mainframe, text="Modify", command=modifyBinFile).grid(column = 6, row = rowsArray[25])

#Modify picture

ttk.Label(mainframe, text = "Modify Picture: " ).grid(row = rowsArray[26], column = 1)

ttk.Label(mainframe, text = "Select item : " ).grid(row = rowsArray[27], column = 2)
pictureComboBox = ttk.Combobox(mainframe, textvariable = pictureItemString)
pictureComboBox.grid(row = rowsArray[27], column = 4)
pictureComboBox.bind('<<ComboboxSelected>>', printTempPicture)
ttk.Label(mainframe, textvariable = currPicturesString).grid(row = rowsArray[27], column = 6)

ttk.Button(mainframe, text="Select Picture ", command=pictureUpdater).grid(column = 4, row = rowsArray[28])
ttk.Button(mainframe, text="Modify", command=modifyBinFile).grid(column = 6, row = rowsArray[28])


#message string
ttk.Label(mainframe, textvariable = message).grid(row = rowsArray[23], column = 1)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
initItemList()
root.bind('<Return>', updateDelay)

root.mainloop()
quit()
