from tkinter import *
from tkinter import ttk

tasklist = [] #This empty list will contain all the tasks to execute. It contains information about the task to execute.

def remove_item():
        """For this part, it is quite confusing. When a user deletes an item from the list, it must also be removed from the 
        tasklist list variable. The only way to get the correct index of the removed treeview item is to concatenate it's values
        and used tasklist.index(values) to find the real index of the item so we can pop it out."""
        #This is the function which removes an item from the list
        item_id = treeview.selection()
        tasklist_id = treeview.item(item_id)
        number = tasklist_id['text']
        values = tasklist_id['values']
        newlist = []
        newlist.append(number)
        newlist.append(values[0])
        newlist.append(values[1])
        newlist.append(values[2])
        newlist.append(values[3])
        newlist.append(values[4])
        index_to_pop = tasklist.index(newlist)
        treeview.delete(item_id)
        tasklist.pop(index_to_pop)
        

def update():
        try:
            #This is the function which adds a task to the tasklist list variable  creating a queue of commands
            last_task = tasklist[-1]
            treeview.insert('', 'end', text = last_task[0], values = last_task[1:], tags = last_task[0])
        except NameError:
            pass
        except Exception as e:
            print(e)
            

def Worklist(): #This is the main  part of the window
    global treeview
    global toplevel
    toplevel = Toplevel() #The toplevel window
    toplevel.title('Queue List') #The title
    toplevel.iconbitmap('icons/icon.ico')
    remove_from_queue_button_image = PhotoImage(file = r'icons//remove.png') 
    toplevel.minsize(height = 250, width = 60)
    treeview = ttk.Treeview(toplevel, columns = ( 'File type', 'extract from', 'from directory', 'to directory', 'mode'))
    treeview.grid(row = 0,column = 0, sticky = W+E+S+N)
    treeview.bind('<<TreeviewSelect>>')
    treeview.column('#0',  width = 50, minwidth = 50)
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
    h_scroll = Scrollbar(toplevel, orient = VERTICAL, command = treeview.yview)
    h_scroll.grid(row = 0, column = 1, sticky = N+S)
    treeview.configure(xscrollcommand = v_scroll.set, yscrollcommand = h_scroll.set)
    toplevel.grid_rowconfigure(0, weight = 1)
    toplevel.grid_columnconfigure(0, weight = 1)
    remove_button = ttk.Button(toplevel, command = remove_item,image = remove_from_queue_button_image, text = 'Remove', compound = LEFT)
    remove_button.image = remove_from_queue_button_image
    remove_button.grid(row = 2, column = 0, sticky = W, padx = 25, pady = 5, ipady = 3)

    
def show():
    Worklist()
    for i in tasklist:
        treeview.insert('', 'end', text = i[0], values = i[1:], tags = i[0])

