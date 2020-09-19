"""
Written in Python 3.8.5
Windows
This is a simple program to extract certain file types from a disk or directory"""

#Imported modules
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from os import remove
import worklist
import worker
import time
from ttkwidgets import linklabel as link
import binary
#Code

binary.icons_creator()

root = Tk()
root.title("Extract From")
root.iconbitmap('icons/icon.ico')
number = 1
menubar = Menu(root)

#Loading of icons and images
queue_button_image = PhotoImage(file = 'icons/add_to_queue.png')
start_button_image = PhotoImage(file = 'icons/start.png')
#Class
class Menubar:
	def __init__(self, menubar):
		self.menubar = menubar

	def show():
		#The show command is for showing the queue list to the user,
		#When the queue list is active and the user activates it again, it will not pop up another window but rather set focus on the existing
		worklist.show()
			

	def about():
		def show_about():
			global top
			top = Toplevel()
			top.title('about')
			top.iconbitmap('icons/icon.ico')
			top.resizable(width = False, height = False)
			heading_label = Label(top, text = 'ExtractFrom', font = ('Times New Roman', 20, 'bold'), fg = 'green').grid(row = 0, column = 0)
			text_label = Label(top, text = '''Version : 0.1.0 Beta\nExtractFrom is a free and open source program that uses extension-based file identification\n to extract files from directories and compressed files.\nLink to source code can be found at my website.
							''', font = ('Times New Roman', 12,'italic')).grid(row = 1, column = 0)
			website_label = Label(top, text = 'Website:', font = ('Times New Roman', 12, 'italic')).grid(row = 2, column = 0, sticky =W, padx = 140)
			website_label_website = link.LinkLabel(top, text = 'http://www.eakloe.com/extractfrom/index.html', font = ('Times New Roman', 12, 'italic'))
			website_label_website.grid(row = 2, column = 0, sticky =W, padx = 200)
		try:
			if top.state() == 'normal':
				top.destroy()
		except:
			show_about()
	def main(self):
		menu = Menu(self.menubar, tearoff = 0)
		menu.add_command(label = 'View Queue List', command = Menubar.show)
		menu.add_command(label = 'About', command = Menubar.about)
		menu.add_separator()
		menu.add_command(label = 'Quit', command = lambda : root.destroy())
		self.menubar.add_cascade(label = 'More...', menu = menu)


#Functions
def add_function():
	global number
	file_types = h_extract_dropdown_variable.get() #This is the file types to select
	source = h_from_dropdown_variable.get()
	from_directory = extract_from_entry_variable.get()
	to_directory = extract_to_entry_variable.get()
	mode = extract_mode.get()
	if file_types == '__________':
		messagebox.showerror(title = 'Error', message = 'You must select the file types to extract')
		return False
	elif source == '__________':
		messagebox.showerror(title = 'Error', message = 'You must select the source of the extraction')
		return False
	elif from_directory == '':
		messagebox.showerror(title = 'Error', message = 'You did not select the directory for the extraction')
		return False
	elif to_directory == '':
		messagebox.showerror(title = 'Error', message = 'You must select where I will extract the files to')
		return False
	elif file_types == 'File':
		contents = file_ext_variable.get() #If the user chooses file,  this will fetch the file_ext_entry contents
		if len(contents) <= 0:
			messagebox.showerror(title = 'Error', message = 'You have to enter a file extension')
			return False
		else:
			worklist.tasklist.append([str(number), contents, source, from_directory, to_directory, mode])
			number += 1
			worklist.update()
			return True
	else:
		worklist.tasklist.append([str(number), file_types, source, from_directory, to_directory, mode])
		number += 1
		worklist.update()
		return True

		

def start():
	"""This is the function which starts the whole process, on activation, it reads from the worklist tasklist variable 
	and starts executing commands"""
	global num
	global progress_bar
	num = 0
	if add_function() == True:
		tasks = worklist.tasklist
		def command():
			global num
			for i in tasks:
				process = worker.Worker(*i)
				process.start()
				num += 1
		

		process_thread = worker.threading.Thread(target = command)
		process_thread.start()
		
		top = Toplevel()
		start_button.configure(state = 'disabled')
		progress_bar = ttk.Progressbar(top, mode = 'determinate', maximum = len(tasks))
		progress_bar.grid(row = 0, column = 0, sticky = W+E)
		top.grid_columnconfigure(0, weight = 1)
		top.resizable(width = False, height = False)
		top.geometry('250x100')
		top.iconbitmap('icons/icon.ico')
		def callback():
			global num
			while process_thread.is_alive() == True:
				progress_bar.configure(value = num)
			worklist.tasklist.clear()
			worklist.delete_all()
			top.destroy()
			start_button.configure(state = 'normal')

		callback_thread = worker.threading.Thread(target = callback)
		callback_thread.start()


	else:
		print('Cannot start')

def callback(*args):
	#The main reason for the callback function is to enable the addition and removal of the file extension label and entry at row 1
	choice = h_extract_dropdown_variable.get()
		
	if choice == 'File':
		global file_ext_entry
		global file_ext_label
		file_ext_label = Label(root, text = 'File Extension:', font = b_font)
		file_ext_label.grid(row = 1, column = 0)
		file_ext_entry = ttk.Entry(root, width = 20, textvariable = file_ext_variable)
		file_ext_entry.grid(row = 1, column = 1, sticky = W+E, ipadx = 20)
	else:
		try:
			file_ext_entry.grid_forget()
			file_ext_label.grid_forget()
			pass
		except NameError as e:
			pass


def from_callback(*args):
	#This is a callback which is activated when a user chooses an option from the 'From' dropdown

	choice = h_from_dropdown_variable.get()

	if choice == '7z':
		#This changes the select directory text on the extract_from_button to 'Select rar'
		#And also, it changes the function of its command
		def select_7z():
			rar_file = filedialog.askopenfilename(title = 'Select 7z File', filetypes = (('7z File', '*.7z'), ('All files', '*.*')))
			if len(rar_file) >= 1:
				if rar_file[-2:] != '7z':
					messagebox.showerror(title = 'Error', message = 'This is not a 7z file.\nYou must select a 7z file.')
					select_rar()
				else:
					extract_from_entry_variable.set(str(rar_file))
		extract_from_entry_variable.set('')
		extract_from_button.configure(text = 'Select 7z File', command = select_7z)
	elif choice == 'Zip':
		def select_zip():
			zip_file = filedialog.askopenfilename(title = 'Select Zip File', filetypes = (('Zip File', '*.zip'), ('All files', '*.*')))
			if len(zip_file) >= 1:
				if zip_file[-3:] != 'zip':
					messagebox.showerror(title = 'Error', message = 'This is not a zip file.\nYou must select a zip file.')
					select_zip()
				else:
					extract_from_entry_variable.set(str(zip_file))
		extract_from_entry_variable.set('')
		extract_from_button.configure(text = 'Select Zip File', command = select_zip)
	elif choice == 'Directory':
		extract_from_entry_variable.set('')
		extract_from_button.configure(text = 'Select Directory', command = extract_from_dir)


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
file_ext_variable = StringVar()

#Font
h_font = ('square kids', 22) #The heading font
b_font = ('Budmo Jiggler', 15)

h_frame = Frame(root) #The heading frame
h_extract_label = Label(h_frame, text = 'Extract', font = h_font, fg = 'blue').grid(row = 0, column = 0) #The heading 'extract' label
h_extract_dropdown = ttk.OptionMenu(h_frame, h_extract_dropdown_variable,'__________','File', 'Pictures','Audios','Videos','Documents', command = callback).grid(row = 0, column = 1) #The heading extract dropdown
h_from_label = Label(h_frame, text = 'from', font = h_font, fg = 'green').grid(row = 0, column = 2) #The heading 'from' label
h_from_dropdown = ttk.OptionMenu(h_frame, h_from_dropdown_variable,'__________','Directory' ,'7z', 'Zip', command = from_callback).grid(row = 0, column = 3)
h_from_dropdown_variable.set('Directory')

#Body

extact_from_label = Label(root, text = 'Extract From:', font = b_font).grid(row = 2, column = 0, pady = 10)
extract_from_entry = ttk.Entry(root, state = 'readonly', textvariable = extract_from_entry_variable, width = 30).grid(row = 2, column = 1)
extract_from_button = ttk.Button(root, text = 'Select Directory', command = extract_from_dir)
extract_from_button.grid(row = 2, column = 2)
h_frame.grid(row = 0, column = 0, columnspan = 3, ipady = 10, pady = 10)

extract_to_label = Label(root, text = 'Extract To:', font = b_font).grid(row = 3, column = 0, sticky = W)
extract_to_entry = ttk.Entry(root, textvariable = extract_to_entry_variable, state = 'readonly', width = 30).grid(row = 3, column = 1)
extract_to_button = ttk.Button(root, text = 'Select Directory', command = extract_to_dir).grid(row = 3, column = 2, padx = 5)

#Radio Buttons
radio_move = ttk.Radiobutton(root, text=  'Move', variable = extract_mode, value = 'move').grid(row = 4, column = 0)
radio_copy = ttk.Radiobutton(root, text = 'Copy', variable = extract_mode, value = 'copy').grid(row = 4, column = 1)
extract_mode.set('move')

#Add to Queue
add_to_queue_button = ttk.Button(root, text = 'Add to Queue', image = queue_button_image, compound = LEFT, command = add_function).grid(row = 5, column = 0, sticky = E, pady = 20)
start_button = ttk.Button(root, text = 'Start', command = start, image = start_button_image, compound = LEFT)
start_button.grid(row = 5, column = 1)
#Starting other things
menu_class = Menubar(menubar)
menu_class.main()

#End
root.resizable(width = False, height = False)
root.geometry('500x270')
root.config(menu = menubar)
root.mainloop()

#Removing of files
worker.shutil.rmtree('icons')