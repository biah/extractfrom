from tkinter import *
from tkinter import messagebox
class More:
	



	def about():
		messagebox._show(title = "About", message = "ExtractFrom\nVersion : 0.0.1\nWebsite : www.eakloe.com/extractfrom/index.html\nRelease Date: 19/08/2020 ")





	def more_menu(root, menubar):
		more_menu = Menu(menubar, tearoff = 0)
		more_menu.add_command(label = "About", command = More.about)
		menubar.add_cascade(label = "More...", menu = more_menu)
	

def main(root, menubar):
	More.more_menu(root, menubar)