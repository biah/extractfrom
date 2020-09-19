"""This is the worker class, it is responsible for handling all the tiring and difficult work. It is also the base of the application
    Note:
    Whenever an operation is completed, the valid paths must be cleared. If not, it will be added to the next operation.
"""

#Imported modules
import shutil
import os
from datetime import datetime as dt
import subprocess
import tempfile #This module is required for making tempoary files and folders
import threading
from configparser import ConfigParser

configuration = ConfigParser()

#Tempoary folder
temporary_folder = tempfile.TemporaryDirectory()




def write_configuration():
    global PICTURES
    global AUDIOS
    global VIDEOS
    global DOCUMENTS
    #This is the function responsible for creating a configuration if it doesn't exist.
    #It handles everything about the configuration
    PICTURES = ['.jpg','.jif','jfif','.jpe', '.png', '.ico', '.jpeg','.gif', '.tiff','.vda','.vst','.tif','.icb','.icns','.webp', '.ppm','.pgm', '.pnm', '.pbm', '.tga', '.pcx', '.jp2','.j2k', '.jpf','jpx','jpm','mj2', 'raw', 'bmp', 'xpm']
    AUDIOS = ['.mp3','.m4r', '.wav','.m4p','m4a', '.pcm','.aiff','.aif', '.aac', '.ogg', '.wma', '.flac', '.alac','.aifc', '.3ga', '.aa','.act', '.al','.bap','.cda','.mp2','.mpa','.oga']
    VIDEOS = ['.mp4','.m4b','.avi','.qt','.mov','.wmv','.flv','.avchd','.webm','.mkv','.ogv','.dirac', '.mpg', '.mpeg','.3gp','.nsv','.3g2','.svi','.m4v']
    DOCUMENTS = ['.txt', '.pdf', '.doc', '.docx','.odt','.tex','.wpd','.md', '.rtf']
    configuration['file types'] = {
        'PICTURES' : PICTURES,
        'AUDIOS' : AUDIOS,
        'VIDEOS' : VIDEOS,
        'DOCUMENTS' : DOCUMENTS
    }
    
    with open('configuration.ini', 'w') as file:
        configuration.write(file)

#Setting the configuration
try:
    configuration.read('configuration.ini')
#File extensions
except:
    write_configuration() 
try:
    PICTURES = configuration['file types'].get('PICTURES')
    AUDIOS = configuration['file types'].get('AUDIOS')
    DOCUMENTS = configuration['file types'].get('DOCUMENTS')
    VIDEOS = configuration['file types'].get('VIDEOS')
except KeyError:
    write_configuration()
#Main work

valid_paths = []

class Worker:
    """The class which does all the work"""
    def __init__(self,number,  file_types, source, from_directory, to_directory, mode):
        self.number = number
        self.file_types = file_types
        self.source = source
        self.from_directory = from_directory
        self.to_directory = to_directory
        self.mode = mode

        #This then changes the file types into a list of extensions for the method 'valid' to use to check
        #if a file extension is valid or not
        if self.file_types == 'Pictures':
            self.file_types = PICTURES
        elif self.file_types == 'Audios':
            self.file_types = AUDIOS
        elif self.file_types == 'Videos':
            self.file_types = VIDEOS
        elif self.file_types == 'Documents':
            self.file_types = DOCUMENTS
        else:
            self.file_types = self.file_types #This refers to the file extensions the user defined by themselves
            print(self.file_types)
    def valid(self, path):
        #This is the method which checks to see if a generated file path is valid
        #It compares the extension of the generated file to self.source.
        #If the file extension is in self.soucre, the valid will return True. Else False
        print(os.path.splitext(path)[1])
        if os.path.splitext(path)[1] in self.file_types:
            if os.path.splitext(path)[1] != '':
                return True
        else:
            return False


    def move(self):
        if self.source == 'Directory':
            for root, folder, file in os.walk(self.from_directory):
                for filename in file:
                    path = os.path.join(root, filename)
                    if Worker.valid(self, path) == True:
                        valid_paths.append(path) #This list contains a number of paths which are valid
                for i in valid_paths: #Then this iterates through the valid paths and move them
                    try:
                        shutil.move(i, self.to_directory)
                    except Exception as message:
                        file = open("logs.txt", "a")
                        print('Error: ',message)
                        time = str(dt.now())[:-7]
                        file.write(time+"\n"+str(message)+'\n')
                        file.close()
                valid_paths.clear()
        elif self.source == 'Zip' or self.source == '7z': #7z makes everything easier so we just use the same alogorithmn for both
            #If the user's choice is a zip file...
            #The subprocess module is used to decompress the file into a tempoary place
            opening = subprocess.Popen(['7z', 'e', '-y', self.from_directory, '-o'+temporary_folder.name+'\\'], stderr = subprocess.PIPE, stdout = subprocess.PIPE, stdin = subprocess.PIPE) 
            output = opening.stdout.read().decode().lower() #This is the output read from stdout
            if 'everything is ok' in output: #7z always include 'Everything is Ok' when the process is successful, so i use that to see if everything really went well
                print('Sucessfull')
                for root, folder, file in os.walk(temporary_folder.name):
                    for filename in file:
                        path = os.path.join(root, filename)
                        if Worker.valid(self, path) == True:
                            valid_paths.append(path) #This list contains a number of paths which are valid
                    for i in valid_paths: #Then this iterates through the valid paths and move them
                        try:
                            shutil.move(i, self.to_directory)
                        except Exception as message:
                            file = open("logs.txt", "a")
                            print('Error: ',message)
             
                #In move, the files moved out of the compressed file, shouldn't be found back in the file again.
                #First of all, the user selects his files, then the compressed file is extracted to a temp folder.
                #The user's files are move from the tempoary folder. The original zip file will be deleted and will be replaced by the tempoary foler compressed in the same name as the original
                os.remove(self.from_directory) #This deletes the original zip file.
                converting = subprocess.Popen(['7z', 'a', self.from_directory, temporary_folder.name+'\\*']) #This command converts the tempoary file into a zip file with the same file name
                valid_paths.clear()
    def copy(self):
        if self.source == 'Directory':
            for root, folder, file in os.walk(self.from_directory):
                for filename in file:
                    path = os.path.join(root, filename)
                    if Worker.valid(self, path) == True:
                        valid_paths.append(path) #This list contains a number of paths which are valid
                for i in valid_paths: #Then this iterates through the valid paths and move them
                    try:
                        shutil.copy(i, self.to_directory)
                    except Exception as message:
                        file = open("logs.txt", "a")
                        print('Error: ',message)
                        time = str(dt.now())[:-7]
                        file.write(time+"\n"+str(message)+'\n')
                        file.close()
                valid_paths.clear() #This is very important. Whenever an operation is completed. If the valid paths are not cleared. It will be appended to the next operation. And that will cause a BUG!!!
        elif self.source == 'Zip' or self.source == '7z': #7z makes everything easier so we just use the same alogorithmn for both
            #If the user's choice is a zip file...
            #The subprocess module is used to decompress the file into a tempoary place
            opening = subprocess.Popen(['7z', 'e', '-y', self.from_directory, '-o'+temporary_folder.name], shell= True, stderr = subprocess.PIPE, stdout = subprocess.PIPE, stdin = subprocess.PIPE) 
            output = opening.stdout.read().decode().lower() #This is the output read from stdout
            if 'everything is ok' in output: #7z always include 'Everything is Ok' when the process is successful, so i use that to see if everything really went well
                print('Sucessfull')
                print(output)
                for root, folder, file in os.walk(temporary_folder.name):
                    for filename in file:
                        path = os.path.join(root, filename)
                        if Worker.valid(self, path) == True:
                            valid_paths.append(path) #This list contains a number of paths which are valid
                    for i in valid_paths: #Then this iterates through the valid paths and move them
                        try:
                            shutil.copy(i, self.to_directory)
                        except Exception as message:
                            file = open("logs.txt", "a")
                            print('Error: ',message)
                temporary_folder.cleanup()
                valid_paths.clear()

    def start(self):
        #This is the method which starts everything
        if self.mode == 'move':      
            Worker.move(self)
            return True


        elif self.mode == 'copy':
            Worker.copy(self)
            return True
            












#process = Worker('1', '.jeta', 'Directory', r'C:\Users\Lucretius\Desktop\Music', r'C:\Users\Lucretius\Desktop\pics', 'copy')
#process.start()