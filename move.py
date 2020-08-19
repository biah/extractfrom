#Imported modules
import shutil
from os import walk, path
from datetime import datetime as dt
class Move:
	"""This is the class which handles the moving of files to the desired location"""
	def __init__(self, filetypes, source, destination):
		self.filetypes = filetypes
		self.source = source
		self.destination = destination


	def move(self):

		def valid(filepath):
			#This method checks to see if a file is valid by comparing it's extension to that of the user's own
			#If the extension of the filetype is inside filetypes, it is then moved to the copy function

			self.filetypes = list(self.filetypes)
			if path.splitext(filepath)[-1] in self.filetypes:
				try:
					shutil.copy(filepath, self.destination)
				except Exception as e:
					file = open("logs\\logs.txt", "a")
					time = str(dt.now()[:-7])
					file.write(time+"\n"+e)
					file.close()
					pass


		for root, folder, files in walk(self.source):
				for filename in files:
					filepath = path.join(root, filename)
					valid(filepath)
