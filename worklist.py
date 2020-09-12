from tkinter import *
from tkinter import ttk

number = 0

tasklist = []


def Worklist():
    global treeview
    toplevel = Toplevel()
    toplevel.title('Queue List')
    treeview = ttk.Treeview(toplevel, columns = ( 'File type', 'extract from', 'from directory', 'to directory', 'mode'))
    treeview.grid(row = 0,column = 0, sticky = W+E+S+N)
    treeview.column('#0',  width = 30, minwidth = 30)
    treeview.column('File type', width = 175, minwidth = 175)
    treeview.column('extract from',  width = 175, minwidth = 175)
    treeview.column('from directory',  width = 175, minwidth = 175)
    treeview.column('to directory',  width = 175, minwidth = 175)
    treeview.column('mode',  width = 75, minwidth = 70)
    treeview.heading('#0', text ='No.')
    treeview.heading('File type', text =  'File type')
    treeview.heading('extract from', text =  'Extracting From')
    treeview.heading('from directory', text =  'Source Directory')
    treeview.heading('to directory', text = 'Dest. Directory')
    treeview.heading('mode', text = 'mode')
    v_scroll = Scrollbar(toplevel, orient = HORIZONTAL, command = treeview.xview)
    v_scroll.grid(row = 1, column = 0, sticky = W+E)
    treeview.configure(xscrollcommand = v_scroll.set)
    toplevel.grid_rowconfigure(0, weight = 1)
    toplevel.grid_columnconfigure(0, weight = 1)
    button = ttk.Button(toplevel, text = 'Remove').grid(row = 2, column = 0, sticky = W, padx = 20)
    
def show():
    Worklist()
    for i in tasklist:
        treeview.insert('', 'end', text = i[0], values = i[1:])