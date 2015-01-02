from Tkinter import *
from ttk import *
import json
import tkFont

class BillTab(Frame):
	def __init__(self, master,data,bill_no, *pargs):
	    self.master = master
	    self.data = data
	    self.bill_no = bill_no
	    Frame.__init__(self, master, *pargs)
	    self.initData()
	    self.initUI()

	def initUI(self):
	    self.master.title("bill-"+str(self.bill_no)+" confirmation ?")
  	    self.customFonts = tkFont.Font(family="Helvetica", size=15)
	    Style().configure("TFrame",background=self.bgcolor)
            self.style=Style()
	    self.master.geometry('300x300+400+200')
	    self.pack(fill=BOTH, expand=1)

	    for each in self.data:
		w=Label(self, text = each ,padding="5 5 5 5",background=self.bgcolor,font=self.customFonts)
		w.pack()
	    
	    self.Print = Label(self, text="Print",padding="5 5 5 5",background=self.bgcolor,font=self.customFonts)
	    self.Print.pack()    
	    
	    self.Delete = Label(self, text="Delete",padding="5 5 5 5",background=self.bgcolor,font=self.customFonts)
	    self.Delete.pack()    
	    
	    loop_list=[]
	    loop_data=[]
	    loop_list.append(self.Print)
	    temp={}
	    temp["type"]="print"
	    loop_data.append(temp)
	    loop_list.append(self.Delete)
	    temp={}
	    temp["type"]="delete"
	    loop_data.append(temp)
	    
	    self.after(1,lambda : self.Interrupt(loop_list,loop_data))
	
	def initData(self):
	    #loading basic settings from settings.txt
	    g=open('settings.txt','r')
	    d=json.loads(g.readline())
	    self.delay=float(d["delay"])
	    self.mainDelay=float(d["mainDelay"])
	    self.highcolour=d["highlight-color"]
	    self.bcDelay=float(d["bcDelay"])
	    self.bgcolor="white"
	    g.close()
	    
	    self.loop_index=-1
    
	def Interrupt(self,loop_list,loop_data):
	    self.loop_index = (self.loop_index+1)%2
	    self.UnHighlightAll(loop_list)
	    loop_list[self.loop_index].configure(background=self.highcolour)
	    self.master.bind('<1>', lambda e: self.ClickHandle(loop_data[self.loop_index]))
	    self.after(int(1000*self.mainDelay),lambda : self.Interrupt(loop_list,loop_data))
	
	def UnHighlightAll(self,loop_list):
	    for each in loop_list:
		each.configure(background=self.bgcolor)

	def ClickHandle(self,data):
	    if data["type"]=="print":
		f=open("bills/bill_"+str(self.bill_no)+".txt","w")
		for each in self.data:
		    f.write(each)
		f.close()
		self.master.destroy()
	    elif data["type"]=="delete":
		self.master.destroy()
