"""
Written in Python 3.8.5
Windows
This is a simple program to extract certain file types from a disk or directory"""


#Imported modules
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from move import Move
from tkinter import messagebox
import icons
from os import remove
import worklist
#Code
root = Tk()
root.title("Extract From")
root.iconbitmap("icon.ico")
number = 1
menubar = Menu(root)
#Loading of icons and images
queue_image = PhotoImage(file = 'icons/add_to_queue.png')


#Class
class Menubar:
	def __init__(self, menubar):
		self.menubar = menubar

	def main(self):
		menu = Menu(self.menubar, tearoff = 0)
		menu.add_command(label = 'View Queue List', command = worklist.show)
		self.menubar.add_cascade(label = 'Menu', menu = menu)


#Functions
def add_fucntion():
	global number
	file_types = h_extract_dropdown_variable.get() #This is the file types to select
	source = h_from_dropdown_variable.get()
	from_directory = extract_from_entry_variable.get()
	to_directory = extract_to_entry_variable.get()
	mode = extract_mode.get()
	if file_types == '__________':
		messagebox.showerror(title = 'Error', message = 'You must select the file types to extract')
	elif source == '__________':
		messagebox.showerror(title = 'Error', message = 'You must select the source of the extraction')
	elif from_directory == '':
		messagebox.showerror(title = 'Error', message = 'You did not select the directory for the extraction')
	elif to_directory == '':
		messagebox.showerror(title = 'Error', message = 'You must select where I will extract the files to')
	else:
		worklist.tasklist.append([number, file_types, source, from_directory, to_directory, mode])
		number += 1
		

def start():
	#This is the function which activates the main work
	file_types = h_extract_dropdown_variable.get() #This is the file types to select
	source = h_from_dropdown_variable.get()
	from_directory = extract_from_entry_variable.get()
	to_directory = extract_to_entry_variable.get()
	if file_types == '__________':
		messagebox.showerror(title = 'Error', message = 'You must select the file types to extract')
	elif source == '__________':
		messagebox.showerror(title = 'Error', message = 'You must select the source of the extraction')
	elif from_directory == '':
		messagebox.showerror(title = 'Error', message = 'You did not select the directory for the extraction')
	elif to_directory == '':
		messagebox.showerror(title = 'Error', message = 'You must select where I will extract the files to')

def callback(*args):
	#The main reason for the callback function is to enable the addition and removal of the file extension label and entry at row 1
	choice = h_extract_dropdown_variable.get()
		
	if choice == 'File':
		global file_ext_entry
		global file_ext_label
		file_ext_label = Label(root, text = 'File Extension:', font = b_font)
		file_ext_label.grid(row = 1, column = 0)
		file_ext_entry = ttk.Entry(root, width = 20)
		file_ext_entry.grid(row = 1, column = 1, sticky = W+E, ipadx = 20)
	else:
		try:
			file_ext_entry.grid_forget()
			file_ext_label.grid_forget()
			pass
		except NameError as e:
			pass
			




def extract_from_dir():
	directory = filedialog.askdirectory()
	extract_from_entry_variable.set(str(directory))

def extract_to_dir():
	#This is the fucnction which sets the destination of the files to be extracted
	directory = filedialog.askdirectory()
	extract_to_entry_variable.set(str(directory))

#List

#Variables
h_extract_dropdown_variable = StringVar()
h_from_dropdown_variable = StringVar()
extract_from_entry_variable = StringVar()
extract_to_entry_variable = StringVar()
extract_mode = StringVar()

#Font
h_font = ('square kids', 22) #The heading font
b_font = ('Budmo Jiggler', 15)

h_frame = Frame(root) #The heading frame
h_extract_label = Label(h_frame, text = 'Extract', font = h_font, fg = 'blue').grid(row = 0, column = 0) #The heading 'extract' label
h_extract_dropdown = ttk.OptionMenu(h_frame, h_extract_dropdown_variable,'__________','File', 'Pictures','Audios','Videos','Documents', command = callback).grid(row = 0, column = 1) #The heading extract dropdown
h_from_label = Label(h_frame, text = 'from', font = h_font, fg = 'green').grid(row = 0, column = 2) #The heading 'from' label
h_from_dropdown = ttk.OptionMenu(h_frame, h_from_dropdown_variable, '__________','Rar', 'Zip','Directory').grid(row = 0, column = 3)


#Body

extact_from_label = Label(root, text = 'Extract From:', font = b_font).grid(row = 2, column = 0, pady = 10)
extract_from_entry = ttk.Entry(root, state = 'readonly', textvariable = extract_from_entry_variable, width = 30).grid(row = 2, column = 1)
extract_from_button = ttk.Button(root, text = 'Select Directory', command = extract_from_dir).grid(row = 2, column = 2)
h_frame.grid(row = 0, column = 0, columnspan = 3, ipady = 10, pady = 10)

extract_to_label = Label(root, text = 'Extract To:', font = b_font).grid(row = 3, column = 0, sticky = W)
extract_to_entry = ttk.Entry(root, textvariable = extract_to_entry_variable, state = 'readonly', width = 30).grid(row = 3, column = 1)
extract_to_button = ttk.Button(root, text = 'Select Directory', command = extract_to_dir).grid(row = 3, column = 2, padx = 5)

#Radio Buttons
radio_move = ttk.Radiobutton(root, text=  'Move', variable = extract_mode, value = 'move').grid(row = 4, column = 0)
radio_copy = ttk.Radiobutton(root, text = 'Copy', variable = extract_mode, value = 'copy').grid(row = 4, column = 1)
extract_mode.set('move')

#Add to Queue
add_to_queue_button = ttk.Button(root, text = 'Add to Queue', image = queue_image, compound = LEFT, command = add_fucntion).grid(row = 5, column = 0, sticky = E, pady = 20)
start_button = ttk.Button(root, text = 'Start', command = start).grid(row = 5, column = 1)


#Starting other things
menu_class = Menubar(menubar)
menu_class.main()
#End
root.resizable(width = False, height = False)
root.config(menu = menubar)
root.mainloop()