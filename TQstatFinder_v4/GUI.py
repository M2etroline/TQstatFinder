from tkinter import *
from runv2 import Check
from tkinter import scrolledtext 

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)
    
root=Tk()
root.title("TQstatFinder")

labelsearch1=Label(root, text='Search for:')
labelsearch1.pack()
e1=Entry(root,width=50)
e1.pack()
labelsearch2=Label(root, text='Ignore if includes:')
labelsearch2.pack()
e2=Entry(root,width=50)
e2.pack()



chance=IntVar()
value=IntVar()
percent=IntVar()
number=IntVar()
lab1=Label(root, text='Sort by:')
lab1.pack()
sort2 = Checkbutton(root,text='Value',variable=value,onvalue=1,offvalue=0)
sort2.pack()
sort1 = Checkbutton(root,text='Chance',variable=chance,onvalue=1,offvalue=0)
sort1.pack()



lab2=Label(root, text='Search for:')
lab2.pack()
search2 = Checkbutton(root,text='Number',variable=number,onvalue=1,offvalue=0)
search2.pack()
search1 = Checkbutton(root,text='Percent',variable=percent,onvalue=1,offvalue=0)
search1.pack()

valuesaved=0
chancesaved=0
percentsaved=0
numbersaved=0
root.update()

sort2.select()
sort1.deselect()
search2.select()
search1.deselect()

def Main():
   win=Tk()
   win.title('Result')

   text_area = scrolledtext.ScrolledText(win,  
                                      wrap = WORD,  
                                      width = 100,  
                                      height = 30,  
                                      font = ("Times New Roman", 
                                              12),)

   text_area.grid(column = 0, pady = 10, padx = 10) 
   text_area.insert(INSERT,Check(e1.get(),e2.get(),number.get(),value.get()))
   text_area.configure(state ='disabled') 

myButton=Button(root,text='Run',command=Main)
myButton.pack()
 
while True:
   try:
      if (valuesaved!=value.get()):
         if value.get()==1:
            sort1.deselect()
         valuesaved=value.get()
           
      if (chancesaved!=chance.get()):
         if chance.get()==1:
            sort2.deselect()
         chancesaved=chance.get()
           
      if (percentsaved!=percent.get()):
         if percent.get()==1:
            search2.deselect()
         percentsaved=percent.get()
           
      if (numbersaved!=number.get()):
         if number.get()==1:
            search1.deselect()
         numbersaved=number.get()
      if (value.get() == 0) and (chance.get() == 0):
         sort2.select()
      if (percent.get() == 0) and (number.get() == 0):
         search2.select()
           
      root.update()
   except:
      break

