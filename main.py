"""This is a simple program to extract certain file types from a disk or directory"""


#Imported modules
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from move import Move
from tkinter import messagebox
import more_menu
import icons
from os import remove
#Code
root = Tk()
root.title("Extract From")
root.iconbitmap("icon.ico")

menubar = Menu(root)
#Variables
frm = StringVar()
to = StringVar()
#Functions and commands
def extract_frm():
	directory = filedialog.askdirectory()
	frm.set(directory)
def extract_to():
	directory = filedialog.askdirectory()
	to.set(directory)

def extract():
	"""This is the function which collects all the data from here and sends it over to the move class"""
	extract_from_directory = frm.get()
	extract_to_directory = to.get()
	extensions = file_ext_ent.get()

	if len(extensions) < 1:
		messagebox.showerror(title = "Error", message = "You have to type in the extensions of the files you want to extract")
	elif len(extract_from_directory) < 1:
		messagebox.showerror(title= "Error", message = "Please select the directory from which the files will be extracted from.")
	elif len(extract_to_directory) < 1:
		messagebox.showerror(title = "Errror", message = "Please select the directory from which the files will be extracted to.")

	else:
		splitted_extension = extensions.split(",")
		command = Move(splitted_extension, extract_from_directory, extract_to_directory)
		command.move()

#Labels
file_ext_lbl = ttk.Label(root, text = "File Extensions :", font = ("Budmo Jiggler", 15))
xtract_frm_lbl = ttk.Label(root, text = "Extract From;", font = ("Budmo Jiggler", 15))
xtract_to_lbl = ttk.Label(root, text = "Extract To;", font = ("Budmo Jiggler", 15))

#Entries
file_ext_ent = ttk.Entry(root, width = 35)
xtract_frm_ent = ttk.Entry(root, state = "readonly", textvariable =  frm)
xtract_to_ent = ttk.Entry(root, state = "readonly", textvariable = to)

#Buttons
btn_xtract_from = ttk.Button(root, text = "Select Directory", command = extract_frm)
btn_xtract_to = ttk.Button(root, text = "Select Directory", command = extract_to)
btn_extract = ttk.Button(root, text = "Extract", width = 30, command = extract)
#Gridding system
	#Labels
file_ext_lbl.grid(row = 0, column = 0, sticky = "w")
xtract_frm_lbl.grid(row = 1, column = 0, pady = 8, sticky = "w")
xtract_to_lbl.grid(row = 2, column = 0, pady = 8, sticky = "w")
	#Entries
file_ext_ent.grid(row = 0, column = 1, columnspan = 2)
xtract_frm_ent.grid(row = 1, column = 1)
xtract_to_ent.grid(row = 2, column = 1)
	#Buttons
btn_xtract_from.grid(row = 1, column = 2, padx = 5)
btn_xtract_to.grid(row = 2, column = 2)
btn_extract.grid(row = 3, column = 0, pady = 20, padx = 50, columnspan =3, ipady = 3)

#Other requirements
more_menu.main(root, menubar)

#End
root.resizable(width = False, height = False)
root.configure(menu = menubar)
root.mainloop()
remove('icon.ico')