from Tkinter import *
from ttk import *
import time
import threading
import thread
import tkFont
import subprocess
#from Run import bill_change_delay
#print bill_change_delay

rows=0
fb=0
gb=0
to_write=0
ColoR='blue'
counting=0
#customFont = tkFont.Font(family="Helvetica", size=12)
#customFont1 =tkFont.Font(family="Helvetica", size=12 , overstrike=True)
customFont=0
customFont1=0
No_of_Windows=0

#To change the switching delay
g=open('settings.txt','r')
f=g.read()
h=f.replace(' ','\n')
h=h.replace('\r','\n')
h=h.split('\n')
bill_change_delay = float(h[h.index('bcDelay') + 2])
print(bill_change_delay)

def firstthread():
	global counting
	while(True):
		time.sleep(bill_change_delay)
		counting=counting+1

class Threading(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.i=0
    def run(self):
        global counting
        while(True):
            time.sleep(1)
            self.i=self.i+1
            counting=self.i

def secondthread():
	global rows
	while(True):
		time.sleep(0.5)
		number=counting%len(rows)
		for i in range(0,len(rows)):
			try:
				rows[i].configure(background='')
			except:
				pass
			if number==i:
				try:
					rows[i].configure(background=ColoR)
				except:
					pass
					

def clickevent(master):
	global to_write
	i=counting%len(rows)
	if i==0:
		wr=open('Bill.txt','w')
		for j in to_write:
			if j==to_write[-1]:
				wr.write(j)
			else:
				wr.write(j+'\n')
		wr.close()
#		subprocess.call('Print.exe')
		master.destroy()
	elif i==len(rows)-1:
		wr=open('Bill.txt','w')
		wr.close()
		master.destroy()
	else:
		
		to_write.remove(rows[i]["text"])
		rows[i].configure(foreground='red')

def thirdthread(master):
	while(True):
		time.sleep(0.2)
		try:
			master.bind('<1>',lambda e:clickevent(master))
		except:
			pass
class ModifyBill(Frame):
	
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent=parent
		self.initUI(parent)
			
		
	def initUI(self,parent):
		global rows
		global gb
		global fb
		global to_write
		##############################3
		gb=open('Bill.txt','r')
		fb=gb.read()
		gb=fb.replace(' ','\n')
		fb=fb.split('\n')
		gb=gb.split('\n')
#print f
		rows=(len(fb)+1)*[0]
		rows.pop()
		fb.pop()
		to_write=fb
		
		##############################3
		self.parent.title("Finalize Bill ?")
#		Style().configure("TFrame")
#		self.style=Style()
		self.columnconfigure(0,weight=1)
#		self.rowconfigure(0,weight=1)
		self.pack(fill=BOTH,expand=1)
		Label(self,text='').grid(row=0,column=0,padx=5,pady=5)
		for i in range(1,len(fb)):
			rows[i]=Label(self,text=fb[i],font=customFont)
			rows[i].grid(row=i,column=0,columnspan=5,padx=5,pady=5)
		Label(self,text='').grid(row=len(fb),column=0,padx=5,pady=5)
		rows[0]=Label(self,text="Print",font=customFont)
		rows[0].grid(row=len(fb)+2,column=0,padx=5,pady=5)
		rows[len(fb)]=Label(self,text="Delete",font=customFont)
		rows[len(fb)].grid(row=len(fb)+1,column=0,padx=5,pady=5)
		thread.start_new_thread(secondthread,())	
		thread.start_new_thread(thirdthread,(parent,))




root=Tk()
root.geometry('300x300+400+200')
thread.start_new_thread(firstthread,())
app=ModifyBill(root)
root.mainloop()
